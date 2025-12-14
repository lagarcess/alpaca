import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd

from market_data.client import AlpacaClient
from market_data.indicators import IndicatorCalculator

logger = logging.getLogger("rich")


class StockDataPipeline:
    """
    Orchestrates the data fetching, processing, and exporting pipeline.
    Handles 'warm-up' periods for technical indicators to ensure data accuracy.
    """

    def __init__(self, output_dir: str = "data"):
        self.client = AlpacaClient()
        self.calculator = IndicatorCalculator()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _calculate_lookback_bars(self, indicators: List[str]) -> int:
        """
        Determines the number of warm-up bars needed based on the requested indicators.
        Default heuristic: max_period * 2.
        """
        max_period = 0
        for ind in indicators:
            parts = ind.split("_")
            # Look for explicit period in name (e.g., SMA_50)
            if len(parts) > 1 and parts[1].isdigit():
                period = int(parts[1])
                max_period = max(max_period, period)

        # Default fallback if no periods found or period is 0
        # (e.g. just "SMA" uses default 30)
        if max_period == 0 and indicators:
            max_period = (
                30  # TA-Lib default 30 for some, 14 for others. 30 is safe-ish.
            )

        return max_period * 2 if max_period > 0 else 0

    def process_ticker(
        self,
        ticker: str,
        timeframe: str,
        start_date: str,
        end_date: Optional[str] = None,
        indicators: Optional[List[str]] = None,
    ) -> Path:
        """
        Fetches data, calculates indicators, and writes to CSV.

        Args:
            ticker: Stock symbol.
            timeframe: Alpaca timeframe string (e.g. '1Day', '15Min').
            start_date: ISO start date string (YYYY-MM-DD).
            end_date: ISO end date string.
            indicators: List of indicator strings (e.g. 'SMA_50').

        Returns:
            Path to the generated CSV file.
        """
        indicators = indicators or []

        # 1. Calculate Warm-up
        # Note: Proper date math for "50 bars ago" is hard without a market calendar.
        # Simple heuristic: Fetch more data than we think we need.
        # For '1Day', 1 bar ~ 1 day. For '1Min', 1 bar ~ 1 min.
        # We will iterate backwards? Or just ask Alpaca for 'limit' bars
        # ending at start_date?
        # Alpaca /bars endpoint supports 'start' and 'end'.

        # Use a safe buffer.
        # If we just fetch requested range, the first N rows are invalid.
        # We need to fetch (Start - Buffer) to End.
        # Since we don't have easy calendar math here, we'll use a simplification:
        # We fetch the requested range + X bars PRIOR.
        # But Alpaca pagination is forward.
        # Alternative: We always fetch from (Start - Delta).
        # Delta depends on timeframe.

        # For this phase, let's implement a 'days' based buffer heuristic for
        # daily data,
        # and maybe just warn for intraday or assume user gives us a buffered start?
        # Requirement said: "Calculate indicators on the combined dataset...
        # then slice off".

        # Let's adjust start_date.
        # For now, simplistic 'days' subtraction for 1Day.
        actual_start_date = start_date

        if indicators and timeframe == "1Day":
            lookback_bars = self._calculate_lookback_bars(indicators)
            if lookback_bars > 0:
                # Sub 2x lookback days (counting weekends/holidays, 2x is
                # usually safe buffer)
                # Actually 4x to be safe for weekends?
                start_dt = datetime.fromisoformat(start_date)
                # This is a naive subtraction, robust solution needs market calendar
                # But sticking to Requirement "robust data processing",
                # we'll do best effort with datetime
                from datetime import timedelta

                # 1.5 * lookback * (7/5) to account for invalid days?
                # Let's just do lookback * 3 days.
                delta = timedelta(days=lookback_bars * 3)
                warmup_start_dt = start_dt - delta
                actual_start_date = warmup_start_dt.date().isoformat()
                logger.info(
                    f"Warm-up: Fetching data from {actual_start_date} "
                    f"(Requested: {start_date})"
                )

        # 2. Fetch Data
        # We likely need pagination loop here if range is huge.
        # Fortunately AlpacaClient handles pagination but returns a List.
        # Ideally we stream, but step 1 is functionality.
        logger.info(f"Processing {ticker}...")
        bars = self.client.get_stock_bars(
            tickers=[ticker],
            timeframe=timeframe,
            limit=10000,  # Large limit to minimize pages
            start=actual_start_date,
            end=end_date,
        )

        if not bars:
            logger.warning(
                f"No data found for {ticker} (Range: {actual_start_date} to "
                f"{end_date}). Check if ticker is valid or market was open."
            )
            return None

        # 3. Convert to DataFrame
        df = pd.DataFrame(bars)
        # Rename columns to standard names for IndicatorCalculator
        # Alpaca: t, o, h, l, c, v
        df.rename(
            columns={
                "t": "date",
                "o": "open",
                "h": "high",
                "l": "low",
                "c": "close",
                "v": "volume",
            },
            inplace=True,
        )
        # Ensure date is index? Or keep as column?
        # Indicators usually don't care about index, just order.

        # 4. Calculate Indicators
        df = self.calculator.add_indicators(df, indicators)

        # 5. Slice off Warm-up
        # original start_date string comparison.
        # Ensure 'date' column is datetime-like or consistent string.
        # Alpaca returns 't' as ISO string usually.
        # Let's assume string comparison works if strict ISO8601.

        # Allow exact match or greater.
        # "2023-01-01" vs "2023-01-01T09:30:00Z"
        # Simple string comparison: row['date'] >= start_date
        mask = df["date"] >= start_date
        final_df = df.loc[mask].copy()

        if final_df.empty:
            logger.warning(
                f"All data was in warm-up period. None remaining after "
                f"slice for {ticker}."
            )
            return None

        # 6. Export to CSV
        filename = f"{ticker}_{timeframe}_{start_date}_{end_date or 'latest'}.csv"
        # Sanitize filename?
        filename = filename.replace(":", "-")
        filepath = self.output_dir / filename

        # Reorder columns explicitly
        # Desired: date, open, high, low, close, volume, trade_count, vwap, [indicators]

        # Ensure we have all base columns
        base_cols = ["date", "open", "high", "low", "close", "volume"]

        # Alpaca extra fields 'n' (trade count) and 'vw' (vwap) usually exist.
        # Check if they exist in df before adding to list.
        # Note: We renamed t->date, o->open, etc. 'n' and 'vw' are likely
        # still 'n' and 'vw'
        # unless we want to rename them too. User asked "where n and vw came from".
        # Let's rename them for clarity if present.

        if "n" in final_df.columns:
            final_df.rename(columns={"n": "trade_count"}, inplace=True)
            base_cols.append("trade_count")
        if "vw" in final_df.columns:
            final_df.rename(columns={"vw": "vwap"}, inplace=True)
            base_cols.append("vwap")

        # Get indicator columns (all cols that are NOT in base_cols/renamed)
        # However, final_df might have other cols?

        # Actually, let's identify indicator columns by the 'indicators' list
        # we calculated.
        # BUT, some indicators return multiple columns
        # (MACD -> MACD, MACD_signal, MACD_hist).
        # Our calculator adds them to DF.

        # Simplest way: Base cols first, then everything else.
        existing_base_cols = [c for c in base_cols if c in final_df.columns]
        other_cols = [c for c in final_df.columns if c not in existing_base_cols]

        ordered_cols = existing_base_cols + other_cols

        final_df = final_df[ordered_cols]

        final_df.to_csv(filepath, index=False)
        logger.info(f"Exported {len(final_df)} rows to {filepath}")

        return filepath
