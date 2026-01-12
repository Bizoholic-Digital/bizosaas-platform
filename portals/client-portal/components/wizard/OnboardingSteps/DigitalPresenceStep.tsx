import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { DigitalPresence } from '../types/onboarding';
import { Globe, Layout, Database } from 'lucide-react';
import { Switch } from '@/components/ui/switch';

interface Props {
    data: DigitalPresence;
    websiteUrl?: string;
    onUpdate: (data: Partial<DigitalPresence>) => void;
}

export function DigitalPresenceStep({ data, websiteUrl, onUpdate }: Props) {

    // Adaptive logic: If website was detected/provided in step 1, we show that
    const renderWebsiteStatus = () => {
        if (websiteUrl) {
            return (
                <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4 flex items-center gap-3 mb-6">
                    <div className="bg-green-500/20 p-2 rounded-full">
                        <Globe className="text-green-600 dark:text-green-400 h-5 w-5" />
                    </div>
                    <div>
                        <p className="font-semibold text-green-700 dark:text-green-400">Website Detected</p>
                        <p className="text-sm text-green-600/80 dark:text-green-400/80">{websiteUrl}</p>
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
                    <p className="font-semibold text-yellow-700 dark:text-yellow-400">No Website Detected</p>
                    <p className="text-sm text-yellow-600/80 dark:text-yellow-400/80">We'll help you set up tracking manually later.</p>
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

                <div className="flex items-center justify-between border rounded-lg p-4">
                    <div className="space-y-0.5">
                        <Label className="text-base">Tracking Scripts</Label>
                        <p className="text-sm text-muted-foreground">Do you already have GA4 or Pixel installed?</p>
                    </div>
                    <Switch
                        checked={data.hasTracking}
                        onCheckedChange={(checked) => onUpdate({ hasTracking: checked })}
                    />
                </div>
            </div>
        </div>
    );
}
