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
    Shield,
    Lock,
    Key,
    Fingerprint,
    UserCheck,
    AlertOctagon,
    Clock,
    History,
    Save,
    RotateCcw,
    Globe,
    ShieldCheck
} from 'lucide-react';
import { toast } from 'sonner';

export default function SecuritySettingsPage() {
    const [mfaRequired, setMfaRequired] = useState(true);
    const [passRotation, setPassRotation] = useState(90);
    const [sessionTimeout, setSessionTimeout] = useState(30);

    const handleSave = () => {
        toast.success("Security policy updated and pushed to global cluster!");
    };

    return (
        <AdminSettingsLayout>
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <h1 className="text-3xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter">
                            Security <span className="text-indigo-600">Policy</span>
                        </h1>
                        <p className="text-slate-500 font-medium flex items-center gap-2">
                            <Lock className="w-4 h-4 text-emerald-500" />
                            Global access control and encryption parameters
                        </p>
                    </div>
                    <div className="flex items-center gap-2">
                        <Button size="sm" className="bg-emerald-600 hover:bg-emerald-700" onClick={handleSave}>
                            <Save className="w-4 h-4 mr-2" />
                            Apply Policy
                        </Button>
                    </div>
                </div>

                <div className="grid grid-cols-1 gap-6">
                    {/* Authentication Protocol */}
                    <Card className="border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden bg-white dark:bg-slate-900">
                        <CardHeader className="border-b border-slate-100 dark:border-slate-800 pb-4">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-indigo-100 dark:bg-indigo-900/30 rounded-xl text-indigo-600">
                                    <Fingerprint className="w-5 h-5" />
                                </div>
                                <div>
                                    <CardTitle className="text-lg font-black uppercase italic tracking-tighter">Auth Protocols</CardTitle>
                                    <CardDescription className="text-[10px] uppercase font-bold tracking-widest text-slate-400">Multi-tenant authentication standards</CardDescription>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="p-6 space-y-6">
                            <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-100 dark:border-slate-800">
                                <div className="space-y-0.5">
                                    <div className="flex items-center gap-2">
                                        <Label className="text-sm font-black uppercase italic tracking-tight flex items-center gap-2 text-slate-900 dark:text-slate-200">
                                            Mandatory 2FA/MFA
                                            <Badge className="bg-emerald-500 text-white border-none text-[8px] italic">ENFORCED</Badge>
                                        </Label>
                                    </div>
                                    <p className="text-xs text-slate-500 font-medium italic">Require multi-factor authentication for all administrative accounts.</p>
                                </div>
                                <Switch checked={mfaRequired} onCheckedChange={setMfaRequired} />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2">
                                        <Clock className="w-3 h-3" />
                                        Session Timeout (min)
                                    </Label>
                                    <Input
                                        type="number"
                                        value={sessionTimeout}
                                        onChange={(e) => setSessionTimeout(parseInt(e.target.value))}
                                        className="h-11 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 font-bold"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2">
                                        <History className="w-3 h-3" />
                                        Password Rotation (days)
                                    </Label>
                                    <Input
                                        type="number"
                                        value={passRotation}
                                        onChange={(e) => setPassRotation(parseInt(e.target.value))}
                                        className="h-11 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 font-bold"
                                    />
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Access Control matrix */}
                    <Card className="border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden bg-white dark:bg-slate-900">
                        <CardHeader className="border-b border-slate-100 dark:border-slate-800 pb-4">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl text-emerald-600">
                                    <Shield className="w-5 h-5" />
                                </div>
                                <div>
                                    <CardTitle className="text-lg font-black uppercase italic tracking-tighter">Access Matrix</CardTitle>
                                    <CardDescription className="text-[10px] uppercase font-bold tracking-widest text-slate-400">Platform-wide permission defaults</CardDescription>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="p-4 space-y-4">
                            {[
                                { name: "Sudo Elevation", desc: "Allow admins to temporary elevate to SuperAdmin", icon: Key, active: true },
                                { name: "Geo-IP Fencing", desc: "Restrict admin access to specific regions", icon: Globe, active: false },
                                { name: "Audit Trail Logging", desc: "Log every single click and API call in the cluster", icon: ShieldCheck, active: true },
                            ].map((policy, idx) => (
                                <div key={idx} className="flex items-center justify-between p-4 border border-slate-100 dark:border-slate-800 rounded-2xl hover:bg-slate-50 dark:hover:bg-slate-800/20 transition-colors">
                                    <div className="flex items-center gap-4">
                                        <div className="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg">
                                            <policy.icon className="w-4 h-4 text-slate-500" />
                                        </div>
                                        <div className="space-y-0.5">
                                            <span className="text-xs font-black uppercase tracking-tight text-slate-900 dark:text-slate-200">{policy.name}</span>
                                            <p className="text-[10px] text-slate-500 italic font-medium">{policy.desc}</p>
                                        </div>
                                    </div>
                                    <Switch defaultChecked={policy.active} />
                                </div>
                            ))}
                        </CardContent>
                    </Card>

                    {/* Danger: Encryption Keys */}
                    <div className="p-6 bg-red-950 rounded-2xl border border-red-900/50 shadow-2xl overflow-hidden relative group">
                        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <AlertOctagon className="w-32 h-32 text-red-500" />
                        </div>
                        <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
                            <div className="space-y-2 text-center md:text-left">
                                <h3 className="text-lg font-black uppercase italic tracking-tighter text-red-400 flex items-center gap-2 justify-center md:justify-start">
                                    <AlertOctagon className="w-5 h-5 text-red-500 animate-pulse" />
                                    Global Encryption Keys
                                </h3>
                                <p className="text-xs font-medium text-red-300/70 italic max-w-md">
                                    Rotating global keys will force all current sessions to logout and may cause temporary service interruptions during re-encryption.
                                </p>
                            </div>
                            <Button variant="destructive" className="bg-red-600 hover:bg-red-700 font-black uppercase tracking-widest text-[10px] h-12 px-8">
                                PROCEED TO KEY ROTATION
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </AdminSettingsLayout>
    );
}
