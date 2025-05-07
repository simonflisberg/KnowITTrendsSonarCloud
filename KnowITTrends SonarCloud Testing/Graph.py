import numpy as np
import pandas as pd
import json
from BananAI import BananAI

class Graph:
  _ai = BananAI()
  def getLinearTrend(self,
                     datapoints: dict,
                     length: int = 0,
                     date_col: str = "date",
                     price_col: str = "close",
                     yearly: bool = False

  ):
    """
    Calculates the trendline (e.g. slope and intercept) for a given a set of datapoints. CURRENTLY RETURNS THE DAILY PRICE CORRESPONDING TO THE TREND

    Args:
      datapoints (dict): A dictionary of timestamps and prices
      length (int): The number of datapoints that are analyzed to give the trendline. 
                    length=0 gives the trend for the whole set of datapoints.
      date_col (str): The key for the date column in the dataset.
      price_col (str): The key for the price column to analyze.
      yearly (bool): Calculates trend for yearly data instead of the default - daily.
    
    Returns:
      out (json): Contains the keys "slope" and "intercept"
    """
    date_format = "%Y" if yearly else "%Y-%m-%d"

    if isinstance(datapoints, str):
      datapoints = json.loads(datapoints) # ensure datapoints are formatted as dict

    df = pd.DataFrame([{date_col: entry[date_col], price_col: entry[price_col] } for entry in datapoints["historical"]]) # extract only date and closing price

    df.reset_index(inplace=True) # set index
    df.rename(columns={"index": date_col}) # correct the naming of date
    
    if yearly:
      df[date_col] = df[date_col].astype(int)  # Ensure years are integers
    else:
      df[date_col] = pd.to_datetime(df[date_col], format=date_format) # format date as datetime
    
    df = df.sort_values(date_col, ascending=False)
    
    if length > 0:
      df = df.head(length)  # limit to the requested "length" of data points
    
    start_date = df[date_col].iloc[-1] # set start date

    if yearly:
      df["numeric_date"] = df[date_col] - start_date
    else:
      df["numeric_date"] = (df[date_col] - start_date) // pd.Timedelta("1D") # create column representing the days since start of data from current datapoint

    slope, intercept = np.polyfit(df["numeric_date"], df[price_col], 1) # calculate trend (based on only close price)
    df["trend"] = intercept+ (slope * df["numeric_date"]) # current version for graph
    
    if not yearly:
      df[date_col] = df[date_col].dt.strftime(date_format) # revert date formatting for output
  
    json_data = df[[date_col, "trend"]].to_json(orient="records", date_format="iso")

    return json_data

