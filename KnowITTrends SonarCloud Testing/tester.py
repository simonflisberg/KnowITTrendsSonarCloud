# test_data_agent.py

import unittest
import json
import requests
from datetime import datetime, timedelta
from unittest.mock import patch

from DataAgent import DataAgent
from StockData import StockData
from fmp import DataAPI

# ==========================
# Dummy classes for testing
# ==========================

# Dummy StockData for testing DataAgent without calling the real API.
class DummyStockData:
    def compilePriceData(self, symbol, start_date, end_date, price_types):
        return {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "price_types": price_types,
            "data": "price data"
        }

    def compileKeyFigures(self, symbol):
        return {
            "symbol": symbol,
            "key_figures": "some key figures"
        }

    def compileKeyInfo(self, symbol):
        return {
            "symbol": symbol,
            "company_profile": "company profile info"
        }


# Dummy DataAPI for testing StockData without making real API calls.
class DummyDataAPI:
    def getStockPrice(self, symbol, start_date, end_date):
        # Return a dummy response similar to what a real API might return.
        return {
            "historical": [
                {"date": "2025-01-01", "open": 100, "close": 110, "high": 115, "low": 95},
                {"date": "2025-01-02", "open": 101, "close": 111, "high": 116, "low": 96},
            ]
        }

    def getStockKeyFigures(self, symbol, requested_data):
        # Return a JSON string with each requested key set to a dummy value.
        return json.dumps({
            "symbol": symbol,
            "key_figures": {key: 1 for key in requested_data}
        })

    def getStockKeyInfo(self, symbol, requested_data):
        # Return a JSON string with each requested key set to a dummy string.
        return json.dumps({
            "symbol": symbol,
            "key_info": {key: f"value for {key}" for key in requested_data}
        })


class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json


# ==========================
# Test cases for DataAgent
# ==========================
class TestDataAgent(unittest.TestCase):
    def setUp(self):
        # Create a DataAgent instance and override its stockData with our dummy version.
        self.agent = DataAgent()
        self.agent.stockData = DummyStockData()

    def test_historic_price(self):
        symbol = "CRWD"
        price_types = ['open', 'close', 'high', 'low']
        years = 0.5

        result = self.agent.queryStock("historic_price", symbol, years=years, price_types=price_types)

        # Calculate expected dates based on the current date.
        expected_end_date = datetime.today().strftime('%Y-%m-%d')
        expected_start_date = (datetime.today() - timedelta(days=(365*years))).strftime('%Y-%m-%d')

        self.assertEqual(result["symbol"], symbol)
        self.assertEqual(result["price_types"], price_types)
        self.assertEqual(result["start_date"], expected_start_date)
        self.assertEqual(result["end_date"], expected_end_date)
        self.assertEqual(result["data"], "price data")

    def test_key_figures(self):
        symbol = "CRWD"
        result = self.agent.queryStock("key_figures", symbol)
        self.assertEqual(result["symbol"], symbol)
        self.assertEqual(result["key_figures"], "some key figures")

    def test_company_profile(self):
        symbol = "CRWD"
        result = self.agent.queryStock("company_profile", symbol)
        self.assertEqual(result["symbol"], symbol)
        self.assertEqual(result["company_profile"], "company profile info")

    def test_invalid_data_type(self):
        symbol = "CRWD"
        result = self.agent.queryStock("invalid", symbol)
        self.assertEqual(result, {})


# ==========================
# Test cases for StockData
# ==========================
class TestStockData(unittest.TestCase):
    def setUp(self):
        # Create a StockData instance and override its dataApi with our dummy.
        self.stock_data = StockData()
        self.stock_data.dataApi = DummyDataAPI()

    def test_compile_price_data(self):
        symbol = "CRWD"
        start_date = "2025-01-01"
        end_date = "2025-01-02"
        # Test with only a subset of price types.
        price_types = ['open', 'close']
        result = self.stock_data.compilePriceData(symbol, start_date, end_date, price_types)
        # The method returns a JSON string; parse it for testing.
        data = json.loads(result)
        expected = {
            "2025-01-01": {"open": 100, "close": 110},
            "2025-01-02": {"open": 101, "close": 111},
        }
        self.assertEqual(data, expected)

    def test_compile_key_figures(self):
        symbol = "CRWD"
        result = self.stock_data.compileKeyFigures(symbol)
        # Parse the JSON string.
        data = json.loads(result)
        self.assertEqual(data["symbol"], symbol)
        # Since the dummy returns 1 for every key, ensure that each key's value is 1.
        for value in data["key_figures"].values():
            self.assertEqual(value, 1)

    def test_compile_key_info(self):
        symbol = "CRWD"
        result = self.stock_data.compileKeyInfo(symbol)
        data = json.loads(result)
        self.assertEqual(data["symbol"], symbol)
        # Check that each value in key_info starts with the expected text.
        for key, value in data["key_info"].items():
            self.assertTrue(value.startswith("value for"))

    # Exception handling tests for StockData methods.
    def test_compile_price_data_exception(self):
        # Override getStockPrice to raise an exception.
        self.stock_data.dataApi.getStockPrice = lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Test exception"))
        result = self.stock_data.compilePriceData("CRWD", "2025-01-01", "2025-01-02", ['open', 'close'])
        self.assertEqual(result, {})

    def test_compile_key_figures_exception(self):
        # Override getStockKeyFigures to raise an exception.
        self.stock_data.dataApi.getStockKeyFigures = lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Test exception"))
        result = self.stock_data.compileKeyFigures("CRWD")
        self.assertEqual(result, {})

    def test_compile_key_info_exception(self):
        # Override getStockKeyInfo to raise an exception.
        self.stock_data.dataApi.getStockKeyInfo = lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Test exception"))
        result = self.stock_data.compileKeyInfo("CRWD")
        self.assertEqual(result, {})


