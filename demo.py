import asyncio
import json
import os
import glob
from fastapi.testclient import TestClient
from app.main import app


def demonstrate_fraud_detection():
    print("🔍 Resume Fraud Detection System - Live Demonstration")
    print("=" * 60)

    client = TestClient(app)

    sample_files = []
    for ext in ["*.pdf", "*.docx", "*.txt"]:
        sample_files.extend(glob.glob(f"samples/{ext}"))

    sample_files.sort()

    for file_path in sample_files:
        print(f"\n📄 Analyzing: {file_path}")
        print("-" * 40)

        try:
            with open(file_path, "rb") as f:
                files = {
                    "file": (file_path.split("/")[-1], f, "application/octet-stream")
                }
                response = client.post("/api/v1/detect/resume", files=files)

            if response.status_code == 200:
                data = response.json()

                risk_score = data.get("overall_risk_score", 0)
                risk_level = data.get("risk_level", "unknown")
                confidence = data.get("confidence", 0)
                issues = data.get("detected_issues", [])

                print(f"🎯 Overall Risk Score: {risk_score:.3f}")
                print(f"⚠️  Risk Level: {risk_level.upper()}")
                print(f"🔒 Confidence: {confidence:.3f}")
                print(f"🚨 Issues Detected: {len(issues)}")

                if issues:
                    for issue in issues[:3]:
                        print(f"   • {issue}")

                contact = data.get("contact_verification", {})
                ai = data.get("ai_content_analysis", {})
                document = data.get("document_analysis", {})

                print(f"\n📧 Contact Risk: {contact.get('risk_score', 0):.3f}")
                print(f"🤖 AI Probability: {ai.get('overall_ai_probability', 0):.3f}")
                print(f"📋 Document Risk: {document.get('risk_score', 0):.3f}")

            else:
                print(f"❌ Error: {response.status_code}")

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

    print(f"\n✅ Demonstration complete!")
    print("🌐 API Documentation: http://localhost:8000/docs")


if __name__ == "__main__":
    demonstrate_fraud_detection()
