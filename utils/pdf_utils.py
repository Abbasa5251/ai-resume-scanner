import re
from typing import List
from pypdf import PdfReader


def extract_pdf_text(file) -> str:
    """Extract text from PDF file with cleaning."""
    reader = PdfReader(file)
    pages = []
    for p in reader.pages:
        pages.append(p.extract_text() or "")
    text = "\n".join(pages)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def split_into_chunks(text: str, max_chars: int = 24000) -> List[str]:
    """Split text into chunks for processing."""
    if len(text) <= max_chars:
        return [text]
    chunks, buf, running = [], [], 0
    for s in re.split(r"(?<=[.!?])\s+", text):
        if running + len(s) + 1 > max_chars:
            chunks.append(" ".join(buf))
            buf, running = [s], len(s) + 1
        else:
            buf.append(s)
            running += len(s) + 1
    if buf:
        chunks.append(" ".join(buf))
    return chunks
