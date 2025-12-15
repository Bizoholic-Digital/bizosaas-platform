export const API_CONFIG = {
    // Base URLs - using environment variables with fallbacks
    AUTH_API_URL: process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8007',
    BRAIN_API_URL: process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8001',
    ANALYTICS_API_URL: process.env.NEXT_PUBLIC_SUPERSET_URL || 'http://localhost:8088',

    // API Endpoints
    ENDPOINTS: {
        // Auth Service
        LOGIN: '/api/v1/auth/login',
        LOGOUT: '/api/v1/auth/logout',
        REFRESH_TOKEN: '/api/v1/auth/refresh',
        VERIFY_SESSION: '/api/v1/users/me',
    }
}

export const AUTH_STORAGE = {
    TOKEN_KEY: 'bizosaas_access_token',
    REFRESH_KEY: 'bizosaas_refresh_token',
    USER_KEY: 'bizosaas_user'
}

export const getApiHeaders = (platform: string) => ({
    'Content-Type': 'application/json',
    'X-Platform': platform,
    'X-Tenant': 'bizosaas' // Default tenant
})
