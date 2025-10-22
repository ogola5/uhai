# app/routes/tts.py
from fastapi import APIRouter, Form
from fastapi.responses import FileResponse
from app.services.tts_service import synthesize_text

# Define router at the top level
router = APIRouter(prefix="/tts", tags=["Text-to-Speech"])

@router.post("/synthesize")
async def synthesize(text: str = Form(...)):
    """
    Convert text to speech and return audio file.
    """
    audio_path = synthesize_text(text)
    return FileResponse(
        audio_path,
        media_type="audio/wav",
        filename="uhai_tts_output.wav"
    )
