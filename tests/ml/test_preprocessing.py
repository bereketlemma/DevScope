"""Tests for ML feature engineering."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ml"))

import pandas as pd
from preprocessing import build_features


class TestBuildFeatures:
    def test_creates_lag_features(self):
        df = pd.DataFrame({
            "metric_date": pd.date_range("2026-01-01", periods=30),
            "metric_value": range(30),
        })
        result = build_features(df)
        assert "lag_1" in result.columns
        assert "lag_7" in result.columns
        assert "lag_14" in result.columns

    def test_creates_rolling_features(self):
        df = pd.DataFrame({
            "metric_date": pd.date_range("2026-01-01", periods=30),
            "metric_value": range(30),
        })
        result = build_features(df)
        assert "rolling_mean_7" in result.columns
        assert "rolling_std_14" in result.columns

    def test_creates_zscore(self):
        df = pd.DataFrame({
            "metric_date": pd.date_range("2026-01-01", periods=30),
            "metric_value": range(30),
        })
        result = build_features(df)
        assert "z_score_14" in result.columns

    def test_drops_nan_rows(self):
        df = pd.DataFrame({
            "metric_date": pd.date_range("2026-01-01", periods=30),
            "metric_value": range(30),
        })
        result = build_features(df)
        assert result.isna().sum().sum() == 0

    def test_minimum_output_rows(self):
        df = pd.DataFrame({
            "metric_date": pd.date_range("2026-01-01", periods=30),
            "metric_value": range(30),
        })
        result = build_features(df)
        # After dropping NaN from lag_14, should have 30 - 14 = 16 rows
        assert len(result) == 16
