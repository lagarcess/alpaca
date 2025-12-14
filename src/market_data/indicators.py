import logging
from typing import List

import pandas as pd
import talib
from talib import abstract

logger = logging.getLogger("rich")


class IndicatorCalculator:
    """
    Calculates technical indicators using TA-Lib.
    """

    def __init__(self):
        self._supported_indicators = self._discover_indicators()

    def _discover_indicators(self) -> List[str]:
        """
        Dynamically discovers all supported indicators from TA-Lib.
        """
        try:
            functions = talib.get_functions()
            logger.info(f"Discovered {len(functions)} TA-Lib indicators.")
            return functions
        except Exception as e:
            logger.error(f"Failed to discover TA-Lib functions: {e}")
            return []

    def get_supported_indicators(self) -> List[str]:
        """Returns a list of all supported indicator names."""
        return self._supported_indicators

    def add_indicators(self, data: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
        """
        Appends technical indicators to the dataframe.

        Args:
            data: OHLCV DataFrame with columns ['open', 'high', 'low',
                  'close', 'volume'].
                  Column names are case-insensitive.
            indicators: List of strings (e.g., ['SMA', 'RSI']).
                        Can also specify parameters if we implement parsing logic later,
                        but for now assumes default parameters or simple names.

        Returns:
            DataFrame with new indicator columns.
        """
        if not indicators:
            return data

        # Ensure column names are lower case for TA-Lib abstract API
        # TA-Lib expects: 'open', 'high', 'low', 'close', 'volume'
        working_data = data.copy()
        working_data.columns = [c.lower() for c in working_data.columns]

        # We need to map back to original index if we are careful,
        # but here we just return the modified dataframe copies.
        # Actually, let's keep the original data columns as they were,
        # and append new ones.

        # Prepare inputs for abstract API
        # Abstract API expects a dict of numpy arrays or a dataframe with
        # lowercase columns
        inputs = {
            "open": working_data["open"].values.astype(float),
            "high": working_data["high"].values.astype(float),
            "low": working_data["low"].values.astype(float),
            "close": working_data["close"].values.astype(float),
            "volume": working_data["volume"].values.astype(float),
        }

        for ind_name in indicators:
            ind_name_upper = ind_name.upper()

            # Parse parameters first to get the base function name
            parts = ind_name_upper.split("_")
            func_name = parts[0]

            # Basic validation
            if func_name not in self._supported_indicators:
                logger.warning(
                    f"Indicator '{func_name}' (from '{ind_name}') "
                    "not found in TA-Lib. Skipping."
                )
                continue

            try:
                # Dynamic function call
                params = {}

                if func_name not in self._supported_indicators:
                    logger.warning(
                        f"Indicator function '{func_name}' not found. Skipping."
                    )
                    continue

                # Simple heuristic for single-parameter indicators (usually timeperiod)
                if len(parts) > 1 and parts[1].isdigit():
                    params["timeperiod"] = int(parts[1])

                func = abstract.Function(func_name)

                # Calculate
                result = func(inputs, **params)

                # Result can be a single array or tuple of arrays (like MACD)
                if isinstance(result, tuple):
                    # For multi-output indicators, we might need specific naming
                    # e.g. MACD returns (macd, macdsignal, macdhist)
                    # We can use the output names from the function info if available
                    # or just append default suffixes.
                    for i, res_array in enumerate(result):
                        col_name = f"{ind_name}_{i}"
                        data[col_name] = res_array
                else:
                    data[ind_name] = result

            except Exception as e:
                logger.error(f"Failed to calculate {ind_name}: {e}")

        return data
