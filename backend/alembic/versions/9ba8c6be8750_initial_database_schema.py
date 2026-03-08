"""Initial database schema

Revision ID: 9ba8c6be8750
Revises: 
Create Date: 2026-03-07 22:44:57.919027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = '9ba8c6be8750'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', mysql.CHAR(36), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('preferred_language', sa.String(10), nullable=False, server_default='en'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW() ON UPDATE NOW()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('phone')
    )
    
    # Create indexes for users table
    op.create_index('idx_user_email', 'users', ['email'])
    op.create_index('idx_user_phone', 'users', ['phone'])
    op.create_index('idx_user_created_at', 'users', ['created_at'])
    
    # Create medical_profiles table
    op.create_table(
        'medical_profiles',
        sa.Column('id', mysql.CHAR(36), nullable=False),
        sa.Column('user_id', mysql.CHAR(36), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(20), nullable=True),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('conditions', sa.JSON(), nullable=True, comment='List of medical conditions/diagnoses'),
        sa.Column('medications', sa.JSON(), nullable=True, comment='List of current medications'),
        sa.Column('test_results', sa.JSON(), nullable=True, comment='Lab results and biomarkers as key-value pairs'),
        sa.Column('medical_history', sa.JSON(), nullable=True, comment='List of past medical history items'),
        sa.Column('allergies', sa.JSON(), nullable=True, comment='List of known allergies'),
        sa.Column('procedures', sa.JSON(), nullable=True, comment='List of past procedures/surgeries'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW() ON UPDATE NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for medical_profiles table
    op.create_index('idx_medical_profile_user_id', 'medical_profiles', ['user_id'])
    op.create_index('idx_medical_profile_age', 'medical_profiles', ['age'])
    op.create_index('idx_medical_profile_gender', 'medical_profiles', ['gender'])
    op.create_index('idx_medical_profile_location', 'medical_profiles', ['location'])
    op.create_index('idx_medical_profile_updated_at', 'medical_profiles', ['updated_at'])
    
    # Create documents table
    op.create_table(
        'documents',
        sa.Column('id', mysql.CHAR(36), nullable=False),
        sa.Column('user_id', mysql.CHAR(36), nullable=False),
        sa.Column('s3_key', sa.String(500), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_type', sa.String(50), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=True, comment='File size in bytes'),
        sa.Column('processing_status', sa.Enum('pending', 'processing', 'completed', 'failed', name='processingstatus'), nullable=False, server_default='pending'),
        sa.Column('extracted_text', sa.Text(), nullable=True),
        sa.Column('processing_error', sa.Text(), nullable=True),
        sa.Column('ocr_confidence', sa.Float(), nullable=True, comment='OCR confidence score 0-1'),
        sa.Column('processing_duration', sa.Integer(), nullable=True, comment='Processing time in seconds'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW() ON UPDATE NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('s3_key')
    )
    
    # Create indexes for documents table
    op.create_index('idx_document_user_id', 'documents', ['user_id'])
    op.create_index('idx_document_status', 'documents', ['processing_status'])
    op.create_index('idx_document_s3_key', 'documents', ['s3_key'])
    op.create_index('idx_document_created_at', 'documents', ['created_at'])
    op.create_index('idx_document_file_type', 'documents', ['file_type'])
    
    # Create clinical_trials table
    op.create_table(
        'clinical_trials',
        sa.Column('id', mysql.CHAR(36), nullable=False),
        sa.Column('ctri_id', sa.String(50), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('condition', sa.String(255), nullable=False),
        sa.Column('phase', sa.Enum('I', 'II', 'III', 'IV', 'N/A', name='trialphase'), nullable=False),
        sa.Column('status', sa.Enum('recruiting', 'active', 'completed', 'suspended', 'terminated', 'withdrawn', name='trialstatus'), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('primary_objective', sa.Text(), nullable=True),
        sa.Column('secondary_objectives', sa.Text(), nullable=True),
        sa.Column('eligibility_criteria', sa.JSON(), nullable=True, comment='Structured eligibility criteria including age, gender, conditions'),
        sa.Column('exclusion_criteria', sa.JSON(), nullable=True, comment='List of exclusion criteria'),
        sa.Column('min_age', sa.Integer(), nullable=True),
        sa.Column('max_age', sa.Integer(), nullable=True),
        sa.Column('gender_criteria', sa.String(20), nullable=True),
        sa.Column('location', sa.String(255), nullable=False),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('state', sa.String(100), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('sponsor', sa.String(255), nullable=False),
        sa.Column('principal_investigator', sa.String(255), nullable=True),
        sa.Column('contact_name', sa.String(255), nullable=True),
        sa.Column('contact_email', sa.String(255), nullable=True),
        sa.Column('contact_phone', sa.String(50), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('estimated_completion', sa.Date(), nullable=True),
        sa.Column('study_type', sa.String(100), nullable=True),
        sa.Column('intervention_type', sa.String(100), nullable=True),
        sa.Column('target_enrollment', sa.Integer(), nullable=True),
        sa.Column('keywords', sa.JSON(), nullable=True, comment='Keywords for search and matching'),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('last_updated_source', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW() ON UPDATE NOW()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ctri_id')
    )
    
    # Create comprehensive indexes for clinical_trials table
    op.create_index('idx_trial_ctri_id', 'clinical_trials', ['ctri_id'])
    op.create_index('idx_trial_condition', 'clinical_trials', ['condition'])
    op.create_index('idx_trial_phase', 'clinical_trials', ['phase'])
    op.create_index('idx_trial_status', 'clinical_trials', ['status'])
    op.create_index('idx_trial_location', 'clinical_trials', ['location'])
    op.create_index('idx_trial_city', 'clinical_trials', ['city'])
    op.create_index('idx_trial_state', 'clinical_trials', ['state'])
    op.create_index('idx_trial_age_range', 'clinical_trials', ['min_age', 'max_age'])
    op.create_index('idx_trial_gender', 'clinical_trials', ['gender_criteria'])
    op.create_index('idx_trial_start_date', 'clinical_trials', ['start_date'])
    op.create_index('idx_trial_coordinates', 'clinical_trials', ['latitude', 'longitude'])
    op.create_index('idx_trial_sponsor', 'clinical_trials', ['sponsor'])
    op.create_index('idx_trial_updated_at', 'clinical_trials', ['updated_at'])
    # Composite indexes for common query patterns
    op.create_index('idx_trial_status_condition', 'clinical_trials', ['status', 'condition'])
    op.create_index('idx_trial_phase_status', 'clinical_trials', ['phase', 'status'])
    op.create_index('idx_trial_location_status', 'clinical_trials', ['location', 'status'])
    
    # Create matches table
    op.create_table(
        'matches',
        sa.Column('id', mysql.CHAR(36), nullable=False),
        sa.Column('user_id', mysql.CHAR(36), nullable=False),
        sa.Column('trial_id', mysql.CHAR(36), nullable=False),
        sa.Column('match_score', sa.Float(), nullable=False, comment='Match score between 0-100'),
        sa.Column('match_explanation', sa.Text(), nullable=True, comment='Human-readable explanation of why this trial matches'),
        sa.Column('condition_score', sa.Float(), nullable=True),
        sa.Column('eligibility_score', sa.Float(), nullable=True),
        sa.Column('location_score', sa.Float(), nullable=True),
        sa.Column('exclusion_score', sa.Float(), nullable=True),
        sa.Column('is_favorite', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('status', sa.Enum('viewed', 'contacted', 'enrolled', 'declined', 'ineligible', name='matchstatus'), nullable=False, server_default='viewed'),
        sa.Column('contact_attempted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('contact_method', sa.String(50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW() ON UPDATE NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['trial_id'], ['clinical_trials.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for matches table
    op.create_index('idx_match_user_id', 'matches', ['user_id'])
    op.create_index('idx_match_trial_id', 'matches', ['trial_id'])
    op.create_index('idx_match_score', 'matches', ['match_score'])
    op.create_index('idx_match_favorite', 'matches', ['is_favorite'])
    op.create_index('idx_match_status', 'matches', ['status'])
    op.create_index('idx_match_created_at', 'matches', ['created_at'])
    # Composite indexes for common query patterns
    op.create_index('idx_match_user_score', 'matches', ['user_id', 'match_score'])
    op.create_index('idx_match_user_favorite', 'matches', ['user_id', 'is_favorite'])
    op.create_index('idx_match_user_status', 'matches', ['user_id', 'status'])
    # Unique constraint to prevent duplicate matches
    op.create_index('idx_match_unique', 'matches', ['user_id', 'trial_id'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order due to foreign key constraints
    op.drop_table('matches')
    op.drop_table('clinical_trials')
    op.drop_table('documents')
    op.drop_table('medical_profiles')
    op.drop_table('users')
