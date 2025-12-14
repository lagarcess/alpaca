import os

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from market_data.client import AlpacaClient


def main():
    load_dotenv()
    console = Console()
    console.rule("[bold cyan]Alpaca Market Data Service Job[/bold cyan]")

    if not os.getenv("APCA_API_KEY_ID") or not os.getenv("APCA_API_SECRET_KEY"):
        console.print(
            "[bold red]Error: Environment variables APCA_API_KEY_ID and "
            "APCA_API_SECRET_KEY must be set.[/bold red]"
        )
        return

    try:
        client = AlpacaClient()

        # Test parameters
        ticker = "QQQ"
        timeframe = "1Day"
        limit = 100

        console.print(
            f"Fetching data for [bold yellow]{ticker}[/bold yellow] (Limit: {limit})..."
        )

        bars = client.get_stock_bars(
            tickers=[ticker], timeframe=timeframe, limit=limit, start="2025-01-01"
        )

        console.print(f"[bold green]Success! Retrieved {len(bars)} bars.[/bold green]")

        # Display first 5 bars as a sample
        if bars:
            table = Table(title=f"Sample Data ({ticker})")
            table.add_column("Time", justify="left")
            table.add_column("Open", justify="right")
            table.add_column("High", justify="right")
            table.add_column("Low", justify="right")
            table.add_column("Close", justify="right")
            table.add_column("Volume", justify="right")

            for bar in bars[:5]:
                open_price = bar.get("o")
                close_price = bar.get("c")

                # Apply green color to all data rows
                color = "green"

                table.add_row(
                    f"[{color}]{str(bar.get('t'))}[/{color}]",
                    f"[{color}]{open_price:.2f}[/{color}]",
                    f"[{color}]{bar.get('h'):.2f}[/{color}]",
                    f"[{color}]{bar.get('l'):.2f}[/{color}]",
                    f"[{color}]{close_price:.2f}[/{color}]",
                    f"[{color}]{str(bar.get('v'))}[/{color}]",
                )

            console.print(table)
            if len(bars) > 5:
                console.print(f"[dim]...and {len(bars) - 5} more bars.[/dim]")
        else:
            console.print("[yellow]No bars returned.[/yellow]")

    except Exception as e:
        console.print(f"[bold red]Job failed:[/bold red] {e}")


if __name__ == "__main__":
    main()
