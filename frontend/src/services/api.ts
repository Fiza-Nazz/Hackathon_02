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

    // 1. Aggressive Persistent Storage Check (Most Reliable on Vercel)
    if (typeof window !== 'undefined') {
      token = localStorage.getItem('access_token') || undefined;
    }

    // 2. Fallback to Session Cache if storage is empty
    if (!token) {
      try {
        const session = await authClient.getSession();
        token = session.data?.session?.token;
      } catch (err) {
        console.warn("[API Engine] Secondary session link failed, using guest context.");
      }
    }

    if (token) {
      config.headers.Authorization = `Bearer ${token.trim()}`;
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