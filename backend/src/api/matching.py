"""Clinical trial matching API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging
import time

from ..database import get_db
from ..schemas.trial import TrialMatchResponse, TrialMatchListResponse, TrialResponse
from ..schemas.match import (
    MatchRequest,
    MatchResultsResponse,
    FavoriteRequest,
    FavoriteResponse,
    FavoriteListResponse
)
from ..services.matching_service import matching_service
from ..models.match import Match
from ..models.medical_profile import MedicalProfile

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/match", tags=["matching"])


# TODO: Replace with actual authentication dependency
def get_current_user_id() -> str:
    """Temporary mock function for user authentication."""
    return "temp-user-123"  # This should be replaced with actual JWT auth


@router.post("/", response_model=TrialMatchListResponse)
async def find_matching_trials(
    match_request: MatchRequest,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Find clinical trials that match the current user's medical profile.
    """
    try:
        start_time = time.time()
        
        # Check if user has a medical profile
        profile = db.query(MedicalProfile).filter(
            MedicalProfile.user_id == current_user_id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical profile not found. Please upload medical documents or create a profile first."
            )
        
        # Find matching trials
        matches = matching_service.find_matching_trials(
            db=db,
            user_id=current_user_id,
            filters=match_request.filters,
            limit=match_request.limit
        )
        
        # Convert to response format
        match_responses = []
        for match in matches:
            trial_response = TrialResponse.from_orm(match.trial)
            
            match_response = TrialMatchResponse(
                trial=trial_response,
                match_score=match.score,
                match_explanation=match.explanation,
                eligibility_summary=match.eligibility_summary,
                distance_km=match.distance_km
            )
            match_responses.append(match_response)
        
        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Build search criteria for response
        search_criteria = {
            "user_conditions": profile.conditions or [],
            "user_age": profile.age,
            "user_gender": profile.gender,
            "user_location": profile.location,
            "filters_applied": match_request.filters or {}
        }
        
        return TrialMatchListResponse(
            matches=match_responses,
            total_matches=len(match_responses),
            processing_time_ms=processing_time_ms,
            search_criteria=search_criteria
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to find matching trials for user {current_user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to find matching clinical trials"
        )


@router.get("/results", response_model=TrialMatchListResponse)
async def get_match_results(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get cached match results for the current user.
    For MVP, this will re-run the matching algorithm.
    In production, this would return cached results.
    """
    try:
        # For MVP, just re-run the matching
        match_request = MatchRequest(limit=limit)
        return await find_matching_trials(match_request, db, current_user_id)
        
    except Exception as e:
        logger.error(f"Failed to get match results for user {current_user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve match results"
        )


@router.post("/favorite", response_model=FavoriteResponse)
async def save_favorite_trial(
    favorite_request: FavoriteRequest,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Save a trial as favorite for the current user.
    """
    try:
        # Check if already favorited
        existing_favorite = db.query(Match).filter(
            Match.user_id == current_user_id,
            Match.trial_id == favorite_request.trial_id,
            Match.is_favorite == True
        ).first()
        
        if existing_favorite:
            return FavoriteResponse(
                message="Trial is already in favorites",
                trial_id=favorite_request.trial_id,
                is_favorite=True
            )
        
        # Check if match record exists
        match_record = db.query(Match).filter(
            Match.user_id == current_user_id,
            Match.trial_id == favorite_request.trial_id
        ).first()
        
        if match_record:
            # Update existing match record
            match_record.is_favorite = True
            match_record.match_explanation = favorite_request.match_explanation or match_record.match_explanation
            match_record.match_score = favorite_request.match_score or match_record.match_score
        else:
            # Create new match record
            match_record = Match(
                user_id=current_user_id,
                trial_id=favorite_request.trial_id,
                match_score=favorite_request.match_score or 0.0,
                match_explanation=favorite_request.match_explanation or "Manually favorited",
                is_favorite=True,
                status="viewed"
            )
            db.add(match_record)
        
        db.commit()
        
        return FavoriteResponse(
            message="Trial added to favorites",
            trial_id=favorite_request.trial_id,
            is_favorite=True
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save favorite trial for user {current_user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save trial as favorite"
        )


@router.get("/favorites", response_model=FavoriteListResponse)
async def get_favorite_trials(
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get all favorite trials for the current user.
    """
    try:
        # Get favorite matches with trial details
        favorites = db.query(Match).filter(
            Match.user_id == current_user_id,
            Match.is_favorite == True
        ).all()
        
        # Convert to response format
        favorite_responses = []
        for favorite in favorites:
            if favorite.trial:  # Ensure trial still exists
                trial_response = TrialResponse.from_orm(favorite.trial)
                
                match_response = TrialMatchResponse(
                    trial=trial_response,
                    match_score=favorite.match_score,
                    match_explanation=favorite.match_explanation,
                    eligibility_summary={
                        "met": ["Saved as favorite"],
                        "not_met": []
                    }
                )
                favorite_responses.append(match_response)
        
        return FavoriteListResponse(
            favorites=favorite_responses,
            total_favorites=len(favorite_responses)
        )
        
    except Exception as e:
        logger.error(f"Failed to get favorite trials for user {current_user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve favorite trials"
        )


@router.delete("/favorite/{trial_id}")
async def remove_favorite_trial(
    trial_id: str,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Remove a trial from favorites.
    """
    try:
        # Find the favorite match record
        match_record = db.query(Match).filter(
            Match.user_id == current_user_id,
            Match.trial_id == trial_id,
            Match.is_favorite == True
        ).first()
        
        if not match_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite trial not found"
            )
        
        # Remove from favorites (but keep the match record)
        match_record.is_favorite = False
        db.commit()
        
        return {
            "message": "Trial removed from favorites",
            "trial_id": trial_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to remove favorite trial for user {current_user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove trial from favorites"
        )