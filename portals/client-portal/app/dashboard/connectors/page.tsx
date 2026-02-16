'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Plug, CheckCircle2, Plus, Loader2, Settings } from "lucide-react"
import { brainApi, ConnectorConfig } from '@/lib/brain-api';
import { useToast } from "@/components/ui/use-toast"

export default function ConnectorsPage() {
    const router = useRouter();
    const [connectors, setConnectors] = useState<ConnectorConfig[]>([]);
    const [loading, setLoading] = useState(true);
    const [statuses, setStatuses] = useState<Record<string, string>>({});
    const { toast } = useToast();

    useEffect(() => {
        loadConnectors();
    }, []);

    const loadConnectors = async () => {
        try {
            const types = await brainApi.connectors.listTypes();
            setConnectors(types);

            // Check status for each
            const statusMap: Record<string, string> = {};
            for (const type of types) {
                try {
                    const status = await brainApi.connectors.getStatus(type.id);
                    statusMap[type.id] = status.status;
                } catch (e) {
                    statusMap[type.id] = 'disconnected';
                }
            }
            setStatuses(statusMap);
        } catch (error) {
            console.error("Failed to load connectors:", error);
            toast({
                title: "Error",
                description: "Failed to load available connectors. Is the Brain Gateway running?",
                variant: "destructive"
            });
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-96">
                <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Connectors</h2>
                    <p className="text-muted-foreground">
                        Manage your integrations with external platforms and services.
                    </p>
                </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {connectors.map((connector) => (
                    <Card key={connector.id} className="cursor-pointer hover:border-purple-500 transition-colors" onClick={() => router.push(`/dashboard/connectors/${connector.id}`)}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">
                                {connector.name}
                            </CardTitle>
                            <Badge variant={statuses[connector.id] === 'connected' ? 'default' : 'outline'}>
                                {statuses[connector.id] === 'connected' ? 'Active' : 'Inactive'}
                            </Badge>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-center space-x-4 py-4">
                                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-xl font-bold text-slate-900 dark:bg-slate-800 dark:text-slate-100">
                                    {/* Use first letter of name as icon fallback */}
                                    {connector.name[0]}
                                </div>
                                <div className="space-y-1">
                                    <p className="text-sm text-muted-foreground">
                                        {connector.type}
                                    </p>
                                </div>
                            </div>
                            <p className="text-sm text-muted-foreground mb-4 min-h-[40px]">
                                {connector.description}
                            </p>

                            <Button className="w-full" variant={statuses[connector.id] === 'connected' ? 'outline' : 'default'}>
                                {statuses[connector.id] === 'connected' ? (
                                    <>
                                        <Settings className="mr-2 h-4 w-4" />
                                        Configure
                                    </>
                                ) : (
                                    <>
                                        <Plug className="mr-2 h-4 w-4" />
                                        Connect
                                    </>
                                )}
                            </Button>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    )
}
