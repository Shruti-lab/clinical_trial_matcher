#!/usr/bin/env python3
"""
Focused script for generating additional clinical trials.
Can be used to add more trials to existing database.
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

from database import SessionLocal
from models import ClinicalTrial, TrialPhase, TrialStatus
from sqlalchemy.exc import IntegrityError


class TrialGenerator:
    """Specialized generator for clinical trials with Indian healthcare focus."""
    
    def __init__(self):
        self.db = SessionLocal()
        
        # Expanded conditions with subcategories
        self.conditions_detailed = {
            "Diabetes": [
                "Type 2 Diabetes Mellitus",
                "Type 1 Diabetes Mellitus", 
                "Gestational Diabetes",
                "Diabetic Nephropathy",
                "Diabetic Retinopathy"
            ],
            "Cancer": [
                "Breast Cancer",
                "Lung Cancer", 
                "Colorectal Cancer",
                "Cervical Cancer",
                "Oral Cancer",
                "Stomach Cancer",
                "Liver Cancer",
                "Prostate Cancer"
            ],
            "Cardiovascular": [
                "Coronary Artery Disease",
                "Hypertension",
                "Heart Failure",
                "Atrial Fibrillation",
                "Peripheral Artery Disease"
            ],
            "Respiratory": [
                "Chronic Obstructive Pulmonary Disease",
                "Asthma",
                "Tuberculosis",
                "Pneumonia",
                "Lung Fibrosis"
            ],
            "Neurological": [
                "Stroke",
                "Epilepsy", 
                "Parkinson's Disease",
                "Alzheimer's Disease",
                "Multiple Sclerosis"
            ],
            "Infectious": [
                "Tuberculosis",
                "Hepatitis B",
                "Hepatitis C", 
                "HIV/AIDS",
                "Malaria"
            ],
            "Autoimmune": [
                "Rheumatoid Arthritis",
                "Systemic Lupus Erythematosus",
                "Inflammatory Bowel Disease",
                "Psoriasis",
                "Multiple Sclerosis"
            ],
            "Renal": [
                "Chronic Kidney Disease",
                "Acute Kidney Injury",
                "Diabetic Nephropathy",
                "Glomerulonephritis",
                "Kidney Stones"
            ],
            "Mental Health": [
                "Depression",
                "Anxiety Disorders",
                "Bipolar Disorder",
                "Schizophrenia",
                "PTSD"
            ],
            "Rare Diseases": [
                "Thalassemia",
                "Sickle Cell Disease",
                "Hemophilia",
                "Muscular Dystrophy",
                "Cystic Fibrosis"
            ]
        }
        
        # Premier Indian medical institutions
        self.premier_institutions = [
            "All India Institute of Medical Sciences (AIIMS), New Delhi",
            "All India Institute of Medical Sciences (AIIMS), Mumbai", 
            "Tata Memorial Hospital, Mumbai",
            "Christian Medical College, Vellore",
            "Postgraduate Institute of Medical Education and Research, Chandigarh",
            "Sanjay Gandhi Postgraduate Institute, Lucknow",
            "King George's Medical University, Lucknow",
            "Madras Medical College, Chennai",
            "Grant Medical College, Mumbai",
            "Maulana Azad Medical College, New Delhi",
            "Armed Forces Medical College, Pune",
            "Jawaharlal Institute of Postgraduate Medical Education, Puducherry",
            "Sree Chitra Tirunal Institute, Thiruvananthapuram",
            "National Institute of Mental Health and Neurosciences, Bangalore",
            "Indian Institute of Science, Bangalore"
        ]
        
        # Indian pharmaceutical and biotech companies
        self.pharma_companies = [
            "Dr. Reddy's Laboratories Ltd.",
            "Cipla Limited",
            "Sun Pharmaceutical Industries Ltd.",
            "Lupin Limited", 
            "Biocon Limited",
            "Cadila Healthcare Ltd.",
            "Glenmark Pharmaceuticals Ltd.",
            "Torrent Pharmaceuticals Ltd.",
            "Alkem Laboratories Ltd.",
            "Mankind Pharma Ltd.",
            "Aurobindo Pharma Ltd.",
            "Divi's Laboratories Ltd.",
            "Hetero Drugs Ltd.",
            "Strides Pharma Science Ltd.",
            "Natco Pharma Ltd."
        ]
        
        # Tier 1 and Tier 2 Indian cities with coordinates
        self.cities_expanded = [
            {"city": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lng": 72.8777},
            {"city": "Delhi", "state": "Delhi", "lat": 28.7041, "lng": 77.1025},
            {"city": "Bangalore", "state": "Karnataka", "lat": 12.9716, "lng": 77.5946},
            {"city": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lng": 80.2707},
            {"city": "Kolkata", "state": "West Bengal", "lat": 22.5726, "lng": 88.3639},
            {"city": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lng": 78.4867},
            {"city": "Pune", "state": "Maharashtra", "lat": 18.5204, "lng": 73.8567},
            {"city": "Ahmedabad", "state": "Gujarat", "lat": 23.0225, "lng": 72.5714},
            {"city": "Lucknow", "state": "Uttar Pradesh", "lat": 26.8467, "lng": 80.9462},
            {"city": "Chandigarh", "state": "Punjab", "lat": 30.7333, "lng": 76.7794},
            {"city": "Jaipur", "state": "Rajasthan", "lat": 26.9124, "lng": 75.7873},
            {"city": "Kochi", "state": "Kerala", "lat": 9.9312, "lng": 76.2673},
            {"city": "Coimbatore", "state": "Tamil Nadu", "lat": 11.0168, "lng": 76.9558},
            {"city": "Indore", "state": "Madhya Pradesh", "lat": 22.7196, "lng": 75.8577},
            {"city": "Bhopal", "state": "Madhya Pradesh", "lat": 23.2599, "lng": 77.4126},
            {"city": "Thiruvananthapuram", "state": "Kerala", "lat": 8.5241, "lng": 76.9366},
            {"city": "Guwahati", "state": "Assam", "lat": 26.1445, "lng": 91.7362},
            {"city": "Bhubaneswar", "state": "Odisha", "lat": 20.2961, "lng": 85.8245}
        ]

    def generate_comprehensive_trials(self, trials_per_condition: int = 6) -> List[ClinicalTrial]:
        """Generate comprehensive set of trials across all conditions."""
        trials = []
        
        for category, conditions in self.conditions_detailed.items():
            for condition in conditions:
                for _ in range(trials_per_condition):
                    trial = self._create_trial_for_condition(condition, category)
                    trials.append(trial)
        
        return trials

    def _create_trial_for_condition(self, condition: str, category: str) -> ClinicalTrial:
        """Create a detailed trial for specific condition."""
        city_info = random.choice(self.cities_expanded)
        
        # Choose sponsor type based on condition
        if category in ["Cancer", "Rare Diseases"]:
            sponsor = random.choice(self.premier_institutions)
        else:
            sponsor = random.choice(self.premier_institutions + self.pharma_companies)
        
        phase = random.choice(list(TrialPhase))
        status = random.choice([
            TrialStatus.RECRUITING, TrialStatus.RECRUITING, TrialStatus.RECRUITING,  # Higher probability
            TrialStatus.ACTIVE, TrialStatus.ACTIVE,
            TrialStatus.COMPLETED
        ])
        
        # Generate unique CTRI ID
        year = random.randint(2022, 2024)
        month = random.randint(1, 12)
        ctri_id = f"CTRI/{year}/{month:02d}/{random.randint(100000, 999999)}"
        
        # Generate trial details
        trial_title = self._generate_detailed_title(condition, phase, category)
        description = self._generate_detailed_description(condition, phase, category)
        eligibility = self._generate_detailed_eligibility(condition, category)
        exclusions = self._generate_detailed_exclusions(condition, category)
        
        # Timeline based on phase
        phase_duration_map = {
            TrialPhase.PHASE_I: (180, 365),
            TrialPhase.PHASE_II: (365, 730),
            TrialPhase.PHASE_III: (730, 1095),
            TrialPhase.PHASE_IV: (365, 1460),
            TrialPhase.NOT_APPLICABLE: (90, 365)
        }
        
        duration_range = phase_duration_map.get(phase, (365, 730))
        start_date = date.today() + timedelta(days=random.randint(-180, 90))
        completion_date = start_date + timedelta(days=random.randint(*duration_range))
        
        # Enrollment based on phase and condition
        enrollment_map = {
            TrialPhase.PHASE_I: (20, 80),
            TrialPhase.PHASE_II: (50, 200),
            TrialPhase.PHASE_III: (200, 1000),
            TrialPhase.PHASE_IV: (500, 3000),
            TrialPhase.NOT_APPLICABLE: (100, 500)
        }
        
        enrollment_range = enrollment_map.get(phase, (100, 300))
        target_enrollment = random.randint(*enrollment_range)
        
        return ClinicalTrial(
            id=str(uuid4()),
            ctri_id=ctri_id,
            title=trial_title,
            condition_name=condition,
            phase=phase,
            status=status,
            description=description,
            primary_objective=self._generate_primary_objective(condition, phase),
            secondary_objectives=self._generate_secondary_objectives(condition),
            eligibility_criteria=eligibility,
            exclusion_criteria=exclusions,
            min_age=eligibility.get("min_age", 18),
            max_age=eligibility.get("max_age", 75),
            gender_criteria=eligibility.get("gender", "Both"),
            location=f"{city_info['city']}, {city_info['state']}",
            city=city_info["city"],
            state=city_info["state"],
            latitude=city_info["lat"],
            longitude=city_info["lng"],
            sponsor=sponsor,
            principal_investigator=self._generate_pi_name(),
            contact_name=self._generate_contact_name(),
            contact_email=self._generate_contact_email(sponsor),
            contact_phone=f"+91-{random.randint(7000000000, 9999999999)}",
            start_date=start_date,
            estimated_completion=completion_date,
            study_type=self._get_study_type(condition, phase),
            intervention_type=self._get_intervention_type(condition, category),
            target_enrollment=target_enrollment,
            keywords=', '.join(self._generate_comprehensive_keywords(condition, category)),
            source_url=f"http://ctri.nic.in/Clinicaltrials/pmaindet2.php?trialid={ctri_id}",
        )

    def _generate_detailed_title(self, condition: str, phase: TrialPhase, category: str) -> str:
        """Generate detailed, realistic trial titles."""
        templates = {
            "Cancer": [
                f"A Randomized, Double-Blind, Placebo-Controlled {phase.value} Study of Novel Targeted Therapy in Advanced {condition}",
                f"Multi-Center {phase.value} Trial Evaluating Combination Immunotherapy for {condition}",
                f"{phase.value} Study of Precision Medicine Approach in Metastatic {condition}",
                f"Open-Label {phase.value} Trial of CAR-T Cell Therapy for Refractory {condition}"
            ],
            "Diabetes": [
                f"A {phase.value} Study of Novel Glucose-Lowering Agent in Patients with {condition}",
                f"Randomized Controlled {phase.value} Trial of Continuous Glucose Monitoring in {condition}",
                f"{phase.value} Study Evaluating Digital Therapeutics for {condition} Management"
            ],
            "Cardiovascular": [
                f"A {phase.value} Trial of Novel Cardioprotective Therapy in {condition}",
                f"Multi-Center {phase.value} Study of Interventional Cardiology Approach for {condition}",
                f"Randomized {phase.value} Trial of Preventive Strategy in {condition}"
            ]
        }
        
        category_templates = templates.get(category, [
            f"A {phase.value} Clinical Trial for {condition}",
            f"Multi-Center {phase.value} Study in {condition} Patients",
            f"Randomized {phase.value} Trial Evaluating Novel Treatment for {condition}"
        ])
        
        return random.choice(category_templates)

    def _generate_detailed_description(self, condition: str, phase: TrialPhase, category: str) -> str:
        """Generate detailed trial descriptions."""
        base_desc = f"This {phase.value} clinical trial is designed to evaluate the safety and efficacy of an investigational treatment approach for {condition}."
        
        phase_specific = {
            TrialPhase.PHASE_I: " The primary focus is on determining the maximum tolerated dose and characterizing the safety profile.",
            TrialPhase.PHASE_II: " The study aims to assess preliminary efficacy while continuing to monitor safety in a larger patient population.",
            TrialPhase.PHASE_III: " This pivotal trial compares the investigational treatment to current standard of care in a large, randomized study.",
            TrialPhase.PHASE_IV: " This post-marketing surveillance study evaluates long-term safety and effectiveness in real-world clinical practice."
        }
        
        return base_desc + phase_specific.get(phase, "")

    def _generate_detailed_eligibility(self, condition: str, category: str) -> Dict[str, Any]:
        """Generate detailed eligibility criteria."""
        base_criteria = {
            "min_age": 18,
            "max_age": 75,
            "gender": "Both",
            "conditions": [f"Confirmed diagnosis of {condition}"]
        }
        
        condition_specific = {
            "Type 2 Diabetes Mellitus": {
                "min_age": 18, "max_age": 70,
                "conditions": [
                    "Confirmed diagnosis of Type 2 Diabetes Mellitus",
                    "HbA1c ≥ 7.0% and ≤ 11.0%",
                    "BMI between 25-40 kg/m²",
                    "Stable diabetes medication for ≥ 3 months"
                ]
            },
            "Breast Cancer": {
                "min_age": 18, "max_age": 80, "gender": "Female",
                "conditions": [
                    "Histologically confirmed invasive breast cancer",
                    "ER/PR positive, HER2 negative",
                    "ECOG performance status 0-1",
                    "Adequate bone marrow, hepatic, and renal function"
                ]
            },
            "Hypertension": {
                "min_age": 21, "max_age": 75,
                "conditions": [
                    "Essential hypertension diagnosis",
                    "Systolic BP 140-180 mmHg or Diastolic BP 90-110 mmHg",
                    "Stable on current antihypertensive therapy for ≥ 4 weeks"
                ]
            },
            "Tuberculosis": {
                "min_age": 18, "max_age": 65,
                "conditions": [
                    "Newly diagnosed pulmonary tuberculosis",
                    "Sputum smear positive for acid-fast bacilli",
                    "No previous anti-TB treatment",
                    "HIV negative status"
                ]
            }
        }
        
        specific = condition_specific.get(condition, {})
        base_criteria.update(specific)
        return base_criteria

    def _generate_detailed_exclusions(self, condition: str, category: str) -> List[str]:
        """Generate comprehensive exclusion criteria."""
        base_exclusions = [
            "Pregnancy or breastfeeding",
            "Severe hepatic impairment (Child-Pugh Class C)",
            "Severe renal impairment (eGFR < 30 mL/min/1.73m²)",
            "Active malignancy other than study indication",
            "Uncontrolled psychiatric disorder",
            "Participation in another clinical trial within 30 days"
        ]
        
        category_exclusions = {
            "Cancer": [
                "Brain metastases (unless treated and stable)",
                "Prior chemotherapy within 4 weeks",
                "Radiation therapy within 2 weeks",
                "Major surgery within 4 weeks"
            ],
            "Diabetes": [
                "Type 1 diabetes mellitus",
                "Diabetic ketoacidosis within 6 months",
                "Severe hypoglycemia requiring assistance within 6 months",
                "Pancreatic surgery or chronic pancreatitis"
            ],
            "Cardiovascular": [
                "Recent myocardial infarction (within 3 months)",
                "Unstable angina",
                "Severe heart failure (NYHA Class IV)",
                "Uncontrolled arrhythmias"
            ],
            "Infectious": [
                "Active opportunistic infections",
                "Immunocompromised state",
                "Recent live vaccine administration",
                "Drug-resistant organism infection"
            ]
        }
        
        return base_exclusions + category_exclusions.get(category, [])

    def _generate_primary_objective(self, condition: str, phase: TrialPhase) -> str:
        """Generate phase-appropriate primary objectives."""
        phase_objectives = {
            TrialPhase.PHASE_I: f"To determine the maximum tolerated dose and dose-limiting toxicities of the investigational treatment in patients with {condition}.",
            TrialPhase.PHASE_II: f"To evaluate the objective response rate of the investigational treatment in patients with {condition}.",
            TrialPhase.PHASE_III: f"To compare the efficacy of the investigational treatment versus standard of care in patients with {condition}, as measured by progression-free survival.",
            TrialPhase.PHASE_IV: f"To evaluate the long-term safety and effectiveness of the approved treatment in real-world patients with {condition}."
        }
        
        return phase_objectives.get(phase, f"To evaluate the safety and efficacy of investigational treatment for {condition}.")

    def _generate_secondary_objectives(self, condition: str) -> str:
        """Generate comprehensive secondary objectives."""
        return ("To assess overall survival; To evaluate quality of life measures using validated instruments; "
                "To analyze biomarker responses and pharmacokinetic parameters; To assess safety and tolerability; "
                "To evaluate patient-reported outcomes; To analyze healthcare resource utilization.")

    def _generate_comprehensive_keywords(self, condition: str, category: str) -> List[str]:
        """Generate comprehensive keywords for search optimization."""
        base_keywords = ["clinical trial", "research study", "medical research"]
        
        condition_keywords = condition.lower().split()
        category_keywords = {
            "Cancer": ["oncology", "tumor", "malignancy", "chemotherapy", "radiation", "immunotherapy"],
            "Diabetes": ["endocrinology", "glucose", "insulin", "metabolism", "HbA1c"],
            "Cardiovascular": ["cardiology", "heart", "blood pressure", "cardiac", "vascular"],
            "Respiratory": ["pulmonology", "lung", "breathing", "respiratory", "pulmonary"],
            "Neurological": ["neurology", "brain", "nervous system", "neurological"],
            "Infectious": ["infectious disease", "infection", "antimicrobial", "pathogen"],
            "Autoimmune": ["immunology", "autoimmune", "inflammation", "immune system"],
            "Renal": ["nephrology", "kidney", "renal", "dialysis", "transplant"],
            "Mental Health": ["psychiatry", "psychology", "mental health", "behavioral"],
            "Rare Diseases": ["rare disease", "orphan drug", "genetic disorder"]
        }
        
        all_keywords = base_keywords + condition_keywords + category_keywords.get(category, [])
        return list(set(all_keywords))  # Remove duplicates

    def _generate_pi_name(self) -> str:
        """Generate realistic Principal Investigator names."""
        titles = ["Dr.", "Prof."]
        first_names = ["Rajesh", "Priya", "Anil", "Sunita", "Vikram", "Meera", "Suresh", "Kavita", "Ravi", "Deepa"]
        last_names = ["Sharma", "Patel", "Kumar", "Singh", "Reddy", "Gupta", "Agarwal", "Jain", "Shah", "Mehta"]
        
        return f"{random.choice(titles)} {random.choice(first_names)} {random.choice(last_names)}"

    def _generate_contact_name(self) -> str:
        """Generate contact person names."""
        first_names = ["Amit", "Neha", "Rohit", "Pooja", "Sanjay", "Ritu", "Manoj", "Seema", "Ajay", "Nisha"]
        last_names = ["Verma", "Joshi", "Malhotra", "Kapoor", "Sinha", "Chopra", "Bansal", "Arora", "Saxena", "Tiwari"]
        
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    def _generate_contact_email(self, sponsor: str) -> str:
        """Generate realistic contact emails based on sponsor."""
        domain_map = {
            "AIIMS": "aiims.edu",
            "Tata Memorial": "tmc.gov.in", 
            "Christian Medical College": "cmcvellore.ac.in",
            "Dr. Reddy's": "drreddys.com",
            "Cipla": "cipla.com",
            "Sun Pharmaceutical": "sunpharma.com"
        }
        
        for key, domain in domain_map.items():
            if key in sponsor:
                return f"clinicaltrials@{domain}"
        
        return "research@clinicaltrials.in"

    def _get_study_type(self, condition: str, phase: TrialPhase) -> str:
        """Determine study type based on condition and phase."""
        if phase == TrialPhase.NOT_APPLICABLE:
            return "Observational"
        return "Interventional"

    def _get_intervention_type(self, condition: str, category: str) -> str:
        """Determine intervention type based on condition category."""
        intervention_map = {
            "Cancer": random.choice(["Drug", "Biological", "Radiation", "Device"]),
            "Diabetes": random.choice(["Drug", "Device", "Behavioral"]),
            "Cardiovascular": random.choice(["Drug", "Device", "Procedure"]),
            "Mental Health": random.choice(["Drug", "Behavioral", "Device"]),
            "Infectious": "Drug"
        }
        
        return intervention_map.get(category, "Drug")

    def add_trials_to_database(self, count: int = 50):
        """Add specified number of trials to database."""
        try:
            print(f"🏥 Generating {count} additional clinical trials...")
            
            # Calculate trials per condition to reach target count
            total_conditions = sum(len(conditions) for conditions in self.conditions_detailed.values())
            trials_per_condition = max(1, count // total_conditions)
            
            trials = self.generate_comprehensive_trials(trials_per_condition)
            
            # If we need more trials, generate additional ones
            while len(trials) < count:
                category = random.choice(list(self.conditions_detailed.keys()))
                condition = random.choice(self.conditions_detailed[category])
                trial = self._create_trial_for_condition(condition, category)
                trials.append(trial)
            
            # Trim to exact count
            trials = trials[:count]
            
            added_count = 0
            for trial in trials:
                try:
                    self.db.add(trial)
                    self.db.commit()
                    added_count += 1
                except IntegrityError:
                    self.db.rollback()
                    print(f"⚠️  Skipped duplicate trial: {trial.ctri_id}")
            
            print(f"✅ Successfully added {added_count} clinical trials to database")
            
        except Exception as e:
            print(f"❌ Error adding trials: {str(e)}")
            self.db.rollback()
            raise
        finally:
            self.db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate additional clinical trials")
    parser.add_argument("--count", type=int, default=50, help="Number of trials to generate")
    args = parser.parse_args()
    
    generator = TrialGenerator()
    generator.add_trials_to_database(args.count)