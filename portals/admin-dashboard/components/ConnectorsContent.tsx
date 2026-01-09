'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Plug, Check, RefreshCw, X, Layout, Database, ShoppingCart, Search, MapPin, Star, Calendar, Mail, MessageSquare, Zap, Activity, Video, Monitor, Facebook, Tag } from 'lucide-react';
import { connectorsApi, ConnectorConfig, ConnectorCredentials } from '@/lib/api/connectors';
import { toast } from 'sonner';
import { useSearchParams } from 'next/navigation';
import { DiscoveryWidget } from '@/components/DiscoveryWidget';


// Icon mapping
const ICONS: Record<string, any> = {
    wordpress: Layout,
    fluentcrm: Database,
    woocommerce: ShoppingCart,
    facebook: Facebook,
    tag: Tag,
    bing: Search,
    'map-pin': MapPin,
    yelp: Star,
    calendly: Calendar,
    mailchimp: Mail,
    'search-console': Search,
    'google-ads': Monitor,
    twilio: MessageSquare,
    gohighlevel: Zap,
    hubspot: Activity,
    'tiktok-ads': Video,
    default: Plug
};

export function ConnectorsContent() {
    const searchParams = useSearchParams();
    const activeCategory = searchParams.get('category');
    const [connectors, setConnectors] = useState<ConnectorConfig[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedConnector, setSelectedConnector] = useState<ConnectorConfig | null>(null);
    const [credentials, setCredentials] = useState<ConnectorCredentials>({});
    const [isConnecting, setIsConnecting] = useState(false);
    const [isValidating, setIsValidating] = useState(false);
    const [dialogOpen, setDialogOpen] = useState(false);


    // Mock data for initial development - Replace with API call later
    const MOCK_CONNECTORS: ConnectorConfig[] = [
        {
            id: 'wordpress',
            name: 'WordPress',
            type: 'cms',
            description: 'Connect your WordPress site to sync pages, posts, and media.',
            icon: 'wordpress',
            version: '2.0.0',
            status: 'disconnected',
            auth_schema: {
                url: { type: 'string', label: 'WordPress Site URL', placeholder: 'https://your-site.com', required: true },
                username: { type: 'string', label: 'Username', required: true },
                application_password: { type: 'password', label: 'Application Password', help: 'Generate in Users > Profile', required: true }
            }
        },
        {
            id: 'fluentcrm',
            name: 'FluentCRM',
            type: 'crm',
            description: 'Sync contacts, tags, and campaigns from FluentCRM.',
            icon: 'fluentcrm',
            version: '1.0.0',
            status: 'disconnected',
            auth_schema: {
                url: { type: 'string', label: 'WordPress Site URL', placeholder: 'https://your-site.com', required: true },
                username: { type: 'string', label: 'Username', required: true },
                application_password: { type: 'password', label: 'Application Password', required: true }
            }
        },
        {
            id: 'woocommerce',
            name: 'WooCommerce',
            type: 'ecommerce',
            description: 'Sync products, orders, and customers from your store.',
            icon: 'woocommerce',
            version: '1.0.0',
            status: 'disconnected',
            auth_schema: {
                url: { type: 'string', label: 'Store URL', placeholder: 'https://your-store.com', required: true },
                consumer_key: { type: 'string', label: 'Consumer Key (CK)', required: true },
                consumer_secret: { type: 'password', label: 'Consumer Secret (CS)', required: true }
            }
        }
    ];

    // Filtered list for display
    const filteredConnectors = connectors.filter(c => {
        if (!activeCategory || activeCategory === 'all') return true;
        return c.type === (activeCategory as any);
    });

    const categoryTitles: Record<string, string> = {
        crm: 'CRM & Marketing Automation',
        cms: 'Content Management Systems',
        ecommerce: 'E-commerce Platforms',
        analytics: 'Analytics & Search Console',
        marketing: 'Digital Marketing & Ads',
        all: 'All Data Connectors'
    };

    const categoryDescription: Record<string, string> = {
        crm: 'Manage your sales pipelines, contacts, and marketing automation.',
        cms: 'Connect your websites and blogs to sync content and media.',
        ecommerce: 'Sync products, orders, and customers from your online stores.',
        analytics: 'Monitor your website performance and SEO intelligence.',
        marketing: 'Manage your ad campaigns and social media presence.',
        all: 'Manage your integrations with external CMS, CRM, and E-commerce platforms.'
    };

    const currentTitle = activeCategory ? (categoryTitles[activeCategory] || 'Connectors') : 'Data Connectors';
    const currentDesc = activeCategory ? (categoryDescription[activeCategory] || 'Manage your integrations.') : 'Manage your integrations with external CMS, CRM, and E-commerce platforms.';


    useEffect(() => {
        loadConnectors();
    }, []);

    const loadConnectors = async () => {
        setLoading(true);
        try {
            const res = await connectorsApi.getConnectors();
            if (res.data && Array.isArray(res.data)) {
                // Merge real status into mock definitions to maintain the full list of available connectors
                const merged = MOCK_CONNECTORS.map(mock => {
                    const real = (res.data as any[]).find(r => r.id === mock.id);
                    return real ? { ...mock, ...real } : mock;
                });
                setConnectors(merged);
            } else {
                setConnectors(MOCK_CONNECTORS);
            }
        } catch (error) {
            console.error("Failed to load connectors", error);
            setConnectors(MOCK_CONNECTORS);
        } finally {
            setLoading(false);
        }
    };

    const handleOpenConnect = (connector: ConnectorConfig) => {
        setSelectedConnector(connector);
        setCredentials({});
        setDialogOpen(true);
    };

    const handleCredentialChange = (key: string, value: string) => {
        setCredentials(prev => ({
            ...prev,
            [key]: value
        }));
    };

    const handleConnect = async () => {
        if (!selectedConnector) return;

        setIsValidating(true);
        try {
            setIsConnecting(true);
            const res = await connectorsApi.connectService(selectedConnector.id, credentials);

            if (res.error) throw new Error(res.error);

            toast.success(`Successfully connected to ${selectedConnector.name}`);
            setDialogOpen(false);

            setConnectors(prev => prev.map(c =>
                c.id === selectedConnector.id ? { ...c, status: 'connected', lastSync: new Date().toISOString() } : c
            ));

        } catch (error: any) {
            console.error("Connection failed", error);
            toast.error(error.message || "Failed to connect");
        } finally {
            setIsValidating(false);
            setIsConnecting(false);
        }
    };

    const handleDisconnect = async (connector: ConnectorConfig) => {
        try {
            await connectorsApi.disconnectService(connector.id);
            toast.success(`Disconnected ${connector.name}`);
            setConnectors(prev => prev.map(c =>
                c.id === connector.id ? { ...c, status: 'disconnected', lastSync: undefined } : c
            ));
        } catch (error) {
            toast.error("Failed to disconnect");
        }
    };

    const handleSync = async (connector: ConnectorConfig) => {
        try {
            toast.info(`Syncing ${connector.name}...`);
            setConnectors(prev => prev.map(c =>
                c.id === connector.id ? { ...c, status: 'syncing' } : c
            ));

            setTimeout(() => {
                setConnectors(prev => prev.map(c =>
                    c.id === connector.id ? { ...c, status: 'connected', lastSync: new Date().toISOString() } : c
                ));
                toast.success(`Synced ${connector.name}`);
            }, 2000);

        } catch (error) {
            toast.error("Sync failed");
        }
    };

    if (loading) return (
        <div className="flex items-center justify-center p-12">
            <RefreshCw className="h-8 w-8 animate-spin text-primary" />
        </div>
    );

    return (
        <div className="space-y-6">
            <DiscoveryWidget />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredConnectors.map(c => {
                    const Icon = ICONS[c.icon] || ICONS.default;
                    const isConnected = c.status?.toUpperCase() === 'CONNECTED' || c.status?.toUpperCase() === 'SYNCING';

                    return (
                        <Card key={c.id} className={`relative overflow-hidden transition-all ${isConnected ? 'border-primary/50 bg-primary/5' : ''}`}>
                            {isConnected && (
                                <div className="absolute top-0 right-0 p-3">
                                    <Badge variant="default" className="bg-green-600 hover:bg-green-700">
                                        <Check className="h-3 w-3 mr-1" /> Connected
                                    </Badge>
                                </div>
                            )}
                            <CardHeader>
                                <div className="flex items-center gap-3 mb-2">
                                    <div className={`p-2 rounded-lg ${isConnected ? 'bg-primary/20 text-primary' : 'bg-muted text-muted-foreground'}`}>
                                        <Icon className="h-6 w-6" />
                                    </div>
                                    <CardTitle>{c.name}</CardTitle>
                                </div>
                                <CardDescription className="h-10 line-clamp-2">
                                    {c.description}
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-3">
                                    <div className="flex items-center justify-between text-sm">
                                        <span className="text-muted-foreground">Version</span>
                                        <span className="font-mono">{c.version}</span>
                                    </div>
                                    <div className="flex items-center justify-between text-sm">
                                        <span className="text-muted-foreground">Status</span>
                                        <span className={`font-medium ${c.status === 'connected' ? 'text-green-600' :
                                            c.status === 'syncing' ? 'text-blue-600 animate-pulse' : 'text-gray-500'
                                            }`}>
                                            {c.status.charAt(0).toUpperCase() + c.status.slice(1)}
                                        </span>
                                    </div>
                                    {c.lastSync && (
                                        <div className="flex items-center justify-between text-xs text-muted-foreground">
                                            <span>Last Synced</span>
                                            <span>{new Date(c.lastSync).toLocaleDateString()}</span>
                                        </div>
                                    )}
                                </div>
                            </CardContent>
                            <CardFooter className="flex gap-2">
                                {isConnected ? (
                                    <>
                                        <Button variant="outline" className="w-full" onClick={() => handleSync(c)} disabled={c.status === 'syncing'}>
                                            <RefreshCw className={`mr-2 h-4 w-4 ${c.status === 'syncing' ? 'animate-spin' : ''}`} />
                                            Sync
                                        </Button>
                                        <Button variant="destructive" size="icon" onClick={() => handleDisconnect(c)}>
                                            <X className="h-4 w-4" />
                                        </Button>
                                    </>
                                ) : (
                                    <Button className="w-full" onClick={() => handleOpenConnect(c)}>
                                        Connect
                                    </Button>
                                )}
                            </CardFooter>
                        </Card>
                    );
                })}
            </div>

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Connect {selectedConnector?.name}</DialogTitle>
                        <DialogDescription>
                            Enter your credentials to establish a secure connection.
                        </DialogDescription>
                    </DialogHeader>

                    <div className="space-y-4 py-4">
                        {selectedConnector && selectedConnector.auth_schema && Object.entries(selectedConnector.auth_schema).map(([key, field]: [string, any]) => (
                            <div key={key} className="space-y-2">
                                <Label htmlFor={key}>
                                    {field.label}
                                    {field.required && <span className="text-red-500 ml-1">*</span>}
                                </Label>
                                <Input
                                    id={key}
                                    type={field.type}
                                    placeholder={field.placeholder}
                                    value={credentials[key] as string || ''}
                                    onChange={(e) => handleCredentialChange(key, e.target.value)}
                                />
                                {field.help && <p className="text-xs text-muted-foreground">{field.help}</p>}
                            </div>
                        ))}
                    </div>

                    <DialogFooter>
                        <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                        <Button onClick={handleConnect} disabled={isValidating || isConnecting}>
                            {(isValidating || isConnecting) && <RefreshCw className="mr-2 h-4 w-4 animate-spin" />}
                            {isValidating ? 'Validating...' : 'Connect'}
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}

export default ConnectorsContent;
