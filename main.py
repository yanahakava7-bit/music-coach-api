from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import tempfile

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "music-coach-api is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze-track")
async def analyze_track(track: UploadFile = File(...)):
    suffix = os.path.splitext(track.filename or "track.wav")[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        data = await track.read()
        f.write(data)
        path = f.name

    result = {
        "status": "ok",
        "filename": track.filename,
        "notes": "stub: replace with real audio analysis later",
        "suggestions": [
            "Check harshness around 2–5 kHz if the mix feels sharp",
            "Make sure kick/sub don't fight: pick one to dominate 40–80 Hz"
        ],
    }

    try:
        os.unlink(path)
    except Exception:
        pass

    return JSONResponse(result)
