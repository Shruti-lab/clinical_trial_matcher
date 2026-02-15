# Clinical Trial Matcher - AI for Bharat Hackathon
## Presentation Deck Content

---

## SLIDE 1: Problem Statement

**Healthcare & Life Sciences Track**

*"Design an AI solution that improves efficiency, understanding, or support within healthcare or life-sciences ecosystems."*

### The Problem We're Solving:

**Critical Gap in Healthcare Access:**
- Patients with serious/rare diseases often exhaust standard treatment options
- Clinical trials offer cutting-edge treatments but remain largely unknown
- 70% of clinical trials struggle to find eligible participants
- Patients spend months searching for trial information manually
- Language barriers and complex medical terminology create additional obstacles
- No centralized, patient-friendly system exists in India

**Impact:**
- Delayed access to potentially life-saving treatments
- Trials get cancelled due to low enrollment
- Healthcare inequality widens

---

## SLIDE 2: Brief About the Idea

**TrialMatch AI** - Intelligent Clinical Trial Discovery Platform

### What is it?
An AI-powered platform that automatically matches patients with relevant clinical trials in India by analyzing medical records and comparing them against active trials from CTRI (Clinical Trials Registry India).

### How it works:
1. Patient uploads medical reports (prescriptions, test results, diagnosis)
2. AI extracts medical conditions, medications, and patient profile
3. System matches against 10,000+ active clinical trials
4. Provides ranked list of eligible trials with plain language explanations
5. Facilitates connection with trial coordinators

### Target Users:
- Patients with serious/rare diseases
- Caregivers seeking treatment options
- Healthcare providers looking for trial options for patients
- Clinical trial coordinators seeking participants


---

## SLIDE 3: How Different from Existing Solutions?

### Competitive Analysis:

| Feature | TrialMatch AI | ClinicalTrials.gov | Hospital Referrals | Generic Search |
|---------|---------------|-------------------|-------------------|----------------|
| India-focused (CTRI) | ✅ | ❌ | ✅ | ❌ |
| Automated matching | ✅ | ❌ | ❌ | ❌ |
| Medical report analysis | ✅ | ❌ | ❌ | ❌ |
| Plain language explanations | ✅ | ❌ | Varies | ❌ |
| Regional language support | ✅ | ❌ | Limited | ❌ |
| Distance calculation | ✅ | ❌ | N/A | ❌ |
| Eligibility pre-screening | ✅ | Manual | Manual | Manual |

### Key Differentiators:

**1. India-First Approach**
- Integrates with CTRI (Clinical Trials Registry India)
- Understands Indian medical report formats
- Regional language support (Hindi, Tamil, Telugu, etc.)
- Indian location-based trial discovery

**2. Intelligent Automation**
- AI extracts medical information automatically (no manual form filling)
- Smart matching algorithm considers complex eligibility criteria
- Continuous learning from user feedback

**3. Patient-Centric Design**
- Simplifies complex medical jargon
- Explains trial phases, risks, and benefits in simple terms
- Calculates travel distance and logistics
- No medical expertise required to use

**4. Comprehensive Matching**
- Considers medical history, current medications, comorbidities
- Checks exclusion criteria automatically
- Ranks trials by relevance score
- Suggests alternative trials if primary match unavailable


---

## SLIDE 4: How Will It Solve the Problem?

### Solution Approach:

**For Patients:**
- ✅ Reduces trial discovery time from months to minutes
- ✅ Eliminates need to understand complex medical terminology
- ✅ Provides comprehensive information in one place
- ✅ Empowers informed decision-making
- ✅ Increases access to cutting-edge treatments

**For Healthcare System:**
- ✅ Improves clinical trial enrollment rates
- ✅ Accelerates medical research timelines
- ✅ Reduces trial recruitment costs
- ✅ Enables better patient-trial matching
- ✅ Supports evidence-based medicine

**For Trial Coordinators:**
- ✅ Pre-screened, interested candidates
- ✅ Reduced recruitment overhead
- ✅ Better quality matches
- ✅ Faster trial completion

