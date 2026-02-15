# Clinical Trial Matcher - Design Document

## 1. System Architecture

### 1.1 Architecture Pattern
**Serverless Microservices Architecture** using AWS services for scalability and cost-efficiency.

### 1.2 High-Level Components

```
┌─────────────┐
│   Client    │ (React Web App)
└──────┬──────┘
       │
┌──────▼──────┐
│ API Gateway │
└──────┬──────┘
       │
┌──────▼──────────────────────────┐
│   Lambda Functions (Python)     │
│  - Auth Service                  │
│  - Upload Service                │
│  - Matching Service              │
│  - Search Service                │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────────────┐
│   AWS AI/ML Services             │
│  - Textract (OCR)                │
│  - Comprehend Medical (NER)      │
│  - Translate (i18n)              │
│  - Bedrock (Explanations)        │
└──────────────────────────────────┘
       │
┌──────▼──────────────────────────┐
│   Data Layer                     │
│  - RDS PostgreSQL (User/Trials) │
│  - S3 (Documents)                │
│  - OpenSearch (Trial Search)     │
│  - Redis (Cache)                 │
└──────────────────────────────────┘
```

## 2. Component Design

### 2.1 Frontend (React Web App)

**Technology Stack:**
- React 18 + TypeScript
- Tailwind CSS for styling
- React Query for data fetching
- React Router for navigation
- Zustand for state management

**Key Pages:**
1. **Landing Page** - Hero, features, CTA
2. **Auth Pages** - Login, signup, OTP verification
3. **Upload Page** - Drag-drop document upload
4. **Profile Page** - View extracted medical info
5. **Results Page** - Matched trials with filters
6. **Trial Detail Page** - Comprehensive trial information

**Component Structure:**
```
src/
├── components/
│   ├── DocumentUpload/
│   ├── TrialCard/
│   ├── MatchScore/
│   └── LanguageSelector/
├── pages/
│   ├── Home/
│   ├── Upload/
│   ├── Results/
│   └── TrialDetail/
├── services/
│   └── api.ts
└── utils/
    └── i18n.ts
```

### 2.2 Backend Services (AWS Lambda)

