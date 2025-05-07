from DataAPIs.swissquote import swissquote # FX api by swissquote
from DataAPIs.FRED import FredApi
import json
import pandas as pd
from Graph import Graph
from datetime import datetime, timedelta
import os

class ForexData:
    _swissquote = swissquote()
    _fred_api = FredApi()
    _graph = Graph()
    
    _CURRENCY_PAIRS = {
        ("EUR", "USD"): "DEXUSEU",
        ("GBP", "USD"): "DEXUSUK",
        ("AUD", "USD"): "DEXUSAL",
        ("NZD", "USD"): "DEXUSNZ",
        ("USD", "JPY"): "DEXJPUS",
        ("USD", "CHF"): "DEXSZUS",
        ("USD", "CAD"): "DEXCAUS",
        ("USD", "SEK"): "DEXSDUS"
    }

    _CURRENCY_NAMES = {
        "EUR": "Euro",
        "USD": "US Dollar",
        "GBP": "British Pound",
        "AUD": "Australian Dollar",
        "NZD": "New Zealand Dollar",
        "JPY": "Japanese Yen",
        "CHF": "Swiss Franc",
        "CAD": "Canadian Dollar",
        "SEK": "Swedish Krona"
    }

    def getLivePair(self, 
                    base: str, 
                    quote: str
    ):
        """
        Returns the current (live) price of a forex pair.

        Args:
            base (str): The base currency, e.g. first currency in pair.
            quote (str): The quote currency, e.g. second currency in pair.

        Returns:
            out (json): contains bid, ask and respective spreads (0-spread server)
        """

        json_data = self._swissquote.getPairLive(base=base, 
                                     quote=quote
        )

        return json_data

    def getHistoricalMajorPair(self,
                               base: str,
                               quote: str,
                               start_date: str
    ):
        """
        Only request Major pairs.

        Returns the historical price of a forex pair.

        Args:
            base (str): The base currency, e.g. first currency in pair.
            quote (str): The quote currency, e.g. second currency in pair.
            start_date (str): Start date of the data, e.g. get data from start_date. 
                Format:
                    "YYYY-MM-DD"

        Returns:
            out (json):
        """
        
        if (base.upper().strip(), quote.upper().strip()) in self._CURRENCY_PAIRS:
            currency_pair_id = self._CURRENCY_PAIRS[(base, quote)]

            # Get current date in ddMMYY format
            today_str = datetime.today().strftime("%d%m%y")

            ### LOAD FROM FILE IF POSSIBLE

            # Define cache file name
            file_name = f"ForexData-{base}-{quote}_start-{start_date}_fetched-{today_str}.json"
            file_path = os.path.join("cached_data", file_name)
            
            # Check if cached file exists
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    cached_data = json.load(f)
                return cached_data
            
            ###
            
            data = self._fred_api.getMajorCurrencyHistorical(series_id=currency_pair_id,
                                                             start_date=start_date)
            data = self.formatFredData(data=data)

            # add pair name to json
            data["currency_pair_abbr"] = f"{base}/{quote}"
            data["currency_pair"] = f"{self._CURRENCY_NAMES[base]} / {self._CURRENCY_NAMES[quote]}"

            # Save to file
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)

            return data
        
        else:
            print("Error, currency pair not found.")

        return {"Error":404}
    
    def formatFredData(self,
                       data: dict
    ):
        """
        Formats and returns FRED currency data incl. trend.
        """

        formatted_data = {
            "observation_start": data["observation_start"],
            "observation_end": data["realtime_end"],
            "count": len([obs for obs in data["observations"] if obs["value"] != "."]),
            "historical": [
                {"date": obs["date"], "value": float(obs["value"])}
                for obs in data["observations"]
                if obs["value"] != "."  # Filter out missing values
            ]
        }

        if formatted_data["historical"]:
            values = [obs["value"] for obs in formatted_data["historical"]]
            high = max(values)  # Highest value in the entire period
            formatted_data["high"] = f"{high:.2f}"
            low = min(values)
            formatted_data["low"] = f"{low:.2f}"   # Lowest value in the entire period
            formatted_data["full_range"] = f"{low:.2f}-{high:.2f}"

            # Compute the 52-week range
            latest_date = datetime.strptime(formatted_data["historical"][-1]["date"], "%Y-%m-%d")
            one_year_ago = (latest_date - timedelta(weeks=52)).strftime("%Y-%m-%d")

            # Filter data from the last 52 weeks
            last_52w_data = [obs["value"] for obs in formatted_data["historical"] if obs["date"] >= one_year_ago]

            if last_52w_data:
                high52 = max(last_52w_data)  # Highest value in the last 52 weeks
                formatted_data["high_52w"] = f"{high52:.2f}"
                low52 = min(last_52w_data)
                formatted_data["low_52w"] = f"{low52:.2f}"   # Lowest value in the last 52 weeks
                formatted_data["range_52w"] = f"{low52:.2f}-{high52:.2f}"
            else:
                formatted_data["high_52w"] = None
                formatted_data["low_52w"] = None
                formatted_data["range_52w"] = None
        else:
            formatted_data["high"] = None
            formatted_data["low"] = None
            formatted_data["high_52w"] = None
            formatted_data["low_52w"] = None
            formatted_data["range_52w"] = None


        changes = self.calculate_changes(historical=formatted_data["historical"])
        
        for change in changes:
            formatted_data[change] = changes[change]

        trend = self._graph.getLinearTrend(formatted_data, price_col="value")
        
        if isinstance(trend, str):
            trend = json.loads(trend)

        df_historical = pd.DataFrame(formatted_data["historical"])
        df_trend = pd.DataFrame(trend)
        df_merged = pd.merge(df_historical, df_trend, on="date", how="left")
        formatted_data["historical"] = df_merged.to_dict(orient="records")

        formatted_data['change_1d'] = float(formatted_data['change_1d'][:-1])

        return formatted_data
    
    def get_closest_value(self, historical, target_date):
        """Find the closest value before or on the target date."""
        for obs in reversed(historical):  # Reverse to find closest earlier date
            if obs["date"] <= target_date:
                return obs["value"]
        return None  # Return None if no value is found
    
    def calculate_changes(self, historical):
        """Calculate percentage changes for 1d, 1w, 1m, 3m, 1y."""
        if not historical:
            return {}

        latest_value = historical[-1]["value"]
        latest_date = datetime.strptime(historical[-1]["date"], "%Y-%m-%d")

        time_deltas = {
            "1d": timedelta(days=1),
            "1w": timedelta(weeks=1),
            "1m": timedelta(days=30),
            "3m": timedelta(days=90),
            "1y": timedelta(days=365),
        }

        changes = {}
        for label, delta in time_deltas.items():
            past_date = (latest_date - delta).strftime("%Y-%m-%d")
            past_value = self.get_closest_value(historical, past_date)

            if past_value is not None:
                percentage_change = ((latest_value - past_value) / past_value) * 100
                changes[f"change_{label}"] = f"{percentage_change:.2f}%"
            else:
                changes[f"change_{label}"] = None  # No data available for this period

        return changes


if __name__ == "__main__":
    f = ForexData()
    #json_data = ForexData().getLivePair("USD", "SEK")
    #print({"USD/SEK":json_data})

    print(f.getHistoricalMajorPair("GBP", "USD", "2024-01-01"))