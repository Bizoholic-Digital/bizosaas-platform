/**
 * Shared API Client for BizOSaaS Frontend Services
 *
 * All frontend services communicate with backend via brain-gateway (API Gateway + CrewAI)
 * This client provides a consistent interface for making HTTP requests.
 */

export interface ApiClientConfig {
  baseURL: string
  timeout?: number
  headers?: Record<string, string>
}

export class ApiClient {
  private baseURL: string
  private timeout: number
  private defaultHeaders: Record<string, string>

  constructor(config: ApiClientConfig) {
    this.baseURL = config.baseURL || process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8001'
    this.timeout = config.timeout || 30000
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      ...config.headers
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`

    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), this.timeout)

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...this.defaultHeaders,
          ...options.headers
        },
        signal: controller.signal
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      clearTimeout(timeoutId)

      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Request timeout')
      }

      throw error
    }
  }

  async get<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' })
  }

  async post<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  async put<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  async patch<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  async delete<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' })
  }

  setAuthToken(token: string) {
    this.defaultHeaders['Authorization'] = `Bearer ${token}`
  }

  clearAuthToken() {
    delete this.defaultHeaders['Authorization']
  }
}

// Default instance
export const apiClient = new ApiClient({
  baseURL: process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8001'
})
