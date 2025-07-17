"""
Simple backtesting framework for rule-based trading strategies.
"""

import pandas as pd
from src.features.signals import add_sma

def simple_strategy_signals(df: pd.DataFrame, rsi_low=40, rsi_high=60, sma_window=20) -> pd.DataFrame:
    """
    Simple strategy: Long if RSI < rsi_low and price > SMA, Short if RSI > rsi_high and price < SMA.
    """
    df = df.copy()
    df = add_sma(df, window=sma_window)  # reuse your sma function
    
    col = 'close' if 'close' in df.columns else 'price'
    df['position'] = 0
    df.loc[(df['rsi_14'] < rsi_low) & (df[col] > df[f'sma_{sma_window}']), 'position'] = 1
    df.loc[(df['rsi_14'] > rsi_high) & (df[col] < df[f'sma_{sma_window}']), 'position'] = -1
    df['position'] = df['position'].shift(1)  # realistic next-day execution
    return df



def backtest_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates strategy returns based on positions.
    """
    col = next((c for c in df.columns if c.lower() == 'close'), 'price')
    df = df.copy()
    df['returns'] = df[col].pct_change()
    df['strategy_returns'] = df['position'] * df['returns']
    return df


def summarize_performance(df: pd.DataFrame) -> dict:
    """
    Computes simple performance metrics.
    """
    total_return = df['strategy_returns'].sum()
    sharpe = (df['strategy_returns'].mean() / (df['strategy_returns'].std() + 1e-10)) * (252 ** 0.5)
    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe
    }
