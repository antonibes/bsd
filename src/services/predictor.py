import datetime

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class ExpensePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False

    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        features = pd.DataFrame()
        features['date'] = df['date']

        features['day_of_month'] = features['date'].dt.day
        features['day_of_week'] = features['date'].dt.dayofweek
        features['is_weekend'] = features['day_of_week'].isin([5, 6]).astype(int)

        features['is_month_start'] = (features['day_of_month'] <= 5).astype(int)
        features['is_month_end'] = (features['day_of_month'] >= 25).astype(int)

        features['time_index'] = (features['date'] - features['date'].min()).dt.days

        return features

    def train(self, historical_df: pd.DataFrame):
        expenses_df = historical_df[historical_df['amount'] < 0].copy()

        daily_expenses = expenses_df.groupby('date')['amount'].sum().reset_index()
        daily_expenses['amount'] = daily_expenses['amount'].abs()

        X_raw = self._engineer_features(daily_expenses)
        y = daily_expenses['amount'].values

        X = X_raw.drop(columns=['date'])
        X_scaled = self.scaler.fit_transform(X)

        self.model.fit(X_scaled, y)
        self.is_trained = True

    def predict_future(self, start_date: datetime.date, days_ahead: int = 30) -> pd.DataFrame:
        if not self.is_trained:
            raise ValueError("Model must be trained before predicting.")

        future_dates = [start_date + datetime.timedelta(days=i) for i in range(days_ahead)]
        future_df = pd.DataFrame({'date': pd.to_datetime(future_dates)})

        X_raw_future = self._engineer_features(future_df)
        X_future = X_raw_future.drop(columns=['date'])
        X_future_scaled = self.scaler.transform(X_future)

        predictions = self.model.predict(X_future_scaled)
        predictions = np.maximum(predictions, 0)

        future_df['predicted_expense'] = predictions
        return future_df
