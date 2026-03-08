"""Match model for storing patient-trial matching results."""

from sqlalchemy import String, Float, Boolean, Text, ForeignKey, Index, Enum, DateTime
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional
from datetime import datetime
import enum

from .base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from .user import User
    from .clinical_trial import ClinicalTrial


class MatchStatus(enum.Enum):
    """Match status enumeration."""
    VIEWED = "viewed"
    CONTACTED = "contacted"
    ENROLLED = "enrolled"
    DECLINED = "declined"
    INELIGIBLE = "ineligible"


class Match(Base, UUIDMixin, TimestampMixin):
    """Match model for storing patient-trial matching results and user interactions."""
    
    __tablename__ = "matches"
    
    # Foreign keys
    user_id: Mapped[str] = mapped_column(
        CHAR(36), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    trial_id: Mapped[str] = mapped_column(
        CHAR(36), 
        ForeignKey("clinical_trials.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Matching results
    match_score: Mapped[float] = mapped_column(
        Float, 
        nullable=False,
        index=True,
        comment="Match score between 0-100"
    )
    match_explanation: Mapped[str] = mapped_column(
        Text, 
        nullable=True,
        comment="Human-readable explanation of why this trial matches"
    )
    
    # Detailed scoring breakdown (for transparency and debugging)
    condition_score: Mapped[float] = mapped_column(Float, nullable=True)
    eligibility_score: Mapped[float] = mapped_column(Float, nullable=True)
    location_score: Mapped[float] = mapped_column(Float, nullable=True)
    exclusion_score: Mapped[float] = mapped_column(Float, nullable=True)
    
    # User interaction tracking
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    status: Mapped[MatchStatus] = mapped_column(
        Enum(MatchStatus),
        default=MatchStatus.VIEWED,
        nullable=False,
        index=True
    )
    
    # Contact tracking
    contact_attempted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    contact_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="matches")
    trial: Mapped["ClinicalTrial"] = relationship("ClinicalTrial", back_populates="matches")
    
    # Indexes for frequently queried fields
    __table_args__ = (
        Index('idx_match_user_id', 'user_id'),
        Index('idx_match_trial_id', 'trial_id'),
        Index('idx_match_score', 'match_score'),
        Index('idx_match_favorite', 'is_favorite'),
        Index('idx_match_status', 'status'),
        Index('idx_match_created_at', 'created_at'),
        # Composite indexes for common query patterns
        Index('idx_match_user_score', 'user_id', 'match_score'),
        Index('idx_match_user_favorite', 'user_id', 'is_favorite'),
        Index('idx_match_user_status', 'user_id', 'status'),
        # Unique constraint to prevent duplicate matches
        Index('idx_match_unique', 'user_id', 'trial_id', unique=True),
    )
    
    def __repr__(self) -> str:
        return f"<Match(id={self.id}, user_id={self.user_id}, trial_id={self.trial_id}, score={self.match_score})>"