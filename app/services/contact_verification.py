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

    async def verify_contact_info(
        self, text: str, client_ip: str = None
    ) -> Dict[str, Any]:
        contact_info = self._extract_contact_info(text)

        email_result = None
        phone_result = None
        ip_result = None

        api_success_count = 0
        total_api_calls = 0

        if contact_info.get("email"):
            email_result, email_api_used = await self._verify_email(
                contact_info["email"]
            )
            total_api_calls += 1
            if email_api_used:
                api_success_count += 1

        if contact_info.get("phone"):
            phone_result, phone_api_used = await self._verify_phone(
                contact_info["phone"]
            )
            total_api_calls += 1
            if phone_api_used:
                api_success_count += 1

        if client_ip and settings.ABSTRACT_API_KEY:
            ip_result, ip_api_used = await self._verify_ip_location(client_ip)
            total_api_calls += 1
            if ip_api_used:
                api_success_count += 1

        risk_score = self._calculate_contact_risk(email_result, phone_result, ip_result)
        confidence = self._calculate_verification_confidence(
            api_success_count, total_api_calls
        )

        return {
            "email_verification": email_result,
            "phone_verification": phone_result,
            "ip_verification": ip_result,
            "risk_score": risk_score,
            "confidence": confidence,
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

    async def _verify_email(self, email: str) -> tuple[Dict[str, Any], bool]:
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
            }, False

        try:
            response = await self.client.get(
                settings.ABSTRACT_EMAIL_API,
                params={"api_key": settings.ABSTRACT_API_KEY, "email": email},
            )

            if response.status_code == 200:
                data = response.json()

                if "error" in data:
                    return self._fallback_email_result(local_valid)

                is_valid_format = self._extract_boolean(data, "is_valid_format")
                is_smtp_valid = self._extract_boolean(data, "is_smtp_valid")
                is_disposable = self._extract_boolean(data, "is_disposable_email")
                deliverability = data.get("deliverability", "UNKNOWN")
                quality_score = float(data.get("quality_score", 0.0))

                is_valid = is_valid_format and is_smtp_valid
                is_deliverable = deliverability in ["DELIVERABLE", "RISKY"]

                return {
                    "valid": is_valid,
                    "disposable": is_disposable,
                    "deliverable": is_deliverable,
                    "quality_score": quality_score,
                }, True
        except Exception:
            pass

        return {
            "valid": local_valid,
            "disposable": False,
            "deliverable": local_valid,
            "quality_score": 0.5 if local_valid else 0.0,
        }

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

    async def _verify_ip_location(self, ip_address: str) -> Dict[str, Any]:
        try:
            response = await self.client.get(
                settings.ABSTRACT_IP_API,
                params={
                    "api_key": settings.ABSTRACT_API_KEY,
                    "ip_address": ip_address,
                    "fields": "country_code,is_vpn,connection,threat,abuse_confidence",
                },
            )

            if response.status_code == 200:
                data = response.json()

                if "error" in data:
                    return self._fallback_ip_result(ip_address)

                connection = data.get("connection", {})
                threat = data.get("threat", {})

                return {
                    "ip_address": ip_address,
                    "country_code": data.get("country_code", "UNKNOWN"),
                    "is_vpn": connection.get("is_vpn", False),
                    "is_tor": threat.get("is_tor", False),
                    "threat_level": threat.get("threat_level", "unknown"),
                    "abuse_confidence": threat.get("abuse_confidence", 0),
                }
        except Exception:
            pass

        return self._fallback_ip_result(ip_address)

    def _fallback_ip_result(self, ip_address: str) -> Dict[str, Any]:
        return {
            "ip_address": ip_address,
            "country_code": "UNKNOWN",
            "is_vpn": False,
            "is_tor": False,
            "threat_level": "unknown",
            "abuse_confidence": 0,
        }

    def _calculate_contact_risk(
        self,
        email_result: Optional[Dict],
        phone_result: Optional[Dict],
        ip_result: Optional[Dict] = None,
    ) -> float:
        risk = 0.0

        if email_result:
            if not email_result.get("valid", True):
                risk += 0.3
            if email_result.get("disposable", False):
                risk += 0.5
            if not email_result.get("deliverable", True):
                risk += 0.2

            quality_score = email_result.get("quality_score", 0.5)
            if quality_score < 0.3:
                risk += 0.3
            elif quality_score < 0.6:
                risk += 0.1

        if phone_result:
            if not phone_result.get("valid", True):
                risk += 0.3

        if ip_result:
            if ip_result.get("is_tor", False):
                risk += 0.6
            elif ip_result.get("is_vpn", False):
                risk += 0.3

            abuse_confidence = ip_result.get("abuse_confidence", 0)
            if abuse_confidence > 50:
                risk += 0.4
            elif abuse_confidence > 25:
                risk += 0.2

        return min(risk, 1.0)

    def _extract_boolean(self, data: Dict, key: str) -> bool:
        value = data.get(key)
        if isinstance(value, bool):
            return value
        elif isinstance(value, dict):
            return value.get("value", False)
        elif isinstance(value, str):
            return value.upper() == "TRUE"
        return False

    def _fallback_email_result(self, local_valid: bool) -> Dict[str, Any]:
        return {
            "valid": local_valid,
            "disposable": False,
            "deliverable": local_valid,
            "quality_score": 0.5 if local_valid else 0.0,
        }

    async def close(self):
        await self.client.aclose()
