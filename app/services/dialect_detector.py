# app/services/dialect_detector.py
"""
Simple dialect detection module.
Two modes:
- Fast heuristic using keyword lists for Sheng/Slang
- Embedding-based classifier stub (for production use)

For now we implement a lightweight keyword-based classifier that inspects ASR text.
"""

from typing import Literal

# Small keyword maps — expand with real data later
_SHENG_KEYWORDS = {"bro","sawa","poa","niko","manze","sasa","mbona"}
_KIMVITA_KEYWORDS = {"mji","bahari","fort","ng'ambo"}  # placeholders
_KIAMU_KEYWORDS = {"kama","nyinyi"}  # placeholders

def detect_dialect_from_text(text: str) -> Literal["standard","sheng","kimvita","kiamu"]:
    txt = text.lower()
    words = set(txt.split())
    if len(words & _SHENG_KEYWORDS) >= 1:
        return "sheng"
    if len(words & _KIMVITA_KEYWORDS) >= 1:
        return "kimvita"
    if len(words & _KIAMU_KEYWORDS) >= 1:
        return "kiamu"
    return "standard"
