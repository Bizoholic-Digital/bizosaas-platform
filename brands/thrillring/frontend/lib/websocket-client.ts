'use client'

import { useEffect, useRef, useState, useCallback } from 'react';
import { useSession } from 'next-auth/react';

export interface WebSocketMessage {
    type: string;
    data: any;
    timestamp: string;
    agent_id?: string;
}

export class WebSocketClient {
    private url: string;
    private socket: WebSocket | null = null;
    private listeners: Map<string, Set<(data: any) => void>> = new Map();
    private connectionListeners: Set<(connected: boolean) => void> = new Set();
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;

    constructor(url: string) {
        this.url = url;
    }

    connect() {
        if (this.socket?.readyState === WebSocket.OPEN) return;

        try {
            this.socket = new WebSocket(this.url);

            this.socket.onmessage = (event) => {
                const message: WebSocketMessage = JSON.parse(event.data);
                const eventListeners = this.listeners.get(message.type);
                if (eventListeners) {
                    eventListeners.forEach(callback => callback(message));
                }
            };

            this.socket.onclose = () => {
                console.log('WebSocket disconnected');
                this.connectionListeners.forEach(callback => callback(false));
                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    this.reconnectAttempts++;
                    setTimeout(() => this.connect(), 1000 * this.reconnectAttempts);
                }
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            this.socket.onopen = () => {
                console.log('WebSocket connected');
                this.reconnectAttempts = 0;
                this.connectionListeners.forEach(callback => callback(true));
            };
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
        }
    }

    disconnect() {
        this.socket?.close();
        this.socket = null;
    }

    onMessage(type: string, callback: (data: any) => void) {
        if (!this.listeners.has(type)) {
            this.listeners.set(type, new Set());
        }
        this.listeners.get(type)!.add(callback);

        return () => {
            this.listeners.get(type)?.delete(callback);
        };
    }

    onConnection(callback: (connected: boolean) => void) {
        this.connectionListeners.add(callback);
        // Immediately call with current state
        callback(this.socket?.readyState === WebSocket.OPEN);
        return () => {
            this.connectionListeners.delete(callback);
        };
    }

    send(data: any) {
        if (this.socket?.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({ ...data, timestamp: new Date().toISOString() }));
        } else {
            console.warn('WebSocket not connected. Failed to send message');
        }
    }

    requestUpdate(type: string) {
        this.send({ type: 'request_update', update_type: type });
    }
}

interface UseWebSocketProps {
    tenantId: string;
    userRole: string;
    userId: string;
}

export function useWebSocket(props?: Partial<UseWebSocketProps>) {
    const { data: session } = useSession()
    const tenantId = props?.tenantId || (session as any)?.tenant || 'default'
    const userId = props?.userId || session?.user?.email || 'anonymous'
    const userRole = props?.userRole || (session as any)?.role || 'guest'

    const [isConnected, setIsConnected] = useState(false);
    const clientRef = useRef<WebSocketClient | null>(null);

    useEffect(() => {
        const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL || 'wss://api.bizoholic.net/ws'}/${tenantId}/${userId}`;
        const client = new WebSocketClient(wsUrl);
        clientRef.current = client;

        client.connect();

        const unsubscribe = client.onConnection((connected) => {
            setIsConnected(connected);
        });

        return () => {
            unsubscribe();
            client.disconnect();
        };
    }, [tenantId, userId]);

    const connectAgents = useCallback(() => {
        if (clientRef.current) {
            clientRef.current.send({ type: 'agent_monitor_connect' });
        }
    }, []);

    const connectDashboard = useCallback(() => {
        if (clientRef.current) {
            clientRef.current.send({ type: 'dashboard_connect' });
        }
    }, []);

    const subscribe = useCallback((type: string, callback: (data: any) => void) => {
        if (clientRef.current) {
            return clientRef.current.onMessage(type, callback);
        }
        return () => { };
    }, []);

    const getConnectionState = useCallback(() => isConnected, [isConnected]);

    return {
        client: clientRef.current,
        isConnected,
        connectAgents,
        connectDashboard,
        subscribe,
        getConnectionState,
        reconnect: () => clientRef.current?.connect()
    };
}
