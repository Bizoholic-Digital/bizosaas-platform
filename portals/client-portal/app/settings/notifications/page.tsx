'use client';

import React from 'react';
import SettingsLayout from '@/components/settings/SettingsLayout';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';

export default function NotificationsSettingsPage() {
    return (
        <SettingsLayout
            title="Notification Settings"
            description="Control how and when you receive alerts"
        >
            <div className="p-6 space-y-8">
                <div className="space-y-6">
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <Label className="text-base">Email Notifications</Label>
                            <p className="text-sm text-muted-foreground">Receive daily summaries and critical alerts via email.</p>
                        </div>
                        <Switch defaultChecked />
                    </div>
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <Label className="text-base">Push Notifications</Label>
                            <p className="text-sm text-muted-foreground">Get real-time updates on your desktop or mobile device.</p>
                        </div>
                        <Switch defaultChecked />
                    </div>
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <Label className="text-base">AI Insight Alerts</Label>
                            <p className="text-sm text-muted-foreground">Notify me when the AI has new recommendations.</p>
                        </div>
                        <Switch defaultChecked />
                    </div>
                </div>

                <div className="pt-6 border-t border-slate-100 dark:border-slate-700 flex justify-end">
                    <Button>Save Preferences</Button>
                </div>
            </div>
        </SettingsLayout>
    );
}
