"""Pydantic schemas for matching API endpoints."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from .trial import TrialMatchResponse


class MatchRequest(BaseModel):
    """Request for finding matching trials."""
    filters: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional filters for matching"
    )
    limit: int = Field(20, ge=1, le=50, description="Maximum number of matches to return")


class MatchResultsResponse(BaseModel):
    """Response for match results."""
    matches: List[TrialMatchResponse]
    total_matches: int
    last_updated: datetime
    user_profile_summary: Dict[str, Any]


class FavoriteRequest(BaseModel):
    """Request to save a trial as favorite."""
    trial_id: str = Field(..., description="ID of the trial to favorite")
    match_score: Optional[float] = Field(None, description="Match score for this trial")
    match_explanation: Optional[str] = Field(None, description="Explanation of the match")


class FavoriteResponse(BaseModel):
    """Response for favorite operations."""
    message: str
    trial_id: str
    is_favorite: bool


class FavoriteListResponse(BaseModel):
    """Response for listing favorite trials."""
    favorites: List[TrialMatchResponse]
    total_favorites: int