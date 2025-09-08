from fastapi import HTTPException, UploadFile
from app.core.config import settings


class FileValidator:
    @staticmethod
    async def validate_file(file: UploadFile) -> bytes:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        file_extension = file.filename.lower().split(".")[-1]
        if file_extension not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(settings.ALLOWED_FILE_TYPES).upper()}",
            )

        file_content = await file.read()

        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file provided")

        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE // 1024 // 1024}MB",
            )

        if file_extension == "txt":
            try:
                file_content.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    file_content.decode("latin-1")
                except UnicodeDecodeError:
                    raise HTTPException(
                        status_code=400, detail="Invalid text file encoding"
                    )

        return file_content
