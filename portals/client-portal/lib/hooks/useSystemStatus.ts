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

  useEffect(() => {
    // Simulate fetching system status
    // In production, this would call the actual API
    const fetchMetrics = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('/api/brain/health');
        if (!response.ok) throw new Error('System unavailable');

        const data = await response.json();

        setMetrics({
          cpu: 45, // Placeholder until backend provides metrics
          memory: 60, // Placeholder
          activeUsers: 1, // Placeholder
          apiRequests: 0, // Placeholder
          status: 'healthy',
          services: {
            'Brain Hub': 'healthy',
            'CRM': 'healthy', // derived from overall health for now
            'CMS': 'healthy',
            'E-commerce': 'healthy'
          }
        });
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch system status');
      } finally {
        setIsLoading(false);
      }
    };

    fetchMetrics();

    // Refresh metrics every 30 seconds
    const interval = setInterval(fetchMetrics, 30000);

    return () => clearInterval(interval);
  }, []);

  return { metrics, isLoading, error };
}
