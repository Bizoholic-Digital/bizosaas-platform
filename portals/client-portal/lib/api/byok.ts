import { brainApi, ApiResponse } from './brain-client';

export interface BYOKKey {
    service_id: string;
    key_type: string;
    value: string;
    is_valid: boolean;
    last_used?: string;
    created_at?: string;
}

export interface BYOKKeyInput {
    service_id: string;
    key_type: string;
    value: string;
}

export class BYOKApi {
    /**
     * Add a new API key
     */
    async addKey(input: BYOKKeyInput): Promise<ApiResponse<{ status: string; message: string }>> {
        return brainApi.post(`/api/connectors/${input.service_id}/connect/`, {
            [input.key_type]: input.value
        });
    }

    /**
     * Test/validate an API key (existing or new)
     */
    async testKey(serviceId: string, credentials?: Record<string, any>): Promise<ApiResponse<{ valid: boolean }>> {
        if (credentials) {
            return brainApi.post(`/api/connectors/${serviceId}/test/`, credentials);
        }
        return brainApi.post(`/api/connectors/${serviceId}/validate/`, {});
    }

    /**
     * Delete an API key
     */
    async deleteKey(serviceId: string): Promise<ApiResponse<{ status: string }>> {
        return brainApi.post(`/api/connectors/${serviceId}/disconnect/`, {});
    }

    /**
     * Rotate an API key
     */
    async rotateKey(serviceId: string, newValue: string, keyType: string): Promise<ApiResponse<{ status: string }>> {
        // Delete old key and add new one
        await this.deleteKey(serviceId);
        return this.addKey({ service_id: serviceId, key_type: keyType, value: newValue });
    }

    /**
     * Get all configured keys (via connectors list)
     */
    async getConfiguredKeys(): Promise<ApiResponse<any[]>> {
        return brainApi.get('/api/connectors/');
    }
}

export const byokApi = new BYOKApi();
