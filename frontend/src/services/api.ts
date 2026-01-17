import axios from 'axios';
import { authClient } from '@/lib/auth-client';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create an axios instance
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
});

// Request interceptor to add token to requests
api.interceptors.request.use(
  async (config) => {
    // Try to get token from Better Auth session first
    const session = await authClient.getSession();
    // @ts-ignore - token might be in session depending on plugin config
    const token = session.data?.session?.token || localStorage.getItem('access_token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be expired, clear it
      localStorage.removeItem('access_token');
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

export default api;