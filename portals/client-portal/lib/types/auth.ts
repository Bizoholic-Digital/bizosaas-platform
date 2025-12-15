export interface User {
    id: string
    email: string
    name: string
    role: string
    tenant_id?: string
    permissions?: string[]
}

export interface LoginCredentials {
    email: string
    password: string
}

export interface SignupData {
    email: string
    password: string
    name: string
    company_name: string
}

export interface Tenant {
    id: string
    name: string
    subdomain: string
}
