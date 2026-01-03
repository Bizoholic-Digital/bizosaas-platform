'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { RefreshCw, Search, Plus, Trash2, Power, PowerOff, ExternalLink, Package } from 'lucide-react';
import { connectorsApi } from '@/lib/api/connectors';
import { toast } from 'sonner';

export interface WordPressPlugin {
    id: string;
    name: string;
    slug: string;
    version: string;
    status: 'active' | 'inactive';
    description: string;
    author: string;
}

export interface WPOrgPlugin {
    name: string;
    slug: string;
    version: string;
    author: string;
    short_description: string;
    rating: number;
    downloaded: number;
}

export function WordPressPluginManager({ connectorId }: { connectorId: string }) {
    const [plugins, setPlugins] = useState<WordPressPlugin[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [directoryResults, setDirectoryResults] = useState<WPOrgPlugin[]>([]);
    const [searching, setSearching] = useState(false);
    const [activeTab, setActiveTab] = useState('installed');

    const loadPlugins = async () => {
        setLoading(true);
        try {
            const res = await connectorsApi.syncResource<{ data: WordPressPlugin[] }>(connectorId, 'plugins');
            if (res.data?.data) {
                setPlugins(res.data.data);
            }
        } catch (error) {
            console.error("Failed to load plugins", error);
            toast.error("Failed to load WordPress plugins");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadPlugins();
    }, [connectorId]);

    const handleToggle = async (slug: string, currentStatus: string) => {
        const newStatus = currentStatus === 'active' ? false : true;
        try {
            toast.info(`${newStatus ? 'Activating' : 'Deactivating'} plugin...`);
            const res = await connectorsApi.performAction<{ status: string }>(connectorId, 'toggle_plugin', {
                slug,
                active: newStatus
            });
            if (res.data?.status === 'success') {
                toast.success(`Plugin ${newStatus ? 'activated' : 'deactivated'}`);
                loadPlugins();
            } else {
                throw new Error("Failed to toggle plugin");
            }
        } catch (error) {
            toast.error("Action failed");
        }
    };

    const handleUninstall = async (slug: string) => {
        if (!confirm("Are you sure you want to uninstall this plugin?")) return;
        try {
            const res = await connectorsApi.performAction<{ status: string }>(connectorId, 'uninstall_plugin', { slug });
            if (res.data?.status === 'success') {
                toast.success("Plugin uninstalled");
                loadPlugins();
            }
        } catch (error) {
            toast.error("Uninstall failed");
        }
    };

    const handleSearchDirectory = async () => {
        if (!searchTerm) return;
        setSearching(true);
        try {
            const res = await connectorsApi.performAction<{ plugins: WPOrgPlugin[] }>(connectorId, 'search_plugin_directory', { query: searchTerm });
            if (res.data?.plugins) {
                setDirectoryResults(res.data.plugins);
            }
        } catch (error) {
            toast.error("Directory search failed");
        } finally {
            setSearching(false);
        }
    };

    const handleInstall = async (slug: string) => {
        toast.info("Standard WordPress REST API does not support remote installs. Log into your dashboard to install this plugin.", {
            description: `Plugin slug: ${slug}`,
            duration: 5000
        });
        // In a real scenario we'd call install_plugin if supported
    };

    return (
        <Card className="border-none shadow-none">
            <CardHeader className="px-0 pt-0">
                <div className="flex justify-between items-center">
                    <div>
                        <CardTitle>Plugin Management</CardTitle>
                        <CardDescription>Manage your WordPress plugins and discover new ones.</CardDescription>
                    </div>
                    <Button variant="outline" size="sm" onClick={loadPlugins} disabled={loading}>
                        <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                        Refresh
                    </Button>
                </div>
            </CardHeader>
            <CardContent className="px-0">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                    <TabsList className="mb-4">
                        <TabsTrigger value="installed">Installed Plugins ({plugins.length})</TabsTrigger>
                        <TabsTrigger value="directory">Wp.org Directory</TabsTrigger>
                    </TabsList>

                    <TabsContent value="installed" className="space-y-4">
                        {loading && plugins.length === 0 ? (
                            <div className="flex justify-center p-8 text-muted-foreground italic">Loading plugins...</div>
                        ) : plugins.length === 0 ? (
                            <div className="flex justify-center p-8 text-muted-foreground italic">No plugins found.</div>
                        ) : (
                            <div className="grid grid-cols-1 gap-3">
                                {plugins.map(plugin => (
                                    <div key={plugin.id} className="flex items-center justify-between p-3 rounded-lg border bg-card hover:bg-accent/5 transition-colors">
                                        <div className="flex items-center gap-3">
                                            <div className={`p-2 rounded bg-primary/10 ${plugin.status === 'active' ? 'text-primary' : 'text-muted-foreground'}`}>
                                                <Package className="h-5 w-5" />
                                            </div>
                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <span className="font-medium">{plugin.name}</span>
                                                    <Badge variant={plugin.status === 'active' ? 'default' : 'secondary'} className="text-[10px]">
                                                        {plugin.status}
                                                    </Badge>
                                                </div>
                                                <p className="text-xs text-muted-foreground line-clamp-1 max-w-[400px]">
                                                    v{plugin.version} | by {plugin.author}
                                                </p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                onClick={() => handleToggle(plugin.id, plugin.status)}
                                                title={plugin.status === 'active' ? 'Deactivate' : 'Activate'}
                                            >
                                                {plugin.status === 'active' ? <PowerOff className="h-4 w-4 text-orange-500" /> : <Power className="h-4 w-4 text-green-500" />}
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                className="text-red-500 hover:text-red-600 hover:bg-red-50"
                                                onClick={() => handleUninstall(plugin.id)}
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </TabsContent>

                    <TabsContent value="directory" className="space-y-4">
                        <div className="flex gap-2">
                            <Input
                                placeholder="Search plugins (e.g. WooCommerce, FluentCRM)..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSearchDirectory()}
                            />
                            <Button onClick={handleSearchDirectory} disabled={searching}>
                                {searching ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
                            </Button>
                        </div>

                        <div className="grid grid-cols-1 gap-3">
                            {directoryResults.map(plugin => (
                                <div key={plugin.slug} className="flex items-center justify-between p-4 rounded-lg border bg-card">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className="font-bold">{plugin.name}</span>
                                            <span className="text-xs text-muted-foreground">v{plugin.version}</span>
                                        </div>
                                        <p className="text-sm text-muted-foreground" dangerouslySetInnerHTML={{ __html: plugin.short_description }} />
                                        <div className="flex gap-4 mt-2 text-xs text-muted-foreground">
                                            <span>by {plugin.author.replace(/<[^>]*>?/gm, '')}</span>
                                            <span>⭐ {plugin.rating}/100</span>
                                        </div>
                                    </div>
                                    <Button size="sm" onClick={() => handleInstall(plugin.slug)}>
                                        <Plus className="h-4 w-4 mr-1" /> Install
                                    </Button>
                                </div>
                            ))}
                            {directoryResults.length === 0 && !searching && searchTerm && (
                                <div className="text-center py-8 text-muted-foreground">No results found in WordPress directory.</div>
                            )}
                            {directoryResults.length === 0 && !searching && !searchTerm && (
                                <div className="text-center py-8 text-muted-foreground">Search for plugins to integrate more features.</div>
                            )}
                        </div>
                    </TabsContent>
                </Tabs>
            </CardContent>
        </Card>
    );
}
