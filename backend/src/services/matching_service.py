"""Clinical trial matching service with multi-criteria scoring."""

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional, Tuple
import logging
import math
from datetime import datetime

from ..models.clinical_trial import ClinicalTrial, TrialStatus
from ..models.medical_profile import MedicalProfile
from ..services.search_service import search_service
from ..services.explanation_service import explanation_service
from ..database import get_db

logger = logging.getLogger(__name__)


class TrialMatch:
    """Represents a trial match with score and explanation."""
    
    def __init__(self, trial: ClinicalTrial, score: float, explanation: str, 
                 eligibility_summary: Dict[str, List[str]], distance_km: Optional[float] = None):
        self.trial = trial
        self.score = score
        self.explanation = explanation
        self.eligibility_summary = eligibility_summary
        self.distance_km = distance_km


class TrialMatchingService:
    """Service for matching patients with clinical trials."""
    
    def __init__(self):
        self.weights = {
            'condition_match': 0.4,    # 40% - Most important
            'eligibility': 0.3,        # 30% - Age, gender, basic criteria
            'exclusion': 0.2,          # 20% - Hard exclusions
            'location': 0.1            # 10% - Geographic proximity
        }
    
    def find_matching_trials(
        self,
        db: Session,
        user_id: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20
    ) -> List[TrialMatch]:
        """
        Find clinical trials that match a patient's medical profile.
        
        Args:
            db: Database session
            user_id: Patient's user ID
            filters: Additional filters (max_distance_km, phases, etc.)
            limit: Maximum number of matches to return
            
        Returns:
            List of TrialMatch objects sorted by score
        """
        try:
            # Get patient's medical profile
            profile = db.query(MedicalProfile).filter(
                MedicalProfile.user_id == user_id
            ).first()
            
            if not profile:
                logger.warning(f"No medical profile found for user {user_id}")
                return []
            
            # Get candidate trials (recruiting status by default)
            candidate_trials = self._get_candidate_trials(db, profile, filters)
            
            # Calculate match scores for each trial
            matches = []
            for trial in candidate_trials:
                match = self._calculate_match(profile, trial)
                if match.score > 0:  # Only include trials with some match
                    matches.append(match)
            
            # Sort by score (descending) and limit results
            matches.sort(key=lambda x: x.score, reverse=True)
            return matches[:limit]
            
        except Exception as e:
            logger.error(f"Error finding matching trials for user {user_id}: {str(e)}")
            raise
    
    def _get_candidate_trials(
        self,
        db: Session,
        profile: MedicalProfile,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ClinicalTrial]:
        """Get candidate trials for matching."""
        try:
            # Start with recruiting trials
            query = db.query(ClinicalTrial).filter(
                ClinicalTrial.status == TrialStatus.RECRUITING
            )
            
            # Apply basic filters
            if filters:
                # Phase filter
                if 'phases' in filters and filters['phases']:
                    query = query.filter(ClinicalTrial.phase.in_(filters['phases']))
                
                # Location filter (if max_distance_km specified, we'll filter later)
                if 'location' in filters and filters['location']:
                    location = filters['location']
                    query = query.filter(
                        ClinicalTrial.location.ilike(f"%{location}%") |
                        ClinicalTrial.city.ilike(f"%{location}%") |
                        ClinicalTrial.state.ilike(f"%{location}%")
                    )
            
            # If patient has conditions, prioritize trials for those conditions
            if profile.conditions:
                condition_trials = []
                for condition in profile.conditions:
                    # Use search service for better condition matching
                    trials, _ = search_service.search_trials(
                        db=db,
                        query=condition,
                        filters={'status': 'recruiting'},
                        limit=100,  # Get more candidates for better matching
                        offset=0
                    )
                    condition_trials.extend(trials)
                
                # Remove duplicates while preserving order
                seen = set()
                unique_trials = []
                for trial in condition_trials:
                    if trial.id not in seen:
                        seen.add(trial.id)
                        unique_trials.append(trial)
                
                return unique_trials
            
            # If no conditions, return general trials
            return query.limit(100).all()
            
        except Exception as e:
            logger.error(f"Error getting candidate trials: {str(e)}")
            return []
    
    def _calculate_match(self, profile: MedicalProfile, trial: ClinicalTrial) -> TrialMatch:
        """Calculate match score between patient profile and trial."""
        try:
            scores = {}
            eligibility_met = []
            eligibility_not_met = []
            
            # 1. Condition Matching (40% weight)
            condition_score, condition_details = self._score_condition_match(profile, trial)
            scores['condition'] = condition_score
            if condition_score > 0:
                eligibility_met.extend(condition_details.get('met', []))
            else:
                eligibility_not_met.extend(condition_details.get('not_met', []))
            
            # 2. Basic Eligibility (30% weight)
            eligibility_score, eligibility_details = self._score_eligibility(profile, trial)
            scores['eligibility'] = eligibility_score
            eligibility_met.extend(eligibility_details.get('met', []))
            eligibility_not_met.extend(eligibility_details.get('not_met', []))
            
            # 3. Exclusion Criteria (20% weight) - Hard fail if excluded
            exclusion_score, exclusion_details = self._score_exclusions(profile, trial)
            scores['exclusion'] = exclusion_score
            if exclusion_score == 0:
                # Hard exclusion - return zero score
                return TrialMatch(
                    trial=trial,
                    score=0.0,
                    explanation=f"Excluded due to: {', '.join(exclusion_details.get('excluded', []))}",
                    eligibility_summary={'met': [], 'not_met': exclusion_details.get('excluded', [])}
                )
            
            # 4. Location Proximity (10% weight)
            location_score, distance_km = self._score_location(profile, trial)
            scores['location'] = location_score
            
            # Calculate weighted final score
            final_score = (
                scores['condition'] * self.weights['condition_match'] +
                scores['eligibility'] * self.weights['eligibility'] +
                scores['exclusion'] * self.weights['exclusion'] +
                scores['location'] * self.weights['location']
            )
            
            # Generate explanation using explanation service
            explanation = explanation_service.generate_detailed_explanation(
                profile=profile,
                trial=trial,
                match_score=final_score,
                eligibility_summary={
                    'met': eligibility_met,
                    'not_met': eligibility_not_met
                }
            )
            
            return TrialMatch(
                trial=trial,
                score=min(100.0, final_score),  # Cap at 100
                explanation=explanation,
                eligibility_summary={
                    'met': eligibility_met,
                    'not_met': eligibility_not_met
                },
                distance_km=distance_km
            )
            
        except Exception as e:
            logger.error(f"Error calculating match for trial {trial.id}: {str(e)}")
            return TrialMatch(
                trial=trial,
                score=0.0,
                explanation="Error calculating match score",
                eligibility_summary={'met': [], 'not_met': ['Error in calculation']}
            )
    
    def _score_condition_match(self, profile: MedicalProfile, trial: ClinicalTrial) -> Tuple[float, Dict]:
        """Score condition matching between patient and trial."""
        if not profile.conditions:
            return 0.0, {'met': [], 'not_met': ['No conditions in profile']}
        
        best_score = 0.0
        best_match = None
        
        for patient_condition in profile.conditions:
            # Use fuzzy matching from search service
            match_score = search_service.fuzzy_match_condition(
                patient_condition, trial.condition
            )
            
            if match_score > best_score:
                best_score = match_score
                best_match = patient_condition
        
        # Convert to 0-100 scale
        score = best_score * 100
        
        details = {
            'met': [f"Condition match: {best_match} → {trial.condition} ({score:.0f}% match)"] if best_match else [],
            'not_met': [] if score > 30 else [f"Low condition match: {trial.condition}"]
        }
        
        return score, details
    
    def _score_eligibility(self, profile: MedicalProfile, trial: ClinicalTrial) -> Tuple[float, Dict]:
        """Score basic eligibility criteria."""
        score = 0.0
        met = []
        not_met = []
        total_criteria = 0
        
        # Age eligibility
        if trial.min_age is not None or trial.max_age is not None:
            total_criteria += 1
            if profile.age is not None:
                age_eligible = True
                
                if trial.min_age is not None and profile.age < trial.min_age:
                    age_eligible = False
                    not_met.append(f"Age {profile.age} below minimum {trial.min_age}")
                
                if trial.max_age is not None and profile.age > trial.max_age:
                    age_eligible = False
                    not_met.append(f"Age {profile.age} above maximum {trial.max_age}")
                
                if age_eligible:
                    score += 50  # 50 points for age eligibility
                    age_range = f"{trial.min_age or 'any'}-{trial.max_age or 'any'}"
                    met.append(f"Age {profile.age} meets requirement ({age_range})")
            else:
                not_met.append("Age not specified in profile")
        
        # Gender eligibility
        if trial.gender_criteria and trial.gender_criteria != 'both':
            total_criteria += 1
            if profile.gender:
                if profile.gender.lower() == trial.gender_criteria.lower():
                    score += 50  # 50 points for gender eligibility
                    met.append(f"Gender {profile.gender} matches requirement")
                else:
                    not_met.append(f"Gender {profile.gender} doesn't match requirement ({trial.gender_criteria})")
            else:
                not_met.append("Gender not specified in profile")
        elif trial.gender_criteria == 'both' or not trial.gender_criteria:
            # No gender restriction
            met.append("No gender restrictions")
        
        # If no specific criteria, give partial score
        if total_criteria == 0:
            score = 30  # Default score when no specific eligibility criteria
            met.append("No specific eligibility restrictions")
        
        return min(100.0, score), {'met': met, 'not_met': not_met}
    
    def _score_exclusions(self, profile: MedicalProfile, trial: ClinicalTrial) -> Tuple[float, Dict]:
        """Check exclusion criteria - returns 0 if excluded, 100 if not excluded."""
        if not trial.exclusion_criteria:
            return 100.0, {'excluded': []}
        
        excluded_reasons = []
        
        # Check each exclusion criterion
        for exclusion in trial.exclusion_criteria:
            exclusion_lower = exclusion.lower()
            
            # Check against patient conditions
            if profile.conditions:
                for condition in profile.conditions:
                    if condition.lower() in exclusion_lower or exclusion_lower in condition.lower():
                        excluded_reasons.append(f"Condition '{condition}' matches exclusion '{exclusion}'")
            
            # Check against medications
            if profile.medications:
                for medication in profile.medications:
                    if medication.lower() in exclusion_lower or exclusion_lower in medication.lower():
                        excluded_reasons.append(f"Medication '{medication}' matches exclusion '{exclusion}'")
        
        if excluded_reasons:
            return 0.0, {'excluded': excluded_reasons}
        
        return 100.0, {'excluded': []}
    
    def _score_location(self, profile: MedicalProfile, trial: ClinicalTrial) -> Tuple[float, Optional[float]]:
        """Score location proximity."""
        if not profile.location or not trial.latitude or not trial.longitude:
            return 50.0, None  # Default score when location data is incomplete
        
        # For MVP, use simple location string matching
        # In production, you'd use actual geocoding and distance calculation
        profile_location_lower = profile.location.lower()
        trial_location_lower = trial.location.lower()
        
        # Exact location match
        if profile_location_lower == trial_location_lower:
            return 100.0, 0.0
        
        # City/state match
        if (trial.city and trial.city.lower() in profile_location_lower) or \
           (trial.state and trial.state.lower() in profile_location_lower):
            return 80.0, 25.0  # Assume ~25km for same city/state
        
        # Partial match
        location_words = set(profile_location_lower.split())
        trial_words = set(trial_location_lower.split())
        
        if location_words.intersection(trial_words):
            return 60.0, 100.0  # Assume ~100km for partial match
        
        # No match
        return 20.0, 500.0  # Assume far distance
    
    def _generate_explanation(
        self,
        profile: MedicalProfile,
        trial: ClinicalTrial,
        scores: Dict[str, float],
        final_score: float
    ) -> str:
        """Generate human-readable explanation for the match."""
        try:
            explanation_parts = []
            
            # Overall match quality
            if final_score >= 80:
                explanation_parts.append("Excellent match")
            elif final_score >= 60:
                explanation_parts.append("Good match")
            elif final_score >= 40:
                explanation_parts.append("Moderate match")
            else:
                explanation_parts.append("Limited match")
            
            # Condition matching
            if scores['condition'] >= 80:
                explanation_parts.append("strong condition alignment")
            elif scores['condition'] >= 50:
                explanation_parts.append("good condition match")
            elif scores['condition'] > 0:
                explanation_parts.append("some condition relevance")
            
            # Eligibility
            if scores['eligibility'] >= 80:
                explanation_parts.append("meets eligibility criteria")
            elif scores['eligibility'] >= 50:
                explanation_parts.append("meets most eligibility requirements")
            
            # Location
            if scores['location'] >= 80:
                explanation_parts.append("convenient location")
            elif scores['location'] >= 50:
                explanation_parts.append("accessible location")
            
            # Combine parts
            if len(explanation_parts) > 1:
                explanation = f"{explanation_parts[0]} with {', '.join(explanation_parts[1:])}"
            else:
                explanation = explanation_parts[0] if explanation_parts else "Basic match"
            
            # Add trial phase info
            explanation += f" for this {trial.phase.value} trial"
            
            return explanation.capitalize() + "."
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return f"Match score: {final_score:.0f}%"


# Global instance
matching_service = TrialMatchingService()