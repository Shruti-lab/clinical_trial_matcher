"""Clinical trial model for storing trial information from CTRI."""

from sqlalchemy import String, Text, Date, Float, JSON, Index, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Dict, List, Optional, TYPE_CHECKING
from datetime import date
import enum

from .base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from .match import Match


class TrialPhase(enum.Enum):
    """Clinical trial phase enumeration."""
    PHASE_I = "Phase 1"
    PHASE_II = "Phase 2"
    PHASE_III = "Phase 3"
    PHASE_IV = "Phase 4"
    NOT_APPLICABLE = "N/A"


class TrialStatus(enum.Enum):
    """Clinical trial status enumeration."""
    RECRUITING = "Open to Recruitment"
    ACTIVE = "active"
    COMPLETED = "Completed"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    WITHDRAWN = "withdrawn"
    OTHER = "Publication Details"


class ClinicalTrial(Base, UUIDMixin, TimestampMixin):
    """Clinical trial model for storing trial information from CTRI database."""
    
    __tablename__ = "clinical_trials"
    
    # CTRI identification
    ctri_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    
    # Basic trial information
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    condition_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phase: Mapped[TrialPhase] = mapped_column(Enum(TrialPhase, values_callable=lambda x: [e.value for e in x]), nullable=False, index=True)
    status: Mapped[TrialStatus] = mapped_column(Enum(TrialStatus, values_callable=lambda x: [e.value for e in x]), nullable=False, index=True)
    
    # Detailed description
    description: Mapped[str] = mapped_column(Text, nullable=True)
    primary_objective: Mapped[str] = mapped_column(Text, nullable=True)
    secondary_objectives: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Eligibility criteria (stored as JSON for flexibility) ie inclusion criteria
    eligibility_criteria: Mapped[Optional[Dict]] = mapped_column(
        JSON, 
        nullable=True,
        comment="Structured eligibility criteria including age, gender, conditions"
    )
    exclusion_criteria: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True,
        comment="List of exclusion criteria"
    )
    
    # Age criteria (extracted for easy querying)
    min_age: Mapped[Optional[int]] = mapped_column(nullable=True, index=True)
    max_age: Mapped[Optional[int]] = mapped_column(nullable=True, index=True)
    gender_criteria: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)
    
    # Location information
    location: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Sponsor and contact information
    sponsor: Mapped[str] = mapped_column(String(255), nullable=False)
    principal_investigator: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Timeline
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    estimated_completion: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    
    # Study design
    study_type: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    intervention_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_enrollment: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    # Additional metadata
    keywords: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True,
        comment="Keywords for search and matching (stored as text)"
    )
    
    # Data source tracking
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Relationships
    matches: Mapped[List["Match"]] = relationship(
        "Match", 
        back_populates="trial",
        cascade="all, delete-orphan"
    )
    
    # Comprehensive indexes for search and filtering
    __table_args__ = (
        Index('idx_trial_ctri_id', 'ctri_id'),
        Index('idx_trial_condition', 'condition_name'),
        Index('idx_trial_phase', 'phase'),
        Index('idx_trial_status', 'status'),
        Index('idx_trial_location', 'location'),
        Index('idx_trial_city', 'city'),
        Index('idx_trial_state', 'state'),
        Index('idx_trial_age_range', 'min_age', 'max_age'),
        Index('idx_trial_gender', 'gender_criteria'),
        Index('idx_trial_start_date', 'start_date'),
        Index('idx_trial_coordinates', 'latitude', 'longitude'),
        Index('idx_trial_sponsor', 'sponsor'),
        Index('idx_trial_updated_at', 'updated_at'),
        # Composite indexes for common query patterns
        Index('idx_trial_status_condition', 'status', 'condition_name'),
        Index('idx_trial_phase_status', 'phase', 'status'),
        Index('idx_trial_location_status', 'location', 'status'),
    )
    
    def __repr__(self) -> str:
        return f"<ClinicalTrial(id={self.id}, ctri_id={self.ctri_id}, condition_name={self.condition_name})>"