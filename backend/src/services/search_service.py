"""Search service for clinical trials using MySQL full-text search."""

from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_
from typing import List, Dict, Any, Optional, Tuple
import logging
import re

from ..models.clinical_trial import ClinicalTrial, TrialStatus
from ..database import get_db

logger = logging.getLogger(__name__)


class TrialSearchService:
    """Service for searching clinical trials using MySQL full-text search and fuzzy matching."""
    
    def __init__(self):
        self.condition_synonyms = {
            # Cancer synonyms
            'cancer': ['carcinoma', 'tumor', 'tumour', 'malignancy', 'oncology', 'neoplasm'],
            'breast cancer': ['breast carcinoma', 'mammary cancer', 'breast tumor'],
            'lung cancer': ['pulmonary cancer', 'lung carcinoma', 'bronchogenic carcinoma'],
            'colon cancer': ['colorectal cancer', 'bowel cancer', 'rectal cancer'],
            
            # Heart conditions
            'heart disease': ['cardiac disease', 'coronary disease', 'cardiovascular disease'],
            'heart attack': ['myocardial infarction', 'mi', 'cardiac arrest'],
            
            # Diabetes
            'diabetes': ['diabetic', 'blood sugar', 'glucose intolerance'],
            'type 1 diabetes': ['t1d', 'juvenile diabetes', 'insulin dependent diabetes'],
            'type 2 diabetes': ['t2d', 'adult onset diabetes', 'non-insulin dependent diabetes'],
            
            # Other common conditions
            'high blood pressure': ['hypertension', 'elevated bp', 'high bp'],
            'kidney disease': ['renal disease', 'nephropathy', 'kidney failure'],
            'liver disease': ['hepatic disease', 'cirrhosis', 'hepatitis'],
        }
    
    def search_trials(
        self,
        db: Session,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[ClinicalTrial], int]:
        """
        Search clinical trials using text search and filters.
        
        Args:
            db: Database session
            query: Search query string
            filters: Additional filters (status, phase, location, etc.)
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            Tuple of (trials, total_count)
        """
        try:
            # Build base query
            base_query = db.query(ClinicalTrial)
            
            # Apply text search if query provided
            if query and query.strip():
                search_conditions = self._build_search_conditions(query.strip())
                base_query = base_query.filter(search_conditions)
            
            # Apply additional filters
            if filters:
                filter_conditions = self._build_filter_conditions(filters)
                if filter_conditions is not None:
                    base_query = base_query.filter(filter_conditions)
            
            # Get total count
            total_count = base_query.count()
            
            # Apply ordering (relevance-based if search query, otherwise by date)
            if query and query.strip():
                # Simple relevance scoring based on title matches
                base_query = base_query.order_by(
                    ClinicalTrial.title.ilike(f"%{query}%").desc(),
                    ClinicalTrial.updated_at.desc()
                )
            else:
                base_query = base_query.order_by(ClinicalTrial.updated_at.desc())
            
            # Apply pagination
            trials = base_query.offset(offset).limit(limit).all()
            
            return trials, total_count
            
        except Exception as e:
            logger.error(f"Error in trial search: {str(e)}")
            raise
    
    def _build_search_conditions(self, query: str):
        """Build search conditions for the query string."""
        search_terms = self._extract_search_terms(query)
        conditions = []
        
        for term in search_terms:
            # Get synonyms for the term
            synonyms = self._get_synonyms(term)
            all_terms = [term] + synonyms
            
            # Create OR conditions for each field
            term_conditions = []
            for search_term in all_terms:
                term_conditions.extend([
                    ClinicalTrial.title.ilike(f"%{search_term}%"),
                    ClinicalTrial.condition_name.ilike(f"%{search_term}%"),
                    ClinicalTrial.description.ilike(f"%{search_term}%"),
                    ClinicalTrial.primary_objective.ilike(f"%{search_term}%")
                ])
            
            # Add condition for this term (OR of all fields and synonyms)
            if term_conditions:
                conditions.append(or_(*term_conditions))
        
        # Return AND of all term conditions
        return and_(*conditions) if conditions else None
    
    def _extract_search_terms(self, query: str) -> List[str]:
        """Extract meaningful search terms from query string."""
        # Remove special characters and split
        clean_query = re.sub(r'[^\w\s]', ' ', query.lower())
        terms = clean_query.split()
        
        # Remove common stop words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
        meaningful_terms = [term for term in terms if term not in stop_words and len(term) > 2]
        
        return meaningful_terms
    
    def _get_synonyms(self, term: str) -> List[str]:
        """Get synonyms for a search term."""
        term_lower = term.lower()
        
        # Direct lookup
        if term_lower in self.condition_synonyms:
            return self.condition_synonyms[term_lower]
        
        # Check if term is a synonym of any key
        for key, synonyms in self.condition_synonyms.items():
            if term_lower in synonyms:
                return [key] + [s for s in synonyms if s != term_lower]
        
        return []
    
    def _build_filter_conditions(self, filters: Dict[str, Any]):
        """Build filter conditions from filter dictionary."""
        conditions = []
        
        # Status filter
        if 'status' in filters and filters['status']:
            try:
                status_enum = TrialStatus(filters['status'].lower())
                conditions.append(ClinicalTrial.status == status_enum)
            except ValueError:
                pass
        
        # Phase filter
        if 'phase' in filters and filters['phase']:
            conditions.append(ClinicalTrial.phase == filters['phase'].upper())
        
        # Location filter
        if 'location' in filters and filters['location']:
            location = filters['location']
            location_condition = or_(
                ClinicalTrial.location.ilike(f"%{location}%"),
                ClinicalTrial.city.ilike(f"%{location}%"),
                ClinicalTrial.state.ilike(f"%{location}%")
            )
            conditions.append(location_condition)
        
        # Age filters
        if 'min_age' in filters and filters['min_age'] is not None:
            conditions.append(
                or_(
                    ClinicalTrial.max_age.is_(None),
                    ClinicalTrial.max_age >= filters['min_age']
                )
            )
        
        if 'max_age' in filters and filters['max_age'] is not None:
            conditions.append(
                or_(
                    ClinicalTrial.min_age.is_(None),
                    ClinicalTrial.min_age <= filters['max_age']
                )
            )
        
        # Gender filter
        if 'gender' in filters and filters['gender']:
            gender = filters['gender'].lower()
            if gender in ['male', 'female']:
                conditions.append(
                    or_(
                        ClinicalTrial.gender_criteria.is_(None),
                        ClinicalTrial.gender_criteria == 'both',
                        ClinicalTrial.gender_criteria == gender
                    )
                )
        
        return and_(*conditions) if conditions else None
    
    def get_condition_suggestions(self, db: Session, query: str, limit: int = 10) -> List[str]:
        """Get autocomplete suggestions for medical conditions."""
        try:
            if not query or len(query) < 2:
                return []
            
            # Search in conditions
            conditions = db.query(ClinicalTrial.condition_name).filter(
                ClinicalTrial.condition_name.ilike(f"%{query}%")
            ).distinct().limit(limit * 2).all()  # Get more to filter
            
            # Extract unique conditions
            unique_conditions = list(set([c[0] for c in conditions if c[0]]))
            
            # Sort by relevance (starts with query first, then contains)
            query_lower = query.lower()
            starts_with = [c for c in unique_conditions if c.lower().startswith(query_lower)]
            contains = [c for c in unique_conditions if query_lower in c.lower() and not c.lower().startswith(query_lower)]
            
            # Combine and limit
            suggestions = (starts_with + contains)[:limit]
            
            # Add synonym suggestions
            for condition, synonyms in self.condition_synonyms.items():
                if query_lower in condition or any(query_lower in syn for syn in synonyms):
                    if condition not in [s.lower() for s in suggestions]:
                        suggestions.append(condition.title())
            
            return suggestions[:limit]
            
        except Exception as e:
            logger.error(f"Error getting condition suggestions: {str(e)}")
            return []
    
    def fuzzy_match_condition(self, patient_condition: str, trial_condition: str) -> float:
        """
        Calculate fuzzy match score between patient condition and trial condition.
        Returns score between 0 and 1.
        """
        try:
            patient_lower = patient_condition.lower().strip()
            trial_lower = trial_condition.lower().strip()
            
            # Exact match
            if patient_lower == trial_lower:
                return 1.0
            
            # Check if one contains the other
            if patient_lower in trial_lower or trial_lower in patient_lower:
                return 0.8
            
            # Check synonyms
            patient_synonyms = self._get_synonyms(patient_lower)
            trial_synonyms = self._get_synonyms(trial_lower)
            
            # Check if trial condition matches patient synonyms
            if trial_lower in patient_synonyms:
                return 0.9
            
            # Check if patient condition matches trial synonyms
            if patient_lower in trial_synonyms:
                return 0.9
            
            # Check if any synonyms match
            for p_syn in patient_synonyms:
                if p_syn in trial_lower or trial_lower in p_syn:
                    return 0.7
                for t_syn in trial_synonyms:
                    if p_syn == t_syn:
                        return 0.8
            
            # Simple word overlap
            patient_words = set(patient_lower.split())
            trial_words = set(trial_lower.split())
            
            if patient_words and trial_words:
                overlap = len(patient_words.intersection(trial_words))
                total_words = len(patient_words.union(trial_words))
                if total_words > 0:
                    return overlap / total_words * 0.6
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error in fuzzy matching: {str(e)}")
            return 0.0


# Global instance
search_service = TrialSearchService()