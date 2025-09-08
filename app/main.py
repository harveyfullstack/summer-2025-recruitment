from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from app.models.schemas import (
    HealthResponse,
    FraudDetectionResult,
    ContactVerificationResult,
    AIContentResult,
    DocumentAnalysisResult,
)
from app.services.document_processor import DocumentProcessor
from app.services.contact_verification import ContactVerificationService
from app.services.ai_detection import AIContentDetectionService
from app.services.document_analysis import DocumentAnalysisService
from app.services.fraud_scorer import FraudScoringService
from app.core.validation import FileValidator
from app.core.rate_limiter import limiter, rate_limit_handler
from app.core.cache import cache
from slowapi.errors import RateLimitExceeded

app = FastAPI(
    title="Resume Fraud Detection System",
    description="AI-powered resume fraud detection system",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)


@app.get("/")
async def root():
    return {"message": "Resume Fraud Detection System", "status": "running"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy")


@app.post("/api/v1/verify/contact")
@limiter.limit("10/minute")
async def verify_contact_only(request: Request, file: UploadFile = File(...)):
    file_content = await FileValidator.validate_file(file)
    document_data = await DocumentProcessor.extract_text_and_metadata(
        file_content, file.filename
    )

    contact_service = ContactVerificationService()
    result = await contact_service.verify_contact_info(document_data["text"])
    await contact_service.close()

    return ContactVerificationResult(**result)


@app.post("/api/v1/analyze/content")
@limiter.limit("10/minute")
async def analyze_ai_content_only(request: Request, file: UploadFile = File(...)):
    file_content = await FileValidator.validate_file(file)
    document_data = await DocumentProcessor.extract_text_and_metadata(
        file_content, file.filename
    )

    ai_service = AIContentDetectionService()
    result = await ai_service.detect_ai_content(document_data["text"])
    await ai_service.close()

    return AIContentResult(**result)


@app.post("/api/v1/examine/document")
@limiter.limit("10/minute")
async def examine_document_only(request: Request, file: UploadFile = File(...)):
    file_content = await FileValidator.validate_file(file)
    document_data = await DocumentProcessor.extract_text_and_metadata(
        file_content, file.filename
    )

    result = DocumentAnalysisService.analyze_document_authenticity(
        document_data["metadata"]
    )
    return DocumentAnalysisResult(**result)


@app.post("/api/v1/detect/resume", response_model=FraudDetectionResult)
@limiter.limit("5/minute")
async def detect_resume_fraud(request: Request, file: UploadFile = File(...)):
    file_content = await FileValidator.validate_file(file)

    try:
        document_data = await DocumentProcessor.extract_text_and_metadata(
            file_content, file.filename
        )
        text = document_data["text"]
        metadata = document_data["metadata"]

        contact_service = ContactVerificationService()
        ai_service = AIContentDetectionService()

        contact_result = await contact_service.verify_contact_info(text)
        ai_result = await ai_service.detect_ai_content(text)
        document_result = DocumentAnalysisService.analyze_document_authenticity(
            metadata
        )

        await contact_service.close()
        await ai_service.close()

        contact_verification = ContactVerificationResult(**contact_result)
        ai_content_analysis = AIContentResult(**ai_result)
        document_analysis = DocumentAnalysisResult(**document_result)

        fraud_result = FraudScoringService.calculate_overall_risk(
            contact_result, ai_result, document_result
        )

        return FraudDetectionResult(
            overall_risk_score=fraud_result["overall_risk_score"],
            risk_level=fraud_result["risk_level"],
            confidence=fraud_result["confidence"],
            detected_issues=fraud_result["detected_issues"],
            contact_verification=contact_verification,
            ai_content_analysis=ai_content_analysis,
            document_analysis=document_analysis,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
