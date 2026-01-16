import axios from 'axios';
import { Business, Category, SearchFilters, SearchResult, Review } from '@/types/business';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://api.bizoholic.net';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const businessAPI = {
    getFeaturedBusinesses: async (): Promise<Business[]> => {
        try {
            const { data } = await api.get('/directory/featured');
            return data;
        } catch (error) {
            console.error('Error fetching featured businesses:', error);
            return [];
        }
    },

    getCategories: async (): Promise<Category[]> => {
        try {
            const { data } = await api.get('/directory/categories');
            return data;
        } catch (error) {
            console.error('Error fetching categories:', error);
            return [];
        }
    },

    getBusiness: async (id: string): Promise<Business | null> => {
        try {
            const { data } = await api.get(`/directory/business/${id}`);
            return data;
        } catch (error) {
            console.error(`Error fetching business ${id}:`, error);
            return null;
        }
    },

    getBusinessReviews: async (id: string): Promise<Review[]> => {
        try {
            const { data } = await api.get(`/directory/business/${id}/reviews`);
            return data;
        } catch (error) {
            console.error(`Error fetching reviews for business ${id}:`, error);
            return [];
        }
    },

    searchBusinesses: async (filters: SearchFilters): Promise<SearchResult> => {
        try {
            const { data } = await api.get('/directory/search', { params: filters });
            return data;
        } catch (error) {
            console.error('Error searching businesses:', error);
            return {
                businesses: [],
                total: 0,
                page: 1,
                limit: 10,
                filters: filters
            };
        }
    },

    getSearchSuggestions: async (query: string, location?: string): Promise<SearchSuggestion[]> => {
        try {
            const { data } = await api.get('/directory/suggestions', {
                params: { q: query, location }
            });
            return data;
        } catch (error) {
            console.error('Error fetching suggestions:', error);
            return [];
        }
    }
};
