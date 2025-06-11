export interface User {
  id: number
  username?: string
  email: string
}

export interface Task {
  id: number
  title: string
  description: string
  completed: boolean
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  title: string
  description: string
}

export interface TaskUpdate {
  title?: string
  description?: string
  completed?: boolean
}

export interface UserCreate {
  username: string
  email: string
  password: string
}

export interface LoginCredentials {
  username?: string
  email?: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
} 