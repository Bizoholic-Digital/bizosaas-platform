import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';

// Types for business operations
export interface PaymentMetrics {
  totalRevenue: number;
  monthlyRevenue: number;
  transactionCount: number;
  successRate: number;
  avgTransactionValue: number;
  gatewayStats: Record<string, {
    count: number;
    revenue: number;
    successRate: number;
  }>;
}

export interface CommunicationMetrics {
  totalCampaigns: number;
  activeCampaigns: number;
  totalSent: number;
  deliveryRate: number;
  openRate: number;
  clickRate: number;
  conversionRate: number;
  channelStats: Record<string, {
    sent: number;
    delivered: number;
    engagement: number;
  }>;
}

export interface SEOMetrics {
  totalKeywords: number;
  avgRanking: number;
  organicTraffic: number;
  indexedPages: number;
  domainAuthority: number;
  backlinks: number;
  searchEngineStats: Record<string, {
    keywords: number;
    avgRank: number;
    traffic: number;
  }>;
}

export interface AnalyticsMetrics {
  totalVisitors: number;
  uniqueVisitors: number;
  pageViews: number;
  bounceRate: number;
  avgSessionDuration: string;
  conversionRate: number;
  revenue: number;
  goalCompletions: number;
}

// Payment Operations Hooks
export function usePaymentMetrics(timeRange: string = '30d') {
  return useQuery({
    queryKey: ['payment-metrics', timeRange],
    queryFn: async () => {
      const response = await fetch(`/api/brain/business-operations/payments/metrics?timeRange=${timeRange}`);
      if (!response.ok) {
        throw new Error('Failed to fetch payment metrics');
      }
      return response.json() as Promise<PaymentMetrics>;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function usePaymentTransactions(filters?: {
  status?: string;
  gateway?: string;
  limit?: number;
}) {
  return useQuery({
    queryKey: ['payment-transactions', filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters?.status) params.append('status', filters.status);
      if (filters?.gateway) params.append('gateway', filters.gateway);
      if (filters?.limit) params.append('limit', filters.limit.toString());
      
      const response = await fetch(`/api/brain/business-operations/payments/transactions?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch payment transactions');
      }
      return response.json();
    },
  });
}

export function useCreatePayment() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (paymentData: {
      amount: number;
      currency: string;
      gateway: string;
      customerEmail: string;
      planId?: string;
    }) => {
      const response = await fetch('/api/brain/business-operations/payments/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paymentData),
      });
      if (!response.ok) {
        throw new Error('Failed to create payment');
      }
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['payment-metrics'] });
      queryClient.invalidateQueries({ queryKey: ['payment-transactions'] });
      toast.success('Payment created successfully');
    },
    onError: (error) => {
      toast.error(`Failed to create payment: ${error.message}`);
    },
  });
}

// Communication Operations Hooks
export function useCommunicationMetrics(timeRange: string = '30d') {
  return useQuery({
    queryKey: ['communication-metrics', timeRange],
    queryFn: async () => {
      const response = await fetch(`/api/brain/business-operations/communications/metrics?timeRange=${timeRange}`);
      if (!response.ok) {
        throw new Error('Failed to fetch communication metrics');
      }
      return response.json() as Promise<CommunicationMetrics>;
    },
    staleTime: 5 * 60 * 1000,
  });
}

export function useCommunicationCampaigns(filters?: {
  status?: string;
  type?: string;
  channel?: string;
}) {
  return useQuery({
    queryKey: ['communication-campaigns', filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters?.status) params.append('status', filters.status);
      if (filters?.type) params.append('type', filters.type);
      if (filters?.channel) params.append('channel', filters.channel);
      
      const response = await fetch(`/api/brain/business-operations/communications/campaigns?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch communication campaigns');
      }
      return response.json();
    },
  });
}

export function useCreateCampaign() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (campaignData: {
      name: string;
      type: string;
      channel: string;
      message: string;
      audience: any;
      schedule?: any;
    }) => {
      const response = await fetch('/api/brain/business-operations/communications/campaigns', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(campaignData),
      });
      if (!response.ok) {
        throw new Error('Failed to create campaign');
      }
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['communication-metrics'] });
      queryClient.invalidateQueries({ queryKey: ['communication-campaigns'] });
      toast.success('Campaign created successfully');
    },
    onError: (error) => {
      toast.error(`Failed to create campaign: ${error.message}`);
    },
  });
}

