import type { User, Task, TaskCreate, TaskUpdate, UserCreate, LoginCredentials, AuthResponse } from './types'

const API_BASE_URL = 'http://localhost:8000'

class ApiClient {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token')
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` })
    }
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`HTTP ${response.status}: ${errorText}`)
    }
    return response.json()
  }

  // Auth endpoints
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new URLSearchParams()
    formData.append('username', credentials.email || credentials.username || '')
    formData.append('password', credentials.password)

    const response = await fetch(`${API_BASE_URL}/auth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData
    })

    return this.handleResponse<AuthResponse>(response)
  }

  async register(userData: UserCreate): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData)
    })

    return this.handleResponse<AuthResponse>(response)
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: this.getAuthHeaders()
    })

    return this.handleResponse<User>(response)
  }

  // Task endpoints
  async getTasks(): Promise<Task[]> {
    const response = await fetch(`${API_BASE_URL}/tasks/get_tasks`, {
      headers: this.getAuthHeaders()
    })

    return this.handleResponse<Task[]>(response)
  }

  async getTask(id: number): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/tasks/get_task/${id}`, {
      headers: this.getAuthHeaders()
    })

    return this.handleResponse<Task>(response)
  }

  async createTask(taskData: TaskCreate): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/tasks/create_task`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(taskData)
    })

    return this.handleResponse<Task>(response)
  }

  async updateTask(id: number, taskData: TaskUpdate): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/tasks/update_task/${id}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(taskData)
    })

    return this.handleResponse<Task>(response)
  }

  async deleteTask(id: number): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/tasks/delete_task/${id}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders()
    })

    return this.handleResponse<{ message: string }>(response)
  }

  async getCompletedTasks(): Promise<Task[]> {
    const response = await fetch(`${API_BASE_URL}/tasks/get_completed_tasks`, {
      headers: this.getAuthHeaders()
    })

    return this.handleResponse<Task[]>(response)
  }

  async getPendingTasks(): Promise<Task[]> {
    const response = await fetch(`${API_BASE_URL}/tasks/get_pending_tasks`, {
      headers: this.getAuthHeaders()
    })

    return this.handleResponse<Task[]>(response)
  }

  async markTaskCompleted(id: number): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/tasks/mark_completed/${id}`, {
      method: 'PATCH',
      headers: this.getAuthHeaders()
    })

    return this.handleResponse<Task>(response)
  }

  async markTaskPending(id: number): Promise<Task> {
    // Используем обычное обновление, так как mark_pending endpoint может не существовать
    return this.updateTask(id, { completed: false })
  }
}

export const apiClient = new ApiClient() 