from fastapi import APIRouter, Form
from app.services.tts_service import synthesize_text

router = APIRouter(prefix="/tts", tags=["Text-to-Speech"])

@router.post("/synthesize")
async def tts(text: str = Form(...)):
    """
    Convert text to speech and return output file path.
    """
    output_path = synthesize_text(text)
    return {"audio_file": output_path}
