'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plug, Check, ExternalLink } from 'lucide-react';

export function ConnectorsContent() {
    const [connectors, setConnectors] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Simulator backend fetch
        const loadData = async () => {
            // In real implementation: const res = await fetch('/api/brain/connectors');
            await new Promise(r => setTimeout(r, 800));
            setConnectors([
                { id: 'google-analytics', name: 'Google Analytics 4', description: 'Traffic and conversion tracking', connected: false },
                { id: 'hubspot', name: 'HubSpot CRM', description: 'Customer relationship data sync', connected: true },
                { id: 'slack', name: 'Slack', description: 'Team notifications and alerts', connected: false },
                { id: 'meta-ads', name: 'Meta Ads', description: 'Campaign performance sync', connected: false },
            ]);
            setLoading(false);
        };
        loadData();
    }, []);

    const handleConnect = (id: string) => {
        // Trigger OAuth flow
        console.log('Connecting', id);
        // window.location.href = `/api/integrations/oauth/${id}/initiate`;
    };

    if (loading) return <div className="p-8 text-center text-gray-500">Loading connectors...</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight">Connectors</h2>
                    <p className="text-muted-foreground">Manage your active data connections and integrations.</p>
                </div>
                <Button>Browse Marketplace</Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {connectors.map(c => (
                    <Card key={c.id} className="relative overflow-hidden">
                        {c.connected && (
                            <div className="absolute top-0 right-0 p-2">
                                <span className="flex h-3 w-3 rounded-full bg-green-500"></span>
                            </div>
                        )}
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Plug className="h-5 w-5 text-primary" />
                                {c.name}
                            </CardTitle>
                            <CardDescription>{c.description}</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-center justify-between mt-2">
                                <span className={`text-sm font-medium ${c.connected ? 'text-green-600 dark:text-green-400' : 'text-gray-500'}`}>
                                    {c.connected ? 'Active' : 'Disconnected'}
                                </span>
                                <Button
                                    variant={c.connected ? "outline" : "default"}
                                    size="sm"
                                    onClick={() => handleConnect(c.id)}
                                >
                                    {c.connected ? 'Configure' : 'Connect'}
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
