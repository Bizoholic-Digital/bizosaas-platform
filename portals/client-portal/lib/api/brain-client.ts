import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Base API response wrapper
export interface ApiResponse<T = any> {
    data?: T;
    error?: string;
    status: number;
}

class BrainApiClient {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: '', // Relative URL to use Next.js API routes
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 30000,
        });

        this.client.interceptors.request.use(async (config) => {
            if (typeof window !== 'undefined') {
                try {
                    // NextAuth tokens are usually handled via cookies
                } catch (e) {
                    console.warn('[BrainSDK] Failed to attach auth token', e);
                }
            }
            return config;
        });
    }

    private async request<T>(method: string, url: string, data?: any): Promise<ApiResponse<T>> {
        try {
            const response: AxiosResponse<T> = await this.client.request({
                method,
                url,
                data,
            });
            return {
                data: response.data,
                status: response.status,
            };
        } catch (error: any) {
            console.error(`API Error ${method} ${url}:`, error);
            return {
                error: error.response?.data?.detail || error.message || 'Unknown error',
                status: error.response?.status || 500,
                data: error.response?.data
            };
        }
    }

    async get<T>(url: string): Promise<ApiResponse<T>> {
        return this.request<T>('GET', url);
    }

    async post<T>(url: string, data?: any): Promise<ApiResponse<T>> {
        return this.request<T>('POST', url, data);
    }

    async put<T>(url: string, data?: any): Promise<ApiResponse<T>> {
        return this.request<T>('PUT', url, data);
    }

    async delete<T>(url: string): Promise<ApiResponse<T>> {
        return this.request<T>('DELETE', url);
    }

    async patch<T>(url: string, data?: any): Promise<ApiResponse<T>> {
        return this.request<T>('PATCH', url, data);
    }
}

export const brainApi = new BrainApiClient();
