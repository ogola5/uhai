# app/services/nlp_service.py
"""
Minimal NLP: rule-based response generator + LLM hook placeholder.
Returns reply text and dialect tag suggestion.
"""

from typing import Tuple
from .dialect_detector import detect_dialect_from_text

def simple_response(text: str) -> Tuple[str,str]:
    """
    Return (reply_text, dialect). Rule-based for demo.
    """
    t = text.lower()
    # Greetings
    if any(g in t for g in ["habari","hi","hello","bonjour","sasa"]):
        reply = "Nzuri sana. Naweza kusaidia vipi?"
    # Ask name
    elif "jina" in t or "who are you" in t:
        reply = "Mimi ni Uhai Voice, mshauri wa sauti wa Kiswahili."
    # Tourism example
    elif "fort" in t or "fort jesus" in t or "ng'ambo" in t:
        reply = "Fort Jesus ni kivutio cha kihistoria huko Mombasa. Unataka maelezo ya ziada?"
    else:
        reply = "Samahani, ninaelewa kwa kiasi. Unaweza kujaribu tena kwa sentensi fupi?"
    dialect = detect_dialect_from_text(text)
    return reply, dialect
