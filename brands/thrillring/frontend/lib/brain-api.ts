// Brain API Client for Thrillring
// Proxies CMS, CRM, and eCommerce requests to Brain Gateway

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8000';

const apiFetch = async (endpoint: string, options: any = {}, token?: string) => {
    let authToken = token;

    if (!authToken && typeof window !== 'undefined') {
        try {
            const impersonationToken = localStorage.getItem('impersonation_token');
            if (impersonationToken) {
                authToken = impersonationToken;
            }
        } catch (e) {
            console.warn('[BrainAPI] Failed to retrieve token', e);
        }
    }

    const headers = {
        ...(!(options.body instanceof FormData) && { 'Content-Type': 'application/json' }),
        ...(authToken ? { 'Authorization': `Bearer ${authToken}` } : {}),
        ...options.headers,
    };

    const baseUrl = typeof window !== 'undefined' ? '/api/brain' : BRAIN_API_URL;
    const sanitizedEndpoint = (typeof window !== 'undefined' && endpoint.startsWith('/api'))
        ? endpoint.substring(4)
        : endpoint;

    const fetchUrl = `${baseUrl}${sanitizedEndpoint}`;

    const res = await fetch(fetchUrl, {
        ...options,
        headers,
    });

    if (!res.ok) {
        let errorDetail = 'API request failed';
        try {
            const errorData = await res.json();
            errorDetail = errorData.detail || errorData.message || `Error ${res.status}: ${res.statusText}`;
        } catch (e) {
            errorDetail = `Error ${res.status}: ${res.statusText}`;
        }
        throw new Error(errorDetail);
    }

    return res.json();
};

export const brainApi = {
    cms: {
        getPages: async (token?: string) => apiFetch('/api/cms/pages', {}, token),
        createPage: async (page: any, token?: string) => apiFetch('/api/cms/pages', { method: 'POST', body: JSON.stringify(page) }, token),
        updatePage: async (id: string, page: any, token?: string) => apiFetch(`/api/cms/pages/${id}`, { method: 'PUT', body: JSON.stringify(page) }, token),
        deletePage: async (id: string, token?: string) => apiFetch(`/api/cms/pages/${id}`, { method: 'DELETE' }, token),
        getPosts: async (token?: string) => apiFetch('/api/cms/posts', {}, token),
        createPost: async (post: any, token?: string) => apiFetch('/api/cms/posts', { method: 'POST', body: JSON.stringify(post) }, token),
        updatePost: async (id: string, post: any, token?: string) => apiFetch(`/api/cms/posts/${id}`, { method: 'PUT', body: JSON.stringify(post) }, token),
        deletePost: async (id: string, token?: string) => apiFetch(`/api/cms/posts/${id}`, { method: 'DELETE' }, token),
        listMedia: async (token?: string) => apiFetch('/api/cms/media', {}, token),
        uploadMedia: async (formData: FormData, token?: string) => apiFetch('/api/cms/media', { method: 'POST', body: formData }, token),
        deleteMedia: async (id: string, token?: string) => apiFetch(`/api/cms/media/${id}`, { method: 'DELETE' }, token),
        getCategories: async (token?: string) => apiFetch('/api/cms/categories', {}, token),
        createCategory: async (category: any, token?: string) => apiFetch('/api/cms/categories', { method: 'POST', body: JSON.stringify(category) }, token),
        updateCategory: async (id: string, category: any, token?: string) => apiFetch(`/api/cms/categories/${id}`, { method: 'PUT', body: JSON.stringify(category) }, token),
        deleteCategory: async (id: string, token?: string) => apiFetch(`/api/cms/categories/${id}`, { method: 'DELETE' }, token),
        getPlugins: async (token?: string) => apiFetch('/api/cms/plugins', {}, token),
        installPlugin: async (slug: string, token?: string) => apiFetch(`/api/cms/plugins/${slug}/install`, { method: 'POST' }, token),
        activatePlugin: async (slug: string, token?: string) => apiFetch(`/api/cms/plugins/${slug}/activate`, { method: 'POST' }, token),
        deactivatePlugin: async (slug: string, token?: string) => apiFetch(`/api/cms/plugins/${slug}/deactivate`, { method: 'POST' }, token),
        deletePlugin: async (slug: string, token?: string) => apiFetch(`/api/cms/plugins/${slug}`, { method: 'DELETE' }, token),
    }
};
