import api from './api';
import { Task } from '../types';

export const taskService = {
  // Get all tasks for current user
  async getTasks(): Promise<Task[]> {
    const response = await api.get('/tasks/', {
      params: { _t: new Date().getTime() }
    });
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