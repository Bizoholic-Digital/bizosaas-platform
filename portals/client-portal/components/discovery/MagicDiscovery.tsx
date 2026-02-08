'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Sparkles, RefreshCw, CheckCircle2, X } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { toast } from 'sonner';
import { useAuth } from '@/components/auth/AuthProvider';
import { DiscoveryModal } from './DiscoveryModal';

export function MagicDiscovery() {
    const { getToken, user } = useAuth();
    const [isVisible, setIsVisible] = useState(false);
    const [isDiscovering, setIsDiscovering] = useState(false);
    const [discoveredData, setDiscoveredData] = useState<any>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        // Check if we should show discovery
        // TODO: Re-implement external account detection with Authentik
        const hasGoogle = false;
        const discoveryDismissed = localStorage.getItem('magic_discovery_dismissed');

        if (hasGoogle && !discoveryDismissed) {
            setIsVisible(true);
        }
    }, [user]);

    const handleDiscover = async () => {
        setIsDiscovering(true);
        try {
            const token = await getToken();
            // const googleAcc = user?.externalAccounts.find(acc => acc.provider === 'google');
            // if (!googleAcc) throw new Error("No Google account linked");

            // 1. First perform discovery (dry run)
            const res = await brainApi.connectors.autoLinkGoogle('MOCK_GOOGLE_TOKEN', { dry_run: true }, token || undefined);

            setDiscoveredData(res.discovered);
            setIsModalOpen(true);
            toast.success("Accounts discovered! Please select which ones to link.");
        } catch (error) {
            console.error("Discovery failed", error);
            toast.error("Account discovery failed. Please connect manually.");
        } finally {
            setIsDiscovering(false);
        }
    };

    const handleConfirmLink = async (selectedIds: string[]) => {
        try {
            const token = await getToken();
            const res = await brainApi.connectors.autoLinkGoogle('MOCK_GOOGLE_TOKEN', {
                dry_run: false,
                selected_connectors: selectedIds
            }, token || undefined);

            setDiscoveredData(res.discovered);
            toast.success(`Successfully connected ${selectedIds.length} accounts!`);
        } catch (error) {
            console.error("Linking failed", error);
            toast.error("Failed to link selected accounts.");
            throw error;
        }
    };

    const dismiss = () => {
        setIsVisible(false);
        localStorage.setItem('magic_discovery_dismissed', 'true');
    };

    if (!isVisible) return null;

    return (
        <Card className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white border-none shadow-xl overflow-hidden mb-8 relative group">
            <div className="absolute top-0 right-0 p-2">
                <button onClick={dismiss} className="p-1 hover:bg-white/20 rounded-full transition-colors">
                    <X className="w-4 h-4" />
                </button>
            </div>

            <CardContent className="p-6">
                <div className="flex flex-col md:flex-row items-center gap-6">
                    <div className="bg-white/20 p-4 rounded-2xl backdrop-blur-md animate-pulse">
                        <Sparkles className="w-10 h-10 text-yellow-300" />
                    </div>

                    <div className="flex-1 text-center md:text-left">
                        <h3 className="text-2xl font-bold mb-1 flex items-center justify-center md:justify-start gap-2">
                            Magic Discovery Active
                            <span className="bg-white/20 text-[10px] uppercase px-2 py-0.5 rounded-full font-bold tracking-widest">AI Sync</span>
                        </h3>
                        <p className="text-indigo-100 text-sm max-w-xl">
                            We've detected a connected Google account. Let our AI automatically find and link your Analytics, Ads, and Business Profile properties in one click.
                        </p>
                    </div>

                    <div className="shrink-0 w-full md:w-auto">
                        <Button
                            onClick={handleDiscover}
                            disabled={isDiscovering}
                            className="w-full md:w-auto bg-white text-indigo-700 hover:bg-indigo-50 font-bold px-8 py-6 text-lg shadow-lg active:scale-95 transition-all"
                        >
                            {isDiscovering ? (
                                <>
                                    <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
                                    Scanning Properties...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-5 h-5 mr-2" />
                                    Launch Discovery
                                </>
                            )}
                        </Button>
                    </div>
                </div>

                {discoveredData && (
                    <div className="mt-6 pt-6 border-t border-white/20 grid grid-cols-2 md:grid-cols-4 gap-4 animate-in slide-in-from-top-4 duration-500">
                        {Object.entries(discoveredData).map(([key, val]: [string, any]) => (
                            <div key={key} className="bg-white/10 rounded-xl p-3 flex items-center gap-3">
                                <CheckCircle2 className="w-5 h-5 text-green-300" />
                                <div className="min-w-0">
                                    <p className="text-[10px] uppercase font-bold text-indigo-200 truncate">{key.replace('google-', '')}</p>
                                    <p className="text-xs font-medium truncate">Connected</p>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </CardContent>

            {discoveredData && (
                <DiscoveryModal
                    isOpen={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                    discoveredData={discoveredData}
                    onConfirm={handleConfirmLink}
                />
            )}
        </Card>
    );
}
