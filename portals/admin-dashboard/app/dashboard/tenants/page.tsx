'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Building2, Plus, Search, MoreVertical, Globe, Users, RefreshCw } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { PageHeader } from '@/components/dashboard/PageHeader';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { adminApi } from '@/lib/api/admin';
import { toast } from 'sonner';

export default function TenantsPage() {
    const [tenants, setTenants] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
    const [newTenant, setNewTenant] = useState({ name: '', domain: '', slug: '' });

    const loadTenants = async () => {
        setLoading(true);
        try {
            const res = await adminApi.getTenants();
            if (res.data && Array.isArray(res.data)) {
                setTenants(res.data);
            } else {
                setTenants([]);
                console.error("Invalid tenants data format:", res.data);
            }
        } catch (error) {
            toast.error("Failed to load tenants");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadTenants();
    }, []);

    const handleCreateTenant = async () => {
        toast.info("Tenant creation is handled via the onboarding workflow.");
        setIsCreateModalOpen(false);
    };

    const filteredTenants = tenants.filter(tenant =>
        tenant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        tenant.domain?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="p-6 space-y-6 bg-slate-50 dark:bg-slate-950 min-h-full">
            <PageHeader
                title={
                    <>Tenant <span className="text-indigo-600">Management</span></>
                }
                description="Manage multi-tenant organizations and their infrastructure."
            >
                <Button onClick={loadTenants} variant="outline" disabled={loading}>
                    <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Refresh
                </Button>
                <Button onClick={() => setIsCreateModalOpen(true)} className="bg-blue-600 hover:bg-blue-700">
                    <Plus className="mr-2 h-4 w-4" /> New Tenant
                </Button>
            </PageHeader>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle>Organizations</CardTitle>
                            <CardDescription>A list of all active tenants on the platform.</CardDescription>
                        </div>
                        <div className="relative w-64">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search tenants..."
                                className="pl-8"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {loading ? (
                            <div className="flex justify-center p-8">
                                <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
                            </div>
                        ) : filteredTenants.length === 0 ? (
                            <div className="text-center p-8 text-muted-foreground">
                                No tenants found.
                            </div>
                        ) : (
                            filteredTenants.map((tenant) => (
                                <div key={tenant.id} className="flex items-center justify-between p-4 border rounded-xl bg-white dark:bg-slate-900 shadow-sm hover:shadow-md transition-shadow group">
                                    <Link href={`/dashboard/tenants/${tenant.id}`} className="flex-1 flex items-center gap-4 cursor-pointer">
                                        <div className="w-12 h-12 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                                            <Building2 className="h-6 w-6" />
                                        </div>
                                        <div>
                                            <h3 className="font-bold text-lg group-hover:text-blue-600 transition-colors">{tenant.name}</h3>
                                            <div className="flex items-center gap-2 text-sm text-muted-foreground">
                                                <Globe className="h-3 w-3" /> {tenant.domain || 'no-domain'}
                                                <span className="mx-1">•</span>
                                                <Users className="h-3 w-3" /> {tenant.users_count || 0} Users
                                            </div>
                                        </div>
                                    </Link>
                                    <div className="flex items-center gap-4">
                                        <Badge variant={tenant.status === 'active' ? 'default' : 'secondary'}>
                                            {(tenant.status || 'active').toUpperCase()}
                                        </Badge>
                                        <div className="text-right hidden sm:block">
                                            <p className="text-sm font-medium">{tenant.plan || 'Free'}</p>
                                            <p className="text-xs text-muted-foreground">Plan Status</p>
                                        </div>
                                        <Button variant="ghost" size="icon">
                                            <MoreVertical className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </CardContent>
            </Card>

            {/* Create Tenant Modal */}
            <Dialog open={isCreateModalOpen} onOpenChange={setIsCreateModalOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Create New Tenant</DialogTitle>
                        <DialogDescription>
                            Initialize a new organization on the BizOSaaS platform.
                        </DialogDescription>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Organization Name</label>
                            <Input
                                placeholder="e.g. Acme Corp"
                                value={newTenant.name}
                                onChange={(e) => setNewTenant({ ...newTenant, name: e.target.value })}
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Primary Domain</label>
                            <Input
                                placeholder="e.g. acme.com"
                                value={newTenant.domain}
                                onChange={(e) => setNewTenant({ ...newTenant, domain: e.target.value })}
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Unique Slug</label>
                            <Input
                                placeholder="e.g. acme-corp"
                                value={newTenant.slug}
                                onChange={(e) => setNewTenant({ ...newTenant, slug: e.target.value })}
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsCreateModalOpen(false)}>Cancel</Button>
                        <Button onClick={handleCreateTenant}>Create Organization</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}
