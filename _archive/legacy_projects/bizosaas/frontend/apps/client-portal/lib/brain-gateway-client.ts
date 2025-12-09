import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios'
import { useTenantStore } from '@/store/useTenantStore'
import { authClient } from './auth-client'

// Response types
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  results: T[]
  count: number
  next: string | null
  previous: string | null
}

// Brain Gateway Client with automatic token refresh
class BrainGatewayClient {
  private client: AxiosInstance
  private isRefreshing = false
  private failedQueue: Array<{
    resolve: (value: any) => void
    reject: (reason: any) => void
  }> = []

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8001/api',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, // Required for HttpOnly cookies
    })

    // Request interceptor - Add auth token and tenant context
    this.client.interceptors.request.use(
      (config) => {
        // Get auth token from memory (via authClient)
        const token = authClient.getAccessToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }

        // Add current tenant ID to headers
        const currentTenant = useTenantStore.getState().currentTenant
        if (currentTenant) {
          config.headers['X-Tenant-ID'] = currentTenant.id
        }

        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor - Handle errors with automatic token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest: any = error.config

        if (error.response) {
          const { status } = error.response

          // Handle 401 Unauthorized - try to refresh token
          if (status === 401 && !originalRequest._retry) {
            if (this.isRefreshing) {
              // Queue the request while token is being refreshed
              return new Promise((resolve, reject) => {
                this.failedQueue.push({ resolve, reject })
              })
                .then((token) => {
                  originalRequest.headers['Authorization'] = `Bearer ${token}`
                  return this.client(originalRequest)
                })
                .catch((err) => Promise.reject(err))
            }

            originalRequest._retry = true
            this.isRefreshing = true

            try {
              // Attempt to refresh the access token
              const newAccessToken = await authClient.refreshAccessToken()

              if (newAccessToken) {
                // Process queued requests with new token
                this.processQueue(null, newAccessToken)

                // Retry original request with new token
                originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`
                return this.client(originalRequest)
              } else {
                // Refresh failed - redirect to login
                this.processQueue(new Error('Token refresh failed'), null)
                if (typeof window !== 'undefined') {
                  window.location.href = '/login?expired=true'
                }
                return Promise.reject(error)
              }
            } catch (refreshError) {
              this.processQueue(refreshError, null)
              if (typeof window !== 'undefined') {
                window.location.href = '/login?expired=true'
              }
              return Promise.reject(refreshError)
            } finally {
              this.isRefreshing = false
            }
          }

          // Handle 403 Forbidden - show permission error
          if (status === 403) {
            console.error('Permission denied:', error.response.data)
          }

          // Handle 429 Too Many Requests - rate limiting
          if (status === 429) {
            console.warn('Rate limit exceeded. Please try again later.')
          }
        }

        return Promise.reject(error)
      }
    )
  }

  // Process queued requests after token refresh
  private processQueue(error: any, token: string | null = null): void {
    this.failedQueue.forEach((prom) => {
      if (error) {
        prom.reject(error)
      } else {
        prom.resolve(token)
      }
    })

    this.failedQueue = []
  }

  // Generic HTTP methods
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config)
    return response.data
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config)
    return response.data
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config)
    return response.data
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config)
    return response.data
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config)
    return response.data
  }

  // === DASHBOARD API ===
  async getDashboardStats() {
    return this.get('/dashboard/stats')
  }

  async getDashboardActivity(limit: number = 10) {
    return this.get(`/dashboard/activity?limit=${limit}`)
  }

  // === TENANT API ===
  async getAvailableTenants() {
    return this.get('/tenants/available')
  }

  async switchTenant(tenantId: string) {
    return this.post('/tenants/switch', { tenantId })
  }

  async getTenantSettings() {
    return this.get('/tenants/settings')
  }

  async updateTenantSettings(settings: any) {
    return this.put('/tenants/settings', settings)
  }

  // === CRM API ===
  async getContacts(params?: { page?: number; search?: string; status?: string }) {
    return this.get('/crm/contacts', { params })
  }

  async getContact(id: string) {
    return this.get(`/crm/contacts/${id}`)
  }

  async createContact(data: any) {
    return this.post('/crm/contacts', data)
  }

  async updateContact(id: string, data: any) {
    return this.put(`/crm/contacts/${id}`, data)
  }

  async deleteContact(id: string) {
    return this.delete(`/crm/contacts/${id}`)
  }

  async getLeads(params?: { page?: number; status?: string }) {
    return this.get('/crm/leads', { params })
  }

  // === CONTENT API (Wagtail) ===
  async getPages(params?: { type?: string; search?: string }) {
    return this.get('/content/pages', { params })
  }

  async getPage(id: string) {
    return this.get(`/content/pages/${id}`)
  }

  async createPage(data: any) {
    return this.post('/content/pages', data)
  }

  async updatePage(id: string, data: any) {
    return this.put(`/content/pages/${id}`, data)
  }

  async publishPage(id: string) {
    return this.post(`/content/pages/${id}/publish`)
  }

  // === E-COMMERCE API (Saleor) ===
  async getProducts(params?: { page?: number; search?: string; category?: string }) {
    return this.get('/ecommerce/products', { params })
  }

  async getProduct(id: string) {
    return this.get(`/ecommerce/products/${id}`)
  }

  async getOrders(params?: { page?: number; status?: string }) {
    return this.get('/ecommerce/orders', { params })
  }

  async getOrder(id: string) {
    return this.get(`/ecommerce/orders/${id}`)
  }

  // === BILLING API ===
  async getSubscription() {
    return this.get('/billing/subscription/current')
  }

  async getInvoices() {
    return this.get('/billing/invoices')
  }

  async createSubscription(data: { planId: string; gateway: string }) {
    return this.post(`/billing/${data.gateway}/create-subscription`, data)
  }

  async cancelSubscription() {
    return this.delete('/billing/subscription/cancel')
  }

  async updatePaymentMethod(gateway: string, data: any) {
    return this.put(`/billing/${gateway}/payment-method`, data)
  }

  // === DIRECTORY API ===
  async getListings(params?: { page?: number; category?: string }) {
    return this.get('/directory/listings', { params })
  }

  async getListing(id: string) {
    return this.get(`/directory/listings/${id}`)
  }

  async createListing(data: any) {
    return this.post('/directory/listings', data)
  }

  // === CAMPAIGNS API ===
  async getCampaigns(params?: { page?: number; status?: string }) {
    return this.get('/campaigns', { params })
  }

  async getCampaign(id: string) {
    return this.get(`/campaigns/${id}`)
  }

  async createCampaign(data: any) {
    return this.post('/campaigns', data)
  }

  async updateCampaign(id: string, data: any) {
    return this.put(`/campaigns/${id}`, data)
  }

  async launchCampaign(id: string) {
    return this.post(`/campaigns/${id}/launch`)
  }

  async pauseCampaign(id: string) {
    return this.post(`/campaigns/${id}/pause`)
  }

  // === AI AGENTS API ===
  async getAgents() {
    return this.get('/ai-agents')
  }

  async getAgent(id: string) {
    return this.get(`/ai-agents/${id}`)
  }

  async executeAgent(id: string, data: any) {
    return this.post(`/ai-agents/${id}/execute`, data)
  }

  // === ANALYTICS API ===
  async getAnalytics(params: { metric: string; period: string }) {
    return this.get('/analytics', { params })
  }

  async getReports(params?: { type?: string; startDate?: string; endDate?: string }) {
    return this.get('/analytics/reports', { params })
  }

  // === REVIEWS API ===
  async getReviews(params?: { page?: number; rating?: number }) {
    return this.get('/reviews', { params })
  }

  async respondToReview(id: string, response: string) {
    return this.post(`/reviews/${id}/respond`, { response })
  }

  // === GAMIFICATION API ===
  async getLeaderboard(period: string = 'month') {
    return this.get(`/gamification/leaderboard?period=${period}`)
  }

  async getAchievements() {
    return this.get('/gamification/achievements')
  }

  async getUserPoints() {
    return this.get('/gamification/points')
  }

  // === APPROVALS API (HITL) ===
  async getPendingApprovals() {
    return this.get('/approvals/pending')
  }

  async approveItem(id: string, data?: any) {
    return this.post(`/approvals/${id}/approve`, data)
  }

  async rejectItem(id: string, reason: string) {
    return this.post(`/approvals/${id}/reject`, { reason })
  }

  // === TEAM API ===
  async getTeamMembers() {
    return this.get('/team/members')
  }

  async inviteTeamMember(data: { email: string; role: string }) {
    return this.post('/team/invite', data)
  }

  async updateTeamMember(id: string, data: any) {
    return this.put(`/team/members/${id}`, data)
  }

  async removeTeamMember(id: string) {
    return this.delete(`/team/members/${id}`)
  }

  // === SUPPORT API ===
  async getTickets(params?: { page?: number; status?: string }) {
    return this.get('/support/tickets', { params })
  }

  async createTicket(data: any) {
    return this.post('/support/tickets', data)
  }

  async getTicket(id: string) {
    return this.get(`/support/tickets/${id}`)
  }

  async updateTicket(id: string, data: any) {
    return this.put(`/support/tickets/${id}`, data)
  }

  // === INTEGRATIONS API ===
  async getIntegrations() {
    return this.get('/integrations')
  }

  async connectIntegration(provider: string, data: any) {
    return this.post(`/integrations/${provider}/connect`, data)
  }

  async disconnectIntegration(provider: string) {
    return this.delete(`/integrations/${provider}/disconnect`)
  }
}

// Export singleton instance
export const brainGateway = new BrainGatewayClient()
export default brainGateway
