'use client';

import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Plus, Trash2, Key, Globe, Zap, Copy, Check } from "lucide-react";

interface IntegrationsContentProps {
    activeTab: string;
}

export const IntegrationsContent: React.FC<IntegrationsContentProps> = ({ activeTab }) => {

    // Webhooks State
    const [webhooks, setWebhooks] = useState([
        { id: 'wh_1', url: 'https://api.mysite.com/hook', events: ['order.created'], status: 'active', last_triggered: '2 mins ago' },
        { id: 'wh_2', url: 'https://crm.external.com/leads', events: ['lead.new'], status: 'failed', last_triggered: '1 hour ago' }
    ]);

    // API Keys State
    const [apiKeys, setApiKeys] = useState([
        { id: 'key_1', name: 'Mobile App', prefix: 'pk_live_...', created: '2023-11-01', last_all: 'Today' },
        { id: 'key_2', name: 'Dev Test', prefix: 'sk_test_...', created: '2023-12-05', last_all: 'Never' }
    ]);
    const [showKey, setShowKey] = useState<string | null>(null);

    // Automation Rules State
    const [rules, setRules] = useState([
        { id: 'rule_1', name: 'Sync High Value Leads', trigger: 'Lead Score > 80', action: 'Sync to Zoho', active: true },
        { id: 'rule_2', name: 'Auto-Tweet Blog Posts', trigger: 'Post Published', action: 'Create Social Post', active: false }
    ]);

    const renderWebhooks = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h3 className="text-lg font-medium">Webhooks</h3>
                    <p className="text-sm text-muted-foreground">Notify external systems when events happen in BizOSaaS.</p>
                </div>
                <Button><Plus className="mr-2 h-4 w-4" /> Add Webhook</Button>
            </div>
            <Card>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Endpoint URL</TableHead>
                            <TableHead>Events</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Last Triggered</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {webhooks.map((wh) => (
                            <TableRow key={wh.id}>
                                <TableCell className="font-medium truncate max-w-[200px]">{wh.url}</TableCell>
                                <TableCell>
                                    <div className="flex gap-1">
                                        {wh.events.map(e => <Badge key={e} variant="secondary" className="text-xs">{e}</Badge>)}
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <Badge variant={wh.status === 'active' ? 'default' : 'destructive'}>{wh.status}</Badge>
                                </TableCell>
                                <TableCell>{wh.last_triggered}</TableCell>
                                <TableCell className="text-right">
                                    <Button variant="ghost" size="sm"><Trash2 className="h-4 w-4 text-red-500" /></Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Card>
        </div>
    );

    const renderApiKeys = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h3 className="text-lg font-medium">API Keys</h3>
                    <p className="text-sm text-muted-foreground">Manage keys for accessing the Brain API externally.</p>
                </div>
                <Button><Plus className="mr-2 h-4 w-4" /> Generate New Key</Button>
            </div>
            <Card>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Name</TableHead>
                            <TableHead>Token Prefix</TableHead>
                            <TableHead>Created</TableHead>
                            <TableHead>Last Used</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {apiKeys.map((key) => (
                            <TableRow key={key.id}>
                                <TableCell className="font-medium">{key.name}</TableCell>
                                <TableCell><code className="bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded">{key.prefix}</code></TableCell>
                                <TableCell>{key.created}</TableCell>
                                <TableCell>{key.last_all}</TableCell>
                                <TableCell className="text-right">
                                    <Button variant="ghost" size="sm"><Trash2 className="h-4 w-4 text-red-500" /></Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Card>
        </div>
    );

    const renderAutomation = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h3 className="text-lg font-medium">Automation Rules</h3>
                    <p className="text-sm text-muted-foreground">Define logic for automatic data flow between connectors.</p>
                </div>
                <Button><Plus className="mr-2 h-4 w-4" /> Create Rule</Button>
            </div>
            <div className="grid gap-4">
                {rules.map(rule => (
                    <Card key={rule.id}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <div className="flex flex-col">
                                <CardTitle className="text-base font-medium">{rule.name}</CardTitle>
                                <CardDescription className="flex items-center gap-2 mt-1">
                                    <Badge variant="outline">{rule.trigger}</Badge>
                                    <span>→</span>
                                    <Badge variant="outline">{rule.action}</Badge>
                                </CardDescription>
                            </div>
                            <div className="flex items-center gap-2">
                                <Badge variant={rule.active ? "default" : "secondary"}>{rule.active ? "Active" : "Paused"}</Badge>
                                <Button variant="ghost" size="sm">Edit</Button>
                            </div>
                        </CardHeader>
                    </Card>
                ))}
            </div>
        </div>
    );

    // Filter based on activeTab sub-route
    if (activeTab === 'integrations-webhooks') return renderWebhooks();
    if (activeTab === 'integrations-api-keys') return renderApiKeys();
    if (activeTab === 'integrations-automation') return renderAutomation();

    // Default Overview
    return (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <Card className="cursor-pointer hover:border-purple-500 transition-colors">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2"><Globe className="h-5 w-5" /> Webhooks</CardTitle>
                    <CardDescription>2 Active Listeners</CardDescription>
                </CardHeader>
                <CardContent>Send real-time data to external URLs based on platform events.</CardContent>
            </Card>
            <Card className="cursor-pointer hover:border-purple-500 transition-colors">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2"><Key className="h-5 w-5" /> API Keys</CardTitle>
                    <CardDescription>2 Keys Generated</CardDescription>
                </CardHeader>
                <CardContent>Manage secure access tokens for third-party integrations.</CardContent>
            </Card>
            <Card className="cursor-pointer hover:border-purple-500 transition-colors">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2"><Zap className="h-5 w-5" /> Automation</CardTitle>
                    <CardDescription>1 Active Rule</CardDescription>
                </CardHeader>
                <CardContent>Connect your tools with "If This Then That" style logic.</CardContent>
            </Card>
        </div>
    );
};
