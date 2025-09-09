import pytest
from unittest.mock import AsyncMock, patch
from app.services.contact_verification import ContactVerificationService


class TestContactVerificationService:
    @pytest.mark.asyncio
    async def test_verify_contact_info_no_api_key(self):
        service = ContactVerificationService()

        with patch(
            "app.services.contact_verification.settings.ABSTRACT_EMAIL_API_KEY", ""
        ), patch(
            "app.services.contact_verification.settings.ABSTRACT_PHONE_API_KEY", ""
        ), patch(
            "app.services.contact_verification.settings.ABSTRACT_IP_API_KEY", ""
        ):
            result = await service.verify_contact_info(
                "John Doe john@example.com (555) 123-4567"
            )

        assert "email_verification" in result
        assert "phone_verification" in result
        assert "risk_score" in result
        assert "confidence" in result
        assert result["confidence"] == 0.5

        await service.close()

    @pytest.mark.asyncio
    async def test_email_verification_fallback(self):
        service = ContactVerificationService()

        with patch(
            "app.services.contact_verification.settings.ABSTRACT_EMAIL_API_KEY", ""
        ):
            email_result, api_used = await service._verify_email("test@example.com")

        assert isinstance(email_result, dict)
        assert isinstance(api_used, bool)
        assert api_used == False
        assert "valid" in email_result
        assert "disposable" in email_result
        assert "deliverable" in email_result

        await service.close()

    @pytest.mark.asyncio
    async def test_phone_verification_fallback(self):
        service = ContactVerificationService()

        with patch(
            "app.services.contact_verification.settings.ABSTRACT_PHONE_API_KEY", ""
        ):
            phone_result, api_used = await service._verify_phone("(555) 123-4567")

        assert isinstance(phone_result, dict)
        assert isinstance(api_used, bool)
        assert api_used == False
        assert "valid" in phone_result
        assert "country" in phone_result

        await service.close()

    @pytest.mark.asyncio
    async def test_ip_verification_fallback(self):
        service = ContactVerificationService()

        with patch(
            "app.services.contact_verification.settings.ABSTRACT_IP_API_KEY", ""
        ):
            ip_result, api_used = await service._verify_ip_location("192.168.1.1")

        assert isinstance(ip_result, dict)
        assert isinstance(api_used, bool)
        assert api_used == False
        assert "ip_address" in ip_result
        assert "country_code" in ip_result
        assert "is_vpn" in ip_result

        await service.close()

    def test_confidence_calculation(self):
        service = ContactVerificationService()

        confidence_all_success = service._calculate_verification_confidence(3, 3)
        assert confidence_all_success == 0.9

        confidence_partial = service._calculate_verification_confidence(2, 3)
        assert abs(confidence_partial - 0.77) < 0.01

        confidence_none = service._calculate_verification_confidence(0, 3)
        assert confidence_none == 0.5

        confidence_no_calls = service._calculate_verification_confidence(0, 0)
        assert confidence_no_calls == 0.5

    def test_extract_boolean_helper(self):
        service = ContactVerificationService()

        assert service._extract_boolean({"key": True}, "key") == True
        assert service._extract_boolean({"key": {"value": True}}, "key") == True
        assert service._extract_boolean({"key": "TRUE"}, "key") == True
        assert service._extract_boolean({"key": "false"}, "key") == False
        assert service._extract_boolean({}, "key") == False

    def test_fallback_email_result(self):
        service = ContactVerificationService()

        result = service._fallback_email_result(True)
        assert result["valid"] == True
        assert result["quality_score"] == 0.5

        result = service._fallback_email_result(False)
        assert result["valid"] == False
        assert result["quality_score"] == 0.0

    def test_fallback_ip_result(self):
        service = ContactVerificationService()

        result = service._fallback_ip_result("192.168.1.1")
        assert result["ip_address"] == "192.168.1.1"
        assert result["country_code"] == "UNKNOWN"
        assert result["is_vpn"] == False
        assert result["is_tor"] == False
