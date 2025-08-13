import io
import os
import difflib
from pathlib import Path

import docx
import pdfplumber
from pptx import Presentation

def extract_text(filename: str, data: bytes) -> str:
    """Extract text from supported document types based on file extension."""
    ext = Path(filename).suffix.lower()
    if ext == ".txt":
        return data.decode("utf-8")
    if ext == ".docx":
        document = docx.Document(io.BytesIO(data))
        return "\n".join(p.text for p in document.paragraphs)
    if ext == ".pdf":
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    if ext == ".pptx":
        prs = Presentation(io.BytesIO(data))
        texts = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    texts.append(shape.text)
        return "\n".join(texts)
    raise ValueError(f"Unsupported file type: {ext}")

def diff_texts(old: str, new: str) -> str:
    """Return a unified diff between two strings."""
    diff = difflib.unified_diff(
        old.splitlines(), new.splitlines(), fromfile="old", tofile="new", lineterm=""
    )
    return "\n".join(diff)

def summarize_changes(diff_text: str) -> str:
    """Summarize diff text using OpenAI if available, otherwise return a stub."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            prompt = (
                "Provide a concise summary of the following document changes "
                "focusing on compliance-relevant updates and sales impact:\n"
                f"{diff_text}"
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            pass
    # Fallback summarization
    return "Summary:\n" + diff_text[:500]
