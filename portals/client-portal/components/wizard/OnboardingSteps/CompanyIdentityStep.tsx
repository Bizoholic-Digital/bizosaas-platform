import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { BusinessProfile } from '../types/onboarding';
import { Search, MapPin, Globe, Phone, Building2, CheckCircle2, Sparkles, Loader2, ExternalLink } from 'lucide-react';
import { generateDirectoryUrl } from '@/lib/business-slug';

interface Props {
    data: BusinessProfile;
    onUpdate: (data: Partial<BusinessProfile>) => void;
    onReset?: () => void;
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

export function CompanyIdentityStep({ data, onUpdate, onReset, discovery, isDiscovering }: Props) {
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

    const [searchError, setSearchError] = useState<string | null>(null);

    // Close predictions when clicking outside
    useEffect(() => {
        const handleClickOutside = () => {
            setShowPredictions(false);
            setShowAddressPredictions(false);
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const parsePhone = (phone: string) => {
        if (!phone) return { code: '+1', number: '', country: 'US' };
        const cleaned = phone.replace(/[^\d+]/g, '');
        const sortedCodes = [...COUNTRY_CODES].sort((a, b) => b.code.length - a.code.length);
        const match = sortedCodes.find(c => cleaned.startsWith(c.code));

        if (match) {
            return { code: match.code, number: cleaned.substring(match.code.length), country: match.country };
        }
        return { code: '+1', number: cleaned, country: 'US' };
    };

    // Initialize state from data (also handles resets)
    useEffect(() => {
        if (data.phone) {
            const parsed = parsePhone(data.phone);
            setCountryISO(parsed.country);
            setPhoneNumber(parsed.number);
        } else {
            setPhoneNumber('');
            setCountryISO('US');
        }
        setSearchQuery(data.companyName || '');
        setLocationQuery(data.location || '');
        setGmbConnected(!!data.gmbLink);
    }, [data.companyName, data.location, data.phone]);

    const syncPhone = (iso: string, num: string) => {
        const code = COUNTRY_CODES.find(c => c.country === iso)?.code || '+1';
        onUpdate({ phone: `${code} ${num.trim()}` });
    };

    const handlePhoneChange = (val: string) => {
        const num = val.replace(/[^\d]/g, '');
        setPhoneNumber(num);
        syncPhone(countryISO, num);
    };

    const handleCountryChange = (iso: string) => {
        setCountryISO(iso);
        syncPhone(iso, phoneNumber);
    };

    // Auto-update website and name as user types
    const handleNameChange = (val: string) => {
        setSearchQuery(val);
        setShowPredictions(true);

        const directoryUrl = generateDirectoryUrl(val, data.location || '');
        const updates: Partial<BusinessProfile> = {
            companyName: val,
            directoryUrl: directoryUrl
        };

        const isCurrentlyDirectory = data.website?.includes('directory.bizoholic.net') || !data.website;
        if (isCurrentlyDirectory) {
            updates.website = directoryUrl;
            updates.websiteType = 'directory';
        }

        onUpdate(updates);
    };

    const handleLocationInputChange = (val: string) => {
        setLocationQuery(val);
        setShowAddressPredictions(true);

        const directoryUrl = generateDirectoryUrl(data.companyName || '', val);
        const updates: Partial<BusinessProfile> = {
            location: val,
            directoryUrl: directoryUrl
        };

        const isCurrentlyDirectory = data.website?.includes('directory.bizoholic.net') || !data.website;
        if (isCurrentlyDirectory) {
            updates.website = directoryUrl;
            updates.websiteType = 'directory';
        }

        onUpdate(updates);
    };

    useEffect(() => {
        const timer = setTimeout(() => {
            if (searchQuery.length > 2 && !gmbConnected && showPredictions) {
                searchPlaces(searchQuery, 'establishment', setPredictions);
            }
        }, 300);
        return () => clearTimeout(timer);
    }, [searchQuery, gmbConnected, showPredictions]);

    useEffect(() => {
        const timer = setTimeout(() => {
            if (locationQuery.length > 2 && !gmbConnected && showAddressPredictions) {
                searchPlaces(locationQuery, 'geocode', setAddressPredictions);
            }
        }, 300);
        return () => clearTimeout(timer);
    }, [locationQuery, gmbConnected, showAddressPredictions]);

    const searchPlaces = async (query: string, type: string, setter: any) => {
        const isAddr = type === 'geocode';
        isAddr ? setIsSearchingAddress(true) : setIsSearching(true);
        try {
            const res = await fetch(`/api/brain/onboarding/places/autocomplete?input=${encodeURIComponent(query)}&types=${type}`);
            const results = await res.json();
            if (results.error) setter([]);
            else setter(results.predictions || []);
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

            const directoryUrl = generateDirectoryUrl(details.companyName || searchQuery, details.location);
            const finalWebsite = details.website || directoryUrl;

            onUpdate({
                companyName: details.companyName || searchQuery,
                location: details.location,
                website: finalWebsite,
                websiteType: details.website ? 'owned' : 'directory',
                directoryUrl: directoryUrl,
                phone: details.phone || '',
                gmbLink: details.gmbLink
            });

            setSearchQuery(details.companyName || searchQuery);
            setLocationQuery(details.location);
            setGmbConnected(true);

            if (details.country) {
                setCountryISO(details.country);
            }

            if (details.phone) {
                const parsed = parsePhone(details.phone);
                if (!details.country) setCountryISO(parsed.country);
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
            const directoryUrl = generateDirectoryUrl(data.companyName || '', details.location);

            const updates: Partial<BusinessProfile> = {
                location: details.location,
                directoryUrl: directoryUrl
            };

            const isCurrentlyDirectory = data.website?.includes('directory.bizoholic.net') || !data.website;
            if (isCurrentlyDirectory) {
                updates.website = directoryUrl;
                updates.websiteType = 'directory';
            }

            if (details.country) {
                setCountryISO(details.country);
                const code = COUNTRY_CODES.find(c => c.country === details.country)?.code || '+1';
                updates.phone = `${code} ${phoneNumber}`;
            }

            onUpdate(updates);
        } catch (error) {
            console.error("Location fetch failed", error);
        } finally {
            setIsSearchingAddress(false);
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="text-center mb-8 relative">
                <div className="inline-flex items-center justify-center p-2 bg-blue-50 dark:bg-blue-900/20 rounded-full mb-4">
                    <Building2 className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
                <h2 className="text-3xl font-black text-gray-900 dark:text-white uppercase tracking-tighter">Your Identity</h2>
                <p className="text-muted-foreground font-medium">Setup your business profile and digital presence.</p>

                {onReset && (
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={onReset}
                        className="absolute top-0 right-0 h-8 px-3 text-[10px] font-bold uppercase tracking-widest text-red-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 border border-transparent hover:border-red-100 dark:hover:border-red-900/30 transition-all rounded-full flex items-center gap-1.5 group"
                    >
                        <Sparkles size={10} className="group-hover:rotate-180 transition-transform duration-500" />
                        Reset Form
                    </Button>
                )}
            </div>

            <div className="space-y-4">
                <div className={`p-5 rounded-2xl border-2 transition-all duration-300 ${gmbConnected ? 'bg-green-50/50 border-green-200 dark:bg-green-900/10 dark:border-green-800/50 shadow-sm' : 'bg-white dark:bg-slate-900 border-gray-100 dark:border-slate-800 shadow-xl shadow-slate-200/50 dark:shadow-none'}`}>
                    {gmbConnected ? (
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <div className="bg-green-100 dark:bg-green-900/30 p-3 rounded-xl"><CheckCircle2 className="w-6 h-6 text-green-600 dark:text-green-400" /></div>
                                <div className="text-left">
                                    <h3 className="font-black text-green-900 dark:text-green-400 uppercase text-xs tracking-widest leading-none mb-1">Profile Verified</h3>
                                    <h4 className="font-bold text-gray-900 dark:text-white text-lg leading-tight">{data.companyName}</h4>
                                    <p className="text-sm text-gray-500 dark:text-gray-400 truncate max-w-[200px] sm:max-w-md">{data.location}</p>
                                </div>
                            </div>
                            <Button variant="outline" size="sm" onClick={() => setGmbConnected(false)} className="rounded-xl border-green-200 hover:bg-green-100 dark:border-green-800 hover:text-green-700 font-bold">Change</Button>
                        </div>
                    ) : (
                        <div className="relative text-left">
                            <Label className="text-[10px] font-black uppercase tracking-widest text-blue-600 mb-2 block flex items-center gap-2">
                                <Search size={12} /> Search Google Maps
                            </Label>
                            <div className="relative">
                                <Input
                                    placeholder="Enter business name (e.g. Bizoholic Digital)..."
                                    value={searchQuery}
                                    onChange={(e) => handleNameChange(e.target.value)}
                                    className="h-12 pl-4 pr-10 rounded-xl border-gray-200 dark:border-slate-800 bg-gray-50/50 dark:bg-slate-950 focus:ring-2 focus:ring-blue-500 transition-all text-lg font-medium"
                                />
                                {isSearching && <Loader2 className="absolute right-3 top-3.5 animate-spin w-5 h-5 text-blue-600" />}

                                {showPredictions && predictions.length > 0 && (
                                    <div className="absolute z-50 w-full mt-2 bg-white dark:bg-slate-900 border border-gray-100 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden max-h-72 overflow-y-auto backdrop-blur-xl bg-opacity-95">
                                        <div className="px-4 py-2 bg-gray-50 dark:bg-slate-800/50 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b dark:border-slate-800">Results from Google</div>
                                        {predictions.map((pred) => (
                                            <div
                                                key={pred.place_id}
                                                className="p-4 hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer border-b last:border-0 dark:border-slate-800 transition-colors group text-left"
                                                onMouseDown={(e) => {
                                                    e.preventDefault();
                                                    selectBusiness(pred.place_id);
                                                }}
                                            >
                                                <div className="font-bold text-gray-900 dark:text-white group-hover:text-blue-600 transition-colors">{pred.structured_formatting.main_text}</div>
                                                <div className="text-xs text-gray-500 dark:text-gray-400">{pred.structured_formatting.secondary_text}</div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2 text-left">
                        <Label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground ml-1">Company Name</Label>
                        <Input
                            value={data.companyName}
                            onChange={(e) => handleNameChange(e.target.value)}
                            disabled={gmbConnected}
                            className="rounded-xl h-11"
                        />
                    </div>
                    <div className="space-y-2 text-left">
                        <Label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground ml-1">Industry</Label>
                        <Input
                            value={data.industry}
                            onChange={(e) => onUpdate({ industry: e.target.value })}
                            placeholder="e.g. Agency, SaaS, Retail"
                            className="rounded-xl h-11"
                        />
                    </div>
                </div>

                <div className="space-y-2 text-left">
                    <Label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground ml-1">Location</Label>
                    <div className="relative">
                        <MapPin className="absolute left-3.5 top-3 h-4 w-4 text-muted-foreground/60 z-10" />
                        <Input
                            value={locationQuery}
                            onChange={(e) => handleLocationInputChange(e.target.value)}
                            className="pl-10 rounded-xl h-11"
                            disabled={gmbConnected}
                            placeholder="Enter city or address..."
                        />
                        {isSearchingAddress && <Loader2 className="absolute right-3 top-3 animate-spin w-5 h-5 text-gray-400" />}

                        {showAddressPredictions && addressPredictions.length > 0 && !gmbConnected && (
                            <div className="absolute z-50 w-full mt-2 bg-white dark:bg-slate-900 border border-gray-100 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden max-h-60 overflow-y-auto backdrop-blur-xl bg-opacity-95">
                                {addressPredictions.map((pred) => (
                                    <div
                                        key={pred.place_id}
                                        className="p-4 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer border-b last:border-0 dark:border-slate-700 transition-colors"
                                        onMouseDown={(e) => {
                                            e.preventDefault();
                                            selectLocation(pred.place_id);
                                        }}
                                    >
                                        <div className="font-bold text-gray-900 dark:text-white">{pred.structured_formatting.main_text}</div>
                                        <div className="text-xs text-gray-500 dark:text-gray-400">{pred.structured_formatting.secondary_text}</div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2 text-left">
                        <Label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground ml-1">Business Website</Label>
                        <div className="relative">
                            <Globe className="absolute left-3.5 top-3 h-4 w-4 text-muted-foreground/60" />
                            <Input
                                value={data.website}
                                onChange={(e) => onUpdate({ website: e.target.value, websiteType: 'owned' })}
                                className="pl-10 rounded-xl h-11"
                                placeholder="https://..."
                            />
                        </div>
                        {data.websiteType === 'directory' ? (
                            <div className="flex items-center gap-1.5 px-1 mt-1">
                                <Sparkles className="w-3 h-3 text-blue-500" />
                                <p className="text-[9px] text-blue-500 font-bold uppercase tracking-widest">Generating Business Directory Website Profile</p>
                            </div>
                        ) : (
                            <div className="flex items-center gap-1.5 px-1 mt-1 text-gray-400">
                                <CheckCircle2 className="w-3 h-3" />
                                <p className="text-[9px] font-bold uppercase tracking-widest">Directory Profile URL: <span className="lowercase font-medium">{data.directoryUrl}</span></p>
                            </div>
                        )}
                    </div>

                    <div className="space-y-2 text-left">
                        <Label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground ml-1">Phone Number</Label>
                        <div className="flex gap-2">
                            <Select value={countryISO} onValueChange={handleCountryChange}>
                                <SelectTrigger className="w-[120px] rounded-xl h-11"><SelectValue /></SelectTrigger>
                                <SelectContent className="max-h-[300px] rounded-xl border-gray-100 dark:border-slate-800 shadow-2xl">
                                    {COUNTRY_CODES.map(c => <SelectItem key={c.country} value={c.country}>{c.label}</SelectItem>)}
                                </SelectContent>
                            </Select>
                            <div className="relative flex-1">
                                <Phone className="absolute left-3.5 top-3 h-4 w-4 text-muted-foreground/60" />
                                <Input
                                    value={phoneNumber}
                                    onChange={(e) => handlePhoneChange(e.target.value)}
                                    className="pl-10 rounded-xl h-11"
                                    type="tel"
                                    placeholder="Enter phone..."
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
