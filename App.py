import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import whisper

# ---------------- Fix Whisper cache issue ----------------
os.environ["XDG_CACHE_HOME"] = "/tmp/.cache"

# ---------------- Config ----------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize FastAPI
app = FastAPI(title="Whisper Audio Transcription API")

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Whisper model (use "small" for speed; can change to "base" or "medium")
try:
    model = whisper.load_model("small")
except Exception as e:
    raise RuntimeError(f"Error loading Whisper model: {str(e)}")


@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Upload an audio file and get the transcription.
    """
    try:
        # Save uploaded file temporarily
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Transcribe with Whisper
        result = model.transcribe(file_path)

        # Cleanup (optional: remove after processing)
        os.remove(file_path)

        # Return text output
        return {"filename": file.filename, "transcription": result.get("text", "")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
