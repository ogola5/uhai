# app/services/tts_service.py
import os
import tempfile
import torch
import asyncio
from TTS.api import TTS

# Detect device safely
use_gpu = torch.cuda.is_available()
device = "cuda" if use_gpu else "cpu"

# Default model (change to Swahili/multilingual later)
TTS_MODEL = os.getenv("TTS_MODEL", "tts_models/en/ljspeech/tacotron2-DDC")

# Initialize model safely
_tts = TTS(model_name=TTS_MODEL, progress_bar=False, gpu=use_gpu)


# --- 1. Sync TTS ---
def tts_to_file_sync(text: str, language: str = "en") -> str:
    """
    Synchronous text-to-speech: generate a WAV file from text.
    Returns the path to the generated audio file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        output_path = tmp_audio.name
    _tts.tts_to_file(text=text, file_path=output_path)
    return output_path


# --- 2. Async TTS wrapper ---
async def tts_to_file(text: str, language: str = "en") -> str:
    """
    Asynchronous version of TTS for FastAPI endpoints.
    Runs in a background thread to avoid blocking.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, tts_to_file_sync, text, language)


# --- 3. Legacy compatibility (for conversation.py and tts.py) ---
def synthesize_text(text: str, language: str = "en") -> str:
    """
    Wrapper for backward compatibility.
    Calls the same sync TTS function internally.
    """
    return tts_to_file_sync(text, language)
