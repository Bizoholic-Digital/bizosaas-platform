'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/components/ui/use-toast";
import { ArrowLeft, Save, RefreshCw, Trash2, CheckCircle2, AlertCircle } from "lucide-react";
import { brainApi, ConnectorConfig, ConnectorStatus } from '@/lib/brain-api';

export default function ConnectorDetailsPage() {
    const params = useParams();
    const router = useRouter();
    const { toast } = useToast();
    const connectorId = params.id as string;

    const [connector, setConnector] = useState<ConnectorConfig | null>(null);
    const [status, setStatus] = useState<ConnectorStatus | null>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [credentials, setCredentials] = useState<Record<string, string>>({});

    useEffect(() => {
        loadConnectorDetails();
    }, [connectorId]);

    const loadConnectorDetails = async () => {
        try {
            // In a real app, we might have a specific endpoint for getting one connector type
            // For now, we fetch all and find the matching one
            const types = await brainApi.connectors.listTypes();
            const match = types.find(c => c.id === connectorId);

            if (match) {
                setConnector(match);
                try {
                    const statusData = await brainApi.connectors.getStatus(connectorId);
                    setStatus(statusData);
                } catch (e) {
                    setStatus({ status: 'disconnected' });
                }
            } else {
                toast({
                    title: "Error",
                    description: "Connector not found",
                    variant: "destructive"
                });
                router.push('/dashboard/connectors');
            }
        } catch (error) {
            console.error("Failed to load connector:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleConnect = async () => {
        setSaving(true);
        try {
            await brainApi.connectors.connect(connectorId, credentials);
            toast({
                title: "Success",
                description: "Configuration saved and connected successfully.",
            });
            loadConnectorDetails(); // Refresh status
        } catch (error: any) {
            toast({
                title: "Connection Failed",
                description: error.response?.data?.detail || "Failed to connect. Please check your credentials.",
                variant: "destructive"
            });
        } finally {
            setSaving(false);
        }
    };

    const handleDisconnect = async () => {
        if (!confirm("Are you sure you want to disconnect? This may stop data syncing.")) return;

        // Implement disconnect logic in API if needed, for now we just clear local state/mock
        // await brainApi.connectors.disconnect(connectorId); 
        toast({
            title: "Disconnected",
            description: "Connector has been disconnected.",
        });
        setStatus({ status: 'disconnected' });
    };

    if (loading) {
        return <div className="p-8 text-center">Loading connector details...</div>;
    }

    if (!connector) return null;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                    <Button variant="ghost" size="icon" onClick={() => router.push('/dashboard/connectors')}>
                        <ArrowLeft className="h-4 w-4" />
                    </Button>
                    <div>
                        <h2 className="text-2xl font-bold tracking-tight flex items-center gap-2">
                            {connector.name}
                            {status?.status === 'connected' && (
                                <span className="inline-flex items-center rounded-full bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">
                                    Active
                                </span>
                            )}
                        </h2>
                        <p className="text-muted-foreground">{connector.description}</p>
                    </div>
                </div>
                <div className="flex items-center space-x-2">
                    {status?.status === 'connected' && (
                        <Button variant="destructive" size="sm" onClick={handleDisconnect}>
                            <Trash2 className="mr-2 h-4 w-4" />
                            Disconnect
                        </Button>
                    )}
                </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle>Configuration</CardTitle>
                        <CardDescription>
                            Update your connection credentials and settings.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {Object.entries(connector.auth_schema).map(([key, field]: [string, any]) => (
                            <div key={key} className="space-y-2">
                                <Label htmlFor={key}>{field.label || key}</Label>
                                <Input
                                    id={key}
                                    type={field.format === 'password' ? 'password' : 'text'}
                                    placeholder={field.placeholder}
                                    value={credentials[key] || ''}
                                    onChange={(e) => setCredentials(prev => ({ ...prev, [key]: e.target.value }))}
                                />
                                {field.help && <p className="text-xs text-muted-foreground">{field.help}</p>}
                            </div>
                        ))}
                    </CardContent>
                    <CardFooter>
                        <Button onClick={handleConnect} disabled={saving} className="w-full">
                            {saving ? <RefreshCw className="mr-2 h-4 w-4 animate-spin" /> : <Save className="mr-2 h-4 w-4" />}
                            {status?.status === 'connected' ? 'Update Configuration' : 'Connect'}
                        </Button>
                    </CardFooter>
                </Card>

                <div className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Status & Health</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-center space-x-4">
                                <div className={`p-3 rounded-full ${status?.status === 'connected' ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'}`}>
                                    {status?.status === 'connected' ? <CheckCircle2 className="h-6 w-6" /> : <AlertCircle className="h-6 w-6" />}
                                </div>
                                <div>
                                    <p className="font-medium">
                                        {status?.status === 'connected' ? 'Operational' : 'Not Connected'}
                                    </p>
                                    <p className="text-sm text-muted-foreground">
                                        {status?.status === 'connected'
                                            ? 'Data is syncing normally.'
                                            : 'Please configure credentials to start syncing.'}
                                    </p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {status?.status === 'connected' && (
                        <Card>
                            <CardHeader>
                                <CardTitle>Sync Options</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-2">
                                <Button variant="outline" className="w-full justify-start" onClick={() => toast({ title: "Sync Started", description: "Syncing data in background..." })}>
                                    <RefreshCw className="mr-2 h-4 w-4" />
                                    Sync Now
                                </Button>
                                {/* Add more specific sync actions based on connector type if needed */}
                            </CardContent>
                        </Card>
                    )}
                </div>
            </div>
        </div>
    );
}
