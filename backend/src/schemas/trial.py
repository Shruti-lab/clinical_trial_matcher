"""Pydantic schemas for clinical trial API responses."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from enum import Enum


class TrialPhaseEnum(str, Enum):
    """Trial phase enumeration for API."""
    PHASE_I = "I"
    PHASE_II = "II"
    PHASE_III = "III"
    PHASE_IV = "IV"
    NOT_APPLICABLE = "N/A"


class TrialStatusEnum(str, Enum):
    """Trial status enumeration for API."""
    RECRUITING = "recruiting"
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    WITHDRAWN = "withdrawn"


class TrialContactInfo(BaseModel):
    """Contact information for a clinical trial."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    principal_investigator: Optional[str] = None


class TrialLocation(BaseModel):
    """Location information for a clinical trial."""
    location: str
    city: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TrialEligibility(BaseModel):
    """Eligibility criteria for a clinical trial."""
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    gender_criteria: Optional[str] = None
    eligibility_criteria: Optional[Dict[str, Any]] = None
    exclusion_criteria: Optional[List[str]] = None


class TrialResponse(BaseModel):
    """Basic trial information for list views."""
    id: str
    ctri_id: str
    title: str
    condition: str
    phase: TrialPhaseEnum
    status: TrialStatusEnum
    location: str
    city: Optional[str] = None
    state: Optional[str] = None
    sponsor: str
    start_date: Optional[date] = None
    estimated_completion: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrialDetailResponse(BaseModel):
    """Detailed trial information for single trial view."""
    id: str
    ctri_id: str
    title: str
    condition: str
    phase: TrialPhaseEnum
    status: TrialStatusEnum
    
    # Detailed description
    description: Optional[str] = None
    primary_objective: Optional[str] = None
    secondary_objectives: Optional[str] = None
    
    # Eligibility
    eligibility_criteria: Optional[Dict[str, Any]] = None
    exclusion_criteria: Optional[List[str]] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    gender_criteria: Optional[str] = None
    
    # Location
    location: str
    city: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Sponsor and contact
    sponsor: str
    principal_investigator: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    
    # Timeline
    start_date: Optional[date] = None
    estimated_completion: Optional[date] = None
    
    # Study design
    study_type: Optional[str] = None
    intervention_type: Optional[str] = None
    target_enrollment: Optional[int] = None
    
    # Metadata
    keywords: Optional[List[str]] = None
    source_url: Optional[str] = None
    last_updated_source: Optional[date] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrialListResponse(BaseModel):
    """Response for trial list/search endpoints."""
    trials: List[TrialResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class TrialSearchRequest(BaseModel):
    """Request body for advanced trial search."""
    condition: Optional[str] = Field(None, description="Medical condition to search for")
    location: Optional[str] = Field(None, description="Location (city, state, or general area)")
    phase: Optional[TrialPhaseEnum] = Field(None, description="Trial phase")
    status: Optional[TrialStatusEnum] = Field(TrialStatusEnum.RECRUITING, description="Trial status")
    
    # Patient criteria
    age: Optional[int] = Field(None, description="Patient age")
    gender: Optional[str] = Field(None, description="Patient gender")
    
    # Search radius for location-based search
    max_distance_km: Optional[int] = Field(100, description="Maximum distance in kilometers")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(20, ge=1, le=100, description="Items per page")


class TrialMatchResponse(BaseModel):
    """Response for trial matching with score."""
    trial: TrialResponse
    match_score: float = Field(..., ge=0, le=100, description="Match score (0-100)")
    match_explanation: str = Field(..., description="Explanation of why this trial matches")
    eligibility_summary: Dict[str, List[str]] = Field(
        ..., 
        description="Summary of met and unmet eligibility criteria"
    )
    distance_km: Optional[float] = Field(None, description="Distance from patient location")


class TrialMatchListResponse(BaseModel):
    """Response for trial matching endpoints."""
    matches: List[TrialMatchResponse]
    total_matches: int
    processing_time_ms: int
    search_criteria: Dict[str, Any]