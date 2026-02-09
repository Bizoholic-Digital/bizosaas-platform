export const API_CONFIG = {
    // Base URLs - using environment variables with fallbacks for internal Docker network
    AUTH_API_URL: process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://bizosaas-auth:8007',
    BRAIN_API_URL: process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000',
    CRM_API_URL: process.env.NEXT_PUBLIC_CRM_API_URL || 'http://crm:8003',
    CMS_API_URL: process.env.NEXT_PUBLIC_CMS_API_URL || 'http://cms:8002',
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
