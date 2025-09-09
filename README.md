# Resume Fraud Detection System

## Overview

A production-ready Python-based resume fraud detection system that identifies potential signs of fraudulent or malicious candidates during the hiring process. This system analyzes resumes using multiple detection techniques to flag suspicious patterns, inconsistencies, and red flags.

**Status**: ✅ **Fully Operational** with real API integrations

## Features Implemented

This system implements **3 detection mechanisms** (exceeding the minimum requirement of 2):

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
ABSTRACT_EMAIL_API_KEY=your_email_validation_key_here
ABSTRACT_PHONE_API_KEY=your_phone_validation_key_here  
ABSTRACT_IP_API_KEY=your_ip_geolocation_key_here
WINSTON_AI_API_KEY=your_winston_ai_key_here

# Optional settings:
DEBUG=True
DOCS_ENABLED=True  # Enable API documentation at /docs
```

### 3. Run the System

```bash
# Start the API server
uvicorn app.main:app --reload --port 8000

# Run live demonstration (Recommended)
python demo.py

# Test the system
python test_api.py

# Run comprehensive tests
python run_tests.py
```

### 4. Live Demonstration

**Recommended**: Run the enhanced demonstration to see the system in action:

```bash
python demo.py
```

This provides:
- **Technical Analysis**: Detailed breakdown of weighted algorithm (40%/35%/25%)
- **Comparative Intelligence**: Cross-file pattern analysis and format-based insights
- **API Integration Showcase**: Fallback mechanisms and error handling demonstration
- **Production Readiness**: Performance metrics and reliability analysis

### 5. API Usage

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

The system uses a weighted scoring approach:

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

## Technical Architecture

### Detection Algorithm Design

#### Weighted Risk Scoring
The system uses a mathematically weighted approach to combine multiple fraud indicators:

```
Overall Risk = (Contact × 0.40) + (AI Content × 0.35) + (Document × 0.25)
```

**Rationale**: Contact verification receives the highest weight (40%) as fake contact information is a common fraud indicator. AI content detection (35%) targets generated resume content. Document analysis (25%) identifies template abuse and metadata anomalies.

#### Contact Information Verification
- **Email validation**: Format validation, deliverability checking, disposable email detection
- **Phone verification**: International format validation, carrier identification, geographic consistency
- **IP geolocation**: VPN/Tor detection, threat intelligence, geographic correlation
- **Fallback strategy**: Local validation when APIs unavailable, maintains functionality

#### AI Content Detection
- **Primary**: Winston AI API for professional-grade detection with 300+ character requirements
- **Fallback**: Pattern-based detection using linguistic markers and generic phrase analysis
- **Section analysis**: Resume parsed into summary, experience, skills, education for targeted detection
- **Confidence weighting**: API success rate tracked for proportional confidence calculation

#### Document Authenticity Analysis
- **Metadata forensics**: Creation/modification timestamps, author information, software signatures
- **Template detection**: Generic titles, rapid creation patterns, missing authorship
- **Format analysis**: Suspicious formatting patterns, embedded object analysis

### API Integration Strategy

#### External Service Architecture
- **Abstract API Suite**: Separate keys for email, phone, IP services for granular control
- **Winston AI**: Professional content detection with intelligent text padding for minimum requirements
- **Async processing**: Concurrent API calls with proper timeout and error handling
- **Rate limiting compliance**: Intelligent request pacing to respect API limits

#### Graceful Degradation
- **API failure handling**: Local fallbacks maintain core functionality
- **Confidence adjustment**: Proportional confidence based on actual API success rates
- **Error isolation**: Single API failure doesn't compromise entire analysis

### System Design Decisions

#### Performance Optimization
- **Caching strategy**: MD5-based document hashing for result caching with 30-minute TTL
- **Async pipeline**: Concurrent API calls reduce total processing time
- **Rate limiting**: 5/min for comprehensive analysis, 10/min for individual services

#### Security Implementation
- **File validation**: Size limits (10MB), type restrictions, encoding verification
- **Input sanitization**: Text extraction with encoding fallbacks
- **API key isolation**: Separate configuration for each external service
- **Documentation control**: Production-safe API docs (disabled by default)

### Tool Selection Rationale

#### External API Choices
- **Abstract API Suite**: Fraud detection APIs with coverage for email, phone, and IP verification. Chosen for reliability and separate service granularity.
- **Winston AI**: Professional AI content detection with high accuracy rates. Selected over OpenAI's detector due to better API stability and commercial licensing.
- **FastAPI**: High-performance async framework with automatic OpenAPI documentation. Optimal for API-heavy workloads with concurrent external calls.

#### Architecture Decisions
- **Modular services**: Separate classes for each detection method enable independent testing and maintenance
- **Async processing**: External API calls are I/O bound, async provides significant performance gains
- **Weighted scoring**: Mathematical approach provides consistent, explainable risk assessment
- **Graceful degradation**: System remains functional without external APIs, critical for production reliability

### Known Limitations and Potential Improvements

#### Current Limitations
- **Professional background verification**: No LinkedIn or employment history cross-referencing
- **Digital footprint analysis**: Limited social media presence validation
- **Advanced AI detection**: Relies on Winston AI; no ensemble model approach
- **Document format support**: Limited to PDF, DOCX, TXT (no RTF, ODT, or image-based resumes)
- **Language support**: English-only content analysis and validation
- **Real-time processing**: Synchronous API calls may impact response times under load

#### Potential Improvements
- **Enhanced AI detection**: Combine multiple AI detection services for higher accuracy
- **Professional verification**: Integrate LinkedIn API or employment verification services
- **Advanced document analysis**: OCR support for image-based resumes, deeper metadata forensics
- **Machine learning**: Custom ML models trained on resume fraud patterns
- **Performance optimization**: Redis caching, async queue processing for heavy workloads
- **Security enhancements**: JWT authentication, request signing, audit logging
- **Monitoring**: Comprehensive logging, metrics collection, alerting for production deployment

## Analysis Report

### Implementation Summary

**Detection Methods Implemented**: 3 of 5 (exceeds minimum requirement)
- **Contact Information Verification**: Email validation, phone verification, IP geolocation analysis
- **AI Content Detection**: Winston AI integration with local fallback detection
- **Document Authenticity**: Metadata forensics, template detection, creation timestamp analysis

**Technical Architecture**: Modular FastAPI service with async processing, graceful API degradation, and weighted risk scoring algorithm (40% contact + 35% AI + 25% document).

### Effectiveness Assessment

#### Contact Verification Performance
- **Strengths**: Reliable format validation, geographic consistency checking, disposable email detection
- **Limitations**: Same-IP testing environment limits geolocation accuracy assessment
- **Production Readiness**: Robust fallback mechanisms ensure functionality without external APIs

#### AI Content Detection Analysis
- **Sample Size Limitation**: Analysis based on 2 resume samples (insufficient for statistical significance)
- **Unexpected Results**: AI-generated content scored lower (0.4-5.3%) than legitimate content (13.4%)
- **Possible Explanations**: 
  - Winston AI optimized for academic/creative writing vs professional resumes
  - Modern AI tools produce sophisticated content that passes detection
  - Text extraction differences affect analysis (PDF: 2,756 chars, DOCX: 2,687 chars, TXT: 4,529 chars)
- **System Response**: Correctly reports low confidence when API unavailable, maintains functionality

#### Document Analysis Effectiveness
- **Metadata Forensics**: Successfully identifies missing authorship, rapid creation patterns
- **Template Detection**: Flags generic document titles and suspicious formatting
- **Format Consistency**: Reliable across PDF, DOCX, and TXT formats

### False Positive/Negative Considerations

**Limited Sample Analysis**: With only 2 resumes tested, statistical analysis is insufficient for production deployment decisions.

**Observed Patterns**:
- **Contact verification**: May flag legitimate international phone formats
- **AI detection**: Current tool may not be optimal for resume-specific content
- **Document analysis**: Appropriately conservative, flags recent creation as potential risk

**Risk Mitigation**: Multi-method approach reduces single-point-of-failure risk. Weighted scoring prevents any single method from dominating results.

### Production Deployment Recommendations

#### Immediate Requirements
- **Expanded Testing**: Minimum 100+ diverse resume samples for statistical validation
- **AI Detection Evaluation**: Consider alternative tools or ensemble approaches for resume-specific content
- **Cost Management**: Current Winston AI costs (~1,000 credits per analysis) require budget planning

#### Infrastructure Considerations
- **Database Integration**: Implement audit logging and analytics storage
- **Monitoring**: Add comprehensive logging, metrics collection, and alerting
- **Scaling**: Current async architecture supports horizontal scaling with load balancers

#### Security Enhancements
- **Authentication**: Implement JWT or API key authentication for production access
- **Rate Limiting**: Current limits (5/min comprehensive, 10/min individual) appropriate for initial deployment
- **Input Validation**: Text length caps (5,000 chars) prevent abuse and control costs

### Key Findings

**System Strengths**:
- Robust error handling and graceful API degradation
- Consistent results across file formats (±0.049 variance)
- Production-ready architecture with caching and rate limiting
- Comprehensive test coverage (34 passing tests)

**Areas for Enhancement**:
- AI detection tool evaluation and potential replacement
- Expanded sample testing for statistical validation
- Additional detection methods (professional background verification, digital footprint analysis)

**Assessment Conclusion**: This 3-day implementation provides a functional foundation for resume fraud detection. The unexpected AI detection results reveal the real-world complexity of this problem space and underscore why comprehensive solutions require multiple detection methods, extensive testing, and iterative refinement.

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
