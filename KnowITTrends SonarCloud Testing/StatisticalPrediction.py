import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class StatisticalPrediction:
    def create_fourier_terms(self, index, period, order):
        t = np.arange(len(index))
        terms = {}
        for i in range(1, order + 1):
            terms[f'sin_{period}_{i}'] = np.sin(2 * np.pi * i * t / period)
            terms[f'cos_{period}_{i}'] = np.cos(2 * np.pi * i * t / period)
        return pd.DataFrame(terms, index=index)
    
    def SARIMA(self, datapoints, interval):
        """
        Build and forecast using the SARIMAX model.
        For daily data, add Fourier terms to capture multiple seasonalities.
        """
        # Define interval mapping: frequency, historical offset, forecast steps, and seasonal period
        freq_map = {
            'daily':    ('D', pd.DateOffset(days=120), 30, 7),      # Daily: 120 days history, 30-day forecast, weekly seasonality (default)
            'weekly':   ('W', pd.DateOffset(weeks=52), 12, 52),       # Weekly: 52 weeks history, 12-week forecast, annual seasonality
            'monthly':  ('MS', pd.DateOffset(months=60), 12, 12),       # Monthly: 60 months history, 12-month forecast, annual seasonality
            'quarterly':('QS', pd.DateOffset(years=5), 8, 4),           # Quarterly: 5 years history, 8-quarter forecast, quarterly seasonality
            'yearly':   ('YS', pd.DateOffset(years=20), 5, 1)           # Yearly: 20 years history, 5-year forecast, no seasonal component (handled separately)
        }
        interval = interval.lower()
        if interval not in freq_map:
            return {"Error": "Interval out of range when calling StatisticalPrediction.SARIMA"}
        
        freq, hist_offset, forecast_steps, seasonal_period = freq_map[interval]
        
        # Create DataFrame from historical data
        df = pd.DataFrame(datapoints["historical"])
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
        elif "year" in df.columns:
            df["year"] = pd.to_datetime(df["year"], format="%Y")
            df.set_index("year", inplace=True)
        else:
            raise ValueError("Data must include either a 'date' or 'year' column")
        
        df.sort_index(inplace=True)
        df = df.asfreq(freq)
        df = df.dropna(subset=["value"])
        
        if interval == 'daily':
            # Add Fourier terms for multiple seasonalities (weekly, monthly, yearly)
            fourier_weekly = self.create_fourier_terms(df.index, period=7, order=2)
            fourier_monthly = self.create_fourier_terms(df.index, period=30, order=2)
            fourier_yearly = self.create_fourier_terms(df.index, period=365, order=2)
            exog = pd.concat([fourier_weekly, fourier_monthly, fourier_yearly], axis=1)
            seasonal_order_used = (0, 0, 0, 0)  # Fourier terms capture seasonality
        else:
            exog = None
            seasonal_order_used = (1, 1, 1, seasonal_period)
        
        # Build and fit the model
        if interval == 'daily':
            model = SARIMAX(df["value"],
                            order=(1, 1, 1),
                            seasonal_order=seasonal_order_used,
                            exog=exog,
                            enforce_stationarity=False,
                            enforce_invertibility=False)
        else:
            model = SARIMAX(df["value"],
                            order=(1, 1, 1),
                            seasonal_order=seasonal_order_used,
                            enforce_stationarity=False,
                            enforce_invertibility=False)
        model_fit = model.fit(disp=False)
        
        # Forecast using the appropriate model (with Fourier terms for daily)
        if interval == 'daily':
            forecast_index = pd.date_range(start=df.index[-1] + pd.tseries.frequencies.to_offset(freq),
                                           periods=forecast_steps, freq=freq)
            fourier_weekly_fc = self.create_fourier_terms(forecast_index, period=7, order=2)
            fourier_monthly_fc = self.create_fourier_terms(forecast_index, period=30, order=2)
            fourier_yearly_fc = self.create_fourier_terms(forecast_index, period=365, order=2)
            exog_forecast = pd.concat([fourier_weekly_fc, fourier_monthly_fc, fourier_yearly_fc], axis=1)
            forecast_values = model_fit.get_forecast(steps=forecast_steps, exog=exog_forecast).predicted_mean
        else:
            forecast_values = model_fit.forecast(steps=forecast_steps)
        
        # Compute recent volatility and scale uncertainty using square-root of horizon
        changes = df["value"].diff().dropna()
        recent_volatility = changes.ewm(span=12, adjust=False).std().iloc[-1]
        multiplier = 1
        step_multipliers = pd.Series(np.sqrt(np.arange(1, forecast_steps + 1)), index=forecast_values.index)
        optimistic_forecast = forecast_values + multiplier * recent_volatility * step_multipliers
        pessimistic_forecast = forecast_values - multiplier * recent_volatility * step_multipliers
        
        future_dates = pd.date_range(start=df.index[-1] + pd.tseries.frequencies.to_offset(freq),
                                     periods=forecast_steps, freq=freq)
        return {
            "forecast": forecast_values,
            "optimistic": optimistic_forecast,
            "pessimistic": pessimistic_forecast,
            "future_dates": future_dates
        }
    
    def ExponentialSmoothingForecast(self, datapoints, forecast_steps):
        """
        Build and forecast using the Exponential Smoothing model.
        This method is tailored for yearly data where fewer data points may be available.
        """
        # Prepare yearly data
        df = pd.DataFrame(datapoints["historical"])
        if "year" in df.columns:
            df["year"] = pd.to_datetime(df["year"], format="%Y")
            df.set_index("year", inplace=True)
        elif "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
        else:
            raise ValueError("Data must include either a 'year' or 'date' column")
        
        df.sort_index(inplace=True)
        df = df.asfreq('YS')
        df = df.dropna(subset=["value"])
        
        model = ExponentialSmoothing(df["value"], trend='add', seasonal=None)
        model_fit = model.fit(optimized=True)
        forecast_values = model_fit.forecast(steps=forecast_steps)
        
        changes = df["value"].diff().dropna()
        recent_volatility = changes.ewm(span=12, adjust=False).std().iloc[-1]
        multiplier = 1
        step_multipliers = pd.Series(np.sqrt(np.arange(1, forecast_steps + 1)), index=forecast_values.index)
        optimistic_forecast = forecast_values + multiplier * recent_volatility * step_multipliers
        pessimistic_forecast = forecast_values - multiplier * recent_volatility * step_multipliers
        
        last_date = df.index[-1]
        future_dates = pd.date_range(start=last_date + pd.tseries.frequencies.to_offset('YS'),
                                     periods=forecast_steps, freq='YS')
        
        return {
            "forecast": forecast_values,
            "optimistic": optimistic_forecast,
            "pessimistic": pessimistic_forecast,
            "future_dates": future_dates
        }
    
    def CreatePNG(self, datapoints, png_name, interval):
        """
        Generate a PNG plot of the forecast along with the uncertainty bounds.
        Uses the SARIMA method for non-yearly intervals and the Exponential Smoothing
        method for yearly forecasts.
        """
        # Mapping for intervals
        freq_map = {
            'daily':    ('D', pd.DateOffset(days=120), 30, 7),
            'weekly':   ('W', pd.DateOffset(weeks=52), 12, 52),
            'monthly':  ('MS', pd.DateOffset(months=60), 12, 12),
            'quarterly':('QS', pd.DateOffset(years=5), 8, 4),
            'yearly':   ('YS', pd.DateOffset(years=20), 5, 1)
        }
        interval = interval.lower()
        if interval not in freq_map:
            raise ValueError("Interval must be one of 'daily', 'weekly', 'monthly', 'quarterly', or 'yearly'")
        freq, hist_offset, forecast_steps, _ = freq_map[interval]
        
        # Prepare the historical data for plotting
        df = pd.DataFrame(datapoints["historical"])
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
        elif "year" in df.columns:
            df["year"] = pd.to_datetime(df["year"], format="%Y")
            df.set_index("year", inplace=True)
        else:
            raise ValueError("Data must include either a 'date' or 'year' column")
        df.sort_index(inplace=True)
        df = df.asfreq(freq)
        df = df.dropna(subset=["value"])
        
        start_plot = df.index[-1] - hist_offset
        df_plot = df.loc[df.index >= start_plot]
        
        # Choose forecasting method based on the interval
        if interval == 'yearly':
            forecast_results = self.ExponentialSmoothingForecast(datapoints, forecast_steps)
        else:
            forecast_results = self.SARIMA(datapoints, interval)

        future_dates = forecast_results["future_dates"]
        forecast_values = forecast_results["forecast"]
        optimistic_forecast = forecast_results["optimistic"]
        pessimistic_forecast = forecast_results["pessimistic"]

        # Create the plot
        plt.figure(figsize=(12, 6))
        plt.plot(df_plot.index, df_plot["value"], label='Historical Data')
        plt.axvline(df.index[-1], color='gray', linestyle='--', label='Forecast Start')
        plt.plot(future_dates, forecast_values, label='Forecast', color='green')
        plt.plot(future_dates, optimistic_forecast, label='Optimistic Forecast', color='green', linestyle='--')
        plt.plot(future_dates, pessimistic_forecast, label='Pessimistic Forecast', color='red', linestyle='--')
        plt.fill_between(future_dates, forecast_values, optimistic_forecast,
                         where=(optimistic_forecast >= forecast_values), color='green', alpha=0.3, interpolate=True)
        plt.fill_between(future_dates, forecast_values, pessimistic_forecast,
                         where=(pessimistic_forecast <= forecast_values), color='red', alpha=0.3, interpolate=True)
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title(f'Forecast ({interval.capitalize()})')
        plt.legend()
        plt.savefig(f"temp/{png_name}.png")
