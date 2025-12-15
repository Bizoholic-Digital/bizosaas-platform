/**
 * CRM API Client
 * Routes all CRM operations through Brain Gateway → Django CRM
 */

import { brainApi, ApiResponse } from './brain-client';

export interface Contact {
    id?: string;
    first_name: string;
    last_name: string;
    email: string;
    phone?: string;
    company?: string;
    title?: string;
    status?: string;
    tags?: string[];
    created_at?: string;
    updated_at?: string;
}

export interface Company {
    id?: string;
    name: string;
    website?: string;
    industry?: string;
    size?: string;
    created_at?: string;
}

export interface Deal {
    id?: string;
    title: string;
    value: number;
    stage: string;
    contact_id?: string;
    company_id?: string;
    probability?: number;
    expected_close_date?: string;
    created_at?: string;
}

export interface Task {
    id?: string;
    title: string;
    description?: string;
    due_date?: string;
    status: 'pending' | 'in_progress' | 'completed';
    assigned_to?: string;
    contact_id?: string;
    deal_id?: string;
}

export class CrmApi {
    // Contacts
    async getContacts(params?: { page?: number; limit?: number; search?: string }): Promise<ApiResponse<Contact[]>> {
        const queryParams = new URLSearchParams(params as any).toString();
        return brainApi.get(`/api/brain/django-crm/contacts${queryParams ? `?${queryParams}` : ''}`);
    }

    async getContact(id: string): Promise<ApiResponse<Contact>> {
        return brainApi.get(`/api/brain/django-crm/contacts/${id}`);
    }

    async createContact(contact: Contact): Promise<ApiResponse<Contact>> {
        return brainApi.post('/api/brain/django-crm/contacts', contact);
    }

    async updateContact(id: string, contact: Partial<Contact>): Promise<ApiResponse<Contact>> {
        return brainApi.put(`/api/brain/django-crm/contacts/${id}`, contact);
    }

    async deleteContact(id: string): Promise<ApiResponse<void>> {
        return brainApi.delete(`/api/brain/django-crm/contacts/${id}`);
    }

    // Companies
    async getCompanies(params?: { page?: number; limit?: number }): Promise<ApiResponse<Company[]>> {
        const queryParams = new URLSearchParams(params as any).toString();
        return brainApi.get(`/api/brain/django-crm/companies${queryParams ? `?${queryParams}` : ''}`);
    }

    async createCompany(company: Company): Promise<ApiResponse<Company>> {
        return brainApi.post('/api/brain/django-crm/companies', company);
    }

    // Deals
    async getDeals(params?: { page?: number; limit?: number }): Promise<ApiResponse<Deal[]>> {
        const queryParams = new URLSearchParams(params as any).toString();
        return brainApi.get(`/api/brain/django-crm/deals${queryParams ? `?${queryParams}` : ''}`);
    }

    async createDeal(deal: Deal): Promise<ApiResponse<Deal>> {
        return brainApi.post('/api/brain/django-crm/deals', deal);
    }

    async updateDeal(id: string, deal: Partial<Deal>): Promise<ApiResponse<Deal>> {
        return brainApi.put(`/api/brain/django-crm/deals/${id}`, deal);
    }

    // Tasks
    async getTasks(params?: { page?: number; limit?: number }): Promise<ApiResponse<Task[]>> {
        const queryParams = new URLSearchParams(params as any).toString();
        return brainApi.get(`/api/brain/django-crm/tasks${queryParams ? `?${queryParams}` : ''}`);
    }

    async createTask(task: Task): Promise<ApiResponse<Task>> {
        return brainApi.post('/api/brain/django-crm/tasks', task);
    }

    async updateTask(id: string, task: Partial<Task>): Promise<ApiResponse<Task>> {
        return brainApi.put(`/api/brain/django-crm/tasks/${id}`, task);
    }
}

// Export singleton instance
export const crmApi = new CrmApi();
