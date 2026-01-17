import { NextRequest, NextResponse } from 'next/server';
import { transformBusinessData } from '@/lib/business-hours-transformer';

// Backend API configuration
const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function GET(
    request: NextRequest,
    { params }: { params: { slug: string } }
) {
    const slug = params.slug;

    try {
        const backendUrl = `${BACKEND_API_URL}/api/brain/business-directory/businesses/${slug}`;
        console.log(`[BUSINESS-DIRECTORY] GET business by slug: ${backendUrl}`);

        try {
            const response = await fetch(backendUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Business-Directory-Frontend/1.0.0'
                },
            });

            if (response.ok) {
                let data = await response.json();
                console.log(`[BUSINESS-DIRECTORY] Backend success for slug: ${slug}`);

                // Transform business hours data for frontend compatibility
                data = transformBusinessData(data);

                return NextResponse.json(data);
            } else {
                console.warn(`[BUSINESS-DIRECTORY] Backend error for slug ${slug}: ${response.status}`);
                return NextResponse.json(
                    { error: 'Business not found' },
                    { status: 404 }
                );
            }
        } catch (backendError) {
            console.error(`[BUSINESS-DIRECTORY] Backend connection failed for slug ${slug}:`, backendError);

            // Attempt fallback from mock data if needed (optional)
            // For now, let's just return 404 if backend is down and we don't have a robust mock strategy for single businesses
            return NextResponse.json(
                { error: 'Service Unavailable', details: backendError.message },
                { status: 503 }
            );
        }
    } catch (error) {
        console.error('[BUSINESS-DIRECTORY] API proxy error:', error);
        return NextResponse.json(
            { error: 'Internal server error', details: error.message },
            { status: 500 }
        );
    }
}
