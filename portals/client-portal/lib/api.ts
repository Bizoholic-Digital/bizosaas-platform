const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';
const AUTH_API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL || API_BASE_URL;
const USE_MOCK_API = process.env.NEXT_PUBLIC_USE_MOCK_API === 'true';

export async function apiRequest(endpoint: string, options?: RequestInit) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  return response.json();
}

export const api = {
  get: (endpoint: string) => apiRequest(endpoint),
  post: (endpoint: string, data: any) => apiRequest(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  put: (endpoint: string, data: any) => apiRequest(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  delete: (endpoint: string) => apiRequest(endpoint, { method: 'DELETE' }),
};

// Authentication Service
interface LoginCredentials {
  email: string;
  password: string;
}

interface LoginResponse {
  success: boolean;
  data?: {
    token: string;
    user?: any;
  };
  error?: string;
}

const apiService = {
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    // Always use the real FastAPI authentication through Brain API Gateway
    try {
      console.log('[API] Attempting login to:', `${AUTH_API_URL}/api/auth/login`);
      console.log('[API] Credentials:', { email: credentials.email, password: '***' });

      const response = await fetch(`${AUTH_API_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: credentials.email,
          password: credentials.password
        }),
      });

      console.log('[API] Response status:', response.status);
      const data = await response.json();
      console.log('[API] Response data:', data);

      // FastAPI returns: { success: true, token: "...", user: {...} }
      if (data.success && data.token) {
        return {
          success: true,
          data: {
            token: data.token,
            user: data.user
          }
        };
      } else {
        return {
          success: false,
          error: data.error || 'Invalid email or password'
        };
      }
    } catch (error: any) {
      console.error('[API] Login error:', error);
      return {
        success: false,
        error: error.message || 'Network error. Please check your connection.'
      };
    }
  }
};

export default apiService;
