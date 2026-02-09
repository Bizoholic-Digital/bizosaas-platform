'use client';

import React from 'react';
import SettingsLayout from '@/components/settings/SettingsLayout';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Sun, Moon, Monitor } from 'lucide-react';

export default function AppearanceSettingsPage() {
    return (
        <SettingsLayout
            title="Appearance Settings"
            description="Customize how the platform looks and feels"
        >
            <div className="p-6 space-y-8">
                <div className="space-y-4">
                    <Label className="text-base">System Theme</Label>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <button className="flex flex-col items-center gap-3 p-4 rounded-xl border-2 border-blue-600 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300">
                            <Sun className="w-8 h-8" />
                            <span className="font-medium">Light</span>
                        </button>
                        <button className="flex flex-col items-center gap-3 p-4 rounded-xl border-2 border-transparent hover:border-slate-200 dark:hover:border-slate-700 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300">
                            <Moon className="w-8 h-8" />
                            <span className="font-medium">Dark</span>
                        </button>
                        <button className="flex flex-col items-center gap-3 p-4 rounded-xl border-2 border-transparent hover:border-slate-200 dark:hover:border-slate-700 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300">
                            <Monitor className="w-8 h-8" />
                            <span className="font-medium">System</span>
                        </button>
                    </div>
                </div>

                <div className="pt-6 border-t border-slate-100 dark:border-slate-700 flex justify-end">
                    <Button>Apply Theme</Button>
                </div>
            </div>
        </SettingsLayout>
    );
}
