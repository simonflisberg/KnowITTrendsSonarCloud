import json
from DataAPIs.worldbank import WorldBankAPI
from Graph import Graph
import pandas as pd
from datetime import datetime
import os

class MacroData:
    _data_api = WorldBankAPI()
    _graph = Graph()

    def __init__(self):
        self.data_types = [
            'inflation',
            'unemployment',
            'gdp',
            'interest_rate',
            'government_debt',
            'gdp_per_capita',
            'fdi',
            'gdp_growth_rate',
            'population',
            'life_expectancy',
            'poverty_rate',
            'income_inequality',
            'forest_area',
            'renewable_energy',
            'air_pollution'
        ]

    def compileCountryData(self, country_code: str, data_type: str, start_year: int, end_year: int):
        """
        Queries the WorldBankAPI for a given country’s macroeconomic data based on the data_type.
        
        Args:
            country_code (str): The country code (e.g., 'US', 'DE').
            data_type (str): The type of macro data to fetch. Should be one of the values in self.data_types.
            start_year (int): The start year for the data.
            end_year (int): The end year for the data.
        
        Returns:
            dict: A dictionary containing the requested macroeconomic data.
        """
        # Format today’s date and construct cache file path
        today_str = datetime.today().strftime("%d%m%y")
        cache_dir = "cached_data"
        file_name = f"MacroData-{country_code}_{data_type}_{start_year}_{end_year}_fetched-{today_str}.json"
        file_path = os.path.join(cache_dir, file_name)

        # Return cached file if it exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)

        if data_type in self.data_types:
            try:
                if data_type == 'inflation':
                    data = self._data_api.get_inflation(country_code, start_year, end_year)
                elif data_type == 'unemployment':
                    data = self._data_api.get_unemployment(country_code, start_year, end_year)
                elif data_type == 'gdp':
                    data = self._data_api.get_gdp(country_code, start_year, end_year)
                elif data_type == 'interest_rate':
                    data = self._data_api.get_interest_rates(country_code, start_year, end_year)
                elif data_type == 'government_debt':
                    data = self._data_api.get_government_debt(country_code, start_year, end_year)
                elif data_type == 'gdp_per_capita':
                    data = self._data_api.get_gdp_per_capita(country_code, start_year, end_year)
                elif data_type == 'fdi':
                    data = self._data_api.get_fdi(country_code, start_year, end_year)
                elif data_type == 'gdp_growth_rate':
                    data = self._data_api.get_gdp_growth_rate(country_code, start_year, end_year)
                elif data_type == 'population':
                    data = self._data_api.get_population(country_code, start_year, end_year)
                elif data_type == 'life_expectancy':
                    data = self._data_api.get_life_expectancy_at_birth(country_code, start_year, end_year)
                elif data_type == 'poverty_rate':
                    data = self._data_api.get_poverty_rate(country_code, start_year, end_year)
                elif data_type == 'income_inequality':
                    data = self._data_api.get_gini_index(country_code, start_year, end_year)
                elif data_type == 'forest_area':
                    data = self._data_api.get_forest_area(country_code, start_year, end_year)
                elif data_type == 'renewable_energy':
                    data = self._data_api.get_renewable_energy(country_code, start_year, end_year)
                elif data_type == 'air_pollution':
                    data = self._data_api.get_air_pollution(country_code, start_year, end_year)

            except Exception as e:
                print(f"Error querying WorldBankAPI for country data: {e}")
                return {}
        else:
            raise ValueError(f"Invalid data type '{data_type}'. Valid types are: {self.data_types}")

        if not data or len(data) < 2:
            return {}

        data_points = data[1]
        if not data_points:
            return {}

        first_point = data_points[0]
        country = first_point.get("country", {}).get("value", "Unknown")
        explanation = first_point.get("indicator", {}).get("value", "No explanation available")
        
        historical = []
        for point in data_points:
            year_str = point.get("date")
            try:
                year = int(year_str)
            except (ValueError, TypeError):
                year = year_str 
            
            value = point.get("value")
            try:
                if value is not None:
                    value = float(value)
            except (ValueError, TypeError):
                value = None

            # Only include the data point if value is not None.
            if value is None:
                continue
            
            historical.append({"year": year, "value": value})
        
        country_data = {
            "country": country,
            "explanation": explanation,
            "historical": historical
        }

        if country_data['historical'] != []:
            trend = self._graph.getLinearTrend(datapoints=country_data, date_col="year", price_col="value", yearly=True)
        
            if isinstance(trend, str):
                trend = json.loads(trend) # ensure trend data is formatted as dict

            df_country = pd.DataFrame(country_data["historical"])
            df_trend = pd.DataFrame(trend)

            new = pd.merge(df_country, df_trend, on="year", how="left").to_dict(orient="records")

            json_data_incl_trend = {
                "country": country,
                "explanation": explanation,
                "historical": new
            }

            # Save result to file
            with open(file_path, "w") as f:
                json.dump(country_data, f, indent=2)
            
            return json_data_incl_trend
        
        else:
            # Save result to file
            with open(file_path, "w") as f:
                json.dump(country_data, f, indent=2)

            return country_data
        
    def compileCountryInfo(self, country_code):
        """
        Queries World Bank API and uses compileCountryData and returns a dictionary of general country info.
        
        Args:
            country_code (str): The country code (e.g., 'US', 'DE').
        
        Returns:
            country_data (dict): General country data.
        """
        data = self._data_api.get_country_info(country_code=country_code)

        country_name = data[1][0]['name']
        capital_city = data[1][0]['capitalCity']
        income_level = data[1][0]['incomeLevel']['value']
        longitude = data[1][0]['longitude']
        latitude = data[1][0]['latitude']


        population_data = self.compileCountryData(country_code=country_code, data_type='population', start_year=2015, end_year=2100)

        if population_data['historical'] != []:
            population = {'value': population_data['historical'][0]['value'], 'year': population_data['historical'][0]['year']}
        else:
            population = {'value': 'Unavailable', 'year': 'Unavailable'}
    
        life_expectancy_data = self.compileCountryData(country_code=country_code, data_type='life_expectancy', start_year=2015, end_year=2100)

        if life_expectancy_data['historical'] != []:
            life_expectancy = {'value': life_expectancy_data['historical'][0]['value'], 'year': life_expectancy_data['historical'][0]['year']}
        else:
            life_expectancy = {'value': 'Unavailable', 'year': 'Unavailable'}

        gdp_data = self.compileCountryData(country_code=country_code, data_type='gdp', start_year=2015, end_year=2100)

        if gdp_data['historical'] != []:
            gdp = {'value': gdp_data['historical'][0]['value'], 'year': gdp_data['historical'][0]['year']}
        else:
            gdp = {'value': 'Unavailable', 'year': 'Unavailable'}

        gdp_per_capita_data = self.compileCountryData(country_code=country_code, data_type='gdp_per_capita', start_year=2015, end_year=2100)

        if gdp_per_capita_data['historical'] != []:
            gdp_per_capita = {'value': gdp_per_capita_data['historical'][0]['value'], 'year': gdp_per_capita_data['historical'][0]['year']}
        else:
            gdp_per_capita = {'value': 'Unavailable', 'year': 'Unavailable'}


        gdp_growth_rate_data = self.compileCountryData(country_code=country_code, data_type='gdp_growth_rate', start_year=2015, end_year=2100)

        if gdp_growth_rate_data['historical'] != []:
            gdp_growth_rate = {'value': gdp_growth_rate_data['historical'][0]['value'], 'year': gdp_growth_rate_data['historical'][0]['year']}
        else:
            gdp_growth_rate = {'value': 'Unavailable', 'year': 'Unavailable'}

        interest_rate_data = self.compileCountryData(country_code=country_code, data_type='interest_rate', start_year=2000, end_year=2100)
    
        if interest_rate_data['historical'] != []:
            interst_rate = {'value': interest_rate_data['historical'][0]['value'], 'year': interest_rate_data['historical'][0]['year']}
        else:
            interst_rate = {'value': 'Unavailable', 'year': 'Unavailable'}

        country_data = {
            'country_name': country_name,
            'capital_city': capital_city,
            'income_level': income_level,
            'longitude': longitude,
            'latitude': latitude,
            'population': population,
            'life_expectancy': life_expectancy,
            'gdp_usd': gdp,
            'gdp_per_capita_usd': gdp_per_capita,
            'gdp_growth_rate': gdp_growth_rate,
            'interst_rate': interst_rate,
            'country_code': country_code
        }

        formatted_data = self.format_number(country_data)

        print(formatted_data)

        formatted_data['gdp_growth_rate']['value'] = float(formatted_data['gdp_growth_rate']['value'][:-1])

        return formatted_data
            
    def format_number(self, n, key=None):
        """
        Recursively formats numeric values in a nested data structure.
        If n is a dict, it formats each value (passing along the key for numbers);
        if it's a list, it processes each element.
        For numbers, the following suffixes are used:
            - T for values >= 1e12
            - B for values >= 1e9
            - M for values >= 1e6
        Numeric values that don't require suffix formatting and are integer-like
        are converted to ints to remove any trailing '.0'.
        Additionally, for numbers with absolute values between 1,000 and 100,000,
        a space is inserted as the thousands separator (e.g., 1 000, 10 000),
        unless the number is associated with the key 'year'.
        
        Args:
            n: A number, dict, list, or any other data type.
            key: The key associated with n (if applicable). Defaults to None.
            
        Returns:
            The data structure with all numeric values formatted as strings.
        """
        # Process dictionaries recursively.
        if isinstance(n, dict):
            return {k: self.format_number(v, key=k) for k, v in n.items()}
        
        # Process lists recursively.
        elif isinstance(n, list):
            return [self.format_number(item) for item in n]
        
        # Format numbers.
        elif isinstance(n, (int, float)):
            # Convert the number to have 4 significant figures.
            formatted = float(f"{n:.4g}")
            abs_n = abs(formatted)
            
            # Handle large numbers with suffixes.
            if abs_n >= 1e12:
                return f"{formatted / 1e12:.2f}T"
            elif abs_n >= 1e9:
                return f"{formatted / 1e9:.2f}B"
            elif abs_n >= 1e6:
                return f"{formatted / 1e6:.2f}M"
            else:
                # Default conversion: remove trailing '.0' for integer-like numbers.
                if formatted.is_integer():
                    result = str(int(formatted))
                else:
                    result = str(formatted)
                
                # For non-'year' keys, insert a space as the thousands separator
                # if the number is between 1,000 (inclusive) and 100,000 (exclusive).
                if key != "year" and abs_n >= 1000 and abs_n < 100000:
                    if '.' in result:
                        integer_part, fractional_part = result.split(".")
                        integer_part = f"{int(integer_part):,}".replace(",", " ")
                        result = f"{integer_part}.{fractional_part}"
                    else:
                        result = f"{int(formatted):,}".replace(",", " ")
                
                return result
        
        # Return any other type as-is.
        else:
            return n
