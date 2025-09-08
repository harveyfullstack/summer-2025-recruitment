import pytest
from app.services.document_processor import DocumentProcessor


class TestDocumentProcessor:
    @pytest.mark.asyncio
    async def test_process_txt_file(self):
        content = b"John Smith\nEmail: john@example.com\nPhone: (555) 123-4567"
        result = await DocumentProcessor.extract_text_and_metadata(content, "test.txt")

        assert result["metadata"]["format"] == "txt"
        assert "john@example.com" in result["text"]
        assert result["metadata"]["file_size"] == len(content)

    @pytest.mark.asyncio
    async def test_unsupported_file_type(self):
        content = b"test content"

        with pytest.raises(ValueError, match="Unsupported file type"):
            await DocumentProcessor.extract_text_and_metadata(content, "test.xyz")

    @pytest.mark.asyncio
    async def test_txt_encoding_fallback(self):
        content = "Test with special chars: café".encode("latin-1")
        result = await DocumentProcessor.extract_text_and_metadata(content, "test.txt")

        assert result["metadata"]["format"] == "txt"
        assert "café" in result["text"]
