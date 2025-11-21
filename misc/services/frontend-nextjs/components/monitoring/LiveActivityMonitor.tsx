'use client';

// Live Activity Monitor Component for BizOSaaS Dashboard
// Displays real-time events, updates, and system activities

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Activity,
  Bot,
  TrendingUp,
  User,
  AlertTriangle,
  CheckCircle,
  Clock,
  Filter,
  Pause,
  Play,
  Trash2,
  Eye,
  EyeOff,
  Wifi,
  WifiOff
} from 'lucide-react';
import { useRealTimeStore, useNotificationStore } from '@/lib/store';
import { useRealTimeConnection } from '@/lib/websocket';
import { RealTimeUpdate, NotificationPriority } from '@/lib/types';

interface ActivityItemProps {
  update: RealTimeUpdate;
  onDismiss?: (updateId: string) => void;
}

const ActivityItem: React.FC<ActivityItemProps> = ({ update, onDismiss }) => {
  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'agent_status': return <Bot className="h-4 w-4" />;
      case 'campaign_update': return <TrendingUp className="h-4 w-4" />;
      case 'new_lead': return <User className="h-4 w-4" />;
      case 'system_alert': return <AlertTriangle className="h-4 w-4" />;
      case 'workflow_progress': return <CheckCircle className="h-4 w-4" />;
      default: return <Activity className="h-4 w-4" />;
    }
  };

  const getActivityColor = (type: string, priority: string) => {
    if (priority === 'critical') return 'text-red-600 bg-red-50';
    if (priority === 'high') return 'text-orange-600 bg-orange-50';
    
    switch (type) {
      case 'agent_status': return 'text-blue-600 bg-blue-50';
      case 'campaign_update': return 'text-green-600 bg-green-50';
      case 'new_lead': return 'text-purple-600 bg-purple-50';
      case 'system_alert': return 'text-yellow-600 bg-yellow-50';
      case 'workflow_progress': return 'text-teal-600 bg-teal-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getPriorityBadge = (priority: string) => {
    const colors = {
      critical: 'bg-red-100 text-red-800 border-red-200',
      high: 'bg-orange-100 text-orange-800 border-orange-200',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      low: 'bg-gray-100 text-gray-800 border-gray-200'
    };
    
    return (
      <Badge variant="outline" className={colors[priority as keyof typeof colors] || colors.low}>
        {priority}
      </Badge>
    );
  };

  const formatActivityMessage = (update: RealTimeUpdate) => {
    switch (update.type) {
      case 'agent_status':
        return `Agent "${update.data.agent_name || 'Unknown'}" is now ${update.data.status}`;
      case 'campaign_update':
        return `Campaign "${update.data.campaign_name || 'Unknown'}" performance updated`;
      case 'new_lead':
        return `New lead: ${update.data.lead?.name || 'Unknown Contact'}`;
      case 'system_alert':
        return `System alert: ${update.data.service_name} - ${update.data.message}`;
      case 'workflow_progress':
        return `Workflow "${update.data.workflow_name || 'Unknown'}" ${update.data.status}`;
      default:
        return update.message || 'System update received';
    }
  };

  const timeAgo = (timestamp: string) => {
    const now = new Date().getTime();
    const time = new Date(timestamp).getTime();
    const diff = now - time;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  };

  return (
    <div className="flex items-start gap-3 p-3 border-b border-gray-100 hover:bg-gray-50 transition-colors">
      <div className={`p-2 rounded-full ${getActivityColor(update.type, update.priority)}`}>
        {getActivityIcon(update.type)}
      </div>
      
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1">
            <div className="text-sm text-gray-900 mb-1">
              {formatActivityMessage(update)}
            </div>
            
            {update.data.details && (
              <div className="text-xs text-gray-600 bg-gray-50 rounded px-2 py-1 mb-2">
                {typeof update.data.details === 'string' 
                  ? update.data.details 
                  : JSON.stringify(update.data.details, null, 2)
                }
              </div>
            )}
            
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1 text-xs text-gray-500">
                <Clock className="h-3 w-3" />
                {timeAgo(update.timestamp)}
              </div>
              
              {getPriorityBadge(update.priority)}
              
              <Badge variant="outline" className="text-xs capitalize">
                {update.type.replace('_', ' ')}
              </Badge>
            </div>
          </div>
          
          {onDismiss && (
            <Button
              size="sm"
              variant="ghost"
              onClick={() => onDismiss(update.id)}
              className="p-1 h-6 w-6"
            >
              <Trash2 className="h-3 w-3" />
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};

interface LiveActivityMonitorProps {
  className?: string;
  maxItems?: number;
}

export const LiveActivityMonitor: React.FC<LiveActivityMonitorProps> = ({ 
  className, 
  maxItems = 50 
}) => {
  const { updates, connected, lastUpdate } = useRealTimeStore();
  const { notifications, unreadCount } = useNotificationStore();
  const [isPaused, setIsPaused] = useState(false);
  const [filter, setFilter] = useState<string>('all');
  const [isVisible, setIsVisible] = useState(true);
  const [displayedUpdates, setDisplayedUpdates] = useState<RealTimeUpdate[]>([]);

  // Enable real-time connection
  const { connected: rtConnected } = useRealTimeConnection(true);

  // Update displayed items when not paused
  useEffect(() => {
    if (!isPaused) {
      const filtered = updates.filter(update => {
        if (filter === 'all') return true;
        if (filter === 'critical') return update.priority === 'critical';
        if (filter === 'high') return update.priority === 'high' || update.priority === 'critical';
        return update.type === filter;
      }).slice(0, maxItems);
      
      setDisplayedUpdates(filtered);
    }
  }, [updates, filter, maxItems, isPaused]);

  const handleClearAll = () => {
    useRealTimeStore.getState().clearUpdates();
    setDisplayedUpdates([]);
  };

  const handleDismiss = (updateId: string) => {
    setDisplayedUpdates(current => current.filter(update => update.id !== updateId));
  };

  const getFilterCounts = () => {
    return {
      all: updates.length,
      critical: updates.filter(u => u.priority === 'critical').length,
      high: updates.filter(u => u.priority === 'high' || u.priority === 'critical').length,
      agent_status: updates.filter(u => u.type === 'agent_status').length,
      campaign_update: updates.filter(u => u.type === 'campaign_update').length,
      system_alert: updates.filter(u => u.type === 'system_alert').length,
    };
  };

  const counts = getFilterCounts();

  if (!isVisible) {
    return (
      <Card className={className}>
        <CardContent className="p-4">
          <Button
            variant="ghost"
            onClick={() => setIsVisible(true)}
            className="w-full flex items-center justify-center gap-2"
          >
            <Eye className="h-4 w-4" />
            Show Live Activity Monitor
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-lg flex items-center gap-2">
              <Activity className="h-5 w-5" />
              Live Activity Monitor
            </CardTitle>
            <CardDescription>
              Real-time events and system updates
            </CardDescription>
          </div>
          
          <div className="flex items-center gap-2">
            {/* Connection Status */}
            <div className="flex items-center gap-1 text-sm">
              {connected ? (
                <>
                  <Wifi className="h-4 w-4 text-green-500" />
                  <span className="text-green-600">Live</span>
                </>
              ) : (
                <>
                  <WifiOff className="h-4 w-4 text-red-500" />
                  <span className="text-red-600">Offline</span>
                </>
              )}
            </div>

            {/* Control Buttons */}
            <Button
              size="sm"
              variant="outline"
              onClick={() => setIsPaused(!isPaused)}
              className="flex items-center gap-1"
            >
              {isPaused ? (
                <>
                  <Play className="h-3 w-3" />
                  Resume
                </>
              ) : (
                <>
                  <Pause className="h-3 w-3" />
                  Pause
                </>
              )}
            </Button>

            <Button
              size="sm"
              variant="ghost"
              onClick={() => setIsVisible(false)}
            >
              <EyeOff className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-1">
            <Filter className="h-4 w-4 text-gray-500" />
            <span className="text-sm text-gray-600">Filter:</span>
          </div>
          
          {[
            { key: 'all', label: 'All', count: counts.all },
            { key: 'critical', label: 'Critical', count: counts.critical },
            { key: 'high', label: 'High Priority', count: counts.high },
            { key: 'agent_status', label: 'Agents', count: counts.agent_status },
            { key: 'campaign_update', label: 'Campaigns', count: counts.campaign_update },
            { key: 'system_alert', label: 'System', count: counts.system_alert },
          ].map(({ key, label, count }) => (
            <Button
              key={key}
              size="sm"
              variant={filter === key ? 'default' : 'outline'}
              onClick={() => setFilter(key)}
              className="text-xs"
            >
              {label}
              {count > 0 && (
                <Badge variant="secondary" className="ml-1 text-xs">
                  {count}
                </Badge>
              )}
            </Button>
          ))}
        </div>

        {/* Status Bar */}
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center gap-4">
            <span>Total Events: {updates.length}</span>
            <span>Filtered: {displayedUpdates.length}</span>
            {lastUpdate && (
              <span>Last Update: {new Date(lastUpdate).toLocaleTimeString()}</span>
            )}
          </div>
          
          <div className="flex items-center gap-2">
            {isPaused && (
              <Badge variant="outline" className="text-orange-600 border-orange-200">
                Paused
              </Badge>
            )}
            
            <Button
              size="sm"
              variant="ghost"
              onClick={handleClearAll}
              className="text-xs"
            >
              Clear All
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-0">
        <ScrollArea className="h-96">
          {displayedUpdates.length > 0 ? (
            <div>
              {displayedUpdates.map((update) => (
                <ActivityItem
                  key={update.id}
                  update={update}
                  onDismiss={handleDismiss}
                />
              ))}
            </div>
          ) : (
            <div className="p-8 text-center">
              <Activity className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {isPaused ? 'Activity Paused' : 'No Recent Activity'}
              </h3>
              <p className="text-gray-600">
                {isPaused 
                  ? 'Click Resume to see new activity updates'
                  : connected 
                    ? 'Waiting for real-time events from the system'
                    : 'Establishing connection to receive live updates'
                }
              </p>
              
              {!connected && (
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => window.location.reload()}
                  className="mt-4"
                >
                  Retry Connection
                </Button>
              )}
            </div>
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  );
};