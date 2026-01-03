'use client';

import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { WordPressPluginManager } from './WordPressPluginManager';
import { WordPressContentManager } from './WordPressContentManager';
import { Layout, Package, Activity, Globe, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';
import { connectorsApi } from '@/lib/api/connectors';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

export function WordPressManagementDialog({
    open,
    onOpenChange,
    connectorId,
    connectorName
}: {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    connectorId: string;
    connectorName: string;
}) {
    const [siteInfo, setSiteInfo] = useState<{ url?: string, plugins?: Record<string, any> }>({});
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (open && connectorId === 'wordpress') {
            loadOverview();
        }
    }, [open, connectorId]);

    const loadOverview = async () => {
        setLoading(true);
        try {
            const res = await connectorsApi.performAction(connectorId, 'discover_plugins');
            if (res.data) {
                setSiteInfo(res.data);
            }
        } catch (error) {
            console.error("Failed to load overview", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="max-w-4xl max-h-[90vh] overflow-hidden flex flex-col p-0 gap-0">
                <DialogHeader className="p-6 pb-0 border-b bg-muted/30">
                    <div className="flex justify-between items-start">
                        <div>
                            <DialogTitle className="text-2xl flex items-center gap-2">
                                <Globe className="h-6 w-6 text-primary" />
                                {connectorName} Management
                            </DialogTitle>
                            <DialogDescription className="mt-1">
                                Advanced control for your WordPress site.
                            </DialogDescription>
                        </div>
                        <Button variant="ghost" size="sm" onClick={loadOverview} disabled={loading}>
                            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                        </Button>
                    </div>

                    <div className="flex gap-4 mt-6">
                        {siteInfo.plugins && Object.entries(siteInfo.plugins).map(([slug, meta]: [string, any]) => (
                            <div key={slug} className="flex items-center gap-2 px-3 py-1.5 rounded-full border bg-background text-sm font-medium">
                                {meta.detected ? <CheckCircle2 className="h-4 w-4 text-green-500" /> : <AlertCircle className="h-4 w-4 text-gray-300" />}
                                {meta.label}
                                {meta.detected ? <Badge variant="secondary" className="ml-1 bg-green-50 text-[10px] text-green-700 h-4">Compatible</Badge> : <Badge variant="secondary" className="ml-1 bg-gray-50 text-[10px] text-gray-500 h-4 px-1">Missing</Badge>}
                            </div>
                        ))}
                    </div>

                    <Tabs defaultValue="content" className="w-full mt-6">
                        <TabsList className="bg-transparent h-auto p-0 border-b rounded-none w-full justify-start gap-6">
                            <TabsTrigger
                                value="content"
                                className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent pb-3 px-1 text-base"
                            >
                                <Layout className="h-4 w-4 mr-2" />
                                Content
                            </TabsTrigger>
                            <TabsTrigger
                                value="plugins"
                                className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent pb-3 px-1 text-base"
                            >
                                <Package className="h-4 w-4 mr-2" />
                                Plugins
                            </TabsTrigger>
                        </TabsList>
                        <div className="overflow-y-auto p-6 flex-1 min-h-[500px]">
                            <TabsContent value="content" className="mt-0">
                                <WordPressContentManager connectorId={connectorId} siteUrl={siteInfo.url} />
                            </TabsContent>
                            <TabsContent value="plugins" className="mt-0">
                                <WordPressPluginManager connectorId={connectorId} />
                            </TabsContent>
                        </div>
                    </Tabs>
                </DialogHeader>
            </DialogContent>
        </Dialog>
    );
}
