import { create } from 'zustand';
import { authClient } from '@/lib/auth-client';
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
  loading: true,
  error: null,

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      // RADICAL FIX: Call our direct auth endpoint instead of Better Auth
      const response = await fetch('/api/auth-direct/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Login failed');
      }

      const token = data.token;
      const user = data.user;

      console.log('[Auth Store - DIRECT] Login successful, token:', token ? 'Present' : 'Missing');

      if (token) {
        localStorage.setItem('access_token', token);
        console.log('[Auth Store - DIRECT] Token saved to localStorage');
      }

      set({
        user: { id: user.id, email: user.email } as any,
        isAuthenticated: true,
        loading: false
      });
    } catch (error: any) {
      console.error('[Auth Store - DIRECT] Login error:', error);
      set({ loading: false, error: error.message });
      throw error;
    }
  },

  register: async (email, password) => {
    set({ loading: true, error: null });
    try {
      // RADICAL FIX: Call our direct auth endpoint
      const response = await fetch('/api/auth-direct/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Registration failed');
      }

      const token = data.token;
      const user = data.user;

      console.log('[Auth Store - DIRECT] Registration successful, token:', token ? 'Present' : 'Missing');

      if (token) {
        localStorage.setItem('access_token', token);
        console.log('[Auth Store - DIRECT] Token saved to localStorage');
      }

      set({
        user: { id: user.id, email: user.email } as any,
        isAuthenticated: true,
        loading: false
      });
    } catch (error: any) {
      console.error('[Auth Store - DIRECT] Registration error:', error);
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

    // RADICAL FIX: Only check localStorage, don't call any server-side session API
    const storedToken = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

    if (storedToken && storedToken.length > 20) {
      console.log("[Auth Store - DIRECT] Valid token found in localStorage, user is authenticated");
      set({ isAuthenticated: true, loading: false });
    } else {
      console.log("[Auth Store - DIRECT] No valid token, user must login");
      set({ user: null, isAuthenticated: false, loading: false });
    }
  },

  setError: (error) => set({ error }),
}));

export const useAuth = () => useAuthStore();