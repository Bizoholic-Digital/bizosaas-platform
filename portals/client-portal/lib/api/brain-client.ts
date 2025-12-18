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

        // Add request interceptor to attach bearer token
        this.client.interceptors.request.use(async (config) => {
            // Only running on client-side
            if (typeof window !== 'undefined') {
                try {
                    // Dynamically import to avoid server-side issues
                    const { getSession } = await import('next-auth/react');
                    const session: any = await getSession();
                    console.log("[BrainSDK] Interceptor Session Check:", {
                        hasSession: !!session,
                        hasToken: !!session?.access_token,
                        tokenPreview: session?.access_token ? session.access_token.substring(0, 10) + '...' : 'N/A'
                    });

                    if (session?.access_token) {
                        config.headers.Authorization = `Bearer ${session.access_token}`;
                        console.log("[BrainSDK] Attached Authorization Header");
                    } else {
                        console.warn("[BrainSDK] No access token found in session");
                    }
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
}

export const brainApi = new BrainApiClient();
