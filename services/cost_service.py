from core.pricing import MODEL_PRICING


class CostService:

    @staticmethod
    def calculate(
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ):

        pricing = MODEL_PRICING.get(model)

        if pricing is None:
            raise ValueError(
                f"No pricing configured for '{model}'"
            )

        input_cost = (
            prompt_tokens
            * pricing.input_price
            / 1_000_000
        )

        output_cost = (
            completion_tokens
            * pricing.output_price
            / 1_000_000
        )

        total_cost = input_cost + output_cost

        return {
            "input_cost": round(input_cost, 8),
            "output_cost": round(output_cost, 8),
            "total_cost": round(total_cost, 8),
        }