import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { AnalyticsConfig } from '../types/onboarding';
import { BarChart3, Search, Sparkles, RefreshCw, CheckCircle2 } from 'lucide-react';
import { useUser } from '@clerk/nextjs';
import { toast } from 'sonner';

interface Props {
    data: AnalyticsConfig;
    onUpdate: (data: Partial<AnalyticsConfig>) => void;
}

export function AnalyticsTrackingStep({ data, onUpdate }: Props) {
    const { user } = useUser();
    const [isDiscovering, setIsDiscovering] = React.useState(false);
    const [discovered, setDiscovered] = React.useState(false);

    const isGmailUser = user?.primaryEmailAddress?.emailAddress.endsWith('@gmail.com');

    const handleMagicConnect = async () => {
        setIsDiscovering(true);
        try {
            // 1. In a real app, this would trigger OAuth with all scopes
            // For now, we simulate the discovery process
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Mock discovery result
            onUpdate({
                gaId: 'G-7Y2B8C9E1A',
                gscId: 'https://' + (user?.primaryEmailAddress?.emailAddress.split('@')[0] || 'example') + '.com'
            });

            setDiscovered(true);
            toast.success("Accounts discovered and connected automatically!");
        } catch (error) {
            toast.error("Discovery failed. Please connect manually.");
        } finally {
            setIsDiscovering(false);
        }
    };
    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Tracking & Analytics</h2>
                <p className="text-gray-500">Data fuels our AI agents. Let's connect your sources.</p>
            </div>

            {isGmailUser && !discovered && (
                <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-xl p-6 text-white mb-8 shadow-lg animate-in zoom-in duration-500">
                    <div className="flex items-center gap-4 mb-4">
                        <div className="bg-white/20 p-2 rounded-lg">
                            <Sparkles className="w-6 h-6 text-yellow-300" />
                        </div>
                        <div>
                            <h3 className="font-bold text-lg">Google Magic Connect</h3>
                            <p className="text-blue-100 text-sm">We detected your Gmail account. We can automatically find your Analytics and Search Console accounts.</p>
                        </div>
                    </div>
                    <Button
                        onClick={handleMagicConnect}
                        disabled={isDiscovering}
                        className="w-full bg-white text-blue-700 hover:bg-blue-50 font-bold py-6 text-lg"
                    >
                        {isDiscovering ? (
                            <>
                                <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
                                Analyzing Google Account...
                            </>
                        ) : (
                            <>
                                <Sparkles className="w-5 h-5 mr-2" />
                                Discover & Connect Now
                            </>
                        )}
                    </Button>
                </div>
            )}

            {discovered && (
                <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex items-center gap-3 mb-8 text-green-800">
                    <CheckCircle2 className="w-6 h-6 text-green-600" />
                    <div>
                        <p className="font-bold">Success! Properties linked.</p>
                        <p className="text-sm">We've automatically configured your tracking IDs below.</p>
                    </div>
                </div>
            )}

            <div className="space-y-4">
                {/* Google Tag Manager - PRIORITY */}
                <div className="border-2 border-blue-200 rounded-xl p-5 bg-blue-50/30 space-y-4 relative overflow-hidden group hover:border-blue-400 transition-colors">
                    <div className="absolute top-0 right-0 bg-blue-600 text-white text-[10px] px-2 py-0.5 font-bold uppercase tracking-widest rounded-bl-lg">
                        Priority
                    </div>
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-blue-600 p-2 rounded-lg text-white shadow-md">
                                <Sparkles size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-bold">Google Tag Manager</Label>
                                <p className="text-xs text-gray-500">Includes GA4, Ads, and FB Pixel automatically.</p>
                            </div>
                        </div>
                        <Button variant="outline" size="sm" className="bg-white border-blue-200 text-blue-700 font-bold">Priority Setup</Button>
                    </div>
                    <div className="pt-2 border-t border-blue-100 mt-2">
                        <Input
                            placeholder="GTM-XXXXXXX"
                            className="h-9 text-sm border-blue-100 focus:border-blue-500"
                            value={data.gtmId}
                            onChange={(e) => onUpdate({ gtmId: e.target.value })}
                        />
                    </div>
                </div>

                {/* Google Analytics */}
                <div className="border rounded-xl p-5 bg-white space-y-4 relative overflow-hidden group hover:border-slate-300 transition-colors">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-orange-100 p-2 rounded-lg text-orange-600">
                                <BarChart3 size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-semibold">Google Analytics 4</Label>
                                <p className="text-xs text-gray-500">Standalone GA4 connection</p>
                            </div>
                        </div>
                        <Button variant="outline" size="sm" className="bg-white">Connect</Button>
                    </div>
                    <div className="pt-2 border-t mt-2">
                        <Input
                            placeholder="G-XXXXXXXXXX"
                            className="h-8 text-sm"
                            value={data.gaId}
                            onChange={(e) => onUpdate({ gaId: e.target.value })}
                        />
                    </div>
                </div>

                {/* Google Search Console */}
                <div className="border rounded-xl p-5 bg-white space-y-4 hover:border-slate-300 transition-colors">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-blue-100 p-2 rounded-lg text-blue-600">
                                <Search size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-semibold">Search Console</Label>
                                <p className="text-xs text-gray-500">For SEO performance and keywords</p>
                            </div>
                        </div>
                        <Button variant="outline" size="sm" className="bg-white">Connect</Button>
                    </div>
                    <div className="pt-2 border-t mt-2">
                        <Input
                            placeholder="example.com"
                            className="h-8 text-sm"
                            value={data.gscId}
                            onChange={(e) => onUpdate({ gscId: e.target.value })}
                        />
                    </div>
                </div>

                <div className="flex items-center justify-end space-x-2 pt-4">
                    <Switch
                        id="setup-later"
                        checked={data.setupLater}
                        onCheckedChange={(checked) => onUpdate({ setupLater: checked })}
                    />
                    <Label htmlFor="setup-later" className="text-sm text-gray-500">I'll set this up later</Label>
                </div>
            </div>
        </div>
    );
}
