/**
 * Real-time Status Indicators
 * Connection status, system health, and live update indicators
 */

'use client';

import React from 'react';
import { 
  Wifi, 
  WifiOff, 
  Loader2, 
  AlertTriangle, 
  CheckCircle2, 
  Clock,
  Activity,
  Zap,
  Signal,
  RefreshCw
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useConnectionStatus, useRealtimePerformance } from '@/lib/hooks/useRealtime';

interface ConnectionStatusProps {
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
  showDetails?: boolean;
  className?: string;
}

export function RealtimeConnectionStatus({ 
  size = 'md', 
  showText = true, 
  showDetails = false,
  className 
}: ConnectionStatusProps) {
  const { 
    connectionState, 
    isConnected, 
    statusColor, 
    statusText, 
    timeSinceLastUpdate,
    isStale 
  } = useConnectionStatus();

  const sizeMap = {
    sm: { icon: 'h-4 w-4', text: 'text-xs', dot: 'w-2 h-2' },
    md: { icon: 'h-5 w-5', text: 'text-sm', dot: 'w-3 h-3' },
    lg: { icon: 'h-6 w-6', text: 'text-base', dot: 'w-4 h-4' }
  };

  const sizes = sizeMap[size];

  const getIcon = () => {
    switch (connectionState.status) {
      case 'connected':
        return <Wifi className={cn(sizes.icon, statusColor)} />;
      case 'connecting':
      case 'reconnecting':
        return <Loader2 className={cn(sizes.icon, statusColor, 'animate-spin')} />;
      case 'disconnected':
        return <WifiOff className={cn(sizes.icon, statusColor)} />;
      case 'error':
        return <AlertTriangle className={cn(sizes.icon, statusColor)} />;
      default:
        return <WifiOff className={cn(sizes.icon, 'text-gray-400')} />;
    }
  };

  return (
    <div className={cn("flex items-center space-x-2", className)}>
      {/* Status Icon */}
      <div className="relative">
        {getIcon()}
        
        {/* Pulse animation for connected state */}
        {isConnected && (
          <div className={cn(
            "absolute inset-0 rounded-full animate-ping",
            sizes.dot,
            "bg-green-400 opacity-30"
          )} />
        )}
      </div>

      {/* Status Text */}
      {showText && (
        <div className="flex flex-col">
          <span className={cn(sizes.text, statusColor, "font-medium")}>
            {statusText}
          </span>
          
          {showDetails && (
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              {timeSinceLastUpdate !== null && (
                <span>
                  Updated {timeSinceLastUpdate}s ago
                </span>
              )}
              
              {isStale && (
                <span className="text-yellow-600">• Stale data</span>
              )}
              
              {connectionState.reconnectAttempts > 0 && (
                <span>
                  • Attempts: {connectionState.reconnectAttempts}
                </span>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// System Health Indicator
interface SystemHealthProps {
  services?: Array<{
    name: string;
    status: 'healthy' | 'degraded' | 'down';
    responseTime?: number;
    uptime?: number;
  }>;
  showDetails?: boolean;
  compact?: boolean;
}

export function RealtimeSystemHealth({ 
  services = [], 
  showDetails = false, 
  compact = false 
}: SystemHealthProps) {
  const overallHealth = services.length > 0 ? 
    services.filter(s => s.status === 'healthy').length / services.length * 100 : 100;

  const getHealthColor = (health: number) => {
    if (health >= 90) return 'text-green-600';
    if (health >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle2 className="h-4 w-4 text-green-500" />;
      case 'degraded':
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
      case 'down':
        return <AlertTriangle className="h-4 w-4 text-red-500" />;
      default:
        return <AlertTriangle className="h-4 w-4 text-gray-400" />;
    }
  };

  if (compact) {
    return (
      <div className="flex items-center space-x-2">
        <Activity className={cn("h-4 w-4", getHealthColor(overallHealth))} />
        <span className={cn("text-sm font-medium", getHealthColor(overallHealth))}>
          {overallHealth.toFixed(0)}%
        </span>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-gray-900">System Health</h3>
        <div className="flex items-center space-x-2">
          <Activity className={cn("h-4 w-4", getHealthColor(overallHealth))} />
          <span className={cn("text-sm font-semibold", getHealthColor(overallHealth))}>
            {overallHealth.toFixed(1)}%
          </span>
        </div>
      </div>

      {showDetails && services.length > 0 && (
        <div className="space-y-2">
          {services.map((service) => (
            <div key={service.name} className="flex items-center justify-between text-sm">
              <div className="flex items-center space-x-2">
                {getStatusIcon(service.status)}
                <span className="text-gray-700">{service.name}</span>
              </div>
              
              <div className="flex items-center space-x-3 text-xs text-gray-500">
                {service.responseTime && (
                  <span>{service.responseTime}ms</span>
                )}
                {service.uptime && (
                  <span>{service.uptime.toFixed(1)}%</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Performance Metrics Indicator
export function RealtimePerformanceIndicator() {
  const { updateFrequency, lastMetricsUpdate } = useRealtimePerformance();

  const getPerformanceColor = (frequency: number) => {
    if (frequency > 0.5) return 'text-green-600';
    if (frequency > 0.1) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="flex items-center space-x-4 text-xs text-gray-500">
      <div className="flex items-center space-x-1">
        <Zap className={cn("h-3 w-3", getPerformanceColor(updateFrequency))} />
        <span>
          {updateFrequency.toFixed(2)} updates/s
        </span>
      </div>
      
      <div className="flex items-center space-x-1">
        <Signal className="h-3 w-3" />
        <span>
          {Object.keys(lastMetricsUpdate).length} metrics
        </span>
      </div>
    </div>
  );
}

// Live Activity Indicator
interface LiveActivityProps {
  isActive?: boolean;
  lastActivity?: number;
  activityType?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function RealtimeLiveActivity({ 
  isActive = false, 
  lastActivity, 
  activityType = 'data',
  size = 'sm' 
}: LiveActivityProps) {
  const sizeMap = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4'
  };

  const dotSize = sizeMap[size];
  const timeSinceActivity = lastActivity ? Math.floor((Date.now() - lastActivity) / 1000) : null;

  return (
    <div className="flex items-center space-x-2">
      <div className={cn(
        "rounded-full transition-all duration-300",
        dotSize,
        isActive ? "bg-green-500 animate-pulse" : "bg-gray-300"
      )} />
      
      <span className="text-xs text-gray-500">
        {isActive ? (
          `Live ${activityType}`
        ) : timeSinceActivity !== null ? (
          `${timeSinceActivity}s ago`
        ) : (
          'No activity'
        )}
      </span>
    </div>
  );
}

// Connection Quality Indicator
interface ConnectionQualityProps {
  latency?: number;
  packetLoss?: number;
  bandwidth?: number;
  compact?: boolean;
}

export function RealtimeConnectionQuality({ 
  latency = 0, 
  packetLoss = 0, 
  bandwidth = 0,
  compact = false 
}: ConnectionQualityProps) {
  const getQualityScore = () => {
    let score = 100;
    
    // Latency impact (0-50ms good, 50-100ms fair, >100ms poor)
    if (latency > 100) score -= 30;
    else if (latency > 50) score -= 15;
    
    // Packet loss impact
    score -= packetLoss * 50;
    
    return Math.max(0, Math.min(100, score));
  };

  const quality = getQualityScore();
  
  const getQualityColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getQualityText = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  };

  if (compact) {
    return (
      <div className="flex items-center space-x-1">
        <Signal className={cn("h-4 w-4", getQualityColor(quality))} />
        <span className={cn("text-xs", getQualityColor(quality))}>
          {getQualityText(quality)}
        </span>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-3">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-700">Connection Quality</span>
        <span className={cn("text-sm font-semibold", getQualityColor(quality))}>
          {getQualityText(quality)}
        </span>
      </div>
      
      <div className="space-y-1 text-xs text-gray-500">
        <div className="flex justify-between">
          <span>Latency:</span>
          <span>{latency}ms</span>
        </div>
        <div className="flex justify-between">
          <span>Packet Loss:</span>
          <span>{(packetLoss * 100).toFixed(1)}%</span>
        </div>
        {bandwidth > 0 && (
          <div className="flex justify-between">
            <span>Bandwidth:</span>
            <span>{bandwidth.toFixed(1)} Mbps</span>
          </div>
        )}
      </div>
    </div>
  );
}

// Unified Status Bar
export function RealtimeStatusBar() {
  const { isConnected, statusText, timeSinceLastUpdate } = useConnectionStatus();
  const { updateFrequency } = useRealtimePerformance();

  return (
    <div className="flex items-center justify-between bg-gray-50 border-t border-gray-200 px-4 py-2">
      <div className="flex items-center space-x-4">
        <RealtimeConnectionStatus size="sm" showText={false} />
        <span className="text-xs text-gray-600">{statusText}</span>
        
        {isConnected && (
          <>
            <div className="w-px h-4 bg-gray-300" />
            <RealtimeLiveActivity 
              isActive={timeSinceLastUpdate !== null && timeSinceLastUpdate < 30}
              lastActivity={timeSinceLastUpdate ? Date.now() - (timeSinceLastUpdate * 1000) : undefined}
            />
          </>
        )}
      </div>

      <div className="flex items-center space-x-4">
        <RealtimePerformanceIndicator />
        
        <div className="text-xs text-gray-500">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}

export default RealtimeConnectionStatus;