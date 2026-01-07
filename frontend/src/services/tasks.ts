import axios from 'axios';
import { Task } from '../types';

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

export const taskService = {
  // Get all tasks for current user
  async getTasks(): Promise<Task[]> {
    const response = await api.get('/tasks/');
    return response.data;
  },

  // Create a new task
  async createTask(taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at' | 'completed'> & { completed?: boolean }): Promise<Task> {
    const response = await api.post('/tasks/', taskData);
    return response.data;
  },

  // Update a task
  async updateTask(id: number, taskData: Partial<Task>): Promise<Task> {
    const response = await api.put(`/tasks/${id}`, taskData);
    return response.data;
  },

  // Delete a task
  async deleteTask(id: number): Promise<void> {
    await api.delete(`/tasks/${id}`);
  },

  // Toggle task completion status
  async toggleTaskCompletion(id: number): Promise<Task> {
    const response = await api.patch(`/tasks/${id}/complete`);
    return response.data;
  },
};