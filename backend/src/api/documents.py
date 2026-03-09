"""Document upload and management API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import logging

from ..database import get_db
from ..schemas.document import (
    DocumentUploadRequest, 
    DocumentUploadResponse, 
    DocumentResponse,
    DocumentListResponse,
    DocumentStatusResponse
)
from ..services.s3_service import s3_service
from ..services.document_service import document_service
from ..services.document_processing import process_document_async
from ..models.document import ProcessingStatus
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])


# TODO: Replace with actual authentication dependency
def get_current_user_id() -> str:
    """Temporary mock function for user authentication."""
    return "temp-user-123"  # This should be replaced with actual JWT auth


@router.post("/", response_model=DocumentUploadResponse)
async def create_document_upload(
    upload_request: DocumentUploadRequest,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Create a pre-signed URL for document upload to S3.
    
    This endpoint:
    1. Validates the upload request
    2. Generates a pre-signed S3 URL
    3. Creates a document record in the database
    4. Returns the upload URL and metadata
    """
    try:
        # Generate pre-signed upload URL
        upload_data = s3_service.generate_presigned_upload_url(
            user_id=current_user_id,
            file_name=upload_request.file_name,
            file_type=upload_request.file_type,
            file_size=upload_request.file_size
        )
        
        # Create document record in database
        document = document_service.create_document(
            db=db,
            user_id=current_user_id,
            upload_request=upload_request,
            s3_key=upload_data["s3_key"],
            document_id=upload_data["document_id"]
        )
        
        # Return upload URL and metadata
        return DocumentUploadResponse(
            document_id=document.id,
            upload_url=upload_data["upload_url"],
            fields=upload_data["fields"],
            expires_in=upload_data["expires_in"],
            max_file_size=10485760  # 10MB
        )
        
    except ValueError as e:
        logger.error(f"Validation error in document upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to create document upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create document upload"
        )


@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    List documents for the current user with pagination.
    """
    try:
        skip = (page - 1) * per_page
        documents, total = document_service.get_user_documents(
            db=db,
            user_id=current_user_id,
            skip=skip,
            limit=per_page
        )
        
        return DocumentListResponse(
            documents=[DocumentResponse.from_orm(doc) for doc in documents],
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        logger.error(f"Failed to list documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve documents"
        )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get a specific document by ID.
    """
    try:
        document = document_service.get_document_by_id(
            db=db,
            document_id=document_id,
            user_id=current_user_id
        )
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        return DocumentResponse.from_orm(document)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get document {document_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve document"
        )


@router.get("/{document_id}/status", response_model=DocumentStatusResponse)
async def get_document_status(
    document_id: str,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get document processing status.
    """
    try:
        document = document_service.get_document_by_id(
            db=db,
            document_id=document_id,
            user_id=current_user_id
        )
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Calculate progress percentage based on status
        progress_map = {
            ProcessingStatus.PENDING: 0,
            ProcessingStatus.PROCESSING: 50,
            ProcessingStatus.COMPLETED: 100,
            ProcessingStatus.FAILED: 0
        }
        
        return DocumentStatusResponse(
            document_id=document.id,
            processing_status=document.processing_status.value,
            progress_percentage=progress_map.get(document.processing_status, 0),
            processing_error=document.processing_error
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get document status {document_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve document status"
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Delete a document from both database and S3.
    """
    try:
        success = document_service.delete_document(
            db=db,
            document_id=document_id,
            user_id=current_user_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        return {"message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete document {document_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete document"
        )


@router.post("/{document_id}/process")
async def trigger_document_processing(
    document_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Trigger document processing after successful upload to S3.
    This endpoint should be called after the client confirms successful upload.
    """
    try:
        document = document_service.get_document_by_id(
            db=db,
            document_id=document_id,
            user_id=current_user_id
        )
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        if document.processing_status != ProcessingStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Document is already {document.processing_status.value}"
            )
        
        # Check if document exists in S3
        if not s3_service.check_document_exists(document.s3_key):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document not found in storage. Please upload first."
            )
        
        # Get settings for S3 bucket
        settings = get_settings()
        
        # Trigger background processing
        background_tasks.add_task(
            process_document_async,
            document_id=document.id,
            s3_bucket=settings.AWS_S3_BUCKET,
            s3_key=document.s3_key
        )
        
        return {
            "message": "Document processing started",
            "document_id": document.id,
            "status": "processing"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to trigger processing for {document_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to trigger document processing"
        )


@router.get("/{document_id}/download")
async def get_document_download_url(
    document_id: str,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get a pre-signed URL for downloading a document from S3.
    """
    try:
        document = document_service.get_document_by_id(
            db=db,
            document_id=document_id,
            user_id=current_user_id
        )
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Check if document exists in S3
        if not s3_service.check_document_exists(document.s3_key):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document file not found in storage"
            )
        
        # Generate download URL
        download_url = s3_service.generate_presigned_download_url(
            s3_key=document.s3_key,
            expires_in=3600  # 1 hour
        )
        
        return {
            "download_url": download_url,
            "expires_in": 3600,
            "file_name": document.file_name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate download URL for {document_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate download URL"
        )