export interface PostMetadata {
    title: string;
    description?: string;
    date?: string;
    slug: string;
}

export interface Service extends PostMetadata {
    icon: string;
    features: string[];
}

export interface CaseStudy extends PostMetadata {
    client: string;
    industry: string;
    results: {
        metric: string;
        value: string;
    }[];
    testimonial?: {
        quote: string;
        author: string;
        role: string;
    };
}
