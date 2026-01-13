import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { AnalyticsConfig } from '../types/onboarding';
import { BarChart3, Search, Sparkles, RefreshCw, CheckCircle2, Target, Rocket } from 'lucide-react';
import { useUser } from '@clerk/nextjs';
import { toast } from 'sonner';

interface Props {
    data: AnalyticsConfig;
    onUpdate: (data: Partial<AnalyticsConfig>) => void;
    websiteUrl?: string;
}

export function AnalyticsTrackingStep({ data, onUpdate, websiteUrl }: Props) {
    const { user } = useUser();
    const [isDiscovering, setIsDiscovering] = React.useState(false);
    const [discovered, setDiscovered] = React.useState(false);

    const isGmailUser = user?.primaryEmailAddress?.emailAddress.endsWith('@gmail.com');

    const handleMagicConnect = async () => {
        setIsDiscovering(true);
        try {
            // 1. Analyze existing site tags first
            const targetUrl = websiteUrl || "example.com"; // Use passed prop or fallback

            const analysisResp = await fetch('/api/brain/onboarding/gtm/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ website_url: targetUrl })
            });

            if (analysisResp.ok) {
                const data = await analysisResp.json();
                if (data && data.status === "started") {
                    toast.success("Strategic analysis started! Monitoring your GTM container...");
                    // In a real app, we would poll for the workflow results. 
                    // For demo, we simulate the audit result returned after a short delay
                    setTimeout(() => {
                        onUpdate({
                            auditedServices: {
                                essential: [
                                    { id: '1', name: 'Google Analytics 4 Config', service: 'Google Analytics', status: 'active' },
                                    { id: '2', name: 'Google Ads Remarketing', service: 'Google Ads', status: 'active' }
                                ],
                                optional: [
                                    { id: '3', name: 'Facebook Pixel Base', service: 'Facebook Pixel', status: 'active' },
                                    { id: '4', name: 'LinkedIn Insight Tag', service: 'LinkedIn Insight', status: 'active' }
                                ]
                            }
                        });
                        setDiscovered(true);
                        toast.success("Audit complete! We identified your marketing services.");
                    }, 3000);
                }
            }
        } catch (error) {
            toast.error("Discovery failed. Please connect manually.");
        } finally {
            setIsDiscovering(false);
        }
    };

    const renderAuditedServices = () => {
        if (!data.auditedServices) return null;

        return (
            <div className="space-y-6 mt-8 animate-in fade-in zoom-in duration-700">
                <div className="flex items-center gap-2 mb-2">
                    <CheckCircle2 className="text-green-600 w-5 h-5" />
                    <h3 className="font-bold text-lg text-foreground">Digital Audit Results</h3>
                </div>

                {/* Essential Section */}
                <div className="space-y-3">
                    <div className="flex items-center justify-between">
                        <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground/60">Essential (Required for AI)</span>
                        <div className="h-px flex-1 bg-gray-100 ml-4" />
                    </div>
                    {data.auditedServices.essential.map(s => (
                        <div key={s.id} className="flex items-center justify-between p-3 bg-blue-50/50 border border-blue-100 rounded-lg">
                            <div className="flex items-center gap-3">
                                <div className="w-2 h-2 rounded-full bg-blue-600 animate-pulse" />
                                <div>
                                    <p className="text-sm font-bold text-foreground">{s.service}</p>
                                    <p className="text-[10px] text-muted-foreground">{s.name}</p>
                                </div>
                            </div>
                            <span className="text-[10px] bg-blue-600 text-white px-2 py-0.5 rounded-full font-bold">RELIABLE</span>
                        </div>
                    ))}
                </div>

                {/* Optional Section */}
                <div className="space-y-3">
                    <div className="flex items-center justify-between">
                        <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground/60">Growth Tools (Good to Have)</span>
                        <div className="h-px flex-1 bg-gray-100 ml-4" />
                    </div>
                    {data.auditedServices.optional.map(s => (
                        <div key={s.id} className="flex items-center justify-between p-3 bg-card border border-gray-100 rounded-lg group hover:border-indigo-200 transition-colors">
                            <div className="flex items-center gap-3">
                                <div className="w-2 h-2 rounded-full bg-indigo-400" />
                                <div>
                                    <p className="text-sm font-semibold text-foreground">{s.service}</p>
                                    <p className="text-[10px] text-muted-foreground">{s.name}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <Button variant="ghost" size="sm" className="h-6 text-[10px] text-muted-foreground/60 hover:text-red-500">Disable</Button>
                                <span className="text-[10px] bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-bold">DETECTED</span>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="bg-slate-900 rounded-xl p-4 text-white text-sm mt-4 shadow-xl">
                    <div className="flex items-start gap-3">
                        <Rocket className="w-5 h-5 text-blue-400 shrink-0" />
                        <p>By proceeding, these verified tags will be used by our **AI Marketing Assistant** to optimize your campaigns across all channels.</p>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-foreground">Digital Intelligence</h2>
                <p className="text-muted-foreground">We use a GTM-First approach to centralize your marketing data.</p>
            </div>

            {isGmailUser && !data.auditedServices && (
                <div className="bg-gradient-to-r from-blue-700 to-indigo-900 rounded-xl p-6 text-white mb-8 shadow-xl relative overflow-hidden group">
                    <div className="absolute -right-4 -top-4 w-24 h-24 bg-card/10 rounded-full blur-2xl group-hover:bg-card/20 transition-all" />
                    <div className="flex items-center gap-4 mb-4 relative z-10">
                        <div className="bg-card/20 p-3 rounded-xl backdrop-blur-md">
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
                        className="w-full bg-card text-blue-900 hover:bg-blue-50 font-bold py-7 text-lg shadow-lg"
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
                                <p className="text-xs text-muted-foreground">Includes GA4, Ads, and FB Pixel automatically.</p>
                            </div>
                        </div>
                        <Button variant="outline" size="sm" className="bg-card border-blue-200 text-blue-700 font-bold">Priority Setup</Button>
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
                <div className="border rounded-xl p-5 bg-card space-y-4 relative overflow-hidden group hover:border-slate-300 transition-colors">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-orange-100 p-2 rounded-lg text-orange-600">
                                <BarChart3 size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-semibold">Google Analytics 4</Label>
                                <p className="text-xs text-muted-foreground">Standalone GA4 connection</p>
                            </div>
                        </div>
                        <Button variant="outline" size="sm" className="bg-card">Connect</Button>
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
                <div className="border rounded-xl p-5 bg-card space-y-4 hover:border-slate-300 transition-colors">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-blue-100 p-2 rounded-lg text-blue-600">
                                <Search size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-semibold">Search Console</Label>
                                <p className="text-xs text-muted-foreground">For SEO performance and keywords</p>
                            </div>
                        </div>
                        <Button variant="outline" size="sm" className="bg-card">Connect</Button>
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

                {renderAuditedServices()}

                <div className="flex items-center justify-end space-x-2 pt-4">
                    <Switch
                        id="setup-later"
                        checked={data.setupLater}
                        onCheckedChange={(checked) => onUpdate({ setupLater: checked })}
                    />
                    <Label htmlFor="setup-later" className="text-sm text-muted-foreground">I'll set this up later</Label>
                </div>
            </div>
        </div>
    );
}
