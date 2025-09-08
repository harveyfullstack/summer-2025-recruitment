import pytest
from fastapi import HTTPException, UploadFile
from io import BytesIO
from app.core.validation import FileValidator


class MockUploadFile:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.content = content
        self.file = BytesIO(content)

    async def read(self):
        return self.content


class TestFileValidator:
    @pytest.mark.asyncio
    async def test_valid_pdf_file(self):
        file = MockUploadFile("test.pdf", b"valid pdf content")
        result = await FileValidator.validate_file(file)
        assert result == b"valid pdf content"

    @pytest.mark.asyncio
    async def test_valid_txt_file(self):
        file = MockUploadFile("test.txt", b"valid text content")
        result = await FileValidator.validate_file(file)
        assert result == b"valid text content"

    @pytest.mark.asyncio
    async def test_invalid_file_type(self):
        file = MockUploadFile("test.exe", b"invalid content")

        with pytest.raises(HTTPException) as exc_info:
            await FileValidator.validate_file(file)

        assert exc_info.value.status_code == 400
        assert "Unsupported file type" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_empty_file(self):
        file = MockUploadFile("test.pdf", b"")

        with pytest.raises(HTTPException) as exc_info:
            await FileValidator.validate_file(file)

        assert exc_info.value.status_code == 400
        assert "Empty file" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_no_filename(self):
        file = MockUploadFile("", b"content")
        file.filename = None

        with pytest.raises(HTTPException) as exc_info:
            await FileValidator.validate_file(file)

        assert exc_info.value.status_code == 400
        assert "No filename" in exc_info.value.detail
