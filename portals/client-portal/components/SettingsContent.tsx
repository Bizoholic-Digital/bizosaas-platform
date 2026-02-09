'use client';

import React, { useState, useEffect } from 'react';
import { User, Lock, Bell, Users, Globe, Save } from 'lucide-react';

interface SettingsContentProps {
    activeTab: string;
}

export const SettingsContent: React.FC<SettingsContentProps> = ({ activeTab }) => {
    const [currentTab, setCurrentTab] = useState('general');
    const [settings, setSettings] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);

    useEffect(() => {
        const fetchSettings = async () => {
            try {
                const response = await fetch('/api/brain/settings');
                if (response.ok) {
                    const data = await response.json();
                    setSettings(data);
                }
            } catch (error) {
                console.error('Failed to fetch settings:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchSettings();
    }, []);

    const handleSave = async () => {
        setIsSaving(true);
        try {
            await fetch('/api/brain/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            });
            alert('Settings saved successfully!');
        } catch (error) {
            console.error('Failed to save settings:', error);
        } finally {
            setIsSaving(false);
        }
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (!settings) return null;

    const renderGeneral = () => (
        <div className="space-y-6">
            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Company Profile</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Company Name</label>
                        <input
                            type="text"
                            defaultValue={settings.general.company_name}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Website</label>
                        <input
                            type="url"
                            defaultValue={settings.general.website}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Support Email</label>
                        <input
                            type="email"
                            defaultValue={settings.general.support_email}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Phone Number</label>
                        <input
                            type="tel"
                            defaultValue={settings.general.phone}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        />
                    </div>
                </div>
            </div>

            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Regional Settings</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Time Zone</label>
                        <select
                            defaultValue={settings.general.timezone}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        >
                            <option>UTC-5 (Eastern Time)</option>
                            <option>UTC-8 (Pacific Time)</option>
                            <option>UTC+0 (GMT)</option>
                            <option>UTC+5:30 (IST)</option>
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Currency</label>
                        <select
                            defaultValue={settings.general.currency}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        >
                            <option>USD ($)</option>
                            <option>EUR (€)</option>
                            <option>GBP (£)</option>
                            <option>INR (₹)</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderSecurity = () => (
        <div className="space-y-6">
            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Authentication</h3>
                <div className="space-y-4">
                    <div className="flex items-center justify-between py-3 border-b border-gray-200 dark:border-gray-800">
                        <div>
                            <p className="font-medium text-gray-900 dark:text-white">Two-Factor Authentication (2FA)</p>
                            <p className="text-sm text-gray-500">Add an extra layer of security to your account</p>
                        </div>
                        <button className={`border px-4 py-2 rounded-lg ${settings.security.two_factor_enabled
                                ? 'bg-green-100 text-green-800 border-green-200'
                                : 'bg-white border-gray-300 text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300'
                            }`}>
                            {settings.security.two_factor_enabled ? 'Enabled' : 'Enable'}
                        </button>
                    </div>
                    <div className="flex items-center justify-between py-3 border-b border-gray-200 dark:border-gray-800">
                        <div>
                            <p className="font-medium text-gray-900 dark:text-white">Password Requirements</p>
                            <p className="text-sm text-gray-500">Require special characters and numbers</p>
                        </div>
                        <div className="relative inline-block w-12 mr-2 align-middle select-none transition duration-200 ease-in">
                            <input
                                type="checkbox"
                                defaultChecked={settings.security.password_requirements}
                                className="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                            />
                            <label className="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderTeam = () => (
        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
            <div className="p-6 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Team Members</h3>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm">
                    Invite Member
                </button>
            </div>
            <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-800">
                    <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Name</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Role</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                    {settings.team.map((member: any, idx: number) => (
                        <tr key={idx}>
                            <td className="px-6 py-4 whitespace-nowrap">
                                <div className="flex items-center">
                                    <div className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 font-bold">
                                        {member.name.charAt(0)}
                                    </div>
                                    <div className="ml-4">
                                        <div className="text-sm font-medium text-gray-900 dark:text-white">{member.name}</div>
                                        <div className="text-sm text-gray-500">{member.email}</div>
                                    </div>
                                </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                {member.role}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                                <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${member.status === 'Active'
                                        ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                                        : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                                    }`}>
                                    {member.status}
                                </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                <button className="text-blue-600 hover:text-blue-900 dark:hover:text-blue-400">Edit</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Settings</h2>
                <button
                    onClick={handleSave}
                    disabled={isLoading}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2 disabled:opacity-50"
                >
                    <Save className="w-4 h-4" />
                    {isLoading ? 'Saving...' : 'Save Changes'}
                </button>
            </div>

            <div className="flex space-x-4 border-b border-gray-200 dark:border-gray-800 overflow-x-auto">
                {[
                    { id: 'general', label: 'General', icon: Globe },
                    { id: 'security', label: 'Security', icon: Lock },
                    { id: 'team', label: 'Team', icon: Users },
                    { id: 'notifications', label: 'Notifications', icon: Bell },
                ].map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setCurrentTab(tab.id)}
                        className={`
              flex items-center gap-2 px-4 py-3 border-b-2 font-medium text-sm whitespace-nowrap transition-colors
              ${currentTab === tab.id
                                ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'}
            `}
                    >
                        <tab.icon className="w-4 h-4" />
                        {tab.label}
                    </button>
                ))}
            </div>

            <div className="mt-6">
                {currentTab === 'general' && renderGeneral()}
                {currentTab === 'security' && renderSecurity()}
                {currentTab === 'team' && renderTeam()}
                {currentTab === 'notifications' && (
                    <div className="text-center py-12 text-gray-500">
                        Notification settings coming soon
                    </div>
                )}
            </div>
        </div>
    );
};
