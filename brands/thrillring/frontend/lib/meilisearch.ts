export const searchClient = {
    index: (indexName: string) => ({
        search: async (query: string) => ({ hits: [] })
    })
};

export const mockBusinessListings = [];
export const initializeMeilisearch = async () => { };
export const indexBusinessListings = async () => { };
export const getBusinessFacets = async () => ({});
export const searchBusinesses = async () => ({ hits: [] });
export const getBusinessSuggestions = async () => [];

export const getMeilisearchClient = () => searchClient;
