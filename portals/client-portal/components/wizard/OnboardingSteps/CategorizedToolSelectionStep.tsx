import React, { useEffect, useState } from 'react';
import { brainApi } from '@/lib/brain-api';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckCircle, Circle, ArrowRight, Loader2 } from 'lucide-react';
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
    capabilities: string[];
}

export function CategorizedToolSelectionStep({ data, onUpdate }: Props) {
    const [categories, setCategories] = useState<Category[]>([]);
    const [mcps, setMcps] = useState<Record<string, Mcp[]>>({}); // category_slug -> mcps
    const [loading, setLoading] = useState(true);
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

    // Initial Data Fetch
    useEffect(() => {
        const load = async () => {
            try {
                const cats = await brainApi.mcp.listCategories();
                setCategories(cats);

                // Fetch all MCPs or fetch strictly per category
                // Ideally fetch all for better UX responsiveness
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

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-foreground">Select Your Tools</h2>
                <p className="text-muted-foreground">Choose the platforms you use to power your business.</p>
            </div>

            <div className="flex flex-col md:grid md:grid-cols-4 gap-6 min-h-[400px]">
                {/* Categories - Horizontal Scroll on Mobile, Sidebar on Desktop */}
                <div className="md:col-span-1 border-b md:border-b-0 md:border-r pb-4 md:pb-0 md:pr-4">
                    <div className="flex flex-row md:flex-col gap-2 overflow-x-auto md:overflow-x-visible pb-2 md:pb-0 no-scrollbar">
                        {categories.map(cat => {
                            const Icon = (Icons as any)[cat.icon] || Icons.Box;
                            const isSelected = selectedCategory === cat.slug;

                            return (
                                <button
                                    key={cat.id}
                                    onClick={() => setSelectedCategory(cat.slug)}
                                    className={`flex-shrink-0 flex items-center gap-2 px-4 py-2.5 md:w-full md:justify-between rounded-full md:rounded-lg text-sm transition-all whitespace-nowrap ${isSelected
                                        ? 'bg-blue-600 text-white shadow-md md:bg-blue-500/10 md:text-blue-700 md:dark:text-blue-400 md:shadow-none font-medium'
                                        : 'text-muted-foreground hover:bg-muted'
                                        }`}
                                >
                                    <div className="flex items-center gap-2">
                                        <Icon size={16} />
                                        <span>{cat.name}</span>
                                    </div>
                                    {data.selectedMcps?.some(s => mcps[cat.slug]?.some(m => m.slug === s)) && (
                                        <div className={`h-1.5 w-1.5 rounded-full ${isSelected ? 'bg-white' : 'bg-green-500'}`} />
                                    )}
                                </button>
                            );
                        })}
                    </div>
                </div>

                {/* MCP Grid */}
                <div className="md:col-span-3">
                    {selectedCategory && mcps[selectedCategory] ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {mcps[selectedCategory].map(mcp => {
                                const isSelected = (data.selectedMcps || []).includes(mcp.slug);
                                return (
                                    <Card
                                        key={mcp.id}
                                        className={`cursor-pointer transition-all hover:border-blue-300 ${isSelected ? 'border-blue-500 bg-blue-500/5 ring-1 ring-blue-500' : ''
                                            }`}
                                        onClick={() => toggleMcp(mcp.slug)}
                                    >
                                        <CardContent className="p-4 flex items-start gap-4">
                                            <div onClick={(e) => { e.stopPropagation(); toggleMcp(mcp.slug); }}>
                                                {isSelected ? (
                                                    <CheckCircle className="text-blue-600 mt-1" size={20} />
                                                ) : (
                                                    <Circle className="text-muted-foreground/40 mt-1" size={20} />
                                                )}
                                            </div>
                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <h3 className="font-semibold text-foreground">{mcp.name}</h3>
                                                    {mcp.is_official && (
                                                        <span className="text-[10px] bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded font-medium">Official</span>
                                                    )}
                                                </div>
                                                <p className="text-sm text-muted-foreground mt-1">{mcp.description}</p>
                                                <div className="flex flex-wrap gap-1 mt-3">
                                                    {mcp.capabilities.slice(0, 3).map(cap => (
                                                        <span key={cap} className="text-[10px] bg-muted text-muted-foreground px-2 py-0.5 rounded-full capitalize">
                                                            {cap}
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>
                                        </CardContent>
                                    </Card>
                                );
                            })}
                        </div>
                    ) : (
                        <div className="flex flex-col items-center justify-center h-full text-muted-foreground/60">
                            <Icons.PackageOpen size={48} className="mb-4 opacity-20" />
                            <p>No tools available in this category yet.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
