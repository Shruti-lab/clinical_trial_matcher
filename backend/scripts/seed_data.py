#!/usr/bin/env python3
"""
Database seeding script for Clinical Trial Matcher.

Generates synthetic clinical trials and patient profiles for testing and demo purposes.
Covers major medical conditions relevant to Indian healthcare.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
import random
from uuid import uuid4

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database import SessionLocal, create_tables
from models import (
    User, MedicalProfile, ClinicalTrial, TrialPhase, TrialStatus,
    Match, MatchStatus, Document, ProcessingStatus
)
from sqlalchemy.exc import IntegrityError


class SeedDataGenerator:
    """Generates synthetic data for clinical trials and patient profiles."""
    
    def __init__(self):
        self.db = SessionLocal()
        
        # Major medical conditions for Indian healthcare context
        self.major_conditions = [
            "Type 2 Diabetes Mellitus",
            "Hypertension", 
            "Coronary Artery Disease",
            "Breast Cancer",
            "Lung Cancer",
            "Colorectal Cancer",
            "Chronic Kidney Disease",
            "Rheumatoid Arthritis",
            "Tuberculosis",
            "Chronic Obstructive Pulmonary Disease"
        ]
        
        # Indian cities with major medical centers
        self.indian_cities = [
            {"city": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lng": 72.8777},
            {"city": "Delhi", "state": "Delhi", "lat": 28.7041, "lng": 77.1025},
            {"city": "Bangalore", "state": "Karnataka", "lat": 12.9716, "lng": 77.5946},
            {"city": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lng": 80.2707},
            {"city": "Kolkata", "state": "West Bengal", "lat": 22.5726, "lng": 88.3639},
            {"city": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lng": 78.4867},
            {"city": "Pune", "state": "Maharashtra", "lat": 18.5204, "lng": 73.8567},
            {"city": "Ahmedabad", "state": "Gujarat", "lat": 23.0225, "lng": 72.5714},
            {"city": "Lucknow", "state": "Uttar Pradesh", "lat": 26.8467, "lng": 80.9462},
            {"city": "Chandigarh", "state": "Punjab", "lat": 30.7333, "lng": 76.7794}
        ]
        
        # Indian pharmaceutical companies and research institutions
        self.indian_sponsors = [
            "All India Institute of Medical Sciences (AIIMS)",
            "Tata Memorial Hospital",
            "Christian Medical College, Vellore",
            "Postgraduate Institute of Medical Education and Research",
            "Dr. Reddy's Laboratories",
            "Cipla Limited",
            "Sun Pharmaceutical Industries",
            "Lupin Limited",
            "Biocon Limited",
            "Cadila Healthcare",
            "Indian Council of Medical Research (ICMR)",
            "Sree Chitra Tirunal Institute",
            "Jawaharlal Institute of Postgraduate Medical Education"
        ]
        
        # Common medications for exclusion criteria
        self.common_medications = [
            "Warfarin", "Aspirin", "Metformin", "Insulin", "Atorvastatin",
            "Amlodipine", "Lisinopril", "Omeprazole", "Levothyroxine", "Metoprolol"
        ]
        
        # Sample patient names (anonymized)
        self.patient_names = [
            "Patient A", "Patient B", "Patient C", "Patient D", "Patient E",
            "Patient F", "Patient G", "Patient H", "Patient I", "Patient J"
        ]

    def generate_clinical_trials(self, count: int = 60) -> List[ClinicalTrial]:
        """Generate synthetic clinical trials covering major conditions."""
        trials = []
        
        for i in range(count):
            condition = random.choice(self.major_conditions)
            city_info = random.choice(self.indian_cities)
            sponsor = random.choice(self.indian_sponsors)
            phase = random.choice(list(TrialPhase))
            status = random.choice([TrialStatus.RECRUITING, TrialStatus.ACTIVE])
            
            # Generate CTRI ID (format: CTRI/YYYY/MM/XXXXXX)
            year = random.randint(2023, 2024)
            month = random.randint(1, 12)
            ctri_id = f"CTRI/{year}/{month:02d}/{random.randint(100000, 999999)}"
            
            # Generate trial title based on condition
            trial_title = self._generate_trial_title(condition, phase)
            
            # Generate eligibility criteria
            eligibility = self._generate_eligibility_criteria(condition)
            exclusion = self._generate_exclusion_criteria(condition)
            
            # Generate dates
            start_date = date.today() + timedelta(days=random.randint(-365, 180))
            completion_date = start_date + timedelta(days=random.randint(365, 1095))
            
            trial = ClinicalTrial(
                id=str(uuid4()),
                ctri_id=ctri_id,
                title=trial_title,
                condition=condition,
                phase=phase,
                status=status,
                description=self._generate_trial_description(condition, phase),
                primary_objective=self._generate_primary_objective(condition),
                secondary_objectives=self._generate_secondary_objectives(condition),
                eligibility_criteria=eligibility,
                exclusion_criteria=exclusion,
                min_age=eligibility.get("min_age", 18),
                max_age=eligibility.get("max_age", 75),
                gender_criteria=eligibility.get("gender", "Both"),
                location=f"{city_info['city']}, {city_info['state']}",
                city=city_info["city"],
                state=city_info["state"],
                latitude=city_info["lat"],
                longitude=city_info["lng"],
                sponsor=sponsor,
                principal_investigator=f"Dr. {random.choice(['Sharma', 'Patel', 'Kumar', 'Singh', 'Reddy'])}",
                contact_name=f"Dr. {random.choice(['Anil', 'Priya', 'Rajesh', 'Sunita', 'Vikram'])}",
                contact_email=f"contact{i+1}@{sponsor.lower().replace(' ', '').replace(',', '')}.in",
                contact_phone=f"+91-{random.randint(7000000000, 9999999999)}",
                start_date=start_date,
                estimated_completion=completion_date,
                study_type=random.choice(["Interventional", "Observational"]),
                intervention_type=random.choice(["Drug", "Device", "Behavioral", "Procedure"]),
                target_enrollment=random.randint(50, 500),
                keywords=self._generate_keywords(condition),
                source_url=f"http://ctri.nic.in/Clinicaltrials/pmaindet2.php?trialid={ctri_id}",
            )
            
            trials.append(trial)
        
        return trials

    def generate_patient_profiles(self, count: int = 10) -> List[tuple]:
        """Generate synthetic patient profiles with users."""
        profiles = []
        
        for i in range(count):
            # Create user
            user = User(
                id=str(uuid4()),
                email=f"patient{i+1}@example.com",
                phone=f"+91{random.randint(7000000000, 9999999999)}",
                password_hash="$2b$12$dummy_hash_for_testing",
                preferred_language=random.choice(["en", "hi", "ta", "te", "bn"])
            )
            
            # Generate realistic medical profile
            age = random.randint(25, 75)
            gender = random.choice(["Male", "Female"])
            condition = random.choice(self.major_conditions)
            
            medical_profile = MedicalProfile(
                id=str(uuid4()),
                user_id=user.id,
                age=age,
                gender=gender,
                location=random.choice(self.indian_cities)["city"],
                conditions=self._generate_patient_conditions(condition),
                medications=self._generate_patient_medications(condition),
                test_results=self._generate_test_results(condition),
                medical_history=self._generate_medical_history(condition, age),
                allergies=self._generate_allergies(),
                procedures=self._generate_procedures(condition)
            )
            
            profiles.append((user, medical_profile))
        
        return profiles

    def _generate_trial_title(self, condition: str, phase: TrialPhase) -> str:
        """Generate realistic trial title."""
        templates = [
            f"A {phase.value} Study of Novel Treatment for {condition}",
            f"{phase.value} Clinical Trial Evaluating Efficacy in {condition}",
            f"Randomized {phase.value} Study for Advanced {condition} Treatment",
            f"Multi-center {phase.value} Trial for {condition} Management",
            f"Double-blind {phase.value} Study in {condition} Patients"
        ]
        return random.choice(templates)

    def _generate_trial_description(self, condition: str, phase: TrialPhase) -> str:
        """Generate trial description."""
        descriptions = {
            "Type 2 Diabetes Mellitus": f"This {phase.value} study evaluates a novel glucose-lowering therapy in patients with inadequately controlled type 2 diabetes mellitus.",
            "Hypertension": f"A {phase.value} clinical trial investigating the efficacy and safety of a new antihypertensive agent in patients with essential hypertension.",
            "Coronary Artery Disease": f"This {phase.value} study assesses the cardiovascular outcomes of an innovative treatment approach in patients with stable coronary artery disease.",
            "Breast Cancer": f"A {phase.value} trial evaluating targeted therapy in patients with hormone receptor-positive breast cancer.",
            "Lung Cancer": f"This {phase.value} study investigates immunotherapy combinations in patients with advanced non-small cell lung cancer.",
            "Colorectal Cancer": f"A {phase.value} clinical trial of precision medicine approaches in metastatic colorectal cancer patients.",
            "Chronic Kidney Disease": f"This {phase.value} study evaluates renal protective therapy in patients with progressive chronic kidney disease.",
            "Rheumatoid Arthritis": f"A {phase.value} trial investigating biologic therapy in patients with moderate to severe rheumatoid arthritis.",
            "Tuberculosis": f"This {phase.value} study evaluates shortened treatment regimens for drug-sensitive pulmonary tuberculosis.",
            "Chronic Obstructive Pulmonary Disease": f"A {phase.value} trial of bronchodilator therapy in patients with moderate to severe COPD."
        }
        return descriptions.get(condition, f"A {phase.value} clinical trial for {condition}.")

    def _generate_primary_objective(self, condition: str) -> str:
        """Generate primary objective based on condition."""
        objectives = {
            "Type 2 Diabetes Mellitus": "To evaluate the efficacy of the investigational drug in reducing HbA1c levels compared to placebo.",
            "Hypertension": "To assess the antihypertensive efficacy in reducing systolic and diastolic blood pressure.",
            "Coronary Artery Disease": "To determine the effect on major adverse cardiovascular events (MACE).",
            "Breast Cancer": "To evaluate progression-free survival in patients receiving the investigational treatment.",
            "Lung Cancer": "To assess overall response rate and progression-free survival.",
            "Colorectal Cancer": "To evaluate overall survival in patients with metastatic disease.",
            "Chronic Kidney Disease": "To assess the rate of decline in estimated glomerular filtration rate (eGFR).",
            "Rheumatoid Arthritis": "To evaluate the proportion of patients achieving ACR20 response.",
            "Tuberculosis": "To assess the efficacy of shortened treatment duration on cure rates.",
            "Chronic Obstructive Pulmonary Disease": "To evaluate improvement in forced expiratory volume (FEV1)."
        }
        return objectives.get(condition, f"To evaluate the safety and efficacy of treatment for {condition}.")

    def _generate_secondary_objectives(self, condition: str) -> str:
        """Generate secondary objectives."""
        return "To assess safety and tolerability; To evaluate quality of life measures; To analyze biomarker responses; To assess long-term outcomes."

    def _generate_eligibility_criteria(self, condition: str) -> Dict[str, Any]:
        """Generate eligibility criteria based on condition."""
        base_criteria = {
            "min_age": 18,
            "max_age": 75,
            "gender": "Both"
        }
        
        condition_specific = {
            "Type 2 Diabetes Mellitus": {
                "min_age": 18, "max_age": 70, "gender": "Both",
                "conditions": ["Confirmed diagnosis of Type 2 Diabetes", "HbA1c ≥ 7.0%", "BMI 25-40 kg/m²"]
            },
            "Hypertension": {
                "min_age": 21, "max_age": 75, "gender": "Both",
                "conditions": ["Essential hypertension", "Systolic BP 140-180 mmHg", "Diastolic BP 90-110 mmHg"]
            },
            "Breast Cancer": {
                "min_age": 18, "max_age": 80, "gender": "Female",
                "conditions": ["Histologically confirmed breast cancer", "ER/PR positive", "HER2 negative"]
            },
            "Lung Cancer": {
                "min_age": 18, "max_age": 85, "gender": "Both",
                "conditions": ["Advanced NSCLC", "ECOG performance status 0-1", "Adequate organ function"]
            }
        }
        
        return condition_specific.get(condition, base_criteria)

    def _generate_exclusion_criteria(self, condition: str) -> List[str]:
        """Generate exclusion criteria."""
        base_exclusions = [
            "Pregnancy or breastfeeding",
            "Severe hepatic impairment",
            "Active malignancy (other than study indication)",
            "Uncontrolled psychiatric disorder"
        ]
        
        condition_exclusions = {
            "Type 2 Diabetes Mellitus": [
                "Type 1 diabetes", "Diabetic ketoacidosis", "Severe hypoglycemia in past 6 months"
            ],
            "Hypertension": [
                "Secondary hypertension", "Recent myocardial infarction", "Severe heart failure"
            ],
            "Breast Cancer": [
                "HER2 positive disease", "Brain metastases", "Prior chemotherapy for metastatic disease"
            ]
        }
        
        return base_exclusions + condition_exclusions.get(condition, [])

    def _generate_keywords(self, condition: str) -> List[str]:
        """Generate search keywords for the condition."""
        keyword_map = {
            "Type 2 Diabetes Mellitus": ["diabetes", "glucose", "insulin", "metformin", "HbA1c"],
            "Hypertension": ["blood pressure", "cardiovascular", "antihypertensive", "ACE inhibitor"],
            "Coronary Artery Disease": ["cardiac", "heart", "coronary", "cardiovascular", "chest pain"],
            "Breast Cancer": ["oncology", "cancer", "chemotherapy", "hormone therapy", "mastectomy"],
            "Lung Cancer": ["oncology", "pulmonary", "chemotherapy", "immunotherapy", "NSCLC"],
            "Colorectal Cancer": ["oncology", "gastrointestinal", "chemotherapy", "colonoscopy"],
            "Chronic Kidney Disease": ["nephrology", "kidney", "dialysis", "creatinine", "GFR"],
            "Rheumatoid Arthritis": ["rheumatology", "arthritis", "joint pain", "inflammation", "DMARDs"],
            "Tuberculosis": ["infectious disease", "pulmonary", "TB", "anti-TB drugs", "chest X-ray"],
            "Chronic Obstructive Pulmonary Disease": ["pulmonary", "COPD", "bronchodilator", "spirometry"]
        }
        return keyword_map.get(condition, ["clinical trial", "research"])

    def _generate_patient_conditions(self, primary_condition: str) -> List[str]:
        """Generate patient conditions including comorbidities."""
        conditions = [primary_condition]
        
        # Add common comorbidities
        comorbidities = {
            "Type 2 Diabetes Mellitus": ["Hypertension", "Dyslipidemia", "Obesity"],
            "Hypertension": ["Type 2 Diabetes Mellitus", "Dyslipidemia"],
            "Coronary Artery Disease": ["Hypertension", "Type 2 Diabetes Mellitus", "Dyslipidemia"],
            "Breast Cancer": ["Hypertension"],
            "Chronic Kidney Disease": ["Hypertension", "Type 2 Diabetes Mellitus"]
        }
        
        possible_comorbidities = comorbidities.get(primary_condition, [])
        if possible_comorbidities:
            conditions.extend(random.sample(possible_comorbidities, random.randint(0, 2)))
        
        return conditions

    def _generate_patient_medications(self, condition: str) -> List[str]:
        """Generate patient medications based on condition."""
        medication_map = {
            "Type 2 Diabetes Mellitus": ["Metformin 500mg", "Glimepiride 2mg", "Insulin Glargine"],
            "Hypertension": ["Amlodipine 5mg", "Lisinopril 10mg", "Hydrochlorothiazide 25mg"],
            "Coronary Artery Disease": ["Aspirin 75mg", "Atorvastatin 20mg", "Metoprolol 50mg"],
            "Breast Cancer": ["Tamoxifen 20mg", "Anastrozole 1mg"],
            "Rheumatoid Arthritis": ["Methotrexate 15mg", "Folic acid 5mg", "Prednisolone 5mg"]
        }
        
        base_meds = medication_map.get(condition, ["Paracetamol 500mg"])
        return random.sample(base_meds, random.randint(1, len(base_meds)))

    def _generate_test_results(self, condition: str) -> Dict[str, Any]:
        """Generate test results based on condition."""
        base_results = {
            "hemoglobin": round(random.uniform(10.0, 15.0), 1),
            "creatinine": round(random.uniform(0.8, 1.5), 2)
        }
        
        condition_results = {
            "Type 2 Diabetes Mellitus": {
                "hba1c": round(random.uniform(7.0, 10.0), 1),
                "fasting_glucose": random.randint(140, 250),
                "cholesterol": random.randint(180, 280)
            },
            "Hypertension": {
                "systolic_bp": random.randint(140, 180),
                "diastolic_bp": random.randint(90, 110)
            },
            "Breast Cancer": {
                "ca_15_3": random.randint(20, 100),
                "cea": round(random.uniform(2.0, 10.0), 1)
            }
        }
        
        base_results.update(condition_results.get(condition, {}))
        return base_results

    def _generate_medical_history(self, condition: str, age: int) -> List[str]:
        """Generate medical history based on condition and age."""
        history = []
        
        if age > 50:
            history.extend(["Hypertension diagnosed 5 years ago", "Regular health checkups"])
        
        condition_history = {
            "Type 2 Diabetes Mellitus": [
                "Diabetes diagnosed 3 years ago",
                "Family history of diabetes",
                "Previous gestational diabetes" if random.choice([True, False]) else None
            ],
            "Breast Cancer": [
                "Breast lump detected 6 months ago",
                "Family history of breast cancer",
                "Previous benign breast biopsy"
            ]
        }
        
        specific_history = condition_history.get(condition, [])
        history.extend([h for h in specific_history if h is not None])
        
        return history

    def _generate_allergies(self) -> List[str]:
        """Generate common allergies."""
        possible_allergies = ["Penicillin", "Sulfa drugs", "Aspirin", "Iodine", "Latex"]
        return random.sample(possible_allergies, random.randint(0, 2))

    def _generate_procedures(self, condition: str) -> List[str]:
        """Generate procedures based on condition."""
        procedure_map = {
            "Coronary Artery Disease": ["Coronary angiography", "Echocardiography"],
            "Breast Cancer": ["Mammography", "Breast biopsy", "CT scan chest"],
            "Lung Cancer": ["Chest CT scan", "Bronchoscopy", "PET scan"],
            "Chronic Kidney Disease": ["Renal ultrasound", "Kidney biopsy"]
        }
        
        procedures = procedure_map.get(condition, ["Routine blood tests"])
        return random.sample(procedures, random.randint(1, len(procedures)))

    def seed_database(self):
        """Main method to seed the database with all data."""
        try:
            print("🌱 Starting database seeding...")
            
            # Create tables if they don't exist
            create_tables()
            print("✅ Database tables verified")
            
            # Generate and insert clinical trials
            print("🏥 Generating clinical trials...")
            trials = self.generate_clinical_trials(60)
            
            for trial in trials:
                try:
                    self.db.add(trial)
                    self.db.commit()
                except IntegrityError:
                    self.db.rollback()
                    print(f"⚠️  Skipped duplicate trial: {trial.ctri_id}")
            
            print(f"✅ Created {len(trials)} clinical trials")
            
            # Generate and insert patient profiles
            print("👥 Generating patient profiles...")
            profiles = self.generate_patient_profiles(10)
            
            for user, medical_profile in profiles:
                try:
                    self.db.add(user)
                    self.db.commit()
                    self.db.add(medical_profile)
                    self.db.commit()
                except IntegrityError:
                    self.db.rollback()
                    print(f"⚠️  Skipped duplicate user: {user.email}")
            
            print(f"✅ Created {len(profiles)} patient profiles")
            
            print("🎉 Database seeding completed successfully!")
            print("\n📊 Summary:")
            print(f"   • Clinical Trials: {len(trials)}")
            print(f"   • Patient Profiles: {len(profiles)}")
            print(f"   • Medical Conditions: {len(self.major_conditions)}")
            print(f"   • Cities Covered: {len(self.indian_cities)}")
            
        except Exception as e:
            print(f"❌ Error during seeding: {str(e)}")
            self.db.rollback()
            raise
        finally:
            self.db.close()


if __name__ == "__main__":
    seeder = SeedDataGenerator()
    seeder.seed_database()