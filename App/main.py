import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from App.api import routes_auth, routes_alert
from App.core.logger import logger
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="🎤 Voice Authentication API",
    description="Authenticate users by voice and detect spoofed or recorded attempts.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(routes_alert.router, prefix="/api", tags=["Alerts"])

@app.on_event("startup")
async def startup_event():
    logger.info("Voice Authentication API started successfully!")
    os.makedirs("models/embeddings", exist_ok=True)
    os.makedirs("audio_samples", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

@app.get("/")
def root():
    return {
        "status": "Voice Authentication API is running 🚀",
        "endpoints": {
            "enroll": "/api/auth/enroll",
            "verify": "/api/auth/verify",
            "health": "/api/health",
            "docs": "/docs"
        }
    }

''''@app.post("/train")
def train_models():
    try:
        from App.training.train import train_spoof_model, train_speaker_model
        logger.info("Starting model training...")
        train_spoof_model()
        train_speaker_model()
        return {"message": "Model training completed successfully!"}
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))'''