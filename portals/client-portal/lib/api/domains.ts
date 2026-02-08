import { brainApi, ApiResponse } from './brain-client';

export interface DomainResult {
    domain: string;
    available: boolean;
    price: number;
    currency: string;
    registrar: string;
    premium: boolean;
}

export interface DomainInventoryItem {
    id: string;
    tenant_id: string;
    domain_name: string;
    registrar: string;
    status: string;
    expiry_date: string | null;
    auto_renew: boolean;
    dns_configured: boolean;
    target_service: string | null;
    target_slug: string | null;
}

export class DomainApi {
    async searchDomains(query: string, tlds: string[] = ["com", "net", "org", "io", "ai"]): Promise<ApiResponse<DomainResult[]>> {
        const params = new URLSearchParams();
        params.append("query", query);
        tlds.forEach(tld => params.append("tlds", tld));
        return brainApi.get<DomainResult[]>(`/api/brain/domains/search?${params.toString()}`);
    }

    async purchaseDomain(domain: string, price: number): Promise<ApiResponse<any>> {
        return brainApi.post<any>('/api/brain/domains/purchase', { domain, price });
    }

    async getMyDomains(): Promise<ApiResponse<DomainInventoryItem[]>> {
        return brainApi.get<DomainInventoryItem[]>('/api/brain/domains/inventory');
    }

    async updateDomainConfig(domainId: string, updates: Partial<DomainInventoryItem>): Promise<ApiResponse<any>> {
        return brainApi.patch<any>(`/api/brain/domains/${domainId}/config`, updates);
    }

    async getDomainDns(domainId: string): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>(`/api/brain/domains/${domainId}/dns`);
    }

    async addDnsRecord(domainId: string, record: any): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/api/brain/domains/${domainId}/dns`, record);
    }
}

export const domainApi = new DomainApi();
