"""
tokenizer.py

Utility functions for counting tokens and comparing prompts using tiktoken.
"""

from typing import Dict
import tiktoken


class Tokenizer:
    """
    Wrapper around tiktoken for counting and comparing tokens.
    """

    def __init__(self, model: str = "gpt-4o"):
        """
        Initialize tokenizer for a specific model.

        Falls back to cl100k_base if model encoding is unavailable.
        """
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in a string.

        Parameters
        ----------
        text : str

        Returns
        -------
        int
        """
        if not text:
            return 0

        return len(self.encoding.encode(text))

    def compare_tokens(
        self,
        original: str,
        optimized: str
    ) -> Dict[str, float]:
        """
        Compare token counts between two prompts.

        Returns
        -------
        dict
        """

        original_tokens = self.count_tokens(original)
        optimized_tokens = self.count_tokens(optimized)

        saved = original_tokens - optimized_tokens

        if original_tokens == 0:
            compression = 0.0
        else:
            compression = round(
                (saved / original_tokens) * 100,
                2
            )

        return {
            "original_tokens": original_tokens,
            "optimized_tokens": optimized_tokens,
            "tokens_saved": saved,
            "compression_ratio": compression
        }


if __name__ == "__main__":

    tokenizer = Tokenizer()

    original = """
    Please please please explain the Transformer architecture in great detail.
    """

    optimized = """
    Please explain the Transformer architecture in detail.
    """

    print(tokenizer.compare_tokens(original, optimized))