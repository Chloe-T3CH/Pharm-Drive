from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from .utils import diff_texts, extract_text, summarize_changes

app = FastAPI(title="Pharm-Drive API")


class CompareResponse(BaseModel):
    diff: str
    summary: str
    method: str
    tokens_used: int | None
    truncated: bool


DEFAULT_MISSION_CONTEXT = (
    "Summarize the document differences with the perspective of a medical science liaison "
    "and tailor the explanation for marketing, medical affairs, legal, and sales teams."
)


@app.post("/compare", response_model=CompareResponse)
async def compare(
    file_old: UploadFile = File(...),
    file_new: UploadFile = File(...),
    mission_context: str | None = Form(None),
    api_key: str | None = Form(None),
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
    summary, metadata = summarize_changes(
        diff,
        mission_context=mission_context or DEFAULT_MISSION_CONTEXT,
        api_keys_override=api_key,
    )
    return CompareResponse(
        diff=diff,
        summary=summary,
        method=metadata["method"],
        tokens_used=metadata["tokens_used"],
        truncated=metadata["truncated"],
    )
