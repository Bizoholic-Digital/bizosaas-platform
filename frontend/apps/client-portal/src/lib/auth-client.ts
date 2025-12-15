import { LoginCredentials, SignupData, User, Tenant } from './types/auth'

const AUTH_API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8007'

export const authClient = {
    async login(credentials: LoginCredentials): Promise<User> {
        const response = await fetch(`${AUTH_API_URL}/api/v1/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ...credentials,
                grant_type: 'password'
            }),
        })

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Login failed' }))
            throw new Error(error.detail || 'Login failed')
        }

        const data = await response.json()

        // Store token in localStorage for client-side usage
        localStorage.setItem('access_token', data.access_token)
        if (data.refresh_token) {
            localStorage.setItem('refresh_token', data.refresh_token)
            // Set refresh_token cookie for Middleware protection
            document.cookie = `refresh_token=${data.refresh_token}; path=/; max-age=2592000; SameSite=Lax`
        }

        return this.getCurrentUser()
    },

    async signup(data: SignupData): Promise<User> {
        const response = await fetch(`${AUTH_API_URL}/api/v1/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })

        if (!response.ok) {
            throw new Error('Signup failed')
        }

        // Auto login after signup
        return this.login({ email: data.email, password: data.password })
    },

    async logout(): Promise<void> {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        document.cookie = 'refresh_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'
    },

    async getCurrentUser(): Promise<User> {
        const token = localStorage.getItem('access_token')
        if (!token) throw new Error('No access token')

        const response = await fetch(`${AUTH_API_URL}/api/v1/users/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })

        if (!response.ok) {
            throw new Error('Failed to fetch user')
        }

        return response.json()
    },

    async getTenants(): Promise<Tenant[]> {
        const token = localStorage.getItem('access_token')
        if (!token) return []

        const response = await fetch(`${AUTH_API_URL}/api/v1/tenants`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })

        if (response.ok) {
            return response.json()
        }
        return []
    },

    async switchTenant(tenantId: string): Promise<User> {
        // Implement based on backend capability, typically getting a new token
        return this.getCurrentUser()
    }
}
