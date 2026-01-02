'use client';

import { useState, useEffect } from 'react';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useToast } from '@/components/ui/use-toast';
import { brainApi } from '@/lib/brain-api';
import { Loader2, Palette, Type, Globe, Check } from 'lucide-react';
import { Separator } from '@/components/ui/separator';

export default function BrandingSettingsPage() {
    const { toast } = useToast();
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);

    // Config State
    const [config, setConfig] = useState({
        portal_title: '',
        logo_url: '',
        favicon_url: '',
        primary_color: '#2563eb',
        secondary_color: '#475569',
        font_family: 'Inter'
    });

    useEffect(() => {
        loadConfig();
    }, []);

    const loadConfig = async () => {
        try {
            setIsLoading(true);
            const data = await brainApi.admin.getTenantConfig();
            if (data) {
                setConfig({
                    portal_title: data.portal_title || 'BizOSaaS Client Portal',
                    logo_url: data.logo_url || '',
                    favicon_url: data.favicon_url || '',
                    primary_color: data.primary_color || '#2563eb',
                    secondary_color: data.secondary_color || '#475569',
                    font_family: data.font_family || 'Inter'
                });
            }
        } catch (error) {
            console.error("Failed to load branding config", error);
            toast({
                title: "Error loading configuration",
                description: "Could not fetch current branding settings.",
                variant: "destructive"
            });
        } finally {
            setIsLoading(false);
        }
    };

    const handleSave = async () => {
        try {
            setIsSaving(true);
            await brainApi.admin.updateTenantConfig(config);
            toast({
                title: "Settings saved",
                description: "Branding configuration has been updated successfully.",
            });
        } catch (error) {
            console.error("Failed to save branding config", error);
            toast({
                title: "Error saving settings",
                description: "Failed to update branding configuration.",
                variant: "destructive"
            });
        } finally {
            setIsSaving(false);
        }
    };

    const handleChange = (field: string, value: string) => {
        setConfig(prev => ({ ...prev, [field]: value }));
    };

    if (isLoading) {
        return (
            <DashboardLayout>
                <div className="flex items-center justify-center h-full">
                    <Loader2 className="w-8 h-8 animate-spin text-primary" />
                </div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout>
            <div className="space-y-6">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Branding & White Label</h2>
                    <p className="text-muted-foreground">Customize the look and feel of your Client Portal.</p>
                </div>

                <div className="grid gap-6 md:grid-cols-2">
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Globe className="w-5 h-5" />
                                Portal Identity
                            </CardTitle>
                            <CardDescription>Basic information displayed in the browser tab and headers.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="portal_title">Portal Title</Label>
                                <Input
                                    id="portal_title"
                                    placeholder="e.g. Acme Client Portal"
                                    value={config.portal_title}
                                    onChange={(e) => handleChange('portal_title', e.target.value)}
                                />
                                <p className="text-xs text-muted-foreground">Matches the HTML &lt;title&gt; tag.</p>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="logo_url">Logo URL</Label>
                                <Input
                                    id="logo_url"
                                    placeholder="https://"
                                    value={config.logo_url}
                                    onChange={(e) => handleChange('logo_url', e.target.value)}
                                />
                                <p className="text-xs text-muted-foreground">Direct link to your logo image (PNG/SVG recommended).</p>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="favicon_url">Favicon URL</Label>
                                <Input
                                    id="favicon_url"
                                    placeholder="https://"
                                    value={config.favicon_url}
                                    onChange={(e) => handleChange('favicon_url', e.target.value)}
                                />
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Palette className="w-5 h-5" />
                                Theme Colors
                            </CardTitle>
                            <CardDescription>Primary colors used for buttons, links, and active states.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            <div className="flex items-center gap-4">
                                <div
                                    className="w-16 h-16 rounded-lg border shadow-sm"
                                    style={{ backgroundColor: config.primary_color }}
                                />
                                <div className="space-y-2 flex-1">
                                    <Label htmlFor="primary_color">Primary Color</Label>
                                    <div className="flex gap-2">
                                        <Input
                                            id="primary_color"
                                            type="color"
                                            className="w-12 p-1 h-9"
                                            value={config.primary_color}
                                            onChange={(e) => handleChange('primary_color', e.target.value)}
                                        />
                                        <Input
                                            value={config.primary_color}
                                            onChange={(e) => handleChange('primary_color', e.target.value)}
                                            className="font-mono uppercase"
                                            maxLength={7}
                                        />
                                    </div>
                                </div>
                            </div>

                            <Separator />

                            <div className="flex items-center gap-4">
                                <div
                                    className="w-16 h-16 rounded-lg border shadow-sm"
                                    style={{ backgroundColor: config.secondary_color }}
                                />
                                <div className="space-y-2 flex-1">
                                    <Label htmlFor="secondary_color">Secondary Color</Label>
                                    <div className="flex gap-2">
                                        <Input
                                            id="secondary_color"
                                            type="color"
                                            className="w-12 p-1 h-9"
                                            value={config.secondary_color}
                                            onChange={(e) => handleChange('secondary_color', e.target.value)}
                                        />
                                        <Input
                                            value={config.secondary_color}
                                            onChange={(e) => handleChange('secondary_color', e.target.value)}
                                            className="font-mono uppercase"
                                            maxLength={7}
                                        />
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="md:col-span-2">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Type className="w-5 h-5" />
                                Typography
                            </CardTitle>
                            <CardDescription>Choose the font family for your portal.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-2 max-w-md">
                                <Label htmlFor="font_family">Font Family</Label>
                                <Input
                                    id="font_family"
                                    value={config.font_family}
                                    onChange={(e) => handleChange('font_family', e.target.value)}
                                    placeholder="e.g. Inter, Roboto, Open Sans"
                                />
                                <p className="text-xs text-muted-foreground">Ensure the font is web-safe or loaded via CSS.</p>
                            </div>
                        </CardContent>
                        <CardFooter className="bg-muted/50 flex justify-end p-4 rounded-b-lg">
                            <Button onClick={handleSave} disabled={isSaving}>
                                {isSaving && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                {isSaving ? "Saving..." : "Save Changes"}
                            </Button>
                        </CardFooter>
                    </Card>
                </div>
            </div>
        </DashboardLayout>
    );
}
