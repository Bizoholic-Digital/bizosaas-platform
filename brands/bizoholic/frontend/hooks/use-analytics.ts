'use client'

import { useState, useEffect } from 'react'

export interface TimeSeriesData {
    timestamp: string;
    value: number;
}

export interface ChartData {
    labels: string[];
    datasets: Array<{
        label: string;
        data: number[];
        backgroundColor?: string | string[];
        borderColor?: string | string[];
    }>;
}

export interface DashboardMetrics {
    overview: {
        totalRevenue: number;
        totalOrders: number;
        activeUsers: number;
        conversionRate: number;
    };
    traffic: {
        pageViews: number;
        sessions: number;
        bounceRate: number;
    };
}

export function useDashboardMetrics() {
    const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        // Mock data for now
        setTimeout(() => {
            setMetrics({
                overview: {
                    totalRevenue: 125000,
                    totalOrders: 1420,
                    activeUsers: 856,
                    conversionRate: 3.2
                },
                traffic: {
                    pageViews: 45000,
                    sessions: 12000,
                    bounceRate: 42.5
                }
            });
            setLoading(false);
        }, 500);
    }, []);

    return { metrics, loading, error };
}

export function useTimeSeries(metric: string, timeRange: string = '7d', granularity: string = 'day') {
    const [data, setData] = useState<TimeSeriesData[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        // Generate mock time series data
        const points = parseInt(timeRange) || 7;
        const mockData: TimeSeriesData[] = [];
        const now = new Date();

        for (let i = points; i >= 0; i--) {
            const date = new Date(now);
            date.setDate(date.getDate() - i);
            mockData.push({
                timestamp: date.toISOString(),
                value: Math.floor(Math.random() * 1000) + 500
            });
        }

        setTimeout(() => {
            setData(mockData);
            setLoading(false);
        }, 500);
    }, [metric, timeRange, granularity]);

    return { data, loading, error };
}

export function useChartData(type: string) {
    const [data, setData] = useState<ChartData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        // Mock chart data based on type
        setTimeout(() => {
            if (type === 'traffic-sources') {
                setData({
                    labels: ['Direct', 'Search', 'Social', 'Referral'],
                    datasets: [{
                        label: 'Visitors',
                        data: [4500, 3200, 1500, 800],
                        backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
                    }]
                });
            } else if (type === 'conversion-funnel') {
                setData({
                    labels: ['Visitors', 'Cart', 'Checkout', 'Purchase'],
                    datasets: [{
                        label: 'Conversions',
                        data: [10000, 4500, 2100, 1420]
                    }]
                });
            }
            setLoading(false);
        }, 500);
    }, [type]);

    return { data, loading, error };
}
