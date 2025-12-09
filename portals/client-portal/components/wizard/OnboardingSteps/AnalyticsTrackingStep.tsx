import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { AnalyticsConfig } from '../types/onboarding';
import { BarChart3, Search } from 'lucide-react';

interface Props {
    data: AnalyticsConfig;
    onUpdate: (data: Partial<AnalyticsConfig>) => void;
}

export function AnalyticsTrackingStep({ data, onUpdate }: Props) {
    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Tracking & Analytics</h2>
                <p className="text-gray-500">Data fuels our AI agents. Let's connect your sources.</p>
            </div>

            <div className="space-y-4">
                {/* Google Analytics */}
                <div className="border rounded-xl p-5 bg-white space-y-4 relative overflow-hidden group hover:border-blue-300 transition-colors">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="bg-orange-100 p-2 rounded-lg text-orange-600">
                                <BarChart3 size={24} />
                            </div>
                            <div className="space-y-1">
                                <Label className="text-base font-semibold">Google Analytics 4</Label>
                                <p className="text-xs text-gray-500">For website traffic and conversion data</p>
                            </div>
                        </div>
                        {/* Mock Connect Button - In real app, this triggers OAuth */}
                        <Button variant="outline" size="sm" className="bg-white">Connect</Button>
                    </div>
                    <div className="pt-2 border-t mt-2">
                        <Label className="text-xs text-gray-500 mb-1.5 block">Or enter Property ID manually</Label>
                        <Input
                            placeholder="G-XXXXXXXXXX"
                            className="h-8 text-sm"
                            value={data.gaId}
                            onChange={(e) => onUpdate({ gaId: e.target.value })}
                        />
                    </div>
                </div>

                {/* Google Search Console */}
                <div className="border rounded-xl p-5 bg-white space-y-4 hover:border-blue-300 transition-colors">
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
                        <Label className="text-xs text-gray-500 mb-1.5 block">Or enter Domain property</Label>
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
