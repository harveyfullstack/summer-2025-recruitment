from typing import Dict, Any, List, Optional
from app.models.schemas import RiskLevel
from app.core.config import settings


class FraudScoringService:
    @staticmethod
    def calculate_overall_risk(
        contact_result: Optional[Dict[str, Any]] = None,
        ai_result: Optional[Dict[str, Any]] = None,
        document_result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        contact_score = contact_result.get("risk_score", 0.0) if contact_result else 0.0
        ai_score = ai_result.get("overall_ai_probability", 0.0) if ai_result else 0.0
        document_score = (
            document_result.get("risk_score", 0.0) if document_result else 0.0
        )

        overall_risk_score = (
            contact_score * settings.CONTACT_WEIGHT
            + ai_score * settings.AI_CONTENT_WEIGHT
            + document_score * settings.DOCUMENT_WEIGHT
        )

        risk_level = FraudScoringService._determine_risk_level(overall_risk_score)

        detected_issues = []
        if contact_result:
            detected_issues.extend(
                FraudScoringService._extract_contact_issues(contact_result)
            )
        if ai_result:
            detected_issues.extend(FraudScoringService._extract_ai_issues(ai_result))
        if document_result:
            detected_issues.extend(document_result.get("suspicious_patterns", []))

        confidence_scores = []
        if contact_result:
            confidence_scores.append(contact_result.get("confidence", 0.0))
        if ai_result:
            confidence_scores.append(ai_result.get("confidence", 0.0))
        if document_result:
            confidence_scores.append(document_result.get("confidence", 0.0))

        overall_confidence = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores
            else 0.0
        )

        return {
            "overall_risk_score": overall_risk_score,
            "risk_level": risk_level,
            "confidence": overall_confidence,
            "detected_issues": detected_issues,
            "contact_verification": contact_result,
            "ai_content_analysis": ai_result,
            "document_analysis": document_result,
        }

    @staticmethod
    def _determine_risk_level(score: float) -> RiskLevel:
        if score >= settings.HIGH_RISK_THRESHOLD:
            return RiskLevel.HIGH
        elif score >= settings.MEDIUM_RISK_THRESHOLD:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    @staticmethod
    def _extract_contact_issues(contact_result: Dict[str, Any]) -> List[str]:
        issues = []

        email_verification = contact_result.get("email_verification", {})
        if email_verification:
            if not email_verification.get("valid", True):
                issues.append("Invalid email format detected")
            if email_verification.get("disposable", False):
                issues.append("Disposable email address detected")
            if not email_verification.get("deliverable", True):
                issues.append("Email address may not be deliverable")

        phone_verification = contact_result.get("phone_verification", {})
        if phone_verification:
            if not phone_verification.get("valid", True):
                issues.append("Invalid phone number format detected")

        return issues

    @staticmethod
    def _extract_ai_issues(ai_result: Dict[str, Any]) -> List[str]:
        issues = []

        overall_probability = ai_result.get("overall_ai_probability", 0.0)
        if overall_probability > 0.7:
            issues.append("High probability of AI-generated content detected")
        elif overall_probability > 0.4:
            issues.append("Moderate probability of AI-generated content detected")

        suspicious_sections = ai_result.get("suspicious_sections", [])
        for section in suspicious_sections:
            issues.append(f"AI-generated content detected in {section} section")

        return issues
