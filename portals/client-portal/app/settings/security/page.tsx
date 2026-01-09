'use client';

import React from 'react';
import SettingsLayout from '@/components/settings/SettingsLayout';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Shield, Lock, Smartphone } from 'lucide-react';

export default function SecuritySettingsPage() {
    return (
        <SettingsLayout
            title="Security Settings"
            description="Manage your password and account security"
        >
            <div className="p-6 space-y-8">
                <div className="space-y-4">
                    <h3 className="text-lg font-medium flex items-center gap-2">
                        <Lock className="w-5 h-5 text-gray-500" />
                        Change Password
                    </h3>
                    <div className="grid grid-cols-1 gap-4 max-w-md">
                        <div className="space-y-2">
                            <Label>Current Password</Label>
                            <Input type="password" />
                        </div>
                        <div className="space-y-2">
                            <Label>New Password</Label>
                            <Input type="password" />
                        </div>
                        <div className="space-y-2">
                            <Label>Confirm New Password</Label>
                            <Input type="password" />
                        </div>
                        <Button className="w-fit">Update Password</Button>
                    </div>
                </div>

                <div className="pt-8 border-t border-slate-100 dark:border-slate-700 space-y-4">
                    <h3 className="text-lg font-medium flex items-center gap-2">
                        <Smartphone className="w-5 h-5 text-gray-500" />
                        Two-Factor Authentication
                    </h3>
                    <p className="text-sm text-muted-foreground">Add an extra layer of security to your account.</p>
                    <Button variant="outline">Enable 2FA</Button>
                </div>
            </div>
        </SettingsLayout>
    );
}
