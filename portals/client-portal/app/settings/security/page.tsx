'use client';

import React from 'react';
import SettingsLayout from '@/components/settings/SettingsLayout';
import { Button } from '@/components/ui/button';
import { Shield, Lock, Smartphone, ExternalLink } from 'lucide-react';

export default function SecuritySettingsPage() {
    const openSecurityPortal = () => {
        window.open('https://auth-sso.bizoholic.net/if/user/#/settings', '_blank');
    };

    return (
        <SettingsLayout
            title="Security Settings"
            description="Manage your password and account security"
        >
            <div className="p-6 space-y-8">
                <div className="bg-slate-50 dark:bg-slate-900/50 p-6 rounded-lg border border-slate-200 dark:border-slate-800">
                    <div className="flex items-start gap-4">
                        <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full text-blue-600 dark:text-blue-400">
                            <Shield className="w-6 h-6" />
                        </div>
                        <div className="space-y-4 flex-1">
                            <div>
                                <h3 className="text-lg font-medium">Account Security</h3>
                                <p className="text-muted-foreground mt-1">
                                    Your account security is managed by our secure identity provider (Authentik).
                                    You can update your password, enable Two-Factor Authentication (2FA), and manage active sessions from the SSO portal.
                                </p>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                                <Button
                                    variant="outline"
                                    className="h-auto py-4 px-6 justify-start space-x-4 bg-white dark:bg-slate-950"
                                    onClick={openSecurityPortal}
                                >
                                    <div className="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg">
                                        <Lock className="w-5 h-5 text-gray-500" />
                                    </div>
                                    <div className="text-left">
                                        <div className="font-medium">Change Password</div>
                                        <div className="text-xs text-muted-foreground">Update in SSO Portal</div>
                                    </div>
                                </Button>

                                <Button
                                    variant="outline"
                                    className="h-auto py-4 px-6 justify-start space-x-4 bg-white dark:bg-slate-950"
                                    onClick={openSecurityPortal}
                                >
                                    <div className="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg">
                                        <Smartphone className="w-5 h-5 text-gray-500" />
                                    </div>
                                    <div className="text-left">
                                        <div className="font-medium">Two-Factor Auth</div>
                                        <div className="text-xs text-muted-foreground">Manage 2FA in SSO Portal</div>
                                    </div>
                                </Button>
                            </div>

                            <div className="mt-6 pt-6 border-t border-slate-200 dark:border-slate-700">
                                <Button onClick={openSecurityPortal} className="gap-2">
                                    Open Security Center <ExternalLink className="w-4 h-4" />
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </SettingsLayout>
    );
}
