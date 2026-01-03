import { brainApi, ApiResponse } from './brain-client';

export interface ConnectorConfig {
    id: string;
    name: string;
    type: 'crm' | 'cms' | 'ecommerce' | 'marketing' | 'analytics' | 'billing' | 'infrastructure';
    description: string;
    icon: string;
    version: string;
    status: 'connected' | 'disconnected' | 'error' | 'syncing' | 'degraded';
    lastSync?: string;
    auth_schema: {
        [key: string]: {
            type: 'string' | 'password' | 'number' | 'boolean';
            label: string;
            placeholder?: string;
            help?: string;
            required?: boolean;
        };
    };
}

export interface ConnectorCredentials {
    [key: string]: string | number | boolean;
}

export class ConnectorsApi {
    /**
     * Get all available connectors with their status for the current tenant
     */
    async getConnectors(): Promise<ApiResponse<ConnectorConfig[]>> {
        return brainApi.get<ConnectorConfig[]>('/api/brain/connectors');
    }

    /**
     * Get details for a specific connector
     */
    async getConnector(connectorId: string): Promise<ApiResponse<ConnectorConfig>> {
        return brainApi.get<ConnectorConfig>(`/api/brain/connectors/${connectorId}`);
    }

    /**
     * Connect a service with credentials
     */
    async connectService(connectorId: string, credentials: ConnectorCredentials): Promise<ApiResponse<{ status: string; message: string }>> {
        return brainApi.post<{ status: string; message: string }>(`/api/brain/connectors/${connectorId}/connect`, credentials);
    }

    /**
     * Disconnect a service
     */
    async disconnectService(connectorId: string): Promise<ApiResponse<{ status: string; message: string }>> {
        return brainApi.post<{ status: string; message: string }>(`/api/brain/connectors/${connectorId}/disconnect`, {});
    }

    /**
     * Test connection validation
     */
    async validateConnection(connectorId: string): Promise<ApiResponse<{ valid: boolean; message: string }>> {
        return brainApi.post<{ valid: boolean; message: string }>(`/api/brain/connectors/${connectorId}/validate`, {});
    }

    /**
     * Trigger a manual sync for a specific resource
     */
    async syncResource<T = any>(connectorId: string, resource: string): Promise<ApiResponse<T>> {
        return brainApi.get<T>(`/api/brain/connectors/${connectorId}/sync/${resource}`);
    }

    /**
     * Execute a specific action on a connector
     */
    async performAction<T = any>(connectorId: string, action: string, payload: any = {}): Promise<ApiResponse<T>> {
        return brainApi.post<T>(`/api/brain/connectors/${connectorId}/action/${action}`, payload);
    }
}

export const connectorsApi = new ConnectorsApi();
