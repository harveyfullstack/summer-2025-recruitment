from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models.schemas import HealthResponse, FraudDetectionResult, RiskLevel
from app.services.document_processor import DocumentProcessor

app = FastAPI(
    title="Resume Fraud Detection System",
    description="AI-powered resume fraud detection system",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "Resume Fraud Detection System", "status": "running"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy")


@app.post("/api/v1/detect/resume", response_model=FraudDetectionResult)
async def detect_resume_fraud(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400, detail="Only PDF and DOCX files are supported"
        )

    file_content = await file.read()
    document_data = await DocumentProcessor.extract_text_and_metadata(
        file_content, file.filename
    )

    return FraudDetectionResult(
        overall_risk_score=0.1,
        risk_level=RiskLevel.LOW,
        confidence=0.8,
        detected_issues=[],
    )
