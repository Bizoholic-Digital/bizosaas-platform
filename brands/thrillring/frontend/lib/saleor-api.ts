export const getProducts = async () => {
    return [];
};

export const getCategory = async () => {
    return null;
};


export const saleorAPI = {
    getProducts,
    getCategory,
    async getProductBySlug(slug: string) {
        return null;
    }
};

export const saleorStoreAPI = {
    getProducts: async (params: { first?: number, filter?: any }) => {
        return {
            products: {
                edges: []
            }
        };
    },
    getProduct: async (slug: string) => {
        return {
            product: null
        };
    }
};
