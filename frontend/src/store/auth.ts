import { create } from 'zustand';
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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  loading: true,
  error: null,

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      // Backend returns { "access_token": "...", "token_type": "bearer" }
      const token = data.access_token;

      if (token) {
        localStorage.setItem('access_token', token);
      }

      // In a real app, we'd fetch /me to get full user details
      // For now, let's decode the token to get the user ID
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const payload = JSON.parse(window.atob(base64));

      set({
        user: { id: payload.sub, email: email } as any,
        isAuthenticated: true,
        loading: false
      });
    } catch (error: any) {
      console.error('[Auth Store] Login error:', error);
      set({ loading: false, error: error.message });
      throw error;
    }
  },

  register: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }

      const token = data.access_token;

      if (token) {
        localStorage.setItem('access_token', token);
      }

      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const payload = JSON.parse(window.atob(base64));

      set({
        user: { id: payload.sub, email: email } as any,
        isAuthenticated: true,
        loading: false
      });
    } catch (error: any) {
      console.error('[Auth Store] Registration error:', error);
      set({ loading: false, error: error.message });
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('access_token');
    set({ user: null, isAuthenticated: false, loading: false });
    window.location.href = '/login';
  },

  checkAuthStatus: async () => {
    set({ loading: true });

    const storedToken = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

    if (storedToken && storedToken.split('.').length === 3) {
      try {
        const base64Url = storedToken.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        const payload = JSON.parse(jsonPayload);
        const userId = payload.sub;

        set({
          isAuthenticated: true,
          loading: false,
          user: { id: userId, email: payload.email || 'operator@neural.net' } as any
        });
      } catch (e) {
        console.error("Failed to decode token:", e);
        localStorage.removeItem('access_token');
        set({ user: null, isAuthenticated: false, loading: false });
      }
    } else {
      set({ user: null, isAuthenticated: false, loading: false });
    }
  },

  setError: (error) => set({ error }),
}));

export const useAuth = () => useAuthStore();