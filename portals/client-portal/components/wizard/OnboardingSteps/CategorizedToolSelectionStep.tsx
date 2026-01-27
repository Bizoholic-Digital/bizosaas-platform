import React, { useEffect, useState, useMemo } from 'react';
import { brainApi } from '@/lib/brain-api';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
    CheckCircle,
    Circle,
    Loader2,
    Sparkles,
    Search,
    LayoutGrid,
    PackageOpen,
    Box,
    AlertTriangle,
    Info,
    Globe,
    Target,
    BarChart3
} from 'lucide-react';
import * as Icons from 'lucide-react';
import { ToolIntegration } from '../types/onboarding';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle
} from '@/components/ui/dialog';

interface Props {
    data: ToolIntegration;
    onUpdate: (data: Partial<ToolIntegration>) => void;
    state?: any; // Pass full state to access detection results
}

interface Category {
    id: string;
    name: string;
    slug: string;
    icon: string;
    description: string;
}

interface Mcp {
    id: string;
    name: string;
    slug: string;
    description: string;
    category_id: string;
    is_official: boolean;
    is_featured: boolean;
    capabilities: string[];
}

export function CategorizedToolSelectionStep({ data, onUpdate, state }: Props) {
    const [categories, setCategories] = useState<Category[]>([]);
    const [mcps, setMcps] = useState<Record<string, Mcp[]>>({}); // category_slug -> mcps
    const [loading, setLoading] = useState(true);
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState('');

    // Auto-selection monitoring
    const [initialSelectedMcps] = useState<string[]>(data.selectedMcps || []);
    const [showConfirm, setShowConfirm] = useState(false);

    // Initial Data Fetch
    useEffect(() => {
        let mounted = true;
        const load = async () => {
            try {
                const cats = await brainApi.mcp.listCategories();

                // Ensure "Project Management" or similar category exists for Plane
                let projectsCat = cats.find(c => c.slug === 'projects' || c.slug === 'tasks');
                if (!projectsCat && cats.length > 0) {
                    // This is a safety check/mocking if backend is missing it
                    console.warn("Backend missing projects/tasks category");
                }

                if (mounted) {
                    setCategories(cats);
                    if (cats.length > 0) setSelectedCategory(cats[0].slug);
                }

                const allMcps = await brainApi.mcp.getRegistry();

                // PLANE.SO INJECTION: Ensure Plane is in the list if not already there
                const hasPlane = allMcps.some(m => m.slug === 'plane');
                if (!hasPlane && projectsCat) {
                    allMcps.push({
                        id: 'plane-mcp',
                        name: 'Plane.so',
                        slug: 'plane',
                        description: 'Open source project management api-first tool for task tracking and planning.',
                        category_id: projectsCat.id,
                        is_official: true,
                        is_featured: true,
                        capabilities: ['Task Tracking', 'Kanban', 'Sprint Planning']
                    });
                }

                const grouped = allMcps.reduce((acc: any, mcp: Mcp) => {
                    const cat = cats.find((c: Category) => c.id === mcp.category_id);
                    if (cat) {
                        if (!acc[cat.slug]) acc[cat.slug] = [];
                        acc[cat.slug].push(mcp);
                    }
                    return acc;
                }, {});

                if (mounted) setMcps(grouped);
            } catch (err) {
                console.error("Failed to load tools", err);
            } finally {
                if (mounted) setLoading(false);
            }
        };
        load();
        return () => { mounted = false; };
    }, []);

    const toggleMcp = (slug: string) => {
        const current = new Set(data.selectedMcps || []);
        if (current.has(slug)) {
            current.delete(slug);
        } else {
            current.add(slug);
        }
        onUpdate({ selectedMcps: Array.from(current) });
    };

    const CORE_SLUGS = ['wordpress', 'shopify', 'fluentcrm', 'hubspot', 'google-tag-manager', 'google-analytics-4'];

    const currentMcps = (selectedCategory ? mcps[selectedCategory] || [] : [])
        .filter(m => !CORE_SLUGS.includes(m.slug));

    const filteredMcps = useMemo(() => {
        return currentMcps.filter(m =>
            m.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            m.description.toLowerCase().includes(searchTerm.toLowerCase())
        );
    }, [currentMcps, searchTerm]);

    const featuredMcps = filteredMcps.filter(m => m.is_featured);
    const standardMcps = filteredMcps.filter(m => !m.is_featured);

    const detectedFoundations = useMemo(() => {
        const found = [];
        if (state?.digitalPresence.cmsType === 'wordpress') found.push({ name: 'WordPress', type: 'CMS', slug: 'wordpress', icon: 'Globe' });
        if (state?.digitalPresence.cmsType === 'shopify') found.push({ name: 'Shopify', type: 'CMS', slug: 'shopify', icon: 'Globe' });
        if (state?.digitalPresence.crmType === 'fluentcrm') found.push({ name: 'FluentCRM', type: 'CRM', slug: 'fluentcrm', icon: 'Target' });
        if (state?.digitalPresence.crmType === 'hubspot') found.push({ name: 'HubSpot', type: 'CRM', slug: 'hubspot', icon: 'Target' });
        if (state?.digitalPresence.ecommerceType === 'woocommerce') found.push({ name: 'WooCommerce', type: 'E-commerce', slug: 'woocommerce', icon: 'ShoppingBag' });

        const analytics = [...(state?.analytics.auditedServices?.essential || []), ...(state?.analytics.auditedServices?.optional || [])];
        if (analytics.some(s => s.service?.toUpperCase() === 'GTM')) found.push({ name: 'Google Tag Manager', type: 'Analytics', slug: 'google-tag-manager', icon: 'BarChart3' });
        if (analytics.some(s => ['GA4', 'GA', 'GOOGLE ANALYTICS'].includes(s.service?.toUpperCase()))) found.push({ name: 'Google Analytics 4', type: 'Analytics', slug: 'google-analytics-4', icon: 'BarChart3' });

        return found;
    }, [state?.digitalPresence, state?.analytics]);

    if (loading) {
        return (
            <div className="flex h-64 flex-col items-center justify-center gap-4">
                <Loader2 className="animate-spin text-blue-600" size={32} />
                <p className="text-sm text-muted-foreground animate-pulse">Loading specialist registry...</p>
            </div>
        );
    }

    const hasSelectionChanges = JSON.stringify(initialSelectedMcps.sort()) !== JSON.stringify((data.selectedMcps || []).sort());

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            {detectedFoundations.length > 0 ? (
                <div className="bg-white dark:bg-slate-900 border-2 border-blue-500/20 rounded-3xl p-6 shadow-xl shadow-blue-500/5 mb-8">
                    <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center gap-3">
                            <div className="bg-blue-600 p-2 rounded-xl text-white">
                                <Box className="w-5 h-5" />
                            </div>
                            <div className="text-left">
                                <h3 className="text-sm font-black text-foreground uppercase tracking-tight leading-none mb-1">Detected Infrastructure</h3>
                                <p className="text-[10px] text-muted-foreground font-bold uppercase tracking-widest">We've established these as your platform core</p>
                            </div>
                        </div>
                        <Badge variant="outline" className="border-blue-500/30 text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 font-black text-[10px] px-3 py-1 rounded-full flex items-center gap-1.5 uppercase transition-all">
                            <CheckCircle size={10} /> Verified Foundations
                        </Badge>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        {detectedFoundations.map(found => {
                            const Icon = (Icons as any)[found.icon] || Globe;
                            return (
                                <div key={found.slug} className="flex items-center gap-4 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 group transition-all hover:border-blue-500/30 hover:bg-white dark:hover:bg-slate-800">
                                    <div className="p-3 rounded-xl bg-white dark:bg-slate-900 shadow-sm text-blue-600 transition-transform group-hover:scale-110">
                                        <Icon size={20} />
                                    </div>
                                    <div className="text-left">
                                        <p className="text-[8px] font-black text-muted-foreground uppercase tracking-widest leading-none mb-1">{found.type}</p>
                                        <h4 className="font-bold text-gray-900 dark:text-white text-sm">{found.name}</h4>
                                    </div>
                                    <div className="ml-auto">
                                        <CheckCircle className="text-green-500 w-4 h-4" />
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            ) : initialSelectedMcps.length > 0 && (
                <div className="bg-blue-500/5 border border-blue-500/10 rounded-2xl p-4 flex items-center gap-4 mb-6">
                    <div className="bg-blue-500/20 p-2 rounded-xl">
                        <Info className="text-blue-600 h-5 w-5" />
                    </div>
                    <div className="flex-1">
                        <p className="text-sm font-bold text-blue-900 dark:text-blue-400 leading-tight text-left">Smart Recommendations Applied</p>
                        <p className="text-xs text-blue-700 dark:text-blue-300/70 text-left">We've pre-selected tools based on your digital presence.</p>
                    </div>
                </div>
            )}

            <div className="flex flex-col md:grid md:grid-cols-4 gap-8 min-h-[500px]">
                {/* Categories */}
                <div className="md:col-span-1 border-b md:border-b-0 md:border-r pb-4 md:pb-0 md:pr-6">
                    <div className="sticky top-4 space-y-2">
                        <Label className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider px-4">Categories</Label>
                        <div className="flex flex-row md:flex-col gap-1 overflow-x-auto md:overflow-x-visible pb-2 md:pb-0 no-scrollbar">
                            {categories.map(cat => {
                                const Icon = (Icons as any)[cat.icon] || Box;
                                const isSelected = selectedCategory === cat.slug;

                                // Count standard tools in this category
                                let countInCat = data.selectedMcps?.filter(s => mcps[cat.slug]?.some(m => m.slug === s)).length || 0;

                                // Manually add foundations to their respective category counts
                                if (cat.slug === 'cms' || cat.slug === 'websites') {
                                    if (data.selectedMcps?.includes('wordpress')) countInCat++;
                                    if (data.selectedMcps?.includes('shopify')) countInCat++;
                                } else if (cat.slug === 'crm' || cat.slug === 'customers') {
                                    if (data.selectedMcps?.includes('fluentcrm')) countInCat++;
                                    if (data.selectedMcps?.includes('hubspot')) countInCat++;
                                } else if (cat.slug === 'analytics' || cat.slug === 'data') {
                                    if (data.selectedMcps?.includes('google-tag-manager')) countInCat++;
                                    if (data.selectedMcps?.includes('google-analytics-4')) countInCat++;
                                } else if (cat.slug === 'ecommerce' || cat.slug === 'store') {
                                    if (data.selectedMcps?.includes('woocommerce')) countInCat++;
                                }

                                return (
                                    <button
                                        key={cat.id}
                                        onClick={() => {
                                            setSelectedCategory(cat.slug);
                                            setSearchTerm('');
                                        }}
                                        className={`flex-shrink-0 flex items-center gap-3 px-4 py-3 md:w-full rounded-xl text-sm transition-all whitespace-nowrap relative ${isSelected
                                            ? 'bg-blue-600 text-white shadow-lg shadow-blue-200 dark:shadow-none font-semibold'
                                            : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                                            }`}
                                    >
                                        <Icon size={18} />
                                        <span>{cat.name}</span>
                                        {countInCat > 0 && (
                                            <Badge className={`ml-auto border-none h-5 min-w-[20px] px-1 justify-center rounded-full ${isSelected ? 'bg-white text-blue-600' : 'bg-green-500 text-white'}`}>
                                                {countInCat}
                                            </Badge>
                                        )}
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                </div>

                {/* MCP Grid */}
                <div className="md:col-span-3 space-y-6">
                    {/* Search & Stats */}
                    <div className="flex flex-col sm:flex-row gap-4 items-center justify-between bg-muted/30 p-4 rounded-2xl border border-muted">
                        <div className="relative w-full sm:max-w-xs">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={16} />
                            <Input
                                placeholder="Search tools..."
                                className="pl-10 bg-background border-none ring-1 ring-muted focus:ring-2 focus:ring-blue-500"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="text-xs font-bold text-muted-foreground px-3 py-1 bg-background rounded-full border border-muted uppercase tracking-tighter">
                                {data.selectedMcps?.length || 0} Tools Enabled
                            </div>
                        </div>
                    </div>

                    {selectedCategory ? (
                        <div className="space-y-8">
                            {/* Featured Tools */}
                            {featuredMcps.length > 0 && !searchTerm && (
                                <div className="space-y-4">
                                    <div className="flex items-center gap-2 px-1">
                                        <Sparkles size={16} className="text-amber-500 fill-amber-500/20" />
                                        <h3 className="text-sm font-black text-foreground uppercase tracking-tight">Recommended Connectors</h3>
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {featuredMcps.map(mcp => (
                                            <McpCard key={mcp.id} mcp={mcp} selected={data.selectedMcps?.includes(mcp.slug)} onToggle={() => toggleMcp(mcp.slug)} />
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Standard Tools */}
                            <div className="space-y-4">
                                {(featuredMcps.length > 0 && !searchTerm) && (
                                    <div className="px-1">
                                        <h3 className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Available MCPs</h3>
                                    </div>
                                )}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    {standardMcps.map(mcp => (
                                        <McpCard key={mcp.id} mcp={mcp} selected={data.selectedMcps?.includes(mcp.slug)} onToggle={() => toggleMcp(mcp.slug)} />
                                    ))}
                                </div>
                            </div>

                            {filteredMcps.length === 0 && (
                                <div className="flex flex-col items-center justify-center py-20 text-muted-foreground/60 bg-muted/10 rounded-3xl border-2 border-dashed border-muted">
                                    <PackageOpen size={64} className="mb-4 opacity-20" />
                                    <p className="text-lg font-medium">No tools found matching "{searchTerm}"</p>
                                    <Button variant="ghost" className="mt-2 text-blue-600" onClick={() => setSearchTerm('')}>Clear search</Button>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="flex flex-col items-center justify-center py-20 text-muted-foreground/60">
                            <LayoutGrid size={64} className="mb-4 opacity-20" />
                            <p>Select a category to explore tools</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

function McpCard({ mcp, selected, onToggle }: { mcp: any, selected: boolean, onToggle: () => void }) {
    return (
        <Card
            className={`group cursor-pointer transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 relative overflow-hidden ${selected
                ? 'border-blue-500 bg-blue-50/50 dark:bg-blue-900/10 ring-4 ring-blue-500/10'
                : 'hover:border-blue-300 dark:border-slate-800'
                }`}
            onClick={onToggle}
        >
            {selected && <div className="absolute top-0 right-0 w-16 h-16 bg-blue-500/10 rounded-bl-full flex items-start justify-end p-2"><CheckCircle size={12} className="text-blue-600" /></div>}

            <CardContent className="p-5 flex items-start gap-4">
                <div className="mt-1">
                    {selected ? (
                        <div className="bg-blue-600 rounded-full p-1 text-white"><CheckCircle size={20} /></div>
                    ) : (
                        <div className="text-muted-foreground/30 group-hover:text-blue-500/50 transition-colors"><Circle size={24} /></div>
                    )}
                </div>
                <div className="flex-1 space-y-2 text-left">
                    <div className="flex items-center justify-between">
                        <h3 className="font-bold text-foreground text-base tracking-tight leading-tight">{mcp.name}</h3>
                        {mcp.is_official && (
                            <Badge className="bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-400 hover:bg-blue-100 border-none text-[8px] font-black px-1.5 py-0 uppercase tracking-tighter">Verified</Badge>
                        )}
                    </div>
                    <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed font-medium">{mcp.description}</p>
                    <div className="flex flex-wrap gap-1 pt-1">
                        {mcp.capabilities.slice(0, 3).map((cap: string) => (
                            <span key={cap} className="text-[8px] bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 px-1.5 py-0.5 rounded-md font-bold uppercase">
                                {cap}
                            </span>
                        ))}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
