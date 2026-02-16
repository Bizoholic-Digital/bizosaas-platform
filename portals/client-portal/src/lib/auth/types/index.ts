export interface User {
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

export interface AuthState {
  user: User | null
  loading: boolean
  error: string | null
}

export interface AuthContextType extends AuthState {
  login: (credentials: { email: string; password: string }) => Promise<void>
  signup: (data: { email: string; password: string; name: string; company?: string }) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}
