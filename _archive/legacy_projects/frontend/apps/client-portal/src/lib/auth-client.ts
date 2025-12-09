// Auth Client for FastAPI Brain Gateway
// Handles all authentication operations with multi-tenancy support

import type {
  User,
  LoginCredentials,
  SignupData,
  AuthResponse,
  AuthError,
  Tenant
} from './types/auth'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ||
                     process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL ||
                     '/api'

/**
 * SECURITY UPDATE: Token storage changed from localStorage to memory
 * - Access tokens stored in memory only (XSS-proof)
 * - Refresh tokens stored in HttpOnly cookies (backend-managed)
 * - Lost on page refresh → Auto-refresh using refresh token cookie
 */
class AuthClient {
  // Store access token in memory only (NOT localStorage)
  private accessToken: string | null = null

  /**
   * Get stored access token from memory
   * SECURITY: Not accessible via localStorage (XSS-proof)
   */
  getAccessToken(): string | null {
    return this.accessToken
  }

  /**
   * Store access token in memory
   * SECURITY: Lost on page refresh, requires token refresh
   */
  setAccessToken(token: string): void {
    this.accessToken = token
  }

  /**
   * Remove access token from memory
   */
  clearAccessToken(): void {
    this.accessToken = null
  }

  /**
   * Get headers with auth token
   */
  private getHeaders(): HeadersInit {
    const token = this.getAccessToken()
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    }
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    return headers
  }

  /**
   * Login with email and password
   * SECURITY: Refresh token stored in HttpOnly cookie (backend-managed)
   * Access token returned in response body and stored in memory
   */
  async login(credentials: LoginCredentials): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Required to receive/send HttpOnly cookies
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      const error: AuthError = await response.json().catch(() => ({ error: 'Login failed' }))
      throw new Error(error.message || error.error || 'Login failed')
    }

    const result: any = await response.json()

    // Handle standardized response format
    if (!result.success) {
      throw new Error(result.error || 'Invalid email or password')
    }

    // Store access token in memory (refresh token in HttpOnly cookie automatically)
    // Handle both response formats: {data: {access_token}} and {token}
    const accessToken = result.data?.access_token || result.token || result.access_token
    if (accessToken) {
      this.setAccessToken(accessToken)
    }

    // Return user data from response
    // Handle both formats: {data: {user}} and {user}
    return result.data?.user || result.user
  }

  /**
   * Register new user account
   * SECURITY: Refresh token stored in HttpOnly cookie (backend-managed)
   */
  async signup(data: SignupData): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      const error: AuthError = await response.json().catch(() => ({ error: 'Registration failed' }))
      throw new Error(error.message || 'Registration failed')
    }

    const result: any = await response.json()

    // Handle standardized response format
    if (!result.success) {
      throw new Error(result.error || 'Registration failed')
    }

    // Store access token in memory
    // Handle both response formats: {data: {access_token}} and {token}
    const accessToken = result.data?.access_token || result.token || result.access_token
    if (accessToken) {
      this.setAccessToken(accessToken)
    }

    // Return user data from response
    // Handle both formats: {data: {user}} and {user}
    return result.data?.user || result.user
  }

  /**
   * Logout current user
   * SECURITY: Clears access token from memory and HttpOnly cookie from backend
   */
  async logout(): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: this.getHeaders(),
        credentials: 'include', // Send HttpOnly cookie to backend for revocation
      })

      if (!response.ok) {
        console.error('Logout endpoint failed, but clearing local state')
      }
    } catch (error) {
      console.error('Logout request failed:', error)
    } finally {
      // Always clear access token from memory
      this.clearAccessToken()
    }
  }

  /**
   * Refresh access token using HttpOnly cookie
   * SECURITY: Refresh token sent automatically via HttpOnly cookie
   * NOTE: /auth/refresh endpoint not yet deployed - this will fail gracefully
   */
  async refreshAccessToken(): Promise<string | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        credentials: 'include', // Send HttpOnly cookie with refresh token
      })

      if (!response.ok) {
        // Refresh endpoint not available or refresh failed
        // User needs to login again
        this.clearAccessToken()
        return null
      }

      const result: any = await response.json()

      if (result.success && result.data && result.data.access_token) {
        this.setAccessToken(result.data.access_token)
        return result.data.access_token
      }

      return null
    } catch (error) {
      // Token refresh not available - fail silently
      this.clearAccessToken()
      return null
    }
  }

  /**
   * Get current authenticated user
   * SECURITY: Uses in-memory access token
   * NOTE: No auto-refresh - returns null if no token (user must login)
   */
  async getCurrentUser(): Promise<User | null> {
    try {
      const token = this.getAccessToken()

      // If no token in memory, return null (user needs to login)
      if (!token) {
        return null
      }

      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: this.getHeaders(),
        credentials: 'include',
      })

      if (!response.ok) {
        // Token invalid or expired - clear it and return null
        this.clearAccessToken()
        return null
      }

      const data: any = await response.json()

      // Handle different response formats
      if (data.user) return data.user
      if (data.success && data.data) return data.data.user || data.data

      return data // Return as-is if it's already a user object
    } catch (error) {
      console.error('Failed to get current user:', error)
      this.clearAccessToken()
      return null
    }
  }

  /**
   * Check if user is authenticated
   */
  async isAuthenticated(): Promise<boolean> {
    const user = await this.getCurrentUser()
    return !!user
  }

  /**
   * Verify token validity
   */
  async verifyToken(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/verify`, {
        headers: this.getHeaders(),
        credentials: 'include',
      })
      return response.ok
    } catch {
      return false
    }
  }

  /**
   * Request password reset
   */
  async forgotPassword(email: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/auth/forgot-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    })

    if (!response.ok) {
      const error: AuthError = await response.json().catch(() => ({ error: 'Password reset request failed' }))
      throw new Error(error.message || 'Password reset request failed')
    }
  }

  /**
   * Reset password with token
   */
  async resetPassword(token: string, password: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/auth/reset-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token, password }),
    })

    if (!response.ok) {
      const error: AuthError = await response.json().catch(() => ({ error: 'Password reset failed' }))
      throw new Error(error.message || 'Password reset failed')
    }
  }

  /**
   * Verify email with token
   */
  async verifyEmail(token: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/auth/verify-email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token }),
    })

    if (!response.ok) {
      const error: AuthError = await response.json().catch(() => ({ error: 'Email verification failed' }))
      throw new Error(error.message || 'Email verification failed')
    }
  }

  /**
   * Get user's tenants (for multi-tenancy)
   */
  async getTenants(): Promise<Tenant[]> {
    const response = await fetch(`${API_BASE_URL}/auth/tenants`, {
      headers: this.getHeaders(),
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error('Failed to fetch tenants')
    }

    return response.json()
  }

  /**
   * Switch active tenant
   */
  async switchTenant(tenantId: string): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/switch-tenant`, {
      method: 'POST',
      headers: this.getHeaders(),
      credentials: 'include',
      body: JSON.stringify({ tenant_id: tenantId }),
    })

    if (!response.ok) {
      const error: AuthError = await response.json().catch(() => ({ error: 'Failed to switch tenant' }))
      throw new Error(error.message || 'Failed to switch tenant')
    }

    const result: any = await response.json()

    // Handle standardized response
    if (!result.success) {
      throw new Error(result.error || 'Failed to switch tenant')
    }

    // Update access token if new one provided
    // Handle both response formats: {data: {access_token}} and {token}
    const accessToken = result.data?.access_token || result.token || result.access_token
    if (accessToken) {
      this.setAccessToken(accessToken)
    }

    // Return user data from response
    // Handle both formats: {data: {user}} and {user}
    return result.data?.user || result.user
  }
}

// Export singleton instance
export const authClient = new AuthClient()

// Export class for type inference
export type { AuthClient }
