from faster_whisper import WhisperModel
import torch

# Load model once globally
device = "cuda" if torch.cuda.is_available() else "cpu"
model = WhisperModel("medium", device=device)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes audio file and returns the text.
    """
    segments, _ = model.transcribe(file_path)
    text = " ".join([seg.text for seg in segments])
    return text.strip()
