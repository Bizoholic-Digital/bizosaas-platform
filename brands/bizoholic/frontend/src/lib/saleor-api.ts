export interface SaleorProductMedia {
    id?: string;
    url: string;
    alt?: string;
    type?: 'IMAGE' | 'VIDEO';
}

export interface SaleorAttribute {
    attribute: {
        id?: string;
        name: string;
        slug: string;
    };
    values: Array<{
        id?: string;
        name: string;
        slug: string;
    }>;
}

export interface SaleorProduct {
    id: string;
    name: string;
    description?: string;
    slug?: string;
    thumbnail?: {
        url: string;
        alt?: string;
    };
    media?: SaleorProductMedia[];
    metadata?: Array<{
        key: string;
        value: string;
    }>;
    category?: {
        id: string;
        name: string;
        slug: string;
    };
    attributes?: SaleorAttribute[];
    variants: SaleorProductVariant[];
    defaultVariant?: SaleorProductVariant;
}

export interface SaleorProductVariant {
    id: string;
    name: string;
    sku: string;
    pricing?: {
        price?: {
            gross: {
                amount: number;
                currency: string;
            };
        };
    };
    quantityAvailable?: number;
    weight?: {
        value: number;
        unit: string;
    };
    attributes: SaleorAttribute[];
}

class SaleorAPIClient {
    private apiBaseUrl: string;

    constructor() {
        this.apiBaseUrl = process.env.NEXT_PUBLIC_SALEOR_API_URL || 'https://api.bizoholic.net/saleor/graphql';
    }

    async getProduct(id: string): Promise<SaleorProduct | null> {
        // Implementation for fetching a product via GraphQL
        return null;
    }

    async getProducts(options?: { first?: number; after?: string }): Promise<any> {
        // Implementation for fetching products via GraphQL
        return {
            products: {
                edges: []
            }
        };
    }

    async addToCart(variantId: string, quantity: number): Promise<boolean> {
        // Implementation for adding to a Saleor checkout
        return true;
    }
}

export const saleorAPI = new SaleorAPIClient();
