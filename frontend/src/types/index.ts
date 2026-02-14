export interface User {
  id: number;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  category: string;
  user_id: number;
  created_at: string;
  updated_at: string;
  tags?: string[];
  due_date?: string;
  is_recurring?: boolean;
  recurring_pattern?: 'daily' | 'weekly' | 'monthly' | 'yearly';
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
}