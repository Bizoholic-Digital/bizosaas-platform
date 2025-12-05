/**
 * BYOK (Bring Your Own Key) Manager
 * Manages tenant API keys with HashiCorp Vault integration
 */

import type {
    APIKey,
    BYOKConfig,
    KeyValidationResult,
    LLMProvider,
} from './types';

// ============================================================================
// Configuration
// ============================================================================

const VAULT_API_URL = process.env.NEXT_PUBLIC_VAULT_API_URL || 'http://localhost:8200';
const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// ============================================================================
// Service Catalog
// ============================================================================

export const SERVICE_CATALOG = {
    // AI Services
    openai: {
        name: 'OpenAI',
        category: 'ai',
        keyTypes: ['api_key', 'organization'],
        requiredKeys: ['api_key'],
        documentation: 'https://platform.openai.com/docs/api-reference',
    },
    anthropic: {
        name: 'Anthropic Claude',
        category: 'ai',
        keyTypes: ['api_key'],
        requiredKeys: ['api_key'],
        documentation: 'https://docs.anthropic.com/claude/reference',
    },
    openrouter: {
        name: 'OpenRouter',
        category: 'ai',
        keyTypes: ['api_key'],
        requiredKeys: ['api_key'],
        documentation: 'https://openrouter.ai/docs',
    },
    google_ai: {
        name: 'Google AI (Gemini)',
        category: 'ai',
        keyTypes: ['api_key'],
        requiredKeys: ['api_key'],
        documentation: 'https://ai.google.dev/docs',
    },

    // Marketing Platforms
    google_ads: {
        name: 'Google Ads',
        category: 'marketing',
        keyTypes: ['developer_token', 'client_id', 'client_secret', 'refresh_token'],
        requiredKeys: ['developer_token'],
        documentation: 'https://developers.google.com/google-ads/api/docs',
    },
    meta_ads: {
        name: 'Meta Ads (Facebook/Instagram)',
        category: 'marketing',
        keyTypes: ['app_id', 'app_secret', 'access_token'],
        requiredKeys: ['access_token'],
        documentation: 'https://developers.facebook.com/docs/marketing-apis',
    },
    linkedin_ads: {
        name: 'LinkedIn Ads',
        category: 'marketing',
        keyTypes: ['access_token', 'client_id', 'client_secret'],
        requiredKeys: ['access_token'],
        documentation: 'https://docs.microsoft.com/en-us/linkedin/marketing/',
    },
    tiktok_ads: {
        name: 'TikTok Ads',
        category: 'marketing',
        keyTypes: ['access_token', 'app_id', 'secret'],
        requiredKeys: ['access_token'],
        documentation: 'https://ads.tiktok.com/marketing_api/docs',
    },

    // Payment Gateways
    stripe: {
        name: 'Stripe',
        category: 'payment',
        keyTypes: ['publishable_key', 'secret_key', 'webhook_secret'],
        requiredKeys: ['secret_key'],
        documentation: 'https://stripe.com/docs/api',
    },
    paypal: {
        name: 'PayPal',
        category: 'payment',
        keyTypes: ['client_id', 'client_secret'],
        requiredKeys: ['client_id', 'client_secret'],
        documentation: 'https://developer.paypal.com/docs/api',
    },
    razorpay: {
        name: 'Razorpay',
        category: 'payment',
        keyTypes: ['key_id', 'key_secret'],
        requiredKeys: ['key_id', 'key_secret'],
        documentation: 'https://razorpay.com/docs/api',
    },

    // Analytics
    google_analytics: {
        name: 'Google Analytics',
        category: 'analytics',
        keyTypes: ['measurement_id', 'api_secret'],
        requiredKeys: ['measurement_id'],
        documentation: 'https://developers.google.com/analytics',
    },
    mixpanel: {
        name: 'Mixpanel',
        category: 'analytics',
        keyTypes: ['project_token', 'api_secret'],
        requiredKeys: ['project_token'],
        documentation: 'https://developer.mixpanel.com/docs',
    },

    // Email Services
    sendgrid: {
        name: 'SendGrid',
        category: 'email',
        keyTypes: ['api_key'],
        requiredKeys: ['api_key'],
        documentation: 'https://docs.sendgrid.com/api-reference',
    },
    mailchimp: {
        name: 'Mailchimp',
        category: 'email',
        keyTypes: ['api_key', 'server_prefix'],
        requiredKeys: ['api_key'],
        documentation: 'https://mailchimp.com/developer/marketing/api/',
    },

    // SMS Services
    twilio: {
        name: 'Twilio',
        category: 'sms',
        keyTypes: ['account_sid', 'auth_token'],
        requiredKeys: ['account_sid', 'auth_token'],
        documentation: 'https://www.twilio.com/docs/usage/api',
    },

    // Cloud Storage
    aws_s3: {
        name: 'AWS S3',
        category: 'storage',
        keyTypes: ['access_key_id', 'secret_access_key', 'region'],
        requiredKeys: ['access_key_id', 'secret_access_key'],
        documentation: 'https://docs.aws.amazon.com/s3/',
    },
    google_cloud_storage: {
        name: 'Google Cloud Storage',
        category: 'storage',
        keyTypes: ['service_account_json'],
        requiredKeys: ['service_account_json'],
        documentation: 'https://cloud.google.com/storage/docs',
    },

    // CRM Integrations
    salesforce: {
        name: 'Salesforce',
        category: 'crm',
        keyTypes: ['client_id', 'client_secret', 'username', 'password', 'security_token'],
        requiredKeys: ['client_id', 'client_secret'],
        documentation: 'https://developer.salesforce.com/docs/apis',
    },
    hubspot: {
        name: 'HubSpot',
        category: 'crm',
        keyTypes: ['api_key', 'access_token'],
        requiredKeys: ['api_key'],
        documentation: 'https://developers.hubspot.com/docs/api',
    },
} as const;