# ==========================
# Test cases for DataAPI
# ==========================
class TestDataAPI(unittest.TestCase):
    def setUp(self):
        self.api = DataAPI()

    # Tests for getStockKeyInfo
    @patch('DataAPI.requests.get')
    def test_getStockKeyInfo_all(self, mock_get):
        dummy_data = [{"symbol": "AAPL", "ceo": "Tim Cook", "industry": "Tech"}]
        mock_get.return_value = DummyResponse(dummy_data)
        result = self.api.getStockKeyInfo("AAPL", requested_data=["all"])
        self.assertEqual(result, dummy_data[0])

    @patch('DataAPI.requests.get')
    def test_getStockKeyInfo_specific(self, mock_get):
        dummy_data = [{"symbol": "AAPL", "ceo": "Tim Cook", "industry": "Tech"}]
        mock_get.return_value = DummyResponse(dummy_data)
        result = self.api.getStockKeyInfo("AAPL", requested_data=["ceo", "industry"])
        expected = {"ceo": "Tim Cook", "industry": "Tech"}
        self.assertEqual(result, expected)

    @patch('DataAPI.requests.get')
    def test_getStockKeyInfo_specific_missing(self, mock_get):
        dummy_data = [{"symbol": "AAPL", "ceo": "Tim Cook", "industry": "Tech"}]
        mock_get.return_value = DummyResponse(dummy_data)
        # Requesting a key that doesn't exist along with one that does.
        result = self.api.getStockKeyInfo("AAPL", requested_data=["ceo", "nonexistent"])
        # Since not all requested keys are found, the method returns the full dictionary.
        self.assertEqual(result, dummy_data[0])

    @patch('DataAPI.requests.get')
    def test_getStockKeyInfo_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test exception")
        result = self.api.getStockKeyInfo("AAPL", requested_data=["all"])
        self.assertEqual(result, {})

    # Tests for getStockPrice
    @patch('DataAPI.requests.get')
    def test_getStockPrice_success(self, mock_get):
        dummy_data = {"historical": [
            {"date": "2025-01-01", "open": 100, "close": 110, "high": 115, "low": 95}
        ]}
        mock_get.return_value = DummyResponse(dummy_data)
        result = self.api.getStockPrice("AAPL", "2025-01-01", "2025-01-02")
        self.assertEqual(result, dummy_data)

    @patch('DataAPI.requests.get')
    def test_getStockPrice_no_historical(self, mock_get):
        dummy_data = {}
        mock_get.return_value = DummyResponse(dummy_data)
        result = self.api.getStockPrice("AAPL", "2025-01-01", "2025-01-02")
        self.assertEqual(result, {})

    @patch('DataAPI.requests.get')
    def test_getStockPrice_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test exception")
        result = self.api.getStockPrice("AAPL", "2025-01-01", "2025-01-02")
        self.assertEqual(result, {})

    # Tests for getStockKeyFigures
    @patch('DataAPI.requests.get')
    def test_getStockKeyFigures_all(self, mock_get):
        dummy_data = [{"revenuePerShareTTM": 1, "netIncomePerShareTTM": 2}]
        mock_get.return_value = DummyResponse(dummy_data)
        result = self.api.getStockKeyFigures("AAPL", requested_data=["all"])
        self.assertEqual(json.loads(result), dummy_data[0])

    @patch('DataAPI.requests.get')
    def test_getStockKeyFigures_specific(self, mock_get):
        dummy_data = [{"revenuePerShareTTM": 1, "netIncomePerShareTTM": 2}]
        mock_get.return_value = DummyResponse(dummy_data)
        result = self.api.getStockKeyFigures("AAPL", requested_data=["revenuePerShareTTM"])
        expected = {"revenuePerShareTTM": 1}
        self.assertEqual(json.loads(result), expected)

    @patch('DataAPI.requests.get')
    def test_getStockKeyFigures_specific_missing(self, mock_get):
        dummy_data = [{"revenuePerShareTTM": 1, "netIncomePerShareTTM": 2}]
        mock_get.return_value = DummyResponse(dummy_data)
        result = self.api.getStockKeyFigures("AAPL", requested_data=["revenuePerShareTTM", "nonexistent"])
        # Since not all keys are found, the full dictionary is returned.
        self.assertEqual(json.loads(result), dummy_data[0])

    @patch('DataAPI.requests.get')
    def test_getStockKeyFigures_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test exception")
        result = self.api.getStockKeyFigures("AAPL", requested_data=["all"])
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
