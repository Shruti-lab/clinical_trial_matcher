"""User model for authentication and profile management."""

from sqlalchemy import String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from .base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from .medical_profile import MedicalProfile
    from .document import Document
    from .match import Match


class User(Base, UUIDMixin, TimestampMixin):
    """User model for storing user authentication and basic information."""
    
    __tablename__ = "users"
    
    # Authentication fields
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # User preferences
    preferred_language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    
    # Relationships
    medical_profile: Mapped["MedicalProfile"] = relationship(
        "MedicalProfile", 
        back_populates="user", 
        uselist=False,
        cascade="all, delete-orphan"
    )
    documents: Mapped[List["Document"]] = relationship(
        "Document", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    matches: Mapped[List["Match"]] = relationship(
        "Match", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    # Indexes for frequently queried fields
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_phone', 'phone'),
        Index('idx_user_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"