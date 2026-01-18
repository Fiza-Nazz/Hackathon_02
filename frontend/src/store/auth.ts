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
  loading: false,
  error: null,

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const { data, error } = await authClient.signIn.email({
        email,
        password,
      });

      if (error) throw new Error(error.message || 'Login failed');

      // Better Auth JWT is usually in the session call or client storage
      const session = await authClient.getSession();
      const token = session.data?.session.token;
      if (token) localStorage.setItem('access_token', token);

      set({
        user: { id: data?.user.id, email: data?.user.email } as any,
        isAuthenticated: true,
        loading: false
      });
    } catch (error: any) {
      set({ loading: false, error: error.message });
      throw error;
    }
  },

  register: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const { data, error } = await authClient.signUp.email({
        email,
        password,
        name: email.split('@')[0], // Default name
      });

      if (error) throw new Error(error.message || 'Registration failed');

      const session = await authClient.getSession();
      const token = session.data?.session.token;
      if (token) localStorage.setItem('access_token', token);

      set({
        user: { id: data?.user.id, email: data?.user.email } as any,
        isAuthenticated: true,
        loading: false
      });
    } catch (error: any) {
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
    const session = await authClient.getSession();
    if (session?.data) {
      const token = session.data.session.token;
      if (token) localStorage.setItem('access_token', token);

      set({
        user: { id: session.data.user.id, email: session.data.user.email } as any,
        isAuthenticated: true
      });
    } else {
      localStorage.removeItem('access_token');
      set({ user: null, isAuthenticated: false });
    }
  },

  setError: (error) => set({ error }),
}));

export const useAuth = () => useAuthStore();