import { useState, useEffect } from 'react';

export interface SystemMetrics {
  cpu: number;
  memory: number;
  activeUsers: number;
  apiRequests: number;
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
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Simulate fetching system status
    // In production, this would call the actual API
    const fetchMetrics = async () => {
      try {
        setIsLoading(true);
        // Simulated metrics for now
        setMetrics({
          cpu: Math.floor(Math.random() * 100),
          memory: Math.floor(Math.random() * 100),
          activeUsers: Math.floor(Math.random() * 1000),
          apiRequests: Math.floor(Math.random() * 10000),
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
