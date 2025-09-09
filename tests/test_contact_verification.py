import pytest
from unittest.mock import AsyncMock, patch
from app.services.contact_verification import ContactVerificationService


class TestContactVerificationService:
    @pytest.mark.asyncio
    async def test_verify_contact_info_no_api_key(self):
        service = ContactVerificationService()

        with patch("app.services.contact_verification.settings.ABSTRACT_API_KEY", ""):
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

        email_result, api_used = await service._verify_email("test@example.com")

        assert isinstance(email_result, dict)
        assert isinstance(api_used, bool)
        assert api_used == False
        assert "valid" in email_result
        assert "disposable" in email_result
        assert "quality_score" in email_result

        await service.close()

    @pytest.mark.asyncio
    async def test_phone_verification_fallback(self):
        service = ContactVerificationService()

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

    @pytest.mark.asyncio
    async def test_abstract_api_success_simulation(self):
        service = ContactVerificationService()

        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "is_valid_format": {"value": True},
            "is_smtp_valid": {"value": True},
            "is_disposable_email": {"value": False},
            "deliverability": "DELIVERABLE",
            "quality_score": 0.85,
        }

        with patch(
            "app.services.contact_verification.settings.ABSTRACT_API_KEY", "test_key"
        ):
            with patch.object(service.client, "get", return_value=mock_response):
                email_result, api_used = await service._verify_email("test@example.com")

        assert api_used == True
        assert email_result["valid"] == True
        assert email_result["disposable"] == False
        assert email_result["quality_score"] == 0.85

        await service.close()

    @pytest.mark.asyncio
    async def test_abstract_api_error_handling(self):
        service = ContactVerificationService()

        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"error": "Invalid API key"}

        with patch(
            "app.services.contact_verification.settings.ABSTRACT_API_KEY", "invalid_key"
        ):
            with patch.object(service.client, "get", return_value=mock_response):
                email_result, api_used = await service._verify_email("test@example.com")

        assert api_used == False
        assert "valid" in email_result

        await service.close()
