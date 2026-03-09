import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, SortAsc, SortDesc, RefreshCw, Heart, Star } from 'lucide-react';
import TrialCard from '../../components/TrialCard';

interface TrialMatch {
  trial: {
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
  };
  match_score: number;
  match_explanation: string;
  eligibility_summary: {
    met: string[];
    not_met: string[];
  };
  distance_km?: number;
}

interface SortOption {
  value: string;
  label: string;
}

const Results = () => {
  const navigate = useNavigate();
  const [matches, setMatches] = useState<TrialMatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<string>('match_score');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [filterPhase, setFilterPhase] = useState<string>('');
  const [filterMinScore, setFilterMinScore] = useState<number>(0);
  const [favorites, setFavorites] = useState<Set<string>>(new Set());
  const [showFilters, setShowFilters] = useState(false);

  const sortOptions: SortOption[] = [
    { value: 'match_score', label: 'Match Score' },
    { value: 'phase', label: 'Trial Phase' },
    { value: 'distance', label: 'Distance' },
    { value: 'start_date', label: 'Start Date' }
  ];

  const fetchMatches = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/match', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          limit: 50,
          filters: {}
        })
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('No medical profile found. Please upload medical documents or create a profile first.');
        }
        throw new Error('Failed to find matching trials');
      }

      const data = await response.json();
      setMatches(data.matches || []);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load trial matches';
      setError(errorMessage);
      console.error('Error fetching matches:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchFavorites = async () => {
    try {
      const response = await fetch('/api/match/favorites');
      if (response.ok) {
        const data = await response.json();
        const favoriteIds = new Set<string>(data.favorites.map((fav: any) => fav.trial.id));
        setFavorites(favoriteIds);
      }
    } catch (error) {
      console.error('Error fetching favorites:', error);
    }
  };

  const handleFavorite = async (trialId: string) => {
    const isFavorite = favorites.has(trialId);
    const match = matches.find(m => m.trial.id === trialId);
    
    if (!match) return;

    try {
      if (isFavorite) {
        const response = await fetch(`/api/match/favorite/${trialId}`, {
          method: 'DELETE'
        });
        
        if (response.ok) {
          setFavorites(prev => {
            const newSet = new Set(prev);
            newSet.delete(trialId);
            return newSet;
          });
        }
      } else {
        const response = await fetch('/api/match/favorite', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            trial_id: trialId,
            match_score: match.match_score,
            match_explanation: match.match_explanation
          })
        });
        
        if (response.ok) {
          setFavorites(prev => new Set(prev).add(trialId));
        }
      }
    } catch (error) {
      console.error('Error updating favorite:', error);
      alert('Failed to update favorite. Please try again.');
    }
  };

  const getSortedAndFilteredMatches = () => {
    let filtered = matches.filter(match => {
      if (filterPhase && match.trial.phase !== filterPhase) return false;
      if (match.match_score < filterMinScore) return false;
      return true;
    });

    return filtered.sort((a, b) => {
      let aValue: any, bValue: any;
      
      switch (sortBy) {
        case 'match_score':
          aValue = a.match_score;
          bValue = b.match_score;
          break;
        case 'phase':
          aValue = a.trial.phase;
          bValue = b.trial.phase;
          break;
        case 'distance':
          aValue = a.distance_km || 999;
          bValue = b.distance_km || 999;
          break;
        case 'start_date':
          aValue = new Date(a.trial.start_date || '1900-01-01');
          bValue = new Date(b.trial.start_date || '1900-01-01');
          break;
        default:
          aValue = a.match_score;
          bValue = b.match_score;
      }

      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });
  };

  useEffect(() => {
    fetchMatches();
    fetchFavorites();
  }, []);

  const filteredMatches = getSortedAndFilteredMatches();

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center py-12">
            <RefreshCw className="w-8 h-8 text-blue-500 animate-spin mr-3" />
            <span className="text-lg text-gray-600">Finding your trial matches...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-red-800 mb-2">Unable to Find Matches</h2>
            <p className="text-red-700 mb-4">{error}</p>
            <div className="flex space-x-3">
              <button
                onClick={() => navigate('/upload')}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Upload Documents
              </button>
              <button
                onClick={() => navigate('/profile')}
                className="px-4 py-2 bg-white text-red-600 border border-red-300 rounded-lg hover:bg-red-50 transition-colors"
              >
                Create Profile
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Your Trial Matches
          </h1>
          <p className="text-lg text-gray-600">
            Clinical trials ranked by how well they match your medical profile
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium text-gray-700">Sort by:</label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  {sortOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
              
              <button
                onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                className="p-1.5 text-gray-400 hover:text-gray-600 transition-colors"
              >
                {sortOrder === 'asc' ? <SortAsc className="w-4 h-4" /> : <SortDesc className="w-4 h-4" />}
              </button>
            </div>

            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="inline-flex items-center px-3 py-1.5 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                <Filter className="w-4 h-4 mr-1" />
                Filters
              </button>
              
              <button
                onClick={fetchMatches}
                className="inline-flex items-center px-3 py-1.5 text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors"
              >
                <RefreshCw className="w-4 h-4 mr-1" />
                Refresh
              </button>
            </div>
          </div>

          {showFilters && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Trial Phase
                  </label>
                  <select
                    value={filterPhase}
                    onChange={(e) => setFilterPhase(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">All Phases</option>
                    <option value="I">Phase I</option>
                    <option value="II">Phase II</option>
                    <option value="III">Phase III</option>
                    <option value="IV">Phase IV</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Minimum Match Score
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={filterMinScore}
                    onChange={(e) => setFilterMinScore(parseInt(e.target.value))}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>0%</span>
                    <span className="font-medium">{filterMinScore}%</span>
                    <span>100%</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-sm">
          {filteredMatches.length > 0 ? (
            <>
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold text-gray-900">
                    {filteredMatches.length} Matching Trial{filteredMatches.length !== 1 ? 's' : ''}
                  </h2>
                  <div className="flex items-center text-sm text-gray-500">
                    <Star className="w-4 h-4 mr-1" />
                    Click the heart to save favorites
                  </div>
                </div>
              </div>
              
              <div className="divide-y divide-gray-200">
                {filteredMatches.map((match) => (
                  <TrialCard
                    key={match.trial.id}
                    trial={{
                      ...match.trial,
                      match_score: match.match_score,
                      match_explanation: match.match_explanation,
                      distance_km: match.distance_km
                    }}
                    showMatchScore={true}
                    onFavorite={handleFavorite}
                    isFavorite={favorites.has(match.trial.id)}
                  />
                ))}
              </div>
            </>
          ) : (
            <div className="text-center py-12">
              <Search className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No matching trials found</h3>
              <p className="text-gray-500 mb-6">
                {matches.length === 0 
                  ? "We couldn't find any trials that match your profile. Try updating your medical information."
                  : "No trials match your current filters. Try adjusting the filter criteria."
                }
              </p>
              <div className="flex justify-center space-x-3">
                <button
                  onClick={() => navigate('/profile')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Update Profile
                </button>
                <button
                  onClick={() => navigate('/trials')}
                  className="px-4 py-2 bg-white text-blue-600 border border-blue-300 rounded-lg hover:bg-blue-50 transition-colors"
                >
                  Browse All Trials
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Results;
