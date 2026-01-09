import { useState, useEffect } from 'react';

export interface SystemMetrics {
    cpu: number;
    memory: number;
    activeUsers: number;
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

            // Fetch real health data from Brain Gateway
            const response = await fetch('/api/brain/health');
            if (response.ok) {
                const healthData = await response.json();
                setRawData(healthData);

                // Map services status
                const servicesStatus: Record<string, 'healthy' | 'degraded' | 'down'> = {
                    'Brain Hub': healthData.dependencies?.database?.status === 'up' ? 'healthy' : 'down',
                    'CRM': healthData.dependencies?.services?.crm === 'up' ? 'healthy' : 'down',
                    'CMS': healthData.dependencies?.services?.cms === 'up' ? 'healthy' : 'down',
                    'E-commerce': 'healthy', // Fallback
                    'Vault': healthData.dependencies?.vault?.status === 'up' ? 'healthy' : 'down',
                    'Temporal': healthData.dependencies?.temporal?.status === 'up' ? 'healthy' : 'down'
                };

                setMetrics({
                    cpu: healthData.system?.cpu_percent || 0,
                    memory: healthData.system?.memory_percent || 0,
                    activeUsers: 1, // Placeholder until user session counting is implemented
                    apiRequests: 0, // Placeholder
                    status: healthData.status === 'healthy' ? 'healthy' : 'degraded',
                    services: servicesStatus
                });
            } else {
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
