#!/usr/bin/env python3
"""
Script for generating diverse synthetic patient profiles for testing.
Creates realistic medical profiles covering various demographics and conditions.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Tuple
import random
from uuid import uuid4

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database import SessionLocal
from models import User, MedicalProfile
from sqlalchemy.exc import IntegrityError


class PatientGenerator:
    """Generates diverse synthetic patient profiles for testing matching algorithms."""
    
    def __init__(self):
        self.db = SessionLocal()
        
        # Indian demographics and regional diversity
        self.indian_regions = {
            "North": {
                "cities": ["Delhi", "Chandigarh", "Lucknow", "Jaipur", "Amritsar"],
                "languages": ["hi", "pa", "ur"]
            },
            "South": {
                "cities": ["Chennai", "Bangalore", "Hyderabad", "Kochi", "Thiruvananthapuram"],
                "languages": ["ta", "te", "kn", "ml"]
            },
            "West": {
                "cities": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Indore"],
                "languages": ["hi", "gu", "mr"]
            },
            "East": {
                "cities": ["Kolkata", "Bhubaneswar", "Guwahati", "Patna"],
                "languages": ["bn", "hi", "as", "or"]
            }
        }
        
        # Age-based condition prevalence (realistic for Indian population)
        self.age_condition_mapping = {
            "young_adult": {  # 18-35
                "conditions": ["Type 1 Diabetes Mellitus", "Asthma", "Depression", "Anxiety Disorders", "Tuberculosis"],
                "weight": [0.1, 0.3, 0.2, 0.2, 0.2]
            },
            "middle_aged": {  # 36-55
                "conditions": ["Type 2 Diabetes Mellitus", "Hypertension", "Breast Cancer", "Coronary Artery Disease", "Rheumatoid Arthritis"],
                "weight": [0.3, 0.3, 0.1, 0.2, 0.1]
            },
            "senior": {  # 56+
                "conditions": ["Type 2 Diabetes Mellitus", "Hypertension", "Coronary Artery Disease", "COPD", "Stroke"],
                "weight": [0.3, 0.4, 0.2, 0.05, 0.05]
            }
        }
        
        # Gender-specific conditions
        self.gender_conditions = {
            "Female": ["Breast Cancer", "Cervical Cancer", "Osteoporosis", "Gestational Diabetes"],
            "Male": ["Prostate Cancer", "Coronary Artery Disease"],
            "Both": ["Type 2 Diabetes Mellitus", "Hypertension", "Lung Cancer", "Tuberculosis"]
        }
        
        # Socioeconomic factors affecting health (Indian context)
        self.socioeconomic_profiles = {
            "urban_affluent": {
                "conditions": ["Type 2 Diabetes Mellitus", "Hypertension", "Coronary Artery Disease"],
                "medications": ["branded", "multiple"],
                "test_frequency": "regular"
            },
            "urban_middle": {
                "conditions": ["Type 2 Diabetes Mellitus", "Hypertension", "Asthma"],
                "medications": ["generic", "essential"],
                "test_frequency": "periodic"
            },
            "rural": {
                "conditions": ["Tuberculosis", "Hypertension", "Type 2 Diabetes Mellitus"],
                "medications": ["basic", "government"],
                "test_frequency": "irregular"
            }
        }

    def generate_diverse_patients(self, count: int = 20) -> List[Tuple[User, MedicalProfile]]:
        """Generate diverse patient profiles representing Indian demographics."""
        patients = []
        
        for i in range(count):
            # Determine demographics
            age = self._generate_realistic_age()
            gender = random.choice(["Male", "Female"])
            region = random.choice(list(self.indian_regions.keys()))
            city = random.choice(self.indian_regions[region]["cities"])
            language = random.choice(self.indian_regions[region]["languages"])
            socioeconomic = random.choice(list(self.socioeconomic_profiles.keys()))
            
            # Create user
            user = User(
                id=str(uuid4()),
                email=f"testpatient{i+1}@example.com",
                phone=f"+91{random.randint(7000000000, 9999999999)}",
                password_hash="$2b$12$dummy_hash_for_testing_only",
                preferred_language=language
            )
            
            # Generate medical profile based on demographics
            medical_profile = self._create_medical_profile(
                user.id, age, gender, city, socioeconomic
            )
            
            patients.append((user, medical_profile))
        
        return patients

    def generate_condition_specific_patients(self, condition: str, count: int = 5) -> List[Tuple[User, MedicalProfile]]:
        """Generate patients with specific medical condition for targeted testing."""
        patients = []
        
        for i in range(count):
            age = self._get_typical_age_for_condition(condition)
            gender = self._get_typical_gender_for_condition(condition)
            region = random.choice(list(self.indian_regions.keys()))
            city = random.choice(self.indian_regions[region]["cities"])
            language = random.choice(self.indian_regions[region]["languages"])
            
            user = User(
                id=str(uuid4()),
                email=f"{condition.lower().replace(' ', '')}patient{i+1}@example.com",
                phone=f"+91{random.randint(7000000000, 9999999999)}",
                password_hash="$2b$12$dummy_hash_for_testing_only",
                preferred_language=language
            )
            
            medical_profile = self._create_condition_specific_profile(
                user.id, condition, age, gender, city
            )
            
            patients.append((user, medical_profile))
        
        return patients

    def _generate_realistic_age(self) -> int:
        """Generate age following Indian population distribution."""
        # Weighted age distribution reflecting Indian demographics
        age_ranges = [(18, 35), (36, 55), (56, 75)]
        weights = [0.5, 0.3, 0.2]  # Younger population in India
        
        selected_range = random.choices(age_ranges, weights=weights)[0]
        return random.randint(*selected_range)

    def _get_age_category(self, age: int) -> str:
        """Categorize age for condition mapping."""
        if age <= 35:
            return "young_adult"
        elif age <= 55:
            return "middle_aged"
        else:
            return "senior"

    def _get_typical_age_for_condition(self, condition: str) -> int:
        """Get typical age range for specific condition."""
        age_mapping = {
            "Type 1 Diabetes Mellitus": random.randint(18, 35),
            "Type 2 Diabetes Mellitus": random.randint(40, 70),
            "Breast Cancer": random.randint(40, 65),
            "Prostate Cancer": random.randint(55, 75),
            "Hypertension": random.randint(35, 70),
            "Coronary Artery Disease": random.randint(45, 75),
            "Tuberculosis": random.randint(20, 50),
            "COPD": random.randint(50, 75),
            "Asthma": random.randint(18, 60),
            "Depression": random.randint(20, 50)
        }
        return age_mapping.get(condition, random.randint(30, 60))

    def _get_typical_gender_for_condition(self, condition: str) -> str:
        """Get typical gender for condition (or random if both)."""
        if condition in self.gender_conditions["Female"]:
            return "Female"
        elif condition in self.gender_conditions["Male"]:
            return "Male"
        else:
            return random.choice(["Male", "Female"])

    def _create_medical_profile(self, user_id: str, age: int, gender: str, city: str, socioeconomic: str) -> MedicalProfile:
        """Create comprehensive medical profile based on demographics."""
        age_category = self._get_age_category(age)
        
        # Select primary condition based on age and demographics
        condition_data = self.age_condition_mapping[age_category]
        primary_condition = random.choices(
            condition_data["conditions"], 
            weights=condition_data["weight"]
        )[0]
        
        # Adjust for gender-specific conditions
        if gender == "Female" and random.random() < 0.3:
            female_conditions = [c for c in self.gender_conditions["Female"] if c != primary_condition]
            if female_conditions:
                primary_condition = random.choice(female_conditions)
        
        return MedicalProfile(
            id=str(uuid4()),
            user_id=user_id,
            age=age,
            gender=gender,
            location=city,
            conditions=self._generate_conditions_with_comorbidities(primary_condition, age, socioeconomic),
            medications=self._generate_realistic_medications(primary_condition, socioeconomic),
            test_results=self._generate_comprehensive_test_results(primary_condition, age),
            medical_history=self._generate_detailed_medical_history(primary_condition, age),
            allergies=self._generate_realistic_allergies(),
            procedures=self._generate_relevant_procedures(primary_condition)
        )

    def _create_condition_specific_profile(self, user_id: str, condition: str, age: int, gender: str, city: str) -> MedicalProfile:
        """Create medical profile optimized for specific condition testing."""
        return MedicalProfile(
            id=str(uuid4()),
            user_id=user_id,
            age=age,
            gender=gender,
            location=city,
            conditions=self._generate_conditions_with_comorbidities(condition, age, "urban_middle"),
            medications=self._generate_condition_specific_medications(condition),
            test_results=self._generate_condition_specific_tests(condition, age),
            medical_history=self._generate_detailed_medical_history(condition, age),
            allergies=self._generate_realistic_allergies(),
            procedures=self._generate_relevant_procedures(condition)
        )

    def _generate_conditions_with_comorbidities(self, primary_condition: str, age: int, socioeconomic: str) -> List[str]:
        """Generate realistic comorbidities based on primary condition."""
        conditions = [primary_condition]
        
        # Common comorbidity patterns in Indian population
        comorbidity_map = {
            "Type 2 Diabetes Mellitus": ["Hypertension", "Dyslipidemia", "Obesity", "Diabetic Nephropathy"],
            "Hypertension": ["Type 2 Diabetes Mellitus", "Dyslipidemia", "Coronary Artery Disease"],
            "Coronary Artery Disease": ["Hypertension", "Type 2 Diabetes Mellitus", "Dyslipidemia"],
            "Breast Cancer": ["Hypertension", "Osteoporosis"],
            "COPD": ["Hypertension", "Coronary Artery Disease", "Depression"],
            "Chronic Kidney Disease": ["Hypertension", "Type 2 Diabetes Mellitus", "Anemia"],
            "Rheumatoid Arthritis": ["Osteoporosis", "Depression", "Cardiovascular Disease"]
        }
        
        possible_comorbidities = comorbidity_map.get(primary_condition, [])
        
        # Age increases comorbidity likelihood
        comorbidity_probability = min(0.8, 0.2 + (age - 30) * 0.02)
        
        for comorbidity in possible_comorbidities:
            if random.random() < comorbidity_probability:
                conditions.append(comorbidity)
        
        return conditions

    def _generate_realistic_medications(self, condition: str, socioeconomic: str) -> List[str]:
        """Generate realist