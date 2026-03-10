import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X, AlertCircle, CheckCircle } from 'lucide-react';

interface DocumentUploadProps {
  onUploadSuccess?: (documentId: string) => void;
  onUploadError?: (error: string) => void;
  maxFileSize?: number;
  acceptedFileTypes?: string[];
}

interface UploadProgress {
  file: File;
  progress: number;
  status: 'uploading' | 'processing' | 'completed' | 'error';
  documentId?: string;
  error?: string;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onUploadSuccess,
  onUploadError,
  maxFileSize = 10 * 1024 * 1024, // 10MB
  acceptedFileTypes = ['application/pdf', 'image/jpeg', 'image/png']
}) => {
  const [uploads, setUploads] = useState<UploadProgress[]>([]);
  const [isDragActive, setIsDragActive] = useState(false);

  const validateFile = (file: File): string | null => {
    if (file.size > maxFileSize) {
      return `File size must be less than ${Math.round(maxFileSize / 1024 / 1024)}MB`;
    }
    
    if (!acceptedFileTypes.includes(file.type)) {
      return 'Only PDF, JPEG, and PNG files are allowed';
    }
    
    return null;
  };

  const uploadFile = async (file: File) => {
    // const uploadId = Date.now().toString();
    
    // Add to uploads list
    const newUpload: UploadProgress = {
      file,
      progress: 0,
      status: 'uploading'
    };
    
    setUploads(prev => [...prev, newUpload]);

    try {
      // Step 1: Get pre-signed upload URL
      const uploadResponse = await fetch('/api/documents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_name: file.name,
          file_type: file.type,
          file_size: file.size
        })
      });

      if (!uploadResponse.ok) {
        throw new Error('Failed to get upload URL');
      }

      const uploadData = await uploadResponse.json();
      
      // Step 2: Upload to S3 using pre-signed URL
      const formData = new FormData();
      
      // Add all the fields from the pre-signed URL
      Object.entries(uploadData.fields).forEach(([key, value]) => {
        formData.append(key, value as string);
      });
      
      // Add the file last
      formData.append('file', file);

      const s3Response = await fetch(uploadData.upload_url, {
        method: 'POST',
        body: formData
      });

      if (!s3Response.ok) {
        throw new Error('Failed to upload file to S3');
      }

      // Update progress to show upload complete
      setUploads(prev => prev.map(upload => 
        upload.file === file 
          ? { ...upload, progress: 100, status: 'processing', documentId: uploadData.document_id }
          : upload
      ));

      // Step 3: Trigger document processing
      const processResponse = await fetch(`/api/documents/${uploadData.document_id}/process`, {
        method: 'POST'
      });

      if (!processResponse.ok) {
        throw new Error('Failed to start document processing');
      }

      // Step 4: Poll for processing status
      await pollProcessingStatus(uploadData.document_id, file);

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Upload failed';
      
      setUploads(prev => prev.map(upload => 
        upload.file === file 
          ? { ...upload, status: 'error', error: errorMessage }
          : upload
      ));
      
      onUploadError?.(errorMessage);
    }
  };

  const pollProcessingStatus = async (documentId: string, file: File) => {
    const maxAttempts = 60; // 5 minutes with 5-second intervals
    let attempts = 0;

    const poll = async () => {
      try {
        const response = await fetch(`/api/documents/${documentId}/status`);
        
        if (!response.ok) {
          throw new Error('Failed to check processing status');
        }

        const statusData = await response.json();
        
        // Update progress
        setUploads(prev => prev.map(upload => 
          upload.file === file 
            ? { 
                ...upload, 
                progress: statusData.progress_percentage,
                status: statusData.processing_status === 'completed' ? 'completed' : 'processing',
                error: statusData.processing_error
              }
            : upload
        ));

        if (statusData.processing_status === 'completed') {
          onUploadSuccess?.(documentId);
          return;
        }

        if (statusData.processing_status === 'failed') {
          throw new Error(statusData.processing_error || 'Processing failed');
        }

        // Continue polling if still processing
        if (statusData.processing_status === 'processing' && attempts < maxAttempts) {
          attempts++;
          setTimeout(poll, 5000); // Poll every 5 seconds
        } else if (attempts >= maxAttempts) {
          throw new Error('Processing timeout');
        }

      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Processing failed';
        
        setUploads(prev => prev.map(upload => 
          upload.file === file 
            ? { ...upload, status: 'error', error: errorMessage }
            : upload
        ));
        
        onUploadError?.(errorMessage);
      }
    };

    // Start polling
    setTimeout(poll, 2000); // Initial delay of 2 seconds
  };

  const removeUpload = (file: File) => {
    setUploads(prev => prev.filter(upload => upload.file !== file));
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    acceptedFiles.forEach(file => {
      const error = validateFile(file);
      if (error) {
        onUploadError?.(error);
        return;
      }
      
      uploadFile(file);
    });
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxSize: maxFileSize,
    onDragEnter: () => setIsDragActive(true),
    onDragLeave: () => setIsDragActive(false),
    onDropAccepted: () => setIsDragActive(false),
    onDropRejected: () => setIsDragActive(false)
  });

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStatusIcon = (status: UploadProgress['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <File className="w-5 h-5 text-blue-500" />;
    }
  };

  const getStatusText = (upload: UploadProgress): string => {
    switch (upload.status) {
      case 'uploading':
        return 'Uploading...';
      case 'processing':
        return 'Processing document...';
      case 'completed':
        return 'Processing complete';
      case 'error':
        return upload.error || 'Upload failed';
      default:
        return '';
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Drop Zone */}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
          }
        `}
      >
        <input {...getInputProps()} />
        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-lg font-medium text-gray-700 mb-2">
          {isDragActive ? 'Drop files here' : 'Upload Medical Documents'}
        </p>
        <p className="text-sm text-gray-500 mb-4">
          Drag and drop your files here, or click to browse
        </p>
        <p className="text-xs text-gray-400">
          Supported formats: PDF, JPEG, PNG • Max size: {Math.round(maxFileSize / 1024 / 1024)}MB
        </p>
      </div>

      {/* Upload Progress */}
      {uploads.length > 0 && (
        <div className="mt-6 space-y-3">
          <h3 className="text-lg font-medium text-gray-900">Upload Progress</h3>
          {uploads.map((upload, index) => (
            <div key={index} className="bg-white border rounded-lg p-4 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(upload.status)}
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {upload.file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatFileSize(upload.file.size)}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeUpload(upload.file)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              
              {/* Progress Bar */}
              {upload.status !== 'error' && (
                <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-300 ${
                      upload.status === 'completed' ? 'bg-green-500' : 'bg-blue-500'
                    }`}
                    style={{ width: `${upload.progress}%` }}
                  />
                </div>
              )}
              
              {/* Status Text */}
              <p className={`text-sm ${
                upload.status === 'error' ? 'text-red-600' : 'text-gray-600'
              }`}>
                {getStatusText(upload)}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;