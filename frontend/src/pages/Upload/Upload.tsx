import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, ArrowRight, CheckCircle } from 'lucide-react';
import DocumentUpload from '../../components/DocumentUpload';

const Upload = () => {
  const navigate = useNavigate();
  const [uploadedDocuments, setUploadedDocuments] = useState<string[]>([]);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleUploadSuccess = (documentId: string) => {
    setUploadedDocuments(prev => [...prev, documentId]);
    setShowSuccess(true);
    
    // Hide success message after 3 seconds
    setTimeout(() => setShowSuccess(false), 3000);
  };

  const handleUploadError = (error: string) => {
    // You can implement a toast notification system here
    console.error('Upload error:', error);
    alert(`Upload failed: ${error}`);
  };

  const handleContinue = () => {
    if (uploadedDocuments.length > 0) {
      navigate('/profile');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-blue-100 p-3 rounded-full">
              <FileText className="w-8 h-8 text-blue-600" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Upload Medical Documents
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Upload your medical reports, test results, or prescriptions. 
            Our AI will extract relevant information to help match you with clinical trials.
          </p>
        </div>

        {/* Success Message */}
        {showSuccess && (
          <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
              <p className="text-green-800">
                Document uploaded and processed successfully!
              </p>
            </div>
          </div>
        )}

        {/* Upload Component */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <DocumentUpload
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
          />
        </div>

        {/* Instructions */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            What documents can I upload?
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Medical Reports</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Blood test results</li>
                <li>• Imaging reports (CT, MRI, X-ray)</li>
                <li>• Pathology reports</li>
                <li>• Biopsy results</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Other Documents</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Prescription records</li>
                <li>• Discharge summaries</li>
                <li>• Treatment history</li>
                <li>• Doctor's notes</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Privacy Notice */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
          <h3 className="font-medium text-blue-900 mb-2">Privacy & Security</h3>
          <p className="text-sm text-blue-800">
            Your medical documents are encrypted and stored securely. We only extract 
            relevant medical information needed for trial matching. You can delete 
            your documents at any time.
          </p>
        </div>

        {/* Continue Button */}
        {uploadedDocuments.length > 0 && (
          <div className="text-center">
            <button
              onClick={handleContinue}
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              View My Medical Profile
              <ArrowRight className="w-4 h-4 ml-2" />
            </button>
            <p className="text-sm text-gray-500 mt-2">
              {uploadedDocuments.length} document{uploadedDocuments.length !== 1 ? 's' : ''} processed
            </p>
          </div>
        )}

        {/* Skip Option */}
        <div className="text-center mt-6">
          <button
            onClick={() => navigate('/trials')}
            className="text-gray-500 hover:text-gray-700 text-sm underline"
          >
            Skip for now and browse trials
          </button>
        </div>
      </div>
    </div>
  );
};

export default Upload;
