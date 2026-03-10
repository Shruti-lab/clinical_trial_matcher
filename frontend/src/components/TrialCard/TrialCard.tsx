import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, Calendar, Users, Heart, ExternalLink} from 'lucide-react';

interface Trial {
  id: string;
  ctri_id: string;
  title: string;
  condition: string;
  phase: string;
  status: string;
  location: string;
  city?: string;
  state?: string;
  sponsor: string;
  start_date?: string;
  estimated_completion?: string;
  match_score?: number;
  match_explanation?: string;
  distance_km?: number;
}

interface TrialCardProps {
  trial: Trial;
  showMatchScore?: boolean;
  onFavorite?: (trialId: string) => void;
  isFavorite?: boolean;
}

const TrialCard: React.FC<TrialCardProps> = ({ 
  trial, 
  showMatchScore = false, 
  onFavorite,
  isFavorite = false 
}) => {
  const navigate = useNavigate();
  const [favoriting, setFavoriting] = useState(false);

  const handleCardClick = () => {
    navigate(`/trials/${trial.id}`);
  };

  const handleFavoriteClick = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!onFavorite) return;

    setFavoriting(true);
    try {
      await onFavorite(trial.id);
    } catch (error) {
      console.error('Error favoriting trial:', error);
    } finally {
      setFavoriting(false);
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

  const getMatchScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50';
    if (score >= 60) return 'text-yellow-600 bg-yellow-50';
    if (score >= 40) return 'text-orange-600 bg-orange-50';
    return 'text-red-600 bg-red-50';
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Not specified';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div 
      onClick={handleCardClick}
      className="p-6 hover:bg-gray-50 cursor-pointer transition-colors border-b border-gray-200 last:border-b-0"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          {/* Header */}
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-semibold text-gray-900 mb-1 line-clamp-2">
                {trial.title}
              </h3>
              <p className="text-sm text-gray-500 mb-2">
                CTRI ID: {trial.ctri_id}
              </p>
            </div>
            
            {/* Match Score */}
            {showMatchScore && trial.match_score !== undefined && (
              <div className={`ml-4 px-3 py-1 rounded-full text-sm font-medium ${getMatchScoreColor(trial.match_score)}`}>
                {trial.match_score.toFixed(0)}% Match
              </div>
            )}
          </div>

          {/* Condition and Phase */}
          <div className="flex flex-wrap items-center gap-2 mb-3">
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

          {/* Details Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
            {/* Location */}
            <div className="flex items-center">
              <MapPin className="w-4 h-4 mr-2 text-gray-400" />
              <span className="truncate">
                {trial.location}
                {trial.distance_km && (
                  <span className="text-gray-500 ml-1">
                    ({trial.distance_km.toFixed(0)}km away)
                  </span>
                )}
              </span>
            </div>

            {/* Sponsor */}
            <div className="flex items-center">
              <Users className="w-4 h-4 mr-2 text-gray-400" />
              <span className="truncate">{trial.sponsor}</span>
            </div>

            {/* Start Date */}
            {trial.start_date && (
              <div className="flex items-center">
                <Calendar className="w-4 h-4 mr-2 text-gray-400" />
                <span>Started: {formatDate(trial.start_date)}</span>
              </div>
            )}

            {/* Estimated Completion */}
            {trial.estimated_completion && (
              <div className="flex items-center">
                <Calendar className="w-4 h-4 mr-2 text-gray-400" />
                <span>Est. completion: {formatDate(trial.estimated_completion)}</span>
              </div>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-2 ml-4">
          {/* Favorite Button */}
          {onFavorite && (
            <button
              onClick={handleFavoriteClick}
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
          )}

          {/* View Details Button */}
          <button
            onClick={handleCardClick}
            className="inline-flex items-center px-3 py-1.5 text-sm font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors"
          >
            View Details
            <ExternalLink className="w-3 h-3 ml-1" />
          </button>
        </div>
      </div>

      {/* Match Explanation (if provided) */}
      {showMatchScore && (trial as any).match_explanation && (
        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>Why this matches:</strong> {(trial as any).match_explanation}
          </p>
        </div>
      )}
    </div>
  );
};

export default TrialCard;