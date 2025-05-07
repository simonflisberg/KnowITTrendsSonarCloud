explanations = {'currency_exchange_graph': 'A currency exchange graph shows how the value of one currency changes relative to another over a period of time. If the line moves upward, the first currency is getting stronger compared to the second; if it moves downward, it is becoming weaker.',
'trendline': 'A trendline is a straight line drawn through a chart to show the overall direction or general pattern of data points. It helps identify whether the data is generally moving upward (increasing trend), downward (decreasing trend), or staying stable.',
'gdp': 'GDP (Gross Domestic Product) measures the total value of all goods and services produced within the borders of a country over a specific time period, usually one year. A rising GDP indicates economic growth, while a falling GDP suggests economic decline.',
'gdp_per_capita': 'GDP per capita is a measure of the economic output of a country divided by its population, indicating the average economic productivity per person. A higher GDP per capita generally suggests better living standards and economic prosperity, while a lower figure may indicate poorer economic conditions.',
'interest_rate': 'An interest rate is the percentage charged or earned for borrowing or lending money. Higher interest rates make loans more expensive but savings more rewarding, while lower interest rates encourage borrowing and spending but offer less incentive to save.',
'market_cap': 'Market cap (market capitalization) is the total value of a company calculated by multiplying its current stock price by the total number of outstanding shares. A higher market cap typically indicates a larger, more established company, while a lower market cap often suggests a smaller or less mature business.',
'pe_ratio': 'The P/E ratio (price-to-earnings ratio) compares the current stock price of a company to its earnings per share, showing how much investors are willing to pay for each dollar of profit. A higher P/E indicates expectations of future growth, while a lower P/E might suggest undervaluation or lower growth expectations.',
'div_yield': 'Dividend yield is a financial ratio showing how much a company pays out in dividends each year relative to its stock price. A higher dividend yield means investors receive more income per dollar invested, while a lower yield indicates less immediate return but possibly more focus on reinvestment and growth.',
'ps_ratio': 'The P/S ratio (price-to-sales ratio) compares the stock price of a company to its total sales per share, showing how much investors are paying for each dollar of revenue. A lower P/S ratio may suggest undervaluation or better value, while a higher ratio indicates investors expect strong future sales growth.'}

class Explainer:
    
    def __init__(self):
        pass

    def get_explanation(self, to_explain):
        return explanations.get(to_explain, 'No explanation available for this string.')
