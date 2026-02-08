export interface ContentBlock {
    type: string;
    value: any;
}

export interface CallToActionBlock {
    title: string;
    description: string;
    button_text: string;
    button_url: string;
    button_style: 'primary' | 'secondary' | 'outline';
}

export interface FeatureBlock {
    title: string;
    description: string;
    icon?: string;
}

export interface TestimonialBlock {
    quote: string;
    author_name: string;
    author_title?: string;
    author_company?: string;
    author_image?: string;
    rating: number;
}

export interface StatsBlock {
    stat_number: string;
    stat_label: string;
    stat_description?: string;
}

export interface PricingBlock {
    plan_name: string;
    price: string;
    price_period: string;
    features: string[];
    is_popular: boolean;
    cta_text: string;
    cta_url: string;
}

export interface CMSPage {
    id: string;
    title: string;
    slug: string;
    content: string;
    status: string;
    published_at?: string;
    content_blocks: ContentBlock[];
    meta_description?: string;
}

// Alias for backward compatibility
export type WagtailPage = CMSPage;

class WordPressCMSClient {
    private apiBaseUrl: string;
    private tenantId: string;

    constructor() {
        this.apiBaseUrl = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'https://api.bizoholic.net';
        this.tenantId = 'bizoholic';
    }

    async getPage(slug: string): Promise<CMSPage | null> {
        try {
            // Centralized routing via Brain Gateway
            const response = await fetch(`${this.apiBaseUrl}/api/cms/pages?slug=${slug}`, {
                headers: {
                    'x-tenant-id': this.tenantId,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) return null;

            const pages = await response.json();
            if (pages && pages.length > 0) {
                const page = pages[0];
                // Ensure content_blocks exists for compatibility
                return {
                    ...page,
                    content_blocks: page.content_blocks || []
                };
            }
            return null;
        } catch (error) {
            console.error('CMS Error:', error);
            return null;
        }
    }

    async getContentPages(limit: number = 10): Promise<CMSPage[]> {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/cms/pages?limit=${limit}`, {
                headers: {
                    'x-tenant-id': this.tenantId,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) return [];

            const pages = await response.json();
            return (pages || []).map((p: any) => ({
                ...p,
                content_blocks: p.content_blocks || []
            }));
        } catch (error) {
            console.error('CMS Error:', error);
            return [];
        }
    }
}

export const cmsClient = new WordPressCMSClient();
// Maintain legacy export for compatibility
export const wagtailCMS = cmsClient;
