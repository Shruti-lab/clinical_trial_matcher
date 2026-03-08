"""Document model for storing uploaded medical documents."""

from sqlalchemy import String, Text, ForeignKey, Index, Enum
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
import enum

from .base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from .user import User


class ProcessingStatus(enum.Enum):
    """Document processing status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(Base, UUIDMixin, TimestampMixin):
    """Document model for storing uploaded medical documents and their processing status."""
    
    __tablename__ = "documents"
    
    # Foreign key to user
    user_id: Mapped[str] = mapped_column(
        CHAR(36), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # File information
    s3_key: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=True, comment="File size in bytes")
    
    # Processing information
    processing_status: Mapped[ProcessingStatus] = mapped_column(
        Enum(ProcessingStatus),
        default=ProcessingStatus.PENDING,
        nullable=False,
        index=True
    )
    
    # Extracted content
    extracted_text: Mapped[str] = mapped_column(Text, nullable=True)
    processing_error: Mapped[str] = mapped_column(Text, nullable=True)
    
    # OCR and processing metadata
    ocr_confidence: Mapped[float] = mapped_column(nullable=True, comment="OCR confidence score 0-1")
    processing_duration: Mapped[int] = mapped_column(nullable=True, comment="Processing time in seconds")
    
    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="documents")
    
    # Indexes for frequently queried fields
    __table_args__ = (
        Index('idx_document_user_id', 'user_id'),
        Index('idx_document_status', 'processing_status'),
        Index('idx_document_s3_key', 's3_key'),
        Index('idx_document_created_at', 'created_at'),
        Index('idx_document_file_type', 'file_type'),
    )
    
    def __repr__(self) -> str:
        return f"<Document(id={self.id}, file_name={self.file_name}, status={self.processing_status.value})>"