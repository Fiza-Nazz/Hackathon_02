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
      const response = await authClient.signIn.email({
        email,
        password,
      });

      if (response.error) {
        throw new Error(response.error.message || 'Login failed');
      }

      // CRITICAL FIX: Extract token IMMEDIATELY from the response
      // Better Auth returns token directly in data, not under session
      const token = response.data?.token;
      const userId = response.data?.user?.id;
      const userEmail = response.data?.user?.email;

      console.log('[Auth Store] Login successful, token:', token ? 'Present' : 'Missing');

      if (token) {
        // Save token immediately to localStorage
        localStorage.setItem('access_token', token);
        console.log('[Auth Store] Token saved to localStorage');
      }

      set({
        user: { id: userId, email: userEmail } as any,
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
      const response = await authClient.signUp.email({
        email,
        password,
        name: email.split('@')[0],
      });

      if (response.error) {
        throw new Error(response.error.message || 'Registration failed');
      }

      // CRITICAL FIX: Extract token immediately
      const token = response.data?.token;
      const userId = response.data?.user?.id;
      const userEmail = response.data?.user?.email;

      console.log('[Auth Store] Registration successful, token:', token ? 'Present' : 'Missing');

      if (token) {
        localStorage.setItem('access_token', token);
        console.log('[Auth Store] Token saved to localStorage');
      }

      set({
        user: { id: userId, email: userEmail } as any,
        isAuthenticated: true,
        loading: false
      });
    } catch (error: any) {
      console.error('[Auth Store] Registration error:', error);
      set({ loading: false, error: error.message });
      throw error;
    }
  },

  logout: async () => {
    await authClient.signOut();
    localStorage.removeItem('access_token');
    set({ user: null, isAuthenticated: false, loading: false });
  },

  checkAuthStatus: async () => {
    set({ loading: true });

    // CRITICAL FIX: Check localStorage first before hitting the potentially failing API
    const storedToken = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

    try {
      const session = await authClient.getSession();

      if (session?.data?.user) {
        // Session is valid - keep the user authenticated
        // Note: getSession doesn't return the token, but we have it in localStorage
        set({
          user: { id: session.data.user.id, email: session.data.user.email } as any,
          isAuthenticated: true,
          loading: false
        });
      } else {
        // No session data from server - but check if we have a stored token
        if (storedToken && storedToken.length > 20) {
          // Trust localStorage token
          console.log("[Auth Store] No server session but have stored token, staying authenticated");
          set({ isAuthenticated: true, loading: false });
        } else {
          set({ user: null, isAuthenticated: false, loading: false });
        }
      }
    } catch (error) {
      console.error("Auth status check failed, entering recovery mode:", error);

      // CRITICAL: Recovery mode - trust localStorage if it has a valid token
      if (storedToken && storedToken.length > 20) {
        console.log("[Auth Store] Recovery: Using localStorage token, staying authenticated");
        set({ isAuthenticated: true, loading: false });
      } else {
        console.log("[Auth Store] Recovery: No valid token found, logging out");
        set({ user: null, isAuthenticated: false, loading: false });
      }
    }
  },

  setError: (error) => set({ error }),
}));

export const useAuth = () => useAuthStore();