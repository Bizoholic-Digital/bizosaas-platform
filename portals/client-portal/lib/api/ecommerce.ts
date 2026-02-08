import { brainApi, ApiResponse } from './brain-client';

export interface Product {
    id: string;
    name: string;
    description: string;
    price: string;
    sku: string;
    stock_quantity: number;
    status: string;
    images: string[];
}

export interface Order {
    id: string;
    number: string;
    status: string;
    total: string;
    currency: string;
    customer_id: number;
    created_at: string;
    line_items: any[];
}

export class EcommerceApi {
    async getProducts(params?: { limit?: number; page?: number }): Promise<ApiResponse<Product[]>> {
        const queryParams = new URLSearchParams(params as any).toString();
        return brainApi.get<Product[]>(`/api/brain/ecommerce/products${queryParams ? `?${queryParams}` : ''}`);
    }

    async getOrders(params?: { limit?: number; status?: string }): Promise<ApiResponse<Order[]>> {
        const queryParams = new URLSearchParams(params as any).toString();
        return brainApi.get<Order[]>(`/api/brain/ecommerce/orders${queryParams ? `?${queryParams}` : ''}`);
    }

    async updateInventory(sku: string, quantity: number): Promise<ApiResponse<any>> {
        return brainApi.post('/api/brain/ecommerce/inventory', { sku, quantity });
    }

    async checkConnection(): Promise<ApiResponse<{ connected: boolean; platform?: string; version?: string }>> {
        return brainApi.get<{ connected: boolean; platform?: string; version?: string }>('/api/brain/ecommerce/status');
    }

    async getStats(): Promise<ApiResponse<{ products: number; orders: number; revenue: number; lastSync?: string }>> {
        return brainApi.get<{ products: number; orders: number; revenue: number; lastSync?: string }>('/api/brain/ecommerce/stats');
    }
}

export const ecommerceApi = new EcommerceApi();
