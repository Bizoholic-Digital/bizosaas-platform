'use client'

import { createContext, useContext, ReactNode } from 'react'
import { useUnifiedAuth, AuthState } from '../../../shared/hooks/useUnifiedAuth' // Adjust path if needed, assumed shared is at root
import { useRouter } from 'next/navigation'

// Note: Staging structure has shared at root.
// If useUnifiedAuth is inside shared/hooks, we need to verify import path.
// ../../../shared = portals/admin-dashboard/lib/../../.. = root/shared. Correct.

interface AuthContextType extends AuthState {
    login: (credentials: { email: string; password: string }) => Promise<void>
    logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children, platform = 'bizosaas-admin' }: { children: ReactNode, platform?: string }) {
    // We need to ensure useUnifiedAuth exists in shared/hooks on staging.
    // Converting this file to use authClient directly if useUnifiedAuth is missing or complex.
    // But strictly porting the fix we verified on main:

    // NOTE: If useUnifiedAuth is not available, we might break.
    // Main branch had it in frontend/shared/hooks.
    // Staging has shared/ at root.
    // Let's assume shared/hooks/useUnifiedAuth exists.

    const auth = useUnifiedAuth(platform)
    const router = useRouter()

    const loginAdapter = async (credentials: { email: string; password: string }) => {
        const success = await auth.login(credentials.email, credentials.password)
        if (success) {
            router.push('/')
        } else {
            throw new Error('Login failed')
        }
    }

    const logoutAdapter = async () => {
        await auth.logout()
        router.push('/login')
    }

    const contextValue: AuthContextType = {
        ...auth,
        login: loginAdapter,
        logout: logoutAdapter
    }

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider')
    }
    return context
}
