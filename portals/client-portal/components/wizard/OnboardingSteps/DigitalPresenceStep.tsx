import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { DigitalPresence } from '../types/onboarding';
import { Globe, Layout, Database, Search, CheckCircle2, Sparkles, Loader2, ShieldCheck, Zap, ShoppingBag, RefreshCcw } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Progress } from '@/components/ui/progress';

interface Props {
    data: DigitalPresence;
    websiteUrl?: string;
    onUpdate: (data: Partial<DigitalPresence>) => void;
    isAuditing?: boolean;
    auditedServices?: any;
    onRerunAudit?: () => void;
}

const SCAN_MESSAGES = [
    "Establishing secure connection...",
    "Analyzing HTML headers & meta tags...",
    "Scanning for Google Tag Manager (GTM)...",
    "Identifying Google Analytics 4 (GA4)...",
    "Checking for Facebook Pixel & LinkedIn Insight...",
    "Verifying container triggers...",
    "Finalizing digital footprint analysis..."
];

export function DigitalPresenceStep({ data, websiteUrl, onUpdate, isAuditing, auditedServices, onRerunAudit }: Props) {
    const [scanProgress, setScanProgress] = React.useState(0);
    const [statusIndex, setStatusIndex] = React.useState(0);

    // Progress Simulation Logic
    React.useEffect(() => {
        let timer: any;
        let msgTimer: any;

        if (isAuditing) {
            setScanProgress(0);
            setStatusIndex(0);

            // Increment progress bar
            timer = setInterval(() => {
                setScanProgress(prev => {
                    if (prev >= 95) return prev;
                    return prev + (Math.random() * 8);
                });
            }, 300);

            // Cycle through status messages
            msgTimer = setInterval(() => {
                setStatusIndex(prev => (prev + 1) % SCAN_MESSAGES.length);
            }, 600);
        } else if (auditedServices) {
            setScanProgress(100);
            setStatusIndex(SCAN_MESSAGES.length - 1);
        }

        return () => {
            clearInterval(timer);
            clearInterval(msgTimer);
        };
    }, [isAuditing, auditedServices]);

    // Adaptive logic: If website was detected/provided in step 1, we show that
    const renderWebsiteStatus = () => {
        const isDirectory = websiteUrl?.includes('directory.bizoholic.net') || (websiteUrl?.includes('bizoholic.net') && !websiteUrl?.includes('app.') && !websiteUrl?.includes('admin.') && !websiteUrl?.includes('api.'));
        if (websiteUrl) {
            return (
                <div className={`border rounded-lg p-4 flex items-center gap-3 mb-6 ${isDirectory ? 'bg-blue-500/10 border-blue-500/20' : 'bg-green-500/10 border-green-500/20'}`}>
                    <div className={`${isDirectory ? 'bg-blue-500/20' : 'bg-green-500/20'} p-2 rounded-full`}>
                        {isDirectory ? <Sparkles className="text-blue-600 dark:text-blue-400 h-5 w-5" /> : <Globe className="text-green-600 dark:text-green-400 h-5 w-5" />}
                    </div>
                    <div>
                        <p className={`font-semibold ${isDirectory ? 'text-blue-700 dark:text-blue-400' : 'text-green-700 dark:text-green-400'}`}>
                            {isDirectory ? 'Directory Profile Active' : 'Website Detected'}
                        </p>
                        <p className={`text-sm ${isDirectory ? 'text-blue-600/80 dark:text-blue-400/80' : 'text-green-600/80 dark:text-green-400/80'}`}>{websiteUrl}</p>
                    </div>
                </div>
            );
        }
        return (
            <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-4 flex items-center gap-3 mb-6">
                <div className="bg-yellow-500/20 p-2 rounded-full">
                    <Globe className="text-yellow-600 dark:text-yellow-400 h-5 w-5" />
                </div>
                <div>
                    <p className="font-semibold text-yellow-700 dark:text-yellow-400">No Digital Presence</p>
                    <p className="text-sm text-yellow-600/80 dark:text-yellow-400/80">We recommend setting up a directory listing in the first step.</p>
                </div>
            </div>
        );
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-foreground">Digital Presence</h2>
                <p className="text-muted-foreground">Connect your existing tech stack.</p>
            </div>

            {renderWebsiteStatus()}

            <div className="space-y-8">
                {/* 1. Tracking Scripts & Auto-Discovery (Moved to Top) */}
                <div className="border-2 border-blue-500/20 rounded-2xl p-6 bg-blue-50/30 dark:bg-blue-900/10 space-y-4 shadow-xl shadow-blue-500/5 transition-all duration-500 hover:border-blue-500/40">
                    <div className="flex items-center justify-between">
                        <div className="space-y-1 text-left">
                            <Label className="text-lg font-black flex items-center gap-2 text-blue-700 dark:text-blue-400 uppercase tracking-tighter">
                                <Search className="h-5 w-5" /> Site Discovery
                            </Label>
                            <p className="text-sm text-blue-600/70 dark:text-blue-400/60 font-medium">Detect CMS, CRM, and Analytics automatically.</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <span className="text-[10px] font-black uppercase tracking-widest text-blue-600/50">Auto-Scan</span>
                            <Switch
                                checked={data.hasTracking}
                                onCheckedChange={(checked) => {
                                    onUpdate({ hasTracking: checked });
                                    if (checked && onRerunAudit) {
                                        onRerunAudit();
                                    }
                                }}
                                className="data-[state=checked]:bg-blue-600"
                            />
                        </div>
                    </div>

                    {data.hasTracking && (
                        <div className="pt-4 border-t border-blue-500/10 border-dashed">
                            {isAuditing ? (
                                <div className="space-y-4 bg-white/50 dark:bg-slate-900/50 p-5 rounded-2xl border border-blue-100 dark:border-blue-900/30 shadow-sm transition-all duration-500">
                                    <div className="flex justify-between items-end mb-1">
                                        <div className="space-y-1 text-left">
                                            <div className="flex items-center gap-2 text-blue-600">
                                                <Zap className="h-4 w-4 animate-pulse fill-blue-600/20" />
                                                <span className="text-sm font-black uppercase tracking-tighter">Analyzing Ecosystem</span>
                                            </div>
                                            <p className="text-xs text-muted-foreground font-medium animate-in fade-in slide-in-from-left-2 duration-300 h-4" key={statusIndex}>
                                                {SCAN_MESSAGES[statusIndex]}
                                            </p>
                                        </div>
                                        <span className="text-xs font-black font-mono text-blue-600 bg-blue-50 dark:bg-blue-900/40 px-2 py-0.5 rounded-full">{Math.round(scanProgress)}%</span>
                                    </div>
                                    <Progress value={scanProgress} className="h-2.5 bg-blue-100 dark:bg-blue-900/20" />
                                    <p className="text-[10px] text-center text-blue-600/40 font-bold uppercase tracking-widest">
                                        Detecting infrastructure for {websiteUrl || 'your website'}
                                    </p>
                                </div>
                            ) : auditedServices ? (
                                <div className="space-y-4 animate-in slide-in-from-top-2 duration-500">
                                    <div className="flex items-center gap-3 text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20 p-4 rounded-2xl border border-green-200 dark:border-green-800/30 shadow-sm">
                                        <div className="bg-green-600 p-2 rounded-xl text-white shadow-lg shadow-green-200 dark:shadow-none">
                                            <ShieldCheck className="h-5 w-5" />
                                        </div>
                                        <div className="text-left flex-1">
                                            <span className="text-sm font-black uppercase tracking-tight leading-none block mb-0.5">Discovery Successful</span>
                                            <p className="text-xs text-green-600/80 font-medium">We've identified {auditedServices.essential.length + auditedServices.optional.length} services in your stack.</p>
                                        </div>
                                        {onRerunAudit && (
                                            <button
                                                onClick={onRerunAudit}
                                                className="p-2 hover:bg-green-100 dark:hover:bg-green-800/40 rounded-lg transition-colors text-green-700"
                                                title="Rescan Website"
                                            >
                                                <RefreshCcw className="h-4 w-4" />
                                            </button>
                                        )}
                                    </div>
                                    <div className="flex flex-wrap gap-2 px-1">
                                        {/* Summarized Essential Tags */}
                                        {Object.entries(
                                            (auditedServices?.essential || []).reduce((acc: any, s: any) => {
                                                acc[s.service] = (acc[s.service] || 0) + 1;
                                                return acc;
                                            }, {})
                                        ).map(([service, count]: [string, any]) => (
                                            <span key={service} className="text-[10px] bg-blue-600 text-white px-3 py-1.5 rounded-full font-black uppercase tracking-widest flex items-center gap-2 shadow-md shadow-blue-200 dark:shadow-none">
                                                <Sparkles className="h-3 w-3" /> {count > 1 ? `${count} ${service} Tags` : service}
                                            </span>
                                        ))}

                                        {/* Detailed breakdown for transparency */}
                                        {(auditedServices?.optional || []).map((s: any) => (
                                            <span key={s.id} className="text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 px-3 py-1.5 rounded-full font-bold uppercase tracking-widest border border-slate-200 dark:border-slate-700">
                                                {s.service}: {s.name}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            ) : (
                                <div className="flex flex-col items-center justify-center py-8 text-muted-foreground/30 space-y-3 bg-white/30 dark:bg-slate-900/30 rounded-2xl border-2 border-dashed border-blue-500/10">
                                    <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-full animate-bounce">
                                        <Search className="h-6 w-6 text-blue-500/50" />
                                    </div>
                                    <p className="text-xs font-bold uppercase tracking-widest">Ready to scan {websiteUrl || 'website'}...</p>
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* 2. Audit Results Visualization (Moved up for immediate feedback) */}
                {auditedServices && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 animate-in fade-in zoom-in-95 duration-700">
                        {data.cmsType && (
                            <div className="flex items-center gap-3 p-4 rounded-2xl bg-blue-600 text-white shadow-lg shadow-blue-200 dark:shadow-none transition-transform hover:scale-[1.02]">
                                <div className="p-2 bg-white/20 rounded-xl">
                                    <Layout className="w-5 h-5" />
                                </div>
                                <div className="text-left">
                                    <p className="text-[8px] font-black uppercase tracking-widest leading-none mb-1 opacity-70">Infrastructure</p>
                                    <p className="text-sm font-black capitalize leading-none">{data.cmsType}</p>
                                </div>
                                <CheckCircle2 className="w-4 h-4 ml-auto opacity-50" />
                            </div>
                        )}
                        {data.crmType && data.crmType !== 'none' && (
                            <div className="flex items-center gap-3 p-4 rounded-2xl bg-purple-600 text-white shadow-lg shadow-purple-200 dark:shadow-none transition-transform hover:scale-[1.02]">
                                <div className="p-2 bg-white/20 rounded-xl">
                                    <Database className="w-5 h-5" />
                                </div>
                                <div className="text-left">
                                    <p className="text-[8px] font-black uppercase tracking-widest leading-none mb-1 opacity-70">Growth Stack</p>
                                    <p className="text-sm font-black capitalize leading-none">{data.crmType}</p>
                                </div>
                                <CheckCircle2 className="w-4 h-4 ml-auto opacity-50" />
                            </div>
                        )}
                        {data.ecommerceType && data.ecommerceType !== 'none' && (
                            <div className="flex items-center gap-3 p-4 rounded-2xl bg-orange-600 text-white shadow-lg shadow-orange-200 dark:shadow-none transition-transform hover:scale-[1.02]">
                                <div className="p-2 bg-white/20 rounded-xl">
                                    <ShoppingBag className="w-5 h-5" />
                                </div>
                                <div className="text-left">
                                    <p className="text-[8px] font-black uppercase tracking-widest leading-none mb-1 opacity-70">Transaction Core</p>
                                    <p className="text-sm font-black capitalize leading-none">{data.ecommerceType}</p>
                                </div>
                                <CheckCircle2 className="w-4 h-4 ml-auto opacity-50" />
                            </div>
                        )}
                        {data.isBizOSaaSActive && (
                            <div className="flex items-center gap-3 p-4 rounded-2xl bg-slate-900 text-white shadow-lg shadow-slate-200 dark:shadow-none transition-transform hover:scale-[1.02] sm:col-span-2">
                                <div className="p-2 bg-blue-500 rounded-xl">
                                    <Zap className="w-5 h-5 fill-white" />
                                </div>
                                <div className="text-left">
                                    <p className="text-[8px] font-black uppercase tracking-widest leading-none mb-1 opacity-70">System Link</p>
                                    <p className="text-sm font-black capitalize leading-none">BizOSaaS Plugin Active</p>
                                </div>
                                <div className="ml-auto flex items-center gap-2">
                                    <Badge className="bg-blue-500 text-[8px] font-black uppercase tracking-widest px-2">Connected</Badge>
                                    <CheckCircle2 className="w-4 h-4 text-blue-500" />
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* 3. Platform Classifiers */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-3 text-left">
                        <Label className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-muted-foreground ml-1">
                            <Layout className="h-3 w-3" /> CMS Platform
                        </Label>
                        <Select
                            value={data.cmsType || 'none'}
                            onValueChange={(val: any) => onUpdate({ cmsType: val })}
                        >
                            <SelectTrigger className="h-12 rounded-xl border-gray-100 dark:border-slate-800 bg-white dark:bg-slate-950 shadow-sm focus:ring-2 focus:ring-blue-500">
                                <SelectValue placeholder="Select platform" />
                            </SelectTrigger>
                            <SelectContent className="rounded-2xl border-gray-100 dark:border-slate-800 shadow-2xl">
                                <SelectItem value="wordpress">WordPress</SelectItem>
                                <SelectItem value="shopify">Shopify</SelectItem>
                                <SelectItem value="wix">Wix</SelectItem>
                                <SelectItem value="webflow">Webflow</SelectItem>
                                <SelectItem value="ghost">Ghost CMS</SelectItem>
                                <SelectItem value="joomla">Joomla</SelectItem>
                                <SelectItem value="squarespace">Squarespace</SelectItem>
                                <SelectItem value="custom">Custom Code</SelectItem>
                                <SelectItem value="other">Other / None</SelectItem>
                            </SelectContent>
                        </Select>
                        <p className="text-[10px] text-muted-foreground/60 font-bold uppercase tracking-wider ml-1">
                            Integrations will adapt to your choice.
                        </p>
                    </div>

                    <div className="space-y-3 text-left">
                        <Label className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-muted-foreground ml-1">
                            <Database className="h-3 w-3" /> CRM System
                        </Label>
                        <Select
                            value={data.crmType || 'none'}
                            onValueChange={(val: any) => onUpdate({ crmType: val })}
                        >
                            <SelectTrigger className="h-12 rounded-xl border-gray-100 dark:border-slate-800 bg-white dark:bg-slate-950 shadow-sm focus:ring-2 focus:ring-blue-500">
                                <SelectValue placeholder="Select CRM" />
                            </SelectTrigger>
                            <SelectContent className="rounded-2xl border-gray-100 dark:border-slate-800 shadow-2xl">
                                <SelectItem value="none">No CRM used</SelectItem>
                                <SelectItem value="fluentcrm">FluentCRM</SelectItem>
                                <SelectItem value="hubspot">HubSpot</SelectItem>
                                <SelectItem value="salesforce">Salesforce</SelectItem>
                                <SelectItem value="zoho">Zoho CRM</SelectItem>
                                <SelectItem value="pipedrive">Pipedrive</SelectItem>
                                <SelectItem value="activecampaign">ActiveCampaign</SelectItem>
                                <SelectItem value="gohighlevel">GoHighLevel</SelectItem>
                            </SelectContent>
                        </Select>
                        <p className="text-[10px] text-muted-foreground/60 font-bold uppercase tracking-wider ml-1">
                            We'll configure syncing accordingly.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
