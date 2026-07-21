"""
pricing.py

LLM Pricing Registry

Prices are in USD per 1,000,000 tokens.

Last Updated:
2026-07-21
"""

from dataclasses import dataclass


PRICING_VERSION = "2026-07-21"


@dataclass(frozen=True)
class ModelPricing:
    provider: str
    input_price: float
    output_price: float


MODEL_PRICING = {

    "groq/llama-3.3-70b-versatile":
        ModelPricing(
            provider="groq",
            input_price=0.59,
            output_price=0.79,
        ),

    "openai/gpt-4.1-mini":
        ModelPricing(
            provider="openai",
            input_price=0.40,
            output_price=1.60,
        ),

    # Verify before production
    "gemini/gemini-2.5-flash-lite":
        ModelPricing(
            provider="gemini",
            input_price=0.10,
            output_price=0.40,
        ),
}


class PricingCalculator:
    """
    Calculates estimated LLM API cost using the pricing registry.
    """

    def __init__(self, model: str):

        if model not in MODEL_PRICING:
            raise ValueError(f"Unsupported model: {model}")

        self.model_name = model
        self.pricing = MODEL_PRICING[model]

    def calculate(
        self,
        input_tokens: int,
        output_tokens: int = 0,
    ) -> dict:

        input_cost = (
            input_tokens / 1_000_000
        ) * self.pricing.input_price

        output_cost = (
            output_tokens / 1_000_000
        ) * self.pricing.output_price

        total_cost = input_cost + output_cost

        return {
            "provider": self.pricing.provider,
            "model": self.model_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost": round(input_cost, 8),
            "output_cost": round(output_cost, 8),
            "total_cost": round(total_cost, 8),
        }


if __name__ == "__main__":

    calculator = PricingCalculator("openai/gpt-4.1-mini")

    result = calculator.calculate(
        input_tokens=2500,
        output_tokens=800,
    )

    from pprint import pprint

    pprint(result)