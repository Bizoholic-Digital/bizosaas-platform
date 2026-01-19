import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { DigitalPresence } from '../types/onboarding';
import { Globe, Layout, Database, Search, CheckCircle2, Sparkles, Loader2, ShieldCheck, Zap } from 'lucide-react';
import { Switch } from '@/components/ui/switch';
import { Progress } from '@/components/ui/progress';

interface Props {
    data: DigitalPresence;
    websiteUrl?: string;
    onUpdate: (data: Partial<DigitalPresence>) => void;
    isAuditing?: boolean;
    auditedServices?: any;
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

export function DigitalPresenceStep({ data, websiteUrl, onUpdate, isAuditing, auditedServices }: Props) {
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

            <div className="space-y-6">
                <div className="space-y-3">
                    <Label className="flex items-center gap-2">
                        <Layout className="h-4 w-4" /> Content Management System (CMS)
                    </Label>
                    <Select
                        value={data.cmsType || 'none'}
                        onValueChange={(val: any) => onUpdate({ cmsType: val })}
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Select your website platform" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="wordpress">WordPress</SelectItem>
                            <SelectItem value="shopify">Shopify</SelectItem>
                            <SelectItem value="wix">Wix</SelectItem>
                            <SelectItem value="squarespace">Squarespace</SelectItem>
                            <SelectItem value="custom">Custom Code</SelectItem>
                            <SelectItem value="other">Other / None</SelectItem>
                        </SelectContent>
                    </Select>
                    <p className="text-xs text-muted-foreground">
                        We'll customize integration instructions based on your platform.
                    </p>
                </div>

                <div className="space-y-3">
                    <Label className="flex items-center gap-2">
                        <Database className="h-4 w-4" /> Customer Relationship Management (CRM)
                    </Label>
                    <Select
                        value={data.crmType || 'none'}
                        onValueChange={(val: any) => onUpdate({ crmType: val })}
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Select your CRM" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="none">No CRM used</SelectItem>
                            <SelectItem value="fluentcrm">FluentCRM</SelectItem>
                            <SelectItem value="hubspot">HubSpot</SelectItem>
                            <SelectItem value="salesforce">Salesforce</SelectItem>
                            <SelectItem value="zoho">Zoho CRM</SelectItem>
                            <SelectItem value="pipedrive">Pipedrive</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div className="border rounded-lg p-5 bg-card/50 space-y-4">
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <Label className="text-base flex items-center gap-2">
                                <Search className="h-4 w-4 text-blue-500" /> Tracking Scripts
                            </Label>
                            <p className="text-sm text-muted-foreground">Detect GA4, Pixel, or GTM automatically.</p>
                        </div>
                        <Switch
                            checked={data.hasTracking}
                            onCheckedChange={(checked) => onUpdate({ hasTracking: checked })}
                        />
                    </div>

                    {data.hasTracking && (
                        <div className="pt-4 border-t border-dashed">
                            {isAuditing ? (
                                <div className="space-y-4 bg-muted/30 p-4 rounded-xl border border-border">
                                    <div className="flex justify-between items-end mb-1">
                                        <div className="space-y-1">
                                            <div className="flex items-center gap-2 text-primary">
                                                <Zap className="h-4 w-4 animate-pulse fill-primary/20" />
                                                <span className="text-sm font-bold">Deep Scan in Progress</span>
                                            </div>
                                            <p className="text-xs text-muted-foreground animate-in fade-in slide-in-from-left-2 duration-300" key={statusIndex}>
                                                {SCAN_MESSAGES[statusIndex]}
                                            </p>
                                        </div>
                                        <span className="text-xs font-mono font-bold text-primary">{Math.round(scanProgress)}%</span>
                                    </div>
                                    <Progress value={scanProgress} className="h-2 bg-primary/10" />
                                    <p className="text-[10px] text-center text-muted-foreground/60">
                                        Checking {websiteUrl || 'your website'} security & tags
                                    </p>
                                </div>
                            ) : auditedServices ? (
                                <div className="space-y-3">
                                    <div className="flex items-center gap-2 text-green-600 dark:text-green-400 bg-green-500/10 p-3 rounded-lg border border-green-500/20 shadow-sm animate-in zoom-in-95 duration-500">
                                        <ShieldCheck className="h-5 w-5" />
                                        <span className="text-sm font-bold">Audit Complete: {auditedServices.essential.length + auditedServices.optional.length} services identified</span>
                                    </div>
                                    <div className="flex flex-wrap gap-2 px-1">
                                        {auditedServices.essential.map((s: any) => (
                                            <span key={s.id} className="text-[10px] bg-blue-500/10 text-blue-700 dark:text-blue-400 border border-blue-500/20 px-2.5 py-1 rounded-full font-bold flex items-center gap-1.5 shadow-sm">
                                                <Sparkles className="h-3 w-3" /> {s.service}
                                            </span>
                                        ))}
                                        {auditedServices.optional.map((s: any) => (
                                            <span key={s.id} className="text-[10px] bg-muted/50 text-muted-foreground border border-border px-2.5 py-1 rounded-full font-medium">
                                                {s.service}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            ) : (
                                <div className="flex flex-col items-center justify-center py-4 text-muted-foreground/40 space-y-2 italic">
                                    <Search className="h-8 w-8 opacity-20" />
                                    <p className="text-xs">Preparing digital asset audit for {websiteUrl || 'website'}...</p>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
