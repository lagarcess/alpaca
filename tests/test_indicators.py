import numpy as np
import pandas as pd
import pytest

from market_data.indicators import IndicatorCalculator


@pytest.fixture
def calculator():
    return IndicatorCalculator()


@pytest.fixture
def sample_data():
    # Create sample OHLCV data
    # Create enough points for indicators to have values
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    df = pd.DataFrame(
        {
            "open": np.random.randn(100) + 100,
            "high": np.random.randn(100) + 105,
            "low": np.random.randn(100) + 95,
            "close": np.random.randn(100) + 100,
            "volume": np.random.randint(100, 1000, size=100),
        },
        index=dates,
    )
    return df


def test_discovery(calculator):
    supported = calculator.get_supported_indicators()
    assert len(supported) > 0
    assert "SMA" in supported
    assert "RSI" in supported


def test_add_no_indicators(calculator, sample_data):
    result = calculator.add_indicators(sample_data, [])
    assert result.equals(sample_data)


def test_add_sma(calculator, sample_data):
    # TA-Lib SMA defaults to 30 usually, we'll check logic
    # We specified logic to parse SMA_50
    result = calculator.add_indicators(sample_data, ["SMA_10"])
    assert "SMA_10" in result.columns
    # Check checks
    assert pd.notna(result["SMA_10"].iloc[-1])  # Should have value at end
    assert pd.isna(result["SMA_10"].iloc[0])  # Should be NaN at start (lookback)


def test_add_multiple(calculator, sample_data):
    result = calculator.add_indicators(sample_data, ["SMA_10", "RSI_14"])
    assert "SMA_10" in result.columns
    assert "RSI_14" in result.columns


def test_alignment(calculator):
    # Precise test for data alignment
    # Create a deterministic series: [1, 2, 3, 4, 5]
    # SMA_3 at index 2 (value 3) should be (1+2+3)/3 = 2
    df = pd.DataFrame(
        {
            "open": [1, 2, 3, 4, 5],
            "high": [1, 2, 3, 4, 5],
            "low": [1, 2, 3, 4, 5],
            "close": [1, 2, 3, 4, 5],
            "volume": [100, 100, 100, 100, 100],
        }
    )

    result = calculator.add_indicators(df, ["SMA_3"])

    # 0, 1 should be NaN
    assert pd.isna(result["SMA_3"].iloc[0])
    assert pd.isna(result["SMA_3"].iloc[1])

    # Index 2: (1+2+3)/3 = 2.0
    assert result["SMA_3"].iloc[2] == 2.0

    # Index 3: (2+3+4)/3 = 3.0
    assert result["SMA_3"].iloc[3] == 3.0
