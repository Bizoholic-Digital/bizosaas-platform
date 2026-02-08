'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter, useParams } from 'next/navigation';
import { Loader2, ArrowLeft, Globe, LineChart, MessageSquare, Tag, MapPin, Phone, Mail, Clock, ShieldCheck, Sparkles, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { businessAPI } from '@/lib/api';
import { Business } from '@/types/business';
import { cn } from '@/lib/utils';
import Image from 'next/image';

export default function ManageBusinessPage() {
    const router = useRouter();
    const params = useParams();
    const id = params?.id as string;

    const [business, setBusiness] = useState<Business | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [analyzing, setAnalyzing] = useState(false);
    const [optimizing, setOptimizing] = useState(false);
    const [actionMessage, setActionMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

    useEffect(() => {
        if (id) {
            fetchBusiness(id);
        }
    }, [id]);

    const fetchBusiness = async (businessId: string) => {
        setLoading(true);
        try {
            // We use the same getMyListings but filter or ideally we would have getBusinessById(id)
            // Since getMyListings returns all owned businesses, we can find the one we need.
            // Or we can use the public getBusinessById if we don't have a secure single-fetch yet, 
            // but for management we really want the secure context. 
            // For now, let's re-use getMyListings and find the specific one.
            const businesses = await businessAPI.getMyListings();
            const found = businesses.find(b => b.id === businessId);

            if (found) {
                setBusiness(found);
                setError(null);
            } else {
                setError("Business not found or you don't have permission to manage it.");
            }
        } catch (err: any) {
            setError("Failed to load business details.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleAnalyze = async () => {
        if (!business) return;
        setAnalyzing(true);
        setActionMessage(null);
        try {
            // We need to add this method to api.ts first, but I'll assume we'll add it momentarily.
            // For now, I'll direct fetch or use a precise proxy.
            const response = await fetch(`/api/brain/business-directory/businesses/${business.id}/analyze`, {
                method: 'POST',
            });
            const data = await response.json();

            if (response.ok) {
                setActionMessage({ type: 'success', text: 'Website analysis complete! Your profile has been enriched.' });
                fetchBusiness(business.id); // Refresh data
            } else {
                throw new Error(data.error || 'Analysis failed');
            }
        } catch (err: any) {
            setActionMessage({ type: 'error', text: err.message || "Failed to analyze website." });
        } finally {
            setAnalyzing(false);
        }
    };

    const handleOptimizeSEO = async () => {
        if (!business) return;
        setOptimizing(true);
        setActionMessage(null);
        try {
            const response = await fetch(`/api/brain/business-directory/businesses/${business.id}/optimize-seo`, {
                method: 'POST',
            });
            const data = await response.json();

            if (response.ok) {
                setActionMessage({ type: 'success', text: 'SEO Optimization complete! Your listing is now more discoverable.' });
                fetchBusiness(business.id); // Refresh data
            } else {
                throw new Error(data.error || 'Optimization failed');
            }
        } catch (err: any) {
            setActionMessage({ type: 'error', text: err.message || "Failed to optimize SEO." });
        } finally {
            setOptimizing(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen pt-24 pb-12 flex justify-center items-center">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
        );
    }

    if (error || !business) {
        return (
            <div className="min-h-screen pt-24 pb-12 max-w-7xl mx-auto px-4">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6 flex flex-col items-center text-center">
                    <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
                    <h2 className="text-lg font-semibold text-red-900 mb-2">Error</h2>
                    <p className="text-red-700 mb-6">{error || "Business not found"}</p>
                    <Button asChild onClick={() => router.push('/dashboard/my-businesses')}>
                        <Link href="/dashboard/my-businesses">Back to My Businesses</Link>
                    </Button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen pt-24 pb-12 bg-gray-50 dark:bg-gray-900">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <Button variant="ghost" size="sm" asChild className="mb-4 pl-0 hover:bg-transparent hover:text-primary">
                        <Link href="/dashboard/my-businesses" className="flex items-center">
                            <ArrowLeft className="w-4 h-4 mr-2" />
                            Back to My Businesses
                        </Link>
                    </Button>
                    <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                        <div className="flex items-center gap-4">
                            <div className="relative w-16 h-16 rounded-lg overflow-hidden bg-gray-200 border border-gray-100 flex-shrink-0">
                                <Image
                                    src={(business.images && business.images[0]) || '/placeholder-business.jpg'}
                                    alt={business.name}
                                    fill
                                    className="object-cover"
                                />
                            </div>
                            <div>
                                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">{business.name}</h1>
                                <div className="flex items-center text-gray-500 mt-1 space-x-2">
                                    <span className={cn(
                                        "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium",
                                        business.verification_status === 'verified' ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"
                                    )}>
                                        {business.verification_status === 'verified' && <ShieldCheck className="w-3 h-3 mr-1" />}
                                        {business.verification_status === 'verified' ? 'Verified' : 'Unverified'}
                                    </span>
                                    <span>•</span>
                                    <span>{business.category.name}</span>
                                    <span>•</span>
                                    <span className="flex items-center">
                                        <MapPin className="w-3 h-3 mr-1" />
                                        {business.location.city}
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <Button variant="outline" asChild>
                                <Link href={`/business/${business.slug || business.id}`}>
                                    <Globe className="w-4 h-4 mr-2" />
                                    View Public Listing
                                </Link>
                            </Button>
                            <Button>
                                Edit Profile
                            </Button>
                        </div>
                    </div>
                </div>

                {/* Notifications */}
                {actionMessage && (
                    <div className={cn(
                        "mb-6 p-4 rounded-md flex items-center",
                        actionMessage.type === 'success' ? "bg-green-50 text-green-800 border border-green-200" : "bg-red-50 text-red-800 border border-red-200"
                    )}>
                        {actionMessage.type === 'success' ? <Sparkles className="w-5 h-5 mr-2" /> : <AlertCircle className="w-5 h-5 mr-2" />}
                        {actionMessage.text}
                    </div>
                )}

                {/* Dashboard Tabs */}
                <Tabs defaultValue="overview" className="space-y-6">
                    <TabsList className="bg-white dark:bg-gray-800 p-1 rounded-lg border border-gray-200 dark:border-gray-700 w-full md:w-auto h-auto grid grid-cols-2 md:inline-flex">
                        <TabsTrigger value="overview">Overview</TabsTrigger>
                        <TabsTrigger value="ai-tools">
                            <Sparkles className="w-3 h-3 mr-1 text-purple-500" />
                            AI Tools
                        </TabsTrigger>
                        <TabsTrigger value="enquiries">Enquiries</TabsTrigger>
                        <TabsTrigger value="reviews">Reviews</TabsTrigger>
                    </TabsList>

                    <TabsContent value="overview" className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {/* Analytics Cards */}
                            <Card>
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-sm font-medium text-muted-foreground">Total Views</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold">{business.analytics?.views || 0}</div>
                                    <p className="text-xs text-muted-foreground mt-1">+12% from last month</p>
                                </CardContent>
                            </Card>
                            <Card>
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-sm font-medium text-muted-foreground">Website Clicks</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold">{business.analytics?.website_clicks || 0}</div>
                                    <p className="text-xs text-muted-foreground mt-1">+5% from last month</p>
                                </CardContent>
                            </Card>
                            <Card>
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-sm font-medium text-muted-foreground">Call Clicks</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold">{business.analytics?.phone_clicks || 0}</div>
                                    <p className="text-xs text-muted-foreground mt-1">Steady</p>
                                </CardContent>
                            </Card>
                        </div>

                        <Card>
                            <CardHeader>
                                <CardTitle>Profile Completion</CardTitle>
                                <CardDescription>Complete your profile to rank higher in searches.</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-4">
                                    <div className="space-y-2">
                                        <div className="flex justify-between text-sm">
                                            <span>Profile Strength</span>
                                            <span className="font-medium">Good (75%)</span>
                                        </div>
                                        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                                            <div className="h-full bg-green-500 w-3/4"></div>
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4">
                                        <div className="flex items-center text-sm text-gray-600">
                                            <div className="w-2 h-2 rounded-full bg-green-500 mr-2"></div>
                                            Business Name & Description
                                        </div>
                                        <div className="flex items-center text-sm text-gray-600">
                                            <div className="w-2 h-2 rounded-full bg-green-500 mr-2"></div>
                                            Contact Information
                                        </div>
                                        <div className="flex items-center text-sm text-gray-600">
                                            <div className="w-2 h-2 rounded-full bg-gray-300 mr-2"></div>
                                            Photos (Add more for better reach)
                                        </div>
                                        <div className="flex items-center text-sm text-gray-600">
                                            <div className="w-2 h-2 rounded-full bg-gray-300 mr-2"></div>
                                            Social Media Links
                                        </div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </TabsContent>

                    <TabsContent value="ai-tools" className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <Card className="border-purple-100 dark:border-purple-900 bg-purple-50/20 dark:bg-purple-900/10">
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Globe className="w-5 h-5 text-purple-600" />
                                        Website Analyzer
                                    </CardTitle>
                                    <CardDescription>
                                        Use AI to scan your website and automatically fill in missing details like social links, amenities, and keywords.
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    {business.contact?.website ? (
                                        <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
                                            Target: <span className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">{business.contact.website}</span>
                                        </p>
                                    ) : (
                                        <p className="text-sm text-yellow-600 mb-4 flex items-center">
                                            <AlertCircle className="w-4 h-4 mr-2" />
                                            Please add a website URL to your profile first.
                                        </p>
                                    )}
                                </CardContent>
                                <CardFooter>
                                    <Button
                                        onClick={handleAnalyze}
                                        disabled={analyzing || !business.contact?.website}
                                        className="w-full bg-purple-600 hover:bg-purple-700"
                                    >
                                        {analyzing ? (
                                            <>
                                                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                                Analyzing Website...
                                            </>
                                        ) : (
                                            <>
                                                <Sparkles className="w-4 h-4 mr-2" />
                                                Enrich Profile with AI
                                            </>
                                        )}
                                    </Button>
                                </CardFooter>
                            </Card>

                            <Card className="border-blue-100 dark:border-blue-900 bg-blue-50/20 dark:bg-blue-900/10">
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <LineChart className="w-5 h-5 text-blue-600" />
                                        SEO Optimizer
                                    </CardTitle>
                                    <CardDescription>
                                        Generate an optimized description, meta tags, and keywords for your listing to improve search visibility.
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm text-gray-600 dark:text-gray-300">
                                        Our AI checks your current content and suggests improvements to help you rank higher on Google and within our directory.
                                    </p>
                                </CardContent>
                                <CardFooter>
                                    <Button
                                        onClick={handleOptimizeSEO}
                                        disabled={optimizing}
                                        className="w-full bg-blue-600 hover:bg-blue-700"
                                    >
                                        {optimizing ? (
                                            <>
                                                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                                Optimizing...
                                            </>
                                        ) : (
                                            <>
                                                <Tag className="w-4 h-4 mr-2" />
                                                Optimize SEO
                                            </>
                                        )}
                                    </Button>
                                </CardFooter>
                            </Card>
                        </div>
                    </TabsContent>

                    <TabsContent value="enquiries">
                        <Card>
                            <CardHeader>
                                <CardTitle>Recent Enquiries</CardTitle>
                                <CardDescription>Messages from potential customers.</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="text-center py-12 text-gray-500">
                                    <MessageSquare className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                                    <p>No enquiries yet.</p>
                                </div>
                            </CardContent>
                        </Card>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
}
