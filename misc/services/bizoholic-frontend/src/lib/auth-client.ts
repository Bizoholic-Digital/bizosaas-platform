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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api'

class AuthClient {
  /**
   * Login with email and password
   * Brain Gateway will set httpOnly cookies (access_token, refresh_token, tenant_id)
   */
  async login(credentials: LoginCredentials): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Important: Send/receive cookies
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      const error: AuthError = await response.json()
      throw new Error(error.message || 'Login failed')
    }

    const data: AuthResponse = await response.json()
    return data.user
  }

  /**
   * Register new user account
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
      const error: AuthError = await response.json()
      throw new Error(error.message || 'Registration failed')
    }

    const result: AuthResponse = await response.json()
    return result.user
  }

  /**
   * Logout current user
   * Brain Gateway will clear cookies
   */
  async logout(): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    })

    if (!response.ok) {
      console.error('Logout failed, but clearing local state')
    }
  }

  /**
   * Get current authenticated user
   * Validates session with Brain Gateway
   */
  async getCurrentUser(): Promise<User | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        credentials: 'include',
      })

      if (!response.ok) {
        return null
      }

      const user: User = await response.json()
      return user
    } catch (error) {
      console.error('Failed to get current user:', error)
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
      const error: AuthError = await response.json()
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
      const error: AuthError = await response.json()
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
      const error: AuthError = await response.json()
      throw new Error(error.message || 'Email verification failed')
    }
  }

  /**
   * Get user's tenants (for multi-tenancy)
   */
  async getTenants(): Promise<Tenant[]> {
    const response = await fetch(`${API_BASE_URL}/auth/tenants`, {
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
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ tenant_id: tenantId }),
    })

    if (!response.ok) {
      const error: AuthError = await response.json()
      throw new Error(error.message || 'Failed to switch tenant')
    }

    const data: AuthResponse = await response.json()
    return data.user
  }
}

// Export singleton instance
export const authClient = new AuthClient()
