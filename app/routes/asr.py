from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.asr_service import transcribe_file
import tempfile
import os

router = APIRouter(prefix="/asr", tags=["Speech-to-Text"])

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """
    Upload audio/video file and return Swahili transcription.
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[-1]) as temp_audio:
            temp_audio.write(await file.read())
            temp_path = temp_audio.name

        # Run transcription using Whisper
        text = transcribe_file(temp_path, language="sw")

        return {"transcription": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")

    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass
@router.post("/transcribe-bytes")
async def transcribe_bytes_api(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    text = transcribe_bytes(audio_bytes, suffix=".wav", language="sw")
    return {"transcription": text}