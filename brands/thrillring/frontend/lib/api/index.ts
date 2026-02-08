// Mock API Client to satisfy build requirements
// This should be replaced with real backend integration later

export const apiClient = {
    getCampaigns: async (params: any) => {
        console.log('Mock getCampaigns call', params);
        return { data: [] };
    },
    getOrders: async () => {
        return { data: [] };
    },
    getAnalytics: async () => {
        return { data: {} };
    }
};
