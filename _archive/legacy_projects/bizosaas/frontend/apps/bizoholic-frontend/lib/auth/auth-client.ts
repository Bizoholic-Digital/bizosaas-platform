/**
 * BizOSaaS Authentication Client for Bizoholic
 * Handles all authentication operations via centralized Auth Service
 *
 * SECURITY: Stores access tokens in memory only (XSS-proof)
 * Refresh tokens are managed via HttpOnly cookies by the backend
 */

const AUTH_API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL || 'https://api.bizoholic.com/auth'

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
  first_name: string
  last_name: string
  tenant_id?: string
}

export interface AuthResponse {
  user: {
    id: string
    email: string
    first_name?: string
    last_name?: string
    role: 'super_admin' | 'tenant_admin' | 'user' | 'readonly' | 'agent'
    tenant_id?: string
    allowed_services?: string[]
    avatar?: string
    created_at?: string
    updated_at?: string
  }
  access_token?: string
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
 * Login user via Auth Service
 * Sets httpOnly cookie automatically via credentials: 'include'
 * Stores access token in memory
 */
export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
  const response = await fetch(`${AUTH_API_URL}/jwt/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    credentials: 'include', // Important: sends and receives cookies
    body: new URLSearchParams({
      username: credentials.email,
      password: credentials.password,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Login failed' }))
    throw new Error(error.detail || error.message || 'Login failed')
  }

  const result: any = await response.json()

  // Extract and store access token
  const token = result.access_token || result.token
  if (token) {
    setAccessToken(token)
  }

  // Get user data
  const userData = await getCurrentUser()

  return {
    user: userData!.user,
    access_token: token,
  }
}

/**
 * Signup new user via Auth Service
 */
export async function signup(data: SignupData): Promise<AuthResponse> {
  const response = await fetch(`${AUTH_API_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      email: data.email,
      password: data.password,
      first_name: data.first_name,
      last_name: data.last_name,
      tenant_id: data.tenant_id || null,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Signup failed' }))
    throw new Error(error.detail || error.message || 'Signup failed')
  }

  const result = await response.json()

  // Auto-login after signup
  return await login({ email: data.email, password: data.password })
}

/**
 * Logout user via Auth Service
 * Clears httpOnly cookie and access token from memory
 */
export async function logout(): Promise<void> {
  try {
    const response = await fetch(`${AUTH_API_URL}/jwt/logout`, {
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

    const response = await fetch(`${AUTH_API_URL}/users/me`, {
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

    const userData = await response.json()

    // Compute full name
    const name = userData.first_name && userData.last_name
      ? `${userData.first_name} ${userData.last_name}`
      : (userData.email ? userData.email.split('@')[0] : 'User')

    return {
      user: {
        ...userData,
        name,
      }
    }
  } catch (error) {
    console.error('Failed to get current user:', error)
    return null
  }
}

/**
 * Request password reset email
 */
export async function requestPasswordReset(data: PasswordResetRequest): Promise<{ message: string }> {
  const response = await fetch(`${AUTH_API_URL}/forgot-password`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(error.detail || error.message || 'Password reset request failed')
  }

  return response.json()
}

/**
 * Confirm password reset with token
 */
export async function confirmPasswordReset(data: PasswordResetConfirm): Promise<{ message: string }> {
  const response = await fetch(`${AUTH_API_URL}/reset-password`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Reset failed' }))
    throw new Error(error.detail || error.message || 'Password reset failed')
  }

  return response.json()
}

/**
 * Verify email with token
 */
export async function verifyEmail(token: string): Promise<{ message: string }> {
  const response = await fetch(`${AUTH_API_URL}/verify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({ token }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Verification failed' }))
    throw new Error(error.detail || error.message || 'Email verification failed')
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
  const headers: HeadersInit = {}
  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`
  }

  const response = await fetch(`${AUTH_API_URL}/tenants`, {
    method: 'GET',
    headers,
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
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  }
  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`
  }

  const response = await fetch(`${AUTH_API_URL}/tenants/switch/${tenantId}`, {
    method: 'POST',
    headers,
    credentials: 'include',
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Switch failed' }))
    throw new Error(error.detail || error.message || 'Failed to switch tenant')
  }

  const result = await response.json()

  // Update access token if provided
  if (result.access_token) {
    setAccessToken(result.access_token)
  }

  return result
}

/**
 * BizOSaaS Auth Client - consolidated API
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
