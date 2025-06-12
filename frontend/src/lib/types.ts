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

// Agentic System Types
export interface FileInfo {
  file_id: string
  filename: string
  file_size: number
  upload_time: string
  content_type: string
}

export interface UploadedFile {
  file_id: string
  filename: string
  content_type: string
  size: number
  upload_time: string
}

export interface ChatMessage {
  timestamp: string
  question: string
  answer: string
  agent_type: string
}

export interface ChatHistory {
  file_id: string
  conversations: ChatMessage[]
}

export interface QuestionRequest {
  file_id: string
  question: string
}

export interface AgentResponse {
  file_id: string
  question: string
  answer: string
  response_time: string
  agent_type: string
}

export interface AgentInfo {
  agent_id: string
  name: string
  description: string
  capabilities: string[]
  status: string
}



 