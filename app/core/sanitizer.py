import re
from typing import Optional


class InputSanitizer:
    @staticmethod
    def sanitize_email(email: str) -> Optional[str]:
        if not email or len(email) > 254:
            return None

        email = email.strip().lower()
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return None

        return email

    @staticmethod
    def sanitize_phone(phone: str) -> Optional[str]:
        if not phone or len(phone) > 20:
            return None

        phone = re.sub(r"[^\d+\-\(\)\s\.]", "", phone)
        if len(phone) < 10:
            return None

        return phone

    @staticmethod
    def sanitize_text(text: str, max_length: int = 5000) -> str:
        if not text:
            return ""

        text = text.strip()
        if len(text) > max_length:
            text = text[:max_length]

        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)

        return text

    @staticmethod
    def sanitize_ip(ip: str) -> Optional[str]:
        if not ip or len(ip) > 45:
            return None

        ip = ip.strip()

        if "." in ip:
            parts = ip.split(".")
            if len(parts) != 4:
                return None
            for part in parts:
                if not part.isdigit() or int(part) > 255:
                    return None
        elif ":" in ip:
            if not re.match(r"^[0-9a-fA-F:]+$", ip):
                return None
        else:
            return None

        return ip
