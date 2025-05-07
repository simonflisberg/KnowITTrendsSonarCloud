from datetime import datetime
import requests

class FredApi:
    _API_KEY = "503742b1d5d17b81b1607c717bbd90e5"
    _BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

    def CallApi(self, 
                series_id: str,
                start_date: str,
    ):
        """
        Args:
            series_id (str): ID of the data series to be collected.
            start_date (str): Start date of the data, e.g. get data from start_date. 
                Format: 
                    "YYYY-MM-DD"

        Returns:
            out (json)
        """

        params = {
            "series_id": series_id,
            "api_key": self._API_KEY,
            "file_type": "json",
            "observation_start": start_date
        }

        try:
            response = requests.get(url=self._BASE_URL, params=params)
            data = response.json()

        except:
            data = {"Error":"Index out of range."}
        
        return data
    
    def getCommodity(self,
                     series_id: str,
                     start_date: str
    ):
        """
        Args:
            series_id (str): ID of the commodity.
                Accepted strings:
                    "copper"
                    "crude_oil"
                    "natural_gas"
            start_date (str): Start date of the data, e.g. get data from start_date. 
                Format: 
                    "YYYY-MM-DD"

        Returns:
            out (json)
        """
        
        json = self.CallApi(series_id=series_id, start_date=start_date)

        return json
    
    def getCommodityIndex(self,
                          series_id: str,
                          start_date: str
    ):
        """
        Returns the dates and prices of a commodity index.

        Args:
            series_id (str): ID of the index
                Accepted Strings:
                    "global_all_commodities"
            start_date (str): Start date of the data, e.g. get data from start_date. 
                Format: 
                    "YYYY-MM-DD"
        """

        json = self.CallApi(series_id=series_id, 
                            start_date=start_date)
        
        return json
    
    def getMajorCurrencyHistorical(self,
                                   series_id: str,
                                   start_date: str
    ):
        """
        Returns the dates and prices of a major currency pair (or USD/SEK).

        Args:
            series_id (str): ID of the index
            start_date (str): Start date of the data, e.g. get data from start_date. 
                Format:
                    "YYYY-MM-DD"
        """
        
        json = self.CallApi(series_id=series_id, 
                            start_date=start_date)
        
        return json