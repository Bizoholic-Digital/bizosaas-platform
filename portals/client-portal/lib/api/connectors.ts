import { brainApi, ApiResponse } from './brain-client';

export interface ConnectorConfig {
    id: string;
    name: string;
    type: 'crm' | 'cms' | 'ecommerce' | 'marketing' | 'analytics' | 'billing';
    description: string;
    icon: string;
    version: string;
    status: 'connected' | 'disconnected' | 'error' | 'syncing';
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
     * Trigger a manual sync
     */
    async syncConnector(connectorId: string, resource?: string): Promise<ApiResponse<{ jobId: string; status: string }>> {
        return brainApi.post<{ jobId: string; status: string }>(`/api/brain/connectors/${connectorId}/sync`, { resource });
    }

    /**
     * Discover plugins for a connected WordPress site
     */
    async discoverPlugins(connectorId: string): Promise<ApiResponse<{ plugins: any[] }>> {
        return brainApi.get<{ plugins: any[] }>(`/api/brain/connectors/${connectorId}/plugins`);
    }

    /**
     * Auto-connect discovered plugins
     */
    async autoConnectPlugins(connectorId: string, pluginSlugs: string[]): Promise<ApiResponse<{ status: string; connected: string[]; errors: any[] }>> {
        return brainApi.post<any>(`/api/brain/connectors/${connectorId}/auto-connect-plugins`, pluginSlugs);
    }

    /**
     * Get marketplace plugins for a platform
     */
    async getMarketplacePlugins(platform: string = 'wordpress'): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>(`/api/brain/connectors/marketplace/plugins?platform=${platform}`);
    }

    /**
     * Track user interest in a plugin
     */
    async trackPluginInterest(pluginSlug: string, action: string, platform: string = 'wordpress'): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/api/brain/connectors/marketplace/track-interest`, { plugin_slug: pluginSlug, action, platform });
    }
}

export const connectorsApi = new ConnectorsApi();
