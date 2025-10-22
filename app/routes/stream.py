# app/routes/stream.py
import json
import asyncio
import tempfile
import os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.asr_service import transcribe_file, transcribe_bytes
from app.services.nlp_service import simple_response
from app.services.tts_service import tts_to_file_sync  # sync method used in thread

router = APIRouter()

@router.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    Protocol:
    - Client sends binary audio chunks (PCM16 or webm/opus) messages
    - Server buffers until sufficient length then runs partial transcription
    - Server sends JSON messages:
      {"type":"partial","text": "..."}
      {"type":"final","text": "..."}
      {"type":"reply_ready","audio_path": "..."}
    """
    await websocket.accept()
    buffer = bytearray()
    try:
        while True:
            data = await websocket.receive()
            if 'bytes' in data:
                chunk = data['bytes']
                buffer.extend(chunk)
                # heuristic: run ASR every ~2s of audio (adjust chunk size)
                if len(buffer) > 16000 * 2 * 2:  # ~2s @16k mono int16
                    # write temporary file and transcribe in thread to avoid blocking
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        tmp.write(buffer)
                        tmp_path = tmp.name
                    # Transcribe in executor
                    loop = asyncio.get_event_loop()
                    transcription = await loop.run_in_executor(None, transcribe_file, tmp_path)
                    await websocket.send_json({"type":"partial","text": transcription})
                    # clear buffer to keep streaming incremental
                    buffer = bytearray()
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass
            elif 'text' in data:
                msg = data['text']
                # Expect control messages e.g., {"cmd":"finalize"}
                try:
                    m = json.loads(msg)
                except:
                    m = {}
                if m.get("cmd") == "finalize":
                    # Finalize: run ASR on remaining buffer and produce reply
                    if buffer:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                            tmp.write(buffer)
                            tmp_path = tmp.name
                        loop = asyncio.get_event_loop()
                        transcription = await loop.run_in_executor(None, transcribe_file, tmp_path)
                        await websocket.send_json({"type":"final","text": transcription})
                        # NLP + TTS
                        reply_text, dialect = simple_response(transcription)
                        # Run blocking TTS in executor (sync tts_to_file_sync)
                        out_path = await loop.run_in_executor(None, tts_to_file_sync, reply_text, None)
                        await websocket.send_json({"type":"reply_ready","audio_path": out_path, "reply_text": reply_text, "dialect": dialect})
                        buffer = bytearray()
                        try:
                            os.remove(tmp_path)
                        except Exception:
                            pass
    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        await websocket.close()
        print("WS error:", e)
