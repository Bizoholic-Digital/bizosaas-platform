import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { BusinessProfile } from '../types/onboarding';
import { Search, MapPin, Globe, Phone } from 'lucide-react';

interface Props {
    data: BusinessProfile;
    onUpdate: (data: Partial<BusinessProfile>) => void;
}

export function CompanyIdentityStep({ data, onUpdate }: Props) {
    const [loadingGmb, setLoadingGmb] = React.useState(false);

    const fetchGmbData = async () => {
        if (!data.gmbLink) return;
        setLoadingGmb(true);
        // Simulate API call to fetch data from GMB
        setTimeout(() => {
            onUpdate({
                companyName: "Acme Corp (Fetched)",
                location: "123 Business Rd, Tech City",
                website: "https://acme.example.com",
                phone: "+1 555 123 4567"
            });
            setLoadingGmb(false);
        }, 1500);
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900">Company Identity</h2>
                <p className="text-gray-500">Let's start with your business basics.</p>
            </div>

            <div className="space-y-4">
                <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                    <Label className="text-blue-900 font-semibold mb-2 block">
                        🚀 Quick Setup with Google Maps
                    </Label>
                    <div className="flex gap-2">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                            <Input
                                placeholder="Paste your Google Maps link to auto-fill"
                                className="pl-9 bg-white"
                                value={data.gmbLink || ''}
                                onChange={(e) => onUpdate({ gmbLink: e.target.value })}
                            />
                        </div>
                        <Button
                            onClick={fetchGmbData}
                            disabled={loadingGmb || !data.gmbLink}
                            className="bg-blue-600 hover:bg-blue-700 text-white"
                        >
                            {loadingGmb ? 'Fetching...' : 'Auto-Fill'}
                        </Button>
                    </div>
                    <p className="text-xs text-blue-600 mt-2">
                        We'll extract your website, address, and phone automatically.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label>Company Name</Label>
                        <Input
                            value={data.companyName}
                            onChange={(e) => onUpdate({ companyName: e.target.value })}
                            placeholder="e.g. Acme Corp"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Industry</Label>
                        <Input
                            value={data.industry}
                            onChange={(e) => onUpdate({ industry: e.target.value })}
                            placeholder="e.g. Retail, SaaS, Agency"
                        />
                    </div>
                </div>

                <div className="space-y-2">
                    <Label>Location</Label>
                    <div className="relative">
                        <MapPin className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                        <Input
                            value={data.location}
                            onChange={(e) => onUpdate({ location: e.target.value })}
                            className="pl-9"
                            placeholder="Full business address"
                        />
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label>Website (Optional)</Label>
                        <div className="relative">
                            <Globe className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                            <Input
                                value={data.website}
                                onChange={(e) => onUpdate({ website: e.target.value })}
                                className="pl-9"
                                placeholder="https://..."
                            />
                        </div>
                    </div>
                    <div className="space-y-2">
                        <Label>Phone (Optional)</Label>
                        <div className="relative">
                            <Phone className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                            <Input
                                value={data.phone}
                                onChange={(e) => onUpdate({ phone: e.target.value })}
                                className="pl-9"
                                placeholder="+1..."
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
