from fastapi import APIRouter, UploadFile, File
from app.services.asr_service import transcribe_audio
import tempfile

router = APIRouter(prefix="/asr", tags=["Speech-to-Text"])

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """
    Upload audio file and get text transcription.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(await file.read())
        temp_path = temp_audio.name
    text = transcribe_audio(temp_path)
    return {"transcription": text}
