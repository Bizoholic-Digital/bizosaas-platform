import { brainApi, ApiResponse } from './brain-client';

export interface CMSPage {
    id: string;
    title: string;
    slug: string;
    content: string;
    status: 'publish' | 'draft' | 'private' | 'trash';
    author_id?: string;
    created_at?: string;
    updated_at?: string;
}

export interface CMSPost {
    id: string;
    title: string;
    slug: string;
    content: string;
    excerpt?: string;
    status: 'publish' | 'draft' | 'private' | 'trash';
    author_id?: string;
    categories?: number[];
    tags?: number[];
    featured_media?: number;
}

export interface CMSMedia {
    id: string;
    url: string;
    title: string;
    mime_type: string;
}

export class CmsApi {
    // Pages
    async getPages(params?: { limit?: number; status?: string }): Promise<ApiResponse<CMSPage[]>> {
        const queryParams = new URLSearchParams(params as any).toString();
        return brainApi.get<CMSPage[]>(`/api/brain/cms/pages${queryParams ? `?${queryParams}` : ''}`);
    }

    async getPage(id: string): Promise<ApiResponse<CMSPage>> {
        return brainApi.get<CMSPage>(`/api/brain/cms/pages/${id}`);
    }

    async createPage(page: Partial<CMSPage>): Promise<ApiResponse<CMSPage>> {
        return brainApi.post<CMSPage>('/api/brain/cms/pages', page);
    }

    async updatePage(id: string, updates: Partial<CMSPage>): Promise<ApiResponse<CMSPage>> {
        return brainApi.put<CMSPage>(`/api/brain/cms/pages/${id}`, updates);
    }

    async deletePage(id: string): Promise<ApiResponse<boolean>> {
        return brainApi.delete<boolean>(`/api/brain/cms/pages/${id}`);
    }

    // Posts
    async getPosts(params?: { limit?: number; status?: string }): Promise<ApiResponse<CMSPost[]>> {
        const queryParams = new URLSearchParams(params as any).toString();
        return brainApi.get<CMSPost[]>(`/api/brain/cms/posts${queryParams ? `?${queryParams}` : ''}`);
    }

    async createPost(post: Partial<CMSPost>): Promise<ApiResponse<CMSPost>> {
        return brainApi.post<CMSPost>('/api/brain/cms/posts', post);
    }

    async updatePost(id: string, updates: Partial<CMSPost>): Promise<ApiResponse<CMSPost>> {
        return brainApi.put<CMSPost>(`/api/brain/cms/posts/${id}`, updates);
    }

    async deletePost(id: string): Promise<ApiResponse<boolean>> {
        return brainApi.delete<boolean>(`/api/brain/cms/posts/${id}`);
    }

    // Media
    async getMedia(params?: { limit?: number }): Promise<ApiResponse<CMSMedia[]>> {
        return brainApi.get<CMSMedia[]>('/api/brain/cms/media');
    }

    // Connection & Analytics
    async checkConnection(): Promise<ApiResponse<{ connected: boolean; platform?: string; version?: string }>> {
        return brainApi.get<{ connected: boolean; platform?: string; version?: string }>('/api/brain/cms/status');
    }

    async getStats(): Promise<ApiResponse<{ pages: number; posts: number; media: number; lastSync?: string }>> {
        return brainApi.get<{ pages: number; posts: number; media: number; lastSync?: string }>('/api/brain/cms/stats');
    }
}

export const cmsApi = new CmsApi();
