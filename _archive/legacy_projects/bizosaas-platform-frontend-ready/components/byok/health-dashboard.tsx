/**
 * BYOK Health Dashboard Component
 * Displays credential health status and monitoring information
 */

'use client';

import { useState } from 'react';
import { 
  CheckCircle, 
  AlertCircle, 
  XCircle, 
  Loader2, 
  RefreshCw, 
  Calendar,
  TrendingUp,
  AlertTriangle,
  Settings
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { useCredentialHealth } from '@/hooks/use-byok';
import { SUPPORTED_PLATFORMS } from '@/lib/api/byok-api';

interface HealthDashboardProps {
  className?: string;
  showDetails?: boolean;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

export function HealthDashboard({ 
  className, 
  showDetails = true, 
  autoRefresh = true,
  refreshInterval = 30000 
}: HealthDashboardProps) {
  const { health, loading, error, refresh, healthyCount, totalCount, healthPercentage } = useCredentialHealth({
    autoRefresh,
    refreshInterval
  });

  const [refreshing, setRefreshing] = useState(false);

  const handleManualRefresh = async () => {
    setRefreshing(true);
    await refresh();
    setRefreshing(false);
  };

  const getHealthIcon = (isHealthy: boolean) => {
    return isHealthy ? (
      <CheckCircle className="h-4 w-4 text-green-500" />
    ) : (
      <XCircle className="h-4 w-4 text-red-500" />
    );
  };

  const getHealthBadge = (isHealthy: boolean) => {
    return (
      <Badge variant={isHealthy ? "default" : "destructive"} className="ml-2">
        {isHealthy ? 'Healthy' : 'Error'}
      </Badge>
    );
  };

  const getPlatformInfo = (platformId: string) => {
    return SUPPORTED_PLATFORMS.find(p => p.id === platformId) || {
      name: platformId,
      icon: '🔧',
      description: 'Integration'
    };
  };

  const formatLastCheck = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffMinutes < 1) return 'Just now';
    if (diffMinutes < 60) return `${diffMinutes}m ago`;
    if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}h ago`;
    return date.toLocaleDateString();
  };

  const formatExpiryDate = (dateString: string | null) => {
    if (!dateString) return 'No expiration';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.ceil((date.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return '⚠️ Expired';
    if (diffDays < 7) return `⚠️ Expires in ${diffDays} days`;
    if (diffDays < 30) return `⏰ Expires in ${diffDays} days`;
    return `✅ Expires ${date.toLocaleDateString()}`;
  };

  if (loading && !health) {
    return (
      <Card className={className}>
        <CardContent className="flex items-center justify-center p-6">
          <Loader2 className="h-6 w-6 animate-spin mr-2" />
          <span>Loading credential health...</span>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardContent className="p-6">
          <Alert>
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>
              Failed to load credential health: {error}
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    );
  }

  if (!health) {
    return (
      <Card className={className}>
        <CardContent className="p-6">
          <Alert>
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              No credential health data available. Configure your integrations to get started.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className={className}>
      {/* Health Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Credential Health Overview
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={handleManualRefresh}
              disabled={refreshing}
              className="flex items-center gap-2"
            >
              <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </CardTitle>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {/* Overall Health Score */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span>Overall Health Score</span>
              <span className="font-medium">{healthyCount}/{totalCount} Healthy</span>
            </div>
            <Progress value={healthPercentage} className="h-2" />
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span>{healthPercentage}% of integrations are healthy</span>
              <span>Last updated: {health.health_statuses[0] ? formatLastCheck(health.health_statuses[0].last_check) : 'Never'}</span>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-3 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{healthyCount}</div>
              <div className="text-sm text-green-700">Healthy</div>
            </div>
            <div className="text-center p-3 bg-red-50 rounded-lg">
              <div className="text-2xl font-bold text-red-600">{totalCount - healthyCount}</div>
              <div className="text-sm text-red-700">Issues</div>
            </div>
            <div className="text-center p-3 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{totalCount}</div>
              <div className="text-sm text-blue-700">Total</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Detailed Health Status */}
      {showDetails && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              Platform Integration Details
            </CardTitle>
          </CardHeader>
          
          <CardContent>
            <div className="space-y-4">
              {health.health_statuses.map((status, index) => {
                const platform = getPlatformInfo(status.platform);
                
                return (
                  <div 
                    key={index} 
                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{platform.icon}</span>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="font-medium">{platform.name}</h4>
                          {getHealthBadge(status.is_healthy)}
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {platform.description}
                        </p>
                      </div>
                    </div>
                    
                    <div className="text-right space-y-1">
                      <div className="flex items-center gap-2">
                        {getHealthIcon(status.is_healthy)}
                        <span className="text-sm font-medium">
                          {status.is_healthy ? 'Connected' : 'Connection Failed'}
                        </span>
                      </div>
                      
                      <div className="text-xs text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          Last check: {formatLastCheck(status.last_check)}
                        </div>
                        
                        {status.expires_at && (
                          <div className="mt-1">
                            {formatExpiryDate(status.expires_at)}
                          </div>
                        )}
                        
                        {status.usage_quota_remaining !== null && (
                          <div className="mt-1">
                            Quota: {status.usage_quota_remaining?.toLocaleString()} remaining
                          </div>
                        )}
                      </div>
                      
                      {status.error_message && (
                        <Alert className="mt-2 max-w-md">
                          <AlertTriangle className="h-4 w-4" />
                          <AlertDescription className="text-xs">
                            {status.error_message}
                          </AlertDescription>
                        </Alert>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default HealthDashboard;