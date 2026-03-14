import React, { useState, useEffect } from 'react';
import { Search, Filter, ChevronDown } from 'lucide-react';
import TrialCard from '../../components/TrialCard';
import apiClient from '../../services/api';

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
}

interface SearchFilters {
  condition: string;
  location: string;
  phase: string;
  status: string;
  min_age?: number;
  max_age?: number;
  gender: string;
}

const Trials: React.FC = () => {
  const [trials, setTrials] = useState<Trial[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<SearchFilters>({
    condition: '',
    location: '',
    phase: '',
    status: 'recruiting',
    gender: ''
  });
  const [showFilters, setShowFilters] = useState(false);
  const [conditionSuggestions, setConditionSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const searchTrials = async (resetPage = false) => {
    setLoading(true);
    try {
      const currentPage = resetPage ? 1 : page;
      const params = new URLSearchParams({
        page: currentPage.toString(),
        per_page: '20'
      });

      if (searchQuery.trim()) params.append('q', searchQuery.trim());
      if (filters.condition) params.append('condition', filters.condition);
      if (filters.location) params.append('location', filters.location);
      if (filters.phase) params.append('phase', filters.phase);
      if (filters.status) params.append('status', filters.status);
      if (filters.min_age) params.append('min_age', filters.min_age.toString());
      if (filters.max_age) params.append('max_age', filters.max_age.toString());
      if (filters.gender) params.append('gender', filters.gender);

      const response = await apiClient.get(`/trials?${params}`);
      setTrials(response.data.trials || []);
      setTotalPages(response.data.total_pages || 1);
      if (resetPage) setPage(1);
    } catch (error) {
      console.error('Search error:', error);
      setTrials([]);
    } finally {
      setLoading(false);
    }
  };

  const getConditionSuggestions = async (query: string) => {
    if (query.length < 2) {
      setConditionSuggestions([]);
      return;
    }

    try {
      const response = await apiClient.get(`/trials/conditions/autocomplete?q=${encodeURIComponent(query)}`);
      setConditionSuggestions(response.data.suggestions || []);
    } catch (error) {
      console.error('Autocomplete error:', error);
    }
  };

  useEffect(() => {
    searchTrials(true);
  }, []);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchQuery || Object.values(filters).some(v => v)) {
        searchTrials(true);
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [searchQuery, filters]);

  const handleConditionChange = (value: string) => {
    setFilters(prev => ({ ...prev, condition: value }));
    getConditionSuggestions(value);
    setShowSuggestions(true);
  };

  const selectSuggestion = (suggestion: string) => {
    setFilters(prev => ({ ...prev, condition: suggestion }));
    setShowSuggestions(false);
    setConditionSuggestions([]);
  };

  const clearFilters = () => {
    setFilters({
      condition: '',
      location: '',
      phase: '',
      status: 'recruiting',
      gender: ''
    });
    setSearchQuery('');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Find Clinical Trials
          </h1>
          <p className="text-lg text-gray-600">
            Search for clinical trials that match your medical condition and location
          </p>
        </div>

        {/* Search Bar */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search by condition, treatment, or keywords..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="inline-flex items-center px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <Filter className="w-4 h-4 mr-2" />
              Filters
              <ChevronDown className={`w-4 h-4 ml-2 transform transition-transform ${showFilters ? 'rotate-180' : ''}`} />
            </button>
          </div>

          {/* Filters Panel */}
          {showFilters && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Condition Filter */}
                <div className="relative">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Medical Condition
                  </label>
                  <input
                    type="text"
                    placeholder="e.g., Cancer, Diabetes"
                    value={filters.condition}
                    onChange={(e) => handleConditionChange(e.target.value)}
                    onFocus={() => setShowSuggestions(true)}
                    onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                  {showSuggestions && conditionSuggestions.length > 0 && (
                    <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-40 overflow-y-auto">
                      {conditionSuggestions.map((suggestion, index) => (
                        <button
                          key={index}
                          onClick={() => selectSuggestion(suggestion)}
                          className="w-full text-left px-3 py-2 hover:bg-gray-100 text-sm"
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                {/* Location Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Location
                  </label>
                  <input
                    type="text"
                    placeholder="City, State"
                    value={filters.location}
                    onChange={(e) => setFilters(prev => ({ ...prev, location: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                {/* Phase Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Trial Phase
                  </label>
                  <select
                    value={filters.phase}
                    onChange={(e) => setFilters(prev => ({ ...prev, phase: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">All Phases</option>
                    <option value="I">Phase I</option>
                    <option value="II">Phase II</option>
                    <option value="III">Phase III</option>
                    <option value="IV">Phase IV</option>
                  </select>
                </div>

                {/* Status Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Status
                  </label>
                  <select
                    value={filters.status}
                    onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">All Statuses</option>
                    <option value="recruiting">Recruiting</option>
                    <option value="active">Active</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>
              </div>

              {/* Age and Gender Filters */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Min Age
                  </label>
                  <input
                    type="number"
                    placeholder="18"
                    value={filters.min_age || ''}
                    onChange={(e) => setFilters(prev => ({ ...prev, min_age: e.target.value ? parseInt(e.target.value) : undefined }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Max Age
                  </label>
                  <input
                    type="number"
                    placeholder="65"
                    value={filters.max_age || ''}
                    onChange={(e) => setFilters(prev => ({ ...prev, max_age: e.target.value ? parseInt(e.target.value) : undefined }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Gender
                  </label>
                  <select
                    value={filters.gender}
                    onChange={(e) => setFilters(prev => ({ ...prev, gender: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">All Genders</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
                </div>
              </div>

              {/* Clear Filters */}
              <div className="mt-4">
                <button
                  onClick={clearFilters}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Clear all filters
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow-sm">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-2 text-gray-600">Searching trials...</span>
            </div>
          ) : trials.length > 0 ? (
            <>
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">
                  Search Results ({trials.length} trials found)
                </h2>
              </div>
              <div className="divide-y divide-gray-200">
                {trials.map((trial) => (
                  <TrialCard key={trial.id} trial={trial} />
                ))}
              </div>
              
              {/* Pagination */}
              {totalPages > 1 && (
                <div className="p-6 border-t border-gray-200">
                  <div className="flex items-center justify-between">
                    <button
                      onClick={() => {
                        if (page > 1) {
                          setPage(page - 1);
                          searchTrials();
                        }
                      }}
                      disabled={page <= 1}
                      className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Previous
                    </button>
                    <span className="text-sm text-gray-700">
                      Page {page} of {totalPages}
                    </span>
                    <button
                      onClick={() => {
                        if (page < totalPages) {
                          setPage(page + 1);
                          searchTrials();
                        }
                      }}
                      disabled={page >= totalPages}
                      className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Next
                    </button>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-12">
              <Search className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No trials found</h3>
              <p className="text-gray-500">
                Try adjusting your search criteria or filters to find more results.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Trials;