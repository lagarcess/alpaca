import logging
import os
import time
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
from tqdm import tqdm

# Configure rich logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("rich")


class AlpacaClient:
    """Client for interacting with the Alpaca Data API v2."""

    BASE_URL = "https://data.alpaca.markets/v2/stocks/bars"

    def __init__(self):
        """Initialize the client by loading credentials from environment."""
        load_dotenv()
        self.api_key = os.getenv("APCA_API_KEY_ID")
        self.secret_key = os.getenv("APCA_API_SECRET_KEY")

        if not self.api_key or not self.secret_key:
            raise ValueError(
                "Missing Alpaca API credentials. Please set APCA_API_KEY_ID "
                "and APCA_API_SECRET_KEY."
            )

        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key,
            "accept": "application/json",
        }
        self.console = Console()

    def get_stock_bars(
        self,
        tickers: List[str],
        timeframe: str,
        limit: int = 1000,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch stock bars for the given tickers.

        Args:
            tickers: List of stock symbols (e.g., ["AAPL", "QQQ"]).
            timeframe: Timeframe for the bars (e.g., "1Day", "1Hour").
            limit: Maximum number of bars to fetch per request (default 1000).
            start: Optional start date/time (e.g., "2023-01-01").
            end: Optional end date/time.

        Returns:
            List of bar objects.
        """
        symbol_str = ",".join(tickers)
        all_bars = []
        next_page_token = None

        self.console.print(
            f"[bold green]Starting data fetch for: {symbol_str}[/bold green]"
        )

        # Initial query params
        params = {
            "symbols": symbol_str,
            "timeframe": timeframe,
            "limit": limit,
            "feed": "iex",
        }
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        # Progress bar (unknown total initially, so just a spinner/counter)
        with tqdm(desc="Fetching pages", unit="page") as pbar:
            while True:
                if next_page_token:
                    params["page_token"] = next_page_token

                try:
                    response = self._make_request(params)
                    data = response.json()

                    bars = data.get("bars", {})
                    # Flatten the dictionary structure: {ticker: [bars]}
                    page_count = 0
                    for _, ticker_bars in bars.items():
                        all_bars.extend(ticker_bars)
                        page_count += len(ticker_bars)

                    pbar.update(1)
                    pbar.set_postfix({"bars": len(all_bars)})

                    next_page_token = data.get("next_page_token")
                    if not next_page_token:
                        break

                except requests.exceptions.HTTPError as e:
                    logger.error(f"HTTP Error: {e}")
                    raise
                except Exception as e:
                    logger.exception(f"Unexpected error: {e}")
                    raise

        self.console.print(
            f"[bold blue]Completed. Fetched {len(all_bars)} bars total.[/bold blue]"
        )
        return all_bars

    def _make_request(
        self, params: Dict[str, Any], max_retries: int = 3
    ) -> requests.Response:
        """Make a request with retry logic for 5xx errors."""
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    self.BASE_URL, headers=self.headers, params=params
                )

                if response.status_code >= 500:
                    logger.warning(
                        f"Server error {response.status_code}. "
                        f"Retrying ({attempt + 1}/{max_retries})..."
                    )
                    time.sleep(2**attempt)  # Exponential backoff
                    continue

                response.raise_for_status()
                return response

            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                if (
                    isinstance(e, requests.exceptions.HTTPError)
                    and 400 <= e.response.status_code < 500
                ):
                    # Don't retry 4xx errors
                    raise
                logger.warning(f"Request failed: {e}. Retrying...")
                time.sleep(1)

        raise requests.exceptions.RetryError("Max retries exceeded")
