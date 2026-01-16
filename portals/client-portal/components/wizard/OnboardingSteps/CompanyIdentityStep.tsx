import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { BusinessProfile } from '../types/onboarding';
import { Search, MapPin, Globe, Phone, Building2, CheckCircle2 } from 'lucide-react';

interface Props {
    data: BusinessProfile;
    onUpdate: (data: Partial<BusinessProfile>) => void;
    discovery?: any;
    isDiscovering?: boolean;
}

interface Prediction {
    description: string;
    place_id: string;
    structured_formatting: {
        main_text: string;
        secondary_text: string;
    };
}

export function CompanyIdentityStep({ data, onUpdate, discovery, isDiscovering }: Props) {
    const [searchQuery, setSearchQuery] = useState('');
    const [predictions, setPredictions] = useState<Prediction[]>([]);
    const [isSearching, setIsSearching] = useState(false);
    const [showPredictions, setShowPredictions] = useState(false);
    const [gmbConnected, setGmbConnected] = useState(!!data.gmbLink);

    // Debounce search input
    useEffect(() => {
        const timer = setTimeout(() => {
            if (searchQuery.length > 2 && !gmbConnected) {
                searchBusiness(searchQuery);
            }
        }, 500);
        return () => clearTimeout(timer);
    }, [searchQuery]);

    // Clear generic defaults if present (fix for legacy data)
    useEffect(() => {
        const defaults = ['My Company', 'My Business', 'Acme Corp'];
        if (defaults.includes(data.companyName) || data.location?.includes('BK Enclave')) {
            onUpdate({ companyName: '', location: '', phone: '', website: '', gmbLink: '' });
            setSearchQuery('');
            setGmbConnected(false);
        }
    }, []);

    const searchBusiness = async (query: string) => {
        setIsSearching(true);
        try {
            const res = await fetch(`/api/brain/onboarding/places/autocomplete?input=${encodeURIComponent(query)}`);
            const data = await res.json();
            setPredictions(data.predictions || []);
            setShowPredictions(true);
        } catch (error) {
            console.error("Failed to search business:", error);
        } finally {
            setIsSearching(false);
        }
    };

    const selectBusiness = async (placeId: string) => {
        setIsSearching(true);
        setShowPredictions(false);
        try {
            const res = await fetch(`/api/brain/onboarding/places/details?place_id=${placeId}`);
            if (!res.ok) throw new Error('Failed to fetch details');

            const details = await res.json();

            onUpdate({
                companyName: details.companyName || searchQuery,
                location: details.location,
                website: details.website,
                phone: details.phone,
                gmbLink: details.gmbLink
            });
            setGmbConnected(true);
            setSearchQuery(details.companyName);
        } catch (error) {
            console.error("Failed to fetch business details:", error);
            // Fallback: just use what we have from prediction if partial
        } finally {
            setIsSearching(false);
        }
    };

    const handleManualMode = () => {
        setShowPredictions(false);
        setGmbConnected(false);
        // Don't clear fields, just allow editing
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-foreground">Company Identity</h2>
                <p className="text-muted-foreground">Start by finding your business on Google.</p>
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
                        <p className="text-xs text-green-600 dark:text-green-400/80 font-medium">
                            We've pre-filled your business details based on detected profiles.
                        </p>
                    </div>
                ) : (
                    // --- NEW GOOGLE PLACES SEARCH UI ---
                    <div className={`p-4 rounded-lg border transition-all ${gmbConnected ? 'bg-green-50 border-green-200' : 'bg-blue-50 border-blue-200'}`}>
                        {gmbConnected ? (
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className="bg-green-100 p-2 rounded-full">
                                        <CheckCircle2 className="w-5 h-5 text-green-600" />
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-green-900">Business Found</h3>
                                        <p className="text-xs text-green-700">We've auto-filled your details from Google.</p>
                                    </div>
                                </div>
                                <Button variant="ghost" size="sm" onClick={handleManualMode} className="text-green-700 hover:text-green-800 hover:bg-green-100">
                                    Edit manually
                                </Button>
                            </div>
                        ) : (
                            <div>
                                <Label className="text-blue-700 dark:text-blue-400 font-semibold mb-2 block flex items-center gap-2">
                                    <Search size={16} /> Search your business
                                </Label>
                                <div className="relative">
                                    <Input
                                        placeholder="Type your business name... (e.g. Acme Corp)"
                                        className="pl-4 bg-white dark:bg-black/20 border-blue-200 focus-visible:ring-blue-500"
                                        value={searchQuery}
                                        onChange={(e) => {
                                            setSearchQuery(e.target.value);
                                            setShowPredictions(true);
                                            if (e.target.value === '') {
                                                setPredictions([]);
                                                onUpdate({ companyName: '' });
                                            } else {
                                                onUpdate({ companyName: e.target.value });
                                            }
                                        }}
                                    />
                                    {isSearching && (
                                        <div className="absolute right-3 top-2.5">
                                            <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                                        </div>
                                    )}

                                    {/* Predictions Dropdown */}
                                    {showPredictions && predictions.length > 0 && (
                                        <div className="absolute z-10 w-full mt-1 bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-md shadow-lg max-h-60 overflow-y-auto">
                                            {predictions.map((pred) => (
                                                <div
                                                    key={pred.place_id}
                                                    className="p-3 hover:bg-gray-50 dark:hover:bg-zinc-800 cursor-pointer text-sm border-b last:border-0 border-gray-100 dark:border-zinc-800"
                                                    onClick={() => selectBusiness(pred.place_id)}
                                                >
                                                    <div className="font-medium text-foreground">{pred.structured_formatting.main_text}</div>
                                                    <div className="text-xs text-muted-foreground">{pred.structured_formatting.secondary_text}</div>
                                                </div>
                                            ))}
                                            <div
                                                className="p-2 text-xs text-center text-blue-600 cursor-pointer hover:underline bg-gray-50 dark:bg-zinc-900/50"
                                                onClick={handleManualMode}
                                            >
                                                Can't find it? Enter details manually
                                            </div>
                                        </div>
                                    )}
                                </div>
                                <p className="text-xs text-blue-600/70 mt-2">
                                    Start typing to find your business on Google Maps.
                                </p>
                            </div>
                        )}
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label>Company Name</Label>
                        <Input
                            value={data.companyName}
                            onChange={(e) => onUpdate({ companyName: e.target.value })}
                            placeholder="e.g. Acme Corp"
                            disabled={gmbConnected} // Disable if auto-filled to encourage correct selection
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
                            disabled={gmbConnected}
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
                            // Website is often wrong/missing in Maps, keep editable
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
                                disabled={gmbConnected}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
