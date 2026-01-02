'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Loader2, CheckCircle, AlertCircle, Lock, Monitor, Shield } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { ToolIntegration } from '../types/onboarding';

interface Props {
    data: ToolIntegration;
    onUpdate: (data: Partial<ToolIntegration>) => void;
}

interface CredentialState {
    [toolSlug: string]: {
        [key: string]: string;
    };
}

interface ConnectionStatus {
    [toolSlug: string]: 'idle' | 'connecting' | 'connected' | 'error';
}

export function DynamicCredentialsStep({ data, onUpdate }: Props) {
    const [credentials, setCredentials] = useState<CredentialState>({});
    const [status, setStatus] = useState<ConnectionStatus>({});
    const [tools, setTools] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const selectedSlugs = data.selectedMcps || [];

    useEffect(() => {
        const loadTools = async () => {
            try {
                // Fetch registry to get metadata (names, icons, auth schemas)
                const registry = await brainApi.mcp.getRegistry();
                const selectedTools = registry.filter(t => selectedSlugs.includes(t.slug));
                setTools(selectedTools);
            } catch (e) {
                console.error("Failed to load tool details", e);
            } finally {
                setLoading(false);
            }
        };
        if (selectedSlugs.length > 0) loadTools();
        else setLoading(false);
    }, [selectedSlugs]);

    const handleChange = (slug: string, field: string, value: string) => {
        setCredentials(prev => ({
            ...prev,
            [slug]: {
                ...prev[slug],
                [field]: value
            }
        }));
    };

    const handleConnect = async (tool: any) => {
        const creds = credentials[tool.slug];
        if (!creds) return;

        setStatus(prev => ({ ...prev, [tool.slug]: 'connecting' }));

        try {
            // Call the connection API
            // Note: connectorId might need mapping from slug. Assuming slug === connectorId for now.
            await brainApi.connectors.connect(tool.slug, creds);

            setStatus(prev => ({ ...prev, [tool.slug]: 'connected' }));

            // Allow parent to know (optional)
            // onUpdate({}); 
        } catch (e) {
            console.error(`Failed to connect ${tool.name}`, e);
            setStatus(prev => ({ ...prev, [tool.slug]: 'error' }));
        }
    };

    const renderFormFields = (tool: any) => {
        // MVP: Specific forms for top tools, generic for others
        // In full version, parse tool.auth_schema

        switch (tool.slug) {
            case 'wordpress':
            case 'woocommerce':
                return (
                    <div className="space-y-4">
                        <div className="space-y-2">
                            <Label>Website URL</Label>
                            <Input
                                placeholder="https://your-site.com"
                                value={credentials[tool.slug]?.url || ''}
                                onChange={e => handleChange(tool.slug, 'url', e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label>Username / Email</Label>
                            <Input
                                placeholder="admin@your-site.com"
                                value={credentials[tool.slug]?.username || ''}
                                onChange={e => handleChange(tool.slug, 'username', e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label>Application Password / Key</Label>
                            <Input
                                type="password"
                                placeholder="xxxx-xxxx-xxxx-xxxx"
                                value={credentials[tool.slug]?.password || ''}
                                onChange={e => handleChange(tool.slug, 'password', e.target.value)}
                            />
                            <p className="text-xs text-muted-foreground">Generated in WP Admin Users Profile</p>
                        </div>
                    </div>
                );
            case 'hubspot':
            case 'zoho-crm':
            case 'google-ads':
            case 'facebook-ads':
            case 'google-analytics':
            case 'google-business-profile':
                return (
                    <div className="flex flex-col items-center justify-center p-6 space-y-4">
                        <p className="text-sm text-center text-muted-foreground">This integration supports One-Click OAuth.</p>
                        <Button
                            className="w-full bg-[#fa7820] hover:bg-[#e66a15] text-white" // Generic orange for OAuth
                            onClick={() => handleConnect(tool)}
                            disabled={status[tool.slug] === 'connecting' || status[tool.slug] === 'connected'}
                        >
                            {status[tool.slug] === 'connecting' ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Lock className="w-4 h-4 mr-2" />}
                            Connect with {tool.name}
                        </Button>
                    </div>
                );
            default:
                return (
                    <div className="space-y-4">
                        <div className="space-y-2">
                            <Label>API Key</Label>
                            <Input
                                type="password"
                                placeholder={`Enter ${tool.name} API Key`}
                                value={credentials[tool.slug]?.api_key || ''}
                                onChange={e => handleChange(tool.slug, 'api_key', e.target.value)}
                            />
                        </div>
                    </div>
                );
        }
    };

    if (loading) return <div className="flex justify-center p-12"><Loader2 className="animate-spin text-blue-600" /></div>;

    if (selectedSlugs.length === 0) {
        return (
            <div className="text-center p-12 space-y-4">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto">
                    <Monitor className="text-gray-400 w-8 h-8" />
                </div>
                <h3 className="text-xl font-semibold">No Tools Selected</h3>
                <p className="text-gray-500">Go back to the previous step to select tools to connect.</p>
            </div>
        );
    }

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Connect Your Tools</h2>
                <p className="text-gray-500">Authorize BizOSaaS to securely access your platforms.</p>
            </div>

            <div className="grid gap-6">
                {tools.map(tool => {
                    const isConnected = status[tool.slug] === 'connected';
                    const isError = status[tool.slug] === 'error';

                    return (
                        <Card key={tool.slug} className={`border transition-all ${isConnected ? 'border-green-500 bg-green-50/20' : 'border-gray-200 hover:border-blue-300'}`}>
                            <CardContent className="p-6">
                                <div className="flex items-start justify-between mb-6">
                                    <div className="flex items-center gap-3">
                                        {/* Icon would go here if available in tool data */}
                                        <div className="h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center font-bold text-blue-600">
                                            {tool.name[0]}
                                        </div>
                                        <div>
                                            <h3 className="font-semibold text-lg">{tool.name}</h3>
                                            <p className="text-xs text-muted-foreground">{tool.description}</p>
                                        </div>
                                    </div>
                                    {isConnected && (
                                        <div className="flex items-center text-green-600 bg-green-100 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
                                            <CheckCircle className="w-3 h-3 mr-1.5" />
                                            Connected
                                        </div>
                                    )}
                                </div>

                                {!isConnected && (
                                    <div className="bg-gray-50 p-6 rounded-xl border border-gray-100">
                                        {renderFormFields(tool)}

                                        {!(tool.slug === 'hubspot' || tool.slug.includes('ads') || tool.slug.includes('analytics') || tool.slug.includes('business-profile')) && (
                                            <div className="mt-4 flex justify-end">
                                                <Button
                                                    onClick={() => handleConnect(tool)}
                                                    disabled={status[tool.slug] === 'connecting'}
                                                >
                                                    {status[tool.slug] === 'connecting' && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                                                    Connect {tool.name}
                                                </Button>
                                            </div>
                                        )}
                                        {isError && (
                                            <div className="mt-4 text-sm text-red-600 flex items-center bg-red-50 p-3 rounded-lg border border-red-100">
                                                <AlertCircle className="w-4 h-4 mr-2" />
                                                Failed to connect. Please check credentials.
                                            </div>
                                        )}
                                    </div>
                                )}

                                <div className="mt-4 flex items-center gap-2 text-xs text-gray-400">
                                    <Shield className="w-3 h-3" />
                                    <span>Credentials are encrypted and stored securely.</span>
                                </div>
                            </CardContent>
                        </Card>
                    );
                })}
            </div>
        </div>
    );
}
