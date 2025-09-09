from decouple import config


class Settings:
    ABSTRACT_API_KEY: str = config("ABSTRACT_API_KEY", default="")
    WINSTON_AI_API_KEY: str = config("WINSTON_AI_API_KEY", default="")
    SECRET_KEY: str = config("SECRET_KEY", default="dev-secret-key")
    DEBUG: bool = config("DEBUG", default=False, cast=bool)
    DOCS_ENABLED: bool = config("DOCS_ENABLED", default=False, cast=bool)

    MAX_FILE_SIZE: int = 10485760
    ALLOWED_FILE_TYPES = ["pdf", "docx", "txt"]

    ABSTRACT_EMAIL_API = "https://emailvalidation.abstractapi.com/v1/"
    ABSTRACT_PHONE_API = "https://phonevalidation.abstractapi.com/v1/"
    ABSTRACT_IP_API = "https://ipgeolocation.abstractapi.com/v1/"
    WINSTON_AI_API = "https://api.gowinston.ai/v2/ai-content-detection"

    CONTACT_WEIGHT = 0.40
    AI_CONTENT_WEIGHT = 0.35
    DOCUMENT_WEIGHT = 0.25

    HIGH_RISK_THRESHOLD = 0.70
    MEDIUM_RISK_THRESHOLD = 0.40


settings = Settings()
