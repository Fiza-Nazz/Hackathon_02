import axios from 'axios';
import { authClient } from '@/lib/auth-client';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://fizu123-todo-backend.hf.space';

// Unified Alpha-Grade API Instance
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  }
});

api.interceptors.request.use(
  async (config) => {
    let token: string | undefined;

    // ONLY check localStorage - never hit Better Auth session API
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('access_token');
      if (stored && stored.length > 10) {
        token = stored;
      }
    }

    if (token) {
      config.headers.Authorization = `Bearer ${token.trim()}`;
    } else {
      console.warn("[API Engine] No token found in localStorage, request may fail.");
    }

    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error("[API Engine] 401 Unauthorized Detected - Neural Link Severed");
      // Don't redirect immediately to avoid loops, let the store handle it
    }
    return Promise.reject(error);
  }
);

export default api;