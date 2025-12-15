/**
 * Centralized Brain API Gateway Client
 * All backend requests route through the Brain Gateway following hexagonal architecture
 */

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'https://api.bizoholic.net';

export interface ApiResponse<T = any> {
    data?: T;
    error?: string;
    status: number;
}

export class BrainApiClient {
    private baseUrl: string;

    constructor(baseUrl: string = BRAIN_API_URL) {
        this.baseUrl = baseUrl;
    }

    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<ApiResponse<T>> {
        const url = `${this.baseUrl}${endpoint}`;

        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers,
                },
            });

            const data = await response.json();

            if (!response.ok) {
                return {
                    error: data.error || data.message || 'Request failed',
                    status: response.status,
                };
            }

            return {
                data,
                status: response.status,
            };
        } catch (error) {
            return {
                error: error instanceof Error ? error.message : 'Network error',
                status: 500,
            };
        }
    }

    // Generic CRUD operations
    async get<T>(endpoint: string): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, { method: 'GET' });
    }

    async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, {
            method: 'POST',
            body: JSON.stringify(body),
        });
    }

    async put<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, {
            method: 'PUT',
            body: JSON.stringify(body),
        });
    }

    async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, { method: 'DELETE' });
    }

    // Health check
    async healthCheck() {
        return this.get('/health');
    }
}

// Export singleton instance
export const brainApi = new BrainApiClient();
