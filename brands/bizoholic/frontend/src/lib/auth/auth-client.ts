/**
 * BizOSaaS Authentication Client for Bizoholic
 * Handles all authentication operations via Next.js API routes (Proxy)
 *
 * SECURITY: Access tokens are managed via HttpOnly cookies by the Next.js server
 */

const AUTH_API_URL = '' // Use relative paths to hit Next.js API routes

// In-memory token storage (optional, mostly for client-side access if needed)
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
  platform?: string
  remember_me?: boolean
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
 * Login user via Next.js API Route
 * This sets the httpOnly cookie on the Next.js domain
 */
export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
  const response = await fetch(`${AUTH_API_URL}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Login failed' }))
    throw new Error(error.error || error.detail || 'Login failed')
  }

  const result: any = await response.json()

  // Extract and store access token (optional for client-side)
  const token = result.access_token
  if (token) {
    setAccessToken(token)
  }

  // The login endpoint returns user data directly
  return {
    user: {
      id: result.user_id || result.id,
      email: result.email,
      first_name: result.full_name?.split(' ')[0] || result.first_name,
      last_name: result.full_name?.split(' ')[1] || result.last_name,
      role: result.role || 'user',
      tenant_id: result.tenant_id
    },
    access_token: token,
  }
}

/**
 * Signup new user via Auth Service
 */
export async function signup(data: SignupData): Promise<AuthResponse> {
  // TODO: Implement /api/auth/register route
  throw new Error('Signup not implemented yet')
}

/**
 * Logout user via Next.js API Route
 * Clears httpOnly cookie
 */
export async function logout(): Promise<void> {
  try {
    await fetch(`${AUTH_API_URL}/api/auth/logout`, {
      method: 'POST',
    })
  } catch (error) {
    console.error('Logout request failed:', error)
  } finally {
    clearAccessToken()
  }
}

/**
 * Get current authenticated user via Next.js API Route
 * This uses the httpOnly cookie to authenticate with the backend
 */
export async function getCurrentUser(): Promise<AuthResponse | null> {
  try {
    console.log('[Auth Client] Calling getCurrentUser...')
    const response = await fetch(`${AUTH_API_URL}/api/auth/me`, {
      method: 'GET',
      cache: 'no-store',
    })

    console.log('[Auth Client] getCurrentUser response status:', response.status)

    if (!response.ok) {
      if (response.status === 401) {
        console.log('[Auth Client] 401 Unauthorized - clearing token')
        clearAccessToken()
      }
      console.log('[Auth Client] getCurrentUser failed, returning null')
      return null
    }

    const userData = await response.json()
    console.log('[Auth Client] getCurrentUser success, user:', userData.email)

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
    console.error('[Auth Client] Failed to get current user:', error)
    return null
  }
}

/**
 * Request password reset email
 */
export async function requestPasswordReset(data: PasswordResetRequest): Promise<{ message: string }> {
  // TODO: Implement proxy route
  throw new Error('Not implemented')
}

/**
 * Confirm password reset with token
 */
export async function confirmPasswordReset(data: PasswordResetConfirm): Promise<{ message: string }> {
  // TODO: Implement proxy route
  throw new Error('Not implemented')
}

/**
 * Verify email with token
 */
export async function verifyEmail(token: string): Promise<{ message: string }> {
  // TODO: Implement proxy route
  throw new Error('Not implemented')
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
  // TODO: Implement proxy route
  return []
}

/**
 * Switch to a different tenant
 */
export async function switchTenant(tenantId: string): Promise<AuthResponse> {
  // TODO: Implement proxy route
  throw new Error('Not implemented')
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
