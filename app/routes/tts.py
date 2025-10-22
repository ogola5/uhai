from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.post("/synthesize")
async def synthesize_speech(data: TextRequest):
    # Placeholder logic — real TTS will come later
    return {"message": f"Generated audio for: {data.text}", "audio_url": "/static/sample.wav"}
