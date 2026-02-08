'use client'

import { useState, useEffect, useCallback } from 'react'
import { crmApi, Lead, CRMStats, LeadActivity } from '@/lib/api/crm-api'
import { getMockDates } from '@/lib/date-utils'

interface UseLeadsOptions {
  page?: number
  limit?: number
  status?: string
  source?: string
  assignedTo?: string
  search?: string
  autoRefresh?: boolean
  refreshInterval?: number
}

export function useLeads(options: UseLeadsOptions = {}) {
  const [leads, setLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(0)
  const [currentPage, setCurrentPage] = useState(options.page || 1)

  const fetchLeads = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      
      const result = await crmApi.getLeads({
        page: currentPage,
        ...options,
      })
      
      setLeads(result.leads)
      setTotal(result.total)
      setTotalPages(result.totalPages)
    } catch (err) {
      console.error('Failed to fetch leads:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch leads')
      
      // Fallback to mock data on API failure - using consistent dates to prevent hydration issues
      const mockDates = getMockDates()
      const mockLeads: Lead[] = [
        {
          id: '1',
          name: 'John Smith',
          email: 'john@example.com',
          phone: '+1-555-0123',
          company: 'Tech Corp',
          status: 'new',
          score: 85,
          source: 'Website Form',
          assignedTo: 'Sarah Wilson',
          createdAt: mockDates.now,
          value: 15000,
          notes: 'Interested in enterprise solution'
        },
        {
          id: '2',
          name: 'Emily Johnson',
          email: 'emily@startup.com',
          phone: '+1-555-0124',
          company: 'Startup Inc',
          status: 'qualified',
          score: 92,
          source: 'LinkedIn',
          assignedTo: 'Mike Chen',
          createdAt: mockDates.yesterday,
          value: 8500,
          notes: 'Quick decision maker, hot lead'
        }
      ]
      
      setLeads(mockLeads)
      setTotal(mockLeads.length)
      setTotalPages(1)
    } finally {
      setLoading(false)
    }
  }, [currentPage, options])

  const refreshLeads = useCallback(() => {
    fetchLeads()
  }, [fetchLeads])

  const updateLead = useCallback(async (id: string, updates: Partial<Lead>) => {
    try {
      const updatedLead = await crmApi.updateLead(id, updates)
      setLeads(prevLeads => 
        prevLeads.map(lead => lead.id === id ? updatedLead : lead)
      )
      return updatedLead
    } catch (err) {
      console.error('Failed to update lead:', err)
      throw err
    }
  }, [])

  const deleteLead = useCallback(async (id: string) => {
    try {
      await crmApi.deleteLead(id)
      setLeads(prevLeads => prevLeads.filter(lead => lead.id !== id))
      setTotal(prev => prev - 1)
    } catch (err) {
      console.error('Failed to delete lead:', err)
      throw err
    }
  }, [])

  const createLead = useCallback(async (leadData: Partial<Lead>) => {
    try {
      const newLead = await crmApi.createLead(leadData)
      setLeads(prevLeads => [newLead, ...prevLeads])
      setTotal(prev => prev + 1)
      return newLead
    } catch (err) {
      console.error('Failed to create lead:', err)
      throw err
    }
  }, [])

  useEffect(() => {
    fetchLeads()
  }, [fetchLeads])

  // Auto-refresh functionality
  useEffect(() => {
    if (options.autoRefresh && options.refreshInterval) {
      const interval = setInterval(fetchLeads, options.refreshInterval)
      return () => clearInterval(interval)
    }
  }, [options.autoRefresh, options.refreshInterval, fetchLeads])

  return {
    leads,
    loading,
    error,
    total,
    totalPages,
    currentPage,
    setCurrentPage,
    refreshLeads,
    updateLead,
    deleteLead,
    createLead,
  }
}

export function useCRMStats() {
  const [stats, setStats] = useState<CRMStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchStats = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const crmStats = await crmApi.getCRMStats()
      setStats(crmStats)
    } catch (err) {
      console.error('Failed to fetch CRM stats:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch CRM stats')
      
      // Fallback to mock stats
      const mockStats: CRMStats = {
        totalLeads: 156,
        newLeads: 23,
        qualifiedLeads: 45,
        convertedLeads: 12,
        conversionRate: 7.7,
        avgLeadScore: 72,
        totalValue: 145600,
        monthlyGrowth: 12.5,
      }
      setStats(mockStats)
    } finally {
      setLoading(false)
    }
  }, [])

  const refreshStats = useCallback(() => {
    fetchStats()
  }, [fetchStats])

  useEffect(() => {
    fetchStats()
  }, [fetchStats])

  return {
    stats,
    loading,
    error,
    refreshStats,
  }
}

export function useLeadActivities(leadId: string) {
  const [activities, setActivities] = useState<LeadActivity[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchActivities = useCallback(async () => {
    if (!leadId) return
    
    try {
      setLoading(true)
      setError(null)
      const leadActivities = await crmApi.getLeadActivities(leadId)
      setActivities(leadActivities)
    } catch (err) {
      console.error('Failed to fetch lead activities:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch activities')
      
      // Mock activities - using consistent dates
      const mockDates = getMockDates()
      const mockActivities: LeadActivity[] = [
        {
          id: '1',
          leadId,
          type: 'email',
          description: 'Sent welcome email',
          createdAt: mockDates.now,
          createdBy: 'System'
        }
      ]
      setActivities(mockActivities)
    } finally {
      setLoading(false)
    }
  }, [leadId])

  const addActivity = useCallback(async (activity: Omit<LeadActivity, 'id' | 'leadId' | 'createdAt' | 'createdBy'>) => {
    try {
      const newActivity = await crmApi.addLeadActivity(leadId, activity)
      setActivities(prev => [newActivity, ...prev])
      return newActivity
    } catch (err) {
      console.error('Failed to add activity:', err)
      throw err
    }
  }, [leadId])

  useEffect(() => {
    fetchActivities()
  }, [fetchActivities])

  return {
    activities,
    loading,
    error,
    addActivity,
    refreshActivities: fetchActivities,
  }
}

// Utility hooks
export function useLeadSources() {
  const [sources, setSources] = useState<string[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSources = async () => {
      try {
        const leadSources = await crmApi.getLeadSources()
        setSources(leadSources)
      } catch (err) {
        console.error('Failed to fetch lead sources:', err)
        // Fallback sources
        setSources(['Website Form', 'LinkedIn', 'Cold Email', 'Referral', 'Social Media', 'Advertisement'])
      } finally {
        setLoading(false)
      }
    }

    fetchSources()
  }, [])

  return { sources, loading }
}

export function useTeamMembers() {
  const [teamMembers, setTeamMembers] = useState<Array<{ id: string, name: string, email: string }>>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTeamMembers = async () => {
      try {
        const members = await crmApi.getTeamMembers()
        setTeamMembers(members)
      } catch (err) {
        console.error('Failed to fetch team members:', err)
        // Fallback team members
        setTeamMembers([
          { id: '1', name: 'Sarah Wilson', email: 'sarah@bizoholic.com' },
          { id: '2', name: 'Mike Chen', email: 'mike@bizoholic.com' },
          { id: '3', name: 'Lisa Rodriguez', email: 'lisa@bizoholic.com' },
        ])
      } finally {
        setLoading(false)
      }
    }

    fetchTeamMembers()
  }, [])

  return { teamMembers, loading }
}