// SEO Operations Hooks
export function useSEOMetrics(timeRange: string = '30d') {
  return useQuery({
    queryKey: ['seo-metrics', timeRange],
    queryFn: async () => {
      const response = await fetch(`/api/brain/business-operations/seo/metrics?timeRange=${timeRange}`);
      if (!response.ok) {
        throw new Error('Failed to fetch SEO metrics');
      }
      return response.json() as Promise<SEOMetrics>;
    },
    staleTime: 10 * 60 * 1000, // 10 minutes for SEO data
  });
}

export function useSEOKeywords(filters?: {
  searchEngine?: string;
  country?: string;
  limit?: number;
}) {
  return useQuery({
    queryKey: ['seo-keywords', filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters?.searchEngine) params.append('searchEngine', filters.searchEngine);
      if (filters?.country) params.append('country', filters.country);
      if (filters?.limit) params.append('limit', filters.limit.toString());
      
      const response = await fetch(`/api/brain/business-operations/seo/keywords?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch SEO keywords');
      }
      return response.json();
    },
  });
}

export function useSEOAudits() {
  return useQuery({
    queryKey: ['seo-audits'],
    queryFn: async () => {
      const response = await fetch('/api/brain/business-operations/seo/audits');
      if (!response.ok) {
        throw new Error('Failed to fetch SEO audits');
      }
      return response.json();
    },
  });
}

export function useRunSEOAudit() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (auditData: {
      url: string;
      searchEngine?: string;
      country?: string;
    }) => {
      const response = await fetch('/api/brain/business-operations/seo/audits', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(auditData),
      });
      if (!response.ok) {
        throw new Error('Failed to start SEO audit');
      }
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['seo-audits'] });
      toast.success('SEO audit started successfully');
    },
    onError: (error) => {
      toast.error(`Failed to start SEO audit: ${error.message}`);
    },
  });
}

// Analytics Operations Hooks
export function useAnalyticsMetrics(timeRange: string = '30d') {
  return useQuery({
    queryKey: ['analytics-metrics', timeRange],
    queryFn: async () => {
      const response = await fetch(`/api/brain/business-operations/analytics/metrics?timeRange=${timeRange}`);
      if (!response.ok) {
        throw new Error('Failed to fetch analytics metrics');
      }
      return response.json() as Promise<AnalyticsMetrics>;
    },
    staleTime: 5 * 60 * 1000,
  });
}

export function useTrafficSources(timeRange: string = '30d') {
  return useQuery({
    queryKey: ['traffic-sources', timeRange],
    queryFn: async () => {
      const response = await fetch(`/api/brain/business-operations/analytics/traffic-sources?timeRange=${timeRange}`);
      if (!response.ok) {
        throw new Error('Failed to fetch traffic sources');
      }
      return response.json();
    },
  });
}

export function useAnalyticsTrends(timeRange: string = '30d', metrics: string[] = ['visitors', 'pageViews']) {
  return useQuery({
    queryKey: ['analytics-trends', timeRange, metrics],
    queryFn: async () => {
      const params = new URLSearchParams();
      params.append('timeRange', timeRange);
      metrics.forEach(metric => params.append('metrics', metric));
      
      const response = await fetch(`/api/brain/business-operations/analytics/trends?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch analytics trends');
      }
      return response.json();
    },
  });
}

// General Business Operations Hook
export function useBusinessOperationsOverview() {
  return useQuery({
    queryKey: ['business-operations-overview'],
    queryFn: async () => {
      const response = await fetch('/api/brain/business-operations/overview');
      if (!response.ok) {
        throw new Error('Failed to fetch business operations overview');
      }
      return response.json();
    },
    staleTime: 5 * 60 * 1000,
  });
}

export function useRefreshAllMetrics() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async () => {
      const response = await fetch('/api/brain/business-operations/refresh', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to refresh metrics');
      }
      return response.json();
    },
    onSuccess: () => {
      // Invalidate all business operations queries
      queryClient.invalidateQueries({ queryKey: ['payment-metrics'] });
      queryClient.invalidateQueries({ queryKey: ['communication-metrics'] });
      queryClient.invalidateQueries({ queryKey: ['seo-metrics'] });
      queryClient.invalidateQueries({ queryKey: ['analytics-metrics'] });
      queryClient.invalidateQueries({ queryKey: ['business-operations-overview'] });
      toast.success('All business metrics refreshed successfully');
    },
    onError: (error) => {
      toast.error(`Failed to refresh metrics: ${error.message}`);
    },
  });
}