'use client';

import React from 'react';
import SettingsLayout from '@/components/settings/SettingsLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { RefreshCw } from 'lucide-react';

import { brainApi } from '@/lib/brain-api';
import { useAuth, useUser } from '@clerk/nextjs';
import { toast } from 'sonner';

export default function ProfileSettingsPage() {
    const { getToken } = useAuth();
    const { user: clerkUser } = useUser();
    const [profile, setProfile] = React.useState<any>({
        first_name: '',
        last_name: '',
        phone: '',
        job_title: '',
        company: ''
    });
    const [isLoading, setIsLoading] = React.useState(true);
    const [isSaving, setIsSaving] = React.useState(false);

    React.useEffect(() => {
        const fetchProfile = async () => {
            try {
                const token = await getToken();
                const data = await brainApi.users.me(token as string);
                setProfile({
                    first_name: data.first_name || '',
                    last_name: data.last_name || '',
                    phone: data.phone || '',
                    job_title: data.job_title || '',
                    company: data.company || ''
                });
            } catch (error) {
                console.error("Failed to fetch profile:", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchProfile();
    }, []);

    const handleSave = async () => {
        setIsSaving(true);
        try {
            const token = await getToken();
            await brainApi.users.updateMe({
                first_name: profile.first_name,
                last_name: profile.last_name,
                phone: profile.phone,
                job_title: profile.job_title
            }, token as string);
            toast.success("Profile updated successfully");
        } catch (error) {
            toast.error("Failed to update profile");
        } finally {
            setIsSaving(false);
        }
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
                                <AvatarImage src={clerkUser?.imageUrl} />
                                <AvatarFallback className="text-2xl bg-blue-100 text-blue-600">
                                    {profile.first_name?.[0]}{profile.last_name?.[0]}
                                </AvatarFallback>
                            </Avatar>
                            <div className="space-y-2">
                                <Button variant="outline" size="sm">Change Avatar</Button>
                                <p className="text-xs text-muted-foreground">JPG, GIF or PNG. Max size of 2MB.</p>
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
                                <Input value={clerkUser?.primaryEmailAddress?.emailAddress || ''} disabled />
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
