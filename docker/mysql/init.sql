-- Clinical Trial Matcher Database Initialization Script

-- Create database if not exists (already handled by MYSQL_DATABASE env var)
USE trialmatch;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    preferred_language VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_phone (phone)
);

-- Create medical_profiles table
CREATE TABLE IF NOT EXISTS medical_profiles (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    age INT,
    gender ENUM('male', 'female', 'other'),
    conditions JSON,
    medications JSON,
    test_results JSON,
    medical_history JSON,
    location VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_location (location)
);

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    s3_key VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size BIGINT,
    processing_status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    extracted_text LONGTEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_processing_status (processing_status),
    INDEX idx_created_at (created_at)
);

-- Create clinical_trials table
CREATE TABLE IF NOT EXISTS clinical_trials (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    ctri_id VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    condition_name VARCHAR(255) NOT NULL,
    phase ENUM('I', 'II', 'III', 'IV', 'Not Applicable') NOT NULL,
    status ENUM('recruiting', 'active', 'completed', 'suspended', 'terminated') DEFAULT 'recruiting',
    eligibility_criteria JSON,
    exclusion_criteria JSON,
    location VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    sponsor VARCHAR(255),
    contact_name VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    start_date DATE,
    estimated_completion DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_ctri_id (ctri_id),
    INDEX idx_condition (condition_name),
    INDEX idx_phase (phase),
    INDEX idx_status (status),
    INDEX idx_location (location),
    FULLTEXT idx_title_description (title, description)
);

-- Create matches table
CREATE TABLE IF NOT EXISTS matches (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    trial_id CHAR(36) NOT NULL,
    match_score DECIMAL(5, 2) NOT NULL,
    match_explanation TEXT,
    is_favorite BOOLEAN DEFAULT FALSE,
    status ENUM('viewed', 'contacted', 'enrolled', 'declined') DEFAULT 'viewed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (trial_id) REFERENCES clinical_trials(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_trial (user_id, trial_id),
    INDEX idx_user_id (user_id),
    INDEX idx_trial_id (trial_id),
    INDEX idx_match_score (match_score),
    INDEX idx_is_favorite (is_favorite)
);

-- Create user_sessions table for JWT token management
CREATE TABLE IF NOT EXISTS user_sessions (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_token_hash (token_hash),
    INDEX idx_expires_at (expires_at)
);

-- Insert sample data for development
INSERT INTO users (id, email, password_hash, preferred_language) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VJWZjqZVu', 'en'),
('550e8400-e29b-41d4-a716-446655440001', 'patient@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VJWZjqZVu', 'hi');

-- Insert sample clinical trials
INSERT INTO clinical_trials (id, ctri_id, title, condition_name, phase, status, location, sponsor, contact_name, contact_email, description) VALUES
('660e8400-e29b-41d4-a716-446655440000', 'CTRI/2024/01/001', 'Phase III Study of Drug X for Breast Cancer', 'Breast Cancer', 'III', 'recruiting', 'AIIMS, New Delhi', 'Pharma Corp', 'Dr. Smith', 'dr.smith@aiims.edu', 'A randomized controlled trial for advanced breast cancer treatment'),
('660e8400-e29b-41d4-a716-446655440001', 'CTRI/2024/01/002', 'Phase II Trial for Diabetes Management', 'Type 2 Diabetes', 'II', 'recruiting', 'CMC Vellore', 'MedTech Ltd', 'Dr. Patel', 'dr.patel@cmc.edu', 'Innovative approach to diabetes management using AI-powered monitoring');

COMMIT;