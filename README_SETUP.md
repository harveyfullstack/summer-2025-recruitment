# Resume Fraud Detection System

## Quick Start

### 1. Setup Environment
```bash
# Set Python version
pyenv local 3.11.2

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys (optional for basic testing)
# ABSTRACT_API_KEY=your_key_here
# WINSTON_AI_API_KEY=your_key_here
```

### 3. Run the API
```bash
# Start the server
uvicorn app.main:app --reload --port 8000

# Test basic functionality
python test_api.py
```

### 4. API Endpoints

- `GET /health` - Health check
- `POST /api/v1/detect/resume` - Full fraud detection
- `POST /api/v1/verify/contact` - Contact verification only
- `POST /api/v1/analyze/content` - AI content detection only
- `POST /api/v1/examine/document` - Document analysis only

### 5. Testing
Upload PDF or DOCX files to any endpoint for analysis.

## Features Implemented

**Contact Information Verification**
- Email validation and disposable email detection
- Phone number validation with geographic consistency
- Abstract API integration (with fallback)

**AI Content Detection**
- Section-by-section analysis (summary, experience, skills, education)
- Winston AI integration (with basic fallback detection)
- Confidence scoring and suspicious section identification

**Document Authenticity Analysis**
- PDF and DOCX metadata extraction
- Creation/modification timestamp analysis
- Creator software fingerprint detection
- Template pattern recognition

**Weighted Risk Scoring**
- Configurable weights (Contact: 40%, AI: 35%, Document: 25%)
- Risk level classification (Low/Medium/High)
- Comprehensive issue detection and reporting