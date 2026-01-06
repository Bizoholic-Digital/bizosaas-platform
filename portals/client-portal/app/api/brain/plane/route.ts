
import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';

// This API route acts as a proxy to the Plane API to avoid CORS issues and hide tokens
export async function GET(req: NextRequest) {
    try {
        const PLANE_API_URL = process.env.PLANE_API_URL || 'https://plane.bizoholic.net/api/v1';
        const PLANE_API_TOKEN = process.env.PLANE_API_TOKEN;
        const WORKSPACE_SLUG = process.env.PLANE_WORKSPACE_SLUG || 'bizosaas';

        // We can use the session for RBAC if needed, but for now we use a system token
        // const session = await getServerSession(authOptions);
        // if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

        if (!PLANE_API_TOKEN) {
            console.warn('PLANE_API_TOKEN is not defined, switching to mock mode.');
            // throw new Error('Mock Mode'); // Throwing error to catch block to return mock data
        }

        // Forward query params? (e.g. project filters)
        const url = new URL(`${PLANE_API_URL}/workspaces/${WORKSPACE_SLUG}/projects/`);

        // Add fake project data if Plane is not actually connected yet (Fallback)
        // REMOVE THIS BLOCK when Plane is live
        try {
            if (!PLANE_API_TOKEN) throw new Error('Mock Mode');
            const response = await fetch(url.toString(), {
                headers: {
                    'X-Api-Key': PLANE_API_TOKEN,
                    'Content-Type': 'application/json',
                },
                next: { revalidate: 60 } // Cache for 1 min
            });

            if (!response.ok) {
                console.warn(`Plane API returned ${response.status}: ${await response.text()}`);
                throw new Error(`Plane API error: ${response.status}`);
            }

            const data = await response.json();
            return NextResponse.json(data);
        } catch (e) {
            console.warn('Plane API unreachable, returning mock data for demo purposes:', e);
            // Fallback Mock Data as requested by user ("create some dummy projects")
            return NextResponse.json({
                results: [
                    { id: '1', name: 'Website Redesign', identifier: 'WEB', state: 'In Progress' },
                    { id: '2', name: 'Q1 Marketing Campaign', identifier: 'MKT', state: 'Planning' },
                    { id: '3', name: 'Mobile App Launch', identifier: 'APP', state: 'Backlog' },
                    { id: '4', name: 'SEO Audit', identifier: 'SEO', state: 'Completed' },
                ]
            });
        }

    } catch (error: any) {
        console.error('Plane Proxy Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
