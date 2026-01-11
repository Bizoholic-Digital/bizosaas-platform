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

    async getAuditLogs(userId?: string, limit: number = 50): Promise<ApiResponse<AuditLog[]>> {
        const params = userId ? `?user_id=${userId}&limit=${limit}` : `?limit=${limit}`;
        return brainApi.get<AuditLog[]>(`/admin/audit-logs${params}`);
    }

    async getHealth(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/health');
    }

    async getAnalytics(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/analytics');
    }

    async createUser(userData: any): Promise<ApiResponse<any>> {
        return brainApi.post<any>('/admin/users', userData);
    }

    async updateUser(userId: string, userData: any): Promise<ApiResponse<any>> {
        return brainApi.put<any>(`/admin/users/${userId}`, userData);
    }

    async deleteUser(userId: string): Promise<ApiResponse<any>> {
        return brainApi.delete<any>(`/admin/users/${userId}`);
    }

    async getSystemStatus(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/system-status');
    }

    async updateUserPermissions(userId: string, permissions: Record<string, boolean>): Promise<ApiResponse<any>> {
        return brainApi.put<any>(`/admin/users/${userId}/permissions`, permissions);
    }

    async impersonateUser(userId: string): Promise<ApiResponse<{ token: string }>> {
        return brainApi.post<{ token: string }>(`/admin/users/${userId}/impersonate`, {});
    }
}

export const adminApi = new AdminApi();
