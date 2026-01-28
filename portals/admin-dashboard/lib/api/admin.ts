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

    async getUsers(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/users');
    }

    async getTenants(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/tenants');
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

    async getWorkflows(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/workflows/');
    }

    async toggleWorkflow(workflowId: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/workflows/${workflowId}/toggle`, {});
    }

    // Directory Management
    async getDirectoryStats(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/directory/stats');
    }

    async getDirectoryListings(query?: string, page: number = 1): Promise<ApiResponse<any>> {
        const q = query ? `&query=${encodeURIComponent(query)}` : '';
        return brainApi.get<any>(`/admin/directory/listings?page=${page}${q}`);
    }

    async getDirectoryClaims(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/directory/claims');
    }

    // Revenue & Partnerships
    async getRevenueStats(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/revenue/stats');
    }

    async getRevenueTransactions(limit: number = 50): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>(`/admin/revenue/transactions?limit=${limit}`);
    }

    async getGlobalDomains(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/api/domains/inventory');
    }

    async getDomainAdminStats(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/api/domains/admin/stats');
    }

    async approveClaim(claimId: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/admin/directory/claims/${claimId}/approve`, {});
    }

    async rejectClaim(claimId: string, reason?: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/admin/directory/claims/${claimId}/reject`, { reason });
    }

    async deleteListing(listingId: string): Promise<ApiResponse<any>> {
        return brainApi.delete<any>(`/admin/directory/listings/${listingId}`);
    }

    async optimizeListing(listingId: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/admin/directory/listings/${listingId}/optimize`, {});
    }

    // Trigger Management
    async getWorkflowTriggers(workflowId: string): Promise<ApiResponse<{ workflow_id: string, triggers: any[] }>> {
        return brainApi.get<{ workflow_id: string, triggers: any[] }>(`/api/triggers/config/${workflowId}`);
    }

    async updateWorkflowTriggers(workflowId: string, triggers: any[]): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/api/triggers/config/${workflowId}`, triggers);
    }

    async getTenantDetails(tenantId: string): Promise<ApiResponse<any>> {
        return brainApi.get<any>(`/admin/tenants/${tenantId}`);
    }

    async updateTenantConfig(tenantId: string, updates: any): Promise<ApiResponse<any>> {
        return brainApi.patch<any>(`/admin/tenants/${tenantId}/config`, updates);
    }

    async bulkTenantAction(tenantIds: string[], action: 'suspend' | 'activate' | 'maintenance'): Promise<ApiResponse<any>> {
        return brainApi.post<any>('/admin/tenants/bulk', { tenant_ids: tenantIds, action });
    }

    async getTenantAnalytics(tenantId: string): Promise<ApiResponse<any>> {
        return brainApi.get<any>(`/admin/tenants/${tenantId}/analytics`);
    }

    async getOnboardingStats(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/tenants/stats/onboarding');
    }

    async getUserSessions(userId: string): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>(`/admin/users/${userId}/sessions`);
    }

    async getMCPStats(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/mcp/stats');
    }

    async getMCPRegistry(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/mcp/registry');
    }

    async getCMSSites(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/cms/sites');
    }

    async getCMSPluginStats(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/cms/plugins/status');
    }

    async deployCMSPlugin(version: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>('/admin/cms/plugins/deploy', { version });
    }

    async getDunningQueue(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/billing/dunning');
    }

    async retryPayment(invoiceId: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/admin/billing/dunning/${invoiceId}/retry`, {});
    }

    async revokeSession(sessionId: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/admin/sessions/${sessionId}/revoke`, {});
    }

    async auditClaims(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/directory/claims/audit');
    }

    // Security Dashboard
    async getSecurityPosture(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/security/posture');
    }

    async getVulnerabilities(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/security/vulnerabilities');
    }

    async getComplianceChecklist(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/security/compliance-checklist');
    }

    async getEncryptionKeys(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/security/encryption/keys');
    }

    async addIpWhitelist(ip: string, reason: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>('/admin/security/ip-whitelist', { ip, reason });
    }

    // Support Ticket Hub
    async getGlobalTickets(status?: string, priority?: string): Promise<ApiResponse<any[]>> {
        const params = new URLSearchParams();
        if (status) params.append('status', status);
        if (priority) params.append('priority', priority);
        return brainApi.get<any[]>(`/admin/support/tickets?${params.toString()}`);
    }

    async updateTicket(ticketId: string, updates: any): Promise<ApiResponse<any>> {
        return brainApi.patch<any>(`/admin/support/tickets/${ticketId}`, updates);
    }

    async getSystemErrors(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/support/errors');
    }

    async executeDbQuery(query: string): Promise<ApiResponse<any>> {
        return brainApi.post<any>('/admin/support/db/query', { query });
    }

    async clearCache(pattern: string = "*"): Promise<ApiResponse<any>> {
        return brainApi.post<any>('/admin/support/cache/clear', { pattern });
    }

    async runDiagnostics(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/support/diagnostics');
    }

    // Reporting & Exports
    async generateCustomReport(metrics: string[], filters: any): Promise<ApiResponse<any>> {
        return brainApi.post<any>('/admin/reporting/builder', { metrics, filters });
    }

    async getScheduledReports(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/reporting/scheduled');
    }

    async exportTenants(format: 'json' | 'csv' = 'json'): Promise<ApiResponse<any>> {
        return brainApi.get<any>(`/admin/reporting/export/tenants?format=${format}`);
    }

    async getComplianceReport(type: string): Promise<ApiResponse<any>> {
        return brainApi.get<any>(`/admin/reporting/compliance/${type}`);
    }

    async getUsageReports(tenantId?: string): Promise<ApiResponse<any>> {
        const query = tenantId ? `?tenant_id=${tenantId}` : '';
        return brainApi.get<any>(`/admin/reporting/usage-breakdown${query}`);
    }

    // System Configuration
    async getSystemEnv(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/system/env');
    }

    async getFeatureFlags(): Promise<ApiResponse<any>> {
        return brainApi.get<any>('/admin/system/feature-flags');
    }

    async configureGlobalWebhook(url: string, events: string[]): Promise<ApiResponse<any>> {
        return brainApi.post<any>('/admin/system/webhooks', { url, events });
    }

    async getEmailTemplates(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/admin/system/email-templates');
    }

    async updateBranding(logoUrl: string, primaryColor: string): Promise<ApiResponse<any>> {
        return brainApi.put<any>('/admin/system/branding', { logo_url: logoUrl, primary_color: primaryColor });
    }

    // Domain & DNS Management
    async getDomainProviders(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/api/domains/providers/config');
    }

    async updateDomainConfig(domainId: string, updates: any): Promise<ApiResponse<any>> {
        return brainApi.patch<any>(`/api/domains/${domainId}/config`, updates);
    }

    async getDomainDns(domain_id: string): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>(`/api/domains/${domain_id}/dns`);
    }

    async addDomainDns(domain_id: string, record: any): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/api/domains/${domain_id}/dns`, record);
    }

    async bulkRenewDomains(domainIds: string[]): Promise<ApiResponse<any>> {
        return brainApi.post<any>('/api/domains/bulk/renew', { domain_ids: domainIds });
    }

    async getAgentProposals(): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>('/api/onboarding/proposals');
    }
}

export const adminApi = new AdminApi();
