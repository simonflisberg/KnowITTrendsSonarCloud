from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from StockData import StockData
from ForexData import ForexData
from MacroData import MacroData
from CommodityData import CommodityData
from BananAI import BananAI

class Predictor:
    _stock_data = StockData()
    _forex_data = ForexData()
    _macro_data = MacroData()
    _commodity_data = CommodityData()
    _banan_ai = BananAI()

    def __init__(self) -> None:
        pass

    def PredictStock(self,
                         symbol: str):
        """
        Queries DataAgent for stock data and then uses that data to query the Banan to generate a prediction about a certain stock.
        Args:
            symbol (str): The symbol for the stock to write a report about.
        Returns:
            predictions (dict): A dictionary containing different types of predictions made by the AI. The dictionary will have the following contents:
                range (str): A price range that the AI thinks is reasonable for the stock in 1 years time.
                price (float): A price that the AI thinks is reasonable for the stock in 1 years time.
                outlook (str): A short explanation of the outlook for the stock during the next year.
        """

        company_profile = str(self._stock_data.compileKeyInfo(symbol=symbol))

        key_figures = str(self._stock_data.compileKeyFigures(symbol=symbol))

        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=365*5)).strftime('%Y-%m-%d')
        historic_price_all_data = self._stock_data.compilePriceData(symbol=symbol, start_date=start_date, end_date=end_date, price_types=['close'])
        historic_price_close = str([
            {"date": entry["date"], "close": entry["close"]}
            for entry in historic_price_all_data["historical"]
            ])

        range = self._banan_ai.SendRequest(f"""
        Could you please provide a price range that you think that the stock will trade within in exactly 1 year based on the data that I provide below?
        Please ONLY answer with the price range in the format "$XX.XX - $XX.XX" and do not write anything else in your answer.
        Company Profile Data: {company_profile}
        Key Figures Data: {key_figures}
        Historic Price Data (Last 5 years): {historic_price_close}
        """)

        price = float(self._banan_ai.SendRequest(f"""
        Could you please provide a an exact price that you think the stock will trade at in exactly 1 year based on the data that I provide below?
        Please ONLY answer with the price in number format and do not write anything else in your answer.
        Company Profile Data: {company_profile}
        Key Figures Data: {key_figures}
        Historic Price Data (Last 5 years): {historic_price_close}

        Make sure that the prediciton is within the range {range}.
        """))

        outlook = self._banan_ai.SendRequest(f"""
        Could you please provide a short outlook for the stock below during the next 1 year period? What do you think will happen to the stock price during the next 1 year?
        The answer should be easy to understand for someone with limited economic knowledge. Do not acknowledge the question that I asked in your response, only respond with the outlook.
        Company Profile Data: {company_profile}
        Key Figures Data: {key_figures}
        Historic Price Data (Last 5 years): {historic_price_close}
        """)

        range = range.replace("\n", "")
        outlook = outlook.replace("\n", "")

        return {
            'range': range,
            'price': price,
            'outlook': outlook
        }
    
    def PredictForex(self,
                         base: str,
                         quote: str):
        """
        Queries DataAgent for commodity data and then uses that data to query the Banan AI to generate predictions about a certain commodity.
        Args:
            base (str): The base currency, e.g. first currency in pair.
            quote (str): The quote currency, e.g. second currency in pair.
        Returns:
            predictions (dict): A dictionary containing different types of predictions made by the AI. The dictionary will have the following contents:
                range (str): A price range that the AI thinks is reasonable for the commodity in 1 years time.
                price (float): A price that the AI thinks is reasonable for the commodity in 1 years time.
                outlook (str): A short explanation of the outlook for the commodity during the next
        """
        start_date = datetime.today() - relativedelta(years=1)
        formatted_start_date = start_date.strftime("%Y-%m-%d")

        currency_data = str(self._forex_data.getHistoricalMajorPair(base=base, quote=quote, start_date=formatted_start_date))

        range = self._banan_ai.SendRequest(f"""
        Could you please provide a price range that you think that the forex pair will trade within in 1 months time based on the data I provide?
        Please ONLY answer with the price range in the format "XX.XX - XX.XX" and do not write anything else in your answer.
        Currency data: {currency_data}
        """)

        price = float(self._banan_ai.SendRequest(f"""
        Could you please provide a an exact price that you think the forex pair will trade at in exactly 1 month based on the data that I provide below?
        Please ONLY answer with the price in number format and do not write anything else in your answer.
        Currency data: {currency_data}

        Make sure that the prediciton is within the range {range}.
        """))

        outlook = self._banan_ai.SendRequest(f"""
        Could you please provide a short outlook for the forex pair below during the next 1 month period? What do you think will happen to the exchange rate during the next month?
        The answer should be easy to understand for someone with limited economic knowledge. Do not acknowledge the question that I asked in your response, only respond with the outlook.
        Currency data: {currency_data}
        """)

        range = range.replace("\n", "")
        outlook = outlook.replace("\n", "")

        return {
            'range': range,
            'price': price,
            'outlook': outlook
        }
    
    def PredictCountry(self,
                           country_code: str):
        """
        Queries DataAgent for country data and then uses that data to query the Banan AI to generate macro economic predictions about a certain country.
        Args:
            country_code (str): The country code for the country to get the data from.
        Returns:
            predictions (dict): A dictionary containing different types of predictions made by the AI. The dictionary will have the following contents:
                range_gdp (str): A range that the AI thinks is reasonable for the country's GDP in 5 years.
                range_gdp_growth_rate (str): A range that the AI thinks is reasonable for the country's GDP Growth Rate in 5 years.
                value_gdp (float): A value that the AI thinks is reasonable for the country's GDP in 5 years.
                value_gdp_growth_rate (float): A value that the AI thinks is reasonable for the country's GDP Growth Rate in 5 years.
                general_outlook (str): A general outlook about the country's gdp and gdp growth rate.
        """

        # Economic Data

        historic_gdp = str(self._macro_data.compileCountryData(country_code=country_code, data_type='gdp', start_year=1970, end_year=2100))
        historic_gdp_growth_rate = str(self._macro_data.compileCountryData(country_code=country_code, data_type='gdp_growth_rate', start_year=1970, end_year=2100))

        range_gdp = self._banan_ai.SendRequest(f"""
        Could you please provide an estimation with the range of this country's GDP in 5 years based on the data that I provide below?
        Please ONLY answer with the GDP range in the format "$X,XXXB - $X,XXXB." and do not write anything else in your answer. Change the b to the appropriate suffix (M = million, B = Billion, T = Trillion, etc.)
        GDP Data: {historic_gdp}
        """)

        value_gdp = float(self._banan_ai.SendRequest(f"""
        Could you please provide an estimation with the value of this country's GDP in 5 years based on the data that I provide below?
        Please ONLY answer with the value of the GDP in number format and nothing else. Do not include the $ sign.
        GDP Data: {historic_gdp}

        Please make sure that the estimation is within the following range: {range_gdp}.
        """))

        range_gdp_growth_rate = self._banan_ai.SendRequest(f"""
        Could you please provide an estimation with the range of this country's GDP Growth Rate in 5 years based on the data that I provide below?
        Please ONLY answer with the GDP Growth Rate range in the format "XX.XX% - XX.XX%" and do not write anything else in your answer.
        GDP Data: {historic_gdp_growth_rate}
        """)

        value_gdp_growth_rate = float(self._banan_ai.SendRequest(f"""
        Could you please provide an estimation with the value of this country's GDP Growth Rate in 5 years based on the data that I provide below?
        Please ONLY answer with the value of the GDP Growth Rate in the format "XX.XX" and do not write anything else in your answer. Do not include the % sign.
        GDP Data: {historic_gdp_growth_rate}

        Please make sure that the estimation is within the following range: {range_gdp_growth_rate}.
        """))

        general_outlook = self._banan_ai.SendRequest(f"""
        Could you please provide me with a brief outlook on this country's GDP and GDP Growth Rate for the next 5 years based on the data that I provide?
        The answer should be easy to understand for someone with limited economic knowledge. Please do not acknowledge my question in the answer, only respond with the brief outlook.

        Historic GDP: {historic_gdp}
        Historic GDP Growth Rate: {historic_gdp_growth_rate}
        """)

        range_gdp = range_gdp.replace("\n", "")
        range_gdp_growth_rate = range_gdp_growth_rate.replace("\n", "")
        general_outlook = general_outlook.replace("\n", "")

        return {
            'range_gdp': range_gdp,
            'value_gdp': value_gdp,
            'range_gdp_growth_rate': range_gdp_growth_rate,
            'value_gdp_growth_rate': value_gdp_growth_rate,
            'general_outlook': general_outlook
        }

    
    def PredictCommodity(self,
                         commodity_id: str):
        """
        Queries DataAgent for commodity data and then uses that data to query the Banan AI to generate predictions about a certain commodity.
        Args:
            
        Returns:
            predictions (dict): A dictionary containing different types of predictions made by the AI. The dictionary will have the following contents:
                range (str): A price range that the AI thinks is reasonable for the commodity in 1 year.
                price (float): A price that the AI thinks is reasonable for the commodity in 1 year.
                outlook (str): A short explanation of the outlook for the commodity during the next year.
        """
        start_date = datetime.today() - relativedelta(years=10)
        formatted_start_date = start_date.strftime("%Y-%m-%d")
        historic_commodity_data = str(self._commodity_data.compileCommodityData(commodity_id=commodity_id, start_date=formatted_start_date))

        if commodity_id != "sunfloweroil":
            range = self._banan_ai.SendRequest(f"""
            Could you please provide a price range that you think that the commodity will trade within in 1 year based on the data that I provide?
            Please ONLY answer with the price range in the format "$XX.XX - $XX.XX" (number format) and do not write anything else in your answer.
            Commodity data: {historic_commodity_data}
            """)

            price = float(self._banan_ai.SendRequest(f"""
            Could you please provide a an exact price that you think the commodity will trade at in exactly 1 year based on the data that I provide below?
            Please ONLY answer with the price in number format and do not write anything else in your answer.
            Commodity data: {historic_commodity_data}

            Make sure that the prediciton is within the range {range}.
            """))

            outlook = self._banan_ai.SendRequest(f"""
            Could you please provide a short outlook for the commodity below during the next 1 year period? What do you think will happen to the commodity price during the next year?
            The answer should be easy to understand for someone with limited economic knowledge. Do not acknowledge the question that I asked in your response, only respond with the outlook.
            Commodity data: {historic_commodity_data}
            """)
        else:
            range = self._banan_ai.SendRequest(f"""
            Could you please provide a price range that you think that the commodity will trade within in 1 year based on the data that I provide?
            Please ONLY answer with the price range in the format "$XX.XX - $XX.XX" (number format) and do not write anything else in your answer.
            Commodity data: {historic_commodity_data}
            """)

            price = float(self._banan_ai.SendRequest(f"""
            Could you please provide a an exact price that you think the commodity will trade at in exactly 1 year based on the data that I provide below?
            Please ONLY answer with the price in number format and do not write anything else in your answer.
            Commodity data: {historic_commodity_data}

            Make sure that the prediciton is within the range {range}.
            """))

            outlook = self._banan_ai.SendRequest(f"""
            Could you please provide a short outlook for the commodity below during the next 5 year period? What do you think will happen to the commodity price during these years and how can Diddy's punishment relate to it for instance would a home arrest still allow him to host parties?
            The answer should be easy to understand for someone with limited economic knowledge, and explain using Diddy. Do not acknowledge the question that I asked in your response, only respond with the outlook and speculate to how Diddy's actions have affected the price.
            In the answer you must speculate to how Diddy's arrest and partys have affected the price rise and fall, etc. If you see sunfloweroil somewhere it is meant to say baby oil, so read it as that. Explain how the massive price increase and decrease (price spike) was related to Diddy and his parties, like that he was partying a lot and needed baby oil and stuff like that, it must be explained using Diddy and his parties. The speculation and outlook about Diddy should be at least 200 words.
            Commodity data: {historic_commodity_data}
            """)

        range = range.replace("\n", "")
        outlook = outlook.replace("\n", "")

        return {
            'range': range,
            'price': price,
            'outlook': outlook
        }



if __name__ == "__main__":
    predictor = Predictor()
    # print(predictor.PredictStock('CRWD'))
    # print(predictor.PredictForex('USD', 'SEK'))
    # print(predictor.PredictCountry('SE'))
    print(predictor.PredictCommodity('sunfloweroil'))
