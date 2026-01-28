'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Globe,
    Search,
    RefreshCw,
    Plus,
    Check,
    X,
    ExternalLink,
    ArrowRight,
    Settings,
    Shield,
    Clock,
    Zap,
    Lock,
    Edit2
} from 'lucide-react';
import { domainApi, DomainResult, DomainInventoryItem } from '@/lib/api/domains';
import { toast } from 'sonner';

export default function DomainsPage() {
    const [myDomains, setMyDomains] = useState<DomainInventoryItem[]>([]);
    const [searchResults, setSearchResults] = useState<DomainResult[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [isSearching, setIsSearching] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [activeTab, setActiveTab] = useState<'my-domains' | 'search'>('my-domains');

    const loadMyDomains = async () => {
        setIsLoading(true);
        try {
            const res = await domainApi.getMyDomains();
            if (res.data) setMyDomains(res.data);
        } catch (error) {
            toast.error("Failed to load your domains");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadMyDomains();
    }, []);

    const handleSearch = async (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        if (!searchQuery) return;

        setIsSearching(true);
        setActiveTab('search');
        try {
            const res = await domainApi.searchDomains(searchQuery);
            if (res.data) setSearchResults(res.data);
        } catch (error) {
            toast.error("Search failed. Please try again.");
        } finally {
            setIsSearching(false);
        }
    };

    const handlePurchase = async (domain: DomainResult) => {
        const toastId = toast.loading(`Initiating registration for ${domain.domain}...`);
        try {
            const res = await domainApi.purchaseDomain(domain.domain, domain.price);
            if (res.error) throw new Error(res.error);
            toast.success(`${domain.domain} registered successfully!`, { id: toastId });
            loadMyDomains();
            setActiveTab('my-domains');
        } catch (error: any) {
            toast.error(error.message || "Registration failed", { id: toastId });
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Domains & Digital Assets</h1>
                    <p className="text-slate-500 mt-1 font-medium">Claim your professional identity and manage your web presence.</p>
                </div>
                <div className="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
                    <Button
                        variant={activeTab === 'my-domains' ? 'default' : 'ghost'}
                        size="sm"
                        onClick={() => setActiveTab('my-domains')}
                        className="rounded-lg text-xs font-bold px-6"
                    >
                        My Portfolio
                    </Button>
                    <Button
                        variant={activeTab === 'search' ? 'default' : 'ghost'}
                        size="sm"
                        onClick={() => setActiveTab('search')}
                        className="rounded-lg text-xs font-bold px-6"
                    >
                        New Domain
                    </Button>
                </div>
            </div>

            {/* Quick Search Bar (Global Access) */}
            <Card className="border-none shadow-xl bg-gradient-to-r from-blue-600 to-indigo-700 text-white overflow-hidden p-6 relative">
                <div className="absolute top-0 right-0 p-8 opacity-10">
                    <Globe className="w-32 h-32" />
                </div>
                <div className="relative z-10 max-w-2xl">
                    <h2 className="text-xl font-bold mb-4">Find your next big idea</h2>
                    <form onSubmit={handleSearch} className="flex gap-2">
                        <div className="relative flex-1">
                            <Search className="absolute left-4 top-3.5 h-5 w-5 text-slate-400" />
                            <Input
                                placeholder="search.com, company.net, myname.ai..."
                                className="pl-12 h-12 bg-white text-slate-900 border-none rounded-2xl focus-visible:ring-offset-0 focus-visible:ring-white/20 text-lg font-medium"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>
                        <Button type="submit" size="lg" className="h-12 px-8 bg-white text-blue-600 hover:bg-white/90 rounded-2xl font-bold text-lg" disabled={isSearching}>
                            {isSearching ? <RefreshCw className="w-5 h-5 animate-spin" /> : "Search"}
                        </Button>
                    </form>
                    <div className="flex gap-4 mt-4 overflow-x-auto pb-2">
                        {['.com', '.net', '.org', '.io', '.ai', '.tech'].map(tld => (
                            <Badge key={tld} variant="outline" className="text-white border-white/20 bg-white/5 hover:bg-white/10 cursor-pointer px-3 py-1 font-black leading-none">
                                {tld}
                            </Badge>
                        ))}
                    </div>
                </div>
            </Card>

            {activeTab === 'my-domains' && (
                <div className="grid gap-6">
                    {isLoading ? (
                        <div className="py-20 flex flex-col items-center justify-center text-slate-400">
                            <RefreshCw className="w-10 h-10 animate-spin mb-4" />
                            <p className="font-bold uppercase tracking-widest text-xs">Syncing with global registries...</p>
                        </div>
                    ) : myDomains.length === 0 ? (
                        <Card className="border-2 border-dashed border-slate-200 dark:border-slate-800 bg-transparent p-12 text-center">
                            <div className="w-16 h-16 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Globe className="w-8 h-8 text-slate-300" />
                            </div>
                            <h3 className="text-lg font-bold">No domains registered yet</h3>
                            <p className="text-slate-500 mb-6">Start your online journey by registering your first domain name.</p>
                            <Button onClick={() => setActiveTab('search')} className="bg-blue-600 hover:bg-blue-700 rounded-xl font-bold">
                                Browse Domains <ArrowRight className="ml-2 w-4 h-4" />
                            </Button>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                            {myDomains.map(domain => (
                                <Card key={domain.id} className="border-none shadow-md hover:shadow-xl transition-all group overflow-hidden bg-white dark:bg-slate-900">
                                    <div className="p-6 flex items-start justify-between">
                                        <div className="flex items-center gap-4">
                                            <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-2xl group-hover:bg-blue-600 group-hover:text-white transition-all duration-300">
                                                <Globe className="w-6 h-6" />
                                            </div>
                                            <div>
                                                <h4 className="text-xl font-black tracking-tight text-slate-900 dark:text-white">{domain.domain_name}</h4>
                                                <div className="flex items-center gap-2 mt-1">
                                                    <Badge className="bg-emerald-500/10 text-emerald-600 border-none text-[10px] font-black uppercase tracking-widest px-1.5 py-0">ACTIVE</Badge>
                                                    <span className="text-[10px] font-bold text-slate-400 uppercase">Provider: {domain.registrar}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <Button variant="ghost" size="icon" className="rounded-xl hover:bg-slate-100">
                                            <Settings className="w-5 h-5 text-slate-400" />
                                        </Button>
                                    </div>

                                    <div className="px-6 py-4 bg-slate-50 dark:bg-slate-800/50 flex items-center justify-between border-t border-slate-100 dark:border-slate-800">
                                        <div className="flex items-center gap-6">
                                            <div>
                                                <p className="text-[8px] font-black uppercase tracking-widest text-slate-400 mb-1">Status</p>
                                                <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-600">
                                                    <Check className="w-3 h-3" /> SECURE
                                                </div>
                                            </div>
                                            <div>
                                                <p className="text-[8px] font-black uppercase tracking-widest text-slate-400 mb-1">Expiry</p>
                                                <div className="flex items-center gap-1.5 text-xs font-bold text-slate-600 dark:text-slate-300">
                                                    <Clock className="w-3 h-3" /> {domain.expiry_date ? new Date(domain.expiry_date).toLocaleDateString() : 'N/A'}
                                                </div>
                                            </div>
                                        </div>
                                        <Button size="sm" variant="outline" className="rounded-lg h-8 text-[10px] font-black uppercase tracking-widest hover:border-blue-600 hover:text-blue-600">
                                            MANAGE DNS
                                        </Button>
                                    </div>
                                </Card>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {activeTab === 'search' && (
                <div className="space-y-6">
                    {isSearching ? (
                        <div className="py-20 flex flex-col items-center justify-center text-slate-400">
                            <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-6" />
                            <p className="text-xl font-bold text-slate-600 dark:text-slate-300">Searching global registries...</p>
                        </div>
                    ) : searchResults.length === 0 ? (
                        <div className="text-center py-20 text-slate-400">
                            <Search className="w-16 h-16 mx-auto mb-4 opacity-20" />
                            <p className="text-lg font-bold">Search for a domain above to check availability</p>
                        </div>
                    ) : (
                        <div className="grid gap-4">
                            {searchResults.map((result, i) => (
                                <Card key={i} className={`overflow-hidden border-none shadow-md ${result.available ? 'bg-white dark:bg-slate-900' : 'bg-slate-50 dark:bg-slate-950 opacity-80'}`}>
                                    <div className="p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
                                        <div className="flex items-center gap-4">
                                            <div className={`p-3 rounded-2xl ${result.available ? 'bg-emerald-50 text-emerald-600' : 'bg-slate-200 text-slate-400'}`}>
                                                {result.available ? <Check className="w-6 h-6" /> : <X className="w-6 h-6" />}
                                            </div>
                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <h4 className="text-2xl font-black tracking-tight text-slate-900 dark:text-white uppercase italic">{result.domain}</h4>
                                                    {result.premium && <Badge className="bg-amber-100 text-amber-600 border-none font-black italic shadow-sm hover:scale-105 transition-transform">PREMIUM</Badge>}
                                                </div>
                                                <p className={`text-sm font-bold ${result.available ? 'text-emerald-500' : 'text-slate-400'}`}>
                                                    {result.available ? 'Available for immediate registration' : 'Taken - Registered elsewhere'}
                                                </p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            {result.available ? (
                                                <>
                                                    <div className="text-right mr-4">
                                                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Starting at</p>
                                                        <p className="text-2xl font-black text-slate-900 dark:text-white italic">${result.price.toFixed(2)}<span className="text-xs font-bold not-italic">/year</span></p>
                                                    </div>
                                                    <Button onClick={() => handlePurchase(result)} className="bg-blue-600 hover:bg-blue-700 h-14 px-8 rounded-2xl font-black text-lg shadow-lg shadow-blue-500/20 group">
                                                        BUY NOW <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                                    </Button>
                                                </>
                                            ) : (
                                                <Button variant="outline" className="h-12 rounded-xl font-bold border-slate-200" disabled>
                                                    Whois Lookup
                                                </Button>
                                            )}
                                        </div>
                                    </div>
                                    {result.available && (
                                        <div className="px-6 py-2 bg-emerald-500/5 flex gap-4 text-[10px] font-black uppercase text-emerald-600 tracking-widest border-t border-emerald-500/10">
                                            <span className="flex items-center gap-1.5"><Shield className="w-3 h-3" /> Free Privacy Control</span>
                                            <span className="flex items-center gap-1.5"><Zap className="w-3 h-3" /> DNS Propagation: &lt; 5m</span>
                                        </div>
                                    )}
                                </Card>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
