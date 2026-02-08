import { brainApi } from './brain-api';

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
    content?: string;
    status?: string;
    published_at?: string;
    content_blocks: ContentBlock[];
    meta_description?: string;
}

const getPage = async (slug: string): Promise<CMSPage | null> => {
    try {
        const pages = await brainApi.cms.getPages();
        const page = pages.find((p: any) => p.slug === slug) || null;
        if (page) {
            return {
                ...page,
                content_blocks: page.content_blocks || []
            };
        }
        return null;
    } catch (e) {
        console.error('Failed to fetch page', e);
        return null;
    }
};

const getContentPages = async (limit: number = 10): Promise<CMSPage[]> => {
    try {
        const pages = await brainApi.cms.getPages();
        return (pages || []).slice(0, limit).map((p: any) => ({
            ...p,
            content_blocks: p.content_blocks || []
        }));
    } catch (e) {
        console.error('Failed to fetch pages', e);
        return [];
    }
};

export const useWagtailPage = (slug: string) => {
    // This could be a real hook, but for now maintaining the structure
    return { page: null, loading: false, error: null };
};

export const useWagtailContentPages = (limit: number = 10) => {
    // Maintaining the structure for dashboard compatibility
    return { pages: [], loading: false, error: null };
};

export const wagtailCMS = {
    getPage,
    getContentPages,
    useWagtailPage
};

export default wagtailCMS;
