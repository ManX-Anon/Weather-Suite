"""Helpers for Rich-based terminal output."""
from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


def format_temperature(value: float) -> Text:
    if value >= 30:
        color = "red"
    elif value <= 10:
        color = "cyan"
    else:
        color = "yellow"
    return Text(f"{value:.1f}°C", style=color)


def weather_table(city: str, rows: list[tuple[str, str]]) -> Panel:
    table = Table.grid(padding=(0, 1))
    for label, value in rows:
        table.add_row(Text(label, style="bold"), value)
    return Panel(table, title=f"Weather: {city}", border_style="bright_blue")
