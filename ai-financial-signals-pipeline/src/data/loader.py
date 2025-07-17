"""
Data ingestion module for public financial APIs.

Includes:
- get_equity_data: Fetches stock data via yfinance.
- get_crypto_data: Fetches crypto data via CoinGecko API.
- get_macro_data: Fetches macroeconomic indicators via FRED API.
"""

import pandas as pd
import yfinance as yf
from pycoingecko import CoinGeckoAPI
from fredapi import Fred

#API Key Imports
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.getenv("FRED_API_KEY")

# Initialize CoinGecko client
cg = CoinGeckoAPI()


def get_equity_data(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Fetches equity historical OHLCV data using Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL")
        period (str): Time period (e.g., "1y", "6mo")
        interval (str): Frequency ("1d", "1h", etc.)

    Returns:
        pd.DataFrame: OHLCV dataframe with datetime index.
    """
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    df.reset_index(inplace=True)
    return df


def get_crypto_data(symbol: str, days: int = 30) -> pd.DataFrame:
    """
    Fetches cryptocurrency market price data from CoinGecko.

    Args:
        symbol (str): CoinGecko coin ID (e.g., "bitcoin", "ethereum")
        days (int): Number of days of historical data

    Returns:
        pd.DataFrame: DataFrame with 'date' and 'price' columns.
    """
    data = cg.get_coin_market_chart_by_id(id=symbol, vs_currency="usd", days=days)
    prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    prices["date"] = pd.to_datetime(prices["timestamp"], unit="ms")
    prices.drop(columns=["timestamp"], inplace=True)
    return prices[["date", "price"]]


def get_macro_data(series_id: str, fred_api_key: str) -> pd.DataFrame:
    """
    Fetches macroeconomic time series from FRED.

    Args:
        series_id (str): FRED series code (e.g., "UNRATE", "FEDFUNDS")
        fred_api_key (str): Your FRED API key

    Returns:
        pd.DataFrame: DataFrame with 'date' and 'value'.
    """
    fred = Fred(api_key=fred_api_key)
    data = fred.get_series(series_id)
    df = data.reset_index()
    df.columns = ["date", "value"]
    return df
