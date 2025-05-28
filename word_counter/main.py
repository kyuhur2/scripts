import sys
import argparse
from pathlib import Path

try:
    from docx import Document
except ImportError:
    Document = None

def count_words_in_text(text: str) -> int:
    return len(text.split())

def count_txt_md(path: Path) -> int:
    return count_words_in_text(path.read_text(encoding="utf-8"))

def count_docx(path: Path) -> int:
    if not Document:
        raise RuntimeError("python-docx is not installed. Run: pip install python-docx")
    doc = Document(path)
    full_text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return count_words_in_text(full_text)

def main():
    parser = argparse.ArgumentParser(description="Count words in a .txt, .md, or .docx file")
    parser.add_argument("file", type=Path, help="Path to input document")
    args = parser.parse_args()

    path = args.file
    if not path.exists():
        print(f"Error: {path} does not exist.", file=sys.stderr)
        sys.exit(1)

    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        total = count_txt_md(path)
    elif suffix == ".docx":
        total = count_docx(path)
    else:
        print("Unsupported file type. Only .txt, .md, and .docx are supported.", file=sys.stderr)
        sys.exit(1)

    print(f"Word count for '{path.name}': {total}")

if __name__ == "__main__":
    main()
