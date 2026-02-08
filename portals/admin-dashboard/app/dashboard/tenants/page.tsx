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
    const [isManageModalOpen, setIsManageModalOpen] = useState(false);
    const [selectedTenant, setSelectedTenant] = useState<any>(null);
    const [onboardingStats, setOnboardingStats] = useState<any>(null);
    const [newTenant, setNewTenant] = useState({ name: '', domain: '', slug: '' });
    const [isSaving, setIsSaving] = useState(false);

    // Bulk Actions
    const [selectedTenantIds, setSelectedTenantIds] = useState<string[]>([]);

    const toggleTenantSelection = (id: string) => {
        setSelectedTenantIds(prev =>
            prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
        );
    };

    const handleBulkAction = async (action: 'suspend' | 'activate' | 'maintenance') => {
        if (!confirm(`Are you sure you want to ${action} ${selectedTenantIds.length} tenants?`)) return;

        setLoading(true);
        try {
            await adminApi.bulkTenantAction(selectedTenantIds, action);
            toast.success(`Bulk ${action} successful`);
            setSelectedTenantIds([]);
            loadData();
        } catch (error) {
            toast.error("Bulk action failed");
            setLoading(false);
        }
    };

    const loadData = async () => {
        setLoading(true);
        try {
            const [tenantsRes, statsRes] = await Promise.all([
                adminApi.getTenants(),
                adminApi.getOnboardingStats()
            ]);

            if (tenantsRes.data?.tenants) {
                setTenants(tenantsRes.data.tenants);
            } else if (Array.isArray(tenantsRes.data)) {
                setTenants(tenantsRes.data);
            }

            if (statsRes.data) {
                setOnboardingStats(statsRes.data);
            }
        } catch (error) {
            toast.error("Failed to sync tenant environment");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const [activeModalTab, setActiveModalTab] = useState<'config' | 'analytics'>('config');
    const [analyticsData, setAnalyticsData] = useState<any>(null);

    const handleManageTenant = async (tenant: any) => {
        setLoading(true);
        setActiveModalTab('config');
        setAnalyticsData(null);
        try {
            const res = await adminApi.getTenantDetails(tenant.id);
            if (res.data) {
                setSelectedTenant(res.data);
                setIsManageModalOpen(true);
            }
        } catch (error) {
            toast.error("Failed to load tenant configuration");
        } finally {
            setLoading(false);
        }
    };

    const handleLoadAnalytics = async () => {
        if (!selectedTenant || analyticsData) return;
        setLoading(true);
        try {
            const res = await adminApi.getTenantAnalytics(selectedTenant.id);
            if (res.data) {
                setAnalyticsData(res.data);
            }
        } catch (error) {
            console.error("Failed to load analytics:", error);
            toast.error("Failed to load usage analytics");
        } finally {
            setLoading(false);
        }
    };

    const handleSaveConfig = async () => {
        if (!selectedTenant) return;
        setIsSaving(true);
        try {
            await adminApi.updateTenantConfig(selectedTenant.id, {
                status: selectedTenant.status,
                limits: selectedTenant.limits,
                features: selectedTenant.features
            });
            toast.success("Identity configuration synchronized");
            setIsManageModalOpen(false);
            loadData();
        } catch (error) {
            toast.error("Failed to update namespace configuration");
        } finally {
            setIsSaving(false);
        }
    };

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
                <Button onClick={loadData} variant="outline" disabled={loading} className="rounded-xl font-bold">
                    <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Sync Nodes
                </Button>
                <Button onClick={() => setIsCreateModalOpen(true)} className="bg-blue-600 hover:bg-blue-700 rounded-xl font-bold shadow-lg shadow-blue-500/20">
                    <Plus className="mr-2 h-4 w-4" /> Provision Namespace
                </Button>
            </PageHeader>

            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm overflow-hidden relative">
                    <div className="absolute top-0 right-0 p-4 opacity-10"><Building2 className="h-12 w-12" /></div>
                    <CardContent className="p-6">
                        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Active Nodes</p>
                        <h3 className="text-2xl font-black mt-1">{tenants.length}</h3>
                        <p className="text-[10px] text-green-500 font-bold mt-1">Status: Stable</p>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-6">
                        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Onboarding Rate</p>
                        <h3 className="text-2xl font-black mt-1">{onboardingStats?.completion_rate?.toFixed(1) || 0}%</h3>
                        <div className="w-full bg-gray-100 dark:bg-gray-800 h-1.5 rounded-full mt-2 overflow-hidden">
                            <div className="bg-blue-600 h-full transition-all duration-1000" style={{ width: `${onboardingStats?.completion_rate || 0}%` }} />
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-6">
                        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Marketplace Apps</p>
                        <h3 className="text-2xl font-black mt-1">482</h3>
                        <p className="text-[10px] text-blue-500 font-bold mt-1">↑ 12% from last cycle</p>
                    </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-indigo-600 to-blue-700 text-white border-none shadow-xl shadow-blue-500/20">
                    <CardContent className="p-6">
                        <p className="text-[10px] font-black text-blue-200 uppercase tracking-widest">Identity Pool</p>
                        <h3 className="text-2xl font-black mt-1">{tenants.reduce((acc, t) => acc + (t.user_count || 0), 0)}</h3>
                        <p className="text-[10px] text-blue-100 font-bold mt-1">Cross-tenant verified users</p>
                    </CardContent>
                </Card>
            </div>

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

                    {selectedTenantIds.length > 0 && (
                        <div className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl flex items-center justify-between border border-blue-100 dark:border-blue-800 animate-in fade-in slide-in-from-top-2">
                            <span className="text-sm font-bold text-blue-700 dark:text-blue-300">{selectedTenantIds.length} tenants selected</span>
                            <div className="flex gap-2">
                                <Button size="sm" variant="outline" className="bg-white hover:text-green-600 font-bold" onClick={() => handleBulkAction('activate')}>Activate</Button>
                                <Button size="sm" variant="outline" className="bg-white hover:text-orange-600 font-bold" onClick={() => handleBulkAction('maintenance')}>Maintenance</Button>
                                <Button size="sm" variant="outline" className="bg-white hover:text-red-600 font-bold" onClick={() => handleBulkAction('suspend')}>Suspend</Button>
                                <Button size="sm" variant="ghost" className="text-gray-500" onClick={() => setSelectedTenantIds([])}>Clear</Button>
                            </div>
                        </div>
                    )}

                    <div className="space-y-4">
                        {loading && !isManageModalOpen ? (
                            <div className="flex justify-center p-8">
                                <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
                            </div>
                        ) : filteredTenants.length === 0 ? (
                            <div className="text-center p-8 text-muted-foreground">
                                No tenants found.
                            </div>
                        ) : (
                            filteredTenants.map((tenant) => (
                                <div key={tenant.id} className={`flex items-center justify-between p-4 border rounded-2xl transition-all shadow-sm hover:shadow-md group ${selectedTenantIds.includes(tenant.id) ? 'bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800' : 'bg-white border-gray-100 dark:bg-slate-900 dark:border-gray-800'}`}>
                                    <div className="flex-1 flex items-center gap-4">
                                        <div className="pl-2">
                                            <input
                                                type="checkbox"
                                                className="w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                                                checked={selectedTenantIds.includes(tenant.id)}
                                                onChange={() => toggleTenantSelection(tenant.id)}
                                            />
                                        </div>
                                        <div className="w-12 h-12 rounded-xl bg-blue-50 dark:bg-blue-900/20 flex items-center justify-center text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-all shadow-sm">
                                            <Building2 className="h-6 w-6" />
                                        </div>
                                        <div>
                                            <div className="flex items-center gap-2">
                                                <h3 className="font-black text-gray-900 dark:text-white uppercase tracking-tight">{tenant.name}</h3>
                                                {tenant.onboarding_completed && (
                                                    <Badge className="bg-green-500/10 text-green-600 border-none text-[8px] font-black px-1.5 h-4">VERIFIED</Badge>
                                                )}
                                            </div>
                                            <div className="flex items-center gap-4 text-[11px] font-bold text-gray-400">
                                                <span className="flex items-center gap-1"><Globe className="h-3 w-3" /> {tenant.domain || 'internal.bizo.local'}</span>
                                                <span className="flex items-center gap-1"><Users className="h-3 w-3" /> {tenant.user_count || 0} Assets</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-4">
                                        <Badge variant="outline" className={`font-black text-[10px] border-none px-2 py-0.5 ${tenant.status === 'active' ? 'bg-green-100 text-green-700' :
                                            tenant.status === 'trial' ? 'bg-blue-100 text-blue-700' : 'bg-red-100 text-red-700'
                                            }`}>
                                            {(tenant.status || 'active').toUpperCase()}
                                        </Badge>
                                        <div className="text-right hidden sm:block mr-2">
                                            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Cluster Plan</p>
                                            <p className="text-xs font-bold text-gray-900 dark:text-gray-100">{tenant.subscription || 'Free'}</p>
                                        </div>
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            className="rounded-xl font-bold text-blue-600 hover:bg-blue-50"
                                            onClick={() => handleManageTenant(tenant)}
                                        >
                                            MANAGE
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

            {/* Manage Tenant Modal */}
            <Dialog open={isManageModalOpen} onOpenChange={setIsManageModalOpen}>
                <DialogContent className="max-w-2xl border-none shadow-2xl bg-white dark:bg-gray-950 p-0 rounded-3xl overflow-hidden min-h-[500px]">
                    <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 text-white relative">
                        <div className="absolute top-0 right-0 p-8 opacity-10"><Building2 className="h-24 w-24" /></div>
                        <DialogHeader className="relative z-10 text-left">
                            <DialogTitle className="text-2xl font-black uppercase tracking-tight">Node: {selectedTenant?.name}</DialogTitle>
                            <DialogDescription className="text-blue-100 border-none">
                                Operational configuration and analytics for this namespace.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="flex space-x-4 mt-6">
                            <button
                                onClick={() => setActiveModalTab('config')}
                                className={`text-xs font-black uppercase tracking-widest pb-2 border-b-2 transition-colors ${activeModalTab === 'config' ? 'border-white text-white' : 'border-transparent text-blue-200 hover:text-white'}`}
                            >
                                Configuration
                            </button>
                            <button
                                onClick={() => { setActiveModalTab('analytics'); handleLoadAnalytics(); }}
                                className={`text-xs font-black uppercase tracking-widest pb-2 border-b-2 transition-colors ${activeModalTab === 'analytics' ? 'border-white text-white' : 'border-transparent text-blue-200 hover:text-white'}`}
                            >
                                Analytics
                            </button>
                        </div>
                    </div>

                    <div className="p-8">
                        {activeModalTab === 'config' && (
                            <div className="space-y-6">
                                <div className="grid grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <p className="text-[10px] font-black uppercase tracking-widest text-gray-400">Operational Status</p>
                                        <select
                                            className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-800 rounded-2xl font-bold text-sm outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                                            value={selectedTenant?.status}
                                            onChange={(e) => setSelectedTenant({ ...selectedTenant, status: e.target.value })}
                                        >
                                            <option value="active">ACTIVE (OPERATIONAL)</option>
                                            <option value="suspended">SUSPENDED (LOCKOUT)</option>
                                            <option value="trial">TRIAL (LIMITED)</option>
                                            <option value="maintenance">MAINTENANCE</option>
                                        </select>
                                    </div>

                                    <div className="space-y-2">
                                        <p className="text-[10px] font-black uppercase tracking-widest text-gray-400">Identity Limit (Max Users)</p>
                                        <Input
                                            type="number"
                                            className="rounded-2xl h-11 font-bold"
                                            value={selectedTenant?.limits?.max_users}
                                            onChange={(e) => setSelectedTenant({
                                                ...selectedTenant,
                                                limits: { ...selectedTenant.limits, max_users: parseInt(e.target.value) }
                                            })}
                                        />
                                    </div>
                                </div>

                                <div className="space-y-3">
                                    <p className="text-[10px] font-black uppercase tracking-widest text-gray-400">Feature Entitlements</p>
                                    <div className="grid grid-cols-2 gap-3">
                                        {Object.keys(selectedTenant?.features || {}).map(f => (
                                            <div key={f} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800">
                                                <span className="text-xs font-black uppercase tracking-tight">{f.replace(/_/g, ' ')}</span>
                                                <input
                                                    type="checkbox"
                                                    className="h-5 w-5 rounded border-gray-300 text-blue-600"
                                                    checked={selectedTenant.features[f]}
                                                    onChange={(e) => setSelectedTenant({
                                                        ...selectedTenant,
                                                        features: { ...selectedTenant.features, [f]: e.target.checked }
                                                    })}
                                                />
                                            </div>
                                        ))}
                                        {Object.keys(selectedTenant?.features || {}).length === 0 && (
                                            <div className="col-span-2 text-center p-4 text-xs font-bold text-gray-400 bg-gray-50 rounded-2xl border border-dashed">
                                                No dynamic features configured for this cluster.
                                            </div>
                                        )}
                                    </div>
                                </div>

                                <div className="pt-4 flex gap-4">
                                    <Button variant="outline" className="flex-1 h-12 rounded-2xl font-bold" onClick={() => setIsManageModalOpen(false)}>
                                        Cancel
                                    </Button>
                                    <Button
                                        className="flex-1 h-12 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-2xl shadow-lg shadow-blue-500/20"
                                        onClick={handleSaveConfig}
                                        disabled={isSaving}
                                    >
                                        {isSaving ? <RefreshCw className="h-4 w-4 animate-spin" /> : "Sync Configuration"}
                                    </Button>
                                </div>
                            </div>
                        )}

                        {activeModalTab === 'analytics' && (
                            <div className="space-y-6">
                                {loading && !analyticsData ? (
                                    <div className="flex justify-center p-12">
                                        <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
                                    </div>
                                ) : !analyticsData ? (
                                    <div className="text-center p-8 text-gray-400">No analytics available</div>
                                ) : (
                                    <>
                                        <div className="grid grid-cols-2 gap-4">
                                            <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-2xl border border-blue-100 dark:border-blue-900/50">
                                                <p className="text-[10px] font-black uppercase tracking-widest text-blue-400">Active Users (30d)</p>
                                                <h3 className="text-2xl font-black text-blue-600 dark:text-blue-400 mt-1">
                                                    {analyticsData.user_engagement.active_users_30d}
                                                    <span className="text-xs text-blue-300 ml-1">/ {analyticsData.user_engagement.total_users}</span>
                                                </h3>
                                            </div>
                                            <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-2xl border border-purple-100 dark:border-purple-900/50">
                                                <p className="text-[10px] font-black uppercase tracking-widest text-purple-400">Total Sessions</p>
                                                <h3 className="text-2xl font-black text-purple-600 dark:text-purple-400 mt-1">{analyticsData.user_engagement.total_logins}</h3>
                                            </div>
                                        </div>

                                        <div className="space-y-3">
                                            <p className="text-[10px] font-black uppercase tracking-widest text-gray-400">Platform Utilization</p>
                                            <div className="bg-gray-50 dark:bg-gray-900 rounded-2xl p-4 border border-gray-100 dark:border-gray-800">
                                                <div className="flex justify-between mb-2">
                                                    <span className="text-xs font-bold">Feature Adoption</span>
                                                    <span className="text-xs font-bold">{analyticsData.feature_adoption.enabled_features} / {analyticsData.feature_adoption.total_available}</span>
                                                </div>
                                                <div className="w-full bg-gray-200 dark:bg-gray-800 h-2 rounded-full overflow-hidden">
                                                    <div
                                                        className="bg-green-500 h-full"
                                                        style={{ width: `${(analyticsData.feature_adoption.enabled_features / (analyticsData.feature_adoption.total_available || 1)) * 100}%` }}
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    </>
                                )}
                            </div>
                        )}
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    );
}
