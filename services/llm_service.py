import time

from litellm import completion

from database.db import DatabaseManager
from providers.router import get_model
from services.cost_service import CostService

db = DatabaseManager()


class LLMService:

    def chat(
        self,
        prompt: str,
        provider: str | None = None
    ):

        model = get_model(provider)

        start_time = time.perf_counter()

        response = completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        latency_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

        usage = response.usage

        # Calculate request cost
        cost = CostService.calculate(
            model=model,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens
        )

        result = {

            "provider": provider or "default",

            "prompt": prompt,

            "response": response.choices[0].message.content,

            "model": response.model,

            "latency_ms": latency_ms,

            "prompt_tokens": usage.prompt_tokens,

            "completion_tokens": usage.completion_tokens,

            "total_tokens": usage.total_tokens,

            "input_cost": cost["input_cost"],

            "output_cost": cost["output_cost"],

            "total_cost": cost["total_cost"]

        }

        db.insert_llm_log(result)

        return result