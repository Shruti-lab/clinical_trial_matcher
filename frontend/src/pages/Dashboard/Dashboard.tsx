import  { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Upload, 
  Search, 
  Heart, 
  FileText, 
  TrendingUp, 
  MapPin,
  Star,
  ArrowRight,
  Plus
} from 'lucide-react';
import apiClient from '../../services/api';

interface DashboardStats {
  totalDocuments: number;
  totalMatches: number;
  totalFavorites: number;
  recentActivity: number;
}

interface RecentMatch {
  id: string;
  trial: {
    id: string;
    title: string;
    condition: string;
    phase: string;
    location: string;
    sponsor: string;
  };
  match_score: number;
  created_at: string;
}

interface FavoriteTrial {
  id: string;
  trial: {
    id: string;
    title: string;
    condition: string;
    phase: string;
    location: string;
    status: string;
  };
  match_score?: number;
  created_at: string;
}

interface MedicalProfileSummary {
  age?: number;
  gender?: string;
  conditions: string[];
  medications: string[];
  location?: string;
  lastUpdated?: string;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStats>({
    totalDocuments: 0,
    totalMatches: 0,
    totalFavorites: 0,
    recentActivity: 0
  });
  const [recentMatches, setRecentMatches] = useState<RecentMatch[]>([]);
  const [favoriteTrials, setFavoriteTrials] = useState<FavoriteTrial[]>([]);
  const [medicalProfile, setMedicalProfile] = useState<MedicalProfileSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load dashboard stats and data in parallel
      const [
        documentsResponse,
        matchesResponse,
        favoritesResponse,
        profileResponse
      ] = await Promise.allSettled([
        apiClient.get('/documents'),
        apiClient.get('/match/results'),
        apiClient.get('/match/favorites'),
        apiClient.get('/profile/medical')
      ]);

      // Process documents
      if (documentsResponse.status === 'fulfilled') {
        const documents = documentsResponse.value.data.documents || [];
        setStats(prev => ({ ...prev, totalDocuments: documents.length }));
      }

      // Process matches
      if (matchesResponse.status === 'fulfilled') {
        const matches = matchesResponse.value.data.matches || [];
        setStats(prev => ({ 
          ...prev, 
          totalMatches: matches.length,
          recentActivity: matches.length 
        }));
        setRecentMatches(matches.slice(0, 5)); // Show top 5 recent matches
      }

      // Process favorites
      if (favoritesResponse.status === 'fulfilled') {
        const favorites = favoritesResponse.value.data.favorites || [];
        setStats(prev => ({ ...prev, totalFavorites: favorites.length }));
        setFavoriteTrials(favorites.slice(0, 3)); // Show top 3 favorites
      }

