"""Service for generating plain language explanations of trial matches."""

import logging
from typing import Dict, List, Any, Optional
import requests
import json

from ..models.clinical_trial import ClinicalTrial
from ..models.medical_profile import MedicalProfile
from ..config import settings

logger = logging.getLogger(__name__)


class ExplanationService:
    """Service for generating human-readable explanations of trial matches."""
    
    def __init__(self):
        self.settings = settings
        # For MVP, we'll use template-based explanations
        # In production, you could integrate with OpenAI API or other LLM services
        
    def generate_detailed_explanation(
        self,
        profile: MedicalProfile,
        trial: ClinicalTrial,
        match_score: float,
        eligibility_summary: Dict[str, List[str]]
    ) -> str:
        """
        Generate a detailed, human-readable explanation of why a trial matches a patient.
        
        Args:
            profile: Patient's medical profile
            trial: Clinical trial
            match_score: Calculated match score (0-100)
            eligibility_summary: Summary of met/unmet criteria
            
        Returns:
            Human-readable explanation string
        """
        try:
            # For MVP, use template-based approach
            return self._generate_template_explanation(
                profile, trial, match_score, eligibility_summary
            )
            
            # Future: Use LLM service
            # return self._generate_llm_explanation(profile, trial, match_score, eligibility_summary)
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return self._generate_fallback_explanation(match_score)
    
    def _generate_template_explanation(
        self,
        profile: MedicalProfile,
        trial: ClinicalTrial,
        match_score: float,
        eligibility_summary: Dict[str, List[str]]
    ) -> str:
        """Generate explanation using templates."""
        
        explanation_parts = []
        
        # Opening based on match score
        if match_score >= 80:
            explanation_parts.append("This trial is an excellent match for you.")
        elif match_score >= 60:
            explanation_parts.append("This trial is a good match for you.")
        elif match_score >= 40:
            explanation_parts.append("This trial may be suitable for you.")
        else:
            explanation_parts.append("This trial has limited relevance to your condition.")
        
        # Condition matching explanation
        if profile.conditions:
            primary_condition = profile.conditions[0]  # Use first condition as primary
            
            if trial.condition_name.lower() in primary_condition.lower() or primary_condition.lower() in trial.condition_name.lower():
                explanation_parts.append(
                    f"The trial focuses on {trial.condition_name.lower()}, which directly relates to your {primary_condition.lower()}."
                )
            else:
                # Check for related conditions
                related_terms = self._find_related_terms(primary_condition, trial.condition_name)
                if related_terms:
                    explanation_parts.append(
                        f"The trial studies {trial.condition_name.lower()}, which may be related to your {primary_condition.lower()} through {related_terms}."
                    )
                else:
                    explanation_parts.append(
                        f"While the trial focuses on {trial.condition_name.lower()}, it may still be relevant to your {primary_condition.lower()}."
                    )
        
        # Eligibility explanation
        met_criteria = eligibility_summary.get('met', [])
        not_met_criteria = eligibility_summary.get('not_met', [])
        
        if met_criteria:
            if len(met_criteria) == 1:
                explanation_parts.append(f"You meet the key requirement: {met_criteria[0].lower()}.")
            else:
                explanation_parts.append(f"You meet several important requirements including {met_criteria[0].lower()}.")
        
        if not_met_criteria:
            if len(not_met_criteria) == 1:
                explanation_parts.append(f"However, please note: {not_met_criteria[0].lower()}.")
            else:
                explanation_parts.append(f"Please note some requirements that may need clarification: {not_met_criteria[0].lower()}.")
        
        # Trial phase explanation
        phase_explanations = {
            "I": "This is a Phase I trial, which typically tests the safety of new treatments in a small group of people.",
            "II": "This is a Phase II trial, which studies how well the treatment works while continuing to monitor safety.",
            "III": "This is a Phase III trial, which compares the new treatment to standard treatments in a larger group of people.",
            "IV": "This is a Phase IV trial, which studies long-term effects of treatments already approved by regulatory authorities."
        }
        
        if trial.phase.value in phase_explanations:
            explanation_parts.append(phase_explanations[trial.phase.value])
        
        # Location information
        if trial.location:
            explanation_parts.append(f"The trial is being conducted at {trial.location}.")
        
        # Contact encouragement
        if match_score >= 50:
            explanation_parts.append(
                "We recommend discussing this trial with your healthcare provider to determine if it's right for you."
            )
        else:
            explanation_parts.append(
                "While this trial may not be a perfect match, it's worth discussing with your healthcare provider."
            )
        
        return " ".join(explanation_parts)
    
    def _find_related_terms(self, condition1: str, condition2: str) -> str:
        """Find related terms between two conditions."""
        # Simple keyword matching for related terms
        condition1_lower = condition1.lower()
        condition2_lower = condition2.lower()
        
        # Common medical term relationships
        relationships = {
            'cancer': ['tumor', 'carcinoma', 'malignancy', 'oncology', 'neoplasm'],
            'diabetes': ['blood sugar', 'glucose', 'insulin'],
            'heart': ['cardiac', 'cardiovascular', 'coronary'],
            'kidney': ['renal', 'nephrology'],
            'liver': ['hepatic', 'hepatitis'],
            'lung': ['pulmonary', 'respiratory'],
            'brain': ['neurological', 'cerebral'],
            'blood': ['hematology', 'hematologic']
        }
        
        for base_term, related_terms in relationships.items():
            if base_term in condition1_lower:
                for related in related_terms:
                    if related in condition2_lower:
                        return f"shared {base_term}-related pathways"
            
            if base_term in condition2_lower:
                for related in related_terms:
                    if related in condition1_lower:
                        return f"shared {base_term}-related pathways"
        
        # Check for common words
        words1 = set(condition1_lower.split())
        words2 = set(condition2_lower.split())
        common_words = words1.intersection(words2)
        
        # Filter out common stop words
        stop_words = {'the', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
        meaningful_common = [word for word in common_words if word not in stop_words and len(word) > 2]
        
        if meaningful_common:
            return f"common medical terminology ({', '.join(meaningful_common)})"
        
        return ""
    
    def _generate_llm_explanation(
        self,
        profile: MedicalProfile,
        trial: ClinicalTrial,
        match_score: float,
        eligibility_summary: Dict[str, List[str]]
    ) -> str:
        """
        Generate explanation using LLM service (OpenAI API).
        This is for future implementation when budget allows.
        """
        try:
            # This would be implemented when integrating with OpenAI API
            # For now, fall back to template explanation
            return self._generate_template_explanation(profile, trial, match_score, eligibility_summary)
            
            # Example implementation:
            # prompt = self._build_llm_prompt(profile, trial, match_score, eligibility_summary)
            # response = self._call_openai_api(prompt)
            # return response
            
        except Exception as e:
            logger.error(f"Error with LLM explanation: {str(e)}")
            return self._generate_template_explanation(profile, trial, match_score, eligibility_summary)
    
    def _build_llm_prompt(
        self,
        profile: MedicalProfile,
        trial: ClinicalTrial,
        match_score: float,
        eligibility_summary: Dict[str, List[str]]
    ) -> str:
        """Build prompt for LLM explanation generation."""
        
        prompt = f"""
        Explain why this clinical trial matches a patient in simple, compassionate language.
        
        Patient Profile:
        - Age: {profile.age or 'Not specified'}
        - Gender: {profile.gender or 'Not specified'}
        - Conditions: {', '.join(profile.conditions) if profile.conditions else 'None specified'}
        - Medications: {', '.join(profile.medications) if profile.medications else 'None specified'}
        - Location: {profile.location or 'Not specified'}
        
        Clinical Trial:
        - Title: {trial.title}
        - Condition: {trial.condition_name}
        - Phase: {trial.phase.value}
        - Location: {trial.location}
        - Description: {trial.description or 'Not provided'}
        
        Match Score: {match_score:.0f}%
        
        Eligibility Met: {', '.join(eligibility_summary.get('met', []))}
        Eligibility Not Met: {', '.join(eligibility_summary.get('not_met', []))}
        
        Please provide a 2-3 sentence explanation in simple language that:
        1. Explains why this trial matches the patient
        2. Mentions key eligibility factors
        3. Encourages discussion with healthcare provider
        4. Is compassionate and hopeful in tone
        
        Explanation:
        """
        
        return prompt.strip()
    
    def _call_openai_api(self, prompt: str) -> str:
        """Call OpenAI API for explanation generation."""
        # This would be implemented when integrating with OpenAI
        # For now, return template explanation
        return "OpenAI integration not implemented yet."
    
    def _generate_fallback_explanation(self, match_score: float) -> str:
        """Generate a simple fallback explanation."""
        if match_score >= 70:
            return "This trial appears to be a good match for your medical profile. Please discuss with your healthcare provider."
        elif match_score >= 40:
            return "This trial may be relevant to your condition. We recommend discussing it with your healthcare provider."
        else:
            return "While this trial may not be a perfect match, it could still be worth discussing with your healthcare provider."
    
    def generate_eligibility_explanation(self, eligibility_criteria: Dict[str, Any]) -> str:
        """Generate human-readable explanation of eligibility criteria."""
        try:
            if not eligibility_criteria:
                return "No specific eligibility criteria listed."
            
            explanations = []
            
            # Age criteria
            if 'min_age' in eligibility_criteria or 'max_age' in eligibility_criteria:
                min_age = eligibility_criteria.get('min_age')
                max_age = eligibility_criteria.get('max_age')
                
                if min_age and max_age:
                    explanations.append(f"Participants must be between {min_age} and {max_age} years old")
                elif min_age:
                    explanations.append(f"Participants must be at least {min_age} years old")
                elif max_age:
                    explanations.append(f"Participants must be no older than {max_age} years")
            
            # Gender criteria
            if 'gender' in eligibility_criteria:
                gender = eligibility_criteria['gender']
                if gender and gender != 'both':
                    explanations.append(f"This trial is open to {gender} participants only")
            
            # Other criteria
            if 'conditions' in eligibility_criteria:
                conditions = eligibility_criteria['conditions']
                if isinstance(conditions, list) and conditions:
                    explanations.append(f"Participants must have: {', '.join(conditions)}")
            
            return ". ".join(explanations) + "." if explanations else "Please contact the trial coordinator for detailed eligibility requirements."
            
        except Exception as e:
            logger.error(f"Error generating eligibility explanation: {str(e)}")
            return "Please contact the trial coordinator for eligibility requirements."


# Global instance
explanation_service = ExplanationService()