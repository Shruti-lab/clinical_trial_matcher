import { useNavigate } from 'react-router-dom';
import { Upload, Search, Heart, BarChart3 } from 'lucide-react';
import { useAuthStore } from '../../stores/authStore';

const Home = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const features = [
    {
      title: 'Upload Medical Records',
      description: 'Securely upload your medical documents for AI-powered analysis',
      icon: Upload,
      action: () => navigate('/upload'),
      color: 'bg-blue-500'
    },
    {
      title: 'Search Clinical Trials',
      description: 'Browse and search through thousands of clinical trials',
      icon: Search,
      action: () => navigate('/trials'),
      color: 'bg-green-500'
    },
    {
      title: 'View Dashboard',
      description: 'Track your matches, favorites, and medical profile',
      icon: BarChart3,
      action: () => navigate('/dashboard'),
      color: 'bg-purple-500'
    },
    {
      title: 'Manage Favorites',
      description: 'Save and organize trials that interest you',
      icon: Heart,
      action: () => navigate('/results'),
      color: 'bg-red-500'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">TrialMatch AI</h1>
            </div>
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
                  <span className="text-sm text-gray-600">
                    Welcome, {user?.email}
                  </span>
                  <button
                    onClick={() => navigate('/dashboard')}
                    className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-lg hover:bg-gray-100"
                  >
                    Dashboard
                  </button>
                  <button
                    onClick={() => navigate('/trials')}
                    className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-lg hover:bg-gray-100"
                  >
                    Browse Trials
                  </button>
                  <button
                    onClick={handleLogout}
                    className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-lg hover:bg-gray-100"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <div>
                  <button
                    onClick={() => navigate('/trials')}
                    className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-lg hover:bg-gray-100"
                  >
                    Browse Trials
                  </button>
                  <button
                    onClick={() => navigate('/login')}
                    className="text-gray-600 hover:text-gray-900 m-12 px-3 py-2 rounded-lg hover:bg-gray-100"
                  >
                    Sign In
                  </button>
                  <button
                    onClick={() => navigate('/register')}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                  >
                    Get Started
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Find Clinical Trials That
            <span className="text-blue-600"> Match Your Condition</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Upload your medical records and let our AI-powered platform find the most relevant
            clinical trials for your specific medical condition. Get personalized matches with
            detailed explanations.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => navigate(isAuthenticated ? '/upload' : '/register')}
              className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 text-lg font-medium"
            >
              {isAuthenticated ? 'Upload Medical Records' : 'Get Started'}
            </button>
            <button
              onClick={() => navigate('/trials')}
              className="bg-white text-blue-600 px-8 py-4 rounded-lg border-2 border-blue-600 hover:bg-blue-50 text-lg font-medium"
            >
              Browse All Trials
            </button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {features.map((feature, index) => (
            <div
              key={index}
              onClick={feature.action}
              className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow cursor-pointer border border-gray-100"
            >
              <div className={`w-12 h-12 ${feature.color} rounded-lg flex items-center justify-center mb-4`}>
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* How It Works */}
        <div className="bg-white rounded-2xl p-8 shadow-sm">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">1</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Upload Documents
              </h3>
              <p className="text-gray-600">
                Securely upload your medical records, test results, and other relevant documents.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-green-600">2</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                AI Analysis
              </h3>
              <p className="text-gray-600">
                Our AI extracts key medical information and builds your comprehensive profile.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-purple-600">3</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Get Matches
              </h3>
              <p className="text-gray-600">
                Receive personalized trial matches with detailed explanations and contact information.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center mt-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Find Your Match?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of patients who have found relevant clinical trials through our platform.
          </p>
          <button
            onClick={() => navigate(isAuthenticated ? '/dashboard' : '/register')}
            className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 text-lg font-medium"
          >
            {isAuthenticated ? 'Go to Dashboard' : 'Get Started'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
