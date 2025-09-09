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

### Deliverables

1. **Working Code**
   - Complete Python implementation
   - Requirements.txt or poetry.lock file
   - Configuration files for API keys and settings

2. **Setup Instructions**
   - Clear installation and configuration steps
   - Example usage commands
   - Sample input/output demonstrations

3. **Documentation**
   - Technical architecture overview
   - Detailed explanation of detection algorithms
   - Rationale for chosen tools and approaches
   - Known limitations and potential improvements

4. **Analysis Report**
   - Summary of implemented features
   - Effectiveness assessment of each detection method
   - Discussion of false positive/negative considerations
   - Recommendations for production deployment

## Evaluation Criteria

### Code Quality (30%)
- Clean, readable, and well-structured code
- Proper error handling and edge case management
- Appropriate use of design patterns and best practices
- Comprehensive testing approach

### Technical Implementation (25%)
- Effectiveness of fraud detection algorithms
- Integration quality with external services
- Performance considerations and optimization
- Security best practices

### Innovation & Approach (25%)
- Creative problem-solving techniques
- Novel detection methods or combinations
- Thoughtful selection of tools and APIs
- Scalability considerations

### Documentation & Usability (20%)
- Clear setup and usage instructions
- Thorough technical documentation
- Quality of analysis and recommendations
- Practical applicability

## Constraints & Guidelines

- **Time Limit**: 3 days from project start
- **External Dependencies**: Any APIs, libraries, or tools are permitted
- **Privacy & Ethics**: Ensure compliance with data protection regulations
- **Honor System**: Work independently; collaboration is not permitted


## Getting Started

1. Fork or download this repository
2. Set up your development environment
3. Review the requirements and plan your approach
4. Begin implementation with your chosen detection methods
5. Document your process and findings as you work

## Questions?

I'm more than happy to help! Feel free to reach out to Paul at paul@validia.ai with any questions or clarifications needed.

## Additional Notes

- Consider rate limiting when working with external APIs
- Implement appropriate caching mechanisms for efficiency
- Think about how this system would scale in production
- Balance detection accuracy with processing speed
- Consider the user experience for both legitimate and flagged candidates

---

**Important**: This challenge assesses both your technical skills and your ability to think like a security-minded engineer. Focus on creating a solution that would be valuable in a real-world hiring scenario.
