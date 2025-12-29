'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Building2, Plus, Search, MoreVertical, Globe, Users, ShieldCheck } from 'lucide-react';
import { Input } from '@/components/ui/input';

export default function TenantsPage() {
    const tenants = [
        { id: '1', name: 'Bizoholic Digital', domain: 'bizoholic.net', users: 12, status: 'active', plan: 'Enterprise' },
        { id: '2', name: 'Corel Dove', domain: 'coreldove.com', users: 5, status: 'active', plan: 'Pro' },
        { id: '3', name: 'Staging Lab', domain: 'staging.bizosaas.com', users: 2, status: 'maintenance', plan: 'Developer' },
    ];

    return (
        <div className="p-6 space-y-6 bg-slate-50 dark:bg-slate-950 min-h-full">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Tenant Management</h1>
                    <p className="text-muted-foreground">Manage multi-tenant organizations and their infrastructure.</p>
                </div>
                <Button className="bg-blue-600 hover:bg-blue-700">
                    <Plus className="mr-2 h-4 w-4" /> New Tenant
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle>Organizations</CardTitle>
                            <CardDescription>A list of all active tenants on the platform.</CardDescription>
                        </div>
                        <div className="relative w-64">
                            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input placeholder="Search tenants..." className="pl-8" />
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {tenants.map((tenant) => (
                            <div key={tenant.id} className="flex items-center justify-between p-4 border rounded-xl bg-white dark:bg-slate-900 shadow-sm hover:shadow-md transition-shadow">
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600">
                                        <Building2 className="h-6 w-6" />
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-lg">{tenant.name}</h3>
                                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                                            <Globe className="h-3 w-3" /> {tenant.domain}
                                            <span className="mx-1">•</span>
                                            <Users className="h-3 w-3" /> {tenant.users} Users
                                        </div>
                                    </div>
                                </div>
                                <div className="flex items-center gap-4">
                                    <Badge variant={tenant.status === 'active' ? 'default' : 'secondary'}>
                                        {tenant.status.toUpperCase()}
                                    </Badge>
                                    <div className="text-right hidden sm:block">
                                        <p className="text-sm font-medium">{tenant.plan}</p>
                                        <p className="text-xs text-muted-foreground">Plan Status</p>
                                    </div>
                                    <Button variant="ghost" size="icon">
                                        <MoreVertical className="h-4 w-4" />
                                    </Button>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
