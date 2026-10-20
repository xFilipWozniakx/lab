from pathlib import Path
import re
import sys
from pypdf import PdfReader



PDF_PATH = Path(sys.argv[1])
OUTPUT_DIR = Path("./chapters/")


# Recognizes headings such as:
# CHAPTER 1
# CHAPTER ONE
# Chapter IV
CHAPTER_PATTERN = re.compile(
    r"^\s*CHAPTER\s+"
    r"(?:\d+|[IVXLCDM]+|ONE|TWO|THREE|FOUR|FIVE|"
    r"SIX|SEVEN|EIGHT|NINE|TEN|ELEVEN|TWELVE|"
    r"THIRTEEN|FOURTEEN|FIFTEEN|SIXTEEN|"
    r"SEVENTEEN|EIGHTEEN|NINETEEN|TWENTY)\b",
    re.IGNORECASE | re.MULTILINE,
)


def extract_pages(reader):
    """Extract text from every page in the PDF."""
    pages = []

    for page_index, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append((page_index, text))

    return pages


def find_chapter_pages(pages):
    """Return zero-based page indexes containing chapter headings."""
    chapter_pages = []

    for page_index, text in pages:
        if CHAPTER_PATTERN.search(text):
            chapter_pages.append(page_index)

    return sorted(set(chapter_pages))


def save_chapters(reader, chapter_pages, output_dir):
    """Save each detected chapter into a separate text file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # The first detected heading starts the first chapter.
    # The end of the final chapter is the end of the PDF.
    boundaries = chapter_pages + [len(reader.pages)]

    for chapter_number, (start, end) in enumerate(
        zip(boundaries, boundaries[1:]),
        start=1,
    ):
        text_parts = []

        for page_index in range(start, end):
            text = reader.pages[page_index].extract_text() or ""

            if text.strip():
                text_parts.append(text.strip())

        chapter_text = "\n\n".join(text_parts).strip()

        output_file = (
            output_dir / f"Chapter_{chapter_number:02d}.txt"
        )

        output_file.write_text(
            chapter_text + "\n",
            encoding="utf-8",
        )

        print(
            f"Created {output_file} "
            f"(PDF pages {start + 1}-{end})"
        )


def main():
    if not PDF_PATH.is_file():
        raise FileNotFoundError(
            f"PDF file not found: {PDF_PATH.resolve()}"
        )

    reader = PdfReader(str(PDF_PATH))

    if reader.is_encrypted:
        raise RuntimeError(
            "The PDF is encrypted. Decrypt it before extraction."
        )

    print(f"PDF: {PDF_PATH}")
    print(f"Total pages: {len(reader.pages)}")

    pages = extract_pages(reader)
    chapter_pages = find_chapter_pages(pages)

    if not chapter_pages:
        print("No chapter headings detected. Saving entire book.")

        chapter_pages = [0]

    print(f"Detected chapter headings: {len(chapter_pages)}")

    save_chapters(reader, chapter_pages, OUTPUT_DIR)

    print("Finished extracting chapters.")


if __name__ == "__main__":
    main()
