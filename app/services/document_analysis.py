from typing import Dict, Any
from datetime import datetime


class DocumentAnalysisService:
    @staticmethod
    def analyze_document_authenticity(metadata: Dict[str, Any]) -> Dict[str, Any]:
        authenticity_indicators = {}
        suspicious_patterns = []
        risk_score = 0.0

        creation_date = metadata.get("creation_date")
        modification_date = metadata.get("modification_date")

        if creation_date and modification_date:
            creation_date = DocumentAnalysisService._parse_date(creation_date)
            modification_date = DocumentAnalysisService._parse_date(modification_date)

            if creation_date and modification_date:
                time_diff = abs((modification_date - creation_date).total_seconds())

                if time_diff < 60:
                    suspicious_patterns.append(
                        "Document created and modified within 1 minute"
                    )
                    risk_score += 0.3

                authenticity_indicators["timestamp_consistency"] = time_diff > 60

        creator_software = metadata.get("creator") or metadata.get("producer")
        if creator_software:
            suspicious_creators = [
                "online converter",
                "free pdf",
                "template",
                "generator",
                "python-docx",
                "mozilla/",
                "chrome/",
                "webkit",
                "headlesschrome",
            ]

            creator_lower = creator_software.lower()
            for suspicious in suspicious_creators:
                if suspicious in creator_lower:
                    suspicious_patterns.append(
                        f"Suspicious creator software: {creator_software}"
                    )
                    risk_score += 0.4
                    break

            authenticity_indicators["creator_software"] = creator_software

        document_format = metadata.get("format", "")
        author = metadata.get("author")

        if document_format != "txt":
            if not author or author.strip() == "":
                suspicious_patterns.append("Missing or empty author information")
                risk_score += 0.2

        authenticity_indicators["has_author"] = bool(author and author.strip())

        title = metadata.get("title")
        if title and document_format != "txt":
            generic_titles = [
                "resume",
                "cv",
                "curriculum vitae",
                "document",
                "untitled",
            ]

            title_lower = title.lower().strip()
            if any(generic in title_lower for generic in generic_titles):
                suspicious_patterns.append("Generic document title")
                risk_score += 0.15

        return {
            "authenticity_indicators": authenticity_indicators,
            "suspicious_patterns": suspicious_patterns,
            "risk_score": min(risk_score, 1.0),
            "confidence": 0.7,
        }

    @staticmethod
    def _parse_date(date_value):
        if not date_value:
            return None

        if isinstance(date_value, datetime):
            return date_value

        if isinstance(date_value, str):
            try:
                if date_value.startswith("D:"):
                    date_str = date_value[2:]
                    if "+" in date_str:
                        date_str = date_str.split("+")[0]
                    elif "'" in date_str:
                        date_str = date_str.split("'")[0]

                    if len(date_str) >= 14:
                        return datetime.strptime(date_str[:14], "%Y%m%d%H%M%S")

                return datetime.fromisoformat(date_value.replace("Z", "+00:00"))
            except:
                return None

        return None