      // Process medical profile
      if (profileResponse.status === 'fulfilled') {
        setMedicalProfile(profileResponse.value.data);
      }

    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    });
  };

  const quickActions = [
    {
      title: 'Upload Documents',
      description: 'Upload medical records to find matching trials',
      icon: Upload,
      color: 'bg-blue-500',
      action: () => navigate('/upload')
    },
    {
      title: 'Search Trials',
      description: 'Browse and search clinical trials',
      icon: Search,
      color: 'bg-green-500',
      action: () => navigate('/trials')
    },
    {
      title: 'View Profile',
      description: 'Update your medical profile',
      icon: FileText,
      color: 'bg-purple-500',
      action: () => navigate('/profile')
    }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Welcome back! Here's an overview of your clinical trial matching journey.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <FileText className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Documents</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalDocuments}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Trial Matches</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalMatches}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center">
              <div className="p-2 bg-red-100 rounded-lg">
                <Heart className="w-6 h-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Favorites</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalFavorites}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Star className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Recent Activity</p>
                <p className="text-2xl font-bold text-gray-900">{stats.recentActivity}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {quickActions.map((action, index) => (
                  <button
                    key={index}
                    onClick={action.action}
                    className="p-4 border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all text-left"
                  >
                    <div className={`w-10 h-10 ${action.color} rounded-lg flex items-center justify-center mb-3`}>
                      <action.icon className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="font-medium text-gray-900 mb-1">{action.title}</h3>
                    <p className="text-sm text-gray-500">{action.description}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Recent Matches */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Recent Trial Matches</h2>
                {recentMatches.length > 0 && (
                  <button
                    onClick={() => navigate('/results')}
                    className="text-sm text-blue-600 hover:text-blue-700 flex items-center"
                  >
                    View All
                    <ArrowRight className="w-4 h-4 ml-1" />
                  </button>
                )}
              </div>

              {recentMatches.length > 0 ? (
                <div className="space-y-4">
                  {recentMatches.map((match) => (
                    <div
                      key={match.id}
                      onClick={() => navigate(`/trials/${match.trial.id}`)}
                      className="p-4 border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all cursor-pointer"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <h3 className="font-medium text-gray-900 mb-1 line-clamp-1">
                            {match.trial.title}
                          </h3>
                          <div className="flex items-center space-x-2 mb-2">
                            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              {match.trial.condition}
                            </span>
                            <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getPhaseColor(match.trial.phase)}`}>
                              Phase {match.trial.phase}
                            </span>
                          </div>
                          <div className="flex items-center text-sm text-gray-500">
                            <MapPin className="w-4 h-4 mr-1" />
                            <span className="truncate">{match.trial.location}</span>
                          </div>
                        </div>
                        <div className="ml-4 text-right">
                          <div className="text-lg font-semibold text-green-600">
                            {match.match_score.toFixed(0)}%
                          </div>
                          <div className="text-xs text-gray-500">
                            {formatDate(match.created_at)}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <Search className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500 mb-4">No trial matches yet</p>
                  <button
                    onClick={() => navigate('/upload')}
                    className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Upload Documents to Find Matches
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            {/* Medical Profile Summary */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Medical Profile</h3>
                <button
                  onClick={() => navigate('/profile')}
                  className="text-sm text-blue-600 hover:text-blue-700"
                >
                  Edit
                </button>
              </div>

              {medicalProfile ? (
                <div className="space-y-3">
                  {medicalProfile.age && (
                    <div>
                      <p className="text-sm font-medium text-gray-500">Age</p>
                      <p className="text-sm text-gray-900">{medicalProfile.age} years</p>
                    </div>
                  )}
                  
                  {medicalProfile.gender && (
                    <div>
                      <p className="text-sm font-medium text-gray-500">Gender</p>
                      <p className="text-sm text-gray-900">{medicalProfile.gender}</p>
                    </div>
                  )}

                  {medicalProfile.conditions.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-gray-500">Conditions</p>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {medicalProfile.conditions.slice(0, 3).map((condition, index) => (
                          <span
                            key={index}
                            className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                          >
                            {condition}
                          </span>
                        ))}
                        {medicalProfile.conditions.length > 3 && (
                          <span className="text-xs text-gray-500">
                            +{medicalProfile.conditions.length - 3} more
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {medicalProfile.location && (
                    <div>
                      <p className="text-sm font-medium text-gray-500">Location</p>
                      <p className="text-sm text-gray-900">{medicalProfile.location}</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-4">
                  <FileText className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                  <p className="text-sm text-gray-500 mb-3">No medical profile yet</p>
                  <button
                    onClick={() => navigate('/profile')}
                    className="text-sm bg-blue-600 text-white px-3 py-1.5 rounded-lg hover:bg-blue-700"
                  >
                    Create Profile
                  </button>
                </div>
              )}
            </div>

            {/* Favorite Trials */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Favorite Trials</h3>
                {favoriteTrials.length > 0 && (
                  <button
                    onClick={() => navigate('/favorites')}
                    className="text-sm text-blue-600 hover:text-blue-700"
                  >
                    View All
                  </button>
                )}
              </div>

              {favoriteTrials.length > 0 ? (
                <div className="space-y-3">
                  {favoriteTrials.map((favorite) => (
                    <div
                      key={favorite.id}
                      onClick={() => navigate(`/trials/${favorite.trial.id}`)}
                      className="p-3 border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all cursor-pointer"
                    >
                      <h4 className="font-medium text-gray-900 text-sm mb-1 line-clamp-2">
                        {favorite.trial.title}
                      </h4>
                      <div className="flex items-center justify-between">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getPhaseColor(favorite.trial.phase)}`}>
                          Phase {favorite.trial.phase}
                        </span>
                        {favorite.match_score && (
                          <span className="text-xs text-green-600 font-medium">
                            {favorite.match_score.toFixed(0)}%
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-4">
                  <Heart className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                  <p className="text-sm text-gray-500">No favorite trials yet</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;