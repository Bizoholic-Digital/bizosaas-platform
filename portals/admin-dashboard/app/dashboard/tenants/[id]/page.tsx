'use client';

import React from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { ArrowLeft, Building2, Users, Settings, Database, Shield } from 'lucide-react';
// import { adminApi } from '@/lib/api/admin'; // TODO: Implement getTenant

export default function TenantDetailsPage() {
    const params = useParams();
    const router = useRouter();
    const tenantId = params.id as string;

    // TODO: Fetch real tenant details
    const tenant = {
        id: tenantId,
        name: 'Acme Corp',
        domain: 'acme.com',
        plan: 'Enterprise',
        status: 'active',
        users: 154,
        created_at: '2025-01-15'
    };

    return (
        <div className="p-6 space-y-6 bg-slate-50 dark:bg-slate-950 min-h-full">
            <div className="flex items-center gap-4 mb-8">
                <Button variant="ghost" size="icon" onClick={() => router.back()}>
                    <ArrowLeft className="w-5 h-5" />
                </Button>
                <div>
                    <h1 className="text-2xl font-bold tracking-tight">{tenant.name}</h1>
                    <p className="text-muted-foreground">Organization ID: {tenant.id}</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Users</CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{tenant.users}</div>
                        <p className="text-xs text-muted-foreground">+12% from last month</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Plan Status</CardTitle>
                        <Shield className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{tenant.plan}</div>
                        <p className="text-xs text-muted-foreground">Active until Dec 2026</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Database Usage</CardTitle>
                        <Database className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">2.4 GB</div>
                        <p className="text-xs text-muted-foreground">of 10 GB quota</p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Settings</CardTitle>
                    <CardDescription>Manage organization configuration</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="p-4 border rounded-lg bg-orange-50 dark:bg-orange-900/10 text-orange-800 dark:text-orange-200">
                        Detailed configuration and resource management coming soon.
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
