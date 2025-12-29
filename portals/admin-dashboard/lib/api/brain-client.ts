import { brainApi } from '../brain-api';

export interface ApiResponse<T> {
    data?: T;
    error?: string;
    status?: number;
}

export const brainClient = {
    get: async <T>(endpoint: string): Promise<ApiResponse<T>> => {
        try {
            const data = await (brainApi as any).apiFetch?.(endpoint) || await fetch(`/api/brain${endpoint}`).then(r => r.json());
            return { data };
        } catch (error: any) {
            return { error: error.message };
        }
    },
    post: async <T>(endpoint: string, body: any): Promise<ApiResponse<T>> => {
        try {
            const data = await fetch(`/api/brain${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            }).then(r => r.json());
            return { data };
        } catch (error: any) {
            return { error: error.message };
        }
    }
};

// For compatibility with the connectors.ts logic
export const brainApiAdapter = brainClient;
