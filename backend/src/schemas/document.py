"""Document-related Pydantic schemas."""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class FileType(str, Enum):
    """Supported file types for document upload."""
    PDF = "pdf"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"


class DocumentUploadRequest(BaseModel):
    """Request schema for document upload."""
    file_name: str = Field(..., min_length=1, max_length=255, description="Original filename")
    file_type: str = Field(..., description="File type (pdf, jpg, jpeg, png)")
    file_size: int = Field(..., gt=0, le=10485760, description="File size in bytes (max 10MB)")
    
    @validator('file_type')
    def validate_file_type(cls, v):
        """Validate file type is supported."""
        allowed_types = ['pdf', 'jpg', 'jpeg', 'png']
        if v.lower() not in allowed_types:
            raise ValueError(f'File type must be one of: {", ".join(allowed_types)}')
        return v.lower()
    
    @validator('file_name')
    def validate_file_name(cls, v):
        """Validate filename doesn't contain dangerous characters."""
        dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
        if any(char in v for char in dangerous_chars):
            raise ValueError('Filename contains invalid characters')
        return v


class DocumentUploadResponse(BaseModel):
    """Response schema for document upload."""
    document_id: str = Field(..., description="Unique document identifier")
    upload_url: str = Field(..., description="Pre-signed S3 URL for upload")
    fields: dict = Field(..., description="Form fields required for S3 POST upload")
    expires_in: int = Field(..., description="URL expiration time in seconds")
    max_file_size: int = Field(default=10485760, description="Maximum allowed file size")


class DocumentResponse(BaseModel):
    """Response schema for document information."""
    id: str
    file_name: str
    file_type: str
    file_size: Optional[int]
    processing_status: str
    extracted_text: Optional[str]
    processing_error: Optional[str]
    ocr_confidence: Optional[float]
    processing_duration: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Response schema for listing documents."""
    documents: List[DocumentResponse]
    total: int
    page: int
    per_page: int


class DocumentStatusResponse(BaseModel):
    """Response schema for document processing status."""
    document_id: str
    processing_status: str
    progress_percentage: Optional[int] = Field(None, description="Processing progress (0-100)")
    processing_error: Optional[str]
    estimated_completion: Optional[datetime]