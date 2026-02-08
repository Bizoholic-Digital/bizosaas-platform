import { useEffect, useCallback } from 'react';
import { WebSocketClient, WebSocketMessage } from './websocket-client';

// Shared instance for the application
let clientInstance: WebSocketClient | null = null;

const getClient = () => {
    if (typeof window === 'undefined') return null;
    if (!clientInstance) {
        const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL || 'wss://api.bizoholic.net/ws'}/bizoholic/demo-user`;
        clientInstance = new WebSocketClient(wsUrl);
        clientInstance.connect();
    }
    return clientInstance;
};

export function usePerformanceMetrics(callback: (data: any) => void) {
    useEffect(() => {
        const client = getClient();
        if (!client) return;

        const unsubscribe = client.onMessage('performance_metrics', (message: WebSocketMessage) => {
            callback(message.data);
        });

        // Request initial metrics
        client.requestUpdate('performance');

        return unsubscribe;
    }, [callback]);
}

export function useWorkflowUpdates(callback: (data: any) => void) {
    useEffect(() => {
        const client = getClient();
        if (!client) return;

        const unsubscribe = client.onMessage('workflow_update', (message: WebSocketMessage) => {
            callback(message.data);
        });

        // Request initial status
        client.requestUpdate('workflows');

        return unsubscribe;
    }, [callback]);
}

export function useAgentStatus(callback: (data: any) => void) {
    useEffect(() => {
        const client = getClient();
        if (!client) return;

        const unsubscribe = client.onMessage('agent_status', (message: WebSocketMessage) => {
            callback(message.data);
        });

        return unsubscribe;
    }, [callback]);
}

// Re-export hook from client for general use
export { useWebSocket } from './websocket-client';

export type WebSocketEventType =
    | 'performance_metrics'
    | 'workflow_update'
    | 'agent_status'
    | 'notification'
    | 'system_alert'
    | 'broadcast'
    | 'campaign_update'
    | 'agent_status_change'
    | 'workflow_complete'
    | 'lead_created'
    | 'billing_event'
    | 'integration_status'
    | 'content_generated'
    | 'analytics_update';

export interface WebSocketEvent {
    type: WebSocketEventType;
    data: any;
    timestamp: string;
}

export { WebSocketClient };
export type { WebSocketMessage };