### Impact Metrics (Projected):
- **80% reduction** in trial discovery time
- **3x increase** in trial awareness among eligible patients
- **50% improvement** in trial enrollment rates
- **Reach 100,000+ patients** in first year

---

## SLIDE 5: USP (Unique Selling Proposition)

### 🎯 Core USPs:

**1. AI-Powered Medical Intelligence**
- Advanced NLP extracts conditions from unstructured medical reports
- Handles multiple document formats (PDFs, images, handwritten notes)
- Understands medical abbreviations and Indian medical terminology
- OCR for scanned documents

**2. Smart Eligibility Matching**
- Multi-factor matching algorithm (age, gender, condition, stage, biomarkers)
- Automatic exclusion criteria checking (medications, comorbidities)
- Confidence scoring for each match
- Explains WHY patient is eligible or not

**3. Accessibility First**
- Works in 10+ Indian languages
- Voice input for illiterate/elderly users
- Simple WhatsApp bot interface (no app installation needed)
- Works on low-bandwidth connections

**4. Trust & Transparency**
- Clear disclaimers about limitations
- Uses only verified CTRI data
- Explains trial phases and risks honestly
- Privacy-first: encrypted data, no sharing without consent
- Shows data sources and matching logic

**5. Actionable Insights**
- Direct contact information for trial coordinators
- Travel distance and logistics planning
- Cost estimates (travel, accommodation)
- Timeline expectations
- Preparation checklist for trial enrollment


---

## SLIDE 6: List of Features

### Core Features (MVP):

**1. Medical Report Analysis**
- Upload multiple document formats (PDF, JPG, PNG)
- OCR for scanned documents
- NLP-based information extraction
- Structured data generation

**2. Intelligent Trial Matching**
- Search 10,000+ CTRI trials
- Multi-criteria matching algorithm
- Relevance scoring (0-100%)
- Ranked results with explanations

**3. Patient Dashboard**
- View matched trials
- Save favorites
- Track application status
- Medical profile management

**4. Trial Information Display**
- Plain language trial descriptions
- Phase explanation (Phase I/II/III/IV)
- Eligibility criteria breakdown
- Location and contact details
- Expected duration and commitment

**5. Multilingual Support**
- Interface in 10+ Indian languages
- Medical term translation
- Voice input/output

### Advanced Features (Future):

**6. Smart Notifications**
- New trial alerts based on profile
- Trial status updates
- Application deadline reminders

**7. Community Features**
- Anonymous patient reviews
- Q&A with trial participants
- Support groups

**8. Healthcare Provider Portal**
- Refer patients to trials
- Track referral outcomes
- Access to trial database

**9. Analytics Dashboard**
- Trial enrollment trends
- Success rate tracking
- Geographic coverage analysis

**10. Integration Capabilities**
- Hospital EMR integration
- Telemedicine platform integration
- Insurance verification


---

## SLIDE 7: Process Flow Diagram

### User Journey Flow:

```
┌─────────────────────────────────────────────────────────────────┐
│                        PATIENT JOURNEY                           │
└─────────────────────────────────────────────────────────────────┘

1. ONBOARDING
   ├─> Create Account (Email/Phone)
   ├─> Basic Profile (Age, Gender, Location)
   └─> Consent & Privacy Agreement

2. MEDICAL INFORMATION INPUT
   ├─> Upload Medical Reports
   │   ├─> Prescription
   │   ├─> Lab Results
   │   ├─> Diagnosis Reports
   │   └─> Imaging Reports
   ├─> OR Manual Entry
   └─> Voice Input (Regional Language)

3. AI PROCESSING
   ├─> Document OCR & Parsing
   ├─> Medical Entity Extraction
   │   ├─> Diagnosis/Conditions
   │   ├─> Medications
   │   ├─> Test Results
   │   ├─> Biomarkers
   │   └─> Medical History
   ├─> Data Structuring
   └─> Profile Validation

4. TRIAL MATCHING
   ├─> Query CTRI Database
   ├─> Apply Matching Algorithm
   │   ├─> Primary Condition Match
   │   ├─> Eligibility Criteria Check
   │   ├─> Exclusion Criteria Filter
   │   ├─> Geographic Proximity
   │   └─> Trial Phase Consideration
   ├─> Calculate Relevance Score
   └─> Rank Results

5. RESULTS PRESENTATION
   ├─> Display Matched Trials
   │   ├─> Trial Title & Description
   │   ├─> Eligibility Summary
   │   ├─> Location & Distance
   │   ├─> Contact Information
   │   └─> Match Confidence Score
   ├─> Plain Language Explanation
   └─> Filter & Sort Options

6. ACTION
   ├─> Save Favorite Trials
   ├─> Contact Trial Coordinator
   ├─> Download Trial Information
   ├─> Share with Doctor
   └─> Track Application Status

7. FOLLOW-UP
   ├─> Receive New Trial Alerts
   ├─> Update Medical Profile
   └─> Provide Feedback
```


