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
            if isinstance(creation_date, str):
                try:
                    creation_date = datetime.fromisoformat(
                        creation_date.replace("Z", "+00:00")
                    )
                except:
                    creation_date = None

            if isinstance(modification_date, str):
                try:
                    modification_date = datetime.fromisoformat(
                        modification_date.replace("Z", "+00:00")
                    )
                except:
                    modification_date = None

            if creation_date and modification_date:
                time_diff = abs((modification_date - creation_date).total_seconds())

                if time_diff < 60:
                    suspicious_patterns.append(
                        "Document created and modified within 1 minute"
                    )
                    risk_score += 0.2

                authenticity_indicators["timestamp_consistency"] = time_diff > 60

        creator_software = metadata.get("creator") or metadata.get("producer")
        if creator_software:
            suspicious_creators = [
                "online converter",
                "free pdf",
                "template",
                "generator",
            ]

            creator_lower = creator_software.lower()
            for suspicious in suspicious_creators:
                if suspicious in creator_lower:
                    suspicious_patterns.append(
                        f"Suspicious creator software: {creator_software}"
                    )
                    risk_score += 0.3
                    break

            authenticity_indicators["creator_software"] = creator_software

        author = metadata.get("author")
        if not author or author.strip() == "":
            suspicious_patterns.append("Missing or empty author information")
            risk_score += 0.1

        authenticity_indicators["has_author"] = bool(author and author.strip())

        title = metadata.get("title")
        if title:
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
                risk_score += 0.1

        return {
            "authenticity_indicators": authenticity_indicators,
            "suspicious_patterns": suspicious_patterns,
            "risk_score": min(risk_score, 1.0),
            "confidence": 0.7,
        }
