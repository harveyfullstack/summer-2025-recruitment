import logging
from typing import Dict, Any, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class APIErrorType(Enum):
    AUTH_ERROR = "auth_error"
    QUOTA_EXCEEDED = "quota_exceeded"
    RATE_LIMITED = "rate_limited"
    SERVER_ERROR = "server_error"
    UNKNOWN_ERROR = "unknown_error"


class APIErrorHandler:
    @staticmethod
    def classify_api_error(
        status_code: int, response_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        if status_code == 401:
            return {
                "type": APIErrorType.AUTH_ERROR,
                "log_level": logging.ERROR,
                "should_fallback": True,
            }
        elif status_code == 402:
            return {
                "type": APIErrorType.QUOTA_EXCEEDED,
                "log_level": logging.CRITICAL,
                "should_fallback": True,
            }
        elif status_code == 429:
            return {
                "type": APIErrorType.RATE_LIMITED,
                "log_level": logging.WARNING,
                "should_fallback": True,
            }
        elif status_code >= 500:
            return {
                "type": APIErrorType.SERVER_ERROR,
                "log_level": logging.ERROR,
                "should_fallback": True,
            }
        else:
            return {
                "type": APIErrorType.UNKNOWN_ERROR,
                "log_level": logging.WARNING,
                "should_fallback": True,
            }

    @staticmethod
    def log_api_error(
        service_name: str,
        status_code: int,
        error_info: Dict[str, Any],
        response_data: Dict[str, Any] = None,
    ) -> None:
        error_type = error_info["type"]
        log_level = error_info["log_level"]

        message = f"{service_name} API error: {error_type.value} (HTTP {status_code})"

        extra_context = {
            "service": service_name,
            "status_code": status_code,
            "error_type": error_type.value,
        }

        if response_data and "error" in response_data:
            extra_context["api_error_message"] = response_data["error"]

        logger.log(log_level, message, extra=extra_context)

    @staticmethod
    def handle_api_response(service_name: str, response) -> Tuple[bool, Dict[str, Any]]:
        if response.status_code == 200:
            return True, {}

        try:
            response_data = response.json()
        except:
            response_data = {}

        error_info = APIErrorHandler.classify_api_error(
            response.status_code, response_data
        )
        APIErrorHandler.log_api_error(
            service_name, response.status_code, error_info, response_data
        )

        return False, error_info
