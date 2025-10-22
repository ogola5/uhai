from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import all route modules
from app.routes import asr, tts, conversation, stream

app = FastAPI(
    title="Uhai Voice AI",
    description="Swahili + African dialect Voice AI stack (ASR ↔ NLP ↔ TTS)",
    version="1.2.0"
)

# Mount static directory (for serving generated audio files)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Enable CORS (for frontend/browser-based streaming client)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(asr.router)
app.include_router(tts.router)
app.include_router(conversation.router)
app.include_router(stream.router)

@app.get("/")
def root():
    return {
        "message": "✅ Uhai Voice AI is running",
        "routes": [
            "/asr/transcribe",
            "/tts/synthesize",
            "/conversation/speak",
            "/ws/stream",
        ],
        "docs": "/docs",
        "static_files": "/static",
    }

@app.on_event("startup")
async def startup_event():
    print("🚀 Uhai Voice AI backend starting... models will load on first use.")

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Uhai Voice AI backend shutting down.")
