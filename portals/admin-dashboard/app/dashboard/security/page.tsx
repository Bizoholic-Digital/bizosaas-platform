'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { adminApi, AuditLog } from '@/lib/api/admin';
import {
    RefreshCw,
    Shield,
    ShieldAlert,
    ShieldCheck,
    Lock,
    Key,
    Server,
    Fingerprint,
    Search,
    Clock,
    User,
    AlertTriangle,
    Eye,
    Globe
} from 'lucide-react';
import { toast } from 'sonner';
import { format } from 'date-fns';

export default function SecurityDashboard() {
    const [loading, setLoading] = useState(true);
    const [posture, setPosture] = useState<any>(null);
    const [vulnerabilities, setVulnerabilities] = useState<any[]>([]);
    const [compliance, setCompliance] = useState<any>(null);
    const [encryptionKeys, setEncryptionKeys] = useState<any[]>([]);
    const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
    const [searchTerm, setSearchTerm] = useState('');

    const loadData = async () => {
        setLoading(true);
        try {
            const [postureRes, vulnRes, compRes, keysRes, logsRes] = await Promise.all([
                adminApi.getSecurityPosture(),
                adminApi.getVulnerabilities(),
                adminApi.getComplianceChecklist(),
                adminApi.getEncryptionKeys(),
                adminApi.getAuditLogs()
            ]);

            if (postureRes.data) setPosture(postureRes.data);
            if (vulnRes.data) setVulnerabilities(vulnRes.data);
            if (compRes.data) setCompliance(compRes.data);
            if (keysRes.data) setEncryptionKeys(keysRes.data);
            if (logsRes.data) setAuditLogs(logsRes.data);

        } catch (error) {
            toast.error("Failed to load security metrics");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const filteredLogs = auditLogs.filter(log =>
        (log.action?.toLowerCase() || '').includes(searchTerm.toLowerCase()) ||
        (log.user?.email?.toLowerCase() || 'system').includes(searchTerm.toLowerCase())
    );

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Security Command Center</h1>
                    <p className="text-muted-foreground">Monitor platform security posture, compliance, and audit logs.</p>
                </div>
                <Button onClick={loadData} variant="outline" disabled={loading}>
                    <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Sync Security Data
                </Button>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="bg-slate-900 text-white border-none">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <Shield className="h-8 w-8 text-emerald-400" />
                            <Badge className="bg-emerald-500/20 text-emerald-400 border-emerald-500/30">Healthy</Badge>
                        </div>
                        <div className="mt-4">
                            <h3 className="text-3xl font-bold">{posture?.overall_score || '--'}/100</h3>
                            <p className="text-slate-400 text-sm">Overall Security Score</p>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <Fingerprint className="h-8 w-8 text-indigo-500" />
                            <Badge variant="secondary">{posture?.mfa_adoption || '0'}%</Badge>
                        </div>
                        <div className="mt-4">
                            <h3 className="text-3xl font-bold">MFA Active</h3>
                            <p className="text-muted-foreground text-sm">User Identity Protection</p>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <ShieldAlert className="h-8 w-8 text-rose-500" />
                            <Badge variant="destructive">{posture?.active_alerts || '0'} Active</Badge>
                        </div>
                        <div className="mt-4">
                            <h3 className="text-3xl font-bold">Threats</h3>
                            <p className="text-muted-foreground text-sm">Security Alerts Detected</p>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <Lock className="h-8 w-8 text-amber-500" />
                            <Badge variant="outline">Vault Protected</Badge>
                        </div>
                        <div className="mt-4">
                            <h3 className="text-3xl font-bold">{encryptionKeys.length} Keys</h3>
                            <p className="text-muted-foreground text-sm">Encryption Key Management</p>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <Tabs defaultValue="overview" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="overview">Postures & Compliance</TabsTrigger>
                    <TabsTrigger value="vulnerabilities">Vulnerability Scan</TabsTrigger>
                    <TabsTrigger value="audit">Audit Logs</TabsTrigger>
                    <TabsTrigger value="network">Network Security</TabsTrigger>
                </TabsList>

                <TabsContent value="overview" className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Card>
                            <CardHeader>
                                <CardTitle className="text-lg">Compliance Status</CardTitle>
                                <CardDescription>Tracking platform global compliance standards.</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                {compliance && Object.entries(compliance).map(([key, val]: [string, any]) => (
                                    <div key={key} className="flex items-center justify-between p-3 border rounded-lg">
                                        <div className="flex items-center gap-3">
                                            <ShieldCheck className={val.status === 'compliant' ? 'text-emerald-500' : 'text-amber-500'} />
                                            <div>
                                                <p className="font-semibold">{key}</p>
                                                <p className="text-xs text-muted-foreground">
                                                    {val.status === 'compliant' ? `Last Audit: ${val.last_audit}` : `${val.completion}% Completed`}
                                                </p>
                                            </div>
                                        </div>
                                        <Badge variant={val.status === 'compliant' ? 'default' : 'secondary'}
                                            className={val.status === 'compliant' ? 'bg-emerald-600' : ''}>
                                            {val.status.replace('_', ' ')}
                                        </Badge>
                                    </div>
                                ))}
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle className="text-lg">Encryption Keys (Vault)</CardTitle>
                                <CardDescription>Status and rotation history of system secrets.</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-3">
                                    {encryptionKeys.map((key) => (
                                        <div key={key.name} className="flex items-center justify-between p-3 border rounded-lg bg-slate-50 dark:bg-slate-900/50">
                                            <div className="flex items-center gap-3">
                                                <Key className="h-4 w-4 text-amber-500" />
                                                <div>
                                                    <p className="text-sm font-medium">{key.name}</p>
                                                    <p className="text-[10px] text-muted-foreground uppercase">{key.type} • Last rotated: {key.last_rotated}</p>
                                                </div>
                                            </div>
                                            <Button variant="ghost" size="sm">Rotate</Button>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </TabsContent>

                <TabsContent value="vulnerabilities">
                    <Card>
                        <CardHeader>
                            <CardTitle>Platform Vulnerability Scan</CardTitle>
                            <CardDescription>Automated container and dependencies security scan results.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="relative w-full overflow-auto">
                                <table className="w-full text-sm">
                                    <thead>
                                        <tr className="border-b text-left">
                                            <th className="h-10 px-4 font-medium">CVE ID</th>
                                            <th className="h-10 px-4 font-medium">Service</th>
                                            <th className="h-10 px-4 font-medium">Severity</th>
                                            <th className="h-10 px-4 font-medium">Status</th>
                                            <th className="h-10 px-4 font-medium">Description</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {vulnerabilities.map((v) => (
                                            <tr key={v.id} className="border-b hover:bg-muted/50 transition-colors">
                                                <td className="p-4 font-mono font-bold text-indigo-600">{v.id}</td>
                                                <td className="p-4">{v.service}</td>
                                                <td className="p-4">
                                                    <Badge variant={v.severity === 'high' ? 'destructive' : 'secondary'} className={v.severity === 'medium' ? 'bg-amber-500 text-white' : ''}>
                                                        {v.severity}
                                                    </Badge>
                                                </td>
                                                <td className="p-4 uppercase text-[10px] font-bold">{v.status}</td>
                                                <td className="p-4 text-muted-foreground">{v.description}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="audit" className="space-y-4">
                    <div className="flex items-center space-x-2">
                        <div className="relative flex-1">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <input
                                type="search"
                                placeholder="Search logs by action or user..."
                                className="w-full bg-background pl-8 h-10 rounded-md border border-input px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>

                    <Card>
                        <CardHeader>
                            <CardTitle>Security Audit Logs</CardTitle>
                            <CardDescription>Immutable record of all security-sensitive actions.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="relative w-full overflow-auto">
                                <table className="w-full text-sm">
                                    <thead>
                                        <tr className="border-b text-left">
                                            <th className="h-10 px-4 font-medium">Timestamp</th>
                                            <th className="h-10 px-4 font-medium">User</th>
                                            <th className="h-10 px-4 font-medium">Action</th>
                                            <th className="h-10 px-4 font-medium">Details</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {filteredLogs.map((log) => (
                                            <tr key={log.id} className="border-b hover:bg-muted/50 transition-colors">
                                                <td className="p-4 whitespace-nowrap text-muted-foreground flex items-center gap-1">
                                                    <Clock className="h-3 w-3" />
                                                    {format(new Date(log.created_at), 'MMM d, HH:mm:ss')}
                                                </td>
                                                <td className="p-4 font-medium underline underline-offset-4 decoration-muted-foreground/30">
                                                    {log.user?.email || 'System'}
                                                </td>
                                                <td className="p-4">
                                                    <Badge variant="outline">{log.action}</Badge>
                                                </td>
                                                <td className="p-4 font-mono text-[10px] opacity-70">
                                                    {JSON.stringify(log.details)}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="network">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Card>
                            <CardHeader>
                                <CardTitle className="text-lg">IP Whitelisting</CardTitle>
                                <CardDescription>Restrict access to the Admin Panel by IP address.</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-bold uppercase text-muted-foreground">Add New IP Range</label>
                                    <div className="flex gap-2">
                                        <input className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm" placeholder="e.g. 192.168.1.1/32" />
                                        <Button>Whitelist</Button>
                                    </div>
                                </div>

                                <div className="space-y-2 mt-4">
                                    <p className="text-xs font-bold uppercase text-muted-foreground">Currently Whitelisted</p>
                                    <div className="p-3 border rounded-lg flex items-center justify-between">
                                        <div className="flex items-center gap-2">
                                            <Globe className="h-4 w-4 text-indigo-500" />
                                            <span>203.0.113.12 (Headquarters)</span>
                                        </div>
                                        <Button variant="ghost" size="sm" className="text-rose-500">Remove</Button>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle className="text-lg">Active Sessions</CardTitle>
                                <CardDescription>Currently active administrative sessions platform-wide.</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-4">
                                    <div className="text-center py-8">
                                        <Eye className="h-12 w-12 text-muted-foreground/30 mx-auto" />
                                        <p className="mt-2 text-muted-foreground">Use the &quot;Users&quot; panel to manage global active sessions.</p>
                                        <Button variant="outline" className="mt-4" onClick={() => window.location.href = '/dashboard/users'}>Go to Users</Button>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
}
