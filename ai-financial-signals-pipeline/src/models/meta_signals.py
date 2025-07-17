"""
Meta-signals model layer for AI-enhanced financial strategy.

Includes:
- train_meta_model: Trains XGBoost classifier on signal features.
- predict_positions: Uses trained model to predict next-day position.
"""

import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def prepare_ml_features(df: pd.DataFrame, signal_cols: list, return_col: str = 'returns', threshold: float = 0.0):
    """
    Prepares X (features) and y (labels) for ML model.
    Label = 1 if next-day return > threshold, else 0.
    """
    df = df.copy()
    df['target'] = (df[return_col].shift(-1) > threshold).astype(int)
    df.dropna(subset=signal_cols + ['target'], inplace=True)

    X = df[signal_cols]
    y = df['target']
    return X, y


def train_meta_model(X, y, test_size=0.2, random_state=42):
    """
    Trains XGBoost classifier on provided features and target.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    model = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    return model


def predict_positions(df: pd.DataFrame, model, signal_cols: list):
    """
    Applies trained model to DataFrame to generate predicted positions (+1/-1).
    """
    df = df.copy()
    df['predicted_prob'] = model.predict_proba(df[signal_cols].fillna(0))[:, 1]
    df['predicted_position'] = np.where(df['predicted_prob'] > 0.5, 1, -1)
    return df
