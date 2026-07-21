"""
metrics.py

Generates optimization reports.
"""

from typing import Optional


class PromptMetrics:
    """
    Generates optimization metrics and reports.
    """

    def generate(
        self,
        original_prompt: str,
        optimized_prompt: str,
        token_stats: dict,
        cost_before: Optional[dict] = None,
        cost_after: Optional[dict] = None,
    ) -> dict:

        report = {
            "original_prompt": original_prompt,
            "optimized_prompt": optimized_prompt,
            **token_stats,
        }

        if cost_before is not None:
            report["cost_before"] = cost_before

        if cost_after is not None:
            report["cost_after"] = cost_after

        if cost_before is not None and cost_after is not None:
            report["money_saved"] = round(
                cost_before["total_cost"] - cost_after["total_cost"],
                8,
            )

        return report


if __name__ == "__main__":

    metrics = PromptMetrics()

    report = metrics.generate(
        original_prompt="Please please explain AI",
        optimized_prompt="Please explain AI",
        token_stats={
            "original_tokens": 12,
            "optimized_tokens": 9,
            "tokens_saved": 3,
            "compression_ratio": 25.0,
        },
        cost_before={"total_cost": 0.000024},
        cost_after={"total_cost": 0.000018},
    )

    from pprint import pprint

    pprint(report)