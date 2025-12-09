import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface ConnectorConfig {
    id: string;
    name: string;
    type: string;
    description: string;
    icon: string;
    version: string;
    auth_schema: Record<string, any>;
}

export interface ConnectorStatus {
    status: 'connected' | 'disconnected' | 'error' | 'pending';
}

export const brainApi = {
    connectors: {
        listTypes: async (): Promise<ConnectorConfig[]> => {
            const response = await api.get('/api/connectors/types');
            return response.data;
        },

        connect: async (connectorId: string, credentials: any) => {
            const response = await api.post(`/api/connectors/${connectorId}/connect`, credentials);
            return response.data;
        },

        getStatus: async (connectorId: string): Promise<ConnectorStatus> => {
            const response = await api.get(`/api/connectors/${connectorId}/status`);
            return response.data;
        },

        sync: async (connectorId: string, resource: string) => {
            const response = await api.get(`/api/connectors/${connectorId}/sync/${resource}`);
            return response.data;
        }
    }
};
