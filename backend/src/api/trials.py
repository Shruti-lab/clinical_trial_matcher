"""Clinical trials API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
import logging

from ..database import get_db
from ..models.clinical_trial import ClinicalTrial, TrialPhase, TrialStatus
from ..schemas.trial import (
    TrialResponse,
    TrialListResponse,
    TrialSearchRequest,
    TrialDetailResponse
)
from ..services.search_service import search_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trials", tags=["trials"])


@router.get("/", response_model=TrialListResponse)
async def search_trials(
    # Search parameters
    q: Optional[str] = Query(None, description="Search query for conditions, titles, descriptions"),
    condition: Optional[str] = Query(None, description="Search by medical condition"),
    location: Optional[str] = Query(None, description="Search by location (city, state)"),
    phase: Optional[str] = Query(None, description="Filter by trial phase (I, II, III, IV)"),
    status: Optional[str] = Query("recruiting", description="Filter by trial status"),
    
    # Age filters
    min_age: Optional[int] = Query(None, description="Minimum age requirement"),
    max_age: Optional[int] = Query(None, description="Maximum age requirement"),
    
    # Gender filter
    gender: Optional[str] = Query(None, description="Gender requirement (male, female, both)"),
    
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    
    db: Session = Depends(get_db)
):
    """
    Search clinical trials with full-text search and filters.
    """
    try:
        # Use the main search query or fall back to condition
        search_query = q or condition
        
        # Build filters
        filters = {}
        if status:
            filters['status'] = status
        if phase:
            filters['phase'] = phase
        if location:
            filters['location'] = location
        if min_age is not None:
            filters['min_age'] = min_age
        if max_age is not None:
            filters['max_age'] = max_age
        if gender:
            filters['gender'] = gender
        
        # Calculate pagination
        offset = (page - 1) * per_page
        
        # Perform search
        trials, total = search_service.search_trials(
            db=db,
            query=search_query,
            filters=filters,
            limit=per_page,
            offset=offset
        )
        
        # Convert to response format
        trial_responses = [TrialResponse.from_orm(trial) for trial in trials]
        
        return TrialListResponse(
            trials=trial_responses,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=(total + per_page - 1) // per_page
        )
        
    except Exception as e:
        logger.error(f"Failed to search trials: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search clinical trials"
        )


@router.get("/{trial_id}", response_model=TrialDetailResponse)
async def get_trial_by_id(
    trial_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific clinical trial.
    """
    try:
        trial = db.query(ClinicalTrial).filter(ClinicalTrial.id == trial_id).first()
        
        if not trial:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Clinical trial not found"
            )
        
        return TrialDetailResponse.from_orm(trial)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get trial {trial_id}: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve clinical trial"
        )


@router.get("/nearby/{latitude}/{longitude}")
async def get_nearby_trials(
    latitude: float,
    longitude: float,
    radius_km: int = Query(50, description="Search radius in kilometers"),
    condition: Optional[str] = Query(None, description="Filter by condition"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get clinical trials near a specific location using Haversine distance formula.
    Note: This is a simplified implementation. For production, consider using PostGIS.
    """
    try:
        # Haversine formula for distance calculation
        # This is a simplified version - for production use PostGIS
        lat_rad = func.radians(latitude)
        lon_rad = func.radians(longitude)
        trial_lat_rad = func.radians(ClinicalTrial.latitude)
        trial_lon_rad = func.radians(ClinicalTrial.longitude)
        
        # Calculate distance using Haversine formula
        distance = (
            6371 * func.acos(
                func.cos(lat_rad) * func.cos(trial_lat_rad) *
                func.cos(trial_lon_rad - lon_rad) +
                func.sin(lat_rad) * func.sin(trial_lat_rad)
            )
        )
        
        # Build query
        query = db.query(
            ClinicalTrial,
            distance.label('distance_km')
        ).filter(
            and_(
                ClinicalTrial.latitude.isnot(None),
                ClinicalTrial.longitude.isnot(None),
                ClinicalTrial.status == TrialStatus.RECRUITING
            )
        )
        
        # Add condition filter if provided
        if condition:
            query = query.filter(ClinicalTrial.condition_name.ilike(f"%{condition}%"))
        
        # Filter by radius and sort by distance
        results = query.having(distance <= radius_km).order_by(distance).limit(limit).all()
        
        # Format response
        nearby_trials = []
        for trial, distance_km in results:
            trial_data = TrialResponse.from_orm(trial).dict()
            trial_data['distance_km'] = round(distance_km, 2)
            nearby_trials.append(trial_data)
        
        return {
            "trials": nearby_trials,
            "search_center": {
                "latitude": latitude,
                "longitude": longitude
            },
            "radius_km": radius_km,
            "total_found": len(nearby_trials)
        }
        
    except Exception as e:
        logger.error(f"Failed to find nearby trials: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to find nearby clinical trials"
        )


@router.get("/conditions/autocomplete")
async def autocomplete_conditions(
    q: str = Query(..., min_length=2, description="Search query for conditions"),
    limit: int = Query(10, ge=1, le=20, description="Maximum number of suggestions"),
    db: Session = Depends(get_db)
):
    """
    Get autocomplete suggestions for medical conditions using enhanced search.
    """
    try:
        suggestions = search_service.get_condition_suggestions(
            db=db,
            query=q,
            limit=limit
        )
        
        return {
            "suggestions": suggestions,
            "query": q
        }
        
    except Exception as e:
        logger.error(f"Failed to get condition autocomplete: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get condition suggestions"
        )


@router.post("/{trial_id}/contact")
async def contact_trial(
    trial_id: str,
    db: Session = Depends(get_db)
):
    """
    Record that a user has contacted a trial coordinator.
    This is a placeholder for future implementation with user tracking.
    """
    try:
        trial = db.query(ClinicalTrial).filter(ClinicalTrial.id == trial_id).first()
        
        if not trial:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Clinical trial not found"
            )
        
        # For now, just return the contact information
        # In the future, this would track user interactions
        return {
            "message": "Contact information retrieved",
            "trial_id": trial_id,
            "contact": {
                "name": trial.contact_name,
                "email": trial.contact_email,
                "phone": trial.contact_phone,
                "principal_investigator": trial.principal_investigator
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get contact info for trial {trial_id}: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get trial contact information"
        )