import React, { useEffect, useState } from 'react';
import { brainApi } from '@/lib/brain-api';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, Circle, Loader2, Sparkles, Search, LayoutGrid, PackageOpen, Box } from 'lucide-react';
import * as Icons from 'lucide-react';
import { ToolIntegration } from '../types/onboarding';

interface Props {
    data: ToolIntegration;
    onUpdate: (data: Partial<ToolIntegration>) => void;
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

export function CategorizedToolSelectionStep({ data, onUpdate }: Props) {
    const [categories, setCategories] = useState<Category[]>([]);
    const [mcps, setMcps] = useState<Record<string, Mcp[]>>({}); // category_slug -> mcps
    const [loading, setLoading] = useState(true);
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState('');

    // Initial Data Fetch
    useEffect(() => {
        const load = async () => {
            try {
                const cats = await brainApi.mcp.listCategories();
                setCategories(cats);

                const allMcps = await brainApi.mcp.getRegistry();
                const grouped = allMcps.reduce((acc: any, mcp: Mcp) => {
                    const cat = cats.find((c: Category) => c.id === mcp.category_id);
                    if (cat) {
                        if (!acc[cat.slug]) acc[cat.slug] = [];
                        acc[cat.slug].push(mcp);
                    }
                    return acc;
                }, {});
                setMcps(grouped);

                if (cats.length > 0) setSelectedCategory(cats[0].slug);
            } catch (e) {
                console.error("Failed to load MCP marketplace", e);
            } finally {
                setLoading(false);
            }
        };
        load();
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

    if (loading) {
        return (
            <div className="flex h-64 items-center justify-center">
                <Loader2 className="animate-spin text-blue-600" size={32} />
            </div>
        );
    }

    const currentMcps = selectedCategory ? mcps[selectedCategory] || [] : [];
    const filteredMcps = currentMcps.filter(m =>
        m.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        m.description.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const featuredMcps = filteredMcps.filter(m => m.is_featured);
    const standardMcps = filteredMcps.filter(m => !m.is_featured);

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-8">
                <h2 className="text-3xl font-extrabold text-foreground tracking-tight">Power Up Your Business</h2>
                <p className="text-muted-foreground text-lg max-w-2xl mx-auto mt-2">
                    Select the platforms you already use. We'll automatically integrate them into your BizOSaaS dashboard.
                </p>
            </div>

            <div className="flex flex-col md:grid md:grid-cols-4 gap-8 min-h-[500px]">
                {/* Categories */}
                <div className="md:col-span-1 border-b md:border-b-0 md:border-r pb-4 md:pb-0 md:pr-6">
                    <div className="sticky top-4 space-y-2">
                        <Label className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider px-4">Categories</Label>
                        <div className="flex flex-row md:flex-col gap-1 overflow-x-auto md:overflow-x-visible pb-2 md:pb-0 no-scrollbar">
                            {categories.map(cat => {
                                const Icon = (Icons as any)[cat.icon] || Box;
                                const isSelected = selectedCategory === cat.slug;

                                return (
                                    <button
                                        key={cat.id}
                                        onClick={() => {
                                            setSelectedCategory(cat.slug);
                                            setSearchTerm('');
                                        }}
                                        className={`flex-shrink-0 flex items-center gap-3 px-4 py-3 md:w-full rounded-xl text-sm transition-all whitespace-nowrap ${isSelected
                                            ? 'bg-blue-600 text-white shadow-lg shadow-blue-200 dark:shadow-none font-semibold'
                                            : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                                            }`}
                                    >
                                        <Icon size={18} />
                                        <span>{cat.name}</span>
                                        {data.selectedMcps?.some(s => mcps[cat.slug]?.some(m => m.slug === s)) && (
                                            <div className={`ml-auto h-2 w-2 rounded-full ${isSelected ? 'bg-white' : 'bg-green-500 animate-pulse'}`} />
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
                        <div className="text-xs font-medium text-muted-foreground px-3 py-1 bg-background rounded-full border border-muted">
                            {data.selectedMcps?.length || 0} tools selected
                        </div>
                    </div>

                    {selectedCategory ? (
                        <div className="space-y-8">
                            {/* Featured Tools */}
                            {featuredMcps.length > 0 && !searchTerm && (
                                <div className="space-y-4">
                                    <div className="flex items-center gap-2 px-1">
                                        <Sparkles size={16} className="text-amber-500" />
                                        <h3 className="text-sm font-bold text-foreground">Recommended for You</h3>
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
                                {featuredMcps.length > 0 && !searchTerm && (
                                    <div className="px-1">
                                        <h3 className="text-sm font-bold text-muted-foreground">All Tools</h3>
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
            className={`group cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1 ${selected ? 'border-blue-500 bg-blue-50/50 dark:bg-blue-900/10 ring-2 ring-blue-500/20' : 'hover:border-blue-300'
                }`}
            onClick={onToggle}
        >
            <CardContent className="p-5 flex items-start gap-5">
                <div className="mt-1">
                    {selected ? (
                        <CheckCircle className="text-blue-600" size={24} />
                    ) : (
                        <Circle className="text-muted-foreground/30 group-hover:text-muted-foreground/60" size={24} />
                    )}
                </div>
                <div className="flex-1 space-y-2">
                    <div className="flex items-center justify-between">
                        <h3 className="font-bold text-foreground text-lg">{mcp.name}</h3>
                        {mcp.is_official && (
                            <Badge className="bg-blue-100 text-blue-700 hover:bg-blue-100 border-none text-[9px] px-2 py-0">Certified</Badge>
                        )}
                    </div>
                    <p className="text-sm text-muted-foreground line-clamp-2 leading-relaxed">{mcp.description}</p>
                    <div className="flex flex-wrap gap-1.5 pt-2">
                        {mcp.capabilities.slice(0, 3).map((cap: string) => (
                            <span key={cap} className="text-[9px] bg-muted/80 text-muted-foreground px-2 py-1 rounded-md font-medium uppercase tracking-wider">
                                {cap}
                            </span>
                        ))}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
