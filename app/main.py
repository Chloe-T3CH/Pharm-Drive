from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from .utils import diff_texts, extract_text, summarize_changes

app = FastAPI(title="Pharm-Drive API")


class CompareResponse(BaseModel):
    diff: str
    summary: str


@app.post("/compare", response_model=CompareResponse)
async def compare(
    file_old: UploadFile = File(...), file_new: UploadFile = File(...)
) -> CompareResponse:
    """Compare two documents and return a diff and AI-generated summary."""
    data_old = await file_old.read()
    data_new = await file_new.read()
    try:
        text_old = extract_text(file_old.filename, data_old)
        text_new = extract_text(file_new.filename, data_new)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    diff = diff_texts(text_old, text_new)
    summary = summarize_changes(diff)
    return CompareResponse(diff=diff, summary=summary)
