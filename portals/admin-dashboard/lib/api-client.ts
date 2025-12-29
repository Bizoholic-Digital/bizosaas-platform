import axios from 'axios';

const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
    async (config) => {
        // Get session on client side
        if (typeof window !== 'undefined') {
            try {
                // @ts-ignore - Clerk global is available
                const token = await window.Clerk?.session?.getToken();

                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
            } catch (error) {
                console.error('Failed to get token:', error);
            }
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Redirect to login on unauthorized
            if (typeof window !== 'undefined') {
                window.location.href = '/login';
            }
        }

        if (error.response?.status === 403) {
            // Redirect to unauthorized page
            if (typeof window !== 'undefined') {
                window.location.href = '/unauthorized';
            }
        }

        return Promise.reject(error);
    }
);

export default apiClient;
