import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { BusinessProfile } from '../types/onboarding';
import { Search, MapPin, Globe, Phone, Building2, CheckCircle2, Sparkles } from 'lucide-react';
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
    { code: '+1', country: 'US', label: '🇺🇸 US (+1)' },
    { code: '+44', country: 'GB', label: '🇬🇧 UK (+44)' },
    { code: '+91', country: 'IN', label: '🇮🇳 IN (+91)' },
    { code: '+61', country: 'AU', label: '🇦🇺 AU (+61)' },
    { code: '+971', country: 'AE', label: '🇦🇪 AE (+971)' },
    { code: '+65', country: 'SG', label: '🇸🇬 SG (+65)' },
    { code: '+1', country: 'CA', label: '🇨🇦 CA (+1)' },
    { code: '+49', country: 'DE', label: '🇩🇪 DE (+49)' },
    { code: '+33', country: 'FR', label: '🇫🇷 FR (+33)' },
    { code: '+39', country: 'IT', label: '🇮🇹 IT (+39)' },
    { code: '+34', country: 'ES', label: '🇪🇸 ES (+34)' },
    { code: '+81', country: 'JP', label: '🇯🇵 JP (+81)' },
    { code: '+86', country: 'CN', label: '🇨🇳 CN (+86)' },
    { code: '+82', country: 'KR', label: '🇰🇷 KR (+82)' },
    { code: '+64', country: 'NZ', label: '🇳🇿 NZ (+64)' },
    { code: '+27', country: 'ZA', label: '🇿🇦 ZA (+27)' },
    { code: '+55', country: 'BR', label: '🇧🇷 BR (+55)' },
    { code: '+52', country: 'MX', label: '🇲🇽 MX (+52)' },
];

