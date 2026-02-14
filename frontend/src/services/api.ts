import axios from 'axios';

// Use backend API for tasks (port 8000), not chatbot (port 8001)
const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  }
});

api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error("[API Engine] 401 Unauthorized - Redirecting to Login");
      if (typeof window !== 'undefined') {
        // Clear token if invalid
        localStorage.removeItem('access_token');
        // We could redirect here, but better to let the store handle state
      }
    }
    return Promise.reject(error);
  }
);

export default api;