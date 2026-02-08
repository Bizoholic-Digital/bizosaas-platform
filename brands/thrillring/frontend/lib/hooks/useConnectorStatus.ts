import { useState, useEffect } from 'react';
import { brainApi } from '../brain-api';

export interface ConnectorStatus {
    id: string;
    name: string;
    status: 'CONNECTED' | 'DISCONNECTED' | 'ERROR' | 'connected' | 'disconnected' | 'error';
    type: string;
    icon?: string;
}

export function useConnectorStatus(connectorId: string, type?: string) {
    const [connector, setConnector] = useState<ConnectorStatus | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const checkStatus = async () => {
        try {
            setIsLoading(true);
            setError(null);

            // Get all connectors with status
            const response = await brainApi.connectors?.getConnectors() || [];

            // Find by ID first, then by type if provided and status is connected
            let found = response.find((c: any) => c.id === connectorId);

            if (!found && type) {
                found = response.find((c: any) =>
                    c.type === type &&
                    (c.status?.toUpperCase() === 'CONNECTED' || c.status === 'connected')
                );
            }

            if (found) {
                setConnector({
                    id: found.id,
                    name: found.name,
                    status: (found.status || 'DISCONNECTED') as ConnectorStatus['status'],
                    type: found.type,
                    icon: found.icon
                });
            } else {
                setConnector(null);
            }
        } catch (err: any) {
            console.error(`Failed to check connector status for ${connectorId}${type ? ' (' + type + ')' : ''}:`, err);
            setError(err.message || 'Failed to check connection status');
            setConnector(null);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        checkStatus();
    }, [connectorId, type]);

    const isConnected = connector?.status?.toUpperCase() === 'CONNECTED' ||
        connector?.status === 'connected';

    return {
        connector,
        isConnected,
        isLoading,
        error,
        refresh: checkStatus
    };
}
