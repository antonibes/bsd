import datetime

import pandas as pd
import pytest

from src.services.predictor import ExpensePredictor


def test_feature_engineering():
    # Arrange
    dates = pd.date_range(start="2026-03-01", end="2026-03-05") # Sunday to Thursday
    df = pd.DataFrame({'date': dates})

    predictor = ExpensePredictor()

    # Act
    features = predictor._engineer_features(df)

    # Assert
    assert 'day_of_month' in features.columns
    assert 'is_weekend' in features.columns
    # March 1 is a Sunday (weekend = 1)
    assert features.loc[0, 'is_weekend'] == 1
    # March 2 is Monday (weekend = 0)
    assert features.loc[1, 'is_weekend'] == 0

def test_training_and_prediction():
    predictor = ExpensePredictor()

    # 1. Provide mock historical expenses
    dates = pd.date_range(start="2025-01-01", end="2025-12-31")
    # Simulate $100 everyday, with a $50 weekend bump (total 150)
    amounts = [-150 if d.weekday() >= 5 else -100 for d in dates]

    historical_df = pd.DataFrame({
        'date': dates,
        'amount': amounts
    })

    # Act
    predictor.train(historical_df)
    assert predictor.is_trained is True

    # Predict next week
    next_week_start = datetime.date(2026, 1, 1)
    predictions = predictor.predict_future(next_week_start, days_ahead=7)

    # Assert
    assert len(predictions) == 7
    assert 'predicted_expense' in predictions.columns
    # We expect predictions to be positive numbers
    assert all(predictions['predicted_expense'] > 0)

def test_predict_fails_if_not_trained():
    predictor = ExpensePredictor()
    with pytest.raises(ValueError):
         predictor.predict_future(datetime.date.today(), days_ahead=5)
