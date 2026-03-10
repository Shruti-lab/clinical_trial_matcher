import React, { useState, useEffect } from 'react';
import { User, Heart, Pill, FileText, Edit3, Save, X, RefreshCw, AlertCircle } from 'lucide-react';
import apiClient from '../../services/api';

interface MedicalProfile {
  id: string;
  user_id: string;
  age?: number;
  gender?: string;
  conditions: string[];
  medications: string[];
  test_results: Record<string, string>;
  medical_history: string[];
  location?: string;
  created_at: string;
  updated_at: string;
}

interface MedicalProfileProps {
  refreshTrigger?: number;
}

const MedicalProfile: React.FC<MedicalProfileProps> = ({ refreshTrigger = 0 }) => {
  const [profile, setProfile] = useState<MedicalProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [editForm, setEditForm] = useState<Partial<MedicalProfile>>({});

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.get('/profile');
      setProfile(response.data);
      
    } catch (err: any) {
      if (err.response?.status === 404) {
        // No profile exists yet
        setProfile(null);
        return;
      }
      
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to load profile';
      setError(errorMessage);
      console.error('Error fetching profile:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, [refreshTrigger]);

  const handleEdit = () => {
    setEditForm({
      age: profile?.age,
      gender: profile?.gender,
      location: profile?.location,
      conditions: [...(profile?.conditions || [])],
      medications: [...(profile?.medications || [])]
    });
    setEditing(true);
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      
      const response = await apiClient.put('/profile', editForm);
      setProfile(response.data);
      setEditing(false);
      setEditForm({});
      
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to save profile';
      alert(`Save failed: ${errorMessage}`);
      console.error('Error saving profile:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setEditing(false);
    setEditForm({});
  };

  const addCondition = () => {
    const condition = prompt('Enter a medical condition:');
    if (condition && condition.trim()) {
      setEditForm(prev => ({
        ...prev,
        conditions: [...(prev.conditions || []), condition.trim()]
      }));
    }
  };

  const removeCondition = (index: number) => {
    setEditForm(prev => ({
      ...prev,
      conditions: prev.conditions?.filter((_, i) => i !== index) || []
    }));
  };

  const addMedication = () => {
    const medication = prompt('Enter a medication:');
    if (medication && medication.trim()) {
      setEditForm(prev => ({
        ...prev,
        medications: [...(prev.medications || []), medication.trim()]
      }));
    }
  };

  const removeMedication = (index: number) => {
    setEditForm(prev => ({
      ...prev,
      medications: prev.medications?.filter((_, i) => i !== index) || []
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <RefreshCw className="w-6 h-6 text-blue-500 animate-spin mr-2" />
        <span className="text-gray-600">Loading medical profile...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center">
          <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
          <div>
            <p className="text-red-800 font-medium">Error loading profile</p>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        </div>
        <button
          onClick={fetchProfile}
          className="mt-3 text-red-600 hover:text-red-800 text-sm underline"
        >
          Try again
        </button>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="text-center py-8">
        <User className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No medical profile found</h3>
        <p className="text-gray-500 mb-4">
          Upload medical documents to automatically create your profile, or create one manually.
        </p>
        <button
          onClick={handleEdit}
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Edit3 className="w-4 h-4 mr-2" />
          Create Profile
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-900">Medical Profile</h2>
        {!editing && (
          <button
            onClick={handleEdit}
            className="inline-flex items-center px-3 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Edit3 className="w-4 h-4 mr-1" />
            Edit
          </button>
        )}
        {editing && (
          <div className="flex space-x-2">
            <button
              onClick={handleSave}
              disabled={saving}
              className="inline-flex items-center px-3 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
            >
              {saving ? (
                <RefreshCw className="w-4 h-4 mr-1 animate-spin" />
              ) : (
                <Save className="w-4 h-4 mr-1" />
              )}
              Save
            </button>
            <button
              onClick={handleCancel}
              className="inline-flex items-center px-3 py-2 text-sm bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              <X className="w-4 h-4 mr-1" />
              Cancel
            </button>
          </div>
        )}
      </div>

      {/* Demographics */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center mb-4">
          <User className="w-5 h-5 text-blue-500 mr-2" />
          <h3 className="text-lg font-medium text-gray-900">Demographics</h3>
        </div>
        
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
            {editing ? (
              <input
                type="number"
                value={editForm.age || ''}
                onChange={(e) => setEditForm(prev => ({ ...prev, age: parseInt(e.target.value) || undefined }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter age"
              />
            ) : (
              <p className="text-gray-900">{profile.age || 'Not specified'}</p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
            {editing ? (
              <select
                value={editForm.gender || ''}
                onChange={(e) => setEditForm(prev => ({ ...prev, gender: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            ) : (
              <p className="text-gray-900 capitalize">{profile.gender || 'Not specified'}</p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
            {editing ? (
              <input
                type="text"
                value={editForm.location || ''}
                onChange={(e) => setEditForm(prev => ({ ...prev, location: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter location"
              />
            ) : (
              <p className="text-gray-900">{profile.location || 'Not specified'}</p>
            )}
          </div>
        </div>
      </div>

      {/* Medical Conditions */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <Heart className="w-5 h-5 text-red-500 mr-2" />
            <h3 className="text-lg font-medium text-gray-900">Medical Conditions</h3>
          </div>
          {editing && (
            <button
              onClick={addCondition}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              + Add Condition
            </button>
          )}
        </div>
        
        {(editing ? editForm.conditions : profile.conditions)?.length ? (
          <div className="flex flex-wrap gap-2">
            {(editing ? editForm.conditions : profile.conditions)?.map((condition, index) => (
              <span
                key={index}
                className="inline-flex items-center px-3 py-1 bg-red-50 text-red-800 text-sm rounded-full"
              >
                {condition}
                {editing && (
                  <button
                    onClick={() => removeCondition(index)}
                    className="ml-2 text-red-600 hover:text-red-800"
                  >
                    <X className="w-3 h-3" />
                  </button>
                )}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 italic">No conditions recorded</p>
        )}
      </div>

      {/* Medications */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <Pill className="w-5 h-5 text-green-500 mr-2" />
            <h3 className="text-lg font-medium text-gray-900">Medications</h3>
          </div>
          {editing && (
            <button
              onClick={addMedication}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              + Add Medication
            </button>
          )}
        </div>
        
        {(editing ? editForm.medications : profile.medications)?.length ? (
          <div className="flex flex-wrap gap-2">
            {(editing ? editForm.medications : profile.medications)?.map((medication, index) => (
              <span
                key={index}
                className="inline-flex items-center px-3 py-1 bg-green-50 text-green-800 text-sm rounded-full"
              >
                {medication}
                {editing && (
                  <button
                    onClick={() => removeMedication(index)}
                    className="ml-2 text-green-600 hover:text-green-800"
                  >
                    <X className="w-3 h-3" />
                  </button>
                )}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 italic">No medications recorded</p>
        )}
      </div>

      {/* Test Results */}
      {profile.test_results && Object.keys(profile.test_results).length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center mb-4">
            <FileText className="w-5 h-5 text-purple-500 mr-2" />
            <h3 className="text-lg font-medium text-gray-900">Test Results</h3>
          </div>
          
          <div className="grid md:grid-cols-2 gap-4">
            {Object.entries(profile.test_results).map(([test, value]) => (
              <div key={test} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0">
                <span className="text-sm font-medium text-gray-700 capitalize">
                  {test.replace('_', ' ')}
                </span>
                <span className="text-sm text-gray-900">{value}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Medical History */}
      {profile.medical_history && profile.medical_history.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center mb-4">
            <FileText className="w-5 h-5 text-gray-500 mr-2" />
            <h3 className="text-lg font-medium text-gray-900">Medical History</h3>
          </div>
          
          <div className="space-y-2">
            {profile.medical_history.map((entry, index) => (
              <p key={index} className="text-sm text-gray-700 p-2 bg-gray-50 rounded">
                {entry}
              </p>
            ))}
          </div>
        </div>
      )}

      {/* Last Updated */}
      <div className="text-center text-sm text-gray-500">
        Last updated: {new Date(profile.updated_at).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })}
      </div>
    </div>
  );
};

export default MedicalProfile;