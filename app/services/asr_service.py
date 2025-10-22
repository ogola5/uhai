# app/services/asr_service.py
import os
import tempfile
import torch
from faster_whisper import WhisperModel

# Device config
device = "cuda" if torch.cuda.is_available() else "cpu"

# Model selection: keep small/medium for latency; swap for fine-tuned paths later
ASR_MODEL_NAME = os.getenv("ASR_MODEL", "medium")  # set env var if needed
_asr_model = WhisperModel(ASR_MODEL_NAME, device=device)

def transcribe_file(path: str, task: str = "transcribe", language: str = "sw"):
    """
    Synchronous transcription wrapper.
    Returns string transcript.
    """
    segments, info = _asr_model.transcribe(path, task=task, language=language)
    text = " ".join([seg.text.strip() for seg in segments if seg.text.strip()])
    return text

def transcribe_bytes(audio_bytes: bytes, suffix: str = ".wav", language: str = "sw"):
    """
    Writes bytes to temp file and transcribes.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    try:
        text = transcribe_file(tmp_path, language=language)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
    return text
