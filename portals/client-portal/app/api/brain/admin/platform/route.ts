/**
 * Super Admin Platform Monitoring API Route
 * Provides system-wide metrics and monitoring
 * Only accessible by super_admin role
 */

import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// GET - Get platform metrics
export async function GET(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        // Check if user is super admin
        if (!session?.access_token || session.user?.role !== 'super_admin') {
            return NextResponse.json(
                { error: 'Forbidden - Super Admin access required' },
                { status: 403 }
            );
        }

        const searchParams = request.nextUrl.searchParams;
        const params = new URLSearchParams();

        // Time range for metrics
        if (searchParams.get('from')) params.set('from', searchParams.get('from')!);
        if (searchParams.get('to')) params.set('to', searchParams.get('to')!);
        if (searchParams.get('interval')) params.set('interval', searchParams.get('interval')!); // hour, day, week

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/admin/platform/metrics?${params.toString()}`,
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
        //   overview: {
        //     total_tenants: 45,
        //     active_tenants: 42,
        //     total_users: 1234,
        //     active_users: 892,
        //     total_api_calls: 1500000,
        //     avg_response_time: "245ms",
        //     error_rate: "0.12%",
        //     uptime: "99.98%"
        //   },
        //   services: {
        //     django_crm: { status: "healthy", response_time: "120ms" },
        //     saleor: { status: "healthy", response_time: "180ms" },
        //     wagtail: { status: "healthy", response_time: "95ms" },
        //     ai_service: { status: "healthy", response_time: "340ms" }
        //   },
        //   resources: {
        //     cpu_usage: "45%",
        //     memory_usage: "62%",
        //     disk_usage: "38%",
        //     database_connections: 45,
        //     cache_hit_rate: "94.5%"
        //   },
        //   ai_agents: {
        //     total_agents: 93,
        //     active_agents: 89,
        //     total_requests: 45000,
        //     avg_processing_time: "1.8s"
        //   },
        //   trends: {
        //     api_calls: [...], // Time series data
        //     response_times: [...],
        //     error_rates: [...],
        //     user_activity: [...]
        //   }
        // }

        return NextResponse.json(data);

    } catch (error) {
        console.error('Platform metrics error:', error);
        return NextResponse.json(
            { error: 'Failed to fetch platform metrics' },
            { status: 500 }
        );
    }
}
