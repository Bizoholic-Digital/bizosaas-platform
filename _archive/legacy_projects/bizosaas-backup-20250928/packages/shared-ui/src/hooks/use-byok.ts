/**
 * React hooks for BYOK functionality
 * Provides state management and API integration for credential management
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { toast } from 'sonner';
import { 
  byokApi, 
  ResolvedCredentials, 
  TenantCredentialHealth, 
  BillingEstimate,
  BillingTierComparison,
  MigrationResult,
  SUPPORTED_PLATFORMS 
} from '@/lib/api/byok-api';

export interface UseCredentialHealthOptions {
  refreshInterval?: number;
  autoRefresh?: boolean;
}

export function useCredentialHealth(options: UseCredentialHealthOptions = {}) {
  const { refreshInterval = 30000, autoRefresh = true } = options;
  
  const [health, setHealth] = useState<TenantCredentialHealth | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHealth = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const healthData = await byokApi.validateTenantCredentials();
      setHealth(healthData);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch credential health';
      setError(errorMessage);
      console.error('Credential health fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHealth();

    if (autoRefresh && refreshInterval > 0) {
      const interval = setInterval(fetchHealth, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetchHealth, autoRefresh, refreshInterval]);

  return {
    health,
    loading,
    error,
    refresh: fetchHealth,
    healthyCount: health?.healthy_count || 0,
    totalCount: health?.total_integrations || 0,
    healthPercentage: health ? Math.round((health.healthy_count / health.total_integrations) * 100) : 0,
  };
}

export function useCredentialResolution() {
  const [resolvedCredentials, setResolvedCredentials] = useState<Record<string, ResolvedCredentials>>({});
  const [loading, setLoading] = useState<Record<string, boolean>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});

  const resolveCredentials = useCallback(async (platform: string) => {
    try {
      setLoading(prev => ({ ...prev, [platform]: true }));
      setErrors(prev => ({ ...prev, [platform]: '' }));
      
      const resolved = await byokApi.getResolvedCredentials(platform);
      setResolvedCredentials(prev => ({ ...prev, [platform]: resolved }));
      
      return resolved;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : `Failed to resolve credentials for ${platform}`;
      setErrors(prev => ({ ...prev, [platform]: errorMessage }));
      throw err;
    } finally {
      setLoading(prev => ({ ...prev, [platform]: false }));
    }
  }, []);

  const resolveAllPlatforms = useCallback(async () => {
    const platforms = SUPPORTED_PLATFORMS.map(p => p.id);
    const results = await Promise.allSettled(
      platforms.map(platform => resolveCredentials(platform))
    );
    
    return results.map((result, index) => ({
      platform: platforms[index],
      success: result.status === 'fulfilled',
      data: result.status === 'fulfilled' ? result.value : null,
      error: result.status === 'rejected' ? result.reason : null,
    }));
  }, [resolveCredentials]);

  return {
    resolvedCredentials,
    loading,
    errors,
    resolveCredentials,
    resolveAllPlatforms,
  };
}

export function useBillingEstimation() {
  const [estimates, setEstimates] = useState<Record<string, BillingEstimate>>({});
  const [tierComparison, setTierComparison] = useState<BillingTierComparison | null>(null);
  const [loading, setLoading] = useState<Record<string, boolean>>({});
  const [error, setError] = useState<string | null>(null);

  const estimateCostChange = useCallback(async (proposedStrategy: string) => {
    try {
      setLoading(prev => ({ ...prev, [proposedStrategy]: true }));
      setError(null);
      
      const estimate = await byokApi.estimateBillingChanges(proposedStrategy);
      setEstimates(prev => ({ ...prev, [proposedStrategy]: estimate }));
      
      return estimate;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to estimate billing changes';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(prev => ({ ...prev, [proposedStrategy]: false }));
    }
  }, []);

  const fetchTierComparison = useCallback(async () => {
    try {
      setLoading(prev => ({ ...prev, comparison: true }));
      setError(null);
      
      const comparison = await byokApi.getBillingTierComparison();
      setTierComparison(comparison);
      
      return comparison;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch billing tier comparison';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(prev => ({ ...prev, comparison: false }));
    }
  }, []);

  useEffect(() => {
    fetchTierComparison();
  }, [fetchTierComparison]);

  return {
    estimates,
    tierComparison,
    loading,
    error,
    estimateCostChange,
    fetchTierComparison,
  };
}

export function useCredentialMigration() {
  const [migrationResult, setMigrationResult] = useState<MigrationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const migrateStrategy = useCallback(async (
    newStrategy: string,
    platforms?: string[]
  ) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await byokApi.migrateCredentialStrategy(newStrategy, platforms);
      setMigrationResult(result);
      
      // Show success/failure notifications
      if (result.successful_platforms.length > 0) {
        toast.success(
          `Successfully migrated ${result.successful_platforms.length} platform(s) to ${newStrategy}`
        );
      }
      
      if (result.failed_platforms.length > 0) {
        toast.error(
          `Failed to migrate ${result.failed_platforms.length} platform(s): ${result.failed_platforms.join(', ')}`
        );
      }
      
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Migration failed';
      setError(errorMessage);
      toast.error(`Migration failed: ${errorMessage}`);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    migrationResult,
    loading,
    error,
    migrateStrategy,
  };
}

export function useIntegrationManagement() {
  const [integrations, setIntegrations] = useState<any[]>([]);
  const [loading, setLoading] = useState<Record<string, boolean>>({});
  const [error, setError] = useState<string | null>(null);

  const fetchIntegrations = useCallback(async () => {
    try {
      setLoading(prev => ({ ...prev, fetch: true }));
      setError(null);
      
      const data = await byokApi.getIntegrations();
      setIntegrations(data);
      
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch integrations';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(prev => ({ ...prev, fetch: false }));
    }
  }, []);

  const createIntegration = useCallback(async (
    platform: string,
    credentials: Record<string, string>
  ) => {
    try {
      setLoading(prev => ({ ...prev, [platform]: true }));
      setError(null);
      
      const integration = await byokApi.createIntegration(platform, credentials);
      
      // Refresh integrations list
      await fetchIntegrations();
      
      toast.success(`Successfully connected to ${platform}`);
      return integration;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : `Failed to connect to ${platform}`;
      setError(errorMessage);
      toast.error(errorMessage);
      throw err;
    } finally {
      setLoading(prev => ({ ...prev, [platform]: false }));
    }
  }, [fetchIntegrations]);

  const updateIntegration = useCallback(async (
    integrationId: string,
    credentials: Record<string, string>
  ) => {
    try {
      setLoading(prev => ({ ...prev, [integrationId]: true }));
      setError(null);
      
      await byokApi.updateIntegration(integrationId, credentials);
      
      // Refresh integrations list
      await fetchIntegrations();
      
      toast.success('Integration updated successfully');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update integration';
      setError(errorMessage);
      toast.error(errorMessage);
      throw err;
    } finally {
      setLoading(prev => ({ ...prev, [integrationId]: false }));
    }
  }, [fetchIntegrations]);

  const testIntegration = useCallback(async (integrationId: string) => {
    try {
      setLoading(prev => ({ ...prev, [`test-${integrationId}`]: true }));
      setError(null);
      
      const result = await byokApi.testIntegration(integrationId);
      
      if (result.success) {
        toast.success('Connection test successful');
      } else {
        toast.error(`Connection test failed: ${result.error}`);
      }
      
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Connection test failed';
      setError(errorMessage);
      toast.error(errorMessage);
      throw err;
    } finally {
      setLoading(prev => ({ ...prev, [`test-${integrationId}`]: false }));
    }
  }, []);

  const deleteIntegration = useCallback(async (integrationId: string) => {
    try {
      setLoading(prev => ({ ...prev, [`delete-${integrationId}`]: true }));
      setError(null);
      
      await byokApi.deleteIntegration(integrationId);
      
      // Refresh integrations list
      await fetchIntegrations();
      
      toast.success('Integration deleted successfully');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete integration';
      setError(errorMessage);
      toast.error(errorMessage);
      throw err;
    } finally {
      setLoading(prev => ({ ...prev, [`delete-${integrationId}`]: false }));
    }
  }, [fetchIntegrations]);

  useEffect(() => {
    fetchIntegrations();
  }, [fetchIntegrations]);

  return {
    integrations,
    loading,
    error,
    fetchIntegrations,
    createIntegration,
    updateIntegration,
    testIntegration,
    deleteIntegration,
  };
}

// Main BYOK hook that combines all functionality
export function useBYOK() {
  const credentialHealth = useCredentialHealth();
  const credentialResolution = useCredentialResolution();
  const billingEstimation = useBillingEstimation();
  const credentialMigration = useCredentialMigration();
  const integrationManagement = useIntegrationManagement();

  return {
    ...credentialHealth,
    ...credentialResolution,
    ...billingEstimation,
    ...credentialMigration,
    ...integrationManagement,
    // Provide easy access to sub-hooks
    hooks: {
      credentialHealth,
      credentialResolution,
      billingEstimation,
      credentialMigration,
      integrationManagement,
    }
  };
}