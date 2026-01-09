'use client';

import React, { useState } from 'react';
import AdminSettingsLayout from '@/components/settings/AdminSettingsLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
    Save,
    RotateCcw,
    ShieldCheck,
    Zap,
    Server,
    Globe,
    Lock,
    UserPlus,
    Wrench
} from 'lucide-react';
import { toast } from 'sonner';
import { PageHeader } from '@/components/dashboard/PageHeader';

export default function AdminSettingsPage() {
    const [platformName, setPlatformName] = useState('BizOSaaS Platform');
    const [maintenanceMode, setMaintenanceMode] = useState(false);
    const [registrationEnabled, setRegistrationEnabled] = useState(true);
    const [debugMode, setDebugMode] = useState(false);
    const [aiEnabled, setAiEnabled] = useState(true);

    const handleSave = () => {
        toast.success("Platform settings updated successfully!");
    };

    return (
        <AdminSettingsLayout>
            <div className="space-y-8 animate-in fade-in duration-500">
                <PageHeader
                    title={
                        <h1 className="text-3xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter">
                            Platform <span className="text-indigo-600">Settings</span>
                        </h1>
                    }
                    description="Global configuration and platform state management"
                >
                    <div className="flex items-center gap-2">
                        <Button variant="outline" size="sm" className="border-slate-200 dark:border-slate-800">
                            <RotateCcw className="w-4 h-4 mr-2" />
                            Reset Defaults
                        </Button>
                        <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700" onClick={handleSave}>
                            <Save className="w-4 h-4 mr-2" />
                            Save Changes
                        </Button>
                    </div>
                </PageHeader>

                <div className="grid grid-cols-1 gap-6">
                    {/* General Configuration */}
                    <Card className="border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden bg-white dark:bg-slate-900">
                        <CardHeader className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/50">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-indigo-100 dark:bg-indigo-900/30 rounded-xl">
                                    <Globe className="w-5 h-5 text-indigo-600" />
                                </div>
                                <div>
                                    <CardTitle className="text-lg font-black uppercase italic tracking-tighter">General Configuration</CardTitle>
                                    <CardDescription className="text-[10px] uppercase font-bold tracking-widest">Platform identity and public behavior</CardDescription>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="p-6 space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label htmlFor="platform-name" className="text-xs font-black uppercase tracking-wider text-slate-500">Platform Name</Label>
                                    <Input
                                        id="platform-name"
                                        value={platformName}
                                        onChange={(e) => setPlatformName(e.target.value)}
                                        className="h-11 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 font-bold"
                                    />
                                    <p className="text-[10px] text-slate-400 font-medium italic">This will appear in emails and browser tabs.</p>
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="support-email" className="text-xs font-black uppercase tracking-wider text-slate-500">Primary Support Email</Label>
                                    <Input
                                        id="support-email"
                                        defaultValue="support@bizosaas.com"
                                        className="h-11 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 font-bold"
                                    />
                                </div>
                            </div>

                            <div className="pt-4 space-y-4">
                                <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-100 dark:border-slate-800">
                                    <div className="space-y-0.5">
                                        <div className="flex items-center gap-2">
                                            <Label className="text-sm font-black uppercase italic tracking-tight">Maintenance Mode</Label>
                                            {maintenanceMode && <Badge className="bg-amber-500 text-white border-none text-[8px] animate-pulse">ACTIVE</Badge>}
                                        </div>
                                        <p className="text-xs text-slate-500 font-medium italic">Disable public access and show a construction page.</p>
                                    </div>
                                    <Switch checked={maintenanceMode} onCheckedChange={setMaintenanceMode} />
                                </div>

                                <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-100 dark:border-slate-800">
                                    <div className="space-y-0.5">
                                        <Label className="text-sm font-black uppercase italic tracking-tight">Public Registration</Label>
                                        <p className="text-xs text-slate-500 font-medium italic">Allow new tenants to sign up through the landing page.</p>
                                    </div>
                                    <Switch checked={registrationEnabled} onCheckedChange={setRegistrationEnabled} />
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Engine Controls */}
                    <Card className="border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden bg-white dark:bg-slate-900">
                        <CardHeader className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/50">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-amber-100 dark:bg-amber-900/30 rounded-xl">
                                    <Zap className="w-5 h-5 text-amber-600" />
                                </div>
                                <div>
                                    <CardTitle className="text-lg font-black uppercase italic tracking-tighter">Engine Controls</CardTitle>
                                    <CardDescription className="text-[10px] uppercase font-bold tracking-widest">Toggle core platform systems</CardDescription>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="p-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="flex items-center justify-between p-4 border border-slate-100 dark:border-slate-800 rounded-2xl">
                                    <div className="flex items-center gap-3">
                                        <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                                            <Server className="w-4 h-4 text-blue-600" />
                                        </div>
                                        <Label className="text-sm font-bold">Debug Mode</Label>
                                    </div>
                                    <Switch checked={debugMode} onCheckedChange={setDebugMode} />
                                </div>
                                <div className="flex items-center justify-between p-4 border border-slate-100 dark:border-slate-800 rounded-2xl">
                                    <div className="flex items-center gap-3">
                                        <div className="p-2 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg">
                                            <ShieldCheck className="w-4 h-4 text-emerald-600" />
                                        </div>
                                        <Label className="text-sm font-bold">AI Orchestrator</Label>
                                    </div>
                                    <Switch checked={aiEnabled} onCheckedChange={setAiEnabled} />
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Advanced Danger Zone */}
                    <Card className="border-red-200 bg-red-50/20 dark:bg-red-900/5 shadow-sm overflow-hidden border-dashed">
                        <CardHeader>
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-red-100 dark:bg-red-900/30 rounded-xl">
                                    <Wrench className="w-5 h-5 text-red-600" />
                                </div>
                                <div>
                                    <CardTitle className="text-lg font-black uppercase italic tracking-tighter text-red-600">Danger Zone</CardTitle>
                                    <CardDescription className="text-[10px] uppercase font-bold tracking-widest text-red-500/70">Irreversible platform actions</CardDescription>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="p-6">
                            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                                <div className="space-y-1">
                                    <h4 className="text-sm font-black uppercase italic tracking-tight text-red-900 dark:text-red-400">Flush Global Cache</h4>
                                    <p className="text-xs text-red-700/60 dark:text-red-400/50 font-medium italic">Immediately clear all Redis and CDN caches for all tenants.</p>
                                </div>
                                <Button variant="destructive" size="sm" className="font-black uppercase tracking-widest text-[10px]">Execute Flush</Button>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </AdminSettingsLayout>
    );
}
