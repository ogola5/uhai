from fastapi import FastAPI
from app.routes import asr, tts

app = FastAPI(title="Uhai Voice AI")

# Include routes
app.include_router(asr.router)
app.include_router(tts.router)

@app.get("/")
def root():
    return {"message": "Uhai Voice AI is running"}
