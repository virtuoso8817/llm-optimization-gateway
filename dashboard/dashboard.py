"""
dashboard.py

Terminal dashboard for the LLM Optimization Gateway.
"""

import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live

from database.db import DatabaseManager


class Dashboard:

    def __init__(self):
        self.console = Console()
        self.database = DatabaseManager()

    

    def build_layout(self):

        summary = self.database.get_summary()
        cost = self.database.get_cost_summary()
        models = self.database.get_model_statistics()

        layout = Layout()

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="summary", size=10),
            Layout(name="cost", size=9),
            Layout(name="models")
        )

        layout["header"].update(
            Panel.fit(
                "[bold cyan]LLM Optimization Gateway Dashboard[/bold cyan]"
            )
        )

        summary_table = Table(title="Optimization Summary")

        summary_table.add_column("Metric")
        summary_table.add_column("Value", justify="right")

        summary_table.add_row("Total Prompts", str(summary["total_prompts"]))
        summary_table.add_row("Tokens Saved", str(summary["total_tokens_saved"]))
        summary_table.add_row("Characters Saved", str(summary["total_characters_saved"]))
        summary_table.add_row(
            "Avg Token Compression",
            f'{summary["average_token_compression"]:.2f}%'
        )
        summary_table.add_row(
            "Avg Character Compression",
            f'{summary["average_character_compression"]:.2f}%'
        )

        layout["summary"].update(summary_table)

        cost_table = Table(title="Cost Analytics")

        cost_table.add_column("Metric")
        cost_table.add_column("Value", justify="right")

        cost_table.add_row("Requests", str(cost["total_requests"]))
        cost_table.add_row("Prompt Tokens", str(cost["prompt_tokens"]))
        cost_table.add_row("Completion Tokens", str(cost["completion_tokens"]))
        cost_table.add_row("Total Tokens", str(cost["total_tokens"]))
        cost_table.add_row("Total Cost", f'${cost["total_cost"]:.6f}')

        layout["cost"].update(cost_table)

        model_table = Table(title="Models")

        model_table.add_column("Model")
        model_table.add_column("Requests", justify="right")
        model_table.add_column("Latency", justify="right")
        model_table.add_column("Avg Cost", justify="right")

        if not models:
            model_table.add_row("No data", "-", "-", "-")
        else:
            for model in models:
                model_table.add_row(
                    model["model"],
                    str(model["requests"]),
                    str(model["average_latency_ms"]),
                    f'{model["average_cost"]:.6f}'
                )

        layout["models"].update(model_table)

        return layout

    def show(self):

        with Live(
            self.build_layout(),
            refresh_per_second=1,
            screen=True
        ) as live:

            while True:

                live.update(self.build_layout())

                time.sleep(2)


if __name__ == "__main__":

    dashboard = Dashboard()

    dashboard.show()