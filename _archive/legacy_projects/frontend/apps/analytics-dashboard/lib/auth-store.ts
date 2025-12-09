/**
 * Legacy Zustand wrapper for backward compatibility
 * Maps centralized auth to Zustand store pattern
 */

import { create } from 'zustand'
import { type User } from './auth/types'
import { authClient } from './auth/auth-client'

interface AuthStore {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  loading: true,

  login: async (email: string, password: string) => {
    try {
      const response = await authClient.login({ email, password })
      set({ user: response.user, loading: false })
    } catch (error) {
      set({ user: null, loading: false })
      throw error
    }
  },

  logout: async () => {
    try {
      await authClient.logout()
      set({ user: null })
    } catch (error) {
      console.error('Logout failed:', error)
      set({ user: null })
    }
  },

  checkAuth: async () => {
    try {
      const response = await authClient.getCurrentUser()
      set({ user: response?.user || null, loading: false })
    } catch (error) {
      set({ user: null, loading: false })
    }
  },
}))
