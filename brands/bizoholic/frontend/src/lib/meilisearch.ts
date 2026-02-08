export interface BusinessListing {
    id: string;
    name: string;
    description: string;
    category: string;
    rating: number;
    reviews: number;
    address: string;
    phone: string;
    hours: string;
    website?: string;
    verified?: boolean;
    premium?: boolean;
    aiEnhanced?: boolean;
    tags?: string[];
}

export const mockBusinessListings: BusinessListing[] = [
    {
        id: "1",
        name: "Zest & Spice",
        description: "Modern fusion restaurant specializing in locally sourced ingredients and artisanal cocktails.",
        category: "Restaurants",
        rating: 4.8,
        reviews: 124,
        address: "123 Culinary Ave, Foodville",
        phone: "(555) 123-4567",
        hours: "11:00 AM - 10:00 PM",
        website: "https://zestandspice.com",
        verified: true,
        premium: true,
        aiEnhanced: true,
        tags: ["Fusion", "Locally Sourced", "Cocktails"]
    },
    {
        id: "2",
        name: "TechNova Solutions",
        description: "Custom software development and IT consulting for small to medium-sized businesses.",
        category: "Technology",
        rating: 4.5,
        reviews: 56,
        address: "456 Innovation Way, Silicon Valley",
        phone: "(555) 987-6543",
        hours: "9:00 AM - 6:00 PM",
        website: "https://technova.io",
        verified: true,
        premium: false,
        aiEnhanced: true,
        tags: ["Software", "Consulting", "IT"]
    }
];

export async function initializeMeilisearch() {
    console.log("Meilisearch initialized (mock)");
    return true;
}

export async function searchBusinesses(params: any) {
    console.log("Searching businesses (mock)", params);
    return {
        hits: mockBusinessListings,
        totalHits: mockBusinessListings.length,
        processingTimeMs: 12
    };
}

export async function getBusinessFacets() {
    return {
        category: {
            "Restaurants": 45,
            "Technology": 32,
            "Retail": 28
        }
    };
}

export async function getBusinessSuggestions(query: string) {
    return mockBusinessListings
        .filter(b => b.name.toLowerCase().includes(query.toLowerCase()))
        .map(b => ({
            id: b.id,
            name: b.name,
            category: b.category,
            highlighted: b.name.replace(new RegExp(query, 'gi'), (match) => `<b>${match}</b>`)
        }));
}

export async function indexBusinessListings(listings: BusinessListing[]) {
    console.log(`Indexing ${listings.length} listings (mock)`);
    return true;
}