---

## SLIDE 8: Use Case Diagram

```
                    ┌─────────────────────────────────┐
                    │   TrialMatch AI System          │
                    └─────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
   ┌────▼────┐              ┌─────▼─────┐           ┌──────▼──────┐
   │ Patient │              │  Doctor   │           │   Trial     │
   │         │              │           │           │ Coordinator │
   └────┬────┘              └─────┬─────┘           └──────┬──────┘
        │                         │                         │
        │                         │                         │
   ┌────▼──────────────────────────────────────────────────▼────┐
   │                                                             │
   │  USE CASES:                                                 │
   │                                                             │
   │  Patient:                                                   │
   │  • Upload Medical Reports                                   │
   │  • Search for Trials                                        │
   │  • View Matched Trials                                      │
   │  • Save Favorite Trials                                     │
   │  • Contact Trial Coordinator                                │
   │  • Track Application Status                                 │
   │  • Receive Trial Alerts                                     │
   │  • Update Medical Profile                                   │
   │                                                             │
   │  Doctor:                                                    │
   │  • Refer Patients to Trials                                 │
   │  • Search Trials for Patient                                │
   │  • View Trial Details                                       │
   │  • Download Trial Information                               │
   │  • Track Referral Outcomes                                  │
   │                                                             │
   │  Trial Coordinator:                                         │
   │  • View Matched Candidates                                  │
   │  • Review Patient Profiles                                  │
   │  • Update Trial Information                                 │
   │  • Manage Applications                                      │
   │  • View Analytics                                           │
   │                                                             │
   │  System (Automated):                                        │
   │  • Extract Medical Information                              │
   │  • Match Patients to Trials                                 │
   │  • Calculate Relevance Scores                               │
   │  • Send Notifications                                       │
   │  • Update Trial Database                                    │
   │  • Generate Reports                                         │
   │                                                             │
   └─────────────────────────────────────────────────────────────┘
```


---

## SLIDE 9: Architecture Diagram

