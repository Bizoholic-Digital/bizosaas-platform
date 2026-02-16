// Tenant types for multi-tenant client portal

export type UserRole = 'client' | 'partner' | 'moderator' | 'admin'

export interface Tenant {
  id: string
  name: string
  slug: string
  logo?: string
  plan: 'free' | 'starter' | 'professional' | 'enterprise'
  status: 'active' | 'suspended' | 'trial'
  createdAt: string
  expiresAt?: string
  settings: TenantSettings
}

export interface TenantSettings {
  timezone: string
  currency: string
  language: string
  dateFormat: string
  features: {
    aiAgents: boolean
    analytics: boolean
    billing: boolean
    crm: boolean
    ecommerce: boolean
    gamification: boolean
    marketing: boolean
    reviews: boolean
  }
}

export interface UserTenantRole {
  tenantId: string
  role: UserRole
  permissions: string[]
}

export interface TenantUser {
  id: string
  email: string
  name: string
  avatar?: string
  roles: UserTenantRole[]
  currentTenant?: string
}

export interface TenantSwitchRequest {
  tenantId: string
}

export interface TenantStats {
  totalUsers: number
  activeUsers: number
  revenue: number
  campaigns: number
  leads: number
  orders: number
}
