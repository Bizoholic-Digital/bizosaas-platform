import React, { useState } from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { ToolIntegration } from '../types/onboarding';
import { Globe, ShoppingCart, Users, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

interface Props {
    data: ToolIntegration;
    onUpdate: (data: Partial<ToolIntegration>) => void;
}

export function ServiceConnectionStep({ data, onUpdate }: Props) {
    const [connecting, setConnecting] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    // WordPress credentials state (local)
    const [wpUrl, setWpUrl] = useState(data.wordpress?.siteUrl || '');
    const [wpUser, setWpUser] = useState('');
    const [wpAppPass, setWpAppPass] = useState('');

    const handleConnectWordPress = async () => {
        setConnecting('wordpress');
        setError(null);
        try {
            // In a real implementation, this would call the backend to verify and store credentials
            // For now, we simulate a connection
            await new Promise(resolve => setTimeout(resolve, 1500));

            onUpdate({
                wordpress: {
                    connected: true,
                    siteUrl: wpUrl,
                    // Bedrock alignment: Use /wp/wp-admin as default for BizoSaaS managed Bedrock
                    adminUrl: wpUrl.endsWith('/wp') ? `${wpUrl}/wp-admin` : `${wpUrl.replace(/\/$/, '')}/wp/wp-admin`
                }
            });
        } catch (err) {
            setError('Failed to connect to WordPress. Please check your credentials.');
        } finally {
            setConnecting(null);
        }
    };

    const handleConnectFluentCRM = () => {
        // FluentCRM usually lives inside WordPress, so if WP is connected, we can just enable it
        if (!data.wordpress?.connected) {
            setError('Please connect WordPress first to enable FluentCRM integration.');
            return;
        }

        onUpdate({
            fluentCrm: {
                connected: !data.fluentCrm?.connected
            }
        });
    };

    const handleConnectWooCommerce = () => {
        // Similarly, WooCommerce lives inside WP often, or we might need separate keys
        if (!data.wordpress?.connected) {
            setError('Please connect WordPress first to enable WooCommerce integration.');
            return;
        }

        onUpdate({
            wooCommerce: {
                connected: !data.wooCommerce?.connected
            }
        });
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-foreground">Connect Your Services</h2>
                <p className="text-muted-foreground">Integrate your existing platforms to power AI automation.</p>
            </div>

            {error && (
                <div className="bg-red-50 text-red-600 p-3 rounded-lg flex items-center gap-2 text-sm">
                    <AlertCircle size={16} />
                    {error}
                </div>
            )}

            <div className="grid gap-6">
                {/* WordPress Connection Card */}
                <Card className={`border-2 ${data.wordpress?.connected ? 'border-green-500 bg-green-50/10' : 'border-gray-200'}`}>
                    <CardContent className="p-6">
                        <div className="flex items-start justify-between mb-4">
                            <div className="flex items-center gap-3">
                                <div className="bg-blue-100 p-2.5 rounded-lg text-blue-600">
                                    <Globe size={24} />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-lg">WordPress</h3>
                                    <p className="text-sm text-muted-foreground">Connect your website for content management</p>
                                </div>
                            </div>
                            {data.wordpress?.connected && (
                                <div className="flex items-center gap-1 text-green-600 font-medium text-sm bg-green-100 px-3 py-1 rounded-full">
                                    <CheckCircle size={14} />
                                    Connected
                                </div>
                            )}
                        </div>

                        {!data.wordpress?.connected ? (
                            <div className="space-y-4 pt-2">
                                <div className="grid gap-2">
                                    <Label>Website URL</Label>
                                    <Input
                                        placeholder="https://your-site.com"
                                        value={wpUrl}
                                        onChange={e => setWpUrl(e.target.value)}
                                    />
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="grid gap-2">
                                        <Label>Username</Label>
                                        <Input
                                            placeholder="admin"
                                            value={wpUser}
                                            onChange={e => setWpUser(e.target.value)}
                                        />
                                    </div>
                                    <div className="grid gap-2">
                                        <Label>Application Password</Label>
                                        <Input
                                            type="password"
                                            placeholder="xxxx xxxx xxxx xxxx"
                                            value={wpAppPass}
                                            onChange={e => setWpAppPass(e.target.value)}
                                        />
                                    </div>
                                </div>
                                <Button
                                    className="w-full bg-blue-600 hover:bg-blue-700"
                                    onClick={handleConnectWordPress}
                                    disabled={!wpUrl || !wpUser || !wpAppPass || connecting === 'wordpress'}
                                >
                                    {connecting === 'wordpress' ? (
                                        <>
                                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                            Connecting...
                                        </>
                                    ) : 'Connect WordPress'}
                                </Button>
                                <p className="text-xs text-center text-muted-foreground/60">
                                    Go to Users → Profile → Application Passwords in WP Admin to generate one.
                                </p>
                            </div>
                        ) : (
                            <div className="flex justify-between items-center bg-card p-3 rounded border">
                                <span className="text-sm text-muted-foreground truncate">{data.wordpress.siteUrl}</span>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    className="text-red-500 hover:text-red-700 hover:bg-red-50"
                                    onClick={() => onUpdate({ wordpress: { connected: false } })}
                                >
                                    Disconnect
                                </Button>
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* FluentCRM & WooCommerce (Dependent on WP) */}
                <div className="grid md:grid-cols-2 gap-6">
                    {/* FluentCRM */}
                    <Card className={`transition-all ${!data.wordpress?.connected ? 'opacity-50 grayscale' : ''}`}>
                        <CardContent className="p-5">
                            <div className="flex items-center gap-3 mb-4">
                                <div className="bg-purple-100 p-2 rounded-lg text-purple-600">
                                    <Users size={20} />
                                </div>
                                <div>
                                    <h3 className="font-semibold">FluentCRM</h3>
                                    <p className="text-xs text-muted-foreground">Marketing automation</p>
                                </div>
                            </div>
                            <Button
                                variant={data.fluentCrm?.connected ? "outline" : "default"}
                                className={`w-full ${data.fluentCrm?.connected ? "border-green-500 text-green-600 bg-green-50" : "bg-purple-600 hover:bg-purple-700"}`}
                                onClick={handleConnectFluentCRM}
                                disabled={!data.wordpress?.connected}
                            >
                                {data.fluentCrm?.connected ? (
                                    <>
                                        <CheckCircle className="mr-2 h-4 w-4" />
                                        Enabled
                                    </>
                                ) : "Enable Integration"}
                            </Button>
                        </CardContent>
                    </Card>

                    {/* WooCommerce */}
                    <Card className={`transition-all ${!data.wordpress?.connected ? 'opacity-50 grayscale' : ''}`}>
                        <CardContent className="p-5">
                            <div className="flex items-center gap-3 mb-4">
                                <div className="bg-orange-100 p-2 rounded-lg text-orange-600">
                                    <ShoppingCart size={20} />
                                </div>
                                <div>
                                    <h3 className="font-semibold">WooCommerce</h3>
                                    <p className="text-xs text-muted-foreground">E-commerce store</p>
                                </div>
                            </div>
                            <Button
                                variant={data.wooCommerce?.connected ? "outline" : "default"}
                                className={`w-full ${data.wooCommerce?.connected ? "border-green-500 text-green-600 bg-green-50" : "bg-orange-600 hover:bg-orange-700"}`}
                                onClick={handleConnectWooCommerce}
                                disabled={!data.wordpress?.connected}
                            >
                                {data.wooCommerce?.connected ? (
                                    <>
                                        <CheckCircle className="mr-2 h-4 w-4" />
                                        Enabled
                                    </>
                                ) : "Enable Integration"}
                            </Button>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
