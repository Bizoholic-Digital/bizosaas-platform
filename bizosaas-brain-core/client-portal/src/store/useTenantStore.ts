import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import type { Tenant, TenantUser } from '@/types/tenant'

interface TenantState {
  // Current state
  currentTenant: Tenant | null
  availableTenants: Tenant[]
  user: TenantUser | null
  isLoading: boolean
  error: string | null

  // Actions
  setCurrentTenant: (tenant: Tenant) => void
  setAvailableTenants: (tenants: Tenant[]) => void
  setUser: (user: TenantUser) => void
  switchTenant: (tenantId: string) => Promise<void>
  loadTenants: () => Promise<void>
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  clearError: () => void
  reset: () => void
}

const initialState = {
  currentTenant: null,
  availableTenants: [],
  user: null,
  isLoading: false,
  error: null,
}

export const useTenantStore = create<TenantState>()(
  persist(
    (set, get) => ({
      ...initialState,

      setCurrentTenant: (tenant) => {
        set({ currentTenant: tenant, error: null })
      },

      setAvailableTenants: (tenants) => {
        set({ availableTenants: tenants })
      },

      setUser: (user) => {
        set({ user })
      },

      switchTenant: async (tenantId: string) => {
        const { availableTenants } = get()
        const tenant = availableTenants.find((t) => t.id === tenantId)

        if (!tenant) {
          set({ error: 'Tenant not found' })
          return
        }

        try {
          set({ isLoading: true, error: null })

          // Call Brain Gateway to switch tenant context
          const response = await fetch(
            `${process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL}/tenants/switch`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ tenantId }),
              credentials: 'include',
            }
          )

          if (!response.ok) {
            throw new Error('Failed to switch tenant')
          }

          set({ currentTenant: tenant, isLoading: false })

          // Reload the page to refresh all data with new tenant context
          window.location.reload()
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to switch tenant',
            isLoading: false,
          })
        }
      },

      loadTenants: async () => {
        try {
          set({ isLoading: true, error: null })

          // Fetch user's available tenants from Brain Gateway
          const response = await fetch(
            `${process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL}/tenants/available`,
            {
              credentials: 'include',
            }
          )

          if (!response.ok) {
            throw new Error('Failed to load tenants')
          }

          const data = await response.json()
          const tenants = data.tenants || []
          const currentTenant = data.currentTenant || (tenants.length > 0 ? tenants[0] : null)

          set({
            availableTenants: tenants,
            currentTenant,
            isLoading: false,
          })
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to load tenants',
            isLoading: false,
          })
        }
      },

      setLoading: (loading) => {
        set({ isLoading: loading })
      },

      setError: (error) => {
        set({ error })
      },

      clearError: () => {
        set({ error: null })
      },

      reset: () => {
        set(initialState)
      },
    }),
    {
      name: 'tenant-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        currentTenant: state.currentTenant,
        availableTenants: state.availableTenants,
      }),
    }
  )
)

// Selectors for optimized re-renders
export const selectCurrentTenant = (state: TenantState) => state.currentTenant
export const selectAvailableTenants = (state: TenantState) => state.availableTenants
export const selectIsLoading = (state: TenantState) => state.isLoading
export const selectError = (state: TenantState) => state.error
export const selectCurrentTenantId = (state: TenantState) => state.currentTenant?.id
export const selectCurrentTenantPlan = (state: TenantState) => state.currentTenant?.plan
export const selectHasFeature = (feature: keyof TenantState['currentTenant']['settings']['features']) =>
  (state: TenantState) => state.currentTenant?.settings.features[feature] ?? false
