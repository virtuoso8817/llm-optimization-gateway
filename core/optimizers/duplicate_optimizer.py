"""
duplicate_optimizer.py

Safe duplicate removal.

Rules:
1. Remove consecutive duplicate words.
2. Remove consecutive duplicate lines.
3. Remove consecutive duplicate paragraphs.

No semantic modifications are performed.
"""

import re


class DuplicateOptimizer:
    """
    Safely removes duplicate content without changing semantics.
    """

    def optimize(self, text: str) -> str:
        if not text:
            return text

        text = self._remove_duplicate_words(text)
        text = self._remove_duplicate_lines(text)
        text = self._remove_duplicate_sentences(text)   # NEW
        text = self._remove_duplicate_paragraphs(text)

        return text.strip()

    def _remove_duplicate_words(self, text: str) -> str:
        """
        Remove consecutive duplicate words.

        Example:
            the the the transformer
            ->
            the transformer
        """

        pattern = r"\b(\w+)(\s+\1\b)+"

        return re.sub(
            pattern,
            r"\1",
            text,
            flags=re.IGNORECASE,
        )

    def _remove_duplicate_lines(self, text: str) -> str:
        """
        Remove consecutive duplicate lines.
        """

        lines = text.splitlines()

        optimized = []
        previous = None

        for line in lines:

            stripped = line.strip()

            if stripped == previous:
                continue

            optimized.append(line)
            previous = stripped

        return "\n".join(optimized)
    

    def _remove_duplicate_sentences(self, text: str) -> str:
        """
        Remove only consecutive duplicate sentences
        within the same paragraph.

        Example:

        You are an AI.
        You are an AI.

        becomes

        You are an AI.

        Non-consecutive duplicate sentences
        are preserved.
        """

        paragraphs = re.split(r"\n\s*\n", text)

        optimized_paragraphs = []

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            # Split paragraph into sentences
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)

            optimized_sentences = []
            previous = None

            for sentence in sentences:

                normalized = sentence.strip().lower()

                if not normalized:
                    continue

                if normalized == previous:
                    continue

                optimized_sentences.append(sentence.strip())
                previous = normalized

            optimized_paragraphs.append(" ".join(optimized_sentences))

        return "\n\n".join(optimized_paragraphs)


    def _remove_duplicate_paragraphs(self, text: str) -> str:
        """
        Remove only consecutive duplicate paragraphs.

        Paragraphs separated by other content are preserved
        because they may be intentionally repeated.
        """

        paragraphs = re.split(r"\n\s*\n", text)

        optimized = []
        previous = None

        for paragraph in paragraphs:

            normalized = paragraph.strip()

            if not normalized:
                continue

            if normalized == previous:
                continue

            optimized.append(normalized)
            previous = normalized

        return "\n\n".join(optimized)


if __name__ == "__main__":

    sample = """
    
    You are an expert AI assistant.
    You are an expert AI assistant.

    Explain Retrieval Augmented Generation.
    Explain Retrieval Augmented Generation.

    Paragraph A.

    Paragraph A.

    Paragraph B.

    Paragraph A.

"""

    optimizer = DuplicateOptimizer()

    print("=" * 60)
    print("Original")
    print("=" * 60)
    print(sample)

    print("\n" + "=" * 60)
    print("Optimized")
    print("=" * 60)
    print(optimizer.optimize(sample))