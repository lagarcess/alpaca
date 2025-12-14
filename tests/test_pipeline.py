import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from market_data.pipeline import StockDataPipeline


class TestStockDataPipeline(unittest.TestCase):
    def setUp(self):
        self.output_dir = Path("tests/test_data")
        self.pipeline = StockDataPipeline(output_dir=str(self.output_dir))

    def tearDown(self):
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

    def test_calculate_lookback(self):
        # SMA_50 -> 50 * 2 = 100
        self.assertEqual(self.pipeline._calculate_lookback_bars(["SMA_50"]), 100)
        # Multiple, take max (RSI_14, SMA_50) -> 100
        self.assertEqual(
            self.pipeline._calculate_lookback_bars(["RSI_14", "SMA_50"]), 100
        )
        # No implicit -> default logic (e.g. 60)
        self.assertEqual(self.pipeline._calculate_lookback_bars(["SMA"]), 60)
        # Empty -> 0
        self.assertEqual(self.pipeline._calculate_lookback_bars([]), 0)

    @patch("market_data.client.AlpacaClient")
    def test_process_ticker_warmup_logic(self, MockClient):
        # Mock the client instance
        mock_client_instance = MockClient.return_value
        self.pipeline.client = mock_client_instance

        # Setup mock data: 100 days of data
        # Request start: Day 50.
        # Warmup: Should fetch earlier.

        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
        mock_bars = []
        for d in dates:
            mock_bars.append(
                {
                    "t": d.isoformat(),
                    "o": 100.0,
                    "h": 105.0,
                    "l": 95.0,
                    "c": 100.0,
                    "v": 1000,
                }
            )

        mock_client_instance.get_stock_bars.return_value = mock_bars

        # We request from 2023-02-20 (Day 50)
        target_start = "2023-02-20"

        # Execute
        path = self.pipeline.process_ticker(
            ticker="TEST",
            timeframe="1Day",
            start_date=target_start,
            indicators=["SMA_10"],
        )

        # Verify call to get_stock_bars used an earlier date than target_start
        # call_args[1] is kwargs
        call_kwargs = mock_client_instance.get_stock_bars.call_args[1]
        called_start = call_kwargs["start"]

        # Check that called_start < target_start (string comparison works for ISO)
        self.assertLess(called_start, target_start)

        # Verify Output
        self.assertTrue(path.exists())

        df = pd.read_csv(path)

        # Verify first row date is >= target_start
        # CSV writes ISO dates? Pandas read_csv logic...
        first_date = df["date"].iloc[0]
        # Allow equality or simply greater
        # "2023-02-20..." >= "2023-02-20"
        self.assertTrue(first_date >= target_start)

        # Verify SMA_10 is calculated and NOT NaN at the very first exported row
        # Because we had mock data prior to it!
        # Convert column to numeric just in case
        sma_val = df["SMA_10"].iloc[0]
        self.assertTrue(
            pd.notna(sma_val),
            f"SMA_10 should not be NaN at start date {first_date} if warm-up worked",
        )
