import argparse

from dotenv import load_dotenv
from rich.console import Console

from market_data.pipeline import StockDataPipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="Alpaca Data Downloader & Technical Analysis Engine"
    )
    parser.add_argument(
        "--tickers",
        type=str,
        required=True,
        help="Comma-separated list of tickers (e.g. AAPL,MSFT)",
    )
    parser.add_argument(
        "--start", type=str, required=True, help="Start date (YYYY-MM-DD)"
    )
    parser.add_argument("--end", type=str, required=False, help="End date (YYYY-MM-DD)")
    parser.add_argument(
        "--timeframe",
        type=str,
        default="1Day",
        help="Timeframe (1Day, 1Hour, 1Min, etc.)",
    )
    parser.add_argument(
        "--indicators",
        type=str,
        default="",
        help="Comma-separated list of indicators (e.g. SMA_50,RSI_14)",
    )
    parser.add_argument(
        "--output-dir", type=str, default="data", help="Directory to save CSV files"
    )
    return parser.parse_args()


def main():
    load_dotenv()
    console = Console()
    console.rule("[bold cyan]Alpaca Production Data Pipeline[/bold cyan]")

    args = parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",")]
    indicators = (
        [i.strip() for i in args.indicators.split(",")] if args.indicators else []
    )

    pipeline = StockDataPipeline(output_dir=args.output_dir)

    console.print(f"[bold]Processing {len(tickers)} tickers...[/bold]")
    console.print(f"Timeframe: {args.timeframe}")
    console.print(f"Indicators: {indicators}")

    success_count = 0
    for ticker in tickers:
        try:
            path = pipeline.process_ticker(
                ticker=ticker,
                timeframe=args.timeframe,
                start_date=args.start,
                end_date=args.end,
                indicators=indicators,
            )
            if path:
                console.print(f"[green]✓ {ticker}: Saved to {path}[/green]")
                success_count += 1
            else:
                console.print(f"[yellow]⚠ {ticker}: No data exported[/yellow]")
        except Exception as e:
            console.print(f"[red]✗ {ticker}: Failed - {e}[/red]")
            # Log full traceback?
            # logging.exception("Failed")

    console.rule()
    console.print(
        f"[bold blue]Job Complete. Successful: {success_count}/{len(tickers)}"
        "[/bold blue]"
    )


if __name__ == "__main__":
    main()
