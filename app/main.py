from pathlib import Path

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


BASE_DIR = Path(__file__).resolve().parent.parent
DEMO_OLD = BASE_DIR / "tests" / "Demo Files" / "IMDELLTRA.pdf"
DEMO_NEW = BASE_DIR / "tests" / "Demo Files" / "IMDELLTRA (1).pdf"
DEMO_SUMMARY = (
    "**IMDELLTRA One-Pager – Sales_Impact AI Summary of Changes**\n\n"
    "**1. Big Picture**\n\n"
    "* The new version shifts from **“how to prepare and dose”** toward **“how to monitor, manage safety, and counsel patients.”**\n"
    "* No change to indication, MOA, or core safety signals—this is a **framing + usability update**, not a label expansion.\n\n"
    "**2. What’s Newly Emphasized**\n\n"
    "* Adds clear, **grade-based CRS management guidance** (when to hold, when to discontinue, what supportive care looks like).\n"
    "* Adds parallel **ICANS/neurologic toxicity management** table tied to ICE score and level of consciousness.\n"
    "* Introduces a dedicated **patient counseling section**:\n\n"
    "  * Driving / hazardous activities restrictions with neuro symptoms.\n"
    "  * Need for close post-infusion monitoring and frequent labs.\n"
    "  * Pregnancy, contraception, and breastfeeding timelines (during + 2 months after last dose).\n"
    "  * Symptom “red flag” lists for CRS, ICANS, cytopenias, infection, liver toxicity, and hypersensitivity.\n\n"
    "**3. What Was Reduced or Removed**\n\n"
    "* Detailed **compounding / reconstitution steps** and infusion-bag prep instructions are removed.\n"
    "* **Step-up dosing schedule** and **“restart after delay”** algorithms are no longer on this sheet.\n"
    "* The piece should no longer be positioned as a **full compounding/operational playbook**.\n\n"
    "**4. How Sales Should Use the New Piece**\n\n"
    "* Position it as a **quick safety and counseling guide**:\n\n"
    "  * “Here’s how we monitor, and what we do if CRS/ICANS occur.”\n"
    "  * “Here’s what you should be telling patients to watch for at home.”\n"
    "* Reinforce that serious toxicities are **expected but manageable** when the recommended monitoring and algorithms are followed.\n"
    "* For detailed questions on **dosing, compounding, or restarts after missed doses**, direct HCPs to:\n\n"
    "  * The **full Prescribing Information** and/or\n"
    "  * Separate **nursing/infusion or compounding guides** (if available locally).\n\n"
    "**5. Key Takeaway for the Field**\n\n"
    "> **Old sheet:** more about *how to mix and schedule doses.*\n"
    "> **New sheet:** more about *how to keep patients safe and informed* while on IMDELLTRA."
)


DEFAULT_MISSION_CONTEXT = (
    "Summarize the document differences with the perspective of a medical science liaison "
    "and tailor the explanation for marketing, medical affairs, legal, and sales teams."
)


@app.post("/compare", response_model=CompareResponse)
async def compare(
    file_old: UploadFile | None = File(None),
    file_new: UploadFile | None = File(None),
    mission_context: str | None = Form(None),
    api_key: str | None = Form(None),
    demo: bool = Form(False),
) -> CompareResponse:
    """Compare two documents and return a diff and AI-generated summary."""
    if demo:
        try:
            data_old = DEMO_OLD.read_bytes()
            data_new = DEMO_NEW.read_bytes()
            text_old = extract_text(DEMO_OLD.name, data_old)
            text_new = extract_text(DEMO_NEW.name, data_new)
        except Exception as exc:
            raise HTTPException(status_code=500, detail="Demo assets missing or unreadable") from exc
        diff = diff_texts(text_old, text_new)
        return CompareResponse(
            diff=diff,
            summary=DEMO_SUMMARY,
            method="demo",
            tokens_used=None,
            truncated=False,
        )

    if not file_old or not file_new:
        raise HTTPException(status_code=400, detail="Both files are required unless demo mode is used.")

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
