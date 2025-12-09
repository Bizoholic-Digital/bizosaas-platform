// Authentication Types for FastAPI Brain Gateway

export interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'manager' | 'client' | 'guest'
  tenant_id: string
  tenant_name: string
  avatar?: string
  created_at: string
  updated_at: string
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
  user: User
  message?: string
}

export interface AuthError {
  error: string
  message: string
  details?: Record<string, string[]>
}

export interface Tenant {
  id: string
  name: string
  slug: string
  plan: 'free' | 'starter' | 'professional' | 'enterprise'
  is_active: boolean
}
