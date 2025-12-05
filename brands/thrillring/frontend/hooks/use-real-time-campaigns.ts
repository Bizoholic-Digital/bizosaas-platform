import { useState, useEffect } from 'react'
import { useCampaignUpdates } from '@/lib/websocket'

interface Campaign {
  id: string
  name: string
  status: 'active' | 'paused' | 'completed' | 'draft'
  type: 'awareness' | 'conversion' | 'retention' | 'lead_gen'
  budget: number
  spent: number
  impressions: number
  clicks: number
  conversions: number
  ctr: number
  cpc: number
  conversion_rate: number
  created_at: string
  updated_at: string
}

export function useRealTimeCampaigns(initialCampaigns: Campaign[] = []) {
  const [campaigns, setCampaigns] = useState<Campaign[]>(initialCampaigns)
  const [recentUpdates, setRecentUpdates] = useState<Array<{
    campaignId: string
    action: string
    timestamp: string
  }>>([])

  // Subscribe to campaign updates
  useEffect(() => {
    const unsubscribe = useCampaignUpdates((data) => {
      const { campaign_id, action, campaign_data } = data
      
      // Add to recent updates
      setRecentUpdates(prev => [
        {
          campaignId: campaign_id,
          action,
          timestamp: new Date().toISOString()
        },
        ...prev.slice(0, 9) // Keep only 10 recent updates
      ])

      // Update campaigns list
      switch (action) {
        case 'created':
          setCampaigns(prev => [campaign_data, ...prev])
          break
          
        case 'updated':
          setCampaigns(prev => prev.map(campaign => 
            campaign.id === campaign_id 
              ? { ...campaign, ...campaign_data, updated_at: new Date().toISOString() }
              : campaign
          ))
          break
          
        case 'deleted':
          setCampaigns(prev => prev.filter(campaign => campaign.id !== campaign_id))
          break
          
        case 'status_changed':
          setCampaigns(prev => prev.map(campaign => 
            campaign.id === campaign_id 
              ? { ...campaign, status: campaign_data.status, updated_at: new Date().toISOString() }
              : campaign
          ))
          break
          
        case 'metrics_updated':
          setCampaigns(prev => prev.map(campaign => 
            campaign.id === campaign_id 
              ? { 
                  ...campaign, 
                  ...campaign_data.metrics,
                  updated_at: new Date().toISOString() 
                }
              : campaign
          ))
          break
      }
    })

    return unsubscribe
  }, [])

  // Utility functions
  const getCampaignById = (id: string) => campaigns.find(campaign => campaign.id === id)
  
  const getCampaignsByStatus = (status: Campaign['status']) => 
    campaigns.filter(campaign => campaign.status === status)
  
  const getActiveCampaigns = () => getCampaignsByStatus('active')
  
  const getTotalBudget = () => campaigns.reduce((sum, campaign) => sum + campaign.budget, 0)
  
  const getTotalSpent = () => campaigns.reduce((sum, campaign) => sum + campaign.spent, 0)
  
  const getTotalImpressions = () => campaigns.reduce((sum, campaign) => sum + campaign.impressions, 0)
  
  const getTotalClicks = () => campaigns.reduce((sum, campaign) => sum + campaign.clicks, 0)
  
  const getTotalConversions = () => campaigns.reduce((sum, campaign) => sum + campaign.conversions, 0)
  
  const getOverallCTR = () => {
    const totalImpressions = getTotalImpressions()
    const totalClicks = getTotalClicks()
    return totalImpressions > 0 ? (totalClicks / totalImpressions) * 100 : 0
  }
  
  const getOverallConversionRate = () => {
    const totalClicks = getTotalClicks()
    const totalConversions = getTotalConversions()
    return totalClicks > 0 ? (totalConversions / totalClicks) * 100 : 0
  }

  const getRecentlyUpdated = (minutes: number = 30) => {
    const cutoff = new Date(Date.now() - minutes * 60 * 1000)
    return campaigns.filter(campaign => new Date(campaign.updated_at) > cutoff)
  }

  return {
    campaigns,
    recentUpdates,
    setCampaigns,
    
    // Utility functions
    getCampaignById,
    getCampaignsByStatus,
    getActiveCampaigns,
    
    // Metrics
    getTotalBudget,
    getTotalSpent,
    getTotalImpressions,
    getTotalClicks,
    getTotalConversions,
    getOverallCTR,
    getOverallConversionRate,
    getRecentlyUpdated,
    
    // Counts
    totalCampaigns: campaigns.length,
    activeCampaigns: getActiveCampaigns().length,
    recentlyUpdatedCount: getRecentlyUpdated().length
  }
}