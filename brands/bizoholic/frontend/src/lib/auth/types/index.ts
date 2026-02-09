export interface User {
  id: string
  email: string
  first_name?: string
  last_name?: string
  name?: string // Computed from first_name + last_name
  role: 'super_admin' | 'tenant_admin' | 'user' | 'readonly' | 'agent'
  tenant_id?: string
  tenant_name?: string
  avatar?: string
  allowed_services?: string[]
  created_at?: string
  updated_at?: string
}

export interface AuthState {
  user: User | null
  loading: boolean
  error: string | null
}

export interface AuthContextType extends AuthState {
  login: (credentials: { email: string; password: string }) => Promise<void>
  signup: (data: { email: string; password: string; first_name: string; last_name: string }) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}
