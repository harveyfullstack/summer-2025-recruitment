from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ContactVerificationResult(BaseModel):
    email_verification: Optional[Dict[str, Any]] = None
    phone_verification: Optional[Dict[str, Any]] = None
    risk_score: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)


class AIContentResult(BaseModel):
    overall_ai_probability: float = Field(ge=0, le=1)
    sections_analyzed: Dict[str, float] = {}
    suspicious_sections: List[str] = []
    confidence: float = Field(ge=0, le=1)


class DocumentAnalysisResult(BaseModel):
    authenticity_indicators: Dict[str, Any] = {}
    suspicious_patterns: List[str] = []
    risk_score: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)


class FraudDetectionResult(BaseModel):
    overall_risk_score: float = Field(ge=0, le=1)
    risk_level: RiskLevel
    confidence: float = Field(ge=0, le=1)
    detected_issues: List[str] = []
    contact_verification: Optional[ContactVerificationResult] = None
    ai_content_analysis: Optional[AIContentResult] = None
    document_analysis: Optional[DocumentAnalysisResult] = None
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
