from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.models.schemas import HealthResponse, ErrorResponse, FraudDetectionResult, RiskLevel
from datetime import datetime

app = FastAPI(
    title="Resume Fraud Detection System",
    description="AI-powered resume fraud detection system",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Resume Fraud Detection System", "status": "running"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy")

@app.post("/api/v1/detect/resume", response_model=FraudDetectionResult)
async def detect_resume_fraud(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    return FraudDetectionResult(
        overall_risk_score=0.1,
        risk_level=RiskLevel.LOW,
        confidence=0.8,
        detected_issues=[]
    )