
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';

// This API route acts as a proxy to the Plane API to avoid CORS issues and hide tokens
export async function GET(req: NextRequest) {
    try {
        const PLANE_API_URL = process.env.PLANE_API_URL || 'https://api.plane.so/api/v1';
        const PLANE_API_TOKEN = process.env.PLANE_API_TOKEN;
        const DEFAULT_WORKSPACE = process.env.PLANE_WORKSPACE_SLUG || 'bizosaas';
        const DEFAULT_PROJECT = '031b7a9e-ee6d-46f5-99da-8e9e911ae71d';

        // Check Clerk session
        const session = await auth();
        const userId = session?.user?.id;
        if (!userId) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

        const searchParams = req.nextUrl.searchParams;
        const workspaceSlug = searchParams.get('workspace') || DEFAULT_WORKSPACE;
        const projectId = searchParams.get('project') || DEFAULT_PROJECT;
        const fetchIssues = searchParams.get('type') === 'issues' || !!projectId;

        let url = `${PLANE_API_URL}/workspaces/${workspaceSlug}/projects/`;
        if (fetchIssues && projectId) {
            url = `${PLANE_API_URL}/workspaces/${workspaceSlug}/projects/${projectId}/issues/`;
        }

        if (!PLANE_API_TOKEN) {
            console.warn('PLANE_API_TOKEN is not defined, returning mock data.');
            return NextResponse.json({
                results: [
                    { id: '1', name: 'Website Redesign', identifier: 'WEB', state: 'In Progress' },
                    { id: '2', name: 'Q1 Marketing Campaign', identifier: 'MKT', state: 'Planning' },
                    { id: '3', name: 'Mobile App Launch', identifier: 'APP', state: 'Backlog' },
                ]
            });
        }

        const response = await fetch(url, {
            headers: {
                'X-Api-Key': PLANE_API_TOKEN as string,
                'Content-Type': 'application/json',
            },
            next: { revalidate: 60 } // Cache for 1 min
        });

        if (!response.ok) {
            const errorText = await response.text();
            return NextResponse.json({ error: errorText }, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data);
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}

export async function POST(req: NextRequest) {
    try {
        const PLANE_API_URL = process.env.PLANE_API_URL || 'https://api.plane.so/api/v1';
        const PLANE_API_TOKEN = process.env.PLANE_API_TOKEN;
        const DEFAULT_WORKSPACE = process.env.PLANE_WORKSPACE_SLUG || 'bizosaas';
        const DEFAULT_PROJECT = '031b7a9e-ee6d-46f5-99da-8e9e911ae71d';

        const session = await auth();
        const userId = session?.user?.id;
        if (!userId) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

        if (!PLANE_API_TOKEN) return NextResponse.json({ error: 'Token missing' }, { status: 500 });

        const body = await req.json();
        const workspaceSlug = body.workspace || DEFAULT_WORKSPACE;
        const projectId = body.project || DEFAULT_PROJECT;

        const url = `${PLANE_API_URL}/workspaces/${workspaceSlug}/projects/${projectId}/issues/`;

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-Api-Key': PLANE_API_TOKEN as string,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body.data || body)
        });

        const data = await response.json();
        return NextResponse.json(data, { status: response.status });
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}

export async function PATCH(req: NextRequest) {
    try {
        const PLANE_API_URL = process.env.PLANE_API_URL || 'https://api.plane.so/api/v1';
        const PLANE_API_TOKEN = process.env.PLANE_API_TOKEN;
        const DEFAULT_WORKSPACE = process.env.PLANE_WORKSPACE_SLUG || 'bizosaas';
        const DEFAULT_PROJECT = '031b7a9e-ee6d-46f5-99da-8e9e911ae71d';

        const session = await auth();
        const userId = session?.user?.id;
        if (!userId) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

        if (!PLANE_API_TOKEN) return NextResponse.json({ error: 'Token missing' }, { status: 500 });

        const body = await req.json();
        const workspaceSlug = body.workspace || DEFAULT_WORKSPACE;
        const projectId = body.project || DEFAULT_PROJECT;
        const issueId = body.issueId;

        if (!issueId) return NextResponse.json({ error: 'Issue ID missing' }, { status: 400 });

        const url = `${PLANE_API_URL}/workspaces/${workspaceSlug}/projects/${projectId}/issues/${issueId}/`;

        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'X-Api-Key': PLANE_API_TOKEN as string,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body.data || body)
        });

        const data = await response.json();
        return NextResponse.json(data, { status: response.status });
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}

export async function DELETE(req: NextRequest) {
    try {
        const PLANE_API_URL = process.env.PLANE_API_URL || 'https://api.plane.so/api/v1';
        const PLANE_API_TOKEN = process.env.PLANE_API_TOKEN;
        const DEFAULT_WORKSPACE = process.env.PLANE_WORKSPACE_SLUG || 'bizosaas';
        const DEFAULT_PROJECT = '031b7a9e-ee6d-46f5-99da-8e9e911ae71d';

        const session = await auth();
        const userId = session?.user?.id;
        if (!userId) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

        const searchParams = req.nextUrl.searchParams;
        const workspaceSlug = searchParams.get('workspace') || DEFAULT_WORKSPACE;
        const projectId = searchParams.get('project') || DEFAULT_PROJECT;
        const issueId = searchParams.get('issueId');

        if (!issueId) return NextResponse.json({ error: 'Issue ID missing' }, { status: 400 });

        const url = `${PLANE_API_URL}/workspaces/${workspaceSlug}/projects/${projectId}/issues/${issueId}/`;

        if (!PLANE_API_TOKEN) return NextResponse.json({ error: 'Token missing' }, { status: 500 });

        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-Api-Key': PLANE_API_TOKEN as string,
            }
        });

        return new NextResponse(null, { status: response.status });
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