export type ServiceId = keyof typeof SERVICE_CATALOG;

// ============================================================================
// BYOK Manager Class
// ============================================================================

export class BYOKManager {
    private tenantId: string;
    private cache: Map<string, APIKey> = new Map();

    constructor(tenantId: string) {
        this.tenantId = tenantId;
    }

    /**
     * Get API key for a service (tenant-specific or platform fallback)
     */
    async getAPIKey(
        service: ServiceId,
        keyType: string,
        fallbackToPlatform: boolean = true
    ): Promise<string | null> {
        try {
            // Check cache first
            const cacheKey = `${service}:${keyType}`;
            const cached = this.cache.get(cacheKey);
            if (cached && this.isKeyValid(cached)) {
                return cached.value;
            }

            // Try to get tenant-specific key from Vault via Brain API
            const tenantKey = await this.getTenantKeyFromVault(service, keyType);
            if (tenantKey) {
                this.cache.set(cacheKey, tenantKey);
                return tenantKey.value;
            }

            // Fallback to platform key if allowed
            if (fallbackToPlatform) {
                const platformKey = await this.getPlatformKeyFromVault(service, keyType);
                if (platformKey) {
                    return platformKey.value;
                }
            }

            return null;
        } catch (error) {
            console.error(`Error getting API key for ${service}:`, error);
            return null;
        }
    }

