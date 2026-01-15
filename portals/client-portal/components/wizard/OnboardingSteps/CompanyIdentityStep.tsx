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

export function CompanyIdentityStep({ data, onUpdate, discovery, isDiscovering }: Props & { discovery?: any, isDiscovering?: boolean }) {
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
                <h2 className="text-2xl font-bold text-foreground">Company Identity</h2>
                <p className="text-muted-foreground">Let's start with your business basics.</p>
            </div>

            <div className="space-y-4">
                {isDiscovering ? (
                    <div className="bg-blue-500/10 p-6 rounded-lg border border-blue-500/20 flex flex-col items-center justify-center text-center">
                        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4" />
                        <h3 className="text-lg font-semibold text-foreground">Discovering your digital footprint...</h3>
                        <p className="text-sm text-blue-600 dark:text-blue-400">We're checking Google and Microsoft services for your email.</p>
                    </div>
                ) : discovery && (discovery.google?.length > 0 || discovery.microsoft?.length > 0) ? (
                    <div className="bg-green-500/10 p-4 rounded-lg border border-green-500/20">
                        <Label className="text-green-700 dark:text-green-400 font-semibold mb-3 block flex items-center gap-2">
                            ✨ Services Detected Automatically
                        </Label>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {[...(discovery.google || []), ...(discovery.microsoft || [])].map((svc: any) => (
                                <div key={svc.id} className="bg-card p-2.5 rounded border border-green-500/20 flex justify-between items-center text-sm shadow-sm">
                                    <div className="flex flex-col">
                                        <span className="font-medium text-foreground">{svc.name}</span>
                                        {svc.cost && <span className="text-[10px] text-orange-600 font-bold uppercase">{svc.cost} May Apply</span>}
                                    </div>
                                    <div className="flex items-center gap-2">
                                        {svc.requiresEnablement && (
                                            <span className="text-[10px] bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300 px-1.5 py-0.5 rounded font-bold">Needs Enablement</span>
                                        )}
                                        <div className="w-2 h-2 rounded-full bg-green-500" />
                                    </div>
                                </div>
                            ))}
                        </div>
                        <p className="text-xs text-green-600 dark:text-green-400/80 mt-3 font-medium">
                            We've pre-filled your business details based on these profiles.
                        </p>
                    </div>
                ) : (
                    <div className="bg-blue-500/10 p-4 rounded-lg border border-blue-500/20">
                        <Label className="text-blue-700 dark:text-blue-400 font-semibold mb-2 block">
                            🚀 Quick Setup with Google Maps
                        </Label>
                        <div className="flex flex-col sm:flex-row gap-2">
                            <div className="relative flex-1">
                                <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/60" />
                                <Input
                                    placeholder="Paste Google Maps link"
                                    className="pl-9 bg-card"
                                    value={data.gmbLink || ''}
                                    onChange={(e) => onUpdate({ gmbLink: e.target.value })}
                                />
                            </div>
                            <Button
                                onClick={fetchGmbData}
                                disabled={loadingGmb || !data.gmbLink}
                                className="bg-blue-600 hover:bg-blue-700 text-white w-full sm:w-auto"
                            >
                                {loadingGmb ? 'Fetching...' : 'Auto-Fill'}
                            </Button>
                        </div>
                    </div>
                )}

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
                        <MapPin className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/60" />
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
                            <Globe className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/60" />
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
                            <Phone className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/60" />
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
