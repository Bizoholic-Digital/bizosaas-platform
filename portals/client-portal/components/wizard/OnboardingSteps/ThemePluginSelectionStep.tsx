import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, Circle, Layout, Puzzle, ShieldCheck, ExternalLink, Zap, Star } from 'lucide-react';
import { MarketplaceConfig, MarketplaceAsset } from '../types/onboarding';

interface Props {
    data: MarketplaceConfig;
    onUpdate: (data: Partial<MarketplaceConfig>) => void;
}

const RECOMMENDED_ASSETS: MarketplaceAsset[] = [
    {
        id: 'theme-1',
        name: 'BizOSaaS Ultra-Clean',
        slug: 'bizosaas-ultra',
        type: 'theme',
        price: 'free',
        provider: 'bizosaas',
        isRecommended: true,
        description: 'Blazing fast, SEO-optimized theme designed specifically for lead generation.',
        image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=400'
    },
    {
        id: 'theme-2',
        name: 'Astra (Pro)',
        slug: 'astra-pro',
        type: 'theme',
        price: 59,
        provider: 'wordpress',
        affiliateLink: 'https://wpastra.com/?bsf=999',
        description: 'The most popular theme for lightweight WordPress performance.',
        image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80&w=400'
    },
    {
        id: 'plugin-bridge',
        name: 'BizOSaaS Connect Bridge',
        slug: 'bizosaas-bridge',
        type: 'plugin',
        price: 'free',
        provider: 'bizosaas',
        isRecommended: true,
        description: 'Core infrastructure: Auto-injects GTM, GA4, and Pixel without bloat.',
    },
    {
        id: 'plugin-seo',
        name: 'RankMath SEO',
        slug: 'rankmath',
        type: 'plugin',
        price: 'free',
        provider: 'wordpress',
        description: 'Advanced SEO tools to help your content rank higher on search engines.',
    }
];

