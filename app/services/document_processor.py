import fitz
from docx import Document
from typing import Dict, Any, Optional
from datetime import datetime


class DocumentProcessor:
    @staticmethod
    async def extract_text_and_metadata(
        file_content: bytes, filename: str
    ) -> Dict[str, Any]:
        file_extension = filename.lower().split(".")[-1]

        if file_extension == "pdf":
            return DocumentProcessor._process_pdf(file_content)
        elif file_extension == "docx":
            return DocumentProcessor._process_docx(file_content)
        elif file_extension == "txt":
            return DocumentProcessor._process_txt(file_content, filename)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    @staticmethod
    def _process_pdf(file_content: bytes) -> Dict[str, Any]:
        doc = fitz.open(stream=file_content, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()

        metadata = doc.metadata

        doc.close()

        return {
            "text": text,
            "metadata": {
                "format": "pdf",
                "page_count": len(doc),
                "creation_date": metadata.get("creationDate"),
                "modification_date": metadata.get("modDate"),
                "author": metadata.get("author"),
                "creator": metadata.get("creator"),
                "producer": metadata.get("producer"),
                "title": metadata.get("title"),
            },
        }

    @staticmethod
    def _process_docx(file_content: bytes) -> Dict[str, Any]:
        doc = Document(file_content)

        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        core_props = doc.core_properties

        return {
            "text": text,
            "metadata": {
                "format": "docx",
                "creation_date": core_props.created,
                "modification_date": core_props.modified,
                "author": core_props.author,
                "title": core_props.title,
                "subject": core_props.subject,
            },
        }

    @staticmethod
    def _process_txt(file_content: bytes, filename: str) -> Dict[str, Any]:
        try:
            text = file_content.decode("utf-8")
        except UnicodeDecodeError:
            text = file_content.decode("latin-1")

        return {
            "text": text,
            "metadata": {
                "format": "txt",
                "creation_date": None,
                "modification_date": None,
                "author": None,
                "title": filename,
                "file_size": len(file_content),
            },
        }
