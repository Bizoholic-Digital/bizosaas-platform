/**
 * Auth Store using Zustand
 * Legacy compatibility layer for existing components
 * Wraps the new centralized auth system
 */

import { create } from 'zustand'

interface User {
  id: string
  email: string
  name: string
  role: string
  tenant_id?: string
  tenant_name?: string
  avatar?: string
}

interface AuthStore {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean

  setUser: (user: User | null) => void
  login: (email: string, password: string) => Promise<boolean>
  logout: () => Promise<void>
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,

  setUser: (user) => set({ user, isAuthenticated: !!user }),

  login: async (email, password) => {
    try {
      set({ isLoading: true })

      // Import auth client dynamically to avoid circular dependencies
      const { authClient } = await import('./auth/auth-client')

      const response = await authClient.login({ email, password })

      if (response.user) {
        set({
          user: {
            ...response.user,
            name: response.user.first_name && response.user.last_name
              ? `${response.user.first_name} ${response.user.last_name}`
              : response.user.email.split('@')[0]
          },
          isAuthenticated: true,
          isLoading: false,
        })
        return true
      }

      set({ isLoading: false })
      return false
    } catch (error) {
      console.error('Login failed:', error)
      set({ user: null, isAuthenticated: false, isLoading: false })
      return false
    }
  },

  logout: async () => {
    try {
      // Import auth client dynamically
      const { authClient } = await import('./auth/auth-client')

      await authClient.logout()
      set({ user: null, isAuthenticated: false })
    } catch (error) {
      console.error('Logout failed:', error)
      // Clear state anyway
      set({ user: null, isAuthenticated: false })
    }
  },
}))
