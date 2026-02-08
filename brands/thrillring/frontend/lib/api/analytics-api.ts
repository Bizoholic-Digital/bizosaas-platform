
export interface TimeSeriesData {
    timestamp: string;
    value: number;
    label: string;
}

export interface ChartData {
    labels: string[];
    datasets: {
        label: string;
        data: number[];
        backgroundColor: string | string[];
    }[];
}

export interface RealtimeMetrics {
    currentUsers: number;
    pageViews: number;
    revenue: number;
    leads: number;
    campaigns?: {
        impressions: number;
        clicks: number;
        conversions: number;
    };
    alerts?: {
        id: string;
        type: string;
        message: string;
        timestamp: string;
    }[];
}

export interface DashboardMetrics {
    overview: {
        totalUsers: number;
        activeUsers: number;
        totalRevenue: number;
        monthlyRevenue: number;
        revenueGrowth: number;
        userGrowth: number;
        conversionRate: number;
        churnRate: number;
    };
    traffic: {
        pageViews: number;
        uniqueVisitors: number;
        bounceRate: number;
        avgSessionDuration: number;
        topPages: { page: string; views: number }[];
        trafficSources: { source: string; visitors: number; percentage: number }[];
    };
    campaigns: {
        activeCampaigns: number;
        totalImpressions: number;
        totalClicks: number;
        averageCTR: number;
        topPerformingCampaigns: {
            id: string;
            name: string;
            impressions: number;
            clicks: number;
            ctr: number;
            conversions: number;
            cost: number;
        }[];
    };
    leads: {
        totalLeads: number;
        newLeadsToday: number;
        qualifiedLeads: number;
        convertedLeads: number;
        leadsBySource: { source: string; count: number }[];
        conversionFunnel: { stage: string; count: number; rate: number }[];
    };
}

// Mock implementation of the API
export const analyticsApi = {
    getDashboardMetrics: async (timeRange: string): Promise<DashboardMetrics> => {
        return {} as DashboardMetrics; // Returns mock or empty, caller handles errors/mocking
    },
    getTrafficTimeSeries: async (range: string, granularity: string): Promise<TimeSeriesData[]> => [],
    getRevenueTimeSeries: async (range: string, granularity: string): Promise<TimeSeriesData[]> => [],
    getLeadsTimeSeries: async (range: string, granularity: string): Promise<TimeSeriesData[]> => [],
    getCampaignPerformanceTimeSeries: async (range: string): Promise<TimeSeriesData[]> => [],
    getTrafficSourcesChart: async (): Promise<ChartData> => ({ labels: [], datasets: [] }),
    getConversionFunnelChart: async (): Promise<ChartData> => ({ labels: [], datasets: [] }),
    getRevenueBreakdownChart: async (): Promise<ChartData> => ({ labels: [], datasets: [] }),
    getCampaignROIChart: async (): Promise<ChartData> => ({ labels: [], datasets: [] }),
    connectRealtime: (callback: (data: RealtimeMetrics) => void) => {
        return () => { }; // Cleanup function
    },
    trackEvent: async (event: any) => { },
    exportData: async (config: any): Promise<Blob> => new Blob(),
};

/**
 * Formats a numeric value based on the specified type
 */
export function formatMetricValue(value: number, type: 'currency' | 'number' | 'percentage' | 'time'): string {
    if (value === undefined || value === null) return '0';

    switch (type) {
        case 'currency':
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0,
            }).format(value);
        case 'percentage':
            return `${value.toFixed(1)}%`;
        case 'time':
            if (value >= 3600) return `${(value / 3600).toFixed(1)}h`;
            if (value >= 60) return `${(value / 60).toFixed(1)}m`;
            return `${value.toFixed(0)}s`;
        case 'number':
        default:
            return value.toLocaleString();
    }
}

/**
 * Generates an array of colors for charts
 */
export function generateChartColors(count: number): string[] {
    const baseColors = [
        '#3B82F6', // blue-500
        '#10B981', // emerald-500
        '#F59E0B', // amber-500
        '#EF4444', // red-500
        '#8B5CF6', // purple-500
        '#EC4899', // pink-500
        '#06B6D4', // cyan-500
        '#F97316', // orange-500
    ];

    if (count <= baseColors.length) {
        return baseColors.slice(0, count);
    }

    // Generate more colors if needed
    const colors = [...baseColors];
    for (let i = baseColors.length; i < count; i++) {
        const hue = (i * 137.508) % 360; // Use golden angle for even distribution
        colors.push(`hsl(${hue}, 70%, 50%)`);
    }

    return colors;
}
