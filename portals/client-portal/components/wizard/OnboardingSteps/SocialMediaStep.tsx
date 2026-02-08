import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { SocialMediaConfig } from '../types/onboarding';
import { Facebook, Instagram, Linkedin, Twitter } from 'lucide-react';

interface Props {
    data: SocialMediaConfig;
    onUpdate: (data: Partial<SocialMediaConfig>) => void;
}

const PLATFORMS = [
    { id: 'facebook', name: 'Facebook', icon: Facebook, color: 'text-blue-600', bg: 'bg-blue-50' },
    { id: 'instagram', name: 'Instagram', icon: Instagram, color: 'text-pink-600', bg: 'bg-pink-50' },
    { id: 'linkedin', name: 'LinkedIn', icon: Linkedin, color: 'text-blue-700', bg: 'bg-blue-50' },
    { id: 'twitter', name: 'Twitter / X', icon: Twitter, color: 'text-sky-500', bg: 'bg-sky-50' },
];

export function SocialMediaStep({ data, onUpdate }: Props) {

    const togglePlatform = (platformId: string) => {
        const current = new Set(data.platforms);
        if (current.has(platformId)) {
            current.delete(platformId);
        } else {
            current.add(platformId);
        }
        onUpdate({ platforms: Array.from(current) });
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-foreground">Social Channels</h2>
                <p className="text-muted-foreground">Where does your audience hang out?</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
                {PLATFORMS.map((platform) => {
                    const isSelected = data.platforms.includes(platform.id);
                    return (
                        <div
                            key={platform.id}
                            onClick={() => togglePlatform(platform.id)}
                            className={`
                cursor-pointer border rounded-xl p-4 transition-all duration-200
                ${isSelected
                                    ? 'border-blue-500 bg-blue-50 ring-1 ring-blue-500'
                                    : 'border-gray-200 hover:border-gray-300 hover:bg-muted'
                                }
              `}
                        >
                            <div className="flex items-center gap-3">
                                <div className={`p-2 rounded-lg ${isSelected ? 'bg-card' : platform.bg}`}>
                                    <platform.icon className={`h-6 w-6 ${platform.color}`} />
                                </div>
                                <span className={`font-medium ${isSelected ? 'text-blue-700' : 'text-foreground'}`}>
                                    {platform.name}
                                </span>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Adaptive Inputs: Show fields only for compliance/connection if platform selected */}
            {data.platforms.length > 0 && (
                <div className="pt-4 border-t space-y-4">
                    <Label>Account Details</Label>

                    {data.platforms.includes('facebook') && (
                        <div className="space-y-2 animate-in fade-in slide-in-from-top-2">
                            <Label className="text-xs text-muted-foreground">Facebook Page URL</Label>
                            <Input
                                placeholder="https://facebook.com/..."
                                value={data.facebookPageId}
                                onChange={(e) => onUpdate({ facebookPageId: e.target.value })}
                            />
                        </div>
                    )}

                    {data.platforms.includes('instagram') && (
                        <div className="space-y-2 animate-in fade-in slide-in-from-top-2">
                            <Label className="text-xs text-muted-foreground">Instagram Handle</Label>
                            <Input
                                placeholder="@username"
                                value={data.instagramHandle}
                                onChange={(e) => onUpdate({ instagramHandle: e.target.value })}
                            />
                        </div>
                    )}

                    {data.platforms.includes('linkedin') && (
                        <div className="space-y-2 animate-in fade-in slide-in-from-top-2">
                            <Label className="text-xs text-muted-foreground">LinkedIn Company URL</Label>
                            <Input
                                placeholder="https://linkedin.com/company/..."
                                value={data.linkedinCompanyId}
                                onChange={(e) => onUpdate({ linkedinCompanyId: e.target.value })}
                            />
                        </div>
                    )}

                    {data.platforms.includes('twitter') && (
                        <div className="space-y-2 animate-in fade-in slide-in-from-top-2">
                            <Label className="text-xs text-muted-foreground">Twitter Handle</Label>
                            <Input
                                placeholder="@username"
                                value={data.twitterHandle}
                                onChange={(e) => onUpdate({ twitterHandle: e.target.value })}
                            />
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