#### 2.2.1 Auth Service
**Endpoint:** `/auth/*`  
**Functions:**
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/verify-otp` - OTP verification
- `GET /auth/me` - Get current user

**Technology:**
- AWS Cognito for user management
- JWT tokens for session
- bcrypt for password hashing

#### 2.2.2 Upload Service
**Endpoint:** `/upload/*`  
**Functions:**
- `POST /upload/document` - Upload medical document
- `GET /upload/status/{id}` - Check processing status
- `GET /upload/documents` - List user documents

**Flow:**
1. Generate pre-signed S3 URL
2. Client uploads directly to S3
3. S3 trigger invokes processing Lambda
4. Extract text using Textract
5. Store metadata in RDS

#### 2.2.3 Processing Service
**Trigger:** S3 event on document upload  
**Functions:**
- OCR using Amazon Textract
- Medical NER using Comprehend Medical
- Extract: conditions, medications, demographics
- Store structured data in RDS
- Update user profile

**Key Logic:**
```python
def process_document(s3_key):
    # 1. OCR
    text = textract.detect_document_text(s3_key)
    
    # 2. Medical NER
    entities = comprehend_medical.detect_entities_v2(text)
    
    # 3. Structure data
    profile = {
        'conditions': extract_conditions(entities),
        'medications': extract_medications(entities),
        'demographics': extract_demographics(entities)
    }
    
    # 4. Save to database
    save_medical_profile(user_id, profile)
```

#### 2.2.4 Matching Service
**Endpoint:** `/match/*`  
**Functions:**
- `POST /match/find-trials` - Find matching trials
- `GET /match/trial/{id}` - Get trial details
- `POST /match/save-favorite` - Save trial to favorites

**Matching Algorithm:**
```python
def calculate_match_score(patient_profile, trial):
    score = 0
    weights = {
        'condition_match': 0.4,
        'eligibility': 0.3,
        'exclusion': 0.2,
        'location': 0.1
    }
    
    # Condition matching
    if patient_condition in trial.conditions:
        score += weights['condition_match'] * 100
    
    # Age/gender eligibility
    if meets_eligibility(patient_profile, trial):
        score += weights['eligibility'] * 100
    
    # Exclusion criteria
    if not has_exclusions(patient_profile, trial):
        score += weights['exclusion'] * 100
    else:
        return 0  # Hard exclusion
    
    # Location proximity
    distance = calculate_distance(patient_location, trial_location)
    location_score = max(0, 100 - (distance / 10))
    score += weights['location'] * location_score
    
    return min(100, score)
```

#### 2.2.5 Search Service
**Endpoint:** `/search/*`  
**Functions:**
- `GET /search/trials` - Search trials with filters
- `GET /search/autocomplete` - Condition autocomplete

**Technology:**
- Amazon OpenSearch for full-text search
- Filters: condition, location, phase, status
- Pagination support

### 2.3 Data Models

#### 2.3.1 User Model
```python
class User:
    id: UUID
    email: str
    phone: str
    password_hash: str
    preferred_language: str
    created_at: datetime
    updated_at: datetime
```

#### 2.3.2 Medical Profile Model
```python
class MedicalProfile:
    id: UUID
    user_id: UUID (FK)
    age: int
    gender: str
    conditions: List[str]  # JSON array
    medications: List[str]  # JSON array
    test_results: Dict  # JSON object
    medical_history: List[str]
    location: str
    created_at: datetime
    updated_at: datetime
```

#### 2.3.3 Document Model
```python
class Document:
    id: UUID
    user_id: UUID (FK)
    s3_key: str
    file_name: str
    file_type: str
    processing_status: str  # pending, processing, completed, failed
    extracted_text: str
    created_at: datetime
```

#### 2.3.4 Clinical Trial Model
```python
class ClinicalTrial:
    id: UUID
    ctri_id: str  # CTRI registry number
    title: str
    condition: str
    phase: str  # I, II, III, IV
    status: str  # recruiting, active, completed
    eligibility_criteria: Dict  # JSON
    exclusion_criteria: List[str]
    location: str
    latitude: float
    longitude: float
    sponsor: str
    contact_name: str
    contact_email: str
    contact_phone: str
    start_date: date
    estimated_completion: date
    description: str
    created_at: datetime
    updated_at: datetime
```

#### 2.3.5 Match Model
```python
class Match:
    id: UUID
    user_id: UUID (FK)
    trial_id: UUID (FK)
    match_score: float  # 0-100
    match_explanation: str
    is_favorite: bool
    status: str  # viewed, contacted, enrolled
    created_at: datetime
```

## 3. API Design

### 3.1 REST API Endpoints

**Base URL:** `https://api.trialmatch.ai/v1`

#### Authentication
```
POST   /auth/register          - Register new user
POST   /auth/login             - Login user
POST   /auth/verify-otp        - Verify OTP
GET    /auth/me                - Get current user
POST   /auth/logout            - Logout user
```

#### Documents
```
POST   /documents              - Upload document
GET    /documents              - List user documents
GET    /documents/{id}         - Get document details
DELETE /documents/{id}         - Delete document
GET    /documents/{id}/status  - Get processing status
```

#### Profile
```
GET    /profile                - Get medical profile
PUT    /profile                - Update profile
GET    /profile/summary        - Get profile summary
```

#### Trials
```
GET    /trials                 - Search trials (with filters)
GET    /trials/{id}            - Get trial details
POST   /trials/{id}/contact    - Contact trial coordinator
GET    /trials/nearby          - Get trials near location
```

#### Matching
```
POST   /match                  - Find matching trials
GET    /match/results          - Get match results
POST   /match/favorite         - Save favorite trial
GET    /match/favorites        - List favorite trials
DELETE /match/favorite/{id}    - Remove favorite
```

### 3.2 Request/Response Examples

**POST /match - Find Matching Trials**

Request:
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "filters": {
    "max_distance_km": 100,
    "phases": ["II", "III"],
    "status": ["recruiting"]
  }
}
```

Response:
```json
{
  "matches": [
    {
      "trial_id": "789e4567-e89b-12d3-a456-426614174111",
      "match_score": 92,
      "trial": {
        "title": "Phase III Study of Drug X for Breast Cancer",
        "condition": "Breast Cancer (Stage II)",
        "phase": "III",
        "location": "AIIMS, New Delhi",
        "distance_km": 15,
        "contact": {
          "name": "Dr. [Name]",
          "email": "[email]",
          "phone": "[phone]"
        }
      },
      "match_explanation": "Strong match based on your Stage II breast cancer diagnosis. You meet all eligibility criteria including age (45) and ER+/PR+ status.",
      "eligibility_summary": {
        "met": ["Age 18-65", "Stage II breast cancer", "ER+/PR+ status"],
        "not_met": []
      }
    }
  ],
  "total_matches": 5,
  "processing_time_ms": 234
}
```

## 4. AI/ML Pipeline

### 4.1 Document Processing Pipeline

```
Document Upload
    ↓
Amazon Textract (OCR)
    ↓
Text Extraction
    ↓
Amazon Comprehend Medical (NER)
    ↓
Entity Extraction
    ↓
Custom Post-Processing
    ↓
Structured Medical Profile
```

### 4.2 Medical Entity Extraction

**Entities to Extract:**
- **Conditions:** Diseases, diagnoses, symptoms
- **Medications:** Drug names, dosages
- **Test Results:** Lab values, biomarkers
- **Procedures:** Surgeries, treatments
- **Demographics:** Age, gender

**Post-Processing:**
- Normalize medical terms (e.g., "BP" → "Blood Pressure")
- Map to ICD-10 codes
- Resolve abbreviations
- Extract numerical values

### 4.3 Matching Algorithm Details

**Step 1: Primary Condition Matching**
- Exact match: 100 points
- Synonym match: 80 points
- Related condition: 60 points
- No match: 0 points

**Step 2: Eligibility Check**
- Age range: Pass/Fail
- Gender: Pass/Fail
- Disease stage: Pass/Fail

**Step 3: Exclusion Criteria**
- Check medications against exclusions
- Check comorbidities
- Any exclusion = 0 score (hard fail)

**Step 4: Location Scoring**
- <50km: 100 points
- 50-100km: 75 points
- 100-200km: 50 points
- >200km: 25 points

**Final Score:** Weighted average of all components

### 4.4 Explanation Generation

Use Amazon Bedrock (Claude) to generate plain language explanations:

```python
def generate_explanation(patient, trial, score):
    prompt = f"""
    Explain why this clinical trial matches the patient:
    
    Patient: {patient.age}yo {patient.gender} with {patient.conditions}
    Trial: {trial.title} for {trial.condition}
    Match Score: {score}%
    
    Provide a 2-3 sentence explanation in simple language.
    """
    
    response = bedrock.invoke_model(
        model='anthropic.claude-v2',
        prompt=prompt
    )
    
    return response.text
```

## 5. Security Design

### 5.1 Authentication & Authorization
- AWS Cognito for user management
- JWT tokens with 24-hour expiry
- Refresh tokens for extended sessions
- Role-based access control (patient, admin)

### 5.2 Data Encryption
- **In Transit:** TLS 1.3 for all API calls
- **At Rest:** 
  - S3: AES-256 encryption
  - RDS: Encryption enabled
  - Secrets Manager for credentials

### 5.3 Privacy Measures
- Medical data anonymized in logs
- PII masked in error messages
- Data retention: 2 years, then auto-delete
- User can request data deletion (GDPR compliance)

### 5.4 API Security
- Rate limiting: 100 requests/minute per user
- AWS WAF for DDoS protection
- Input validation and sanitization
- CORS configuration

## 6. Deployment Strategy

### 6.1 Infrastructure as Code
- AWS CloudFormation templates
- Separate stacks for dev, staging, prod
- Automated deployment via AWS CodePipeline

### 6.2 CI/CD Pipeline
```
GitHub Push
    ↓
AWS CodeBuild (Run Tests)
    ↓
Build Docker Images
    ↓
Push to ECR
    ↓
Deploy to Lambda (via CloudFormation)
    ↓
Run Integration Tests
    ↓
Production Deployment (Manual Approval)
```

### 6.3 Monitoring & Logging
- CloudWatch for logs and metrics
- X-Ray for distributed tracing
- Custom dashboards for key metrics
- Alerts for errors and performance issues

## 7. Testing Strategy

### 7.1 Unit Tests
- pytest for Python backend
- Jest for React frontend
- Target: >80% code coverage

### 7.2 Integration Tests
- Test API endpoints end-to-end
- Mock AWS services using moto
- Test document processing pipeline

### 7.3 User Acceptance Testing
- Test with 10 synthetic patient profiles
- Verify match accuracy
- Test multilingual support
- Performance testing (load testing with 100 concurrent users)

## 8. Scalability Considerations

### 8.1 Horizontal Scaling
- Lambda auto-scales based on requests
- RDS read replicas for read-heavy operations
- OpenSearch cluster can scale nodes

### 8.2 Caching Strategy
- Redis cache for:
  - Trial search results (TTL: 1 hour)
  - User profiles (TTL: 30 minutes)
  - Frequently accessed trials (TTL: 24 hours)

### 8.3 Database Optimization
- Indexes on frequently queried fields
- Partitioning for large tables
- Connection pooling

## 9. Future Enhancements

### 9.1 Phase 2 Features
- Mobile app (React Native)
- WhatsApp bot integration
- Doctor portal
- Real-time notifications

### 9.2 Advanced AI Features
- Predictive trial success probability
- Personalized trial recommendations
- Automated follow-up scheduling
- Natural language query interface

### 9.3 Integrations
- Hospital EMR systems
- Insurance verification APIs
- Telemedicine platforms
- Payment gateways

## 10. Correctness Properties

### 10.1 Matching Accuracy
**Property 1:** All returned trials must meet minimum eligibility criteria (age, gender)  
**Property 2:** Trials with exclusion criteria violations must have score = 0  
**Property 3:** Match scores must be between 0-100 and deterministic

### 10.2 Data Integrity
**Property 4:** Uploaded documents must be retrievable and unchanged  
**Property 5:** Medical profile updates must be atomic (all or nothing)  
**Property 6:** User data must be isolated (no cross-user data leakage)

### 10.3 Performance
**Property 7:** Search response time must be <5 seconds for 95th percentile  
**Property 8:** Document processing must complete within 60 seconds  
**Property 9:** System must handle 100 concurrent users without degradation
