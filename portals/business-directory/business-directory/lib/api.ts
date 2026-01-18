import axios from 'axios';
import { Business, Category, SearchFilters, SearchResult, Review, SearchSuggestion } from '@/types/business';

// For client-side requests, use relative path to hit Next.js API routes
// For server-side requests (SSR), use the configured API URL or localhost
const API_BASE_URL = typeof window !== 'undefined'
    ? ''
    : ((process.env.NEXT_PUBLIC_API_BASE_URL) || 'http://localhost:3005');

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const businessAPI = {
    getFeaturedBusinesses: async (): Promise<Business[]> => {
        try {
            const { data } = await api.get('/api/brain/business-directory/businesses/featured');
            return data;
        } catch (error) {
            console.error('Error fetching featured businesses:', error);
            return [];
        }
    },

    getCategories: async (): Promise<Category[]> => {
        try {
            const { data } = await api.get('/api/brain/business-directory/categories');
            return data;
        } catch (error) {
            console.error('Error fetching categories:', error);
            return [];
        }
    },

    getBusiness: async (id: string): Promise<Business | null> => {
        try {
            const { data } = await api.get(`/api/brain/business-directory/businesses/${id}`);
            return data;
        } catch (error) {
            console.error(`Error fetching business ${id}:`, error);
            return null;
        }
    },

    getBusinessBySlug: async (slug: string): Promise<Business | null> => {
        try {
            const { data } = await api.get(`/api/brain/business-directory/businesses/${slug}`);
            return data;
        } catch (error) {
            console.error(`Error fetching business by slug ${slug}:`, error);
            return null;
        }
    },

    getBusinessReviews: async (id: string): Promise<Review[]> => {
        try {
            const { data } = await api.get(`/api/brain/business-directory/businesses/${id}/reviews`);
            return data;
        } catch (error) {
            console.error(`Error fetching reviews for business ${id}:`, error);
            return [];
        }
    },

    getBusinessEvents: async (id: string): Promise<any[]> => {
        try {
            const { data } = await api.get(`/api/brain/business-directory/businesses/${id}/events`);
            return data;
        } catch (error) {
            console.error(`Error fetching events for business ${id}:`, error);
            return [];
        }
    },

    getBusinessProducts: async (id: string): Promise<any[]> => {
        try {
            const { data } = await api.get(`/api/brain/business-directory/businesses/${id}/products`);
            return data;
        } catch (error) {
            console.error(`Error fetching products for business ${id}:`, error);
            return [];
        }
    },

    getBusinessCoupons: async (id: string): Promise<any[]> => {
        try {
            const { data } = await api.get(`/api/brain/business-directory/businesses/${id}/coupons`);
            return data;
        } catch (error) {
            console.error(`Error fetching coupons for business ${id}:`, error);
            return [];
        }
    },

    searchBusinesses: async (filters: SearchFilters): Promise<SearchResult> => {
        try {
            const { data } = await api.get('/api/brain/business-directory/search', { params: filters });
            return data;
        } catch (error) {
            console.error('Error searching businesses:', error);
            return {
                businesses: [],
                total: 0,
                page: 1,
                limit: 10,
                filters: filters,
                suggestions: []
            };
        }
    },

    getSearchSuggestions: async (query: string, location?: string): Promise<SearchSuggestion[]> => {
        try {
            // Call local proxy instead of direct backend to get transformed suggestions
            const { data } = await axios.get('/api/brain/business-directory/suggestions', {
                params: { q: query, location }
            });
            return data;
        } catch (error) {
            console.error('Error fetching suggestions:', error);
            return [];
        }
    },

    claimBusiness: async (id: string, method: string, contactData: any): Promise<any> => {
        try {
            const { data } = await api.post(`/api/brain/business-directory/businesses/${id}/claim`, {
                method,
                data: contactData
            });
            return data;
        } catch (error) {
            console.error(`Error claiming business ${id}:`, error);
            throw error;
        }
    },

    verifyClaim: async (claimId: string, code: string): Promise<any> => {
        try {
            const { data } = await api.post(`/api/brain/business-directory/claims/${claimId}/verify`, {
                code
            });
            return data;
        } catch (error) {
            console.error(`Error verifying claim ${claimId}:`, error);
            throw error;
        }
    },

    resendVerificationCode: async (claimId: string): Promise<any> => {
        try {
            const { data } = await api.post(`/api/brain/business-directory/claims/${claimId}/resend`);
            return data;
        } catch (error) {
            console.error(`Error resending code for claim ${claimId}:`, error);
            throw error;
        }
    },

    getMyListings: async (): Promise<Business[]> => {
        try {
            // Using a specific proxy route to ensure valid auth context is passed
            const { data } = await api.get('/api/brain/business-directory/businesses/my');
            return data;
        } catch (error) {
            console.error('Error fetching user listings:', error);
            return [];
        }
    }
};
