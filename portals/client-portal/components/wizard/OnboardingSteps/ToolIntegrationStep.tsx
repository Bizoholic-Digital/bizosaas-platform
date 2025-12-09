import React from 'react';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ToolIntegration } from '../types/onboarding';
import { Mail, Megaphone } from 'lucide-react';

interface Props {
    data: ToolIntegration;
    onUpdate: (data: Partial<ToolIntegration>) => void;
}

export function ToolIntegrationStep({ data, onUpdate }: Props) {

    const toggleAdPlatform = (platform: string) => {
        const current = new Set(data.adPlatforms);
        if (current.has(platform)) {
            current.delete(platform);
        } else {
            current.add(platform);
        }
        onUpdate({ adPlatforms: Array.from(current) });
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Tools Integration</h2>
                <p className="text-gray-500">Connect your marketing stack.</p>
            </div>

            <div className="space-y-6">
                <div className="bg-white border rounded-xl p-5 space-y-4">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="bg-purple-100 p-2 rounded-lg text-purple-600">
                            <Mail size={20} />
                        </div>
                        <h3 className="font-semibold">Email Marketing</h3>
                    </div>

                    <Select
                        value={data.emailMarketing || 'none'}
                        onValueChange={(val: any) => onUpdate({ emailMarketing: val })}
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Select Provider" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="none">Not using yet</SelectItem>
                            <SelectItem value="mailchimp">Mailchimp</SelectItem>
                            <SelectItem value="klaviyo">Klaviyo</SelectItem>
                            <SelectItem value="activecampaign">ActiveCampaign</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div className="bg-white border rounded-xl p-5 space-y-4">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="bg-green-100 p-2 rounded-lg text-green-600">
                            <Megaphone size={20} />
                        </div>
                        <h3 className="font-semibold">Ad Platforms</h3>
                    </div>

                    <div className="space-y-3">
                        <div className="flex items-center justify-between">
                            <Label>Google Ads</Label>
                            <Switch
                                checked={data.adPlatforms.includes('google_ads')}
                                onCheckedChange={() => toggleAdPlatform('google_ads')}
                            />
                        </div>
                        <div className="flex items-center justify-between">
                            <Label>Facebook / Meta Ads</Label>
                            <Switch
                                checked={data.adPlatforms.includes('meta_ads')}
                                onCheckedChange={() => toggleAdPlatform('meta_ads')}
                            />
                        </div>
                        <div className="flex items-center justify-between">
                            <Label>LinkedIn Ads</Label>
                            <Switch
                                checked={data.adPlatforms.includes('linkedin_ads')}
                                onCheckedChange={() => toggleAdPlatform('linkedin_ads')}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
