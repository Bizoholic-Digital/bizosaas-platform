/**
 * Base API Client for Brain Gateway
 * Handles common HTTP operations with proper error handling and authentication
 */

const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'https://api.bizoholic.com'

export interface ApiError {
  message: string
  status?: number
  details?: unknown
}

export interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean>
  timeout?: number
}

/**
 * Creates an ApiError from a Response object
 */
async function createApiError(response: Response): Promise<ApiError> {
  try {
    const errorData = await response.json()
    return {
      message: errorData.message || errorData.detail || `Request failed with status ${response.status}`,
      status: response.status,
      details: errorData,
    }
  } catch {
    return {
      message: `Request failed with status ${response.status}`,
      status: response.status,
    }
  }
}

/**
 * Base HTTP client with automatic error handling and authentication
 */
export class BaseApiClient {
  private baseUrl: string

  constructor(baseUrl: string = BRAIN_GATEWAY_URL) {
    this.baseUrl = baseUrl
  }

  /**
   * Makes an HTTP request to the Brain Gateway API
   */
  async request<T>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<T> {
    const {
      params,
      timeout = 30000,
      headers = {},
      ...fetchOptions
    } = options

    // Build URL with query parameters
    let url = `${this.baseUrl}${endpoint}`
    if (params) {
      const searchParams = new URLSearchParams()
      Object.entries(params).forEach(([key, value]) => {
        searchParams.append(key, String(value))
      })
      url += `?${searchParams.toString()}`
    }

    // Set up abort controller for timeout
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), timeout)

    try {
      const response = await fetch(url, {
        ...fetchOptions,
        headers: {
          'Content-Type': 'application/json',
          ...headers,
        },
        credentials: 'include', // Always include cookies for authentication
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        const error = await createApiError(response)
        throw error
      }

      // Handle no content responses
      if (response.status === 204 || response.headers.get('content-length') === '0') {
        return {} as T
      }

      return response.json()
    } catch (error) {
      clearTimeout(timeoutId)

      if (error instanceof Error && error.name === 'AbortError') {
        throw {
          message: 'Request timeout',
          status: 408,
        } as ApiError
      }

      throw error
    }
  }

  /**
   * GET request
   */
  async get<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' })
  }

  /**
   * POST request
   */
  async post<T>(
    endpoint: string,
    data?: unknown,
    options?: RequestOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  /**
   * PUT request
   */
  async put<T>(
    endpoint: string,
    data?: unknown,
    options?: RequestOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  /**
   * PATCH request
   */
  async patch<T>(
    endpoint: string,
    data?: unknown,
    options?: RequestOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  /**
   * DELETE request
   */
  async delete<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' })
  }
}

// Export singleton instance
export const apiClient = new BaseApiClient()
