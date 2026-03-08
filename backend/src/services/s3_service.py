"""S3 service for handling document uploads and storage."""

import boto3
import uuid
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging

from ..config import settings

logger = logging.getLogger(__name__)


class S3Service:
    """Service for handling S3 operations."""
    
    def __init__(self):
        """Initialize S3 client."""
        try:
            self.s3_client = boto3.client(
                's3',
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key
            )
            self.bucket_name = settings.s3_bucket_name
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise
    
    def generate_presigned_upload_url(
        self, 
        user_id: str, 
        file_name: str, 
        file_type: str,
        file_size: int,
        expires_in: int = 3600
    ) -> Dict[str, str]:
        """
        Generate a pre-signed URL for uploading a file to S3.
        
        Args:
            user_id: User identifier
            file_name: Original filename
            file_type: File type (pdf, jpg, jpeg, png)
            file_size: File size in bytes
            expires_in: URL expiration time in seconds (default: 1 hour)
            
        Returns:
            Dictionary containing upload URL and metadata
            
        Raises:
            ClientError: If S3 operation fails
            ValueError: If file type or size is invalid
        """
        # Validate file type
        if not self._is_valid_file_type(file_type):
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB in bytes
        if file_size > max_size:
            raise ValueError(f"File size {file_size} exceeds maximum allowed size of {max_size} bytes")
        
        try:
            # Generate unique S3 key
            document_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().strftime('%Y/%m/%d')
            s3_key = f"documents/{user_id}/{timestamp}/{document_id}_{file_name}"
            
            # Define upload conditions
            conditions = [
                {"bucket": self.bucket_name},
                {"key": s3_key},
                ["content-length-range", 1, max_size],  # Enforce file size limit
                ["eq", "$Content-Type", self._get_content_type(file_type)],
            ]
            
            # Generate pre-signed POST URL
            response = self.s3_client.generate_presigned_post(
                Bucket=self.bucket_name,
                Key=s3_key,
                Fields={
                    "Content-Type": self._get_content_type(file_type),
                    "x-amz-server-side-encryption": "AES256",  # Enable encryption
                },
                Conditions=conditions,
                ExpiresIn=expires_in
            )
            
            return {
                "document_id": document_id,
                "s3_key": s3_key,
                "upload_url": response["url"],
                "fields": response["fields"],
                "expires_in": expires_in
            }
            
        except ClientError as e:
            logger.error(f"Failed to generate pre-signed URL: {e}")
            raise
    
    def generate_presigned_download_url(
        self, 
        s3_key: str, 
        expires_in: int = 3600
    ) -> str:
        """
        Generate a pre-signed URL for downloading a file from S3.
        
        Args:
            s3_key: S3 object key
            expires_in: URL expiration time in seconds
            
        Returns:
            Pre-signed download URL
            
        Raises:
            ClientError: If S3 operation fails
        """
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expires_in
            )
            return response
            
        except ClientError as e:
            logger.error(f"Failed to generate download URL: {e}")
            raise
    
    def delete_document(self, s3_key: str) -> bool:
        """
        Delete a document from S3.
        
        Args:
            s3_key: S3 object key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            logger.info(f"Successfully deleted document: {s3_key}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to delete document {s3_key}: {e}")
            return False
    
    def check_document_exists(self, s3_key: str) -> bool:
        """
        Check if a document exists in S3.
        
        Args:
            s3_key: S3 object key
            
        Returns:
            True if document exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
            
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            logger.error(f"Error checking document existence {s3_key}: {e}")
            return False
    
    def get_document_metadata(self, s3_key: str) -> Optional[Dict]:
        """
        Get document metadata from S3.
        
        Args:
            s3_key: S3 object key
            
        Returns:
            Document metadata dictionary or None if not found
        """
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return {
                'size': response.get('ContentLength'),
                'last_modified': response.get('LastModified'),
                'content_type': response.get('ContentType'),
                'etag': response.get('ETag'),
                'encryption': response.get('ServerSideEncryption')
            }
            
        except ClientError as e:
            logger.error(f"Failed to get document metadata {s3_key}: {e}")
            return None
    
    def _get_content_type(self, file_type: str) -> str:
        """
        Get MIME content type for file type.
        
        Args:
            file_type: File extension
            
        Returns:
            MIME content type
        """
        content_types = {
            'pdf': 'application/pdf',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png'
        }
        return content_types.get(file_type.lower(), 'application/octet-stream')
    
    def _is_valid_file_type(self, file_type: str) -> bool:
        """
        Check if file type is supported.
        
        Args:
            file_type: File extension
            
        Returns:
            True if file type is supported, False otherwise
        """
        supported_types = {'pdf', 'jpg', 'jpeg', 'png'}
        return file_type.lower() in supported_types


# Global S3 service instance
s3_service = S3Service()