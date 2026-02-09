export interface Product {
    id: string;
    title: string;
    sku: string;
    asin?: string;
    pricing: {
        source_price: number;
        current_selling_price: number;
        profit_margin: number;
        currency: string;
    };
    ai_metrics: {
        classification: 'HERO' | 'GOOD' | 'MODERATE' | 'POOR';
        dropship_score: number;
        market_demand?: string;
        competition_level?: string;
        trend?: 'up' | 'down' | 'stable';
    };
    performance?: {
        views: number;
        orders: number;
        conversion_rate: number;
        total_revenue: number;
    };
    inventory?: {
        available: number;
        reorder_level?: number;
        status: 'in_stock' | 'low_stock' | 'out_of_stock';
    };
    category?: string;
    status: 'active' | 'draft' | 'archived';
    images?: string[];
    description?: string;
}

export interface ProductListResponse {
    success: boolean;
    data?: {
        items: Product[];
        total: number;
        page: number;
        pages: number;
    };
    error?: string;
}

class CoreLDoveAPIClient {
    private apiBaseUrl: string;
    private tenantId: string;

    constructor() {
        this.apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://api.bizoholic.net';
        this.tenantId = 'bizoholic';
    }

    async getProducts(filters: {
        search?: string;
        category?: string;
        classification?: string;
        status?: string;
        page?: number;
        per_page?: number;
    }): Promise<ProductListResponse> {
        try {
            const queryParams = new URLSearchParams();
            if (filters.search) queryParams.append('search', filters.search);
            if (filters.category) queryParams.append('category', filters.category);
            if (filters.classification) queryParams.append('classification', filters.classification);
            if (filters.status) queryParams.append('status', filters.status);
            if (filters.page) queryParams.append('page', filters.page.toString());
            if (filters.per_page) queryParams.append('per_page', filters.per_page.toString());

            const response = await fetch(`${this.apiBaseUrl}/api/products?${queryParams.toString()}`, {
                headers: {
                    'x-tenant-id': this.tenantId
                }
            });

            if (!response.ok) {
                return { success: false, error: `API error: ${response.statusText}` };
            }

            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('CoreLDove API Error:', error);
            return { success: false, error: 'Connection failed' };
        }
    }

    async getProduct(id: string): Promise<{ success: boolean; data?: Product; error?: string }> {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/products/${id}`, {
                headers: {
                    'x-tenant-id': this.tenantId
                }
            });

            if (!response.ok) {
                return { success: false, error: `API error: ${response.statusText}` };
            }

            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('CoreLDove API Error:', error);
            return { success: false, error: 'Connection failed' };
        }
    }
}

export const coreLDoveAPI = new CoreLDoveAPIClient();
