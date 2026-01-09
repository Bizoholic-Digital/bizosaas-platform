// Brain API Client
// Handles communication with the Brain Gateway Service

const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8000';

export interface Connector {
    id: string;
    name: string;
    type: string;
    icon: string;
    description: string;
    auth_schema?: any;
    status?: string;
}

export interface Agent {
    id: string;
    name: string;
    description: string;
    role: string;
    capabilities: string[];
    tools: string[];
    icon: string;
    color: string;
    status: 'active' | 'inactive';
    category: string;
    costTier: 'free' | 'standard' | 'premium';
}

export interface ChatResponse {
    agent_id: string;
    message: string;
    suggestions: string[];
    actions: any[];
}

const apiFetch = async (endpoint: string, options: any = {}, token?: string) => {
    let authToken = token;

    // Auto-retrieve token from Clerk if not provided (Client-side only)
    if (!authToken && typeof window !== 'undefined') {
        try {
            // @ts-ignore
            authToken = await window.Clerk?.session?.getToken();
        } catch (e) {
            console.warn('[BrainAPI] Failed to auto-retrieve Clerk token', e);
        }
    }

    const headers = {
        ...(!(options.body instanceof FormData) && { 'Content-Type': 'application/json' }),
        ...(authToken ? { 'Authorization': `Bearer ${authToken}` } : {}),
        ...options.headers,
    };

    const baseUrl = typeof window !== 'undefined' ? '/api/brain' : BRAIN_GATEWAY_URL;

    // If endpoint starts with /api and we are using the proxied baseUrl (/api/brain),
    // strip the /api prefix from the endpoint to avoid double /api/api/...
    const sanitizedEndpoint = (typeof window !== 'undefined' && endpoint.startsWith('/api'))
        ? endpoint.substring(4)
        : endpoint;

    const fetchUrl = `${baseUrl}${sanitizedEndpoint}`;

    if (process.env.NODE_ENV === 'development') {
        console.log(`[BrainAPI] Fetching: ${fetchUrl}`, { method: options.method || 'GET' });
    }

    const res = await fetch(fetchUrl, {
        ...options,
        headers,
    });


    if (!res.ok) {
        // Handle 401/403 specifically if needed
        if (res.status === 401) {
            console.error('[BrainAPI] Unauthorized access to Brain Gateway');
        }

        let errorDetail = 'API request failed';
        try {
            const errorData = await res.json();
            errorDetail = errorData.detail || errorData.message || `Error ${res.status}: ${res.statusText}`;
        } catch (e) {
            errorDetail = `Error ${res.status}: ${res.statusText}`;
            // If it's a 404/500 with HTML body, log it
            console.warn(`[BrainAPI] Non-JSON error response from ${fetchUrl}`, res.status);
        }

        throw new Error(errorDetail);
    }

    return res.json();
};

