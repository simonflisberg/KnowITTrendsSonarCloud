import json
from  DataAPIs.fmp import fmpAPI
from Graph import Graph
import pandas as pd

class StockData:
    _data_api = fmpAPI()
    _graph = Graph()

    def __init__(self):
        pass

    def compilePriceData(self, 
                         symbol: str, 
                         start_date: str,
                         end_date: str,
                         price_types: list):
        """
        A method to query fmpAPI for stock price data.

        Args:
            symbol (str): The stock ticker name of the stock to be queried
            start_date (str): The start date for the price data.
            end_date (str): The end date for the price data.
            price_types (list): A list of strings containing the wanted price data. Available data are open, close, high, low.
        Returns:
            out (json): Json string with a dictionary containing the queried price data.
            The dictionary will be in the following format: {date: [open, close, high, low], ...}
            Open, close, high, low will always have the same index. If a price type is not requested, None is used in its place.
        """

        json_data = self._data_api.getStockPrice(symbol=symbol, start_date=start_date, end_date=end_date)

        trend = self._graph.getLinearTrend(datapoints=json_data)
        
        if isinstance(trend, str):
            trend = json.loads(trend) # ensure trend data is formatted as dict


        df_stock = pd.DataFrame(json_data["historical"])
        df_trend = pd.DataFrame(trend)

        new = pd.merge(df_stock, df_trend, on="date", how="left").to_dict(orient="records")

        json_data_incl_trend = {
            "symbol": symbol,
            "historical": new
        }

        return json_data_incl_trend

    def compileKeyFigures(self, 
                          symbol: str):
        '''
        A method to query fmpAPI for stock key figure data.
        Key figures are for the trailing twelve months.
        Args:
            symbol (str): The stock ticker name of the stock to be queried
        Returns:
            out (json): Json string with a dictionary containing the queried key figures data.
        '''

        # these are all included keys, may remove some in the future if we only want to include parts of it.
        requested_data = [
                        "revenuePerShareTTM",
                        "netIncomePerShareTTM",
                        "operatingCashFlowPerShareTTM",
                        "freeCashFlowPerShareTTM",
                        "cashPerShareTTM",
                        "bookValuePerShareTTM",
                        "tangibleBookValuePerShareTTM",
                        "shareholdersEquityPerShareTTM",
                        "interestDebtPerShareTTM",
                        "marketCapTTM",
                        "enterpriseValueTTM",
                        "peRatioTTM",
                        "priceToSalesRatioTTM",
                        "pocfratioTTM",
                        "pfcfRatioTTM",
                        "pbRatioTTM",
                        "ptbRatioTTM",
                        "evToSalesTTM",
                        "enterpriseValueOverEBITDATTM",
                        "evToOperatingCashFlowTTM",
                        "evToFreeCashFlowTTM",
                        "earningsYieldTTM",
                        "freeCashFlowYieldTTM",
                        "debtToEquityTTM",
                        "debtToAssetsTTM",
                        "netDebtToEBITDATTM",
                        "currentRatioTTM",
                        "interestCoverageTTM",
                        "incomeQualityTTM",
                        "dividendYieldTTM",
                        "dividendYieldPercentageTTM",
                        "payoutRatioTTM",
                        "salesGeneralAndAdministrativeToRevenueTTM",
                        "researchAndDevelopementToRevenueTTM",
                        "intangiblesToTotalAssetsTTM",
                        "capexToOperatingCashFlowTTM",
                        "capexToRevenueTTM",
                        "capexToDepreciationTTM",
                        "stockBasedCompensationToRevenueTTM",
                        "grahamNumberTTM",
                        "roicTTM",
                        "returnOnTangibleAssetsTTM",
                        "grahamNetNetTTM",
                        "workingCapitalTTM",
                        "tangibleAssetValueTTM",
                        "netCurrentAssetValueTTM",
                        "investedCapitalTTM",
                        "averageReceivablesTTM",
                        "averagePayablesTTM",
                        "averageInventoryTTM",
                        "daysSalesOutstandingTTM",
                        "daysPayablesOutstandingTTM",
                        "daysOfInventoryOnHandTTM",
                        "receivablesTurnoverTTM",
                        "payablesTurnoverTTM",
                        "inventoryTurnoverTTM",
                        "roeTTM",
                        "capexPerShareTTM",
                        "dividendPerShareTTM",
                        "debtToMarketCapTTM"
            ]


        try:
            data = self._data_api.getStockKeyFigures(symbol=symbol, requested_data=requested_data)
            
            formatted_data = {}
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    formatted_data[key] = self.format_number(value)
                else:
                    formatted_data[key] = value
            
            return formatted_data

        except Exception as e:
            print(f"Error querying fmpAPI for key figures data: {e}")
            return {}

    def compileKeyInfo(self, 
                       symbol: str):
        """
        A method to query fmpAPI for key stock info data.
        
        Args:
            symbol (str): The stock ticker name of the stock to be queried
        
        Returns:
            out (json): Json string with a dictionary containing the queried key figures data.
        """
        
        
        # these are all included keys, may remove some in the future if we only want to include parts of it.
        requested_data = [
                        "symbol",
                        "price",
                        "beta",
                        "volAvg",
                        "mktCap",
                        "lastDiv",
                        "range",
                        "changes",
                        "companyName",
                        "currency",
                        "cik",
                        "isin",
                        "cusip",
                        "exchange",
                        "exchangeShortName",
                        "industry",
                        "website",
                        "description",
                        "ceo",
                        "sector",
                        "country",
                        "fullTimeEmployees",
                        "phone",
                        "address",
                        "city",
                        "state",
                        "zip",
                        "dcfDiff",
                        "dcf",
                        "image",
                        "ipoDate",
                        "defaultImage",
                        "isEtf",
                        "isActivelyTrading",
                        "isAdr",
                        "isFund"
            ]
        
        try:
            data = self._data_api.getStockKeyInfo(symbol=symbol, requested_data=requested_data)
            
            formatted_data = {}
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    formatted_data[key] = self.format_number(value)
                else:
                    formatted_data[key] = value

            formatted_data['changes'] = float(formatted_data['changes']) # Change changes to float for frontend integration
            
            return formatted_data

        except Exception as e:
            print(f"Error querying fmpAPI for key info data: {e}")
            return {}
        
    def format_number(self, n):
        """
        Formats a number and adds the appropriate suffix, returns the number as a string.
        Args:
            n (int): The number to be formatted.
        Returns:
            n (str): The formatted number as a string.
        """
        if not isinstance(n, (int, float)):
            return n

        n = float(f"{n:.4g}") # Converts number to 4 value figures.

        abs_n = abs(n)
        if abs_n >= 1e12:
            return f"{n / 1e12:.2f}T"
        elif abs_n >= 1e9:
            return f"{n / 1e9:.2f}B"
        elif abs_n >= 1e6:
            return f"{n / 1e6:.2f}M"
        else:
            return str(n)

if __name__ == "__main__":
    stockData = StockData()
    #prices = stockData.compilePriceData(symbol="AAPL", start_date="2025-01-01", end_date="2025-03-01", price_types=["close"])
    #print(prices)
    #key_figures = stockData.compileKeyFigures(symbol="AAPL")
    #print(key_figures)
    info = stockData.compileKeyInfo(symbol="AAPL")
    print(info)