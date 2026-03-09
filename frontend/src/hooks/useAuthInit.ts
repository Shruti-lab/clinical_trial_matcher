import { useEffect } from 'react';
import { useAuthStore } from '../stores/authStore';

export const useAuthInit = () => {
  const { getCurrentUser, isAuthenticated } = useAuthStore();

  useEffect(() => {
    // Check if user is authenticated on app initialization
    const token = localStorage.getItem('auth_token');
    if (token && !isAuthenticated) {
      getCurrentUser();
    }
  }, [getCurrentUser, isAuthenticated]);
};