```
┌───────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                             │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │   Web App    │  │  Mobile App  │  │ WhatsApp Bot │               │
│  │  (React.js)  │  │ (React Native│  │   (Twilio)   │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                  │                  │                        │
│         └──────────────────┼──────────────────┘                        │
│                            │                                           │
└────────────────────────────┼───────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   AWS API       │
                    │   Gateway       │
                    └────────┬────────┘
                             │
┌────────────────────────────┼───────────────────────────────────────────┐
│                      APPLICATION LAYER                                 │
├────────────────────────────┼───────────────────────────────────────────┤
│                            │                                           │
│  ┌─────────────────────────▼──────────────────────────┐               │
│  │         AWS Lambda Functions (Python)               │               │
│  ├─────────────────────────────────────────────────────┤               │
│  │                                                      │               │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │               │
│  │  │   Auth       │  │   Upload     │  │  Search  │ │               │
│  │  │   Service    │  │   Service    │  │  Service │ │               │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │               │
│  │                                                      │               │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │               │
│  │  │   Matching   │  │ Notification │  │Analytics │ │               │
│  │  │   Service    │  │   Service    │  │ Service  │ │               │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │               │
│  └──────────────────────────────────────────────────────┘              │
│                            │                                           │
└────────────────────────────┼───────────────────────────────────────────┘
                             │
┌────────────────────────────┼───────────────────────────────────────────┐
│                         AI/ML LAYER                                    │
├────────────────────────────┼───────────────────────────────────────────┤
│                            │                                           │
│  ┌─────────────────────────▼──────────────────────────┐               │
│  │         AWS AI/ML Services                          │               │
│  ├─────────────────────────────────────────────────────┤               │
│  │                                                      │               │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │               │
│  │  │   Amazon     │  │   Amazon     │  │ Amazon   │ │               │
│  │  │   Textract   │  │ Comprehend   │  │ Translate│ │               │
│  │  │    (OCR)     │  │Medical (NER) │  │          │ │               │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │               │
│  │                                                      │               │
│  │  ┌──────────────┐  ┌──────────────┐                │               │
│  │  │  SageMaker   │  │   Amazon     │                │               │
│  │  │  (Custom ML) │  │   Bedrock    │                │               │
│  │  │              │  │   (LLM)      │                │               │
│  │  └──────────────┘  └──────────────┘                │               │
│  └──────────────────────────────────────────────────────┘              │
│                            │                                           │
└────────────────────────────┼───────────────────────────────────────────┘
                             │
┌────────────────────────────┼───────────────────────────────────────────┐
│                         DATA LAYER                                     │
├────────────────────────────┼───────────────────────────────────────────┤
│                            │                                           │
│  ┌──────────────┐  ┌───────▼──────┐  ┌──────────────┐               │
│  │   Amazon S3  │  │   Amazon     │  │  Amazon      │               │
│  │  (Documents) │  │   DynamoDB   │  │  RDS         │               │
│  │              │  │  (NoSQL)     │  │  (PostgreSQL)│               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │  OpenSearch  │  │   ElastiCache│  │   AWS        │               │
│  │  (Search)    │  │   (Redis)    │  │   Secrets    │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL INTEGRATIONS                               │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │     CTRI     │  │   SMS/Email  │  │   Payment    │               │
│  │   Database   │  │   (AWS SNS)  │  │   Gateway    │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```


---

## SLIDE 10: Technologies to be Used

### Frontend Technologies:

**Web Application:**
- **React.js** - Modern UI framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Responsive styling
- **Redux Toolkit** - State management
- **React Query** - Data fetching & caching
- **Axios** - HTTP client

**Mobile Application:**
- **React Native** - Cross-platform mobile development
- **Expo** - Development tooling

### Backend Technologies:

**Core Backend:**
- **Python 3.11+** - Primary language
- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM for database
- **Alembic** - Database migrations
- **Celery** - Async task queue
- **Redis** - Caching & message broker

**AI/ML Stack:**
- **spaCy** - NLP processing
- **Transformers (HuggingFace)** - Pre-trained models
- **scikit-learn** - ML algorithms
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **PyTorch** - Deep learning (if needed)

**Document Processing:**
- **PyPDF2 / pdfplumber** - PDF parsing
- **Pillow** - Image processing
- **python-docx** - Word document handling


### AWS Services:

**Compute:**
- **AWS Lambda** - Serverless functions
- **AWS API Gateway** - REST API management
- **AWS Fargate** - Container orchestration (for heavy ML tasks)

**AI/ML Services:**
- **Amazon Textract** - OCR for document extraction
- **Amazon Comprehend Medical** - Medical NER & entity extraction
- **Amazon Translate** - Multi-language support
- **Amazon Bedrock** - LLM for explanations (Claude/Titan)
- **Amazon SageMaker** - Custom ML model training & deployment

**Storage:**
- **Amazon S3** - Document storage
- **Amazon RDS (PostgreSQL)** - Relational database
- **Amazon DynamoDB** - NoSQL for user sessions
- **Amazon ElastiCache (Redis)** - Caching layer

**Search & Analytics:**
- **Amazon OpenSearch** - Full-text search for trials
- **Amazon CloudWatch** - Monitoring & logging
- **AWS X-Ray** - Distributed tracing