    /**
     * Get tenant-specific key from Vault
     */
    private async getTenantKeyFromVault(
        service: ServiceId,
        keyType: string
    ): Promise<APIKey | null> {
        try {
            const response = await fetch(
                `${BRAIN_API_URL}/api/brain/portal/tenant/${this.tenantId}/api-keys/${service}/${keyType}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                }
            );

            if (!response.ok) {
                return null;
            }

            const data = await response.json();
            return data.key || null;
        } catch (error) {
            console.error('Error fetching tenant key from Vault:', error);
            return null;
        }
    }

    /**
     * Get platform-level key from Vault (fallback)
     */
    private async getPlatformKeyFromVault(
        service: ServiceId,
        keyType: string
    ): Promise<APIKey | null> {
        try {
            const response = await fetch(
                `${BRAIN_API_URL}/api/brain/portal/platform/api-keys/${service}/${keyType}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                }
            );

            if (!response.ok) {
                return null;
            }

            const data = await response.json();
            return data.key || null;
        } catch (error) {
            console.error('Error fetching platform key from Vault:', error);
            return null;
        }
    }

    /**
     * Set API key for tenant
     */
    async setAPIKey(
        service: ServiceId,
        keyType: string,
        value: string
    ): Promise<boolean> {
        try {
            const response = await fetch(
                `${BRAIN_API_URL}/api/brain/portal/tenant/${this.tenantId}/api-keys`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        service,
                        keyType,
                        value,
                    }),
                }
            );

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Failed to set API key');
            }

            // Clear cache for this key
            const cacheKey = `${service}:${keyType}`;
            this.cache.delete(cacheKey);

            return true;
        } catch (error) {
            console.error('Error setting API key:', error);
            return false;
        }
    }

    /**
     * Delete API key for tenant
     */
    async deleteAPIKey(service: ServiceId, keyType: string): Promise<boolean> {
        try {
            const response = await fetch(
                `${BRAIN_API_URL}/api/brain/portal/tenant/${this.tenantId}/api-keys/${service}/${keyType}`,
                {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                }
            );

            if (!response.ok) {
                return false;
            }

            // Clear cache
            const cacheKey = `${service}:${keyType}`;
            this.cache.delete(cacheKey);

            return true;
        } catch (error) {
            console.error('Error deleting API key:', error);
            return false;
        }
    }

    /**
     * List all API keys for tenant
     */
    async listAPIKeys(): Promise<APIKey[]> {
        try {
            const response = await fetch(
                `${BRAIN_API_URL}/api/brain/portal/tenant/${this.tenantId}/api-keys`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                }
            );

            if (!response.ok) {
                return [];
            }

            const data = await response.json();
            return data.keys || [];
        } catch (error) {
            console.error('Error listing API keys:', error);
            return [];
        }
    }

    /**
     * Test API key validity
     */
    async testAPIKey(
        service: ServiceId,
        keyType: string,
        value: string
    ): Promise<KeyValidationResult> {
        try {
            const response = await fetch(
                `${BRAIN_API_URL}/api/brain/portal/tenant/${this.tenantId}/api-keys/test`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        service,
                        keyType,
                        value,
                    }),
                }
            );

            if (!response.ok) {
                return {
                    isValid: false,
                    strength: 0,
                    compliance: {
                        pciDss: false,
                        soc2: false,
                        gdpr: false,
                        hipaa: false,
                    },
                    error: 'Failed to validate key',
                };
            }

            const data = await response.json();
            return data.validation;
        } catch (error) {
            console.error('Error testing API key:', error);
            return {
                isValid: false,
                strength: 0,
                compliance: {
                    pciDss: false,
                    soc2: false,
                    gdpr: false,
                    hipaa: false,
                },
                error: error instanceof Error ? error.message : 'Unknown error',
            };
        }
    }

    /**
     * Get LLM provider configuration with BYOK
     */
    async getLLMConfig(provider: LLMProvider): Promise<{
        apiKey: string | null;
        baseURL?: string;
        usingPlatformKey: boolean;
    }> {
        let apiKey: string | null = null;
        let usingPlatformKey = false;

        switch (provider) {
            case 'openai':
                apiKey = await this.getAPIKey('openai', 'api_key', true);
                usingPlatformKey = !(await this.getTenantKeyFromVault('openai', 'api_key'));
                break;

            case 'anthropic':
                apiKey = await this.getAPIKey('anthropic', 'api_key', true);
                usingPlatformKey = !(await this.getTenantKeyFromVault('anthropic', 'api_key'));
                break;

            case 'openrouter':
                apiKey = await this.getAPIKey('openrouter', 'api_key', true);
                usingPlatformKey = !(await this.getTenantKeyFromVault('openrouter', 'api_key'));
                return {
                    apiKey,
                    baseURL: 'https://openrouter.ai/api/v1',
                    usingPlatformKey,
                };

            case 'google':
                apiKey = await this.getAPIKey('google_ai', 'api_key', true);
                usingPlatformKey = !(await this.getTenantKeyFromVault('google_ai', 'api_key'));
                break;

            default:
                break;
        }

        return {
            apiKey,
            usingPlatformKey,
        };
    }

    /**
     * Get usage statistics for tenant
     */
    async getUsageStats(): Promise<{
        totalRequests: number;
        totalCost: number;
        byService: Record<string, { requests: number; cost: number }>;
    }> {
        try {
            const response = await fetch(
                `${BRAIN_API_URL}/api/brain/portal/tenant/${this.tenantId}/usage-stats`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                }
            );

            if (!response.ok) {
                return {
                    totalRequests: 0,
                    totalCost: 0,
                    byService: {},
                };
            }

            const data = await response.json();
            return data.stats;
        } catch (error) {
            console.error('Error fetching usage stats:', error);
            return {
                totalRequests: 0,
                totalCost: 0,
                byService: {},
            };
        }
    }

    /**
     * Check if key is still valid (not expired)
     */
    private isKeyValid(key: APIKey): boolean {
        if (!key.expiresAt) {
            return key.isValid;
        }

        const expirationDate = new Date(key.expiresAt);
        const now = new Date();

        return key.isValid && expirationDate > now;
    }

    /**
     * Clear cache
     */
    clearCache(): void {
        this.cache.clear();
    }

    /**
     * Rotate API key (delete old, set new)
     */
    async rotateAPIKey(
        service: ServiceId,
        keyType: string,
        newValue: string
    ): Promise<boolean> {
        try {
            // Test new key first
            const validation = await this.testAPIKey(service, keyType, newValue);
            if (!validation.isValid) {
                throw new Error('New API key is invalid');
            }

            // Set new key
            const success = await this.setAPIKey(service, keyType, newValue);
            if (!success) {
                throw new Error('Failed to set new API key');
            }

            return true;
        } catch (error) {
            console.error('Error rotating API key:', error);
            return false;
        }
    }
}

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Get service information
 */
