import json
from DataAPIs.FRED import FredApi
from Graph import Graph
import pandas as pd
from datetime import datetime, timedelta
from BananAI import BananAI
import os

class CommodityData:
    _data_api = FredApi()
    _graph = Graph()
    _bananai = BananAI()

    def __init__(self):
        with open("commodities.json", "r") as file:
            data = json.load(file)
            self._commodoties = self.flatten_two_layers(data["COMMODOTIES"])

    # index, old
    _GLOBAL_PRICE_INDEX_OF_ALL_COMMODITIES = "PALLFNFINDEXQ"

    def flatten_two_layers(self, nested_dict):
        """Flattens two layers of the nested dictionary structure."""
        flat_dict = {}
        for key, value in nested_dict.items():
            if isinstance(value, dict):  # If it's a dictionary, merge its contents
                flat_dict.update(value)
            else:
                flat_dict[key] = value
        return flat_dict

    def compileCommodityData(self,
                             commodity_id,
                             start_date
    ):
        commodity_id = commodity_id.upper()
        series_id = ""

        if commodity_id in self._commodoties:
            series_id = self._commodoties[commodity_id]["series_id"]

        else:
            json_data = {"Error":"ID out of Range."}
            return json_data
        
        ### CHECK IF CACHED

         # Get current date in ddMMYY format
        today_str = datetime.today().strftime("%d%m%y")

        # Define cache file name
        file_name = f"CommodityData_{commodity_id}_start-{start_date}_fetched-{today_str}.json"
        file_path = os.path.join("cached_data", file_name)
        
        # Check if cached file exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                cached_data = json.load(f)
            return cached_data
        
        ###

        json_data = self._data_api.getCommodity(series_id=series_id, start_date=start_date)

        if "error_code" in json_data:
            return json_data
        else:
            json_data = self.formatData(json_data=json_data, commodity_id=commodity_id)

        # Save to file
        with open(file_path, "w") as f:
            json.dump(json_data, f, indent=2)

        return json_data

    def compileCommodityIndex(self,
                              commodity_id: str,
                              start_date: str
    ):
        return self.compileCommodityData(commodity_id=commodity_id, start_date=start_date, index=True)

    def compileCommodityIndexOld(self,
                                 name: str,
                                 start_date: str):
        """
        Args:
            name (str): The name of the commodity index,
                Accepted names:
                    "global_all_commodities"
            start_date (str): The start date of the data to be fetched.
                Date format:
                    "YYYY-mm-dd"

        Returns:
            out (json)
        """
        if name == "global_all_commodities":
            json_data = self._data_api.getCommodityIndex(series_id=self._GLOBAL_PRICE_INDEX_OF_ALL_COMMODITIES,
                                                       start_date=start_date)
        else:
            json_data = {"Error":"Index out of range."}

        json_data = self.formatData(json_data=json_data)

        return json_data
    
    def addTrend(self, 
                 json_data: dict
    ):
        """
        Returns data with added trendline.
        """
        
        trend = self._graph.getLinearTrend(json_data, price_col="value")
        
        if isinstance(trend, str):
            trend = json.loads(trend)

        df_historical = pd.DataFrame(json_data["historical"])
        df_trend = pd.DataFrame(trend)
        df_merged = pd.merge(df_historical, df_trend, on="date", how="left")
        json_data["historical"] = df_merged.to_dict(orient="records")

        return json_data
    
    
    def addPrediction(self, 
                      json_data: dict
    ):
        """
        Returns data with added prediction and disclaimer.
        """
        
        prediction = self._bananai.GetCrazyBananasPrediction(json_data["historical"])
        prediction = prediction.removeprefix("```json")
        prediction = prediction.removesuffix("```")
        prediction = prediction.replace("\n", "")
        prediction = prediction.replace(f"\\", "")

        prediction = json.loads(prediction)

        json_data["ai_prediction"] = prediction

        return json_data

    def detectFrequency(self, 
                        observations
    ):
        """
        Determines the frequency of the dataset based on date differences.
        Returns 'Daily', 'Weekly', 'Monthly', or 'Yearly'.
        """
        if not observations or len(observations) < 2:
            return "Unknown"

        # Convert string dates to datetime objects
        dates = [datetime.strptime(obs["date"], "%Y-%m-%d") for obs in observations]

        # Calculate the average difference between consecutive dates
        diffs = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
        avg_diff = sum(diffs) / len(diffs)

        # Assign frequency based on the average difference
        if avg_diff <= 1.5:
            return "Daily"
        elif 6 <= avg_diff <= 8:
            return "Weekly"
        elif 28 <= avg_diff <= 32:
            return "Monthly"
        elif avg_diff > 300:
            return "Yearly"
        else:
            return "Unknown"
        
    def calculateRanges(self, observations):
        """
        Calculates full historical range and yearly (52-week) range.
        """
        if not observations:
            return {"full_range": None, "52w_range": None}

        # Convert observations to a sorted list of values
        prices = [float(obs["value"]) for obs in observations if obs["value"] != "."]
        prices.sort()

        # Calculate full range
        full_range = {"min": min(prices), "max": max(prices)}

        # Get date range for 52 weeks
        latest_date = datetime.strptime(observations[-1]["date"], "%Y-%m-%d")
        one_year_ago = latest_date - timedelta(weeks=52)

        # Filter observations within the past year
        yearly_prices = [
            float(obs["value"]) for obs in observations
            if datetime.strptime(obs["date"], "%Y-%m-%d") >= one_year_ago and obs["value"] != "."
        ]

        # Calculate 52-week range if enough data is available
        if yearly_prices:
            yearly_range = {"min": min(yearly_prices), "max": max(yearly_prices)}
        else:
            yearly_range = None

        return {"range": full_range, "range_52w": yearly_range}
    
    def get_yearly_data(self, observations):
        """
        Extracts observations for each available year in the dataset.

        Returns a dictionary where keys are years (e.g., "2023", "2022"),
        and values are in the same format as the main historical data.
        """
        if not observations:
            return {}

        # Organize data by year
        yearly_data = {}
        for obs in observations:
            if obs["value"] == ".":
                continue  # Skip missing values

            year = obs["date"][:4]  # Extract year as string (YYYY)
            month = int(obs["date"][5:7])  # Extract month as integer (1-12)

            if year not in yearly_data:
                yearly_data[year] = {
                    "observation_start": f"{year}-01-01",
                    "observation_end": f"{year}-12-31",
                    "historical": []
                }

            yearly_data[year]["historical"].append({"date": month, "value": float(self.format_number(float(obs["value"])))})

        return yearly_data

    def formatData(self, 
                   json_data: dict,
                   commodity_id: str,
                   index: bool = False
    ):
        ranges = self.calculateRanges(observations=json_data["observations"])

        # Get yearly data for the last two years
        yearly_data = self.get_yearly_data(observations=json_data["observations"])
        years = sorted(yearly_data.keys(), reverse=True)  # Sort years in descending order

        min_52w = self.format_number(ranges["range_52w"]["min"])
        max_52w = self.format_number(ranges["range_52w"]["max"])
        min_full_range = self.format_number(ranges["range"]["min"])
        max_full_range = self.format_number(ranges["range"]["max"])

        filtered_json = {
            "observation_start": json_data["observation_start"],
            "observation_end": json_data["realtime_end"],
            "count": json_data["count"],
            "range_52w": f"{min_52w} - {max_52w}",
            "range": f"{min_full_range} - {max_full_range}",
            "frequency": self.detectFrequency(json_data["observations"]),
            "commodity_id": commodity_id,
            "historical": [
                {"date": obs["date"], "value": float(obs["value"])} for obs in json_data["observations"]
            ],
        }

        dct = self._commodoties
        
        filtered_json["name"] = dct[commodity_id]["name"]
        filtered_json["name_full"] = dct[commodity_id]["name_full"]
        filtered_json["unit"] = dct[commodity_id]["unit"]
        filtered_json["type"] = dct[commodity_id]["type"]
        filtered_json["note"] = dct[commodity_id]["note"]
        filtered_json["citation"] = dct[commodity_id]["citation"]

        if len(years) >= 2:
            filtered_json["current_year"] = yearly_data[years[0]]
            filtered_json["previous_year1"] = yearly_data[years[1]]
            filtered_json["previous_year2"] = yearly_data[years[2]]
            filtered_json["current_year_name"] = years[0]
            filtered_json["previous_year1_name"] = years[1]
            filtered_json["previous_year2_name"] = years[2]
        elif len(years) == 1:
            filtered_json["current_year"] = yearly_data[years[0]]
            filtered_json["current_year_name"] = years[0]
            filtered_json["previous_year_1_name"] = yearly_data[years[1]]
            filtered_json["previous_year1_name"] = years[1]

        filtered_json = self.addTrend(json_data=filtered_json)

        filtered_json['change_1m'] = float(((filtered_json["historical"][-1]['value'] - filtered_json["historical"][-2]['value']) / filtered_json["historical"][-2]['value']) * 100)

        for obs in filtered_json["historical"]:
            obs["value"] = self.format_number(obs["value"])
            obs["trend"] = self.format_number(obs["trend"])

        filtered_json["change_1m"] = self.format_number(filtered_json["change_1m"])
        
        filtered_json = self.addPrediction(json_data=filtered_json)

        return filtered_json
    
    def format_number(self, n):
        """
        Recursively formats numeric values in a nested data structure.
        If n is a dict, it formats each value; if it's a list, it processes each element.
        For numbers, the following suffixes are used:
            - T for values >= 1e12
            - B for values >= 1e9
            - M for values >= 1e6
        Numeric values that don't require suffix formatting and are integer-like
        are converted to ints to remove any trailing '.0'.

        Args:
            n: A number, dict, list, or any other data type.

        Returns:
            The data structure with all numeric values formatted as strings.
        """
        # Process dictionaries recursively.
        if isinstance(n, dict):
            return {key: self.format_number(value) for key, value in n.items()}
        
        # Process lists recursively.
        elif isinstance(n, list):
            return [self.format_number(item) for item in n]
        
        # Format numbers.
        elif isinstance(n, (int, float)):
            formatted = float(f"{n:.4g}") # Convert to 4 value figures

            abs_n = abs(formatted)
            if abs_n >= 1e12:
                return f"{formatted / 1e12:.2f}T"
            elif abs_n >= 1e9:
                return f"{formatted / 1e9:.2f}B"
            elif abs_n >= 1e6:
                return f"{formatted / 1e6:.2f}M"
            else:
                # Check if the number is an integer to avoid trailing '.0'
                if formatted.is_integer():
                    return float(int(formatted))
                else:
                    return float(formatted)
        
        # Return any other type as-is.
        else:
            return float(n)
    
if __name__ == "__main__":
    c = CommodityData()
    print(c.compileCommodityData("bananas", "2010-01-01"))