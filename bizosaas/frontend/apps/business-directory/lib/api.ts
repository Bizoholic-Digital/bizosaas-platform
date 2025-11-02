// Business Directory API Client
// Modular DDD Microservice - Self-contained API utilities

import { Business, Review, Category, SearchFilters, SearchResult, SearchSuggestion, BusinessEvent, BusinessProduct, BusinessCoupon } from '@/types/business';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3004';

async function apiRequest(endpoint: string, options?: RequestInit) {
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

export const businessAPI = {
  // Search businesses
  searchBusinesses: async (filters: SearchFilters): Promise<SearchResult> => {
    const params = new URLSearchParams();
    if (filters.query) params.append('query', filters.query);
    if (filters.location) params.append('location', filters.location);
    if (filters.category) params.append('category', filters.category);
    if (filters.rating) params.append('rating', filters.rating.toString());
    if (filters.priceRange) params.append('priceRange', filters.priceRange);
    if (filters.openNow) params.append('openNow', 'true');
    if (filters.featured) params.append('featured', 'true');
    if (filters.sortBy) params.append('sortBy', filters.sortBy);
    if (filters.sortOrder) params.append('sortOrder', filters.sortOrder);

    return apiRequest(`/api/brain/business-directory/search?${params.toString()}`);
  },

  // Get a single business by ID
  getBusiness: async (id: string): Promise<Business> => {
    return apiRequest(`/api/brain/business-directory/businesses/${id}`);
  },

  // Get featured businesses
  getFeaturedBusinesses: async (): Promise<Business[]> => {
    return apiRequest('/api/brain/business-directory/businesses?featured=true');
  },

  // Get business reviews
  getBusinessReviews: async (businessId: string): Promise<Review[]> => {
    return apiRequest(`/api/brain/business-directory/businesses/${businessId}/reviews`);
  },

  // Get business events
  getBusinessEvents: async (businessId: string): Promise<BusinessEvent[]> => {
    return apiRequest(`/api/brain/business-directory/businesses/${businessId}/events`);
  },

  // Get business products/services
  getBusinessProducts: async (businessId: string): Promise<BusinessProduct[]> => {
    return apiRequest(`/api/brain/business-directory/businesses/${businessId}/products`);
  },

  // Get business coupons/offers
  getBusinessCoupons: async (businessId: string): Promise<BusinessCoupon[]> => {
    return apiRequest(`/api/brain/business-directory/businesses/${businessId}/coupons`);
  },

  // Get categories
  getCategories: async (): Promise<Category[]> => {
    return apiRequest('/api/brain/business-directory/categories');
  },

  // Get search suggestions (autocomplete)
  getSearchSuggestions: async (query: string, location?: string): Promise<SearchSuggestion[]> => {
    const params = new URLSearchParams();
    params.append('query', query);
    if (location) params.append('location', location);

    return apiRequest(`/api/brain/business-directory/suggestions?${params.toString()}`);
  },
};
