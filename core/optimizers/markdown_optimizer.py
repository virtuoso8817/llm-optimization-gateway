import re


class MarkdownOptimizer:
    """
    Performs safe Markdown optimizations without changing semantics.
    """

    def optimize(self, text: str) -> str:
        if not text:
            return text

        text = self._remove_trailing_spaces(text)
        text = self._normalize_blank_lines(text)
        text = self._normalize_horizontal_rules(text)
        text = self._normalize_headings(text)
        text = self._normalize_bullets(text)

        return text.strip()

    def _remove_trailing_spaces(self, text: str) -> str:
        """Remove trailing whitespace from every line."""
        return "\n".join(line.rstrip() for line in text.splitlines())

    def _normalize_blank_lines(self, text: str) -> str:
        """Reduce 3+ consecutive blank lines to 2."""
        return re.sub(r"\n{3,}", "\n\n", text)

    def _normalize_headings(self, text: str) -> str:
        """
        Ensure exactly one space after Markdown heading markers.

        ##Heading
        ->
        ## Heading
        """

        def fix_heading(match):
            hashes = match.group(1)
            title = match.group(2).strip()
            return f"{hashes} {title}"

        return re.sub(
            r"^(#{1,6})\s*(.+)$",
            fix_heading,
            text,
            flags=re.MULTILINE,
        )

    def _normalize_bullets(self, text: str) -> str:
        """
        Normalize unordered list markers.

        *Item
        +Item
        -Item

        ->
        - Item

        Does NOT modify horizontal rules (---, ***, ___).
        """

        lines = []

        for line in text.splitlines():

            stripped = line.strip()

            # Ignore horizontal rules
            if stripped in ("---", "***", "___"):
                lines.append(line)
                continue

            line = re.sub(
                r"^(\s*)[*+-]\s*(\S.*)$",
                r"\1- \2",
                line,
            )

            lines.append(line)

        return "\n".join(lines)

    def _normalize_horizontal_rules(self, text: str) -> str:
        """
        Collapse consecutive horizontal rules.

        ---
        ---
        ---

        ->
        ---
        """

        pattern = (
            r"(?m)"
            r"^(?:-{3,}|\*{3,}|_{3,})\s*$"
            r"(?:\n^(?:-{3,}|\*{3,}|_{3,})\s*$)+"
        )

        return re.sub(pattern, "---", text)


if __name__ == "__main__":

    sample = """
#Heading

##Section


Some text.    

*Item one
+Item two
-Item three

---
---
---

###Another Heading



End
"""

    optimizer = MarkdownOptimizer()

    print("=" * 60)
    print("Original Markdown")
    print("=" * 60)
    print(sample)

    print("\n" + "=" * 60)
    print("Optimized Markdown")
    print("=" * 60)
    print(optimizer.optimize(sample))