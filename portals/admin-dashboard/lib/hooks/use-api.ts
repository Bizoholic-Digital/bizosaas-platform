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
        refetchInterval: 30000, // Refresh every 30 seconds
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
        refetchInterval: 60000, // Refresh every minute
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
        refetchInterval: 10000, // Refresh every 10 seconds
    });
}