export function ThemePluginSelectionStep({ data, onUpdate }: Props) {
    const [activeTab, setActiveTab] = useState<'themes' | 'plugins'>('themes');

    const themes = RECOMMENDED_ASSETS.filter(a => a.type === 'theme');
    const plugins = RECOMMENDED_ASSETS.filter(a => a.type === 'plugin');

    const toggleTheme = (slug: string) => {
        const current = new Set(data.selectedThemes || []);
        if (current.has(slug)) {
            current.delete(slug);
        } else {
            current.clear(); // Typically one theme at a time
            current.add(slug);
        }
        onUpdate({ selectedThemes: Array.from(current) });
    };

    const togglePlugin = (slug: string) => {
        const current = new Set(data.selectedPlugins || []);
        if (current.has(slug)) {
            current.delete(slug);
        } else {
            current.add(slug);
        }
        onUpdate({ selectedPlugins: Array.from(current) });
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="text-center space-y-2">
                <h2 className="text-2xl font-bold">Design & Performance</h2>
                <p className="text-muted-foreground max-w-lg mx-auto">
                    Select a theme and essential plugins. We recommend keeping plugins to a minimum for speed and security.
                </p>
            </div>

            <div className="flex justify-center gap-2 md:gap-4 px-2">
                <Button
                    variant={activeTab === 'themes' ? 'default' : 'outline'}
                    onClick={() => setActiveTab('themes')}
                    className="flex-1 md:flex-none gap-2"
                    size="sm"
                >
                    <Layout className="h-4 w-4" /> Themes
                </Button>
                <Button
                    variant={activeTab === 'plugins' ? 'default' : 'outline'}
                    onClick={() => setActiveTab('plugins')}
                    className="flex-1 md:flex-none gap-2"
                    size="sm"
                >
                    <Puzzle className="h-4 w-4" /> Plugins
                </Button>
            </div>

            {/* Bridge Notice */}
            <div className="bg-blue-500/5 border border-blue-500/20 rounded-xl p-4 flex items-start gap-4 mx-auto max-w-2xl">
                <div className="bg-blue-500/10 p-2 rounded-lg">
                    <ShieldCheck className="h-5 w-5 text-blue-600" />
                </div>
                <div className="space-y-1">
                    <h4 className="text-sm font-bold text-blue-900 dark:text-blue-100 uppercase tracking-wider">BizOSaaS Safety First</h4>
                    <p className="text-xs text-blue-700/80 dark:text-blue-300/80 leading-relaxed">
                        By default, we implement the <strong>BizOSaaS Connect Bridge</strong>. This replaces multiple bloated plugins with a single secure interface for your analytics and CRM sync.
                    </p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
                {(activeTab === 'themes' ? themes : plugins).map((asset) => {
                    const isSelected = activeTab === 'themes'
                        ? (data.selectedThemes || []).includes(asset.slug)
                        : (data.selectedPlugins || []).includes(asset.slug);

                    const isBridge = asset.slug === 'bizosaas-bridge';

                    return (
                        <Card
                            key={asset.id}
                            className={`group relative overflow-hidden transition-all duration-300 hover:shadow-lg ${isSelected ? 'ring-2 ring-primary border-primary bg-primary/5' : ''
                                } ${isBridge ? 'opacity-90 grayscale-[0.5]' : ''}`}
                            onClick={() => activeTab === 'themes' ? toggleTheme(asset.slug) : togglePlugin(asset.slug)}
                        >
                            <CardContent className="p-0">
                                {asset.image && (
                                    <div className="h-24 md:h-32 w-full overflow-hidden bg-muted">
                                        <img src={asset.image} alt={asset.name} className="w-full h-full object-cover transition-transform group-hover:scale-105" />
                                    </div>
                                )}
                                <div className="p-4 space-y-3">
                                    <div className="flex justify-between items-start">
                                        <div className="space-y-1">
                                            <div className="flex items-center gap-2">
                                                <h3 className="font-bold text-sm">{asset.name}</h3>
                                                {asset.isRecommended && (
                                                    <Badge variant="secondary" className="bg-green-500/10 text-green-700 dark:text-green-400 text-[9px] h-4">
                                                        <Zap className="h-2 w-2 mr-1" /> Recommended
                                                    </Badge>
                                                )}
                                            </div>
                                            <p className="text-xs text-muted-foreground line-clamp-2">{asset.description}</p>
                                        </div>
                                        {isSelected ? (
                                            <CheckCircle className="h-5 w-5 text-primary flex-shrink-0" />
                                        ) : (
                                            <Circle className="h-5 w-5 text-muted-foreground/30 flex-shrink-0" />
                                        )}
                                    </div>

                                    <div className="flex items-center justify-between pt-2 border-t border-dashed">
                                        <div className="flex items-center gap-2">
                                            <span className="text-xs font-bold">
                                                {asset.price === 'free' ? 'Free' : `$${asset.price}`}
                                            </span>
                                            {asset.provider === 'envato' && <Badge variant="outline" className="text-[10px]">Envato</Badge>}
                                        </div>
                                        {asset.affiliateLink && (
                                            <a
                                                href={asset.affiliateLink}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-[10px] text-blue-600 hover:underline flex items-center gap-1"
                                                onClick={(e) => e.stopPropagation()}
                                            >
                                                View Source <ExternalLink className="h-2.5 w-2.5" />
                                            </a>
                                        )}
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    );
                })}
            </div>

            {/* Paid Asset Notice */}
            {(data.selectedThemes || []).some(slug => {
                const a = themes.find(t => t.slug === slug);
                return a && typeof a.price === 'number';
            }) && (
                    <div className="bg-yellow-500/10 border border-yellow-500/20 p-4 rounded-lg flex items-center gap-3 animate-in slide-in-from-top-2">
                        <Star className="h-5 w-5 text-yellow-600" />
                        <p className="text-sm text-yellow-800 dark:text-yellow-400 font-medium">
                            You've selected a premium asset. We'll handle the bulk-rate licensing for you as part of your onboarding package.
                        </p>
                    </div>
                )}
        </div>
    );
}
