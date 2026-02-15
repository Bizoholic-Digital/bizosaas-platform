/**
 * AI Agents API Route
 * Lists available AI agents and their capabilities
 * Provides agent selection and configuration
 */

import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth/auth-options";

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// GET - List all available AI agents
export async function GET(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        if (!session?.access_token) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        const searchParams = request.nextUrl.searchParams;
        const params = new URLSearchParams();

        // Filter by category
        if (searchParams.get('category')) {
            params.set('category', searchParams.get('category')!);
        }

        // Filter by capability
        if (searchParams.get('capability')) {
            params.set('capability', searchParams.get('capability')!);
        }

        // Include user role for permission-based filtering
        params.set('user_role', session.user?.role || 'user');

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/ai/agents?${params.toString()}`,
            {
                headers,
                cache: 'no-store'
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: response.status });
        }

        const data = await response.json();

        // Response format:
        // {
        //   agents: [
        //     {
        //       id: "crm_lead_scorer",
        //       name: "Lead Scoring Agent",
        //       category: "crm",
        //       description: "Analyzes and scores leads based on behavior",
        //       capabilities: ["analyze", "predict", "score"],
        //       status: "active",
        //       usage_count: 1234,
        //       avg_response_time: "1.2s"
        //     },
        //     ...
        //   ],
        //   total: 93,
        //   categories: ["crm", "ecommerce", "analytics", "content", "automation"]
        // }

        return NextResponse.json(data);

    } catch (error) {
        console.error('AI Agents GET error:', error);
        return NextResponse.json(
            { error: 'Failed to fetch AI agents' },
            { status: 500 }
        );
    }
}
