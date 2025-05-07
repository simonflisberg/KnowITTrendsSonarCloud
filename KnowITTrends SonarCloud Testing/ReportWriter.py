from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from StockData import StockData
from ForexData import ForexData
from MacroData import MacroData
from CommodityData import CommodityData
from BananAI import BananAI
from AIPredictions import Predictor

class ReportWriter:
    _stock_data = StockData()
    _forex_data = ForexData()
    _macro_data = MacroData()
    _commodity_data = CommodityData()
    _banan_ai = BananAI()
    _predictor = Predictor()

    def __init__(self) -> None:
        pass

    def WriteStockReport(self,
                         symbol: str):
        """
        Queries DataAgent for stock data and then uses that data to query the Banan AI to write a report about a certain stock.
        The report includes historic performance and predictions about the future.
        Args:
            symbol (str): The symbol for the stock to write a report about.
        Returns:
            text (str): A string with a report about the stock.
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
        
        outlook = str(self._predictor.PredictStock(symbol=symbol))

        text = self._banan_ai.SendRequest(f"""
        Could you please write a report about the stock below based on the info that I provide?
        Divide it into the sections 1. What does [company] do? 2. Key Numbers 3. Recent Stock Performance 4. Future Outlook. Do not write any introduction in your answer before point 1.
        At the end of the report, there should also be a section called 5. SARIMA Forecast. Give a brief explanation of what SARIMA forecast is generally, under this section there will be a graph with a SARIMA Forecast (I will provide this graph so please don't describe what the actual graph in this case would be like). Also please don't put any text similar to [Insert SARIMA graph here], simply type the rubric and a general explanation of what it is.
        Do not put any acknowledgement of where the actual SARIMA graph will be put, this will be provided later when this text is put into a PDF. So do not write [SARIMA Graph] at the end.
        It should be very easy to understand for an average person with little knowledge about economics or the stock market.
        It should include a brief overview of the company, the most important key figures, a brief explanation of its historic performance and a future outlook based on the outlook data that I provide.
        Make sure that there are no # signs in your response, only use bold text for the section rubrics.
        Remove all text in your report where it says exactly [SARIMA Graph].
        Company Profile Data: {company_profile}
        Key Figures Data: {key_figures}
        Historic Price Data (Last 5 years): {historic_price_close}
        Future Outlook Data: {outlook}
        """)

        # text = text.replace("\n", "")

        return text
    
    def WriteForexReport(self,
                         base: str,
                         quote: str,
                         overview: bool = True,
                         key_figures: bool = True,
                         recent_performance: bool = True,
                         future_outlook: bool = True,
                         forecast: bool = True):
        """
        Queries DataAgent for forex data and then uses that data to query the Banan AI to write a report about a certain currency pair.
        The report includes historic performance (1 year history) and predictions about the future.
        Args:
            base (str): The base currency, e.g. first currency in pair.
            quote (str): The quote currency, e.g. second currency in pair.
        Returns:
            text (str): A string with a report about the currency pair.
        """
        start_date = datetime.today() - relativedelta(years=1)
        formatted_start_date = start_date.strftime("%Y-%m-%d")

        currency_data = str(self._forex_data.getHistoricalMajorPair(base=base, quote=quote, start_date=formatted_start_date))

        if future_outlook == True:
            outlook = f"Future Outlook Data: {self._predictor.PredictForex(base=base, quote=quote)}"
        else:
            outlook = ""

        if overview == True:
            overview_text = "Overview"
        else:
            overview_text = ""

        if key_figures == True:
            key_figures_text = "Key Figures"
        else:
            key_figures_text = ""
        
        if recent_performance == True:
            recent_performance_text = "Recent Performance"
        else:
            recent_performance_text = ""

        if future_outlook == True:
            future_outlook_text = "Future Outlook"
        else:
            future_outlook_text = ""

        if forecast == True:
            forecast_text = """At the end of the report, there should also be a section called SARIMA Forecast. 
            Give a brief explanation of what SARIMA forecast is generally, under this section there will be a graph with a SARIMA Forecast (I will provide this graph so please don't describe what the actual graph in this case would be like).
            Also please dont put any text similar to [Insert SARIMA graph here], simply type the rubric and a general explanation of what it is.
            Do not put any acknowledgement of where the actual SARIMA graph will be put, this will be provided later when this text is put into a PDF. So do not write [SARIMA Graph] at the end."""
        else:
            forecast_text = ""

        text = self._banan_ai.SendRequest(f"""
        Could you please write a report about the currency pair below based on the info that I provide?
        Do not write any acknowledgement of the question that I asked and divide it into the following sections:
        {overview_text}
        {key_figures_text}
        {recent_performance_text}
        {future_outlook_text}
        {forecast_text}
        Please put the appropriate number for each section. DO NOT add any sections of your own, only add the ones that I specify.
        Do not add a section called Future Outlook unless it is specified. Please do not add any additional sections.
        It should be very easy to understand for an average person with little knowledge about economics or the forex market.
        Make sure that there are no # signs in your response, only use bold text for the section rubrics.
        Remove all text in your report where it says exactly [SARIMA Graph]. It is very important that it does not say [SARIMA Graph] at the end of your response.
        Info about the currency pair: {currency_data}
        {outlook}
        """)

        return text
    
    def WriteCountryReport(self,
                           country_code: str,
                           introduction: bool = True,
                           historic_economic_performance: bool = True,
                           historic_social_data: bool = True,
                           historic_environmental_data: bool = True,
                           future_economic_outlook: bool = True,
                           forecast: bool = True):
        """
        Queries DataAgent for country data and then uses that data to query the Banan AI to write a report about a certain country.
        This report includes historic economic performance, as well as explanations of historic social and environmental data.
        Args:
            country_code (str): The country code for the country to get the data from.
        Returns:
            text (str): A report about the country.
        """

        # Economic Data

        historic_inflation = str(self._macro_data.compileCountryData(country_code=country_code, data_type='inflation', start_year=1970, end_year=2100))
        historic_gdp = str(self._macro_data.compileCountryData(country_code=country_code, data_type='gdp', start_year=1970, end_year=2100))
        historic_gdp_per_capita = str(self._macro_data.compileCountryData(country_code=country_code, data_type='gdp_per_capita', start_year=1970, end_year=2100))
        historic_gdp_growth_rate = str(self._macro_data.compileCountryData(country_code=country_code, data_type='gdp_growth_rate', start_year=1970, end_year=2100))

        # Social Data

        historic_population = str(self._macro_data.compileCountryData(country_code=country_code, data_type='population', start_year=1970, end_year=2100))
        historic_life_expectancy = str(self._macro_data.compileCountryData(country_code=country_code, data_type='life_expectancy', start_year=1970, end_year=2100))
        historic_unemployment = str(self._macro_data.compileCountryData(country_code=country_code, data_type='unemployment', start_year=1970, end_year=2100))
        historic_poverty_rate = str(self._macro_data.compileCountryData(country_code=country_code, data_type='poverty_rate', start_year=1970, end_year=2100))
        historic_income_inequality = str(self._macro_data.compileCountryData(country_code=country_code, data_type='income_inequality', start_year=1970, end_year=2100))

        # Environmental Data

        historic_forest_area = str(self._macro_data.compileCountryData(country_code=country_code, data_type='forest_area', start_year=1970, end_year=2100))
        historic_renewable_energy = str(self._macro_data.compileCountryData(country_code=country_code, data_type='renewable_energy', start_year=1970, end_year=2100))
        historic_air_pollution = str(self._macro_data.compileCountryData(country_code=country_code, data_type='air_pollution', start_year=1970, end_year=2100))

        outlook = str(self._predictor.PredictCountry(country_code=country_code))

        if introduction == True:
            introduction_text = "Introduction. Please make this short."
        else:
            introduction_text = ""

        if historic_economic_performance == True:
            historic_economic_performance_text = "Historic Economic Performance"
            historic_economic_performance_data = f"""
            Historic Economic Performance:
            Historic Inflation: {historic_inflation}
            Historic GDP: {historic_gdp}
            Historic GDP Per Capita: {historic_gdp_per_capita}
            Historic GDP Growth Rate: {historic_gdp_growth_rate}
            """
        else:
            historic_economic_performance_text = ""
            historic_economic_performance_data = ""

        if historic_social_data == True:
            historic_social_data_text = "Historic Social Data"
            historic_social_data_data = f"""
            Historic Social Data:
            Historic Population: {historic_population}
            Historic Life Expectancy: {historic_life_expectancy}
            Historic Unemployment: {historic_unemployment}
            Historic Poverty Rate: {historic_poverty_rate}
            Historic Income Inequality: {historic_income_inequality}
            """
        else:
            historic_social_data_text = ""
            historic_social_data_data = ""

        if historic_environmental_data == True:
            historic_environmental_data_text = "Historic Environmental Data"
            historic_environmental_data_data = f"""
            Historic Environmental Data:
            Historic Forest Area: {historic_forest_area}
            Historic Renewable Energy: {historic_renewable_energy}
            Historic Air Pollution: {historic_air_pollution}
            """
        else:
            historic_environmental_data_text = ""
            historic_environmental_data_data = ""

        if future_economic_outlook == True:
            future_economic_outlook_text = "Future Economic Outlook"
            future_economic_outlook_data = f"Future Economic Outlook Data: {outlook}"
        else:
            future_economic_outlook_text = ""
            future_economic_outlook_data = ""

        if forecast == True:
            forecast_text = "At the end of the report, there should also be a section called Forecast. Do not write anything at all under this section, only write Forecast"
        else:
            forecast_text = ""

        text = self._banan_ai.SendRequest(f"""
        Could you please write a report about the country below based on the data that I provide?
        Do not write any acknowledgement of the question that I asked and divide it into the following sections: 
        {introduction_text}
        {historic_economic_performance_text}
        {historic_social_data_text}
        {historic_environmental_data_text}
        {future_economic_outlook_text}
        {forecast_text}
        Please put the appropriate number for each section. DO NOT add any sections of your own, only add the ones that I specify.
        It should be very easy to understand for an average person with little knowledge about economics, social data or environmental data.
        If some data is missing, please ignore that part and do not include it in the report.
        Write the report in free text based on the data, do not make bullet point lists.
        Make sure that there are no # signs in your response, only use bold text for the section rubrics.

        {historic_economic_performance_data}

        {historic_social_data_data}

        {historic_environmental_data_data}

        {future_economic_outlook_data}
        """)

        return text
    
    def WriteCommodityReport(self,
                             commodity_id: str,
                             commodity_overview: bool = True,
                             historic_price_analysis: bool = True,
                             recent_price_trends: bool = True,
                             future_outlook: bool = True,
                             forecast: bool = True):
        """
        Queries DataAgent for commodity data and then uses that data to query Banan AI to write a report about the commodity.
        The report includes historic price information about the commodity.
        """

        start_date = datetime.today() - relativedelta(years=10)
        formatted_start_date = start_date.strftime("%Y-%m-%d")

        historic_commodity_data = str(self._commodity_data.compileCommodityData(commodity_id=commodity_id, start_date=formatted_start_date))

        if future_outlook == True:
            outlook = f"Future Outlook Data: {self._predictor.PredictCommodity(commodity_id=commodity_id)}"
        else:
            outlook = ""

        if commodity_overview == True:
            commodity_overview_text = "Commodity Overview"
        else:
            commodity_overview_text = ""

        if historic_price_analysis == True:
            historic_price_analysis_text = "Historic Price Analysis"
        else:
            historic_price_analysis_text = ""

        if recent_price_trends == True:
            recent_price_trends_text = "Recent Price Trends"
        else:
            recent_price_trends_text = ""

        if future_outlook == True:
            future_outlook_text = "Future Outlook"
        else:
            future_outlook_text = ""

        if forecast == True:
            forecast_text = """At the end of the report, there should also be a section called SARIMA Forecast. 
            Give a brief explanation of what SARIMA forecast is generally, under this section there will be a graph with a SARIMA Forecast (I will provide this graph so please don't describe what the actual graph in this case would be like).
            Also please dont put any text similar to [Insert SARIMA graph here], simply type the rubric and a general explanation of what it is.
            Do not put any acknowledgement of where the actual SARIMA graph will be put, this will be provided later when this text is put into a PDF. So do not write [SARIMA Graph] at the end."""
        else:
            forecast_text = ""

        text = self._banan_ai.SendRequest(f"""
        Could you please write a report about the commodity below based on the data that I provide?
        Do not write any acknowledgement of the question that I asked and divide the report into the following sections: 
        {commodity_overview_text}
        {historic_price_analysis_text}
        {recent_price_trends_text}
        {future_outlook_text}
        {forecast_text}
        Please put the appropriate number for each section. DO NOT add any sections of your own, only add the ones that I specify.
        The report should be very easy to understand for someone with little economic knowledge.
        Write the report in free text under the appropriate sections, do not make bullet points. Do not write anything about the commodity ID or about the value of the trend.
        Make sure that there are no # signs in your response, only use bold text for the section rubrics.
        Remove all text in your report where it says exactly [SARIMA Graph].
        Historic commodity data: {historic_commodity_data}
        Future outlook data: {outlook}
        """)

        return text



if __name__ == "__main__":
    report_writer = ReportWriter()
    print(report_writer.WriteStockReport('BABA'))
    print(report_writer.WriteForexReport(base='USD', quote='SEK'))
    print(report_writer.WriteCountryReport('SE'))
    print(report_writer.WriteCommodityReport('fish'))