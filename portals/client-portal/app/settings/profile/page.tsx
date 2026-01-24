'use client';

import React from 'react';
import SettingsLayout from '@/components/settings/SettingsLayout';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { RefreshCw } from 'lucide-react';

import { brainApi } from '@/lib/brain-api';
import { useAuth } from '@/components/auth/AuthProvider';
import { toast } from 'sonner';

export default function ProfileSettingsPage() {
    const { getToken, user } = useAuth();
    const [profile, setProfile] = React.useState<any>({
        first_name: '',
        last_name: '',
        phone: '',
        job_title: '',
        company: '',
        timezone: '',
        locale: ''
    });
    const [isLoading, setIsLoading] = React.useState(true);
    const [isSaving, setIsSaving] = React.useState(false);

    React.useEffect(() => {
        const fetchProfile = async () => {
            try {
                const token = await getToken();
                if (!token) return;

                const data = await brainApi.users.me(token as string);
                setProfile({
                    first_name: data.first_name || '',
                    last_name: data.last_name || '',
                    phone: data.phone || '',
                    job_title: data.job_title || '',
                    company: data.company || '',
                    timezone: data.timezone || 'UTC',
                    locale: data.locale || 'en-US'
                });
            } catch (error) {
                console.error("Failed to fetch profile:", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchProfile();
    }, [getToken]);

    const handleSave = async () => {
        setIsSaving(true);
        try {
            const token = await getToken();
            if (!token) throw new Error("No token");

            await brainApi.users.updateMe({
                first_name: profile.first_name,
                last_name: profile.last_name,
                phone: profile.phone,
                job_title: profile.job_title,
                timezone: profile.timezone,
                locale: profile.locale
            }, token as string);
            toast.success("Profile updated successfully");
        } catch (error) {
            toast.error("Failed to update profile");
        } finally {
            setIsSaving(false);
        }
    };

    const getInitials = (name: string) => {
        return name
            .split(' ')
            .map(part => part[0])
            .join('')
            .toUpperCase()
            .slice(0, 2);
    };

    return (
        <SettingsLayout
            title="Profile Settings"
            description="Manage your personal information and public profile"
        >
            <div className="p-6 space-y-8">
                {isLoading ? (
                    <div className="flex justify-center p-12">
                        <RefreshCw className="w-8 h-8 animate-spin text-blue-600" />
                    </div>
                ) : (
                    <>
                        <div className="flex items-center gap-6">
                            <Avatar className="w-24 h-24">
                                {/* Use empty src for now as we don't have image in session yet */}
                                <AvatarImage src="" />
                                <AvatarFallback className="text-2xl bg-blue-100 text-blue-600">
                                    {user?.name ? getInitials(user.name) : 'U'}
                                </AvatarFallback>
                            </Avatar>
                            <div className="space-y-2">
                                <Button variant="outline" size="sm" disabled>Change Avatar (Coming Soon)</Button>
                                <p className="text-xs text-muted-foreground">Managed via SSO Provider</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <Label>First Name</Label>
                                <Input
                                    value={profile.first_name}
                                    onChange={e => setProfile({ ...profile, first_name: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Last Name</Label>
                                <Input
                                    value={profile.last_name}
                                    onChange={e => setProfile({ ...profile, last_name: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Email Address</Label>
                                <Input value={user?.email || ''} disabled />
                            </div>
                            <div className="space-y-2">
                                <Label>Phone</Label>
                                <Input
                                    value={profile.phone}
                                    onChange={e => setProfile({ ...profile, phone: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Job Title</Label>
                                <Input
                                    value={profile.job_title}
                                    onChange={e => setProfile({ ...profile, job_title: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Company</Label>
                                <Input value={profile.company} disabled />
                            </div>
                            <div className="space-y-2">
                                <Label>Timezone</Label>
                                <Input
                                    value={profile.timezone}
                                    onChange={e => setProfile({ ...profile, timezone: e.target.value })}
                                    placeholder="e.g. UTC, America/New_York"
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Locale / Language</Label>
                                <Input
                                    value={profile.locale}
                                    onChange={e => setProfile({ ...profile, locale: e.target.value })}
                                    placeholder="e.g. en-US"
                                />
                            </div>
                        </div>

                        <div className="pt-6 border-t border-slate-100 dark:border-slate-700 flex justify-end">
                            <Button onClick={handleSave} disabled={isSaving}>
                                {isSaving && <RefreshCw className="w-4 h-4 mr-2 animate-spin" />}
                                Save Changes
                            </Button>
                        </div>
                    </>
                )}
            </div>
        </SettingsLayout>
    );
}