export function getServiceInfo(serviceId: ServiceId) {
    return SERVICE_CATALOG[serviceId];
}

/**
 * Get all services by category
 */
export function getServicesByCategory(category: string) {
    return Object.entries(SERVICE_CATALOG)
        .filter(([_, service]) => service.category === category)
        .map(([id, service]) => ({ id, ...service }));
}

/**
 * Get all service categories
 */
export function getServiceCategories(): string[] {
    const categories = new Set(
        Object.values(SERVICE_CATALOG).map((service) => service.category)
    );
    return Array.from(categories);
}

/**
 * Validate key format (basic validation)
 */
export function validateKeyFormat(
    service: ServiceId,
    keyType: string,
    value: string
): { isValid: boolean; error?: string } {
    if (!value || value.trim().length === 0) {
        return { isValid: false, error: 'Key cannot be empty' };
    }

    // Service-specific validation
    switch (service) {
        case 'openai':
            if (keyType === 'api_key' && !value.startsWith('sk-')) {
                return { isValid: false, error: 'OpenAI API keys should start with "sk-"' };
            }
            break;

        case 'anthropic':
            if (keyType === 'api_key' && !value.startsWith('sk-ant-')) {
                return { isValid: false, error: 'Anthropic API keys should start with "sk-ant-"' };
            }
            break;

        case 'openrouter':
            if (keyType === 'api_key' && !value.startsWith('sk-or-')) {
                return { isValid: false, error: 'OpenRouter API keys should start with "sk-or-"' };
            }
            break;

        case 'stripe':
            if (keyType === 'secret_key' && !value.startsWith('sk_')) {
                return { isValid: false, error: 'Stripe secret keys should start with "sk_"' };
            }
            if (keyType === 'publishable_key' && !value.startsWith('pk_')) {
                return { isValid: false, error: 'Stripe publishable keys should start with "pk_"' };
            }
            break;

        default:
            break;
    }

    // Check minimum length
    if (value.length < 20) {
        return { isValid: false, error: 'Key is too short (minimum 20 characters)' };
    }

    return { isValid: true };
}

/**
 * Mask API key for display
 */
export function maskAPIKey(value: string): string {
    if (!value || value.length < 8) {
        return '••••••••';
    }

    const visibleChars = 4;
    const start = value.substring(0, visibleChars);
    const end = value.substring(value.length - visibleChars);

    return `${start}${'•'.repeat(Math.max(8, value.length - visibleChars * 2))}${end}`;
}

/**
 * Calculate key strength (0-100)
 */
export function calculateKeyStrength(value: string): number {
    let strength = 0;

    // Length
    if (value.length >= 32) strength += 25;
    else if (value.length >= 24) strength += 15;
    else if (value.length >= 16) strength += 10;

    // Character diversity
    const hasUpperCase = /[A-Z]/.test(value);
    const hasLowerCase = /[a-z]/.test(value);
    const hasNumbers = /[0-9]/.test(value);
    const hasSpecialChars = /[^A-Za-z0-9]/.test(value);

    if (hasUpperCase) strength += 15;
    if (hasLowerCase) strength += 15;
    if (hasNumbers) strength += 15;
    if (hasSpecialChars) strength += 15;

    // Entropy
    const uniqueChars = new Set(value).size;
    const entropyScore = (uniqueChars / value.length) * 15;
    strength += entropyScore;

    return Math.min(100, Math.round(strength));
}

// ============================================================================
// Export singleton factory
// ============================================================================

const byokManagers = new Map<string, BYOKManager>();

export function getBYOKManager(tenantId: string): BYOKManager {
    if (!byokManagers.has(tenantId)) {
        byokManagers.set(tenantId, new BYOKManager(tenantId));
    }
    return byokManagers.get(tenantId)!;
}