export const brainApi = {
    // Generic helper for direct URL access if needed
    get: async (endpoint: string, token?: string) => {
        return apiFetch(endpoint, {}, token);
    },
    connectors: {
        getConnectors: async (token?: string): Promise<Connector[]> => {
            return apiFetch('/api/connectors', {}, token);
        },
        listTypes: async (token?: string): Promise<Connector[]> => {
            return apiFetch('/api/connectors/types', {}, token);
        },
        connect: async (connectorId: string, credentials: any, token?: string) => {
            return apiFetch(`/api/connectors/${connectorId}/connect`, {
                method: 'POST',
                body: JSON.stringify(credentials)
            }, token);
        },
        sync: async (connectorId: string, resource: string, token?: string) => {
            return apiFetch(`/api/connectors/${connectorId}/sync/${resource}`, {}, token);
        },
        performAction: async (connectorId: string, action: string, payload: any, token?: string) => {
            return apiFetch(`/api/connectors/${connectorId}/action/${action}`, {
                method: 'POST',
                body: JSON.stringify(payload)
            }, token);
        },
        getStatus: async (connectorId: string, token?: string) => {
            try {
                return await apiFetch(`/api/connectors/${connectorId}/status`, {}, token);
            } catch (e) {
                return { status: 'disconnected' };
            }
        },
        discover: async (connectorId: string, resource: string, token?: string) => {
            return apiFetch(`/api/connectors/${connectorId}/discover/${resource}`, {}, token);
        },
        autoLinkGoogle: async (accessToken: string, extraPayload: any = {}, token?: string) => {
            return apiFetch('/api/onboarding/google/discover', {
                method: 'POST',
                body: JSON.stringify({ access_token: accessToken, ...extraPayload })
            }, token);
        }
    },
    agents: {
        list: async (token?: string): Promise<Agent[]> => {
            const data = await apiFetch('/api/agents/', {}, token);
            return data.map((agent: any) => ({
                ...agent,
                status: 'active',
                category: 'general',
                costTier: 'standard'
            }));
        },
        get: async (agentId: string, token?: string): Promise<Agent> => {
            const data = await apiFetch(`/api/agents/${agentId}`, {}, token);
            return {
                ...data,
                status: 'active',
                category: 'general',
                costTier: 'standard'
            };
        },
        chat: async (agentId: string, message: string, context?: any, token?: string): Promise<ChatResponse> => {
            return apiFetch(`/api/agents/${agentId}/chat`, {
                method: 'POST',
                body: JSON.stringify({ message, context })
            }, token);
        },
        updateConfig: async (agentId: string, config: any, token?: string) => {
            console.log(`[Mock] Updating config for agent ${agentId}`, config);
            return { success: true };
        },
        getHistory: async (agentId: string, token?: string) => {
            try {
                return await apiFetch(`/api/agents/${agentId}/history`, {}, token);
            } catch (e) {
                return [];
            }
        }
    },
    mcp: {
        listCategories: async (token?: string): Promise<any[]> => {
            return apiFetch('/api/mcp/categories', {}, token);
        },
        getRegistry: async (categorySlug?: string, token?: string): Promise<any[]> => {
            const path = categorySlug
                ? `/api/mcp/registry?category=${categorySlug}`
                : '/api/mcp/registry';
            return apiFetch(path, {}, token);
        },
        install: async (mcpSlug: string, config?: any, token?: string) => {
            return apiFetch('/api/mcp/install', {
                method: 'POST',
                body: JSON.stringify({ mcp_slug: mcpSlug, config })
            }, token);
        },
        getInstalled: async (token?: string): Promise<any[]> => {
            return apiFetch('/api/mcp/installed', {}, token);
        }
    },
    cms: {
        getPages: async (token?: string) => {
            return apiFetch('/api/cms/pages', {}, token);
        },
        createPage: async (page: any, token?: string) => {
            return apiFetch('/api/cms/pages', {
                method: 'POST',
                body: JSON.stringify(page)
            }, token);
        },
        updatePage: async (id: string, page: any, token?: string) => {
            return apiFetch(`/api/cms/pages/${id}`, {
                method: 'PUT',
                body: JSON.stringify(page)
            }, token);
        },
        deletePage: async (id: string, token?: string) => {
            return apiFetch(`/api/cms/pages/${id}`, {
                method: 'DELETE'
            }, token);
        },
        getPosts: async (token?: string) => {
            return apiFetch('/api/cms/posts', {}, token);
        },
        createPost: async (post: any, token?: string) => {
            return apiFetch('/api/cms/posts', {
                method: 'POST',
                body: JSON.stringify(post)
            }, token);
        },
        updatePost: async (id: string, post: any, token?: string) => {
            return apiFetch(`/api/cms/posts/${id}`, {
                method: 'PUT',
                body: JSON.stringify(post)
            }, token);
        },
        deletePost: async (id: string, token?: string) => {
            return apiFetch(`/api/cms/posts/${id}`, {
                method: 'DELETE'
            }, token);
        },
        listMedia: async (token?: string) => {
            return apiFetch('/api/cms/media', {}, token);
        },
        uploadMedia: async (formData: FormData, token?: string) => {
            // Note: FormData handling needs special care for headers usually, 
            // but apiFetch handles JSON. For upload we might need to bypass content-type json.
            // Assuming the gateway handles multipart/form-data if we don't set Content-Type.
            return apiFetch('/api/cms/media', {
                method: 'POST',
                body: formData,
                headers: {} // Let browser set boundary
            }, token);
        },
        deleteMedia: async (id: string, token?: string) => {
            return apiFetch(`/api/cms/media/${id}`, {
                method: 'DELETE'
            }, token);
        },
        getCategories: async (token?: string) => {
            return apiFetch('/api/cms/categories', {}, token);
        },
        createCategory: async (category: any, token?: string) => {
            return apiFetch('/api/cms/categories', {
                method: 'POST',
                body: JSON.stringify(category)
            }, token);
        },
        updateCategory: async (id: string, category: any, token?: string) => {
            return apiFetch(`/api/cms/categories/${id}`, {
                method: 'PUT',
                body: JSON.stringify(category)
            }, token);
        },
        deleteCategory: async (id: string, token?: string) => {
            return apiFetch(`/api/cms/categories/${id}`, {
                method: 'DELETE'
            }, token);
        },
        getPlugins: async (token?: string) => {
            return apiFetch('/api/cms/plugins', {}, token);
        },
        installPlugin: async (slug: string, token?: string) => {
            return apiFetch(`/api/cms/plugins/${slug}/install`, {
                method: 'POST'
            }, token);
        },
        activatePlugin: async (slug: string, token?: string) => {
            return apiFetch(`/api/cms/plugins/${slug}/activate`, {
                method: 'POST'
            }, token);
        },
        deactivatePlugin: async (slug: string, token?: string) => {
            return apiFetch(`/api/cms/plugins/${slug}/deactivate`, {
                method: 'POST'
            }, token);
        },
        deletePlugin: async (slug: string, token?: string) => {
            return apiFetch(`/api/cms/plugins/${slug}`, {
                method: 'DELETE'
            }, token);
        }
    },
    crm: {
        getContacts: async (limit: number = 100, token?: string) => {
            return apiFetch(`/api/crm/contacts?limit=${limit}`, {}, token);
        },
        getDeals: async (limit: number = 100, token?: string) => {
            return apiFetch(`/api/crm/deals?limit=${limit}`, {}, token);
        },
        createContact: async (contact: any, token?: string) => {
            return apiFetch('/api/crm/contacts', {
                method: 'POST',
                body: JSON.stringify(contact)
            }, token);
        },
        updateContact: async (id: string, contact: any, token?: string) => {
            return apiFetch(`/api/crm/contacts/${id}`, {
                method: 'PUT',
                body: JSON.stringify(contact)
            }, token);
        },
        deleteContact: async (id: string, token?: string) => {
            return apiFetch(`/api/crm/contacts/${id}`, {
                method: 'DELETE'
            }, token);
        },
        createDeal: async (deal: any, token?: string) => {
            return apiFetch('/api/crm/deals', {
                method: 'POST',
                body: JSON.stringify(deal)
            }, token);
        },
        updateDeal: async (id: string, deal: any, token?: string) => {
            return apiFetch(`/api/crm/deals/${id}`, {
                method: 'PUT',
                body: JSON.stringify(deal)
            }, token);
        },
        deleteDeal: async (id: string, token?: string) => {
            return apiFetch(`/api/crm/deals/${id}`, {
                method: 'DELETE'
            }, token);
        }
    },
    ecommerce: {
        getProducts: async (limit: number = 100, token?: string) => {
            return apiFetch(`/api/ecommerce/products?limit=${limit}`, {}, token);
        },
        createProduct: async (product: any, token?: string) => {
            return apiFetch('/api/ecommerce/products', {
                method: 'POST',
                body: JSON.stringify(product)
            }, token);
        },
        updateProduct: async (id: string, product: any, token?: string) => {
            return apiFetch(`/api/ecommerce/products/${id}`, {
                method: 'PUT',
                body: JSON.stringify(product)
            }, token);
        },
        deleteProduct: async (id: string, token?: string) => {
            return apiFetch(`/api/ecommerce/products/${id}`, {
                method: 'DELETE'
            }, token);
        },
        getOrders: async (limit: number = 100, token?: string) => {
            return apiFetch(`/api/ecommerce/orders?limit=${limit}`, {}, token);
        }
    },
    marketing: {
        getLists: async (token?: string) => {
            return apiFetch('/api/marketing/lists', {}, token);
        },
        getCampaigns: async (token?: string) => {
            return apiFetch('/api/marketing/campaigns', {}, token);
        },
        getStats: async (token?: string) => {
            return apiFetch('/api/marketing/stats', {}, token);
        },
        createList: async (name: string, token?: string) => {
            return apiFetch('/api/marketing/lists', {
                method: 'POST',
                body: JSON.stringify({ name })
            }, token);
        },
        deleteList: async (id: string, token?: string) => {
            return apiFetch(`/api/marketing/lists/${id}`, {
                method: 'DELETE'
            }, token);
        },
        createCampaign: async (campaign: any, token?: string) => {
            return apiFetch('/api/marketing/campaigns', {
                method: 'POST',
                body: JSON.stringify(campaign)
            }, token);
        },
        deleteCampaign: async (id: string, token?: string) => {
            return apiFetch(`/api/marketing/campaigns/${id}`, {
                method: 'DELETE'
            }, token);
        }
    },
    campaigns: {
        create: async (data: any, token?: string) => {
            return apiFetch('/api/campaigns/', {
                method: 'POST',
                body: JSON.stringify(data)
            }, token);
        },
        list: async (token?: string) => {
            return apiFetch('/api/campaigns/', {}, token);
        },
        get: async (id: string, token?: string) => {
            return apiFetch(`/api/campaigns/${id}`, {}, token);
        },
        publish: async (id: string, token?: string) => {
            return apiFetch(`/api/campaigns/${id}/publish`, {
                method: 'POST'
            }, token);
        }
    },
    users: {
        me: async (token?: string) => {
            return apiFetch('/api/users/me', {}, token);
        },
        updateMe: async (data: any, token?: string) => {
            return apiFetch('/api/users/me', {
                method: 'PATCH',
                body: JSON.stringify(data)
            }, token);
        }
    },
    workflows: {
        list: async (token?: string) => {
            return apiFetch('/api/workflows', {}, token);
        },
        create: async (workflow: any, token?: string) => {
            return apiFetch('/api/workflows', {
                method: 'POST',
                body: JSON.stringify(workflow)
            }, token);
        },
        updateConfig: async (id: string, config: any, token?: string) => {
            return apiFetch(`/api/workflows/${id}/config`, {
                method: 'POST',
                body: JSON.stringify(config)
            }, token);
        },
        toggle: async (id: string, token?: string) => {
            return apiFetch(`/api/workflows/${id}/toggle`, {
                method: 'POST'
            }, token);
        },
        getExecutionData: async (id: string, token?: string) => {
            // Mocking execution data for DAG visualization
            return {
                nodes: [
                    { id: 'start', label: 'Trigger: New Lead', type: 'trigger', status: 'completed' },
                    { id: 'qualify', label: 'AI Qualification', type: 'action', status: 'completed' },
                    { id: 'score', label: 'Lead Scoring', type: 'action', status: 'running' },
                    { id: 'assign', label: 'CRM Assignment', type: 'action', status: 'pending' },
                    { id: 'notify', label: 'Slack Notification', type: 'action', status: 'pending' }
                ],
                edges: [
                    { from: 'start', to: 'qualify' },
                    { from: 'qualify', to: 'score' },
                    { from: 'score', to: 'assign' },
                    { from: 'assign', to: 'notify' }
                ]
            };
        },
        getOptimizations: async (token?: string) => {
            return apiFetch('/api/workflows/optimizations', {}, token);
        }
    },
    discovery: {
        getRecommendations: async (token?: string) => {
            return apiFetch('/api/discovery/recommendations', {}, token);
        }
    }
};
