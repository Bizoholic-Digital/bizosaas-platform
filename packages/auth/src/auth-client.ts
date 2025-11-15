/**
 * Brain Gateway Authentication Client
 * Handles all authentication operations via Brain Gateway API
 *
 * SECURITY: Stores access tokens in memory only (XSS-proof)
 * Refresh tokens are managed via HttpOnly cookies by the backend
 */

const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'https://api.bizoholic.com/api'

// In-memory token storage (lost on page refresh - requires token refresh)
let accessToken: string | null = null

export function getAccessToken(): string | null {
  return accessToken
}

export function setAccessToken(token: string): void {
  accessToken = token
}

export function clearAccessToken(): void {
  accessToken = null
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface SignupData {
  email: string
  password: string
  name: string
  company?: string
}

export interface AuthResponse {
  user: {
    id: string
    email: string
    name: string
    role: 'client' | 'partner' | 'moderator' | 'admin' | 'superadmin'
    tenant_id?: string
    tenant_name?: string
    avatar?: string
    created_at?: string
    updated_at?: string
  }
  message?: string
}

export interface PasswordResetRequest {
  email: string
}

export interface PasswordResetConfirm {
  token: string
  new_password: string
}

/**
 * Login user via Brain Gateway
 * Sets httpOnly cookie automatically via credentials: 'include'
 * Stores access token in memory
 */
export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
  const response = await fetch(`${BRAIN_GATEWAY_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Important: sends and receives cookies
    body: JSON.stringify(credentials),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Login failed' }))
    throw new Error(error.message || 'Login failed')
  }

  const result: any = await response.json()

  // Extract and store access token (handle multiple response formats)
  const token = result.token || result.access_token || result.data?.access_token
  if (token) {
    setAccessToken(token)
  }

  // Return response (with user data)
  return result
}

/**
 * Signup new user via Brain Gateway
 */
export async function signup(data: SignupData): Promise<AuthResponse> {
  const response = await fetch(`${BRAIN_GATEWAY_URL}/auth/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Signup failed' }))
    throw new Error(error.message || 'Signup failed')
  }

  return response.json()
}

/**
 * Logout user via Brain Gateway
 * Clears httpOnly cookie and access token from memory
 */
export async function logout(): Promise<void> {
  try {
    const response = await fetch(`${BRAIN_GATEWAY_URL}/auth/logout`, {
      method: 'POST',
      headers: accessToken ? { 'Authorization': `Bearer ${accessToken}` } : {},
      credentials: 'include',
    })

    if (!response.ok) {
      console.error('Logout endpoint failed, but clearing local state')
    }
  } catch (error) {
    console.error('Logout request failed:', error)
  } finally {
    // Always clear access token from memory
    clearAccessToken()
  }
}

/**
 * Get current authenticated user
 * Uses in-memory access token and httpOnly cookie
 */
export async function getCurrentUser(): Promise<AuthResponse | null> {
  try {
    const headers: HeadersInit = {}
    if (accessToken) {
      headers['Authorization'] = `Bearer ${accessToken}`
    }

    const response = await fetch(`${BRAIN_GATEWAY_URL}/auth/me`, {
      method: 'GET',
      headers,
      credentials: 'include',
    })

    if (!response.ok) {
      // Token invalid or expired - clear it
      if (response.status === 401) {
        clearAccessToken()
      }
      return null
    }

    return response.json()
  } catch (error) {
    return null
  }
}

/**
 * Request password reset email
 */
export async function requestPasswordReset(data: PasswordResetRequest): Promise<{ message: string }> {
  const response = await fetch(`${BRAIN_GATEWAY_URL}/auth/password-reset/request`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }))
    throw new Error(error.message || 'Password reset request failed')
  }

  return response.json()
}

/**
 * Confirm password reset with token
 */
export async function confirmPasswordReset(data: PasswordResetConfirm): Promise<{ message: string }> {
  const response = await fetch(`${BRAIN_GATEWAY_URL}/auth/password-reset/confirm`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Reset failed' }))
    throw new Error(error.message || 'Password reset failed')
  }

  return response.json()
}

/**
 * Verify email with token
 */
export async function verifyEmail(token: string): Promise<{ message: string }> {
  const response = await fetch(`${BRAIN_GATEWAY_URL}/auth/verify-email/${token}`, {
    method: 'POST',
    credentials: 'include',
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Verification failed' }))
    throw new Error(error.message || 'Email verification failed')
  }

  return response.json()
}

export interface Tenant {
  id: string
  name: string
  slug: string
  status: string
  created_at?: string
}

/**
 * Get all tenants for current user
 */
export async function getTenants(): Promise<Tenant[]> {
  const response = await fetch(`${BRAIN_GATEWAY_URL}/auth/tenants`, {
    method: 'GET',
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('Failed to load tenants')
  }

  return response.json()
}

/**
 * Switch to a different tenant
 */
export async function switchTenant(tenantId: string): Promise<AuthResponse> {
  const response = await fetch(`${BRAIN_GATEWAY_URL}/auth/switch-tenant/${tenantId}`, {
    method: 'POST',
    credentials: 'include',
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Switch failed' }))
    throw new Error(error.message || 'Failed to switch tenant')
  }

  return response.json()
}

/**
 * Brain Gateway Auth Client - consolidated API
 */
export const authClient = {
  login,
  signup,
  logout,
  getCurrentUser,
  requestPasswordReset,
  confirmPasswordReset,
  verifyEmail,
  getTenants,
  switchTenant,
  getAccessToken,
  setAccessToken,
  clearAccessToken,
}
