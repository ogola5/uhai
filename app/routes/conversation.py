# app/routes/conversation.py
from fastapi import APIRouter, UploadFile, File
import asyncio
from app.services.asr_service import transcribe_bytes
from app.services.nlp_service import simple_response
from app.services.tts_service import synthesize_text  # ✅ fixed import

router = APIRouter(prefix="/conversation", tags=["Conversation"])

@router.post("/speak")
async def converse(file: UploadFile = File(...)):
    """
    Upload user audio; returns transcription, reply text, and audio reply path.
    """
    audio_bytes = await file.read()
    
    # Run ASR (speech → text)
    loop = asyncio.get_event_loop()
    transcription = await loop.run_in_executor(None, transcribe_bytes, audio_bytes, ".wav", "sw")

    # Generate reply (simple NLP)
    reply_text, detected_dialect = simple_response(transcription)

    # Generate voice reply (text → speech)
    reply_audio_path = await loop.run_in_executor(None, synthesize_text, reply_text)

    return {
        "transcription": transcription,
        "reply_text": reply_text,
        "reply_audio": reply_audio_path,
        "dialect": detected_dialect
    }
