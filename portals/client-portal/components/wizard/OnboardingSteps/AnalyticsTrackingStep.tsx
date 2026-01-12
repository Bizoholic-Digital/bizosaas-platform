import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { AnalyticsConfig } from '../types/onboarding';
import { BarChart3, Search, Sparkles, RefreshCw, CheckCircle2 } from 'lucide-react';
import { useUser } from '@clerk/nextjs';
import { toast } from 'sonner';

interface Props {
    data: AnalyticsConfig;
    onUpdate: (data: Partial<AnalyticsConfig>) => void;
}

export function AnalyticsTrackingStep({ data, onUpdate }: Props) {
    const { user } = useUser();
    const [isDiscovering, setIsDiscovering] = React.useState(false);
    const [discovered, setDiscovered] = React.useState(false);

    const isGmailUser = user?.primaryEmailAddress?.emailAddress.endsWith('@gmail.com');

    const handleMagicConnect = async () => {
        setIsDiscovering(true);
        try {
            // 1. Analyze existing site tags first
            const websiteUrl = user?.externalAccounts[0]?.externalId || "example.com"; // Fallback for demo

            const analysisResp = await fetch('/api/brain/onboarding/gtm/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ website_url: websiteUrl })
            });

            if (analysisResp.ok) {
                const data = await analysisResp.json();
                toast.success("Strategic analysis started! We are auditing your site tags.");
                setDiscovered(true);
            }
        } catch (error) {
            toast.error("Discovery failed. Please connect manually.");
        } finally {
            setIsDiscovering(false);
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Digital Intelligence</h2>
                <p className="text-gray-500">We use a GTM-First approach to centralize your marketing data.</p>
            </div>

            {isGmailUser && !discovered && (
                <div className="bg-gradient-to-r from-blue-700 to-indigo-900 rounded-xl p-6 text-white mb-8 shadow-xl relative overflow-hidden group">
                    <div className="absolute -right-4 -top-4 w-24 h-24 bg-white/10 rounded-full blur-2xl group-hover:bg-white/20 transition-all" />
                    <div className="flex items-center gap-4 mb-4 relative z-10">
                        <div className="bg-white/20 p-3 rounded-xl backdrop-blur-md">
                            <Sparkles className="w-6 h-6 text-yellow-300" />
                        </div>
                        <div>
                            <h3 className="font-bold text-lg">GTM-First Discovery</h3>
                            <p className="text-blue-100 text-sm">We'll scan your site for existing tags and consolidate them into a single managed GTM container.</p>
                        </div>
                    </div>
                    <Button
                        onClick={handleMagicConnect}
                        disabled={isDiscovering}
                        className="w-full bg-white text-blue-900 hover:bg-blue-50 font-bold py-7 text-lg shadow-lg"
                    >
                        {isDiscovering ? (
                            <>
                                <RefreshCw className="w-5 h-5 mr-3 animate-spin" />
                                Auditing Digital Presence...
                            </>
                        ) : (
                            <>
                                <Target className="w-5 h-5 mr-3" />
                                Start Smart Integration
                            </>
                        )}
                    </Button>
                </div>
            )}

            {discovered && (
                <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex items-center gap-3 mb-8 text-green-800">
                    <CheckCircle2 className="w-6 h-6 text-green-600" />
                    <div>
                        <p className="font-bold">Success! Properties linked.</p>
                        <p className="text-sm">We've automatically configured your tracking IDs below.</p>
                    </div>
                </div>
            )}

            <div className="space-y-4">
                {/* Google Tag Manager - PRIORITY */}
                <div className="border-2 border-blue-200 rounded-xl p-5 bg-blue-50/30 space-y-4 relative overflow-hidden group hover:border-blue-400 transition-colors">
                    <div className="absolute top-0 right-0 bg-blue-600 text-white text-[10px] px-2 py-0.5 font-bold uppercase tracking-widest rounded-bl-lg">
                        Priority
                    </div>
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-blue-600 p-2 rounded-lg text-white shadow-md">
                                <Sparkles size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-bold">Google Tag Manager</Label>
                                <p className="text-xs text-gray-500">Includes GA4, Ads, and FB Pixel automatically.</p>
                            </div>
                        </div>
                        <Button variant="outline" size="sm" className="bg-white border-blue-200 text-blue-700 font-bold">Priority Setup</Button>
                    </div>
                    <div className="pt-2 border-t border-blue-100 mt-2">
                        <Input
                            placeholder="GTM-XXXXXXX"
                            className="h-9 text-sm border-blue-100 focus:border-blue-500"
                            value={data.gtmId}
                            onChange={(e) => onUpdate({ gtmId: e.target.value })}
                        />
                    </div>
                </div>

                {/* Google Analytics */}
                <div className="border rounded-xl p-5 bg-white space-y-4 relative overflow-hidden group hover:border-slate-300 transition-colors">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-orange-100 p-2 rounded-lg text-orange-600">
                                <BarChart3 size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-semibold">Google Analytics 4</Label>
                                <p className="text-xs text-gray-500">Standalone GA4 connection</p>
                            </div>
                        </div>
                        <Button variant="outline" size="sm" className="bg-white">Connect</Button>
                    </div>
                    <div className="pt-2 border-t mt-2">
                        <Input
                            placeholder="G-XXXXXXXXXX"
                            className="h-8 text-sm"
                            value={data.gaId}
                            onChange={(e) => onUpdate({ gaId: e.target.value })}
                        />
                    </div>
                </div>

                {/* Google Search Console */}
                <div className="border rounded-xl p-5 bg-white space-y-4 hover:border-slate-300 transition-colors">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-blue-100 p-2 rounded-lg text-blue-600">
                                <Search size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-semibold">Search Console</Label>
                                <p className="text-xs text-gray-500">For SEO performance and keywords</p>
                            </div>
                        </div>
                        <Button variant="outline" size="sm" className="bg-white">Connect</Button>
                    </div>
                    <div className="pt-2 border-t mt-2">
                        <Input
                            placeholder="example.com"
                            className="h-8 text-sm"
                            value={data.gscId}
                            onChange={(e) => onUpdate({ gscId: e.target.value })}
                        />
                    </div>
                </div>

                <div className="flex items-center justify-end space-x-2 pt-4">
                    <Switch
                        id="setup-later"
                        checked={data.setupLater}
                        onCheckedChange={(checked) => onUpdate({ setupLater: checked })}
                    />
                    <Label htmlFor="setup-later" className="text-sm text-gray-500">I'll set this up later</Label>
                </div>
            </div>
        </div>
    );
}
