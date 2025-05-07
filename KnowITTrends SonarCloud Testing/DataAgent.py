from StockData import StockData
from MacroData import MacroData
from ForexData import ForexData
from Explanation import Explainer
from CommodityData import CommodityData
from ReportWriter import ReportWriter
from AIPredictions import Predictor
from ReportCompiler import ReportCompiler
from datetime import datetime, timedelta
import os

class DataAgent:
    _stock_data = StockData()
    _macro_data = MacroData()
    _forex_data = ForexData()
    _commodity_data = CommodityData()
    _explainer = Explainer()
    _report_writer = ReportWriter()
    _report_compiler = ReportCompiler()
    _predictor = Predictor()

    def __init__(self):
        self.createFolders()
        
    def createFolders(self):
        """
        If there is no temp folder, create it.
        """

        # Temp folder
        if not os.path.exists("temp"):
            os.makedirs("temp")

        # Data cache
        if not os.path.exists("cached_data"):
            os.makedirs("cached_data")

    def queryStock(self,
                   dataType: str,
                   symbol: str,
                   years: float = 5, # 5 years of data as standard
                   price_types: list = ['close'], # Only closing price as standard
    ):
        """
        A method to query StockData for stock data.

        Args:
            dataType (str): The type of data queried.
                Accepted strings: 
                    "historic_price": returns the specified price data for the specified period of time
                    "key_figures": returns many useful key figures
                    "company_profile": returns a written company profile
            symbol (str): The stock ticker name of the stock to be queried
            years (int): The number of years to get price data for.
            price_types (list): A list of strings containing the wanted price data. Available data are open, close, low, high.
        Returns:
            out (json): Json string containing the queried data
        """

        if dataType.lower() == 'historic_price':
            end_date = datetime.today().strftime('%Y-%m-%d')
            start_date = (datetime.today() - timedelta(days=365*years)).strftime('%Y-%m-%d')
            return self._stock_data.compilePriceData(symbol=symbol, start_date=start_date, end_date=end_date, price_types=price_types)

        elif dataType.lower() == 'key_figures':
            return self._stock_data.compileKeyFigures(symbol=symbol)

        elif dataType.lower() == 'company_profile':
            return self._stock_data.compileKeyInfo(symbol=symbol)
        
        else:
            print(f"{dataType} is an invalid data type, input a valid data type intead.")
            return {}
        
    def queryCountry(self,
                     country_code: str,
                     data_type: str,
                     start_year: int,
                     end_year: int):
        """
        A method to query MacroData for country data (economic, social, environmental, etc.)

        Args:
            data_type (str): The type of data queried.
                Accepted strings: 
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
                'country_info'
            country_code (str): The country code for the country to get the data from.
            start_year (int): The start year for the requested data.
            end_year (int): The end year for the requested data.
        Returns:
            out (dict): A dictionary containing the queried data
        """
        if data_type == 'country_info':
            country_data = self._macro_data.compileCountryInfo(country_code=country_code)
            explainations = {
                'explain_interest_rate': self.queryExplanation('interest_rate'),
                'explain_gdp': self.queryExplanation('gdp'),
                'explain_gdp_per_capita': self.queryExplanation('gdp_per_capita')
            }
            country_data.update(explainations)

            return country_data
        
        elif data_type in ['inflation',
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
                'air_pollution']:
            return self._macro_data.compileCountryData(country_code=country_code, data_type=data_type, start_year=start_year, end_year=end_year)

        else:
            print(f"{data_type} is an invalid data type, input a valid data type intead.")
            return {}

    def queryForexMajor(self,
                        base: str,
                        quote: str,
                        start_date: str):
        """
        Only request Major pairs and USD/SEK.

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
        
        try:
            json = self._forex_data.getHistoricalMajorPair(base=base, quote=quote, start_date=start_date)
        
        except:
            json = {"Error":-1}

        return json
    
    def queryCommodities(self,
                         commodity_id,
                         start_date
    ):
        """

        """
        try:
            json = self._commodity_data.compileCommodityData(commodity_id=commodity_id, start_date=start_date)

        except:
            json = {"Error":-1}

        return json
    
    def queryExplanation(self,
                         to_explain: str):
        """
        Returns a string with an explanation based on the to_explain argument.

        Args:
            to_explain (str): Specifies what to explain.
            Accepted strings:
            'currency_exchange_graph'
            'trendline'
            'gdp'
            'gdp_per_capita'
            'interest_rate'
            'market_cap'
            'pe_ratio'
            'div_yield'
            'ps_ratio'

        out (str): A string with an explanation.
        """
        return self._explainer.get_explanation(to_explain)
    
    def queryReport(self,
                    report_type: str,
                    code1: str,
                    code2: str = None,
                    overview_forex: bool = True,
                    key_figures_forex: bool = True,
                    recent_performance_forex: bool = True,
                    future_outlook_forex: bool = True,
                    forecast_forex: bool = True,
                    introduction_country: bool = True,
                    historic_economic_performance_country: bool = True,
                    historic_social_data_country: bool = True,
                    historic_environmental_data_country: bool = True,
                    future_economic_outlook_country: bool = True,
                    forecast_country: bool = True,
                    commodity_overview_commodity: bool = True,
                    historic_price_analysis_commodity: bool = True,
                    recent_price_trends_commodity: bool = True,
                    future_outlook_commodity: bool = True,
                    forecast_commodity: bool = True
                    ):
        """
        Returns a string with a report about a stock, forex pair, country or commodity.

        Args:
            report_type (str): What the report should be about.
                Acceptend strings:
                    'stock'
                    'forex_pair'
                    'country'
                    'commodity'
            code1 (str): Used to identify what to write the report about.
            code2 (str): Used to identify the second currency code. Only used for forex reports.
        Returns:
            text (str): A report.
        """

        if report_type == 'stock':
            try:
                return self._report_writer.WriteStockReport(symbol=code1)
            except Exception as e:
                print(f'Failed to generate stock report: {e}')
        
        elif report_type == 'forex_pair':
            try:
                return self._report_writer.WriteForexReport(base=code1, 
                                                            quote=code2, 
                                                            overview=overview_forex, 
                                                            key_figures=key_figures_forex, 
                                                            recent_performance=recent_performance_forex, 
                                                            future_outlook=future_outlook_forex, 
                                                            forecast=forecast_forex)
            except Exception as e:
                print(f'Failed to generate forex report: {e}')        

        elif report_type == 'country':
            try: 
                return self._report_writer.WriteCountryReport(country_code=code1, 
                                                              introduction=introduction_country, 
                                                              historic_economic_performance=historic_economic_performance_country, 
                                                              historic_social_data=historic_social_data_country, 
                                                              historic_enironmental_data=historic_environmental_data_country, 
                                                              future_economic_outlook=future_economic_outlook_country, 
                                                              forecast=forecast_country)
            except Exception as e:
                print(f'Failed to generate country report: {e}')

        elif report_type == 'commodity':
            try:
                return self._report_writer.WriteCommodityReport(commodity_id=code1,
                                                                commodity_overview=commodity_overview_commodity,
                                                                historic_price_analysis=historic_price_analysis_commodity,
                                                                recent_price_trends=recent_price_trends_commodity,
                                                                future_outlook=future_outlook_commodity,
                                                                forecast=forecast_commodity)
            except Exception as e:
                print(f'Failed to generate commodity report: {e}')

        else:
            raise ValueError('Please use an appropriate report type.')
        
    def queryPrediction(self, 
                        prediction_type: str, 
                        code1: str,
                        code2: str = None):
        """
        Queries AIPredictions to get AI predictions for stocks, currency pairs, countries or commodities.

        Args:
            prediction_type (str): What the prediction should be about.
                Acceptend strings:
                    'stock'
                    'forex_pair'
                    'country'
                    'commodity'
            code1 (str): Used to identify what to write the report about.
            code2 (str): Used to identify the second currency code. Only used for forex reports.
        Returns:
            prediction (dict): A dictionary including a future range, a predicted future price and a brief outlook.
        """

        if prediction_type == 'stock':
            try:
                return self._predictor.PredictStock(symbol=code1)
            except Exception as e:
                print(f'Failed to generate stock prediction: {e}')
        
        elif prediction_type == 'forex_pair':
            try:
                return self._predictor.PredictForex(base=code1, quote=code2)
            except Exception as e:
                print(f'Failed to generate forex prediction: {e}')

        elif prediction_type == 'country':
            try: 
                return self._predictor.PredictCountry(country_code=code1)
            except Exception as e:
                print(f'Failed to generate country prediction: {e}')

        elif prediction_type == 'commodity':
            try:
                return self._predictor.PredictCommodity(commodity_id=code1)
            except Exception as e:
                print(f'Failed to generate commodity report: {e}')

        else:
            raise ValueError('Please use an appropriate prediction type.')
    
    def queryRerportPDF(self,
                        report_type,
                        type_id,
                        overview_forex: bool = True,
                        key_figures_forex: bool = True,
                        recent_performance_forex: bool = True,
                        future_outlook_forex: bool = True,
                        forecast_forex: bool = True,
                        introduction_country: bool = True,
                        historic_economic_performance_country: bool = True,
                        historic_social_data_country: bool = True,
                        historic_environmental_data_country: bool = True,
                        future_economic_outlook_country: bool = True,
                        forecast_country: bool = True,
                        commodity_overview_commodity: bool = True,
                        historic_price_analysis_commodity: bool = True,
                        recent_price_trends_commodity: bool = True,
                        future_outlook_commodity: bool = True,
                        forecast_commodity: bool = True
                        ):
        
        if report_type == "commodity":
            data = self.queryCommodities(commodity_id=type_id, start_date="2015-01-01")
            interval = "monthly"

        if report_type == "country":
            data = self.queryCountry(country_code=type_id, data_type="gdp", start_year="1974", end_year="2025")
            interval = "yearly"

        if report_type == "forex":
            base = str(type_id[:3]).strip()
            quote = str(type_id[-3:]).strip()
            data = self.queryForexMajor(base=base, quote=quote, start_date="2015-01-01")
            interval = "daily"

        return self._report_compiler.CompilePDF(report_type=report_type, 
                                                type_id=type_id, 
                                                data=data, 
                                                interval=interval,
                                                overview_forex=overview_forex, 
                                                key_figures_forex=key_figures_forex, 
                                                recent_performance_forex=recent_performance_forex, 
                                                future_outlook_forex=future_outlook_forex,
                                                forecast_forex=forecast_forex,
                                                introduction_country=introduction_country,
                                                historic_economic_performance_country=historic_economic_performance_country,
                                                historic_social_data_country=historic_social_data_country,
                                                historic_environmental_data_country=historic_environmental_data_country,
                                                future_economic_outlook_country=future_economic_outlook_country,
                                                forecast_country=forecast_country,
                                                commodity_overview_commodity=commodity_overview_commodity,
                                                historic_price_analysis_commodity=historic_price_analysis_commodity,
                                                recent_price_trends_commodity=recent_price_trends_commodity,
                                                future_outlook_commodity=future_outlook_commodity,
                                                forecast_commodity=forecast_commodity
                                                )

data_agent = DataAgent() # global instans för test

if __name__ == "__main__":
    # test of price function
    # print('FMP price function:\n\n', data_agent.queryStock(dataType='historic_price', symbol='DADADADADA', price_types=['open', 'close', 'high', 'low'], years=0.5))

    # test of key figure function
    # print('\nFMP key figures function:\n\n', data_agent.queryStock(dataType='key_figures', symbol='CRWD'))

    # # test key info function
    # print('\nFMP key info function:\n\n', data_agent.queryStock(dataType='company_profile', symbol='CRWD'))

    # test of country data
    # print('Country data test:\n\n', data_agent.queryCountry(country_code='SE', data_type='population', start_year=1970, end_year=2100))
    print('Country info test:\n\n', data_agent.queryCountry(country_code='FI', data_type='country_info', start_year=1980, end_year=2100))

    # test major forex pair data
    # print(data_agent.queryForexMajor(base="GBP", quote="USD", start_date="2025-01-01"))

    # commodity test
    # print(data_agent.queryCommodities('wti', '2015-01-01'))

    # explainer test
    # print(data_agent.queryExplanation('gdp'))

    # report test
    # print(data_agent.queryReport(report_type='country', code1='US', introduction_country=True, historic_economic_performance_country=False, historic_social_data_country=False, historic_environmental_data_country=True, future_economic_outlook_country=True, forecast_country=True))
    # print(data_agent.queryReport(report_type='forex_pair', code1='USD', code2='SEK', overview_forex=False, key_figures_forex=False, recent_performance_forex=True, future_outlook_forex=True, forecast_forex=True))
    # print(data_agent.queryReport(report_type='commodity', code1='wti', commodity_overview_commodity=True, historic_price_analysis_commodity=False, recent_price_trends_commodity=False, future_outlook_commodity=True, forecast_commodity=False))

    # prediction test
   # print(data_agent.queryPrediction(prediction_type='country', code1='SE'))

    # report pdf thing
    # print(data_agent.queryRerportPDF("commodity", "bananas", historic_price_analysis_commodity=False, recent_price_trends_commodity=False))
    # print(data_agent.queryRerportPDF("forex", "USDCAD", key_figures_forex=False, recent_performance_forex=False))
    # print(data_agent.queryRerportPDF("country", "SE"))

    print('babas')