export function CompanyIdentityStep({ data, onUpdate, discovery, isDiscovering }: Props) {
    const [searchQuery, setSearchQuery] = useState(data.companyName || '');
    const [predictions, setPredictions] = useState<Prediction[]>([]);
    const [isSearching, setIsSearching] = useState(false);
    const [showPredictions, setShowPredictions] = useState(false);

    const [locationQuery, setLocationQuery] = useState(data.location || '');
    const [addressPredictions, setAddressPredictions] = useState<Prediction[]>([]);
    const [showAddressPredictions, setShowAddressPredictions] = useState(false);
    const [isSearchingAddress, setIsSearchingAddress] = useState(false);

    const [gmbConnected, setGmbConnected] = useState(!!data.gmbLink);
    const [countryISO, setCountryISO] = useState('US');
    const [phoneNumber, setPhoneNumber] = useState('');

    const parsePhone = (phone: string) => {
        if (!phone) return { code: '+1', number: '', country: 'US' };
        const cleaned = phone.replace(/[^0-9+]/g, '');
        const match = COUNTRY_CODES.find(c => cleaned.startsWith(c.code));
        if (match) return { code: match.code, number: cleaned.substring(match.code.length), country: match.country };
        return { code: '+1', number: cleaned, country: 'US' };
    };

    // Initialize phone
    useEffect(() => {
        if (data.phone) {
            const parsed = parsePhone(data.phone);
            setCountryISO(parsed.country);
            setPhoneNumber(parsed.number);
        }
    }, []);

    // Push local changes to parent only on user interaction or mount
    const handlePhoneChange = (val: string) => {
        const num = val.replace(/[^0-9]/g, '');
        setPhoneNumber(num);
        const code = COUNTRY_CODES.find(c => c.country === countryISO)?.code || '+1';
        onUpdate({ phone: `${code} ${num}` });
    };

    const handleCountryChange = (iso: string) => {
        setCountryISO(iso);
        const code = COUNTRY_CODES.find(c => c.country === iso)?.code || '+1';
        onUpdate({ phone: `${code} ${phoneNumber}` });
    };

    // Business Search Logic
    useEffect(() => {
        const timer = setTimeout(() => {
            if (searchQuery.length > 2 && !gmbConnected && showPredictions) {
                searchPlaces(searchQuery, 'establishment', setPredictions);
            }
        }, 500);
        return () => clearTimeout(timer);
    }, [searchQuery, gmbConnected, showPredictions]);

    // Location Search Logic
    useEffect(() => {
        const timer = setTimeout(() => {
            if (locationQuery.length > 2 && showAddressPredictions && !gmbConnected) {
                searchPlaces(locationQuery, 'geocode', setAddressPredictions);
            }
        }, 500);
        return () => clearTimeout(timer);
    }, [locationQuery, showAddressPredictions, gmbConnected]);


    const [searchError, setSearchError] = useState<string | null>(null);

    const searchPlaces = async (query: string, type: string, setter: any) => {
        const isAddr = type === 'geocode';
        isAddr ? setIsSearchingAddress(true) : setIsSearching(true);
        setSearchError(null);
        try {
            const res = await fetch(`/api/brain/onboarding/places/autocomplete?input=${encodeURIComponent(query)}&types=${type}`);
            const data = await res.json();
            if (data.error) setter([]);
            else setter(data.predictions || []);
        } catch (error) {
            setter([]);
        } finally {
            isAddr ? setIsSearchingAddress(false) : setIsSearching(false);
        }
    };

    const selectBusiness = async (placeId: string) => {
        setIsSearching(true);
        setShowPredictions(false);
        try {
            const res = await fetch(`/api/brain/onboarding/places/details?place_id=${placeId}`);
            const details = await res.json();
            const directoryUrl = !details.website ? generateDirectoryUrl(details.companyName || searchQuery, details.location) : null;

            onUpdate({
                companyName: details.companyName || searchQuery,
                location: details.location,
                website: details.website || directoryUrl || '',
                phone: details.phone || '',
                gmbLink: details.gmbLink
            });

            setSearchQuery(details.companyName || searchQuery);
            setLocationQuery(details.location);
            setGmbConnected(true);

            if (details.country) {
                setCountryISO(details.country);
            } else if (details.phone) {
                const parsed = parsePhone(details.phone);
                setCountryISO(parsed.country);
            }

            if (details.phone) {
                const parsed = parsePhone(details.phone);
                setPhoneNumber(parsed.number);
            }
        } catch (error) {
            setSearchError("Failed to fetch details.");
        } finally {
            setIsSearching(false);
        }
    };

    const selectLocation = async (placeId: string) => {
        setIsSearchingAddress(true);
        setShowAddressPredictions(false);
        try {
            const res = await fetch(`/api/brain/onboarding/places/details?place_id=${placeId}`);
            const details = await res.json();

            setLocationQuery(details.location);
            onUpdate({ location: details.location });

            if (details.country) {
                setCountryISO(details.country);
                // Also update the phone code in the data if we have a number
                const code = COUNTRY_CODES.find(c => c.country === details.country)?.code || '+1';
                onUpdate({ phone: `${code} ${phoneNumber}` }); // Re-save with new code
            }
        } catch (error) {
            console.error("Location fetch failed", error);
        } finally {
            setIsSearchingAddress(false);
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-foreground">Company Identity</h2>
                <p className="text-muted-foreground">Start by finding your business profile.</p>
            </div>

            <div className="space-y-4">
                {/* Search / GMB Connection Card */}
                <div className={`p-4 rounded-lg border transition-all ${gmbConnected ? 'bg-green-50 border-green-200' : 'bg-blue-50 border-blue-200'}`}>
                    {gmbConnected ? (
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div className="bg-green-100 p-2 rounded-full"><CheckCircle2 className="w-5 h-5 text-green-600" /></div>
                                <div>
                                    <h3 className="font-semibold text-green-900">Profile Found</h3>
                                    <h4 className="font-bold text-green-800">{data.companyName}</h4>
                                    <p className="text-xs text-green-700">{data.location}</p>
                                </div>
                            </div>
                            <Button variant="ghost" size="sm" onClick={() => setGmbConnected(false)} className="text-green-700">Edit</Button>
                        </div>
                    ) : (
                        <div>
                            <Label className="text-blue-700 font-semibold mb-2 block flex items-center gap-2"><Search size={16} /> Search business</Label>
                            <div className="relative">
                                <Input
                                    placeholder="Business name..."
                                    value={searchQuery}
                                    onChange={(e) => { setSearchQuery(e.target.value); setShowPredictions(true); onUpdate({ companyName: e.target.value }); }}
                                />
                                {isSearching && <div className="absolute right-3 top-2.5 animate-spin w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full" />}
                                {showPredictions && predictions.length > 0 && (
                                    <div className="absolute z-10 w-full mt-1 bg-white border rounded-md shadow-lg max-h-60 overflow-y-auto">
                                        {predictions.map((pred) => (
                                            <div key={pred.place_id} className="p-3 hover:bg-gray-50 cursor-pointer border-b last:border-0" onClick={() => selectBusiness(pred.place_id)}>
                                                <div className="font-medium">{pred.structured_formatting.main_text}</div>
                                                <div className="text-xs text-muted-foreground">{pred.structured_formatting.secondary_text}</div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label>Company Name</Label>
                        <Input value={data.companyName} onChange={(e) => onUpdate({ companyName: e.target.value })} disabled={gmbConnected} />
                    </div>
                    <div className="space-y-2">
                        <Label>Industry</Label>
                        <Input value={data.industry} onChange={(e) => onUpdate({ industry: e.target.value })} placeholder="SaaS, Agency..." />
                    </div>
                </div>

                {/* Location Field with Autocomplete */}
                <div className="space-y-2">
                    <Label>Location</Label>
                    <div className="relative">
                        <MapPin className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/60 z-10" />
                        <Input
                            value={locationQuery}
                            onChange={(e) => {
                                setLocationQuery(e.target.value);
                                setShowAddressPredictions(true);
                                onUpdate({ location: e.target.value });
                            }}
                            className="pl-9"
                            disabled={gmbConnected}
                            placeholder="Enter city or address..."
                        />
                        {isSearchingAddress && <div className="absolute right-3 top-2.5 animate-spin w-4 h-4 border-2 border-slate-600 border-t-transparent rounded-full" />}

                        {/* Address Autocomplete Dropdown */}
                        {showAddressPredictions && addressPredictions.length > 0 && !gmbConnected && (
                            <div className="absolute z-20 w-full mt-1 bg-white dark:bg-slate-800 border rounded-md shadow-lg max-h-60 overflow-y-auto">
                                {addressPredictions.map((pred) => (
                                    <div key={pred.place_id} className="p-3 hover:bg-gray-50 dark:hover:bg-slate-700 cursor-pointer border-b last:border-0 dark:border-slate-700" onClick={() => selectLocation(pred.place_id)}>
                                        <div className="font-medium">{pred.structured_formatting.main_text}</div>
                                        <div className="text-xs text-muted-foreground">{pred.structured_formatting.secondary_text}</div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label>Website</Label>
                        <div className="relative">
                            <Globe className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/60" />
                            <Input value={data.website} onChange={(e) => onUpdate({ website: e.target.value })} className="pl-9" placeholder="https://..." />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label>Phone</Label>
                        <div className="flex gap-2">
                            <Select value={countryISO} onValueChange={handleCountryChange}>
                                <SelectTrigger className="w-[120px]"><SelectValue /></SelectTrigger>
                                <SelectContent className="max-h-[300px]">
                                    {COUNTRY_CODES.map(c => <SelectItem key={c.country} value={c.country}>{c.label}</SelectItem>)}
                                </SelectContent>
                            </Select>
                            <div className="relative flex-1">
                                <Phone className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/60" />
                                <Input value={phoneNumber} onChange={(e) => handlePhoneChange(e.target.value)} className="pl-9" type="tel" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
