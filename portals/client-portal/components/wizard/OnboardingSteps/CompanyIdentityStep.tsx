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
    const [countryCode, setCountryCode] = useState('+1');
    const [phoneNumber, setPhoneNumber] = useState('');

    const parsePhone = (phone: string, location: string) => {
        if (!phone) {
            // Check location for default country
            if (location) {
                const l = location.toLowerCase();
                if (l.includes('india')) return { code: '+91', number: '' };
                if (l.includes('uk') || l.includes('united kingdom')) return { code: '+44', number: '' };
                if (l.includes('australia')) return { code: '+61', number: '' };
                if (l.includes('uae') || l.includes('emirates')) return { code: '+971', number: '' };
            }
            return { code: '+1', number: '' };
        }

        // Take the first number if multiple provided (Google sometimes returns "num1, num2" or "num1 num2")
        const firstPart = phone.split(/[\s,]+/)[0];

        // Remove formatting but keep leading +
        const cleaned = firstPart.startsWith('+')
            ? '+' + firstPart.replace(/[^0-9]/g, '')
            : firstPart.replace(/[^0-9]/g, '');

        const sortedCodes = COUNTRY_CODES.slice().sort((a, b) => b.code.length - a.code.length);
        const match = sortedCodes.find(c => cleaned.startsWith(c.code));

        if (match) {
            return {
                code: match.code,
                number: cleaned.substring(match.code.length).replace(/^0+/, '') // Remove leading zeros often found in local formats
            };
        }

        return { code: '+1', number: cleaned.replace('+', '') };
    };

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

            if (data.phone) {
                const phoneStr = data.phone.trim();
                // Find matching country code from the start
                const match = COUNTRY_CODES.slice().sort((a, b) => b.code.length - a.code.length)
                    .find(c => phoneStr.startsWith(c.code));

                if (match) {
                    setCountryCode(match.code);
                    setPhoneNumber(phoneStr.substring(match.code.length).trim());
                } else {
                    setPhoneNumber(phoneStr);
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

            // Create directory listing in backend if it doesn't have a website
            if (!details.website && directoryUrl) {
                try {
                    const slug = directoryUrl.split('//')[1].split('.')[0];
                    await fetch('/api/brain/business-directory/businesses', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            name: details.companyName || searchQuery,
                            slug: slug,
                            google_place_id: placeId,
                            location: details.location,
                            phone: details.phone,
                            website: directoryUrl,
                            category: details.category || 'Local Business',
                            google_data: details,
                            google_rating: details.rating,
                            google_reviews_count: details.user_ratings_total
                        })
                    });
                } catch (err) {
                    console.error("Failed to create directory listing:", err);
                }
            }

            setSearchQuery(details.companyName);
            setLocationQuery(details.location);
            setGmbConnected(true);

            // Try parsing phone
            if (details.phone) {
                const { code, number } = parsePhone(details.phone, details.location);
                setCountryCode(code);
                setPhoneNumber(number);
                onUpdate({ phone: `${code} ${number}`.trim() });
            } else if (details.location) {
                const { code } = parsePhone('', details.location);
                setCountryCode(code);
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
                                    <SelectTrigger className="bg-white dark:bg-black/20 border-blue-200">
                                        <SelectValue placeholder="Code" />
                                    </SelectTrigger>
                                    <SelectContent className="max-h-[300px]">
                                        {COUNTRY_CODES.map((c, i) => (
                                            <SelectItem key={`${c.code}-${c.country}-${i}`} value={c.code}>
                                                <span className="flex items-center gap-2">
                                                    <span className="text-base">{c.label.split(' ')[0]}</span>
                                                    <span className="font-medium">{c.label.split(' ').slice(1).join(' ')}</span>
                                                </span>
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
                                    className="pl-9 bg-white dark:bg-black/20 border-blue-200"
                                    placeholder="Number without code"
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
