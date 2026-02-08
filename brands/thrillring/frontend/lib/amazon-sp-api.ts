export class AmazonSPAPI {
    async getProducts() {
        console.warn("AmazonSPAPI stub called");
        return [];
    }

    async getOrders() {
        return [];
    }
}

export interface AmazonProduct {
    asin: string;
    title: string;
    brand: string;
    category: string;
    images: string[];
    price: {
        amount: number;
        currency: string;
    };
    reviews: {
        rating: number;
        count: number;
    };
    dropshipEligible: boolean;
    commission?: {
        amount: number;
    };
}

export interface SellerInventoryItem {
    sku: string;
    asin: string;
    productName: string;
    quantity: number;
    price: number;
}

export const mockDropshipProducts: AmazonProduct[] = [
    {
        asin: 'B08N5KWB9H',
        title: 'Sony WH-1000XM4 Wireless Noise Canceling Overhead Headphones',
        brand: 'Sony',
        category: 'electronics',
        images: ['/placeholder-headphone.jpg'],
        price: { amount: 348.00, currency: 'USD' },
        reviews: { rating: 4.8, count: 25400 },
        dropshipEligible: true,
        commission: { amount: 34.80 }
    },
    {
        asin: 'B09G3F5G2P',
        title: 'Advanced Yoga Mat 1/4 inch Thick',
        brand: 'Gaiam',
        category: 'sports-outdoors',
        images: ['/placeholder-yoga.jpg'],
        price: { amount: 29.99, currency: 'USD' },
        reviews: { rating: 4.6, count: 12500 },
        dropshipEligible: true,
        commission: { amount: 5.00 }
    }
];

// Types
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
    platforms: {
        [key: string]: {
            status: string;
        };
    };
}

// Service
export const productListingService = {
    getAvailablePlatforms: (): ListingPlatform[] => [
        {
            id: 'medusajs',
            name: 'MedusaJS Store',
            enabled: true,
            fees: { listingFee: 0, commissionRate: 0.0, fulfillmentFee: 5.0 }
        },
        {
            id: 'amazon',
            name: 'Amazon Marketplace',
            enabled: false,
            fees: { listingFee: 39.99, commissionRate: 0.15, fulfillmentFee: 3.5 }
        },
        {
            id: 'flipkart',
            name: 'Flipkart',
            enabled: false,
            fees: { listingFee: 0, commissionRate: 0.12, fulfillmentFee: 2.0 }
        }
    ],

    createListing: async (product: AmazonProduct, platforms: string[], markup: number): Promise<ProductListing> => {
        const cost = product.price.amount;
        const sellingPrice = cost * (1 + markup);
        const margin = sellingPrice - cost; // Simplified

        return {
            id: `listing_${product.asin}_${Date.now()}`,
            title: product.title,
            sourceAsin: product.asin,
            price: {
                selling: sellingPrice,
                margin: margin
            },
            platforms: platforms.reduce((acc, p) => ({
                ...acc,
                [p]: { status: 'pending' }
            }), {})
        };
    },

    calculateProfitMargins: (cost: number, markup: number) => {
        const platforms = ['MedusaJS', 'Amazon', 'Flipkart'];
        const sellingPrice = cost * (1 + markup);

        return platforms.map(p => ({
            platform: p,
            sellingPrice,
            profit: sellingPrice - cost - (p === 'Amazon' ? sellingPrice * 0.15 : 0),
            profitMargin: Math.round(((sellingPrice - cost) / sellingPrice) * 100)
        }));
    }
};

export const amazonSPAPI = new AmazonSPAPI();
