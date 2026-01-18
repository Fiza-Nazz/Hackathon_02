import axios from 'axios';
import { LoginCredentials, RegisterData, Token, User } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create an axios instance
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
});

// Request interceptor to add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
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

export const authService = {
  // Register a new user
  async register(userData: RegisterData): Promise<User> {
    console.error("CRITICAL: Deprecated authService.register called. Use better-auth instead.");
    throw new Error("Use Better Auth frontend for registration");
  },

  // Login user and get token
  async login(credentials: LoginCredentials): Promise<Token> {
    console.error("CRITICAL: Deprecated authService.login called. Use better-auth instead.");
    throw new Error("Use Better Auth frontend for login");
  },

  // Logout user
  async logout(): Promise<void> {
    localStorage.removeItem('access_token');
  },

  // Get current user info
  async getCurrentUser(): Promise<User> {
    const response = await api.get('/users/me');
    return response.data;
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  },
};