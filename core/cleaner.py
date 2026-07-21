"""
cleaner.py

Prompt cleaning and optimization utilities.
Performs lightweight, rule-based optimizations to reduce unnecessary tokens
without changing the prompt's meaning.
"""

import re


class PromptCleaner:
    """
    Cleans and optimizes prompts before sending them to an LLM.
    """

    def normalize_whitespace(self, text: str) -> str:
        """Replace multiple spaces/tabs with a single space."""
        return re.sub(r"[ \t]+", " ", text)

    def remove_extra_blank_lines(self, text: str) -> str:
        """Reduce multiple blank lines to a single blank line."""
        return re.sub(r"\n\s*\n+", "\n\n", text)

    def remove_duplicate_words(self, text: str) -> str:
        """
        Remove consecutive duplicate words.

        Example:
        'Please please explain explain'
        ->
        'Please explain'
        """
        pattern = r"\b(\w+)(\s+\1\b)+"
        return re.sub(pattern, r"\1", text, flags=re.IGNORECASE)

    def normalize_punctuation(self, text: str) -> str:
        """
        Reduce repeated punctuation.

        !!!!! -> !
        ..... -> .
        ????? -> ?
        """
        text = re.sub(r"\.{2,}", ".", text)
        text = re.sub(r"!{2,}", "!", text)
        text = re.sub(r"\?{2,}", "?", text)
        return text

    def optimize_common_phrases(self, text: str) -> str:
        """
        Replace verbose phrases with shorter equivalents.
        """

        replacements = {
            r"\bcould you kindly\b": "",
            r"\bcould you\b": "",
            r"\bcan you\b": "",
            r"\bi would like you to\b": "",
            r"\bplease kindly\b": "please",
            r"\bkindly\b": "",
            r"\btell me about\b": "explain",
            r"\bgive me information about\b": "explain",
        }

        for pattern, replacement in replacements.items():
            text = re.sub(
                pattern,
                replacement,
                text,
                flags=re.IGNORECASE,
            )

        return text

    def clean_prompt(self, prompt: str) -> str:
        """
        Apply all cleaning steps.
        """

        prompt = self.normalize_whitespace(prompt)

        prompt = self.remove_extra_blank_lines(prompt)

        prompt = self.remove_duplicate_words(prompt)

        prompt = self.normalize_punctuation(prompt)

        prompt = self.optimize_common_phrases(prompt)

        return prompt.strip()


if __name__ == "__main__":

    cleaner = PromptCleaner()

    prompt = """
    Could you kindly please please explain....

    the Transformer     architecture!!!!!

    Please Please explain.

    Thanks!!!!!!!!
    """

    cleaned = cleaner.clean_prompt(prompt)

    print("\nOriginal:\n")
    print(prompt)

    print("\nCleaned:\n")
    print(cleaned)