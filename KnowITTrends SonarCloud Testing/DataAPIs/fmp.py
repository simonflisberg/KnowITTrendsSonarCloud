import requests

class fmpAPI:
    _current_api_key = 0
    _API_KEYS = [
        "rLtoT9btGbygbQemp541mkM6iZ8GJ2PZ", 
        "OE02vOLdSNDZgFrIKoOXBssRa69Dgpye", 
        "YuKZuxADK9tCTB9x2Cel9GnFhyqXgy6Q", 
        "XuhLndBAIgrgpAWCefK9G7qzI0Ntnj2a", 
        "1bksG3iaOygeYy4Z1rf5mLgNb2nCiHoJ"
    ]

    def __init__(self):
        pass

    def getNewAPIKey(self):
        self._current_api_key += 1
        return self._API_KEYS[self._current_api_key]

    def getStockKeyInfo(self, 
                        symbol: str,
                        requested_data: list = ["all"]
        ):
        """
        Sends an API call to fetch key stock info for a given stock symbol.
        
        Args:
            symbol (str): The stock ticker name of the stock to be queried
            requested_data (list): Option to only get some of the key info, place all requested data in a list. requested_data=["all"] includes all key info.
        
        Returns:
            out (json): Json string containing key info about the stock, including "decsription", "ceo", "image" (logotype), "industry", and more. 
                        More info about which keys are in the output: https://site.financialmodelingprep.com/developer/docs/companies-key-stats-free-api
        """
        url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={self._API_KEYS[self._current_api_key]}"

        try:
            response = requests.get(url)
            json_data = response.json()

            # Check if the response has the "Limit Reach" error
            if "Error Message" in json_data and "Limit Reach" in json_data["Error Message"]:
                # Switch to the next API key and retry
                self.getNewAPIKey()
                return self.getStockKeyInfo(symbol, requested_data)

            json_data = json_data[0] # remove the outer list to only include a json string

            if requested_data != ["all"]: # if only specific data is requested
                filtered_data = {key: json_data[key] for key in requested_data if key in json_data}

                if len(requested_data) == len(filtered_data): # check if all data was found
                    json_data = filtered_data
                else:
                    print("Error: All requested data was not found in Key Info. Returning all Key Info instead.")

            return json_data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching key stock info for '{symbol}' through API call: {e}")
            return {}

    def getStockPrice(self,
                      symbol: str,
                      start_date: str,
                      end_date: str):
        """
        Sends an API call to fetch the stock price for a given stock symbol, time interval and price types(s) and returns a json string with the data.

        Args:
            symbol (str): The stock ticker name of the stock to be queried
            start_date (str): The start date for the price data.
            end_date (str): The end date for the price data.
        
        Returns:
            out (json): Json string with a dictionary containing the queried price data.
            The dictionary will be in the following format: {date: [open, close, high, low], ...}
        """
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={start_date}&to={end_date}&apikey={self._API_KEYS[self._current_api_key]}"

        try:
            response = requests.get(url)
            json_data = response.json()

                        # Check if the response has the "Limit Reach" error
            if "Error Message" in json_data and "Limit Reach" in json_data["Error Message"]:
                # Switch to the next API key and retry
                self.getNewAPIKey()
                return self.getStockPrice(symbol, start_date, end_date)

            if "historical" not in json_data:
                print("No historical data available for this ticker.")
                return {}
    
            return json_data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching price data through API call: {e}")
            return {}
        
    def getStockKeyFigures(self,
                           symbol: str,
                           requested_data: list = ["all"]
        ):
        '''
        A method to send an API call for stock key figure data.
        Key figures are for the trailing twelve months.

        Args:
            symbol (str): The stock ticker name of the stock to be queried.
            requested_data (list): Option to only get some of the key figures, place all requested data in a list. requested_data=["all"] includes all key figures.
       
        Returns:
            out (json): Json string with a dictionary containing the queried key figures data.
        '''
        url = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={self._API_KEYS[self._current_api_key]}"

        try:
            response = requests.get(url)
            json_data = response.json()

            # Check if the response has the "Limit Reach" error
            if "Error Message" in json_data and "Limit Reach" in json_data["Error Message"]:
                # Switch to the next API key and retry
                self.getNewAPIKey()
                return self.getStockKeyFigures(symbol, requested_data)

            if not json_data or isinstance(json_data, dict) and "Error Message" in json_data:
                print(f"No key figures available for {symbol}.")
                return {}

            json_data = json_data[0] # remove the outer list to only include a json string

            if requested_data != ["all"]: # if only specific data is requested
                filtered_data = {key: json_data[key] for key in requested_data if key in json_data}

                if len(requested_data) == len(filtered_data): # check if all data was found
                    json_data = filtered_data
                else:
                    print("Error: All requested data was not found in Key Info. Returning all Key Info instead.")

            return json_data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching key figures data thorugh API call: {e}")
            return {}
        