import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, FileText, Search, ArrowRight } from 'lucide-react';
import MedicalProfile from '../../components/MedicalProfile';
import DocumentList from '../../components/DocumentList';

const Profile: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'profile' | 'documents'>('profile');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleDocumentDeleted = () => {
    // Refresh medical profile when document is deleted
    setRefreshTrigger(prev => prev + 1);
  };

  const handleFindTrials = () => {
    navigate('/trials');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-blue-100 p-3 rounded-full">
              <User className="w-8 h-8 text-blue-600" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            My Medical Profile
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Review your medical information and uploaded documents. 
            This information helps us find the most relevant clinical trials for you.
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-lg shadow-sm mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              <button
                onClick={() => setActiveTab('profile')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'profile'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center">
                  <User className="w-4 h-4 mr-2" />
                  Medical Profile
                </div>
              </button>
              <button
                onClick={() => setActiveTab('documents')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'documents'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center">
                  <FileText className="w-4 h-4 mr-2" />
                  Documents
                </div>
              </button>
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'profile' && (
              <MedicalProfile refreshTrigger={refreshTrigger} />
            )}
            
            {activeTab === 'documents' && (
              <DocumentList 
                onDocumentDeleted={handleDocumentDeleted}
                refreshTrigger={refreshTrigger}
              />
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/upload')}
            className="inline-flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <FileText className="w-4 h-4 mr-2" />
            Upload More Documents
          </button>
          
          <button
            onClick={handleFindTrials}
            className="inline-flex items-center justify-center px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors"
          >
            <Search className="w-4 h-4 mr-2" />
            Find Clinical Trials
            <ArrowRight className="w-4 h-4 ml-2" />
          </button>
        </div>

        {/* Help Section */}
        <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-medium text-blue-900 mb-3">
            How does this work?
          </h3>
          <div className="grid md:grid-cols-3 gap-6 text-sm text-blue-800">
            <div>
              <div className="bg-blue-100 w-8 h-8 rounded-full flex items-center justify-center mb-2">
                <span className="font-bold">1</span>
              </div>
              <h4 className="font-medium mb-1">Upload Documents</h4>
              <p>Upload your medical reports, test results, and prescriptions.</p>
            </div>
            <div>
              <div className="bg-blue-100 w-8 h-8 rounded-full flex items-center justify-center mb-2">
                <span className="font-bold">2</span>
              </div>
              <h4 className="font-medium mb-1">AI Processing</h4>
              <p>Our AI extracts relevant medical information from your documents.</p>
            </div>
            <div>
              <div className="bg-blue-100 w-8 h-8 rounded-full flex items-center justify-center mb-2">
                <span className="font-bold">3</span>
              </div>
              <h4 className="font-medium mb-1">Find Trials</h4>
              <p>Get matched with clinical trials that are relevant to your condition.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;