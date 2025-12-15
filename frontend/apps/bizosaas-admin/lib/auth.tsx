'use client'

import { createContext, useContext, ReactNode } from 'react'
import { useUnifiedAuth, AuthState } from '../../../../shared/hooks/useUnifiedAuth'
import { useRouter } from 'next/navigation'

// Extended AuthContext type to match the usage in LoginPage (login taking an object)
interface AuthContextType extends AuthState {
    login: (credentials: { email: string; password: string }) => Promise<void>
    logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children, platform = 'bizosaas-admin' }: { children: ReactNode, platform?: string }) {
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
