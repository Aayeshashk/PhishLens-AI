import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Add the project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.api.url_analysis import router as url_analysis_router


app = FastAPI(
    title="PhishLens AI",
    description="AI-powered phishing and scam detection platform",
    version="1.0.0",
)


# Allow the React frontend to communicate with
# the FastAPI backend during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(url_analysis_router)


@app.get("/")
def root():
    return {
        "name": "PhishLens AI",
        "status": "running",
        "message": "Phishing detection platform is online.",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }