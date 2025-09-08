from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ContactVerificationResult(BaseModel):
    email_verification: Optional[Dict[str, Any]] = Field(
        None,
        description="Email validation results including format, deliverability, and disposable status",
    )
    phone_verification: Optional[Dict[str, Any]] = Field(
        None,
        description="Phone number validation results including format, carrier, and geographic data",
    )
    risk_score: float = Field(
        ge=0,
        le=1,
        description="Contact information fraud risk score (0=low risk, 1=high risk)",
    )
    confidence: float = Field(
        ge=0, le=1, description="Confidence level in the risk assessment"
    )


class AIContentResult(BaseModel):
    overall_ai_probability: float = Field(
        ge=0, le=1, description="Overall probability that content was AI-generated"
    )
    sections_analyzed: Dict[str, float] = Field(
        default={}, description="AI probability scores for individual resume sections"
    )
    suspicious_sections: List[str] = Field(
        default=[], description="Resume sections flagged as likely AI-generated"
    )
    confidence: float = Field(
        ge=0, le=1, description="Confidence level in the AI detection analysis"
    )


class DocumentAnalysisResult(BaseModel):
    authenticity_indicators: Dict[str, Any] = {}
    suspicious_patterns: List[str] = []
    risk_score: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)


class FraudDetectionResult(BaseModel):
    overall_risk_score: float = Field(
        ge=0, le=1, description="Combined fraud risk score from all detection methods"
    )
    risk_level: RiskLevel = Field(
        description="Risk classification: low, medium, or high"
    )
    confidence: float = Field(
        ge=0, le=1, description="Overall confidence in the fraud assessment"
    )
    detected_issues: List[str] = Field(
        default=[], description="List of specific fraud indicators found"
    )
    contact_verification: Optional[ContactVerificationResult] = Field(
        None, description="Contact information verification results"
    )
    ai_content_analysis: Optional[AIContentResult] = Field(
        None, description="AI content detection results"
    )
    document_analysis: Optional[DocumentAnalysisResult] = Field(
        None, description="Document authenticity analysis results"
    )
    analysis_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when analysis was performed",
    )


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
