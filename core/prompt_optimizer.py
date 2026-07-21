from dataclasses import dataclass

from core.optimizers.duplicate_optimizer import DuplicateOptimizer
from core.optimizers.markdown_optimizer import MarkdownOptimizer
from core.optimizers.json_optimizer import JsonOptimizer
from core.tokenizer import Tokenizer


@dataclass
class OptimizationResult:
    original_prompt: str
    optimized_prompt: str

    optimization_applied: bool

    original_chars: int
    optimized_chars: int
    chars_saved: int

    original_tokens: int
    optimized_tokens: int
    tokens_saved: int

    compression_percent: float
    token_compression_percent: float


class PromptOptimizer:
    """
    Runs all deterministic prompt optimizers in sequence.

    Pipeline:
        Duplicate Optimizer
            ↓
        Markdown Optimizer
            ↓
        JSON Optimizer
    """

    def __init__(self):
        self.duplicate_optimizer = DuplicateOptimizer()
        self.markdown_optimizer = MarkdownOptimizer()
        self.json_optimizer = JsonOptimizer()
        self.tokenizer = Tokenizer()

    def optimize(self, prompt: str) -> OptimizationResult:

        if not prompt:
            return OptimizationResult(
                original_prompt="",
                optimized_prompt="",
                optimization_applied=False,
                original_chars=0,
                optimized_chars=0,
                chars_saved=0,
                original_tokens=0,
                optimized_tokens=0,
                tokens_saved=0,
                compression_percent=0.0,
                token_compression_percent=0.0,
            )

        original = prompt

        optimized = self.duplicate_optimizer.optimize(original)
        optimized = self.markdown_optimizer.optimize(optimized)
        optimized = self.json_optimizer.optimize(optimized)

        optimization_applied = optimized != original

        # Character statistics
        original_chars = len(original)
        optimized_chars = len(optimized)
        chars_saved = original_chars - optimized_chars

        compression_percent = (
            round((chars_saved / original_chars) * 100, 2)
            if original_chars
            else 0.0
        )

        # Token statistics
        token_stats = self.tokenizer.compare_tokens(
            original,
            optimized
        )

        original_tokens = token_stats["original_tokens"]
        optimized_tokens = token_stats["optimized_tokens"]
        tokens_saved = token_stats["tokens_saved"]
        token_compression_percent = token_stats["compression_ratio"]

        return OptimizationResult(
            original_prompt=original,
            optimized_prompt=optimized,
            optimization_applied=optimization_applied,
            original_chars=original_chars,
            optimized_chars=optimized_chars,
            chars_saved=chars_saved,
            original_tokens=original_tokens,
            optimized_tokens=optimized_tokens,
            tokens_saved=tokens_saved,
            compression_percent=compression_percent,
            token_compression_percent=token_compression_percent,
        )


if __name__ == "__main__":

    sample = """
#Heading

#Heading

This is a test.

This is a test.

*Item one
+Item two

---
---
---
"""

    optimizer = PromptOptimizer()

    result = optimizer.optimize(sample)

    print("=" * 60)
    print("Original Prompt")
    print("=" * 60)
    print(result.original_prompt)

    print("\n" + "=" * 60)
    print("Optimized Prompt")
    print("=" * 60)
    print(result.optimized_prompt)

    print("\n" + "=" * 60)
    print("Statistics")
    print("=" * 60)

    print(f"Optimization Applied   : {result.optimization_applied}")

    print()

    print(f"Original Characters    : {result.original_chars}")
    print(f"Optimized Characters   : {result.optimized_chars}")
    print(f"Characters Saved       : {result.chars_saved}")
    print(f"Character Compression  : {result.compression_percent}%")

    print()

    print(f"Original Tokens        : {result.original_tokens}")
    print(f"Optimized Tokens       : {result.optimized_tokens}")
    print(f"Tokens Saved           : {result.tokens_saved}")
    print(f"Token Compression      : {result.token_compression_percent}%")