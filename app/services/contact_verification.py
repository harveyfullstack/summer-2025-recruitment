import httpx
import re
from typing import Dict, Any, Optional
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException
from app.core.config import settings


class ContactVerificationService:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def verify_contact_info(self, text: str) -> Dict[str, Any]:
        contact_info = self._extract_contact_info(text)

        email_result = None
        phone_result = None

        if contact_info.get("email"):
            email_result = await self._verify_email(contact_info["email"])

        if contact_info.get("phone"):
            phone_result = await self._verify_phone(contact_info["phone"])

        risk_score = self._calculate_contact_risk(email_result, phone_result)

        return {
            "email_verification": email_result,
            "phone_verification": phone_result,
            "risk_score": risk_score,
            "confidence": 0.8,
        }

    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        phone_pattern = (
            r"(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})"
        )

        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)

        return {
            "email": emails[0] if emails else None,
            "phone": "".join(phones[0]) if phones else None,
        }

    async def _verify_email(self, email: str) -> Dict[str, Any]:
        try:
            validate_email(email)
            local_valid = True
        except EmailNotValidError:
            local_valid = False

        if not settings.ABSTRACT_API_KEY:
            return {
                "valid": local_valid,
                "disposable": False,
                "deliverable": local_valid,
            }

        try:
            response = await self.client.get(
                settings.ABSTRACT_EMAIL_API,
                params={"api_key": settings.ABSTRACT_API_KEY, "email": email},
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "valid": data.get("is_valid_format", {}).get("value", False),
                    "disposable": data.get("is_disposable_email", {}).get(
                        "value", False
                    ),
                    "deliverable": data.get("deliverability", "") == "DELIVERABLE",
                }
        except Exception:
            pass

        return {"valid": local_valid, "disposable": False, "deliverable": local_valid}

    async def _verify_phone(self, phone: str) -> Dict[str, Any]:
        try:
            parsed = phonenumbers.parse(phone, "US")
            local_valid = phonenumbers.is_valid_number(parsed)
            country = phonenumbers.region_code_for_number(parsed)
        except NumberParseException:
            local_valid = False
            country = None

        if not settings.ABSTRACT_API_KEY:
            return {"valid": local_valid, "country": country, "carrier": None}

        try:
            response = await self.client.get(
                settings.ABSTRACT_PHONE_API,
                params={"api_key": settings.ABSTRACT_API_KEY, "phone": phone},
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "valid": data.get("valid", False),
                    "country": data.get("country", {}).get("code"),
                    "carrier": data.get("carrier"),
                }
        except Exception:
            pass

        return {"valid": local_valid, "country": country, "carrier": None}

    def _calculate_contact_risk(
        self, email_result: Optional[Dict], phone_result: Optional[Dict]
    ) -> float:
        risk = 0.0

        if email_result:
            if not email_result.get("valid", True):
                risk += 0.3
            if email_result.get("disposable", False):
                risk += 0.4
            if not email_result.get("deliverable", True):
                risk += 0.2

        if phone_result:
            if not phone_result.get("valid", True):
                risk += 0.3

        return min(risk, 1.0)

    async def close(self):
        await self.client.aclose()
