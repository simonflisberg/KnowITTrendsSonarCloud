import requests

class swissquote:
    _FOREX_BASE_URL = "https://forex-data-feed.swissquote.com/public-quotes/bboquotes/instrument/"
    
    def __init__(self):
        pass

    def callForexApi(self, endpoint):
        try:
            url = self._FOREX_BASE_URL + endpoint
            response = requests.get(url=url)

        except:
            print("Error: Failed to call API 'Swissquote'.")

        json_data = response.json()

        return json_data
    
    def getPairLive(self, 
                base: str,
                quote: str
    ):
        """
        Sends an API call to 'Swissquote' for a major currency pair (USD pair) in the format "GBP/USD".

        Args:
            base (str): The base currency, e.g. first currency in pair.
            quote (str): The quote currency, e.g. second currency in pair.

        Returns:
            out (json)
        """
        
        pair = f"{base}/{quote}"

        json_data = self.callForexApi(endpoint=pair)
        
        # fetch the prices for the 0-spread server
        elite_live5 = []
        for entry in json_data:
            if entry["topo"]["server"] == "Live5":
                for spread in entry["spreadProfilePrices"]:
                    if spread["spreadProfile"] == "Elite":
                        elite_live5.append(spread)

        return elite_live5[0]

if __name__ == "__main__":
    a = swissquote()
    print({"GBP/USD":a.getPairLive(base="GBP", quote="USD")})
    #print(a.getPairLive(base="EUR", quote="USD"))
    #print(a.getPairLive(base="NZD", quote="USD"))
    #print(a.getPairLive(base="AUD", quote="USD"))
    #print(a.getPairLive(base="USD", quote="JPY"))
    #print(a.getPairLive(base="USD", quote="CHF"))
    #print(a.getPairLive(base="USD", quote="CAD"))
    print({"USD/SEK":a.getPairLive(base="USD", quote="SEK")}) #bonus