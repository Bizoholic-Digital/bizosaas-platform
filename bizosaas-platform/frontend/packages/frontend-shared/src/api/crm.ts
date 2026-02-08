/**
 * CRM API Module
 *
 * Handles all CRM-related API calls to Django CRM via brain-gateway
 */

import { apiClient } from './client'

export const crmApi = {
  // ========== Leads ==========
  getLeads: async () => {
    return apiClient.get('/api/crm/leads')
  },

  createLead: async (data: any) => {
    return apiClient.post('/api/crm/leads', data)
  },

  getLead: async (id: string) => {
    return apiClient.get(`/api/crm/leads/${id}`)
  },

  updateLead: async (id: string, data: any) => {
    return apiClient.put(`/api/crm/leads/${id}`, data)
  },

  // ========== Campaigns ==========
  getCampaigns: async () => {
    return apiClient.get('/api/crm/campaigns')
  },

  getCampaign: async (id: string) => {
    return apiClient.get(`/api/crm/campaigns/${id}`)
  },

  createCampaign: async (data: any) => {
    return apiClient.post('/api/crm/campaigns', data)
  },

  // ========== Clients ==========
  getClient: async (id: string) => {
    return apiClient.get(`/api/crm/clients/${id}`)
  },

  updateClient: async (id: string, data: any) => {
    return apiClient.put(`/api/crm/clients/${id}`, data)
  },

  getClientCampaigns: async (clientId: string) => {
    return apiClient.get(`/api/crm/clients/${clientId}/campaigns`)
  },

  // ========== Analytics ==========
  getAnalytics: async (clientId: string) => {
    return apiClient.get(`/api/crm/clients/${clientId}/analytics`)
  },

  getDashboardStats: async () => {
    return apiClient.get('/api/crm/dashboard/stats')
  }
}
