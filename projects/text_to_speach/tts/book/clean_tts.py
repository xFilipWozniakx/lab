import argparse
import re
from pathlib import Path
from wordfreq import zipf_frequency


# python clean_tts.py input/chapter01.txt cleaned/chapter01.txt


MIN_WORD_FREQUENCY = 3.0
MIN_FREQUENCY_GAIN = 1.5


def is_likely_split_word(left: str, right: str) -> bool:
    """
    Determine whether two adjacent words are probably one word
    that was incorrectly split by PDF extraction.
    """

    if len(left) < 3 or len(right) < 3:
        return False

    if not left.isalpha() or not right.isalpha():
        return False

    joined = left + right

    left_freq = zipf_frequency(left.lower(), "en")
    right_freq = zipf_frequency(right.lower(), "en")
    joined_freq = zipf_frequency(joined.lower(), "en")

    if joined_freq < MIN_WORD_FREQUENCY:
        return False

    # If both parts are common English words, this is probably
    # a legitimate phrase rather than a broken word.
    if left_freq >= MIN_WORD_FREQUENCY and right_freq >= MIN_WORD_FREQUENCY:
        return False

    separate_score = max(left_freq, right_freq)

    if joined_freq - separate_score < MIN_FREQUENCY_GAIN:
        return False

    return True


def repair_split_words(text: str) -> str:
    """
    Automatically repair words split by PDF extraction.

    Example:
        imp ortant -> important
        com pany   -> company
    """

    pattern = re.compile(r"\b([A-Za-z]{3,})\s+([A-Za-z]{3,})\b")

    changed = True

    while changed:
        changed = False

        def replace(match):
            nonlocal changed

            left = match.group(1)
            right = match.group(2)

            if is_likely_split_word(left, right):
                changed = True
                return left + right

            return match.group(0)

        text = pattern.sub(replace, text)

    return text


def remove_page_headers(text: str) -> str:
    """
    Remove page numbers and chapter headers.
    """

    # Example: Chapter 1 • 15
    text = re.sub(
        r"^\s*Chapter\s+\d+\s*•\s*\d+\s*$",
        "",
        text,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    # Example: CHAPTER 1
    text = re.sub(
        r"^\s*CHAPTER\s+\d+\s*$",
        "",
        text,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    # Example: • Tuesday, September 2
    text = re.sub(
        r"^\s*•\s*[A-Za-z]+,\s+[A-Za-z]+\s+\d+\s*$",
        "",
        text,
        flags=re.MULTILINE,
    )

    return text


def repair_hyphenated_words(text: str) -> str:
    """
    Join words split across lines by a PDF hyphen.

    Example:

        com -
        pany

    becomes:

        company
    """

    return re.sub(
        r"([A-Za-z])-\s*\n\s*([A-Za-z])",
        r"\1\2",
        text,
    )


def repair_apostrophes(text: str) -> str:
    """
    Repair apostrophes broken by PDF extraction.
    """

    # Normalize curly apostrophes.
    text = text.replace("’", "'")
    text = text.replace("‘", "'")

    # Example:
    # I ' m      -> I'm
    # You ' re   -> You're
    # wasn ' t   -> wasn't
    text = re.sub(
        r"(?<=\w)\s*'\s*(?=\w)",
        "'",
        text,
    )

    return text


def remove_quotes(text: str) -> str:
    """
    Remove quotation marks because they are not needed by TTS.
    """

    text = text.replace('"', "")
    text = text.replace("“", "")
    text = text.replace("”", "")

    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize line endings and whitespace.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n[ \t]+", "\n", text)

    return text


def merge_pdf_lines(text: str) -> str:
    """
    Reconstruct paragraphs broken by PDF line wrapping.
    """

    lines = [line.strip() for line in text.splitlines()]

    paragraphs = []
    current = []

    for line in lines:
        if not line:
            if current:
                paragraphs.append(" ".join(current))
                current = []

            continue

        current.append(line)

    if current:
        paragraphs.append(" ".join(current))

    return "\n\n".join(paragraphs)


def clean_punctuation(text: str) -> str:
    """
    Clean spaces around punctuation and remove standalone
    hyphens that are PDF artifacts.
    """

    # "hello , world" -> "hello, world"
    text = re.sub(
        r"\s+([,.!?;:])",
        r"\1",
        text,
    )

    # "word - word" -> "word word"
    #
    # Normal hyphenated words remain untouched.
    text = re.sub(
        r"\s+-\s+",
        " ",
        text,
    )

    text = re.sub(r" {2,}", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def clean_text(text: str) -> str:
    """
    Run the complete PDF -> TTS cleaning pipeline.
    """

    text = normalize_whitespace(text)

    text = remove_page_headers(text)

    text = repair_hyphenated_words(text)

    text = repair_apostrophes(text)

    text = remove_quotes(text)

    text = merge_pdf_lines(text)

    text = repair_split_words(text)

    text = clean_punctuation(text)

    paragraphs = []

    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()

        if paragraph:
            paragraphs.append(paragraph)

    return "\n\n".join(paragraphs)


def main():
    parser = argparse.ArgumentParser(
        description="Clean a PDF-extracted text file for TTS."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input text file",
    )

    parser.add_argument(
        "output",
        type=Path,
        help="Output text file",
    )

    args = parser.parse_args()

    if not args.input.exists():
        parser.error(f"Input file does not exist: {args.input}")

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(f"Reading: {args.input}")
    print("Cleaning text...")

    text = args.input.read_text(
        encoding="utf-8",
    )

    cleaned = clean_text(text)

    args.output.write_text(
        cleaned,
        encoding="utf-8",
    )

    print("Done!")
    print(f"Output: {args.output}")
    print(f"Characters: {len(cleaned):,}")


if __name__ == "__main__":
    main()
