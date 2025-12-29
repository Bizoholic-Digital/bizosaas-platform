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
        return brainApi.get<ConnectorConfig[]>('/api/brain/connectors/');
    }

    async getConnector(connectorId: string): Promise<ApiResponse<ConnectorConfig>> {
        return brainApi.get<ConnectorConfig>(`/api/brain/connectors/${connectorId}/`);
    }

    async connectService(connectorId: string, credentials: ConnectorCredentials): Promise<ApiResponse<{ status: string; message: string }>> {
        return brainApi.post<{ status: string; message: string }>(`/api/brain/connectors/${connectorId}/connect/`, credentials);
    }

    async disconnectService(connectorId: string): Promise<ApiResponse<{ status: string; message: string }>> {
        return brainApi.post<{ status: string; message: string }>(`/api/brain/connectors/${connectorId}/disconnect/`, {});
    }

    async validateConnection(connectorId: string): Promise<ApiResponse<{ valid: boolean; message: string }>> {
        return brainApi.post<{ valid: boolean; message: string }>(`/api/brain/connectors/${connectorId}/validate/`, {});
    }

    async syncConnector(connectorId: string, resource?: string): Promise<ApiResponse<{ jobId: string; status: string }>> {
        return brainApi.post<{ jobId: string; status: string }>(`/api/brain/connectors/${connectorId}/sync/`, { resource });
    }
}

export const connectorsApi = new ConnectorsApi();
