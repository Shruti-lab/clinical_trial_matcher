import  { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  MapPin,
  Heart,
  Phone,
  Mail,
  ExternalLink,
  Clock,
  User,
  Building,
  FileText,
  CheckCircle,
  XCircle,
  AlertCircle,
} from 'lucide-react';
import apiClient from '../../services/api';

interface TrialDetail {
  id: string;
  ctri_id: string;
  title: string;
  condition: string;
  phase: string;
  status: string;
  description?: string;
  primary_objective?: string;
  secondary_objectives?: string;
  eligibility_criteria?: Record<string, any>;
  exclusion_criteria?: string[];
  min_age?: number;
  max_age?: number;
  gender_criteria?: string;
  location: string;
  city?: string;
  state?: string;
  latitude?: number;
  longitude?: number;
  sponsor: string;
  principal_investigator?: string;
  contact_name?: string;
  contact_email?: string;
  contact_phone?: string;
  start_date?: string;
  estimated_completion?: string;
  study_type?: string;
  intervention_type?: string;
  target_enrollment?: number;
  keywords?: string[];
  source_url?: string;
  last_updated_source?: string;
  created_at: string;
  updated_at: string;
}

const TrialDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [trial, setTrial] = useState<TrialDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isFavorite, setIsFavorite] = useState(false);
  const [favoriting, setFavoriting] = useState(false);

  useEffect(() => {
    if (id) {
      fetchTrialDetail(id);
    }
  }, [id]);

  const fetchTrialDetail = async (trialId: string) => {
    try {
      setLoading(true);
      const response = await apiClient.get(`/trials/${trialId}`);
      setTrial(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load trial details');
    } finally {
      setLoading(false);
    }
  };

  const handleFavorite = async () => {
    if (!trial) return;

    setFavoriting(true);
    try {
      if (isFavorite) {
        await apiClient.delete(`/match/favorite/${trial.id}`);
        setIsFavorite(false);
      } else {
        await apiClient.post('/match/favorite', {
          trial_id: trial.id
        });
        setIsFavorite(true);
      }
    } catch (err) {
      console.error('Error updating favorite:', err);
    } finally {
      setFavoriting(false);
    }
  };

  const handleContact = async () => {
    if (!trial) return;

    try {
      await apiClient.post(`/trials/${trial.id}/contact`);
      // Show success message or redirect to contact info
    } catch (err) {
      console.error('Error recording contact:', err);
    }
  };

  const getPhaseColor = (phase: string) => {
    switch (phase) {
      case 'I': return 'bg-blue-100 text-blue-800';
      case 'II': return 'bg-green-100 text-green-800';
      case 'III': return 'bg-yellow-100 text-yellow-800';
      case 'IV': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'recruiting': return 'bg-green-100 text-green-800';
      case 'active': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Not specified';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const renderEligibilityCriteria = () => {
    if (!trial?.eligibility_criteria) return null;

    const criteria = trial.eligibility_criteria;
    const criteriaList = [];

    // Age criteria
    if (trial.min_age || trial.max_age) {
      const ageText = trial.min_age && trial.max_age
        ? `Ages ${trial.min_age}-${trial.max_age} years`
        : trial.min_age
        ? `Age ${trial.min_age}+ years`
        : `Age up to ${trial.max_age} years`;
      criteriaList.push(ageText);
    }

    // Gender criteria
    if (trial.gender_criteria && trial.gender_criteria !== 'both') {
      criteriaList.push(`Gender: ${trial.gender_criteria}`);
    }

    // Other criteria from the eligibility_criteria object
    Object.entries(criteria).forEach(([key, value]) => {
      if (typeof value === 'string' && value.trim()) {
        criteriaList.push(`${key.replace(/_/g, ' ')}: ${value}`);
      } else if (Array.isArray(value) && value.length > 0) {
        criteriaList.push(`${key.replace(/_/g, ' ')}: ${value.join(', ')}`);
      }
    });

    return criteriaList;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading trial details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Trial</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/trials')}
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Trials
          </button>
        </div>
      </div>
    );
  }

  if (!trial) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Trial not found</p>
          <button
            onClick={() => navigate('/trials')}
            className="mt-4 inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Trials
          </button>
        </div>
      </div>
    );
  }

  const eligibilityCriteria = renderEligibilityCriteria();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate(-1)}
            className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Results
          </button>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h1 className="text-2xl font-bold text-gray-900 mb-2">
                  {trial.title}
                </h1>
                <p className="text-sm text-gray-500 mb-4">
                  CTRI ID: {trial.ctri_id}
                </p>

                {/* Status badges */}
                <div className="flex flex-wrap items-center gap-2">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {trial.condition}
                  </span>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPhaseColor(trial.phase)}`}>
                    Phase {trial.phase}
                  </span>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(trial.status)}`}>
                    {trial.status.charAt(0).toUpperCase() + trial.status.slice(1)}
                  </span>
                </div>
              </div>

              {/* Action buttons */}
              <div className="flex items-center space-x-3 ml-4">
                <button
                  onClick={handleFavorite}
                  disabled={favoriting}
                  className={`p-2 rounded-full transition-colors ${
                    isFavorite
                      ? 'text-red-600 hover:text-red-700 bg-red-50'
                      : 'text-gray-400 hover:text-red-600 hover:bg-red-50'
                  } ${favoriting ? 'opacity-50 cursor-not-allowed' : ''}`}
                  title={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                >
                  <Heart className={`w-5 h-5 ${isFavorite ? 'fill-current' : ''}`} />
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Description */}
            {trial.description && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <FileText className="w-5 h-5 mr-2" />
                  Study Description
                </h2>
                <p className="text-gray-700 leading-relaxed">{trial.description}</p>
              </div>
            )}

            {/* Objectives */}
            {(trial.primary_objective || trial.secondary_objectives) && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Study Objectives
                </h2>
                {trial.primary_objective && (
                  <div className="mb-4">
                    <h3 className="font-medium text-gray-900 mb-2">Primary Objective</h3>
                    <p className="text-gray-700">{trial.primary_objective}</p>
                  </div>
                )}
                {trial.secondary_objectives && (
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Secondary Objectives</h3>
                    <p className="text-gray-700">{trial.secondary_objectives}</p>
                  </div>
                )}
              </div>
            )}

            {/* Eligibility Criteria */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                Eligibility Criteria
              </h2>

              {eligibilityCriteria && eligibilityCriteria.length > 0 ? (
                <ul className="space-y-2">
                  {eligibilityCriteria.map((criterion, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{criterion}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No specific eligibility criteria listed</p>
              )}

              {/* Exclusion Criteria */}
              {trial.exclusion_criteria && trial.exclusion_criteria.length > 0 && (
                <div className="mt-6">
                  <h3 className="font-medium text-gray-900 mb-3 flex items-center">
                    <XCircle className="w-5 h-5 mr-2 text-red-600" />
                    Exclusion Criteria
                  </h3>
                  <ul className="space-y-2">
                    {trial.exclusion_criteria.map((criterion, index) => (
                      <li key={index} className="flex items-start">
                        <XCircle className="w-4 h-4 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-700">{criterion}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Study Details */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Study Details
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {trial.study_type && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Study Type</dt>
                    <dd className="text-sm text-gray-900">{trial.study_type}</dd>
                  </div>
                )}
                {trial.intervention_type && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Intervention Type</dt>
                    <dd className="text-sm text-gray-900">{trial.intervention_type}</dd>
                  </div>
                )}
                {trial.target_enrollment && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Target Enrollment</dt>
                    <dd className="text-sm text-gray-900">{trial.target_enrollment} participants</dd>
                  </div>
                )}
                <div>
                  <dt className="text-sm font-medium text-gray-500">Start Date</dt>
                  <dd className="text-sm text-gray-900">{formatDate(trial.start_date)}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Estimated Completion</dt>
                  <dd className="text-sm text-gray-900">{formatDate(trial.estimated_completion)}</dd>
                </div>
              </div>

              {/* Keywords */}
              {trial.keywords && trial.keywords.length > 0 && (
                <div className="mt-4">
                  <dt className="text-sm font-medium text-gray-500 mb-2">Keywords</dt>
                  <div className="flex flex-wrap gap-2">
                    {trial.keywords.map((keyword, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Location */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <MapPin className="w-5 h-5 mr-2" />
                Location
              </h3>
              <p className="text-gray-700">{trial.location}</p>
              {(trial.city || trial.state) && (
                <p className="text-sm text-gray-500 mt-1">
                  {[trial.city, trial.state].filter(Boolean).join(', ')}
                </p>
              )}
            </div>

            {/* Sponsor */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Building className="w-5 h-5 mr-2" />
                Sponsor
              </h3>
              <p className="text-gray-700">{trial.sponsor}</p>
              {trial.principal_investigator && (
                <div className="mt-3">
                  <p className="text-sm font-medium text-gray-500">Principal Investigator</p>
                  <p className="text-sm text-gray-900">{trial.principal_investigator}</p>
                </div>
              )}
            </div>

            {/* Contact Information */}
            {(trial.contact_name || trial.contact_email || trial.contact_phone) && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <User className="w-5 h-5 mr-2" />
                  Contact Information
                </h3>

                {trial.contact_name && (
                  <div className="mb-3">
                    <p className="text-sm font-medium text-gray-500">Contact Person</p>
                    <p className="text-sm text-gray-900">{trial.contact_name}</p>
                  </div>
                )}

                <div className="space-y-2">
                  {trial.contact_email && (
                    <a
                      href={`mailto:${trial.contact_email}`}
                      className="flex items-center text-sm text-blue-600 hover:text-blue-700"
                    >
                      <Mail className="w-4 h-4 mr-2" />
                      {trial.contact_email}
                    </a>
                  )}

                  {trial.contact_phone && (
                    <a
                      href={`tel:${trial.contact_phone}`}
                      className="flex items-center text-sm text-blue-600 hover:text-blue-700"
                    >
                      <Phone className="w-4 h-4 mr-2" />
                      {trial.contact_phone}
                    </a>
                  )}
                </div>

                <button
                  onClick={handleContact}
                  className="w-full mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Contact Study Team
                </button>
              </div>
            )}

            {/* Additional Information */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Clock className="w-5 h-5 mr-2" />
                Additional Information
              </h3>

              <div className="space-y-3 text-sm">
                <div>
                  <p className="font-medium text-gray-500">Last Updated</p>
                  <p className="text-gray-900">{formatDate(trial.updated_at)}</p>
                </div>

                {trial.source_url && (
                  <div>
                    <p className="font-medium text-gray-500">Source</p>
                    <a
                      href={trial.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-blue-600 hover:text-blue-700"
                    >
                      View Original Listing
                      <ExternalLink className="w-3 h-3 ml-1" />
                    </a>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrialDetail;
