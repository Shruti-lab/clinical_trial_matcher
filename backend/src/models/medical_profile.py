"""Medical profile model for storing patient medical information."""

from sqlalchemy import String, Integer, Text, JSON, ForeignKey, Index
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Dict, List, Optional, TYPE_CHECKING

from .base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from .user import User


class MedicalProfile(Base, UUIDMixin, TimestampMixin):
    """Medical profile model for storing extracted patient medical information."""
    
    __tablename__ = "medical_profiles"
    
    # Foreign key to user
    user_id: Mapped[str] = mapped_column(
        CHAR(36), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Demographics
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Medical information (stored as JSON arrays/objects)
    conditions: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True,
        comment="List of medical conditions/diagnoses"
    )
    medications: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True,
        comment="List of current medications"
    )
    test_results: Mapped[Optional[Dict]] = mapped_column(
        JSON, 
        nullable=True,
        comment="Lab results and biomarkers as key-value pairs"
    )
    medical_history: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True,
        comment="List of past medical history items"
    )
    
    # Additional medical information
    allergies: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True,
        comment="List of known allergies"
    )
    procedures: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True,
        comment="List of past procedures/surgeries"
    )
    
    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="medical_profile")
    
    # Indexes for frequently queried fields
    __table_args__ = (
        Index('idx_medical_profile_user_id', 'user_id'),
        Index('idx_medical_profile_age', 'age'),
        Index('idx_medical_profile_gender', 'gender'),
        Index('idx_medical_profile_location', 'location'),
        Index('idx_medical_profile_updated_at', 'updated_at'),
    )
    
    def __repr__(self) -> str:
        return f"<MedicalProfile(id={self.id}, user_id={self.user_id}, age={self.age})>"