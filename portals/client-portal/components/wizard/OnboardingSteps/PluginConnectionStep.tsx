import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Download, RefreshCw, CheckCircle, AlertTriangle, ExternalLink, ShieldCheck } from 'lucide-react';
import { toast } from 'sonner';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface Props {
    websiteUrl?: string; // e.g. "bizoholic.com"
    onVerified: () => void;
    onSkip?: () => void;
}

export function PluginConnectionStep({ websiteUrl, onVerified, onSkip }: Props) {
    const [status, setStatus] = useState<'checking' | 'connected' | 'not_connected'>('checking');
    const [isVerifying, setIsVerifying] = useState(false);
    const [isConnecting, setIsConnecting] = useState(false);
    const [apiKey, setApiKey] = useState('demo_key_12345');

    // Auto-Connect Form State
    const [wpUser, setWpUser] = useState('');
    const [wpAppPass, setWpAppPass] = useState('');

    const normalizedUrl = websiteUrl?.startsWith('http') ? websiteUrl : `https://${websiteUrl}`;

    // Auto-check on mount
    useEffect(() => {
        if (websiteUrl) {
            verifyPlugin(true);
        } else {
            setStatus('not_connected');
        }
    }, [websiteUrl]);

    const verifyPlugin = async (silent = false) => {
        if (!silent) setIsVerifying(true);
        try {
            const res = await fetch('/api/brain/onboarding/tools/verify-plugin', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ website_url: websiteUrl })
            });

            if (res.ok) {
                const data = await res.json();
                if (data.status === 'connected') {
                    setStatus('connected');
                    if (!silent) toast.success("Plugin detected and connected securely!");
                    onVerified();
                    return;
                }
            }
            if (!silent) setStatus('not_connected');
        } catch (error) {
            console.error(error);
            if (!silent) setStatus('not_connected');
        } finally {
            if (!silent) setIsVerifying(false);
        }
    };

    const handleAutoConnect = async () => {
        setIsConnecting(true);
        try {
            const res = await fetch('/api/brain/onboarding/tools/connect-wordpress', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    website_url: websiteUrl,
                    username: wpUser,
                    application_password: wpAppPass
                })
            });

            if (res.ok) {
                const data = await res.json();
                if (data.status === 'connected') {
                    setStatus('connected');
                    toast.success(`Connected to WordPress as ${data.wp_user_name}!`);
                    onVerified();
                } else {
                    toast.error(data.message || "Connection failed. Check credentials.");
                }
            } else {
                toast.error("Connection failed.");
            }
        } catch (err) {
            toast.error("Network error connecting to site.");
        } finally {
            setIsConnecting(false);
        }
    };

    const downloadPlugin = () => {
        window.open('/api/brain/onboarding/tools/download-plugin', '_blank');
        toast.info("Downloading BizoSaaS Connect plugin...");
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-foreground">Connect Your Website</h2>
                <p className="text-muted-foreground mt-2 max-w-lg mx-auto">
                    Link your website to enable AI Agents to manage content, analytics, and optimization.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
                {/* Visual Graphic */}
                <div className="relative hidden md:block h-80 bg-blue-500/5 rounded-2xl flex items-center justify-center">
                    {status === 'connected' ? (
                        <div className="text-center space-y-4">
                            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto animate-bounce">
                                <CheckCircle className="w-10 h-10 text-green-600" />
                            </div>
                            <h3 className="text-xl font-bold text-green-700">Securely Connected</h3>
                            <p className="text-sm text-green-600 px-8">
                                BizoSaaS Agents now have authorized access to manage your site's intelligence.
                            </p>
                        </div>
                    ) : (
                        <div className="flex flex-col items-center gap-4 opacity-80">
                            <div className="flex items-center gap-4">
                                <div className="bg-white dark:bg-slate-800 p-4 rounded-xl shadow-lg border border-border w-24 h-24 flex flex-col items-center justify-center">
                                    <div className="text-4xl">🌍</div>
                                    <div className="mt-2 text-[10px] font-bold text-center">Your Site</div>
                                </div>
                                <div className="w-16 h-1 bg-dashed border-t-2 border-dashed border-gray-300 relative">
                                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-card border rounded-full p-1">
                                        <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse" />
                                    </div>
                                </div>
                                <div className="bg-white dark:bg-slate-800 p-4 rounded-xl shadow-lg border border-border w-24 h-24 flex flex-col items-center justify-center">
                                    <ShieldCheck className="w-8 h-8 text-blue-600" />
                                    <div className="mt-2 text-[10px] font-bold text-center">BizoSaaS</div>
                                </div>
                            </div>
                            <p className="text-xs text-muted-foreground mt-4">Waiting for handshake...</p>
                        </div>
                    )}
                </div>

                {/* Actions */}
                <div className="space-y-6">
                    {status === 'connected' ? (
                        <div className="space-y-4">
                            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-xl p-6">
                                <h3 className="font-bold text-green-800 mb-2">Connection Active</h3>
                                <p className="text-sm text-green-700">We have established a secure link to <b>{normalizedUrl}</b>.</p>
                            </div>
                            <Button className="w-full" onClick={onSkip}>Continue to Next Step</Button>
                        </div>
                    ) : (
                        <Tabs defaultValue="manual" className="w-full">
                            <TabsList className="grid w-full grid-cols-2 mb-4">
                                <TabsTrigger value="manual">Plugin (Robust) *</TabsTrigger>
                                <TabsTrigger value="auto">Auto-Connect</TabsTrigger>
                            </TabsList>

                            <Alert className="mb-4 bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800">
                                <AlertDescription className="text-xs text-blue-800 dark:text-blue-300">
                                    <span className="font-semibold">* Recommended:</span> The Plugin method provides better security, reliability, and full feature access. Auto-Connect is faster but may have limited functionality.
                                </AlertDescription>
                            </Alert>

                            <TabsContent value="manual">
                                <Card className="shadow-md">
                                    <CardContent className="pt-6 space-y-4">
                                        <div className="space-y-2">
                                            <h3 className="font-bold text-sm">1. Download Plugin</h3>
                                            <Button onClick={downloadPlugin} variant="outline" className="w-full justify-start h-auto py-3">
                                                <Download className="w-5 h-5 mr-3 text-blue-600" />
                                                <div className="text-left">
                                                    <div className="font-semibold">BizoSaaS Connect.zip</div>
                                                    <div className="text-xs text-muted-foreground">v1.0.0 • 15KB</div>
                                                </div>
                                            </Button>
                                        </div>

                                        <div className="space-y-2">
                                            <h3 className="font-bold text-sm">2. Install & Verify</h3>
                                            <div className="bg-muted p-3 rounded-lg text-xs space-y-2">
                                                <p>Upload to WP Admin {'>'} Plugins. Activate it.</p>
                                                <div onClick={() => { navigator.clipboard.writeText(apiKey); toast.success("Copied!"); }}
                                                    className="bg-background border p-2 rounded cursor-pointer font-mono text-center hover:bg-accent/50 transition">
                                                    API Key: {apiKey}
                                                </div>
                                            </div>
                                            <Button onClick={() => verifyPlugin(false)} disabled={isVerifying} className="w-full">
                                                {isVerifying ? <RefreshCw className="w-4 h-4 animate-spin mr-2" /> : <ShieldCheck className="w-4 h-4 mr-2" />}
                                                Verify Plugin Status
                                            </Button>
                                        </div>
                                    </CardContent>
                                </Card>
                            </TabsContent>

                            <TabsContent value="auto">
                                <Card className="shadow-md">
                                    <CardContent className="pt-6 space-y-4">
                                        <div className="space-y-3">
                                            <p className="text-xs text-muted-foreground">
                                                Connect using WordPress Application Passwords.
                                                Go to <b>Users {'>'} Profile {'>'} Application Passwords</b> to generate one.
                                            </p>
                                            <div className="space-y-1">
                                                <Label>WordPress Username</Label>
                                                <Input
                                                    placeholder="e.g. admin"
                                                    value={wpUser}
                                                    onChange={e => setWpUser(e.target.value)}
                                                />
                                            </div>
                                            <div className="space-y-1">
                                                <Label>Application Password</Label>
                                                <Input
                                                    type="password"
                                                    placeholder="xxxx xxxx xxxx xxxx"
                                                    value={wpAppPass}
                                                    onChange={e => setWpAppPass(e.target.value)}
                                                />
                                            </div>
                                            <Button onClick={handleAutoConnect} disabled={isConnecting} className="w-full mt-2">
                                                {isConnecting ? <RefreshCw className="w-4 h-4 animate-spin mr-2" /> : <ShieldCheck className="w-4 h-4 mr-2" />}
                                                Connect & Approve
                                            </Button>
                                        </div>
                                    </CardContent>
                                </Card>
                            </TabsContent>
                        </Tabs>
                    )}

                    {status !== 'connected' && (
                        <div className="text-center">
                            <Button variant="ghost" size="sm" onClick={onSkip} className="text-muted-foreground hover:text-foreground">
                                Skip this step for now
                            </Button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
