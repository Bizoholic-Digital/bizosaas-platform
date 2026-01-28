import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';

// Tenant Management Hooks
export function useTenants() {
    return useQuery({
        queryKey: ['tenants'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/tenants');
            return data;
        },
    });
}

export function useUsers() {
    return useQuery({
        queryKey: ['users'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/users');
            return data;
        },
    });
}

export function useCreateTenant() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (tenantData: any) => {
            const { data } = await apiClient.post('/api/admin/tenants', tenantData);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tenants'] });
        },
    });
}

export function useUpdateTenant() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async ({ id, ...tenantData }: any) => {
            const { data } = await apiClient.put(`/api/admin/tenants/${id}`, tenantData);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tenants'] });
        },
    });
}

export function useDeleteTenant() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (id: string) => {
            const { data } = await apiClient.delete(`/api/admin/tenants/${id}`);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tenants'] });
        },
    });
}

// AI Agent Hooks
export function useAgents() {
    return useQuery({
        queryKey: ['agents'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/agents');
            return data;
        },
    });
}

export function useAgentMetrics(agentId: string) {
    return useQuery({
        queryKey: ['agent-metrics', agentId],
        queryFn: async () => {
            const { data } = await apiClient.get(`/api/agents/${agentId}/metrics`);
            return data;
        },
        enabled: !!agentId,
    });
}

// Connector Hooks
export function useConnectors() {
    return useQuery({
        queryKey: ['connectors'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/connectors');
            return data;
        },
    });
}

export function useConnectorStatus(connectorId: string) {
    return useQuery({
        queryKey: ['connector-status', connectorId],
        queryFn: async () => {
            const { data } = await apiClient.get(`/api/connectors/${connectorId}/status`);
            return data;
        },
        enabled: !!connectorId,
    });
}

// System Health Hooks
export function useSystemHealth() {
    return useQuery({
        queryKey: ['system-health'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/health');
            return data;
        },
        refetchInterval: 30000,
    });
}

export function useServiceLogs(serviceName: string) {
    return useQuery({
        queryKey: ['service-logs', serviceName],
        queryFn: async () => {
            const { data } = await apiClient.get(`/api/admin/logs/${serviceName}`);
            return data;
        },
        enabled: !!serviceName,
    });
}

// Audit Logs Hooks
export function useAuditLogs(filters?: any) {
    return useQuery({
        queryKey: ['audit-logs', filters],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/audit-logs', {
                params: filters,
            });
            return data;
        },
    });
}

// Platform Stats Hook
export function usePlatformStats() {
    return useQuery({
        queryKey: ['platform-stats'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/stats');
            return data;
        },
        refetchInterval: 60000,
    });
}

// Billing Administration Hooks
export function useBillingSummary() {
    return useQuery({
        queryKey: ['admin-billing-summary'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/billing/summary');
            return data;
        },
    });
}

export function useSubscriptions() {
    return useQuery({
        queryKey: ['admin-subscriptions'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/billing/subscriptions');
            return data;
        },
    });
}

// CMS & WP Administration Hooks
export function useConnectedSites() {
    return useQuery({
        queryKey: ['admin-cms-sites'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/cms/sites');
            return data;
        },
    });
}

// Analytics Administration Hooks
export function useGlobalGtmContainers() {
    return useQuery({
        queryKey: ['admin-analytics-gtm'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/analytics/gtm/containers');
            return data;
        },
    });
}

// Agent Administration Hooks
export function useGlobalAgentsRegistry() {
    return useQuery({
        queryKey: ['admin-agents-registry'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/agents/registry');
            return data;
        },
    });
}

// Temporal Administration Hooks
export function useTemporalStatus() {
    return useQuery({
        queryKey: ['admin-temporal-status'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/temporal/status');
            return data;
        },
    });
}

export function useTemporalExecutions() {
    return useQuery({
        queryKey: ['admin-temporal-executions'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/temporal/executions');
            return data;
        },
    });
}

// API Analytics Hook
export function useAPIAnalytics() {
    return useQuery({
        queryKey: ['api-analytics'],
        queryFn: async () => {
            const { data } = await apiClient.get('/api/admin/analytics');
            return data;
        },
        refetchInterval: 10000,
    });
}
