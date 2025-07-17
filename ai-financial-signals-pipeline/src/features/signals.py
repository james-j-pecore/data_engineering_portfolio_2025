"""
Signal engineering module for alpha factor generation.

Includes:
- add_sma: Simple Moving Average
- add_rsi: Relative Strength Index
- add_momentum: Price momentum
- add_macd: Moving Average Convergence Divergence
"""

# Imports
import pandas as pd
import numpy as np

def _get_price_column(df: pd.DataFrame) -> str:
    """
    Helper function to find the price or close column in a DataFrame.
    Returns:
        str: Name of the column to use for price-based calculations.
    Raises:
        KeyError: If no suitable column is found.
    """
    for candidate in ['close', 'Close', 'price']:
        if candidate in df.columns:
            return candidate
    raise KeyError(f"No 'close', 'Close', or 'price' column found in {df.columns}")


def add_sma(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Adds Simple Moving Average (SMA) column to DataFrame.
    """
    col = _get_price_column(df)
    df[f'sma_{window}'] = df[col].rolling(window=window).mean()
    return df


def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Adds Relative Strength Index (RSI) column to DataFrame.
    """
    col = _get_price_column(df)
    delta = df[col].diff()

    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    # Flatten to avoid shape errors
    gain = pd.Series(gain.flatten())
    loss = pd.Series(loss.flatten())

    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()

    rs = avg_gain / (avg_loss + 1e-10)
    df[f'rsi_{window}'] = 100 - (100 / (1 + rs))
    return df



def add_momentum(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    """
    Adds Momentum column to DataFrame.
    """
    col = _get_price_column(df)
    df[f'momentum_{window}'] = df[col] - df[col].shift(window)
    return df


def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """
    Adds MACD and MACD Signal Line columns to DataFrame.
    """
    col = _get_price_column(df)
    ema_fast = df[col].ewm(span=fast, adjust=False).mean()
    ema_slow = df[col].ewm(span=slow, adjust=False).mean()
    df['macd'] = ema_fast - ema_slow
    df['macd_signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
    return df