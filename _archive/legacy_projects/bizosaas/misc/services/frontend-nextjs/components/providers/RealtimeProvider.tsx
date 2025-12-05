/**
 * Real-time WebSocket Provider
 * Manages WebSocket connection and provides real-time data to the entire application
 */

'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRealtimeConnection } from '@/lib/hooks/useRealtime';
import { RealtimeToastContainer } from '@/components/realtime/RealtimeNotifications';
import { WebSocketConfig, SubscriptionOptions } from '@/lib/websocket/types';

interface RealtimeContextType {
  isConnected: boolean;
  connectionState: any;
  reconnect: () => Promise<void>;
  subscribe: (options: SubscriptionOptions) => void;
  unsubscribe: () => void;
}

const RealtimeContext = createContext<RealtimeContextType | null>(null);

interface RealtimeProviderProps {
  children: ReactNode;
  config?: WebSocketConfig;
  subscription?: SubscriptionOptions;
  enableToasts?: boolean;
}

export function RealtimeProvider({ 
  children, 
  config,
  subscription,
  enableToasts = true 
}: RealtimeProviderProps) {
  const [isInitialized, setIsInitialized] = useState(false);

  // Default configuration
  const defaultConfig: WebSocketConfig = {
    url: process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'ws://localhost:8001/ws/realtime',
    heartbeatInterval: 30000,
    reconnectInterval: 1000,
    maxReconnectAttempts: 10,
    backoffMultiplier: 1.5,
    maxBackoffDelay: 30000,
    ...config
  };

  // Default subscription options
  const defaultSubscription: SubscriptionOptions = {
    metrics: ['dashboard', 'social_media', 'campaigns', 'leads', 'system_health', 'ai_agents'],
    notifications: true,
    events: ['campaign', 'lead', 'payment', 'system', 'ai_agent'],
    real_time_updates: true,
    ...subscription
  };

  const {
    client,
    connectionState,
    isConnected,
    connect,
    disconnect,
    subscribe: subscribeToUpdates,
    unsubscribe,
    reconnect
  } = useRealtimeConnection(defaultConfig);

  // Initialize connection on mount
  useEffect(() => {
    if (!isInitialized && client) {
      setIsInitialized(true);
      
      // Auto-connect with default subscription
      connect(defaultSubscription).catch(error => {
        console.error('Failed to establish initial connection:', error);
      });
    }

    // Cleanup on unmount
    return () => {
      if (client && isInitialized) {
        disconnect();
      }
    };
  }, [client, isInitialized]);

  // Monitor connection state
  useEffect(() => {
    if (connectionState.status === 'error') {
      console.error('WebSocket connection error:', connectionState.error);
    }
  }, [connectionState]);

  const contextValue: RealtimeContextType = {
    isConnected,
    connectionState,
    reconnect,
    subscribe: subscribeToUpdates,
    unsubscribe
  };

  return (
    <RealtimeContext.Provider value={contextValue}>
      {children}
      {enableToasts && <RealtimeToastContainer />}
    </RealtimeContext.Provider>
  );
}

// Hook to use the realtime context
export function useRealtimeContext(): RealtimeContextType {
  const context = useContext(RealtimeContext);
  
  if (!context) {
    throw new Error('useRealtimeContext must be used within a RealtimeProvider');
  }
  
  return context;
}

// Higher-order component for components that need realtime data
export function withRealtime<P extends object>(
  Component: React.ComponentType<P>,
  options?: {
    subscription?: SubscriptionOptions;
    requireConnection?: boolean;
  }
) {
  return function WrappedComponent(props: P) {
    const { isConnected, subscribe } = useRealtimeContext();
    const [hasSubscribed, setHasSubscribed] = useState(false);

    useEffect(() => {
      if (isConnected && options?.subscription && !hasSubscribed) {
        subscribe(options.subscription);
        setHasSubscribed(true);
      }
    }, [isConnected, hasSubscribed]);

    // If connection is required but not available, show loading state
    if (options?.requireConnection && !isConnected) {
      return (
        <div className="flex items-center justify-center p-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Connecting to real-time data...</p>
          </div>
        </div>
      );
    }

    return <Component {...props} />;
  };
}

export default RealtimeProvider;