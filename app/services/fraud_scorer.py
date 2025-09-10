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

        weighted_confidence = 0.0
        total_weight = 0.0

        if contact_result:
            contact_confidence = contact_result.get("confidence", 0.0)
            weighted_confidence += contact_confidence * settings.CONTACT_WEIGHT
            total_weight += settings.CONTACT_WEIGHT

        if ai_result:
            ai_confidence = ai_result.get("confidence", 0.0)
            weighted_confidence += ai_confidence * settings.AI_CONTENT_WEIGHT
            total_weight += settings.AI_CONTENT_WEIGHT

        if document_result:
            doc_confidence = document_result.get("confidence", 0.0)
            weighted_confidence += doc_confidence * settings.DOCUMENT_WEIGHT
            total_weight += settings.DOCUMENT_WEIGHT

        overall_confidence = (
            weighted_confidence / total_weight if total_weight > 0 else 0.0
        )

        explanation = FraudScoringService._generate_explanation(
            overall_risk_score, risk_level, detected_issues
        )
        recommendations = FraudScoringService._generate_recommendations(
            risk_level, detected_issues
        )

        return {
            "overall_risk_score": overall_risk_score,
            "risk_level": risk_level,
            "confidence": overall_confidence,
            "detected_issues": detected_issues,
            "explanation": explanation,
            "recommendations": recommendations,
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

    @staticmethod
    def _generate_explanation(
        score: float, risk_level: RiskLevel, issues: List[str]
    ) -> str:
        if risk_level == RiskLevel.LOW:
            return f"Low fraud risk detected (score: {score:.3f}). Resume appears legitimate with minimal suspicious indicators."
        elif risk_level == RiskLevel.MEDIUM:
            return f"Medium fraud risk detected (score: {score:.3f}). Several suspicious patterns identified requiring additional verification."
        else:
            return f"High fraud risk detected (score: {score:.3f}). Multiple fraud indicators present, recommend thorough investigation."

    @staticmethod
    def _generate_recommendations(
        risk_level: RiskLevel, issues: List[str]
    ) -> List[str]:
        recommendations = []

        if risk_level == RiskLevel.LOW:
            recommendations.append("Proceed with standard hiring process")
            if issues:
                recommendations.append("Consider minor verification of flagged items")
        elif risk_level == RiskLevel.MEDIUM:
            recommendations.append("Conduct additional verification before proceeding")
            recommendations.append("Verify contact information independently")
            if any("AI-generated" in issue for issue in issues):
                recommendations.append(
                    "Request clarification on resume content authenticity"
                )
        else:
            recommendations.append("Recommend thorough background investigation")
            recommendations.append("Verify all claims independently")
            recommendations.append(
                "Consider rejecting application pending investigation"
            )

        return recommendations
