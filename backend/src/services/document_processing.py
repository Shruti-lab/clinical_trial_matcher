"""Document processing service using Amazon Textract for OCR and simple medical entity extraction."""

import boto3
import json
import re
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.document import Document
from ..models.medical_profile import MedicalProfile
from ..config import settings

logger = logging.getLogger(__name__)
# settings = settings()

class DocumentProcessor:
    """Service for processing medical documents with OCR and entity extraction."""
    
    def __init__(self):
        self.textract_client = boto3.client(
            'textract',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.s3_client = boto3.client(
            's3',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
    
    def process_document(self, document_id: str, s3_bucket: str, s3_key: str) -> Dict:
        """
        Process a document with OCR and medical entity extraction.
        
        Args:
            document_id: Database ID of the document
            s3_bucket: S3 bucket name
            s3_key: S3 object key
            
        Returns:
            Dict with processing results
        """
        try:
            logger.info(f"Starting document processing for {document_id}")
            
            # Update document status to processing
            self._update_document_status(document_id, "processing")
            
            # Step 1: Extract text using Textract
            extracted_text = self._extract_text_with_textract(s3_bucket, s3_key)
            
            # Step 2: Extract medical entities using simple pattern matching
            medical_entities = self._extract_medical_entities_simple(extracted_text)
            
            # Step 3: Update medical profile
            self._update_medical_profile(document_id, medical_entities, extracted_text)
            
            # Step 4: Update document status to completed
            self._update_document_status(document_id, "completed")
            
            logger.info(f"Document processing completed for {document_id}")
            
            return {
                "status": "success",
                "document_id": document_id,
                "extracted_text_length": len(extracted_text),
                "entities_found": len(medical_entities.get("conditions", [])) + len(medical_entities.get("medications", []))
            }
            
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {str(e)}")
            self._update_document_status(document_id, "failed", str(e))
            return {
                "status": "error",
                "document_id": document_id,
                "error": str(e)
            }
    
    def _extract_text_with_textract(self, bucket: str, key: str) -> str:
        """Extract text from document using Amazon Textract."""
        try:
            # For single-page documents, use detect_document_text
            response = self.textract_client.detect_document_text(
                Document={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                }
            )
            
            # Extract text from blocks
            text_lines = []
            for block in response.get('Blocks', []):
                if block['BlockType'] == 'LINE':
                    text_lines.append(block['Text'])
            
            extracted_text = '\n'.join(text_lines)
            logger.info(f"Extracted {len(extracted_text)} characters from document")
            
            return extracted_text
            
        except Exception as e:
            logger.error(f"Textract extraction failed: {str(e)}")
            raise
    
    def _extract_medical_entities_simple(self, text: str) -> Dict[str, List[str]]:
        """
        Extract medical entities using simple pattern matching.
        This is a cost-effective alternative to Amazon Comprehend Medical.
        """
        text_lower = text.lower()
        
        # Define medical condition patterns
        condition_patterns = {
            'cancer': ['cancer', 'carcinoma', 'tumor', 'tumour', 'malignancy', 'oncology'],
            'diabetes': ['diabetes', 'diabetic', 'blood sugar', 'glucose', 'insulin'],
            'hypertension': ['hypertension', 'high blood pressure', 'bp', 'blood pressure'],
            'heart disease': ['heart disease', 'cardiac', 'coronary', 'myocardial', 'angina'],
            'kidney disease': ['kidney', 'renal', 'nephrology', 'dialysis'],
            'liver disease': ['liver', 'hepatic', 'hepatitis', 'cirrhosis'],
            'lung disease': ['lung', 'pulmonary', 'respiratory', 'asthma', 'copd'],
            'arthritis': ['arthritis', 'joint pain', 'rheumatoid', 'osteoarthritis'],
            'depression': ['depression', 'anxiety', 'mental health', 'psychiatric'],
            'stroke': ['stroke', 'cerebrovascular', 'brain attack']
        }
        
        # Define medication patterns
        medication_patterns = [
            'metformin', 'insulin', 'aspirin', 'lisinopril', 'atorvastatin',
            'amlodipine', 'omeprazole', 'levothyroxine', 'warfarin', 'prednisone',
            'chemotherapy', 'radiation', 'immunotherapy'
        ]
        
        # Extract conditions
        conditions = []
        for condition, patterns in condition_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    conditions.append(condition.title())
                    break
        
        # Extract medications
        medications = []
        for med in medication_patterns:
            if med in text_lower:
                medications.append(med.title())
        
        # Extract demographics using regex
        demographics = self._extract_demographics(text)
        
        # Extract test results
        test_results = self._extract_test_results(text)
        
        return {
            'conditions': list(set(conditions)),  # Remove duplicates
            'medications': list(set(medications)),
            'demographics': demographics,
            'test_results': test_results
        }
    
    def _extract_demographics(self, text: str) -> Dict[str, Optional[str]]:
        """Extract demographic information using regex patterns."""
        demographics = {}
        
        # Extract age
        age_patterns = [
            r'age[:\s]*(\d{1,3})',
            r'(\d{1,3})\s*years?\s*old',
            r'(\d{1,3})\s*yo'
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, text.lower())
            if match:
                age = int(match.group(1))
                if 0 <= age <= 120:  # Reasonable age range
                    demographics['age'] = age
                    break
        
        # Extract gender
        if re.search(r'\b(male|man|mr\.?)\b', text.lower()):
            demographics['gender'] = 'male'
        elif re.search(r'\b(female|woman|mrs?\.?|ms\.?)\b', text.lower()):
            demographics['gender'] = 'female'
        
        return demographics
    
    def _extract_test_results(self, text: str) -> Dict[str, str]:
        """Extract test results and lab values."""
        test_results = {}
        
        # Common lab value patterns
        lab_patterns = {
            'hemoglobin': r'h[ae]moglobin[:\s]*(\d+\.?\d*)',
            'glucose': r'glucose[:\s]*(\d+\.?\d*)',
            'cholesterol': r'cholesterol[:\s]*(\d+\.?\d*)',
            'blood_pressure': r'bp[:\s]*(\d+/\d+)',
            'weight': r'weight[:\s]*(\d+\.?\d*)\s*kg',
            'height': r'height[:\s]*(\d+\.?\d*)\s*cm'
        }
        
        for test_name, pattern in lab_patterns.items():
            match = re.search(pattern, text.lower())
            if match:
                test_results[test_name] = match.group(1)
        
        return test_results
    
    def _update_medical_profile(self, document_id: str, entities: Dict, extracted_text: str):
        """Update or create medical profile with extracted entities."""
        db = next(get_db())
        try:
            # Get document to find user_id
            document = db.query(Document).filter(Document.id == document_id).first()
            if not document:
                raise ValueError(f"Document {document_id} not found")
            
            # Get or create medical profile
            profile = db.query(MedicalProfile).filter(
                MedicalProfile.user_id == document.user_id
            ).first()
            
            if not profile:
                profile = MedicalProfile(
                    user_id=document.user_id,
                    conditions=[],
                    medications=[],
                    test_results={},
                    medical_history=[]
                )
                db.add(profile)
            
            # Update profile with new entities
            if entities.get('conditions'):
                existing_conditions = set(profile.conditions or [])
                new_conditions = set(entities['conditions'])
                profile.conditions = list(existing_conditions.union(new_conditions))
            
            if entities.get('medications'):
                existing_medications = set(profile.medications or [])
                new_medications = set(entities['medications'])
                profile.medications = list(existing_medications.union(new_medications))
            
            # Update demographics
            if entities.get('demographics'):
                demo = entities['demographics']
                if demo.get('age'):
                    profile.age = demo['age']
                if demo.get('gender'):
                    profile.gender = demo['gender']
            
            # Update test results
            if entities.get('test_results'):
                existing_results = profile.test_results or {}
                existing_results.update(entities['test_results'])
                profile.test_results = existing_results
            
            # Add to medical history
            if not profile.medical_history:
                profile.medical_history = []
            
            history_entry = f"Document processed on {datetime.now().strftime('%Y-%m-%d')}: Found {len(entities.get('conditions', []))} conditions, {len(entities.get('medications', []))} medications"
            profile.medical_history.append(history_entry)
            
            # Update document with extracted text
            document.extracted_text = extracted_text
            
            db.commit()
            logger.info(f"Updated medical profile for user {document.user_id}")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update medical profile: {str(e)}")
            raise
        finally:
            db.close()
    
    def _update_document_status(self, document_id: str, status: str, error_message: str = None):
        """Update document processing status."""
        db = next(get_db())
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            if document:
                document.processing_status = status
                if error_message:
                    document.processing_error = error_message
                db.commit()
                logger.info(f"Updated document {document_id} status to {status}")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update document status: {str(e)}")
        finally:
            db.close()


# Lambda function handler for AWS Lambda deployment
def lambda_handler(event, context):
    """
    AWS Lambda handler for document processing.
    Expected event format:
    {
        "document_id": "uuid",
        "s3_bucket": "bucket-name",
        "s3_key": "path/to/file"
    }
    """
    try:
        processor = DocumentProcessor()
        
        # Extract parameters from event
        document_id = event.get('document_id')
        s3_bucket = event.get('s3_bucket')
        s3_key = event.get('s3_key')
        
        if not all([document_id, s3_bucket, s3_key]):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required parameters: document_id, s3_bucket, s3_key'
                })
            }
        
        # Process document
        result = processor.process_document(document_id, s3_bucket, s3_key)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        logger.error(f"Lambda handler error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


# Async task for FastAPI (alternative to Lambda)
async def process_document_async(document_id: str, s3_bucket: str, s3_key: str):
    """
    Async task for document processing in FastAPI.
    Can be used with background tasks or Celery.
    """
    processor = DocumentProcessor()
    return processor.process_document(document_id, s3_bucket, s3_key)