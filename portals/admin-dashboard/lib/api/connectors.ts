import { brainClient as brainApi, ApiResponse } from './brain-client';

export interface ConnectorConfig {
    id: string;
    name: string;
    type: 'crm' | 'cms' | 'ecommerce' | 'marketing' | 'analytics' | 'billing';
    description: string;
    icon: string;
    version: string;
    status: 'connected' | 'disconnected' | 'error' | 'syncing' | 'CONNECTED' | 'DISCONNECTED' | 'ERROR' | 'SYNCING';
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
    async getConnectors(): Promise<ApiResponse<ConnectorConfig[]>> {
        return brainApi.get<ConnectorConfig[]>('/connectors');
    }

    async getConnector(connectorId: string): Promise<ApiResponse<ConnectorConfig>> {
        return brainApi.get<ConnectorConfig>(`/connectors/${connectorId}`);
    }

    async connectService(connectorId: string, credentials: ConnectorCredentials): Promise<ApiResponse<{ status: string; message: string }>> {
        return brainApi.post<{ status: string; message: string }>(`/connectors/${connectorId}/connect`, credentials);
    }

    async disconnectService(connectorId: string): Promise<ApiResponse<{ status: string; message: string }>> {
        return brainApi.post<{ status: string; message: string }>(`/connectors/${connectorId}/disconnect`, {});
    }

    async validateConnection(connectorId: string): Promise<ApiResponse<{ valid: boolean; message: string }>> {
        return brainApi.post<{ valid: boolean; message: string }>(`/connectors/${connectorId}/validate`, {});
    }

    async syncConnector(connectorId: string, resource?: string): Promise<ApiResponse<{ jobId: string; status: string }>> {
        return brainApi.post<{ jobId: string; status: string }>(`/connectors/${connectorId}/sync`, { resource });
    }

    async getMarketplaceMetrics(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/connectors/marketplace/metrics');
    }

    async getConnectorAnalytics(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/connectors/analytics');
    }
}

export const connectorsApi = new ConnectorsApi();
