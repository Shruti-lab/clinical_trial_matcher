"""Document service for database operations."""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Tuple
from uuid import uuid4
import logging

from ..models.document import Document, ProcessingStatus
from ..schemas.document import DocumentUploadRequest, DocumentResponse
from .s3_service import s3_service

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document database operations."""
    
    def create_document(
        self, 
        db: Session, 
        user_id: str, 
        upload_request: DocumentUploadRequest,
        s3_key: str,
        document_id: str
    ) -> Document:
        """
        Create a new document record in the database.
        
        Args:
            db: Database session
            user_id: User identifier
            upload_request: Document upload request data
            s3_key: S3 object key
            document_id: Unique document identifier
            
        Returns:
            Created document instance
        """
        try:
            document = Document(
                id=document_id,
                user_id=user_id,
                s3_key=s3_key,
                file_name=upload_request.file_name,
                file_type=upload_request.file_type,
                file_size=upload_request.file_size,
                processing_status=ProcessingStatus.PENDING
            )
            
            db.add(document)
            db.commit()
            db.refresh(document)
            
            logger.info(f"Created document record: {document_id}")
            return document
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create document record: {e}")
            raise
    
    def get_document_by_id(
        self, 
        db: Session, 
        document_id: str, 
        user_id: str
    ) -> Optional[Document]:
        """
        Get a document by ID, ensuring it belongs to the user.
        
        Args:
            db: Database session
            document_id: Document identifier
            user_id: User identifier
            
        Returns:
            Document instance or None if not found
        """
        return db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == user_id
        ).first()
    
    def get_user_documents(
        self, 
        db: Session, 
        user_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Document], int]:
        """
        Get documents for a user with pagination.
        
        Args:
            db: Database session
            user_id: User identifier
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (documents list, total count)
        """
        query = db.query(Document).filter(Document.user_id == user_id)
        
        total = query.count()
        documents = query.order_by(desc(Document.created_at)).offset(skip).limit(limit).all()
        
        return documents, total
    
    def update_document_status(
        self, 
        db: Session, 
        document_id: str, 
        status: ProcessingStatus,
        extracted_text: Optional[str] = None,
        processing_error: Optional[str] = None,
        ocr_confidence: Optional[float] = None,
        processing_duration: Optional[int] = None
    ) -> Optional[Document]:
        """
        Update document processing status and related fields.
        
        Args:
            db: Database session
            document_id: Document identifier
            status: New processing status
            extracted_text: Extracted text content
            processing_error: Error message if processing failed
            ocr_confidence: OCR confidence score
            processing_duration: Processing time in seconds
            
        Returns:
            Updated document instance or None if not found
        """
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            
            if not document:
                return None
            
            document.processing_status = status
            
            if extracted_text is not None:
                document.extracted_text = extracted_text
            
            if processing_error is not None:
                document.processing_error = processing_error
            
            if ocr_confidence is not None:
                document.ocr_confidence = ocr_confidence
            
            if processing_duration is not None:
                document.processing_duration = processing_duration
            
            db.commit()
            db.refresh(document)
            
            logger.info(f"Updated document {document_id} status to {status.value}")
            return document
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update document status: {e}")
            raise
    
    def delete_document(
        self, 
        db: Session, 
        document_id: str, 
        user_id: str
    ) -> bool:
        """
        Delete a document from database and S3.
        
        Args:
            db: Database session
            document_id: Document identifier
            user_id: User identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            document = self.get_document_by_id(db, document_id, user_id)
            
            if not document:
                return False
            
            # Delete from S3 first
            s3_deleted = s3_service.delete_document(document.s3_key)
            
            if not s3_deleted:
                logger.warning(f"Failed to delete document from S3: {document.s3_key}")
            
            # Delete from database
            db.delete(document)
            db.commit()
            
            logger.info(f"Deleted document: {document_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to delete document: {e}")
            return False
    
    def get_documents_by_status(
        self, 
        db: Session, 
        status: ProcessingStatus,
        limit: int = 100
    ) -> List[Document]:
        """
        Get documents by processing status (for background processing).
        
        Args:
            db: Database session
            status: Processing status to filter by
            limit: Maximum number of documents to return
            
        Returns:
            List of documents with the specified status
        """
        return db.query(Document).filter(
            Document.processing_status == status
        ).order_by(Document.created_at).limit(limit).all()


# Global document service instance
document_service = DocumentService()