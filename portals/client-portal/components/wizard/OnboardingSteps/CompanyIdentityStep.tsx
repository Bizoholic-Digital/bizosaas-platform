import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { BusinessProfile } from '../types/onboarding';
import { Search, MapPin, Globe, Phone, Building2, CheckCircle2 } from 'lucide-react';
import { generateDirectoryUrl } from '@/lib/business-slug';

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

const COUNTRY_CODES = [
    { code: '+1', country: 'US', label: '🇺🇸 United States (+1)' },
    { code: '+44', country: 'GB', label: '🇬🇧 United Kingdom (+44)' },
    { code: '+91', country: 'IN', label: '🇮🇳 India (+91)' },
    { code: '+61', country: 'AU', label: '🇦🇺 Australia (+61)' },
    { code: '+86', country: 'CN', label: '🇨🇳 China (+86)' },
    { code: '+49', country: 'DE', label: '🇩🇪 Germany (+49)' },
    { code: '+33', country: 'FR', label: '🇫🇷 France (+33)' },
    { code: '+81', country: 'JP', label: '🇯🇵 Japan (+81)' },
    { code: '+971', country: 'AE', label: '🇦🇪 UAE (+971)' },
    // Add more as needed
];

export function CompanyIdentityStep({ data, onUpdate, discovery, isDiscovering }: Props) {
    // Main Business Search State
    const [searchQuery, setSearchQuery] = useState(data.companyName || '');
    const [predictions, setPredictions] = useState<Prediction[]>([]);
    const [isSearching, setIsSearching] = useState(false);
    const [showPredictions, setShowPredictions] = useState(false);

    // Address Search State
    const [locationQuery, setLocationQuery] = useState(data.location || '');
    const [addressPredictions, setAddressPredictions] = useState<Prediction[]>([]);
    const [showAddressPredictions, setShowAddressPredictions] = useState(false);
    const [isSearchingAddress, setIsSearchingAddress] = useState(false);

    // Connection State
    const [gmbConnected, setGmbConnected] = useState(!!data.gmbLink);

    // Phone State
    const [countryCode, setCountryCode] = useState(data.phone?.split(' ')[0] || '+1');
    const [phoneNumber, setPhoneNumber] = useState(data.phone?.split(' ').slice(1).join(' ') || '');

    // Initialize/Fix Data
    useEffect(() => {
        const defaults = ['My Company', 'My Business', 'Acme Corp'];
        if (defaults.includes(data.companyName) || data.location?.includes('BK Enclave')) {
            onUpdate({ companyName: '', location: '', phone: '', website: '', gmbLink: '' });
            setSearchQuery('');
            setLocationQuery('');
            setGmbConnected(false);
        } else {
            // Ensure local state syncs with props if coming back to step
            setSearchQuery(data.companyName || '');
            setLocationQuery(data.location || '');
            if (data.phone && data.phone.includes(' ')) {
                const parts = data.phone.split(' ');
                if (COUNTRY_CODES.some(c => c.code === parts[0])) {
                    setCountryCode(parts[0]);
                    setPhoneNumber(parts.slice(1).join(' '));
                } else {
                    setPhoneNumber(data.phone);
                }
            }
        }
    }, []);

    // Effect to update parent phone state when parts change
    useEffect(() => {
        if (phoneNumber) {
            onUpdate({ phone: `${countryCode} ${phoneNumber}` });
        }
    }, [countryCode, phoneNumber]);

    // --- BUSINESS SEARCH LOGIC ---
    useEffect(() => {
        const timer = setTimeout(() => {
            if (searchQuery.length > 2 && !gmbConnected && showPredictions) {
                searchPlaces(searchQuery, 'establishment', setPredictions);
            }
        }, 500);
        return () => clearTimeout(timer);
    }, [searchQuery, gmbConnected, showPredictions]);

    // --- ADDRESS SEARCH LOGIC ---
    useEffect(() => {
        const timer = setTimeout(() => {
            if (locationQuery.length > 2 && !gmbConnected && showAddressPredictions) {
                searchPlaces(locationQuery, 'geocode', setAddressPredictions);
            }
        }, 500);
        return () => clearTimeout(timer);
    }, [locationQuery, gmbConnected, showAddressPredictions]);

    const searchPlaces = async (query: string, type: string, setter: any) => {
        const isAddr = type === 'geocode';
        isAddr ? setIsSearchingAddress(true) : setIsSearching(true);
        try {
            const res = await fetch(`/api/brain/onboarding/places/autocomplete?input=${encodeURIComponent(query)}&types=${type}`);
            const data = await res.json();
            setter(data.predictions || []);
        } catch (error) {
            console.error(`Failed to search ${type}:`, error);
        } finally {
            isAddr ? setIsSearchingAddress(false) : setIsSearching(false);
        }
    };

    const selectBusiness = async (placeId: string) => {
        setIsSearching(true);
        setShowPredictions(false);
        try {
            const res = await fetch(`/api/brain/onboarding/places/details?place_id=${placeId}`);
            if (!res.ok) throw new Error('Failed to fetch details');

            const details = await res.json();

            // IMPORTANT: Clear all fields first to avoid stale data
            onUpdate({
                companyName: '',
                location: '',
                website: '',
                phone: '',
                gmbLink: ''
            });

            // Generate directory URL if business doesn't have a website
            const directoryUrl = !details.website
                ? generateDirectoryUrl(details.companyName || searchQuery, details.location)
                : null;

            // Then populate with new data
            onUpdate({
                companyName: details.companyName || searchQuery,
                location: details.location,
                website: details.website || directoryUrl || '', // Use directory URL as fallback
                websiteType: details.website ? 'owned' : 'directory', // Flag for backend
                phone: details.phone, // Use GMB phone directly if available
                gmbLink: details.gmbLink
            });

            setSearchQuery(details.companyName);
            setLocationQuery(details.location);
            setGmbConnected(true);

            // Try parsing phone
            if (details.phone) {
                // Simple heurestic or just set it
                setPhoneNumber(details.phone); // Might need manual cleanup if GMB format is weird
            }

        } catch (error) {
            console.error("Failed to fetch business details:", error);
        } finally {
            setIsSearching(false);
        }
    };

    const selectAddress = (description: string) => {
        setLocationQuery(description);
        onUpdate({ location: description });
        setShowAddressPredictions(false);
    };

    const handleManualMode = () => {
        setShowPredictions(false);
        setGmbConnected(false);
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-foreground">Company Identity</h2>
                <p className="text-muted-foreground">Start by finding your business profile.</p>
            </div>

            <div className="space-y-4">
                {/* --- MAIN BUSINESS SEARCH --- */}
                <div className={`p-4 rounded-lg border transition-all ${gmbConnected ? 'bg-green-50 border-green-200' : 'bg-blue-50 border-blue-200'}`}>
                    {gmbConnected ? (
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div className="bg-green-100 p-2 rounded-full">
                                    <CheckCircle2 className="w-5 h-5 text-green-600" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-green-900">Business Profile Found</h3>
                                    <h4 className="font-bold text-green-800">{data.companyName}</h4>
                                    <p className="text-xs text-green-700">{data.location}</p>
                                </div>
                            </div>
                            <Button variant="ghost" size="sm" onClick={handleManualMode} className="text-green-700 hover:text-green-800 hover:bg-green-100">
                                Edit details
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

                                {/* Business Predictions Dropdown */}
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
                                    </div>
                                )}
                            </div>
                            <p className="text-xs text-blue-600/70 mt-2">
                                Finding your profile helps us auto-fill your details. Use manual entry below if needed.
                            </p>
                        </div>
                    )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label>Company Name</Label>
                        <Input
                            value={data.companyName}
                            onChange={(e) => {
                                onUpdate({ companyName: e.target.value });
                                setSearchQuery(e.target.value); // Sync back
                            }}
                            placeholder="e.g. Acme Corp"
                            disabled={gmbConnected}
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

                {/* --- ADDRESS AUTOCOMPLETE --- */}
                <div className="space-y-2">
                    <Label>Location</Label>
                    <div className="relative">
                        <MapPin className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/60" />
                        <Input
                            value={locationQuery}
                            onChange={(e) => {
                                setLocationQuery(e.target.value);
                                setShowAddressPredictions(true);
                                onUpdate({ location: e.target.value });
                            }}
                            onFocus={() => setShowAddressPredictions(true)}
                            className="pl-9"
                            placeholder="Search your street address..."
                            disabled={gmbConnected} // Can enable if they click "Edit Details"
                        />
                        {isSearchingAddress && (
                            <div className="absolute right-3 top-2.5">
                                <div className="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
                            </div>
                        )}

                        {/* Address Predictions Dropdown */}
                        {showAddressPredictions && addressPredictions.length > 0 && !gmbConnected && (
                            <div className="absolute z-10 w-full mt-1 bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-md shadow-lg max-h-60 overflow-y-auto">
                                {addressPredictions.map((pred) => (
                                    <div
                                        key={pred.place_id}
                                        className="p-3 hover:bg-gray-50 dark:hover:bg-zinc-800 cursor-pointer text-sm border-b last:border-0 border-gray-100 dark:border-zinc-800"
                                        onClick={() => selectAddress(pred.description)}
                                    >
                                        <div className="font-medium text-foreground">{pred.description}</div>
                                    </div>
                                ))}
                            </div>
                        )}
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

                    {/* --- ENHANCED PHONE INPUT --- */}
                    <div className="space-y-2">
                        <Label>Phone (Optional)</Label>
                        <div className="flex gap-2">
                            <div className="w-[140px]">
                                <Select value={countryCode} onValueChange={setCountryCode} disabled={gmbConnected && !!data.phone}>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Code" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {COUNTRY_CODES.map((c) => (
                                            <SelectItem key={c.code} value={c.code}>
                                                {c.label}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="relative flex-1">
                                <Phone className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/60" />
                                <Input
                                    value={phoneNumber}
                                    onChange={(e) => {
                                        const val = e.target.value.replace(/[^0-9]/g, ''); // Validate number only
                                        setPhoneNumber(val);
                                    }}
                                    className="pl-9"
                                    placeholder="Mobile number..."
                                    disabled={gmbConnected && !!data.phone}
                                    type="tel"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
