export interface AmazonProduct {
    asin: string;
    title: string;
    brand: string;
    category: string;
    price: {
        amount: number;
        currency: string;
    };
    reviews: {
        rating: number;
        count: number;
    };
    images: string[];
    dropshipEligible: boolean;
    commission?: {
        amount: number;
        currency: string;
    };
}

export interface ListingPlatform {
    id: string;
    name: string;
    enabled: boolean;
    fees: {
        listingFee: number;
        commissionRate: number;
        fulfillmentFee: number;
    };
}

export interface ProductListing {
    id: string;
    title: string;
    sourceAsin: string;
    price: {
        selling: number;
        margin: number;
    };
    platforms: Record<string, {
        status: 'active' | 'pending' | 'failed' | 'processing';
        platformProductId?: string;
        url?: string;
    }>;
    createdAt: string;
}

export interface SellerInventoryItem {
    asin: string;
    sellerSku: string;
    title: string;
    brand?: string;
    price: number;
    quantity: number;
    status: 'active' | 'inactive' | 'incomplete';
    fulfillmentChannel: 'FBA' | 'FBM';
    images: string[];
}

export interface BulkInventoryUpdate {
    asin: string;
    quantity?: number;
    price?: number;
    status?: string;
}

export const mockDropshipProducts: AmazonProduct[] = [
    {
        asin: 'B08N5WRWNW',
        title: 'Adjustable Dumbbell Set - 52.5 lbs',
        brand: 'FitCraft',
        category: 'Electronics',
        price: { amount: 199.99, currency: 'USD' },
        reviews: { rating: 4.8, count: 1245 },
        images: ['https://images.unsplash.com/photo-1583454110551-21f2fa200c01?w=800&auto=format&fit=crop'],
        dropshipEligible: true,
        commission: { amount: 30.00, currency: 'USD' }
    }
];

class AmazonSPAPIClient {
    async searchDropshipProducts(query: string, category: string, minRating: number): Promise<AmazonProduct[]> {
        return mockDropshipProducts;
    }
}

class ProductListingService {
    getAvailablePlatforms(): ListingPlatform[] {
        return [
            { id: 'medusajs', name: 'MedusaJS', enabled: true, fees: { listingFee: 0, commissionRate: 0.05, fulfillmentFee: 2.0 } },
            { id: 'amazon', name: 'Amazon Seller', enabled: true, fees: { listingFee: 0.99, commissionRate: 0.15, fulfillmentFee: 5.0 } },
            { id: 'flipkart', name: 'Flipkart', enabled: false, fees: { listingFee: 0.5, commissionRate: 0.10, fulfillmentFee: 3.0 } }
        ];
    }

    async createListing(product: AmazonProduct, platformIds: string[], markup: number): Promise<ProductListing> {
        const sellingPrice = product.price.amount * (1 + markup);
        const margin = sellingPrice - product.price.amount;

        const platforms: Record<string, any> = {};
        platformIds.forEach(id => {
            platforms[id] = { status: 'pending' };
        });

        return {
            id: `list_${Date.now()}`,
            title: product.title,
            sourceAsin: product.asin,
            price: { selling: sellingPrice, margin },
            platforms,
            createdAt: new Date().toISOString()
        };
    }

    calculateProfitMargins(cost: number, markup: number) {
        const platforms = this.getAvailablePlatforms();
        return platforms.map(p => {
            const sellingPrice = cost * (1 + markup);
            const profit = sellingPrice - cost - (sellingPrice * p.fees.commissionRate) - p.fees.listingFee - p.fees.fulfillmentFee;
            return {
                platform: p.name,
                sellingPrice,
                profit,
                profitMargin: ((profit / sellingPrice) * 100).toFixed(1)
            };
        });
    }
}

export const amazonSPAPI = new AmazonSPAPIClient();
export const productListingService = new ProductListingService();
