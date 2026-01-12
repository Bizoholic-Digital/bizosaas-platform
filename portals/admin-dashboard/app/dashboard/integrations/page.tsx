'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Globe, Shield, Zap, Info, MoreHorizontal, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useSetHeader } from '@/lib/contexts/HeaderContext';

export default function IntegrationsPage() {
    useSetHeader("MCP Registry & Integrations", "Centrally manage and monitor the Model Context Protocol ecosystem.");

    const [mcps, setMcps] = useState([
        { id: 1, name: 'FluentCRM', slug: 'fluentcrm', status: 'active', type: 'Official', category: 'CRM', version: '1.2.0' },
        { id: 2, name: 'Brave Search', slug: 'brave-search', status: 'active', type: 'Official', category: 'Search', version: '1.0.0' },
        { id: 3, name: 'Google Drive', slug: 'google-drive', status: 'active', type: 'Official', category: 'Productivity', version: '1.1.0' },
        { id: 4, name: 'Filesystem', slug: 'filesystem', status: 'active', type: 'Official', category: 'Utilities', version: '1.0.0' },
        { id: 5, name: 'GitHub', slug: 'github', status: 'active', type: 'Official', category: 'DevTools', version: '1.0.0' },
        { id: 6, name: 'Slack', slug: 'slack', status: 'maintenance', type: 'Official', category: 'Communication', version: '1.0.0' },
        { id: 7, name: 'WooCommerce', slug: 'woocommerce', status: 'deprecated', type: 'Community', category: 'Ecommerce', version: '0.8.0' },
    ]);

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center bg-blue-50 dark:bg-blue-900/10 p-4 rounded-xl border border-blue-100 dark:border-blue-900/20">
                <div className="flex gap-4 items-center">
                    <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center text-white shadow-lg">
                        <Shield className="w-6 h-6" />
                    </div>
                    <div>
                        <h4 className="font-bold text-sm">Security Policy Active</h4>
                        <p className="text-xs text-muted-foreground">All MCP servers are currently isolated in sandboxed containers with restricted volume access.</p>
                    </div>
                </div>
                <Button size="sm" variant="outline">View Policy</Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mcps.map((mcp) => (
                    <Card key={mcp.id} className="group hover:border-blue-500 transition-all">
                        <CardHeader className="pb-2">
                            <div className="flex justify-between items-start">
                                <div className="space-y-1">
                                    <div className="flex items-center gap-2">
                                        <CardTitle className="text-lg">{mcp.name}</CardTitle>
                                        <Badge variant="secondary" className="text-[9px] uppercase font-bold">{mcp.category}</Badge>
                                    </div>
                                    <CardDescription className="text-xs font-mono">mcp://{mcp.slug}</CardDescription>
                                </div>
                                <div className={`p-1.5 rounded-full ${mcp.status === 'active' ? 'bg-emerald-100 text-emerald-600' :
                                        mcp.status === 'maintenance' ? 'bg-amber-100 text-amber-600' :
                                            'bg-red-100 text-red-600'
                                    }`}>
                                    {mcp.status === 'active' ? <CheckCircle className="w-4 h-4" /> :
                                        mcp.status === 'maintenance' ? <Loader2 className="w-4 h-4 animate-spin" /> :
                                            <XCircle className="w-4 h-4" />}
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-center justify-between text-xs mb-4">
                                <span className="text-muted-foreground font-medium">Type: <span className="text-slate-900 dark:text-slate-100">{mcp.type}</span></span>
                                <span className="text-muted-foreground font-medium">v{mcp.version}</span>
                            </div>
                            <div className="flex gap-2">
                                <Button size="sm" variant="secondary" className="flex-1 text-xs">Configure</Button>
                                <Button size="sm" variant="outline" className="flex-1 text-xs">Monitor</Button>
                                <Button size="sm" variant="ghost" size="icon"><MoreHorizontal className="w-4 h-4" /></Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <Card className="border-dashed border-2 bg-slate-50/50 dark:bg-slate-900/50">
                <CardContent className="h-48 flex flex-col items-center justify-center p-6 text-center">
                    <Zap className="w-10 h-10 text-slate-300 mb-4" />
                    <h3 className="font-bold text-lg">Add Custom MCP Server</h3>
                    <p className="text-sm text-muted-foreground max-w-sm mx-auto mb-6">Deploy your own MCP server using Docker or SSE to extend the platform's intelligence.</p>
                    <Button className="font-bold">Register New Server</Button>
                </CardContent>
            </Card>
        </div>
    );
}
