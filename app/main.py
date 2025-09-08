from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Resume Fraud Detection System",
    description="AI-powered resume fraud detection system",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Resume Fraud Detection System", "status": "running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }