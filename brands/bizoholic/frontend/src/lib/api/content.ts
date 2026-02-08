import { getSession } from 'next-auth/react';

const API_BASE = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8000';

export interface Page {
    id: string;
    title: string;
    slug: string;
    content: string;
    status: string;
    published_at?: string;
    updated_at?: string;
    author?: string;
}

export interface Post {
    id: string;
    title: string;
    slug: string;
    content: string;
    excerpt?: string;
    status: string;
    published_at?: string;
    author?: string;
}

async function getAuthHeader(): Promise<HeadersInit> {
    // Client-side session fetching
    // For server-side, this needs to be passed in or handled differently
    return {};
}

export async function getPages(): Promise<Page[]> {
    const res = await fetch(`${API_BASE}/api/cms/pages`, {
        headers: {
            'Content-Type': 'application/json',
            // Auth handling needed here
        }
    });
    if (!res.ok) throw new Error('Failed to fetch pages');
    return res.json();
}

export async function getPage(slug: string): Promise<Page | null> {
    // The CMS API returns list, we filter or if it supports slug query
    // app/api/cms.py endpoint `list_pages` returns all.
    // It doesn't seem to have `get_page_by_slug` endpoint exposed directly in the router!
    // It has `create_page` and `update_page`.
    // Wait, step 5870 line 116 is list_pages.
    // There is no `get_page(slug)` endpoint in cms.py!
    // There IS `list_pages`.

    // I should create get_page endpoint in cms.py if I want efficiency.
    // For now, fetch all and find? (Inefficient but works for small sites)
    const pages = await getPages();
    return pages.find(p => p.slug === slug) || null;
}
