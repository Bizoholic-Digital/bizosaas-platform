'use client';

import { useState, useEffect } from 'react';

export function useApiGatewayDashboard() {
    const [data, setData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Mock data for API Gateway Dashboard
        const mockData = {
            status: 'healthy',
            throughput: '1.2k req/s',
            latency: '45ms',
            error_rate: '0.02%',
            active_connections: 856
        };

        setTimeout(() => {
            setData(mockData);
            setIsLoading(false);
        }, 500);
    }, []);

    return { data, isLoading };
}
