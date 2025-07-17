"""
Visualization utilities for financial signals pipeline.

Includes:
- plot_cumulative_returns: Strategy vs market performance.
- plot_signal_distribution: Distribution of signal values.
- plot_signal_correlation: Heatmap of signal correlations.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_cumulative_returns(df: pd.DataFrame, strategy_col: str = 'strategy_returns', market_col: str = 'returns'):
    """
    Plots cumulative returns of strategy vs market.
    """
    df = df.copy()
    df['cum_strategy'] = (1 + df[strategy_col].fillna(0)).cumprod()
    df['cum_market'] = (1 + df[market_col].fillna(0)).cumprod()

    plt.figure(figsize=(10, 5))
    plt.plot(df['cum_strategy'], label='Strategy')
    plt.plot(df['cum_market'], label='Market (Buy & Hold)')
    plt.title('Cumulative Returns')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_signal_distribution(df: pd.DataFrame, signal_cols: list):
    """
    Plots histogram distribution of signal columns.
    """
    df = df.copy()
    df[signal_cols].hist(bins=30, figsize=(12, 6))
    plt.tight_layout()
    plt.show()


def plot_signal_correlation(df: pd.DataFrame, signal_cols: list):
    """
    Plots correlation heatmap of signal features.
    """
    corr = df[signal_cols].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Signal Feature Correlation Heatmap')
    plt.tight_layout()
    plt.show()
