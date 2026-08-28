#!/usr/bin/env python3
"""Extract text and metadata from a research paper PDF using PyMuPDF."""

from __future__ import annotations

import sys
import json
import argparse

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)


def extract_pdf(pdf_path: str, max_pages: int | None = None) -> dict:
    """Extract text and metadata from a PDF.

    Args:
        pdf_path: Path to the PDF file.
        max_pages: Optional limit on pages to extract (None = all).

    Returns:
        Dict with keys: title, authors, abstract, metadata, pages (list of page text),
        total_pages, page_range_extracted.
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    page_end = min(max_pages, total_pages) if max_pages else total_pages

    pages = []
    for i in range(page_end):
        page = doc[i]
        text = page.get_text("text")
        pages.append(text)

    # Extract metadata
    meta = doc.metadata or {}
    title = meta.get("title", "")
    authors = meta.get("author", "")

    # Try to get abstract from first page
    abstract = ""
    if pages:
        first_page = pages[0]
        abstract = _extract_abstract(first_page)
        if not abstract:
            abstract = first_page[:500].strip() + "..."

    doc.close()

    # Warn if text is very short (possibly scanned PDF)
    total_text = " ".join(pages)
    if len(total_text.strip()) < 100:
        print("WARNING: Very little text extracted. PDF may be scanned/image-based.", file=sys.stderr)

    return {
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "metadata": meta,
        "pages": pages,
        "total_pages": total_pages,
        "page_range_extracted": f"1-{page_end}",
    }


def _extract_abstract(first_page_text: str) -> str:
    """Heuristic extraction of abstract from first page text."""
    text = first_page_text.strip()
    lower = text.lower()

    # Find "abstract" header
    idx = lower.find("abstract")
    if idx == -1:
        return ""

    # Skip the word "abstract" itself and any following colon/dash
    start = idx + len("abstract")
    while start < len(text) and text[start] in ":-— \t\n":
        start += 1

    # Find end: look for "introduction" or "1." at line start, or double newline
    end_markers = ["introduction", "\n1.", "\n1 ", "\n\n\n"]
    end = len(text)
    for marker in end_markers:
        pos = lower.find(marker, start)
        if pos != -1 and pos < end:
            end = pos

    abstract = text[start:end].strip()
    # Clean up single newlines within abstract
    abstract = " ".join(line.strip() for line in abstract.splitlines() if line.strip())
    return abstract


def main():
    parser = argparse.ArgumentParser(description="Extract text from a research paper PDF")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--max-pages", type=int, default=None, help="Max pages to extract")
    parser.add_argument(
        "--format",
        choices=["json", "text", "pages"],
        default="json",
        help="Output format: json (full), text (concatenated), pages (numbered)",
    )
    args = parser.parse_args()

    result = extract_pdf(args.pdf_path, args.max_pages)

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.format == "text":
        for page in result["pages"]:
            print(page)
    elif args.format == "pages":
        for i, page in enumerate(result["pages"], 1):
            print(f"\n--- Page {i} ---\n")
            print(page)


if __name__ == "__main__":
    main()
