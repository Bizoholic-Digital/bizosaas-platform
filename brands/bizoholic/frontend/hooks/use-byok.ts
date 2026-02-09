'use client';

import { useState, useEffect } from 'react';

export function useBillingEstimation() {
    const [tierComparison, setTierComparison] = useState<any>(null);
    const [estimates, setEstimates] = useState<any>({});
    const [loading, setLoading] = useState({ comparison: true, estimation: false });

    useEffect(() => {
        // Mock data for tier comparison
        const mockTiers = {
            byok_discounted: {
                monthly_base_fee: 49,
                usage_rates: { api_call: 0.0001, campaign_execution: 0.5 },
                included_quotas: { api_call: 5000 },
                best_for: 'Users with their own API keys'
            },
            full_service: {
                monthly_base_fee: 99,
                usage_rates: { api_call: 0.0005, campaign_execution: 1.0 },
                included_quotas: { api_call: 10000 },
                best_for: 'Full platform management'
            },
            pay_per_use: {
                monthly_base_fee: 0,
                usage_rates: { api_call: 0.001, campaign_execution: 2.0 },
                included_quotas: { api_call: 0 },
                best_for: 'Low volume or testing'
            }
        };

        setTimeout(() => {
            setTierComparison(mockTiers);
            setLoading(prev => ({ ...prev, comparison: false }));
        }, 500);
    }, []);

    const estimateCostChange = async (strategy: string) => {
        setLoading(prev => ({ ...prev, estimation: true }));

        // Mock estimation logic
        const mockEstimate = {
            current_monthly_cost: 150,
            proposed_monthly_cost: 85,
            monthly_savings: 65,
            savings_percentage: 43.3,
            annual_savings: 780,
            current_strategy: 'platform_managed',
            proposed_strategy: strategy,
            recommendation: 'switch'
        };

        setTimeout(() => {
            setEstimates(prev => ({ ...prev, [strategy]: mockEstimate }));
            setLoading(prev => ({ ...prev, estimation: false }));
        }, 800);
    };

    return { tierComparison, estimates, loading, estimateCostChange };
}

export function useIntegrationManagement() {
    const [loading, setLoading] = useState<Record<string, boolean>>({});

    const createIntegration = async (platformId: string, credentials: Record<string, string>) => {
        setLoading(prev => ({ ...prev, [platformId]: true }));
        // Mock implementation
        await new Promise(resolve => setTimeout(resolve, 800));
        setLoading(prev => ({ ...prev, [platformId]: false }));
        return { id: `int_${Math.random().toString(36).substr(2, 9)}`, platform_id: platformId, credentials };
    };

    const updateIntegration = async (integrationId: string, credentials: Record<string, string>) => {
        setLoading(prev => ({ ...prev, [integrationId]: true }));
        await new Promise(resolve => setTimeout(resolve, 800));
        setLoading(prev => ({ ...prev, [integrationId]: false }));
        return { id: integrationId, credentials };
    };

    const testIntegration = async (integrationId: string) => {
        setLoading(prev => ({ ...prev, [`test-${integrationId}`]: true }));
        await new Promise(resolve => setTimeout(resolve, 1000));
        setLoading(prev => ({ ...prev, [`test-${integrationId}`]: false }));
        return { success: true };
    };

    return { createIntegration, updateIntegration, testIntegration, loading };
}

export function useCredentialHealth(options: { autoRefresh?: boolean; refreshInterval?: number } = {}) {
    const [health, setHealth] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const refresh = async () => {
        setLoading(true);
        // Mock health data
        const mockHealth = {
            health_statuses: [
                {
                    platform: 'openai',
                    is_healthy: true,
                    last_check: new Date().toISOString(),
                    expires_at: new Date(Date.now() + 1000 * 60 * 60 * 24 * 90).toISOString(),
                    usage_quota_remaining: 15600,
                    error_message: null
                },
                {
                    platform: 'anthropic',
                    is_healthy: true,
                    last_check: new Date().toISOString(),
                    expires_at: null,
                    usage_quota_remaining: 8500,
                    error_message: null
                }
            ]
        };

        setTimeout(() => {
            setHealth(mockHealth);
            setLoading(false);
        }, 800);
    };

    useEffect(() => {
        refresh();

        if (options.autoRefresh) {
            const interval = setInterval(refresh, options.refreshInterval || 30000);
            return () => clearInterval(interval);
        }
    }, [options.autoRefresh, options.refreshInterval]);

    const healthyCount = health?.health_statuses.filter((s: any) => s.is_healthy).length || 0;
    const totalCount = health?.health_statuses.length || 0;
    const healthPercentage = totalCount > 0 ? (healthyCount / totalCount) * 100 : 0;

    return { health, loading, error, refresh, healthyCount, totalCount, healthPercentage };
}

export function useBYOK() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const refresh = async () => {
        setLoading(true);
        await new Promise(resolve => setTimeout(resolve, 800));
        setLoading(false);
    };

    return { refresh, loading, error };
}

export function useCredentialMigration() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [migrationResult, setMigrationResult] = useState<any>(null);

    const migrateStrategy = async (strategy: string, platforms?: string[]) => {
        setLoading(true);
        setError(null);

        // Mock migration logic
        await new Promise(resolve => setTimeout(resolve, 1500));

        setMigrationResult({
            successful_platforms: platforms || ['openai', 'anthropic'],
            failed_platforms: []
        });

        setLoading(false);
    };

    return { migrateStrategy, migrationResult, loading, error };
}

export function useCredentialResolution() {
    const [resolvedCredentials, setResolvedCredentials] = useState<Record<string, any>>({});
    const [loading, setLoading] = useState<Record<string, boolean>>({});

    const resolveCredentials = async (platformId: string) => {
        setLoading(prev => ({ ...prev, [platformId]: true }));

        // Mock resolution logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        setResolvedCredentials(prev => ({
            ...prev,
            [platformId]: {
                health_status: 'healthy',
                source: 'tenant'
            }
        }));

        setLoading(prev => ({ ...prev, [platformId]: false }));
    };

    return { resolvedCredentials, loading, resolveCredentials };
}
