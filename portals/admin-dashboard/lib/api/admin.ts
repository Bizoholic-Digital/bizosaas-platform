import { brainClient as brainApi, ApiResponse } from './brain-client';

export interface AuditLog {
    id: string;
    user_id: string;
    action: string;
    details: any;
    created_at: string;
    ip_address?: string;
    user?: {
        email: string;
        first_name: string;
        last_name: string;
    };
}

export class AdminApi {
    async getStats(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/stats');
    }

    async getUsers(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/users');
    }

    async getTenants(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/tenants');
    }

    async promoteUser(userId: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/admin/users/${userId}/promote`, {});
    }

    async demoteUser(userId: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/admin/users/${userId}/demote`, {});
    }

    async getAuditLogs(limit: number = 50): Promise<ApiResponse<AuditLog[]>> {
        return brainApi.get<AuditLog[]>(`/admin/audit-logs?limit=${limit}`);
    }

    async getHealth(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/health');
    }

    async getAnalytics(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/analytics');
    }
}

export const adminApi = new AdminApi();
