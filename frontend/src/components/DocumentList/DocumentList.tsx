import React, { useState, useEffect } from 'react';
import { File, Download, Trash2, Clock, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';

interface Document {
  id: string;
  file_name: string;
  file_type: string;
  file_size: number;
  processing_status: 'pending' | 'processing' | 'completed' | 'failed';
  processing_error?: string;
  created_at: string;
  updated_at: string;
}

interface DocumentListProps {
  onDocumentDeleted?: (documentId: string) => void;
  refreshTrigger?: number;
}

const DocumentList: React.FC<DocumentListProps> = ({ 
  onDocumentDeleted,
  refreshTrigger = 0 
}) => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingIds, setDeletingIds] = useState<Set<string>>(new Set());

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/documents');
      
      if (!response.ok) {
        throw new Error('Failed to fetch documents');
      }
      
      const data = await response.json();
      setDocuments(data.documents || []);
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load documents';
      setError(errorMessage);
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [refreshTrigger]);

  const handleDelete = async (documentId: string) => {
    if (!confirm('Are you sure you want to delete this document?')) {
      return;
    }

    setDeletingIds(prev => new Set(prev).add(documentId));

    try {
      const response = await fetch(`/api/documents/${documentId}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        throw new Error('Failed to delete document');
      }

      // Remove from local state
      setDocuments(prev => prev.filter(doc => doc.id !== documentId));
      onDocumentDeleted?.(documentId);

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete document';
      alert(`Delete failed: ${errorMessage}`);
      console.error('Error deleting document:', err);
    } finally {
      setDeletingIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(documentId);
        return newSet;
      });
    }
  };

  const handleDownload = async (documentId: string, fileName: string) => {
    try {
      const response = await fetch(`/api/documents/${documentId}/download`);
      
      if (!response.ok) {
        throw new Error('Failed to get download URL');
      }
      
      const data = await response.json();
      
      // Open download URL in new tab
      window.open(data.download_url, '_blank');
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to download document';
      alert(`Download failed: ${errorMessage}`);
      console.error('Error downloading document:', err);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusIcon = (status: Document['processing_status']) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-4 h-4 text-yellow-500" />;
      case 'processing':
        return <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'failed':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      default:
        return <File className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusText = (status: Document['processing_status']) => {
    switch (status) {
      case 'pending':
        return 'Pending';
      case 'processing':
        return 'Processing...';
      case 'completed':
        return 'Completed';
      case 'failed':
        return 'Failed';
      default:
        return 'Unknown';
    }
  };

  const getStatusColor = (status: Document['processing_status']) => {
    switch (status) {
      case 'pending':
        return 'text-yellow-600 bg-yellow-50';
      case 'processing':
        return 'text-blue-600 bg-blue-50';
      case 'completed':
        return 'text-green-600 bg-green-50';
      case 'failed':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <RefreshCw className="w-6 h-6 text-blue-500 animate-spin mr-2" />
        <span className="text-gray-600">Loading documents...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center">
          <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
          <div>
            <p className="text-red-800 font-medium">Error loading documents</p>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        </div>
        <button
          onClick={fetchDocuments}
          className="mt-3 text-red-600 hover:text-red-800 text-sm underline"
        >
          Try again
        </button>
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="text-center py-8">
        <File className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No documents uploaded</h3>
        <p className="text-gray-500">
          Upload your first medical document to get started with trial matching.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">
          My Documents ({documents.length})
        </h2>
        <button
          onClick={fetchDocuments}
          className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
        >
          <RefreshCw className="w-4 h-4 mr-1" />
          Refresh
        </button>
      </div>

      <div className="space-y-3">
        {documents.map((document) => (
          <div
            key={document.id}
            className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3 flex-1 min-w-0">
                <File className="w-8 h-8 text-blue-500 flex-shrink-0" />
                
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-medium text-gray-900 truncate">
                    {document.file_name}
                  </h3>
                  <div className="flex items-center space-x-4 mt-1">
                    <span className="text-xs text-gray-500">
                      {formatFileSize(document.file_size)}
                    </span>
                    <span className="text-xs text-gray-500">
                      {formatDate(document.created_at)}
                    </span>
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                {/* Status Badge */}
                <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(document.processing_status)}`}>
                  {getStatusIcon(document.processing_status)}
                  <span className="ml-1">{getStatusText(document.processing_status)}</span>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center space-x-1">
                  {document.processing_status === 'completed' && (
                    <button
                      onClick={() => handleDownload(document.id, document.file_name)}
                      className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                      title="Download document"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                  )}
                  
                  <button
                    onClick={() => handleDelete(document.id)}
                    disabled={deletingIds.has(document.id)}
                    className="p-1 text-gray-400 hover:text-red-600 transition-colors disabled:opacity-50"
                    title="Delete document"
                  >
                    {deletingIds.has(document.id) ? (
                      <RefreshCw className="w-4 h-4 animate-spin" />
                    ) : (
                      <Trash2 className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Error Message */}
            {document.processing_status === 'failed' && document.processing_error && (
              <div className="mt-3 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-700">
                <strong>Processing Error:</strong> {document.processing_error}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default DocumentList;