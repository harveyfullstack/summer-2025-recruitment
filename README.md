# Resume Fraud Detection System

## Overview

A production-ready Python-based resume fraud detection system that identifies potential signs of fraudulent or malicious candidates during the hiring process. This system analyzes resumes using multiple detection techniques to flag suspicious patterns, inconsistencies, and red flags.

**Status**: ✅ **Fully Operational** with real API integrations

## Features Implemented

This system implements **3 comprehensive detection mechanisms** (exceeding the minimum requirement of 2):

### 1. Contact Information Verification ✅
- **Email validation** with disposable email detection and quality scoring
- **Phone number validation** with international format support (190+ countries)
- **IP geolocation analysis** with VPN/Tor detection and threat intelligence
- **Geographic consistency** analysis across contact methods
- **Integration**: Abstract API suite with graceful fallback mechanisms

### 2. AI Content Detection ✅
- **Section-by-section analysis** (summary, experience, skills, education)
- **Professional AI detection** using Winston AI (99.98% claimed accuracy)
- **Confidence scoring** with suspicious section identification
- **Fallback detection** using pattern analysis for offline operation
- **Integration**: Winston AI with intelligent text padding for API requirements

### 3. Document Authenticity Analysis ✅
- **Metadata forensics** for PDF and DOCX files
- **Creation/modification timestamp** analysis for authenticity verification
- **Creator software fingerprinting** to detect template abuse
- **File format support**: PDF, DOCX, and TXT with comprehensive validation
- **Security-minded processing** with size limits and encoding validation

## Quick Start

### 1. Environment Setup

```bash
# Ensure Python 3.11+ is installed
python --version  # Should be 3.11+

# Clone the repository
git clone <repository-url>
cd resume-fraud-detector

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# Required for full functionality:
ABSTRACT_EMAIL_API_KEY=your_email_validation_key
ABSTRACT_PHONE_API_KEY=your_phone_validation_key  
ABSTRACT_IP_API_KEY=your_ip_geolocation_key
WINSTON_AI_API_KEY=your_winston_ai_key

# Optional settings:
DEBUG=True
DOCS_ENABLED=True  # Enable API documentation at /docs
```

### 3. Run the System

```bash
# Start the API server
uvicorn app.main:app --reload --port 8000

# Test the system
python test_api.py

# Run comprehensive tests
python run_tests.py
```

### 4. API Usage

The system provides both individual service endpoints and comprehensive fraud detection:

```bash
# Health check
curl http://localhost:8000/health

# Complete fraud detection
curl -X POST "http://localhost:8000/api/v1/detect/resume" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@sample_resume.pdf"

# Individual services
curl -X POST "http://localhost:8000/api/v1/verify/contact" -F "file=@resume.pdf"
curl -X POST "http://localhost:8000/api/v1/analyze/content" -F "file=@resume.pdf"  
curl -X POST "http://localhost:8000/api/v1/examine/document" -F "file=@resume.pdf"
```

## Technical Architecture

### System Design
- **Framework**: FastAPI with async support for high-performance concurrent processing
- **Detection Pipeline**: Modular services with weighted risk scoring algorithm
- **External APIs**: Abstract API suite + Winston AI with intelligent fallback mechanisms
- **Performance**: In-memory caching, rate limiting, and async processing
- **Security**: Input validation, file sanitization, and controlled API documentation

### Weighted Risk Scoring Algorithm

The system uses a sophisticated weighted scoring approach:

```python
# Risk calculation weights
Contact Verification: 40%    # Highest weight - hard to fake
AI Content Detection: 35%    # High weight - detects modern fraud  
Document Authenticity: 25%   # Supporting weight - metadata analysis

# Risk levels
Low Risk:    0.0 - 0.39 (Green)
Medium Risk: 0.40 - 0.69 (Yellow)  
High Risk:   0.70 - 1.0 (Red)
```

### API Endpoints

| Endpoint | Method | Description | Rate Limit |
|----------|--------|-------------|------------|
| `/health` | GET | System health check | None |
| `/api/v1/detect/resume` | POST | Complete fraud analysis | 5/minute |
| `/api/v1/verify/contact` | POST | Contact verification only | 10/minute |
| `/api/v1/analyze/content` | POST | AI content detection only | 10/minute |
| `/api/v1/examine/document` | POST | Document analysis only | 10/minute |
| `/docs` | GET | Interactive API documentation | None* |

*API documentation requires `DOCS_ENABLED=True` in environment

### Response Format

All detection endpoints return structured JSON with confidence scores:

```json
{
  "overall_risk_score": 0.46,
  "risk_level": "medium", 
  "confidence": 0.83,
  "detected_issues": [
    "Invalid email format detected",
    "Suspicious document metadata"
  ],
  "contact_verification": { "risk_score": 0.8, "confidence": 0.9 },
  "ai_content_analysis": { "overall_ai_probability": 0.02, "confidence": 0.85 },
  "document_analysis": { "risk_score": 0.3, "confidence": 0.7 },
  "analysis_timestamp": "2024-01-15T10:30:00Z"
}
```

## Performance & Security

### Performance Features
- **Async Processing**: Concurrent API calls for faster analysis
- **Intelligent Caching**: 30-minute TTL for repeated document analysis
- **Rate Limiting**: Prevents abuse while ensuring fair usage
- **Fallback Mechanisms**: Graceful degradation when external APIs fail

### Security Implementation
- **Input Validation**: File type, size, and encoding verification
- **Sanitization**: Secure file processing with automatic cleanup
- **API Security**: Controlled documentation access and rate limiting
- **Privacy Compliance**: In-memory processing with no persistent storage

### Supported File Formats
- **PDF**: Full metadata extraction and text analysis
- **DOCX**: Microsoft Word document processing
- **TXT**: Plain text resume analysis

## Technology Stack

- **Framework**: FastAPI 0.104.1 with async support
- **Document Processing**: PyMuPDF (PDF), python-docx (DOCX)
- **External APIs**: Abstract API suite, Winston AI
- **Performance**: slowapi (rate limiting), in-memory caching
- **Testing**: pytest with 34 comprehensive tests
- **Security**: File validation, input sanitization

## API Keys Required

To use the full functionality, obtain API keys from:

1. **Abstract API** (3 separate keys needed):
   - Email Validation API: https://app.abstractapi.com/api/email-validation
   - Phone Validation API: https://app.abstractapi.com/api/phone-validation  
   - IP Geolocation API: https://app.abstractapi.com/api/ip-geolocation

2. **Winston AI**:
   - AI Content Detection: https://gowinston.ai/

**Note**: The system works without API keys using intelligent fallback mechanisms, but with reduced accuracy.

## License

This project is developed as a technical assessment for Validia.
