'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Loader2, Plus, Building2, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { businessAPI } from '@/lib/api';
import { Business } from '@/types/business';
import { cn } from '@/lib/utils';
import Image from 'next/image';

export default function MyBusinessesPage() {
    const router = useRouter();
    const [businesses, setBusinesses] = useState<Business[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchMyListings();
    }, []);

    const fetchMyListings = async () => {
        setLoading(true);
        try {
            const data = await businessAPI.getMyListings();
            setBusinesses(data);
            setError(null);
        } catch (err: any) {
            // In a real app, we would check for 401 Unauthorized here
            if (err.response?.status === 401) {
                setError("Please log in to view your businesses.");
            } else {
                setError("Failed to load your businesses. Please try again later.");
            }
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen pt-24 pb-12 flex justify-center items-center">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen pt-24 pb-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6 flex flex-col items-center text-center">
                    <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
                    <h2 className="text-lg font-semibold text-red-900 mb-2">Access Denied</h2>
                    <p className="text-red-700 mb-6">{error}</p>
                    <div className="flex gap-4">
                        <Button onClick={() => router.push('/')}>Go Home</Button>
                        <Button variant="outline" onClick={() => window.location.reload()}>Try Again</Button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen pt-24 pb-12 bg-gray-50 dark:bg-gray-900">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">My Businesses</h1>
                        <p className="mt-2 text-gray-600 dark:text-gray-400">
                            Manage your claimed business listings and view analytics.
                        </p>
                    </div>
                    <Button asChild>
                        <Link href="/list-business">
                            <Plus className="w-4 h-4 mr-2" />
                            Add New Business
                        </Link>
                    </Button>
                </div>

                {businesses.length === 0 ? (
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center">
                        <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                            <Building2 className="w-8 h-8 text-gray-400" />
                        </div>
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No businesses found</h3>
                        <p className="text-gray-500 dark:text-gray-400 mb-8 max-w-md mx-auto">
                            You haven't claimed or added any businesses yet. Search for your business to claim it, or list a new one.
                        </p>
                        <div className="flex justify-center gap-4">
                            <Button asChild variant="outline">
                                <Link href="/search">Find my Business</Link>
                            </Button>
                            <Button asChild>
                                <Link href="/list-business">List a Business</Link>
                            </Button>
                        </div>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {businesses.map((business) => (
                            <Card key={business.id} className="flex flex-col h-full overflow-hidden hover:shadow-md transition-shadow">
                                <div className="relative h-48 bg-gray-200">
                                    <Image
                                        src={(business.images && business.images[0]) || '/placeholder-business.jpg'}
                                        alt={business.name}
                                        fill
                                        className="object-cover"
                                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                                    />
                                    <div className="absolute top-2 right-2">
                                        <span className={cn(
                                            "px-2 py-1 rounded-full text-xs font-medium bg-white/90 backdrop-blur-sm",
                                            business.verification_status === 'verified' ? "text-green-700 bg-green-50" :
                                                business.verification_status === 'pending' ? "text-yellow-700 bg-yellow-50" :
                                                    "text-gray-700 bg-gray-50"
                                        )}>
                                            {business.verification_status === 'verified' ? 'Verified' :
                                                business.verification_status === 'pending' ? 'Verification Pending' : 'Unverified'}
                                        </span>
                                    </div>
                                </div>
                                <CardHeader>
                                    <CardTitle className="line-clamp-1">{business.name}</CardTitle>
                                    <CardDescription className="line-clamp-1">
                                        {business.location?.city ? `${business.location.city}, ${business.location.state || ''}` : 'Location n/a'}
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="flex-grow">
                                    <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                                        <div className="flex justify-between">
                                            <span>Views (30d)</span>
                                            <span className="font-medium text-gray-900 dark:text-white">
                                                {business.analytics?.views || 0}
                                            </span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span>Rating</span>
                                            <span className="font-medium text-gray-900 dark:text-white">
                                                {business.rating} ★
                                            </span>
                                        </div>
                                    </div>
                                </CardContent>
                                <CardFooter className="pt-0 border-t border-gray-100 dark:border-gray-800 p-4 bg-gray-50/50 dark:bg-gray-900/50">
                                    <div className="flex w-full gap-2">
                                        <Button asChild variant="outline" className="flex-1">
                                            <Link href={`/biz/${business.slug || business.id}`}>
                                                View
                                            </Link>
                                        </Button>
                                        <Button asChild className="flex-1">
                                            <Link href={`/dashboard/business/${business.id}`}>
                                                Manage
                                            </Link>
                                        </Button>
                                    </div>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
