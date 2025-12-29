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
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchMetrics = async () => {
        try {
            setIsLoading(true);

            // Fetch connectors status
            let servicesStatus: Record<string, 'healthy' | 'degraded' | 'down'> = {
                'Brain Hub': 'healthy',
                'CRM': 'down',
                'CMS': 'down',
                'E-commerce': 'down'
            };

            try {
                const response = await fetch('/api/brain/connectors');
                if (response.ok) {
                    const connectors = await response.json();

                    if (Array.isArray(connectors)) {
                        const cms = connectors.find((c: any) => c.type === 'cms' && c.status === 'connected');
                        const crm = connectors.find((c: any) => c.type === 'crm' && c.status === 'connected');
                        const ecommerce = connectors.find((c: any) => c.type === 'ecommerce' && c.status === 'connected');

                        servicesStatus = {
                            'Brain Hub': 'healthy',
                            'CRM': crm ? 'healthy' : 'down',
                            'CMS': cms ? 'healthy' : 'down',
                            'E-commerce': ecommerce ? 'healthy' : 'down'
                        };
                    } else {
                        console.warn("Connectors API returned non-array data:", connectors);
                    }
                }
            } catch (e) {
                console.error("Failed to fetch connectors for status", e);
            }

            setMetrics({
                cpu: 45,
                memory: 60,
                activeUsers: 1,
                apiRequests: 0,
                status: Object.values(servicesStatus).every(s => s === 'healthy') ? 'healthy' : 'degraded',
                services: servicesStatus
            });
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
        isLoading,
        error,
        refreshStatus: fetchMetrics,
        getOverallHealth
    };
}
