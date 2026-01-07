import { create } from 'zustand';
import { authService } from '../services/auth';
import { User } from '../types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;

  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuthStatus: () => Promise<void>;
  setError: (error: string | null) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  loading: false,
  error: null,

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const token = await authService.login({ email, password });
      const user = await authService.getCurrentUser();
      set({ user, isAuthenticated: true, loading: false });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Login failed';
      set({ loading: false, error: errorMessage });
      throw new Error(errorMessage);
    }
  },

  register: async (email, password) => {
    set({ loading: true, error: null });
    try {
      await authService.register({ email, password });
      // Log in immediately after registration to get the token
      const tokenData = await authService.login({ email, password });
      const user = await authService.getCurrentUser();
      set({ user, isAuthenticated: true, loading: false });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Registration failed';
      set({ loading: false, error: errorMessage });
      throw new Error(errorMessage);
    }
  },

  logout: () => {
    authService.logout();
    set({ user: null, isAuthenticated: false, loading: false });
  },

  checkAuthStatus: async () => {
    if (authService.isAuthenticated()) {
      try {
        const user = await authService.getCurrentUser();
        set({ user, isAuthenticated: true });
      } catch (error) {
        // If token is invalid, logout user
        authService.logout();
        set({ user: null, isAuthenticated: false });
      }
    }
  },

  setError: (error) => set({ error }),
}));

// Create a custom hook for easier usage
export const useAuth = () => useAuthStore();