# Clinical Trial Matcher - Requirements Document

## 1. Project Overview

**Project Name:** TrialMatch AI  
**Problem Statement:** Healthcare & Life Sciences - AI solution that improves efficiency and support within healthcare ecosystems  
**Target:** AI for Bharat Hackathon

### Vision
An AI-powered platform that automatically matches patients with relevant clinical trials in India by analyzing medical records and comparing them against active trials from CTRI (Clinical Trials Registry India).

### Goals
- Reduce trial discovery time from months to minutes
- Increase trial enrollment rates by 50%
- Make clinical trials accessible to non-technical users
- Support 10+ Indian regional languages

## 2. User Stories

### 2.1 Patient User Stories

**US-1: Medical Report Upload**  
As a patient, I want to upload my medical reports (PDF/images) so that the system can analyze my condition without manual data entry.

**Acceptance Criteria:**
- Support PDF, JPG, PNG formats
- Maximum file size: 10MB per document
- Multiple documents can be uploaded
- Progress indicator during upload
- Success/error feedback

**US-2: View Matched Trials**  
As a patient, I want to see clinical trials that match my medical condition so that I can explore treatment options.

**Acceptance Criteria:**
- Display trials ranked by relevance (0-100% match score)
- Show trial title, location, phase, and eligibility summary
- Calculate and display distance from patient location
- Provide contact information for trial coordinator
- Explain why the trial is a match

**US-3: Understand Trial Information**  
As a patient, I want trial information in simple language so that I can make informed decisions without medical expertise.

**Acceptance Criteria:**
- Plain language descriptions (no medical jargon)
- Explain trial phases (I, II, III, IV) in simple terms
- Break down eligibility criteria into understandable points
- Show expected time commitment
- Display potential risks and benefits clearly

**US-4: Multilingual Support**  
As a non-English speaking patient, I want to use the platform in my regional language so that I can understand the information.

**Acceptance Criteria:**
- Support Hindi, Tamil, Telugu, Bengali, Marathi
- Interface translated completely
- Medical terms explained in regional language
- Language selection persists across sessions

### 2.2 System User Stories

**US-5: Medical Information Extraction**  
As the system, I need to extract medical information from uploaded documents so that I can match patients with trials.

**Acceptance Criteria:**
- Extract diagnosis/conditions
- Extract current medications
- Extract test results and biomarkers
- Extract patient demographics (age, gender)
- Handle handwritten and scanned documents
- Accuracy: >85% for typed documents, >70% for handwritten

**US-6: Trial Matching Algorithm**  
As the system, I need to match patient profiles with trial eligibility criteria so that I can recommend relevant trials.

**Acceptance Criteria:**
- Match on primary medical condition
- Check age and gender requirements
- Verify exclusion criteria (medications, comorbidities)
- Consider geographic proximity
- Calculate confidence score for each match
- Return results in <5 seconds

## 3. Functional Requirements

### 3.1 Core Features (MVP)

**FR-1: User Authentication**
- Email/phone-based registration
- OTP verification
- Secure password storage
- Session management

**FR-2: Document Processing**
- OCR for scanned documents
- PDF text extraction
- Image preprocessing
- Document storage in S3

**FR-3: Medical NLP**
- Named Entity Recognition for medical terms
- Condition extraction
- Medication extraction
- Structured data generation

**FR-4: Trial Database**
- Store CTRI trial data
- Update weekly via scraper
- Full-text search capability
- Filter by status (recruiting/active)

**FR-5: Matching Engine**
- Multi-criteria matching algorithm
- Relevance scoring
- Ranking by confidence
- Explanation generation

**FR-6: Results Display**
- Trial cards with key information
- Filtering and sorting options
- Save favorites functionality
- Share trial information

### 3.2 Advanced Features (Future)

**FR-7: Notifications**
- New trial alerts
- Trial status updates
- Email and SMS notifications

**FR-8: WhatsApp Bot**
- Voice input for medical information
- Text-based trial search
- Results via WhatsApp messages

**FR-9: Analytics Dashboard**
- User engagement metrics
- Trial match statistics
- Geographic distribution

## 4. Non-Functional Requirements

### 4.1 Performance
- API response time: <3 seconds for search
- Document processing: <30 seconds per document
- Support 100 concurrent users (MVP)
- 99.5% uptime

### 4.2 Security
- HIPAA-compliant data handling
- End-to-end encryption for medical data
- Role-based access control
- Regular security audits
- Data retention policy: 2 years

### 4.3 Scalability
- Serverless architecture for auto-scaling
- Handle 10,000 users in Phase 2
- Database sharding for growth
- CDN for static content

### 4.4 Usability
- Mobile-responsive design
- Accessibility (WCAG 2.1 Level AA)
- Maximum 3 clicks to view trial results
- Clear error messages

### 4.5 Compliance
- Clear disclaimers about limitations
- Not a medical diagnosis tool
- Privacy policy and terms of service
- GDPR/Indian data protection compliance

## 5. Data Requirements

### 5.1 Data Sources
- **CTRI Database:** Primary source for Indian clinical trials
- **User Uploads:** Medical reports, prescriptions, lab results
- **Medical Ontologies:** ICD-10, SNOMED CT, UMLS

### 5.2 Data Storage
- **User Data:** Encrypted in RDS PostgreSQL
- **Documents:** S3 with encryption at rest
- **Trial Data:** OpenSearch for full-text search
- **Cache:** Redis for frequently accessed data

### 5.3 Synthetic Data (for Demo)
- 500 synthetic clinical trials
- 30 synthetic patient profiles
- Covering 10 major conditions (cancer, diabetes, cardiac, rare diseases)

## 6. Constraints & Assumptions

### 6.1 Constraints
- Hackathon timeline: 2-3 weeks for MVP
- Budget: AWS free tier + potential credits
- CTRI has no official API (requires scraping)
- Medical data requires careful handling

### 6.2 Assumptions
- Users have smartphones with camera
- Internet connectivity available (minimum 3G)
- Users consent to data processing
- CTRI website structure remains stable

## 7. Success Metrics

### 7.1 MVP Success Criteria
- 50+ synthetic trials in database
- 90% accuracy in medical entity extraction
- <5 second search response time
- 5 supported languages
- Successful demo with 10 test cases

### 7.2 Post-Launch Metrics
- 1,000 users in first 3 months
- 70% user satisfaction score
- 30% conversion to trial inquiry
- 50% reduction in trial discovery time

## 8. Out of Scope (for MVP)

- Real-time trial coordinator chat
- Video consultations
- Insurance verification
- Payment processing
- Mobile app (web-only for MVP)
- International trials (focus on India)
- Doctor portal (patient-only for MVP)
