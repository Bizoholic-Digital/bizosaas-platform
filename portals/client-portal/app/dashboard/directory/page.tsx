'use client';

import React, { useEffect, useState } from 'react';
import { useSetHeader } from '@/lib/contexts/HeaderContext';
import { brainApi } from '@/lib/brain-api';
import { Plus, Building2, ExternalLink, MessageSquare, Calendar, Tag, ChevronRight } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import ListingWizard from '@/components/directory/ListingWizard';
import LeadCenter from '@/components/directory/LeadCenter';
import EventManager from '@/components/directory/EventManager';
import CouponManager from '@/components/directory/CouponManager';

export default function DirectoryPage() {
    useSetHeader("My Directory Listings", "Manage your business profiles, promotions, and leads.");
    const [listings, setListings] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [view, setView] = useState<'list' | 'wizard' | 'enquiries' | 'events' | 'coupons'>('list');
    const [selectedListing, setSelectedListing] = useState<any>(null);

    const fetchListings = async () => {
        setLoading(true);
        try {
            const data = await brainApi.directory.getMyListings();
            setListings(data);
        } catch (err) {
            console.error("Failed to fetch listings", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchListings();
    }, []);

    if (view === 'wizard') {
        return (
            <ListingWizard
                initialData={selectedListing}
                onComplete={() => {
                    setView('list');
                    fetchListings();
                }}
                onCancel={() => setView('list')}
            />
        );
    }

    if (view === 'enquiries' && selectedListing) {
        return (
            <LeadCenter
                listing={selectedListing}
                onBack={() => setView('list')}
            />
        );
    }

    if (loading) {
        return (
            <div className="p-6 space-y-4">
                {[...Array(3)].map((_, i) => (
                    <div key={i} className="h-40 bg-gray-100 dark:bg-gray-800 animate-pulse rounded-xl" />
                ))}
            </div>
        );
    }

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-black text-gray-900 dark:text-white uppercase tracking-tighter">Your Listings</h2>
                <Button
                    onClick={() => {
                        setSelectedListing(null);
                        setView('wizard');
                    }}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl px-6 py-2 shadow-lg shadow-blue-500/20 gap-2"
                >
                    <Plus className="w-4 h-4" /> Add New Listing
                </Button>
            </div>

            {listings.length === 0 ? (
                <Card className="border-dashed border-2 py-12 flex flex-col items-center justify-center text-center">
                    <div className="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
                        <Building2 className="w-8 h-8 text-gray-400" />
                    </div>
                    <CardTitle className="text-xl mb-2">No listings found</CardTitle>
                    <CardDescription className="max-w-sm">
                        You haven't claimed or created any business listings yet. Reach more customers by listing your business today.
                    </CardDescription>
                    <Button variant="outline" className="mt-6 font-bold rounded-xl px-8">
                        Get Started
                    </Button>
                </Card>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {listings.map((listing) => (
                        <Card key={listing.id} className="overflow-hidden hover:border-blue-500 transition-all group border-gray-200 dark:border-gray-800">
                            <CardHeader className="flex flex-row items-center justify-between pb-2">
                                <div className="flex items-center gap-3">
                                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center text-blue-600 dark:text-blue-400">
                                        <Building2 className="w-6 h-6" />
                                    </div>
                                    <div>
                                        <CardTitle className="text-lg font-bold group-hover:text-blue-600 transition-colors uppercase tracking-tight">
                                            {listing.business_name}
                                        </CardTitle>
                                        <CardDescription className="text-xs truncate max-w-[200px]">{listing.city || 'Remote'}, {listing.state || 'Online'}</CardDescription>
                                    </div>
                                </div>
                                <Badge variant={listing.status === 'active' ? 'default' : 'secondary'} className="uppercase font-black text-[10px]">
                                    {listing.status}
                                </Badge>
                            </CardHeader>
                            <CardContent>
                                <div className="grid grid-cols-3 gap-2 mt-4">
                                    <div className="bg-gray-50 dark:bg-gray-800/50 p-3 rounded-xl border border-gray-100 dark:border-gray-800 text-center">
                                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1">Views</p>
                                        <p className="text-xl font-black text-gray-900 dark:text-white leading-none">0</p>
                                    </div>
                                    <div className="bg-gray-50 dark:bg-gray-800/50 p-3 rounded-xl border border-gray-100 dark:border-gray-800 text-center">
                                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1">Leads</p>
                                        <p className="text-xl font-black text-gray-900 dark:text-white leading-none">0</p>
                                    </div>
                                    <div className="bg-gray-50 dark:bg-gray-800/50 p-3 rounded-xl border border-gray-100 dark:border-gray-800 text-center">
                                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1">Rating</p>
                                        <p className="text-xl font-black text-gray-900 dark:text-white leading-none">{listing.google_rating || '5.0'}</p>
                                    </div>
                                </div>

                                <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-100 dark:border-gray-800">
                                    <div className="flex gap-1 sm:gap-2">
                                        <Button
                                            onClick={() => {
                                                setSelectedListing(listing);
                                                setView('enquiries');
                                            }}
                                            size="sm"
                                            variant="ghost"
                                            className="h-8 px-2 text-[10px] sm:text-xs font-bold uppercase tracking-tight gap-1.5 hover:text-blue-600 text-blue-600 bg-blue-50/50 dark:bg-blue-900/10"
                                        >
                                            <MessageSquare className="w-3.5 h-3.5" /> Enquiries
                                        </Button>
                                        <Button
                                            onClick={() => {
                                                setSelectedListing(listing);
                                                setView('events');
                                            }}
                                            size="sm"
                                            variant="ghost"
                                            className="h-8 px-2 text-[10px] sm:text-xs font-bold uppercase tracking-tight gap-1.5 hover:text-indigo-600"
                                        >
                                            <Calendar className="w-3.5 h-3.5" /> Events
                                        </Button>
                                        <Button
                                            onClick={() => {
                                                setSelectedListing(listing);
                                                setView('coupons');
                                            }}
                                            size="sm"
                                            variant="ghost"
                                            className="h-8 px-2 text-[10px] sm:text-xs font-bold uppercase tracking-tight gap-1.5 hover:text-green-600"
                                        >
                                            <Tag className="w-3.5 h-3.5" /> Coupons
                                        </Button>
                                    </div>
                                    <Link href={`https://directory.bizoholic.net/biz/${listing.business_slug}`} target="_blank">
                                        <Button size="sm" variant="outline" className="h-8 px-3 rounded-lg text-[9px] sm:text-[10px] font-black uppercase tracking-widest gap-1.5">
                                            View <ExternalLink className="w-3 h-3" />
                                        </Button>
                                    </Link>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
}
