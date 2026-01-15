import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { AnalyticsConfig } from '../types/onboarding';
import {
    BarChart3,
    Search,
    Sparkles,
    RefreshCw,
    CheckCircle2,
    Target,
    Rocket,
    AlertCircle,
    ChevronRight,
    Globe,
    Facebook,
    Activity,
    TrendingUp
} from 'lucide-react';
import { useUser } from '@clerk/nextjs';
import { toast } from 'sonner';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Badge } from '@/components/ui/badge';

interface Props {
    data: AnalyticsConfig;
    onUpdate: (data: Partial<AnalyticsConfig>) => void;
    websiteUrl?: string;
    isDiscoveringCloud?: boolean;
}

export function AnalyticsTrackingStep({ data, onUpdate, websiteUrl, isDiscoveringCloud }: Props) {
    const { user } = useUser();
    const [isDiscovering, setIsDiscovering] = React.useState(false);
    const [discovered, setDiscovered] = React.useState(false);

    const hasGoogleLink = user?.externalAccounts.some(acc => acc.provider.includes('google'));
    const hasMicrosoftLink = user?.externalAccounts.some(acc => acc.provider.includes('microsoft'));
    const isCloudConnected = hasGoogleLink || hasMicrosoftLink;

    const handleMagicConnect = async () => {
        setIsDiscovering(true);
        try {
            // Determine provider - default to google if checks fail but user clicked "Start Smart Integration"
            // (Assumes the button is only shown if isCloudConnected is true, or we fallback)
            const provider = hasGoogleLink ? 'oauth_google' : hasMicrosoftLink ? 'oauth_microsoft' : 'oauth_google';

            // 1. Kick off the backend provisioning (Real API / "Magic" Discovery)
            // We fire this but don't blocking-wait for its complex result to populate UI
            // We rely on the standard discovery endpoint for the UI data structure.
            if (provider.includes('google')) {
                fetch('/api/brain/onboarding/google/discover', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        access_token: "user_session_token",
                        dry_run: true
                    })
                }).catch(err => console.error("Background discovery trigger failed", err));
            }

            // 2. Fetch the UI-ready data structure (Standard Discovery)
            const discoverRes = await fetch('/api/brain/onboarding/discover', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: user?.primaryEmailAddress?.emailAddress || "user@example.com",
                    provider: provider
                })
            });

            if (discoverRes.ok) {
                const discoData = await discoverRes.json();

                // Merge Google and Microsoft results if both present, or just use relevant
                const gList = discoData.discovery.google || [];
                const mList = discoData.discovery.microsoft || [];
                const allList = [...gList, ...mList];

                if (gList.length > 0 || mList.length > 0) {
                    onUpdate({
                        // Google Assets
                        availableGtmContainers: gList.filter((s: any) => s.type === 'gtm_container').map((s: any) => ({ id: s.id, name: s.name })),
                        availableGaProperties: gList.filter((s: any) => s.type === 'ga4_property').map((s: any) => ({ id: s.id, name: s.name })),
                        availableGscSites: gList.filter((s: any) => s.type === 'gsc_site').map((s: any) => ({ id: s.id, name: s.name })),
                        availableFbPixels: gList.filter((s: any) => s.type === 'fb_analytics').map((s: any) => ({ id: s.id, name: s.name })),

                        // Microsoft Assets
                        availableClarityProjects: mList.filter((s: any) => s.type === 'clarity_project').map((s: any) => ({ id: s.id, name: s.name })),
                        availableBingProfiles: mList.filter((s: any) => s.type === 'bing_profile').map((s: any) => ({ id: s.id, name: s.name })),

                        // Smart Selections (Auto-select first available if currently empty)
                        gtmId: data.gtmId || gList.find((s: any) => s.type === 'gtm_container')?.id,
                        gaId: data.gaId || gList.find((s: any) => s.type === 'ga4_property')?.id,
                        gscId: data.gscId || gList.find((s: any) => s.type === 'gsc_site')?.id,
                        fbId: data.fbId || gList.find((s: any) => s.type === 'fb_analytics')?.id,
                        clarityId: data.clarityId || mList.find((s: any) => s.type === 'clarity_project')?.id,
                        bingId: data.bingId || mList.find((s: any) => s.type === 'bing_profile')?.id,

                        // Mark as audited/discovered
                        auditedServices: {
                            essential: [
                                { id: '1', name: 'Cloud Integration', service: 'Google/Microsoft', status: 'active' }
                            ],
                            optional: []
                        }
                    });
                    setDiscovered(true);
                    toast.success("Sync complete! Cloud assets have been retrieved.");
                } else {
                    toast.info("No supported marketing assets found in this account.");
                }
            } else {
                throw new Error("Discovery API failed");
            }

        } catch (error) {
            console.error(error);
            toast.error("Discovery failed. Please try manual entry.");
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

            {isDiscoveringCloud ? (
                <div className="bg-blue-600/5 dark:bg-blue-600/10 border border-blue-600/20 rounded-xl p-8 mb-8 flex flex-col items-center justify-center text-center animate-pulse">
                    <RefreshCw className="w-10 h-10 text-blue-600 animate-spin mb-4" />
                    <h3 className="text-xl font-bold text-foreground mb-2">Syncing Cloud Intelligence...</h3>
                    <p className="text-muted-foreground max-w-sm">We are pulling your property IDs from your connected Google and Microsoft accounts to pre-populate this view.</p>
                </div>
            ) : isCloudConnected && !data.auditedServices && (
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
                <div className="border-2 border-primary/20 rounded-xl p-5 bg-primary/5 space-y-4 relative overflow-hidden group hover:border-primary/40 transition-colors">
                    <div className="absolute top-0 right-0 bg-primary text-white text-[10px] px-2 py-0.5 font-bold uppercase tracking-widest rounded-bl-lg">
                        Priority
                    </div>
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-primary p-2 rounded-lg text-white shadow-md">
                                <Sparkles size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-bold">Google Tag Manager</Label>
                                <p className="text-xs text-muted-foreground">Central hub for tracking pixels & events.</p>
                            </div>
                        </div>
                        <Badge variant="secondary" className="bg-primary/10 text-primary border-none">
                            Required
                        </Badge>
                    </div>

                    <div className="pt-2 border-t border-primary/10 mt-2 space-y-3">
                        {data.availableGtmContainers && data.availableGtmContainers.length > 0 ? (
                            <div className="space-y-2">
                                <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">Select Container</p>
                                <Select
                                    value={data.gtmId}
                                    onValueChange={(val) => onUpdate({ gtmId: val })}
                                >
                                    <SelectTrigger className="w-full bg-card/50 backdrop-blur-sm border-primary/20">
                                        <SelectValue placeholder="Choose GTM Container" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {data.availableGtmContainers.map(container => (
                                            <SelectItem key={container.id} value={container.id}>
                                                <div className="flex flex-col">
                                                    <span className="font-medium">{container.name}</span>
                                                    <span className="text-[10px] text-muted-foreground">{container.id}</span>
                                                </div>
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                        ) : (
                            <Input
                                placeholder="GTM-XXXXXXX"
                                className="h-10 text-sm bg-card/50"
                                value={data.gtmId}
                                onChange={(e) => onUpdate({ gtmId: e.target.value })}
                            />
                        )}
                    </div>
                </div>

                {/* Google Analytics 4 */}
                <div className="border rounded-xl p-5 bg-card/50 backdrop-blur-sm space-y-4 group hover:border-slate-300 transition-colors">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-orange-100 dark:bg-orange-950/30 p-2 rounded-lg text-orange-600">
                                <BarChart3 size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-semibold">Google Analytics 4</Label>
                                <p className="text-xs text-muted-foreground">Property for user behavioral insights.</p>
                            </div>
                        </div>
                        {data.gaId ? (
                            <div className="flex items-center gap-1 text-green-600 text-xs font-bold">
                                <CheckCircle2 size={12} /> Linked
                            </div>
                        ) : (
                            <Button variant="ghost" size="sm" className="h-8 text-xs">Manual Link</Button>
                        )}
                    </div>

                    <div className="pt-2 border-t mt-2 space-y-3">
                        {data.availableGaProperties && data.availableGaProperties.length > 0 ? (
                            <div className="space-y-2">
                                <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">Select Property</p>
                                <Select
                                    value={data.gaId}
                                    onValueChange={(val) => onUpdate({ gaId: val })}
                                >
                                    <SelectTrigger className="w-full bg-background/50">
                                        <SelectValue placeholder="Choose GA4 Property" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {data.availableGaProperties.map(prop => (
                                            <SelectItem key={prop.id} value={prop.id}>
                                                <div className="flex flex-col">
                                                    <span className="font-medium">{prop.name}</span>
                                                    <span className="text-[10px] text-muted-foreground">ID: {prop.id}</span>
                                                </div>
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                        ) : (
                            <Input
                                placeholder="G-XXXXXXXXXX"
                                className="h-10 text-sm"
                                value={data.gaId}
                                onChange={(e) => onUpdate({ gaId: e.target.value })}
                            />
                        )}
                    </div>
                </div>

                {/* Search Console */}
                <div className="border rounded-xl p-5 bg-card/50 backdrop-blur-sm space-y-4 hover:border-slate-300 transition-colors">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-blue-100 dark:bg-blue-950/30 p-2 rounded-lg text-blue-600">
                                <Search size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-semibold">Search Console</Label>
                                <p className="text-xs text-muted-foreground">Verified site for SEO health.</p>
                            </div>
                        </div>
                    </div>

                    <div className="pt-2 border-t mt-2 space-y-2">
                        {data.availableGscSites && data.availableGscSites.length > 0 ? (
                            <Select
                                value={data.gscId}
                                onValueChange={(val) => onUpdate({ gscId: val })}
                            >
                                <SelectTrigger className="w-full bg-background/50">
                                    <SelectValue placeholder="Choose Site Profile" />
                                </SelectTrigger>
                                <SelectContent>
                                    {data.availableGscSites.map(site => (
                                        <SelectItem key={site.id} value={site.id}>
                                            <div className="flex items-center gap-2">
                                                <Globe size={14} className="text-muted-foreground" />
                                                <span>{site.name}</span>
                                            </div>
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        ) : (
                            <Input
                                placeholder="https://example.com"
                                className="h-10 text-sm"
                                value={data.gscId}
                                onChange={(e) => onUpdate({ gscId: e.target.value })}
                            />
                        )}
                    </div>
                </div>

                {/* Meta Pixel / Facebook Analytics */}
                <div className="border rounded-xl p-5 bg-card/50 backdrop-blur-sm space-y-4 hover:border-slate-300 transition-colors">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-blue-50 dark:bg-blue-950/20 p-2 rounded-lg text-blue-700">
                                <Facebook size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-semibold">Meta Pixel</Label>
                                <p className="text-xs text-muted-foreground">Track conversions for Facebook ads.</p>
                            </div>
                        </div>
                        <Badge variant="outline" className="text-[10px] font-normal">Optional</Badge>
                    </div>

                    <div className="pt-2 border-t mt-2 space-y-2">
                        {data.availableFbPixels && data.availableFbPixels.length > 0 ? (
                            <Select
                                value={data.fbId}
                                onValueChange={(val) => onUpdate({ fbId: val })}
                            >
                                <SelectTrigger className="w-full bg-background/50">
                                    <SelectValue placeholder="Choose Meta Pixel" />
                                </SelectTrigger>
                                <SelectContent>
                                    {data.availableFbPixels.map(pixel => (
                                        <SelectItem key={pixel.id} value={pixel.id}>
                                            <div className="flex flex-col">
                                                <span className="font-medium">{pixel.name}</span>
                                                <span className="text-[10px] text-muted-foreground">{pixel.id}</span>
                                            </div>
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        ) : (
                            <Input
                                placeholder="Pixel ID (e.g. 123456789)"
                                className="h-10 text-sm"
                                value={data.fbId}
                                onChange={(e) => onUpdate({ fbId: e.target.value })}
                            />
                        )}
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Microsoft Clarity */}
                    <div className="border rounded-xl p-5 bg-card/50 backdrop-blur-sm space-y-4 hover:border-slate-300 transition-colors">
                        <div className="flex items-start justify-between">
                            <div className="flex items-center gap-3">
                                <div className="bg-orange-50 dark:bg-orange-950/20 p-2 rounded-lg text-orange-600">
                                    <Activity size={20} />
                                </div>
                                <div className="space-y-1">
                                    <Label className="text-sm font-semibold">Microsoft Clarity</Label>
                                    <p className="text-[10px] text-muted-foreground">Heatmaps & recordings.</p>
                                </div>
                            </div>
                        </div>

                        <div className="pt-2 border-t mt-2">
                            {data.availableClarityProjects && data.availableClarityProjects.length > 0 ? (
                                <Select
                                    value={data.clarityId}
                                    onValueChange={(val) => onUpdate({ clarityId: val })}
                                >
                                    <SelectTrigger className="w-full bg-background/50 h-9 text-xs">
                                        <SelectValue placeholder="Select Project" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {data.availableClarityProjects.map(proj => (
                                            <SelectItem key={proj.id} value={proj.id} className="text-xs">
                                                {proj.name}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            ) : (
                                <Input
                                    placeholder="Project ID"
                                    className="h-9 text-xs"
                                    value={data.clarityId}
                                    onChange={(e) => onUpdate({ clarityId: e.target.value })}
                                />
                            )}
                        </div>
                    </div>

                    {/* Bing Analytics */}
                    <div className="border rounded-xl p-5 bg-card/50 backdrop-blur-sm space-y-4 hover:border-slate-300 transition-colors">
                        <div className="flex items-start justify-between">
                            <div className="flex items-center gap-3">
                                <div className="bg-teal-50 dark:bg-teal-950/20 p-2 rounded-lg text-teal-600">
                                    <TrendingUp size={20} />
                                </div>
                                <div className="space-y-1">
                                    <Label className="text-sm font-semibold">Bing Webmaster</Label>
                                    <p className="text-[10px] text-muted-foreground">Microsoft search performance.</p>
                                </div>
                            </div>
                        </div>

                        <div className="pt-2 border-t mt-2">
                            {data.availableBingProfiles && data.availableBingProfiles.length > 0 ? (
                                <Select
                                    value={data.bingId}
                                    onValueChange={(val) => onUpdate({ bingId: val })}
                                >
                                    <SelectTrigger className="w-full bg-background/50 h-9 text-xs">
                                        <SelectValue placeholder="Select Profile" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {data.availableBingProfiles.map(prof => (
                                            <SelectItem key={prof.id} value={prof.id} className="text-xs">
                                                {prof.name}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            ) : (
                                <Input
                                    placeholder="Profile ID"
                                    className="h-9 text-xs"
                                    value={data.bingId}
                                    onChange={(e) => onUpdate({ bingId: e.target.value })}
                                />
                            )}
                        </div>
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
