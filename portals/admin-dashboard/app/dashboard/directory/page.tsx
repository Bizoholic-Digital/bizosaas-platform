'use client';

import React, { useState, useEffect } from 'react';
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CardDescription
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import {
    Search,
    Building2,
    Globe,
    Activity,
    Users,
    ShieldCheck,
    Clock,
    MoreVertical,
    ExternalLink,
    MapPin,
    RefreshCw,
    PieChart,
    BarChart3,
    Sparkles
} from 'lucide-react';
import { PageHeader } from '@/components/dashboard/PageHeader';
import { adminApi } from '@/lib/api/admin';
import { toast } from 'sonner';

export default function DirectoryPage() {
    const [listings, setListings] = useState<any[]>([]);
    const [stats, setStats] = useState<any>(null);
    const [claims, setClaims] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [activeTab, setActiveTab] = useState<'listings' | 'claims'>('listings');

    const loadData = async () => {
        setLoading(true);
        try {
            const [listingsRes, statsRes, claimsRes] = await Promise.all([
                adminApi.getDirectoryListings(searchTerm),
                adminApi.getDirectoryStats(),
                adminApi.getDirectoryClaims()
            ]);

            if (listingsRes.data?.businesses) {
                setListings(listingsRes.data.businesses);
            }
            if (statsRes.data) {
                setStats(statsRes.data);
            }
            if (claimsRes.data) {
                setClaims(claimsRes.data);
            }
        } catch (error) {
            console.error("Failed to load directory data:", error);
            toast.error("Failed to sync directory data");
        } finally {
            setLoading(false);
        }
    };

    const handleApproveClaim = async (claimId: string) => {
        if (!confirm("Are you sure you want to approve this claim? The user will become the owner of the listing.")) return;

        try {
            const res = await adminApi.approveClaim(claimId);
            if (res.error) throw new Error(res.error);
            toast.success("Claim approved successfully");
            loadData();
        } catch (error: any) {
            toast.error(error.message || "Failed to approve claim");
        }
    };

    const handleRejectClaim = async (claimId: string) => {
        const reason = prompt("Reason for rejection (optional):");
        if (reason === null) return;

        try {
            const res = await adminApi.rejectClaim(claimId, reason);
            if (res.error) throw new Error(res.error);
            toast.success("Claim rejected");
            loadData();
        } catch (error: any) {
            toast.error(error.message || "Failed to reject claim");
        }
    };

    const handleDeleteListing = async (listingId: string) => {
        if (!confirm("Are you sure you want to delete this listing? It will be hidden from the directory.")) return;

        try {
            const res = await adminApi.deleteListing(listingId);
            if (res.error) throw new Error(res.error);
            toast.success("Listing deleted");
            loadData();
        } catch (error: any) {
            toast.error(error.message || "Failed to delete listing");
        }
    };

    const handleOptimizeListing = async (listingId: string) => {
        const toastId = toast.loading("AI is optimizing listing SEO...");
        try {
            const res = await adminApi.optimizeListing(listingId);
            if (res.error) throw new Error(res.error);
            toast.success("SEO Optimization complete!", { id: toastId });
            loadData();
        } catch (error: any) {
            toast.error(error.message || "Optimization failed", { id: toastId });
        }
    };

    useEffect(() => {
        loadData();
    }, [searchTerm]);

    return (
        <div className="p-6 space-y-6 bg-slate-50 dark:bg-slate-950 min-h-full">
            <PageHeader
                title={
                    <>Business <span className="text-blue-600">Directory</span></>
                }
                description="Manage the BizoLocal global business network and ownership claims."
            >
                <Button onClick={loadData} variant="outline" disabled={loading}>
                    <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Refresh
                </Button>
            </PageHeader>

            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-6 flex items-center justify-between">
                        <div>
                            <p className="text-xs font-bold text-gray-500 uppercase tracking-wider">Total Listings</p>
                            <h3 className="text-2xl font-black mt-1">{stats?.total_listings || 0}</h3>
                        </div>
                        <div className="w-12 h-12 bg-blue-50 dark:bg-blue-900/20 rounded-xl flex items-center justify-center text-blue-600">
                            <Building2 className="w-6 h-6" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-6 flex items-center justify-between">
                        <div>
                            <p className="text-xs font-bold text-gray-500 uppercase tracking-wider">Claimed</p>
                            <h3 className="text-2xl font-black mt-1">{stats?.claimed_listings || 0}</h3>
                        </div>
                        <div className="w-12 h-12 bg-green-50 dark:bg-green-900/20 rounded-xl flex items-center justify-center text-green-600">
                            <ShieldCheck className="w-6 h-6" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-6 flex items-center justify-between">
                        <div>
                            <p className="text-xs font-bold text-gray-500 uppercase tracking-wider">Pending Claims</p>
                            <h3 className="text-2xl font-black mt-1 text-orange-600">{stats?.pending_claims || 0}</h3>
                        </div>
                        <div className="w-12 h-12 bg-orange-50 dark:bg-orange-900/20 rounded-xl flex items-center justify-center text-orange-600">
                            <Activity className="w-6 h-6" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-6 flex items-center justify-between">
                        <div>
                            <p className="text-xs font-bold text-gray-500 uppercase tracking-wider">Platform Views</p>
                            <h3 className="text-2xl font-black mt-1">{stats?.total_views?.toLocaleString() || 0}</h3>
                        </div>
                        <div className="w-12 h-12 bg-purple-50 dark:bg-purple-900/20 rounded-xl flex items-center justify-center text-purple-600">
                            <BarChart3 className="w-6 h-6" />
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div className="flex space-x-4 border-b border-gray-200 dark:border-gray-800 pb-px">
                <button
                    onClick={() => setActiveTab('listings')}
                    className={`pb-4 px-2 text-sm font-bold transition-all relative ${activeTab === 'listings'
                        ? 'text-blue-600'
                        : 'text-gray-500 hover:text-gray-700'
                        }`}
                >
                    Active Listings
                    {activeTab === 'listings' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />}
                </button>
                <button
                    onClick={() => setActiveTab('claims')}
                    className={`pb-4 px-2 text-sm font-bold transition-all relative ${activeTab === 'claims'
                        ? 'text-blue-600'
                        : 'text-gray-500 hover:text-gray-700'
                        }`}
                >
                    Claim Requests
                    {stats?.pending_claims > 0 && (
                        <span className="ml-2 inline-flex items-center justify-center h-4 w-4 bg-orange-500 text-white text-[10px] rounded-full">
                            {stats.pending_claims}
                        </span>
                    )}
                    {activeTab === 'claims' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />}
                </button>
            </div>

            <Card className="border-none shadow-sm">
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle>{activeTab === 'listings' ? 'Business Network' : 'Ownership Claims'}</CardTitle>
                        {activeTab === 'listings' && (
                            <div className="relative w-72">
                                <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                                <Input
                                    placeholder="Search by name or slug..."
                                    className="pl-9 rounded-xl"
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                />
                            </div>
                        )}
                    </div>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <div className="flex flex-col items-center justify-center p-12">
                            <RefreshCw className="w-8 h-8 animate-spin text-blue-600 mb-4" />
                            <p className="text-gray-500 font-medium">Fetching directory records...</p>
                        </div>
                    ) : activeTab === 'listings' ? (
                        <div className="space-y-4">
                            {listings.length === 0 ? (
                                <div className="text-center p-12 text-gray-400 bg-gray-50 dark:bg-gray-900/50 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-800">
                                    <Building2 className="w-12 h-12 mx-auto mb-4 opacity-20" />
                                    <p className="font-bold">No business listings found</p>
                                    <p className="text-sm">Newly onboarded businesses will appear here automatically.</p>
                                </div>
                            ) : (
                                listings.map((item) => (
                                    <div key={item.id} className="group p-4 bg-white dark:bg-slate-900 border border-gray-100 dark:border-gray-800 rounded-2xl flex items-center justify-between hover:border-blue-200 dark:hover:border-blue-900/50 transition-all shadow-sm hover:shadow-md">
                                        <div className="flex items-center gap-4">
                                            <div className="w-14 h-14 bg-gray-50 dark:bg-gray-800 rounded-xl flex items-center justify-center overflow-hidden border border-gray-200 dark:border-gray-700">
                                                {item.google_photos && item.google_photos[0] ? (
                                                    <img src={item.google_photos[0]} alt="" className="w-full h-full object-cover" />
                                                ) : (
                                                    <Building2 className="w-6 h-6 text-gray-400" />
                                                )}
                                            </div>
                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <h4 className="font-black text-gray-900 dark:text-white group-hover:text-blue-600 transition-colors uppercase tracking-tight">{item.business_name}</h4>
                                                    {item.claimed ? (
                                                        <Badge className="bg-green-500/10 text-green-600 border-none text-[10px] font-black uppercase tracking-widest px-1.5 py-0">CLAIMED</Badge>
                                                    ) : (
                                                        <Badge className="bg-gray-500/10 text-gray-500 border-none text-[10px] font-black uppercase tracking-widest px-1.5 py-0">UNCLAIMED</Badge>
                                                    )}
                                                </div>
                                                <div className="flex items-center gap-4 mt-1 text-[11px] font-bold text-gray-500">
                                                    <span className="flex items-center gap-1">
                                                        <MapPin className="w-3 h-3" /> {item.city || 'Remote'}, {item.country || 'Global'}
                                                    </span>
                                                    <span className="flex items-center gap-1">
                                                        <Globe className="w-3 h-3 text-blue-500" /> directory.bizoholic.net/biz/{item.business_slug}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex items-center gap-3">
                                            <div className="text-right mr-4 hidden md:block">
                                                <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Category</p>
                                                <p className="text-sm font-bold">{item.category || 'Local Business'}</p>
                                            </div>
                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                className="rounded-xl flex items-center gap-1.5 text-blue-600 hover:text-blue-700 hover:bg-blue-50"
                                                onClick={() => handleOptimizeListing(item.id)}
                                            >
                                                <Sparkles className="w-4 h-4" />
                                                <span className="text-[10px] font-black uppercase tracking-widest">AI Optimize</span>
                                            </Button>
                                            <a
                                                href={`https://directory.bizoholic.net/biz/${item.business_slug}`}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-xl transition-all"
                                            >
                                                <ExternalLink className="w-5 h-5" />
                                            </a>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="rounded-xl text-red-500 hover:text-red-600 hover:bg-red-50"
                                                onClick={() => handleDeleteListing(item.id)}
                                            >
                                                <MoreVertical className="w-5 h-5 text-gray-400" />
                                            </Button>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {claims.length === 0 ? (
                                <div className="text-center p-12 text-gray-400 bg-gray-50 dark:bg-gray-900/50 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-800">
                                    <ShieldCheck className="w-12 h-12 mx-auto mb-4 opacity-20" />
                                    <p className="font-bold">No pending claim requests</p>
                                    <p className="text-sm">Verified business owners will request ownership here.</p>
                                </div>
                            ) : (
                                claims.map((claim) => (
                                    <div key={claim.id} className="p-4 bg-white dark:bg-slate-900 border border-gray-100 dark:border-gray-800 rounded-2xl flex items-center justify-between">
                                        <div className="flex items-center gap-4">
                                            <div className="w-12 h-12 bg-orange-50 dark:bg-orange-900/20 rounded-xl flex items-center justify-center text-orange-600">
                                                <Users className="w-6 h-6" />
                                            </div>
                                            <div>
                                                <h4 className="font-bold text-gray-900 dark:text-white uppercase tracking-tight">{claim.user_email}</h4>
                                                <div className="flex items-center gap-3 mt-1 text-[11px] font-bold text-gray-500">
                                                    <span>Listing ID: {claim.listing_id.slice(0, 8)}...</span>
                                                    <span className="mx-1">•</span>
                                                    <span className="flex items-center gap-1 uppercase tracking-widest text-[9px]">
                                                        <Clock className="w-3 h-3" /> Requested {new Date(claim.created_at).toLocaleDateString()}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex items-center gap-2">
                                            <Badge className={
                                                claim.status === 'pending' ? 'bg-orange-500/10 text-orange-600' :
                                                    claim.status === 'approved' ? 'bg-green-500/10 text-green-600' :
                                                        'bg-red-500/10 text-red-600'
                                            }>
                                                {claim.status.toUpperCase()}
                                            </Badge>
                                            {claim.status === 'pending' && (
                                                <div className="flex items-center gap-1">
                                                    <Button
                                                        size="sm"
                                                        variant="ghost"
                                                        className="rounded-lg h-8 text-[11px] font-bold text-green-600 hover:text-green-700 hover:bg-green-50"
                                                        onClick={() => handleApproveClaim(claim.id)}
                                                    >
                                                        APPROVE
                                                    </Button>
                                                    <Button
                                                        size="sm"
                                                        variant="ghost"
                                                        className="rounded-lg h-8 text-[11px] font-bold text-red-600 hover:text-red-700 hover:bg-red-50"
                                                        onClick={() => handleRejectClaim(claim.id)}
                                                    >
                                                        REJECT
                                                    </Button>
                                                </div>
                                            )}
                                            <Button size="sm" variant="outline" className="rounded-lg h-8 text-[11px] font-bold">MANAGE</Button>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Platform Health Integration */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                <Card className="bg-gradient-to-br from-indigo-600 to-blue-700 text-white border-none shadow-xl shadow-blue-500/20">
                    <CardHeader>
                        <PieChart className="w-8 h-8 mb-2 opacity-50" />
                        <CardTitle className="text-xl">SEO Performance Hub</CardTitle>
                        <CardDescription className="text-blue-100">Directroy listings contribute 42% of platform-wide backlink organic health.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-end justify-between">
                            <div>
                                <p className="text-3xl font-black">94.2</p>
                                <p className="text-xs font-bold uppercase tracking-widest text-blue-200">Network SEO Score</p>
                            </div>
                            <Button className="bg-white text-blue-600 hover:bg-white/90 rounded-xl font-bold">OPTIMIZE ALL</Button>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm overflow-hidden relative">
                    <div className="absolute top-0 right-0 p-4">
                        <div className="w-24 h-24 bg-blue-500/5 rounded-full -mr-12 -mt-12" />
                    </div>
                    <CardHeader>
                        <CardTitle className="text-lg">Discovery Hotspots</CardTitle>
                        <CardDescription>Top cities generating directory traffic today.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-3">
                            {[
                                { city: 'London', views: 1240, color: 'bg-blue-600' },
                                { city: 'New York', views: 890, color: 'bg-indigo-600' },
                                { city: 'Sydney', views: 450, color: 'bg-purple-600' }
                            ].map((item, i) => (
                                <div key={i} className="flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <div className={`w-2 h-2 rounded-full ${item.color}`} />
                                        <span className="text-xs font-bold">{item.city}</span>
                                    </div>
                                    <span className="text-[10px] font-black text-gray-400">{item.views} VIEWS</span>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
