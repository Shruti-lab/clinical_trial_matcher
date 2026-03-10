import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import apiClient from '../services/api';

export interface User {
  id: string;
  email: string;
  phone?: string;
  preferred_language: string;
  created_at: string;
  updated_at: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  getCurrentUser: () => Promise<void>;
  updateProfile: (profileData: ProfileUpdateData) => Promise<void>;
  clearError: () => void;
}

interface RegisterData {
  email: string;
  phone?: string;
  password: string;
  preferred_language: string;
}

interface ProfileUpdateData {
  phone?: string;
  preferred_language?: string;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await apiClient.post('/auth/login', {
            email,
            password
          });
          
          const { access_token, refresh_token } = response.data;
          
          // Store tokens
          localStorage.setItem('auth_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          
          // Get user info
          await get().getCurrentUser();
          
          set({ 
            isAuthenticated: true,
            isLoading: false,
            error: null 
          });
          
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 'Login failed';
          set({ 
            isLoading: false, 
            error: errorMessage,
            isAuthenticated: false,
            user: null 
          });
          throw error;
        }
      },

      register: async (userData: RegisterData) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await apiClient.post('/auth/register', userData);
          
          const { access_token, refresh_token } = response.data;
          
          // Store tokens
          localStorage.setItem('auth_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          
          // Get user info
          await get().getCurrentUser();
          
          set({ 
            isAuthenticated: true,
            isLoading: false,
            error: null 
          });
          
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 'Registration failed';
          set({ 
            isLoading: false, 
            error: errorMessage,
            isAuthenticated: false,
            user: null 
          });
          throw error;
        }
      },

      logout: () => {
        // Clear tokens
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        
        // Reset state
        set({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null
        });
      },

      refreshToken: async () => {
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (!refreshToken) {
          get().logout();
          return;
        }
        
        try {
          const response = await apiClient.post('/auth/refresh', {
            refresh_token: refreshToken
          });
          
          const { access_token, refresh_token: newRefreshToken } = response.data;
          
          // Update tokens
          localStorage.setItem('auth_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);
          
        } catch (error) {
          console.error('Token refresh failed:', error);
          get().logout();
          throw error;
        }
      },

      getCurrentUser: async () => {
        const token = localStorage.getItem('auth_token');
        
        if (!token) {
          set({ isAuthenticated: false, user: null });
          return;
        }
        
        try {
          const response = await apiClient.get('/auth/me');
          
          // Convert datetime objects to strings for frontend
          const userData = {
            ...response.data,
            created_at: new Date(response.data.created_at).toISOString(),
            updated_at: new Date(response.data.updated_at).toISOString()
          };
          
          set({
            user: userData,
            isAuthenticated: true,
            error: null
          });
          
        } catch (error: any) {
          console.error('Failed to get current user:', error);
          
          // If token is invalid, try to refresh
          if (error.response?.status === 401) {
            try {
              await get().refreshToken();
              // Retry getting user info
              const response = await apiClient.get('/auth/me');
              
              // Convert datetime objects to strings for frontend
              const userData = {
                ...response.data,
                created_at: new Date(response.data.created_at).toISOString(),
                updated_at: new Date(response.data.updated_at).toISOString()
              };
              
              set({
                user: userData,
                isAuthenticated: true,
                error: null
              });
            } catch (refreshError) {
              get().logout();
            }
          } else {
            set({ error: 'Failed to load user information' });
          }
        }
      },

      updateProfile: async (profileData: ProfileUpdateData) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await apiClient.put('/auth/profile', profileData);
          
          set({
            user: response.data,
            isLoading: false,
            error: null
          });
          
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 'Profile update failed';
          set({ 
            isLoading: false, 
            error: errorMessage 
          });
          throw error;
        }
      },

      clearError: () => {
        set({ error: null });
      }
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated
      })
    }
  )
);