**Security & Identity:**
- **AWS Cognito** - User authentication
- **AWS Secrets Manager** - Credential management
- **AWS KMS** - Encryption key management
- **AWS WAF** - Web application firewall

**Messaging & Notifications:**
- **Amazon SNS** - Push notifications
- **Amazon SES** - Email service
- **Amazon EventBridge** - Event-driven architecture

**DevOps:**
- **AWS CodePipeline** - CI/CD
- **AWS CodeBuild** - Build automation
- **AWS CloudFormation** - Infrastructure as Code
- **Amazon ECR** - Container registry

### Additional Tools:

**Development:**
- **Docker** - Containerization
- **Git/GitHub** - Version control
- **Poetry** - Python dependency management
- **pytest** - Testing framework
- **Black/Ruff** - Code formatting & linting

**Monitoring:**
- **Sentry** - Error tracking
- **Grafana** - Metrics visualization
- **Prometheus** - Metrics collection

**External APIs:**
- **Twilio** - WhatsApp bot integration
- **Google Maps API** - Distance calculation
- **CTRI Web Scraping** - Trial data collection


---

## SLIDE 11: Estimated Implementation Cost

### Cost Breakdown (Monthly - AWS India Region)

#### Phase 1: MVP Development (Months 1-3)
**Estimated Users: 1,000 active users/month**

| Service | Usage | Monthly Cost (USD) |
|---------|-------|-------------------|
| **Compute** | | |
| AWS Lambda | 5M requests, 512MB, 3s avg | $25 |
| API Gateway | 5M requests | $18 |
| **AI/ML Services** | | |
| Amazon Textract | 10,000 pages | $150 |
| Comprehend Medical | 1M characters | $120 |
| Amazon Translate | 500K characters | $8 |
| Amazon Bedrock (Claude) | 100K tokens | $30 |
| **Storage** | | |
| S3 (Documents) | 100GB storage, 50GB transfer | $15 |
| RDS PostgreSQL (db.t3.medium) | Single AZ | $60 |
| DynamoDB | 5GB storage, on-demand | $10 |
| ElastiCache (cache.t3.micro) | Redis | $15 |
| **Search** | | |
| OpenSearch (t3.small) | Single node | $40 |
| **Security & Auth** | | |
| AWS Cognito | 1,000 MAU | Free |
| Secrets Manager | 10 secrets | $4 |
| **Monitoring** | | |
| CloudWatch | Logs & metrics | $20 |
| **Networking** | | |
| Data Transfer | 100GB outbound | $9 |
| **External Services** | | |
| Twilio (WhatsApp) | 5,000 messages | $50 |
| Domain & SSL | Route53, ACM | $5 |
| **TOTAL PHASE 1** | | **~$579/month** |

#### Phase 2: Growth (Months 4-12)
**Estimated Users: 10,000 active users/month**

| Service | Usage | Monthly Cost (USD) |
|---------|-------|-------------------|
| **Compute** | | |
| AWS Lambda | 50M requests | $240 |
| API Gateway | 50M requests | $175 |
| **AI/ML Services** | | |
| Amazon Textract | 100,000 pages | $1,500 |
| Comprehend Medical | 10M characters | $1,200 |
| Amazon Translate | 5M characters | $75 |
| Amazon Bedrock | 1M tokens | $300 |
| SageMaker (ml.t3.medium) | Custom models | $150 |
| **Storage** | | |
| S3 | 1TB storage, 500GB transfer | $85 |
| RDS (db.r5.large) | Multi-AZ | $350 |
| DynamoDB | 50GB storage | $50 |
| ElastiCache (cache.r5.large) | | $120 |
| **Search** | | |
| OpenSearch (r5.large) | 3-node cluster | $450 |
| **Security & Auth** | | |
| AWS Cognito | 10,000 MAU | $275 |
| **Monitoring** | | |
| CloudWatch + X-Ray | Enhanced | $100 |
| **Networking** | | |
| Data Transfer | 1TB outbound | $90 |
| **External Services** | | |
| Twilio | 50,000 messages | $500 |
| **TOTAL PHASE 2** | | **~$5,660/month** |

