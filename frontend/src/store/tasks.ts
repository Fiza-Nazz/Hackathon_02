import { create } from 'zustand';
import { taskService } from '../services/tasks';
import { Task } from '../types';

interface TasksState {
  tasks: Task[];
  loading: boolean;
  error: string | null;

  // Actions
  fetchTasks: () => Promise<void>;
  createTask: (taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at' | 'completed'> & { completed?: boolean }) => Promise<void>;
  updateTask: (id: number, taskData: Partial<Task>) => Promise<void>;
  deleteTask: (id: number) => Promise<void>;
  toggleTaskCompletion: (id: number) => Promise<void>;
  setError: (error: string | null) => void;
}

export const useTasksStore = create<TasksState>((set) => ({
  tasks: [],
  loading: false,
  error: null,

  fetchTasks: async () => {
    set({ loading: true, error: null });
    try {
      const tasks = await taskService.getTasks();
      set({ tasks, loading: false });
    } catch (error: any) {
      console.error('Neural Task Log Error:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to fetch tasks';
      set({ loading: false, error: errorMessage });
      throw new Error(errorMessage);
    }
  },

  createTask: async (taskData) => {
    set({ loading: true, error: null });
    try {
      const newTask = await taskService.createTask(taskData);
      set((state) => ({ tasks: [...state.tasks, newTask], loading: false }));
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to create task';
      set({ loading: false, error: errorMessage });
      throw new Error(errorMessage);
    }
  },

  updateTask: async (id, taskData) => {
    set({ loading: true, error: null });
    try {
      const updatedTask = await taskService.updateTask(id, taskData);
      set((state) => ({
        tasks: state.tasks.map(task => task.id === id ? updatedTask : task),
        loading: false,
      }));
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to update task';
      set({ loading: false, error: errorMessage });
      throw new Error(errorMessage);
    }
  },

  deleteTask: async (id) => {
    set({ loading: true, error: null });
    try {
      await taskService.deleteTask(id);
      set((state) => ({
        tasks: state.tasks.filter(task => task.id !== id),
        loading: false,
      }));
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to delete task';
      set({ loading: false, error: errorMessage });
      throw new Error(errorMessage);
    }
  },

  toggleTaskCompletion: async (id) => {
    set({ loading: true, error: null });
    try {
      const updatedTask = await taskService.toggleTaskCompletion(id);
      set((state) => ({
        tasks: state.tasks.map(task => task.id === id ? updatedTask : task),
        loading: false,
      }));
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to toggle task completion';
      set({ loading: false, error: errorMessage });
      throw new Error(errorMessage);
    }
  },

  setError: (error) => set({ error }),
}));

// Create a custom hook for easier usage
export const useTasks = () => useTasksStore();