import requests

class WorldBankAPI:
    
    def __init__(self):
        pass
    
    def fetch_macro_data(self, url: str) -> str:
        """
        Helper function to retrieve data from a given URL.
        Returns the response as a JSON string.
        Raises an exception if the request fails.
        """
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Returns JSON string
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")

    def get_inflation(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves the Consumer Price Index (CPI) data for inflation.
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/FP.CPI.TOTL?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)

    def get_unemployment(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves the unemployment rate data.
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SL.UEM.TOTL.ZS?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)

    def get_gdp(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves the Gross Domestic Product (GDP) data.
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)

    def get_interest_rates(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves lending interest rate data.
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/FR.INR.LEND?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)

    def get_government_debt(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves government debt data as a percentage of GDP.
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/GC.DOD.TOTL.GD.ZS?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)

    def get_population(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves total population data.
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.TOTL?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)

    def get_gdp_per_capita(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves GDP per capita data.
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.PCAP.CD?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)

    def get_fdi(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves Foreign Direct Investment (FDI) data.
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/BX.KLT.DINV.CD.WD?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)
    
    def get_gdp_growth_rate(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves GDP Growth Rate Data
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.KD.ZG?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)

    def get_life_expectancy_at_birth(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves life expectancy data.
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SP.DYN.LE00.IN?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)
    
    def get_poverty_rate(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves Poverty Headcount Ratio ($1.90/day)
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SI.POV.DDAY?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)
    
    def get_gini_index(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves Gini Index (Income Inequality)
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SI.POV.GINI?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)
    
    def get_forest_area(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves Forest Area (% of land area)
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/AG.LND.FRST.ZS?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)
    
    def get_renewable_energy(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves Renewable Energy Consumption (% of total)
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/EG.FEC.RNEW.ZS?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)
    
    def get_air_pollution(self, country_code: str, start_year: int, end_year: int) -> str:
        """
        Retrieves Air Pollution (PM2.5 concentration)
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/EN.ATM.PM25.MC.M3?date={start_year}:{end_year}&format=json"
        return self.fetch_macro_data(url)
    
    def get_country_info(self, country_code: str) -> str:
        """
        Retrieves general information about a country.
        """
        url = f"https://api.worldbank.org/v2/country/{country_code}?format=json"
        return self.fetch_macro_data(url)