import json


class JsonOptimizer:
    """
    Performs safe JSON optimization.

    Optimizations:
    - Removes unnecessary whitespace
    - Removes indentation
    - Preserves key order
    - Preserves all values

    If the input is not valid JSON, it is returned unchanged.
    """

    def optimize(self, text: str) -> str:
        if not text or not text.strip():
            return text

        try:
            parsed = json.loads(text)

            return json.dumps(
                parsed,
                separators=(",", ":"),
                ensure_ascii=False,
            )

        except (json.JSONDecodeError, TypeError):
            return text


if __name__ == "__main__":

    optimizer = JsonOptimizer()

    sample_json = """
    {
        "name": "Om",
        "age": 22,
        "skills": [
            "Python",
            "FastAPI",
            "LLMs"
        ],
        "active": true
    }
    """

    sample_text = """
    Explain the difference between AI and Machine Learning.
    """

    print("=" * 60)
    print("Original JSON")
    print("=" * 60)
    print(sample_json)

    print("\n" + "=" * 60)
    print("Optimized JSON")
    print("=" * 60)
    print(optimizer.optimize(sample_json))

    print("\n" + "=" * 60)
    print("Normal Prompt")
    print("=" * 60)
    print(sample_text)

    print("\n" + "=" * 60)
    print("After Optimization")
    print("=" * 60)
    print(optimizer.optimize(sample_text))