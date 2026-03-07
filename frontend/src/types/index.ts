// User types
export interface User {
  id: string;
  email: string;
  phone?: string;
  preferred_language: string;
  created_at: string;
  updated_at: string;
}

// Medical Profile types
export interface MedicalProfile {
  id: string;
  user_id: string;
  age: number;
  gender: string;
  conditions: string[];
  medications: string[];
  test_results: Record<string, unknown>;
  medical_history: string[];
  location: string;
  created_at: string;
  updated_at: string;
}

// Document types
export interface Document {
  id: string;
  user_id: string;
  s3_key: string;
  file_name: string;
  file_type: string;
  processing_status: 'pending' | 'processing' | 'completed' | 'failed';
  extracted_text?: string;
  created_at: string;
}

// Clinical Trial types
export interface ClinicalTrial {
  id: string;
  ctri_id: string;
  title: string;
  condition: string;
  phase: 'I' | 'II' | 'III' | 'IV';
  status: 'recruiting' | 'active' | 'completed';
  eligibility_criteria: Record<string, unknown>;
  exclusion_criteria: string[];
  location: string;
  latitude: number;
  longitude: number;
  sponsor: string;
  contact_name: string;
  contact_email: string;
  contact_phone: string;
  start_date: string;
  estimated_completion: string;
  description: string;
  created_at: string;
  updated_at: string;
}

// Match types
export interface Match {
  id: string;
  user_id: string;
  trial_id: string;
  match_score: number;
  match_explanation: string;
  is_favorite: boolean;
  status: 'viewed' | 'contacted' | 'enrolled';
  created_at: string;
}

// API Response types
export interface MatchResponse {
  matches: Array<{
    trial_id: string;
    match_score: number;
    trial: ClinicalTrial;
    match_explanation: string;
    eligibility_summary: {
      met: string[];
      not_met: string[];
    };
  }>;
  total_matches: number;
  processing_time_ms: number;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: Record<string, unknown>;
}
