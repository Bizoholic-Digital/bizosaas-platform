export const searchClient = {
    index: (indexName: string) => ({
        search: async (query: string) => ({ hits: [] })
    })
};

export const getMeilisearchClient = () => searchClient;
