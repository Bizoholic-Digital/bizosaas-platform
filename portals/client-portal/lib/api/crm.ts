import { brainApi, ApiResponse } from './brain-client';

export interface CRMContact {
    id: string;
    first_name?: string;
    last_name?: string;
    email: string;
    phone?: string;
    company?: string;
    status?: string;
    tags?: string[];
    source?: string;
    created_at?: string;
}

export class CrmApi {
    async getContacts(params?: { limit?: number; search?: string }): Promise<ApiResponse<CRMContact[]>> {
        const queryParams = new URLSearchParams(params as any).toString();
        return brainApi.get<CRMContact[]>(`/api/brain/crm/contacts${queryParams ? `?${queryParams}` : ''}`);
    }

    async getContact(id: string): Promise<ApiResponse<CRMContact>> {
        return brainApi.get<CRMContact>(`/api/brain/crm/contacts/${id}`);
    }

    async createContact(contact: Partial<CRMContact>): Promise<ApiResponse<CRMContact>> {
        return brainApi.post<CRMContact>('/api/brain/crm/contacts', contact);
    }

    async updateContact(id: string, updates: Partial<CRMContact>): Promise<ApiResponse<CRMContact>> {
        return brainApi.put<CRMContact>(`/api/brain/crm/contacts/${id}`, updates);
    }

    async deleteContact(id: string): Promise<ApiResponse<boolean>> {
        return brainApi.delete<boolean>(`/api/brain/crm/contacts/${id}`);
    }

    async checkConnection(): Promise<ApiResponse<{ connected: boolean; platform?: string; version?: string }>> {
        return brainApi.get<{ connected: boolean; platform?: string; version?: string }>('/api/brain/crm/status');
    }

    async getStats(): Promise<ApiResponse<{ contacts: number; leads: number; campaigns: number; lastSync?: string }>> {
        return brainApi.get<{ contacts: number; leads: number; campaigns: number; lastSync?: string }>('/api/brain/crm/stats');
    }
}

export const crmApi = new CrmApi();
