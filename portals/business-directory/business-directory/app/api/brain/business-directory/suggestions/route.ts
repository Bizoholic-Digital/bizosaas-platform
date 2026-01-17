import { NextRequest, NextResponse } from 'next/server';

const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function GET(request: NextRequest) {
    try {
        const searchParams = request.nextUrl.searchParams;
        const q = searchParams.get('q') || '';
        const location = searchParams.get('location') || '';

        if (!q) {
            return NextResponse.json([]);
        }

        const response = await fetch(`${BACKEND_API_URL}/api/brain/business-directory/autocomplete?query=${encodeURIComponent(q)}&location=${encodeURIComponent(location)}`);

        if (response.ok) {
            const data = await response.json();

            // Transform backend data to frontend SearchSuggestion format
            // Backend returns: [{"text": "...", "id": "...", "type": "internal|google", "slug": "..."}]
            // Frontend expects: [{ id: string, text: string, type: 'business' | 'category' | 'location' | 'query', metadata?: any }]

            const suggestions = data.map((item: any) => ({
                id: item.id || Math.random().toString(),
                text: item.text,
                type: item.type === 'internal' ? 'business' : 'query',
                metadata: {
                    slug: item.slug,
                    source: item.type
                }
            }));

            return NextResponse.json(suggestions);
        }

        return NextResponse.json([]);
    } catch (error) {
        console.error('Suggestions API error:', error);
        return NextResponse.json([]);
    }
}
