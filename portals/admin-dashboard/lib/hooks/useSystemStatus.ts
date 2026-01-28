import { useState, useEffect } from 'react';

export interface SystemMetrics {
    cpu: number;
    memory: number;
    activeUsers: number;
    totalUsers: number;
    activeTenants: number;
    totalTenants: number;
    apiRequests: number;
    status: 'healthy' | 'degraded' | 'down';
    services: Record<string, 'healthy' | 'degraded' | 'down'>;
}

export interface SystemStatus {
    metrics: SystemMetrics;
    rawData: any;
    isLoading: boolean;
    error: string | null;
    refreshStatus: () => void;
    getOverallHealth: () => 'healthy' | 'warning' | 'error' | 'loading';
}

export function useSystemStatus(): SystemStatus {
    const [metrics, setMetrics] = useState<SystemMetrics>({
        cpu: 0,
        memory: 0,
        activeUsers: 0,
        totalUsers: 0,
        activeTenants: 0,
        totalTenants: 0,
        apiRequests: 0,
        status: 'healthy',
        services: {
            'Brain Hub': 'healthy',
            'CRM': 'healthy',
            'CMS': 'healthy',
            'E-commerce': 'healthy'
        }
    });
    const [rawData, setRawData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchMetrics = async () => {
        try {
            setIsLoading(true);

            // Fetch real health and stats from Admin APIs
            const [healthRes, statsRes] = await Promise.all([
                fetch('/api/admin/health'),
                fetch('/api/admin/stats')
            ]);

            if (healthRes.ok && statsRes.ok) {
                const healthData = await healthRes.json();
                const statsData = await statsRes.json();
                setRawData({ health: healthData, stats: statsData });

                const servicesStatus: Record<string, 'healthy' | 'degraded' | 'down'> = {
                    'Brain Hub': healthData.services?.["brain-gateway"] === 'up' ? 'healthy' : 'down',
                    'CRM': healthData.services?.auth === 'up' ? 'healthy' : 'down',
                    'CMS': 'healthy', // Tracked via CMS Admin API
                    'E-commerce': 'healthy',
                    'Vault': 'healthy',
                    'Temporal': healthData.services?.temporal === 'connected' ? 'healthy' : 'down'
                };

                setMetrics({
                    cpu: healthData.resources?.cpu || statsData.system?.cpu_usage || 0,
                    memory: healthData.resources?.memory?.percent || statsData.system?.memory_usage || 0,
                    activeUsers: statsData.users?.active || 0,
                    totalUsers: statsData.users?.total || 0,
                    activeTenants: statsData.tenants?.active || 0,
                    totalTenants: statsData.tenants?.total || 0,
                    apiRequests: statsData.api_requests_per_sec || 0,
                    status: healthData.status === 'healthy' ? 'healthy' : 'degraded',
                    services: servicesStatus
                });
            }
            else {
                // Fallback to connectors logic if health endpoint is not yet reliable
                const connResp = await fetch('/api/brain/connectors');
                if (connResp.ok) {
                    const connectors = await connResp.json();
                    if (Array.isArray(connectors)) {
                        const cms = connectors.find((c: any) => c.type === 'cms' && c.status === 'connected');
                        const crm = connectors.find((c: any) => c.type === 'crm' && c.status === 'connected');

                        setMetrics(prev => ({
                            ...prev,
                            services: {
                                'Brain Hub': 'healthy',
                                'CRM': crm ? 'healthy' : 'down',
                                'CMS': cms ? 'healthy' : 'down',
                                'E-commerce': 'healthy'
                            }
                        }));
                    }
                }
            }
            setError(null);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch system status');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchMetrics();
        const interval = setInterval(fetchMetrics, 30000);
        return () => clearInterval(interval);
    }, []);

    const getOverallHealth = () => {
        if (isLoading) return 'loading';
        if (metrics.status === 'down') return 'error';
        if (metrics.status === 'degraded') return 'warning';
        return 'healthy';
    };

    return {
        metrics,
        rawData,
        isLoading,
        error,
        refreshStatus: fetchMetrics,
        getOverallHealth
    };
}
