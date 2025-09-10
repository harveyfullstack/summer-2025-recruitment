import pytest
from app.services.fraud_scorer import FraudScoringService
from app.models.schemas import RiskLevel


class TestFraudScoringService:
    def test_calculate_low_risk(self):
        contact_result = {"risk_score": 0.1, "confidence": 0.9}
        ai_result = {"overall_ai_probability": 0.2, "confidence": 0.8}
        document_result = {"risk_score": 0.1, "confidence": 0.7}

        result = FraudScoringService.calculate_overall_risk(
            contact_result, ai_result, document_result
        )

        assert result["risk_level"] == RiskLevel.LOW
        assert result["overall_risk_score"] < 0.35
        assert len(result["detected_issues"]) == 0

    def test_calculate_high_risk(self):
        contact_result = {"risk_score": 0.8, "confidence": 0.9}
        ai_result = {"overall_ai_probability": 0.9, "confidence": 0.8}
        document_result = {"risk_score": 0.7, "confidence": 0.7}

        result = FraudScoringService.calculate_overall_risk(
            contact_result, ai_result, document_result
        )

        assert result["risk_level"] == RiskLevel.HIGH
        assert result["overall_risk_score"] >= 0.6

    def test_weighted_scoring_algorithm(self):
        contact_result = {"risk_score": 1.0, "confidence": 0.9}
        ai_result = {"overall_ai_probability": 0.0, "confidence": 0.8}
        document_result = {"risk_score": 0.0, "confidence": 0.7}

        result = FraudScoringService.calculate_overall_risk(
            contact_result, ai_result, document_result
        )

        expected_score = 1.0 * 0.45 + 0.0 * 0.35 + 0.0 * 0.20
        assert abs(result["overall_risk_score"] - expected_score) < 0.01

    def test_extract_contact_issues(self):
        contact_result = {
            "email_verification": {"valid": False, "disposable": True},
            "phone_verification": {"valid": False},
        }

        issues = FraudScoringService._extract_contact_issues(contact_result)

        assert "Invalid email format detected" in issues
        assert "Disposable email address detected" in issues
        assert "Invalid phone number format detected" in issues

    def test_extract_ai_issues(self):
        ai_result = {
            "overall_ai_probability": 0.8,
            "suspicious_sections": ["summary", "experience"],
        }

        issues = FraudScoringService._extract_ai_issues(ai_result)

        assert "High probability of AI-generated content detected" in issues
        assert "AI-generated content detected in summary section" in issues
        assert "AI-generated content detected in experience section" in issues
