# Alpaca Data Service

A production-grade Python data pipeline module to download stock market data using the Alpaca API.

## Features

- **Technical Indicators**: Calculate 150+ indicators (SMA, RSI, MACD, etc.) using `ta-lib` via the official C library.
- **Smart Warm-up**: Automatically fetches extra "warm-up" data so your indicators are valid from the very first requested date.
- **Streaming Export**: Memory-efficient CSV export for large datasets.
- **Dockerized**: No need to manually install complex C libraries—just run with Docker.

## Setup

### Option A: Local Python Setup (Advanced)
Requires `ta-lib` C library installed on your host.

1.  Install dependencies:
    ```bash
    poetry install
    ```
2.  Set up environment variables in `.env` (copy from `.env.example`).

### Option B: Docker Setup (Recommended)
NO C library installation required.

1.  Ensure Docker and Docker Compose are installed.
2.  Build the container:
    ```bash
    docker-compose build
    ```

## Usage

### CLI Arguments
| Argument | Description | Example |
| :--- | :--- | :--- |
| `--tickers` | Comma-separated list of symbols | `AAPL,MSFT` |
| `--start` | Start date (YYYY-MM-DD) | `2023-01-01` |
| `--end` | End date (Optional) | `2023-12-31` |
| `--timeframe` | Timeframe (1Day, 1Hour, 1Min) | `1Day` |
| `--indicators` | Comma-separated indicators | `SMA_50,RSI_14` |
| `--output-dir` | Output directory (default `data/`) | `my_exports` |

### Examples

**1. Basic Download (Local)**
```bash
python main.py --tickers AAPL --start 2023-01-01
```

**2. Download with Indicators (Docker)**
Fetch `AAPL` and `MSFT` data from Jan 1st, 2023, with 50-day SMA and 14-day RSI added.
```bash
docker-compose run --rm alpaca-downloader \
  --tickers AAPL,MSFT \
  --start 2023-01-01 \
  --indicators SMA_50,RSI_14
```
*Note: The CSV files will appear in your local `data/` folder.*
