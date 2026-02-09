import React from 'react';
import { notFound } from 'next/navigation';
import { businessAPI } from '@/lib/api';
import { Header } from '@/components/layout/header';
import { ClaimForm } from '@/components/business/claim-form';
import { CheckCircle2, ShieldCheck, MapPin } from 'lucide-react';

interface Props {
    params: { slug: string };
}

export default async function ClaimBusinessPage({ params }: Props) {
    const business = await businessAPI.getBusinessBySlug(params.slug);

    if (!business) {
        notFound();
    }

    if (business.claimStatus === 'claimed') {
        return (
            <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
                <Header />
                <main className="max-w-4xl mx-auto px-4 py-20 text-center">
                    <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <ShieldCheck className="w-8 h-8 text-green-600" />
                    </div>
                    <h1 className="text-3xl font-bold mb-4">This Business is Already Claimed</h1>
                    <p className="text-muted-foreground text-lg max-w-lg mx-auto mb-8">
                        <strong>{business.name}</strong> has already been verified and claimed by its owner.
                    </p>
                    <div className="flex justify-center space-x-4">
                        <a href={`/biz/${business.slug}`} className="text-primary hover:underline font-medium">
                            Return to Business Profile
                        </a>
                        <span className="text-muted-foreground">•</span>
                        <a href="/search" className="text-primary hover:underline font-medium">
                            Search Other Businesses
                        </a>
                    </div>
                </main>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
            <Header />

            <div className="bg-primary/5 border-b border-primary/10 py-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Grow Your Business Presence</h1>
                            <p className="text-muted-foreground max-w-2xl">
                                Join our network of thousands of verified businesses and take control of your online reputation.
                            </p>
                        </div>
                        <div className="flex items-center space-x-4 text-sm font-medium">
                            <div className="flex items-center text-green-600">
                                <CheckCircle2 className="w-4 h-4 mr-1.5" />
                                100% Free Verification
                            </div>
                            <div className="flex items-center text-blue-600">
                                <ShieldCheck className="w-4 h-4 mr-1.5" />
                                Instant Management
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                    {/* Main Content */}
                    <div className="lg:col-span-2">
                        <ClaimForm business={business} />
                    </div>

                    {/* Sidebar Information */}
                    <div className="space-y-8">
                        <div>
                            <h2 className="text-xl font-bold mb-4">Why Claim Your Listing?</h2>
                            <ul className="space-y-4">
                                <li className="flex items-start">
                                    <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center mr-3 mt-0.5">
                                        <span className="text-xs font-bold text-primary">1</span>
                                    </div>
                                    <div>
                                        <p className="font-semibold text-sm">Update Information</p>
                                        <p className="text-xs text-muted-foreground">Keep your address, hours, and contact details up-to-date.</p>
                                    </div>
                                </li>
                                <li className="flex items-start">
                                    <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center mr-3 mt-0.5">
                                        <span className="text-xs font-bold text-primary">2</span>
                                    </div>
                                    <div>
                                        <p className="font-semibold text-sm">Manage Reviews</p>
                                        <p className="text-xs text-muted-foreground">Reply directly to your customers and build trust.</p>
                                    </div>
                                </li>
                                <li className="flex items-start">
                                    <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center mr-3 mt-0.5">
                                        <span className="text-xs font-bold text-primary">3</span>
                                    </div>
                                    <div>
                                        <p className="font-semibold text-sm">Add Photos & Events</p>
                                        <p className="text-xs text-muted-foreground">Showcase your products, services, and upcoming promotions.</p>
                                    </div>
                                </li>
                            </ul>
                        </div>

                        <div className="p-6 bg-white dark:bg-slate-900 rounded-xl border border-dashed border-gray-300 dark:border-gray-700">
                            <h3 className="font-bold flex items-center mb-3">
                                <MapPin className="w-4 h-4 mr-2" />
                                Business Location
                            </h3>
                            <p className="text-sm font-medium mb-1">{business.name}</p>
                            <p className="text-xs text-muted-foreground mb-4">
                                {business.location.address}, {business.location.city}, {business.location.state} {business.location.zipCode}
                            </p>
                            <div className="aspect-video relative rounded-lg bg-slate-100 dark:bg-slate-800 flex items-center justify-center border">
                                <span className="text-xs text-muted-foreground italic">Map Preview</span>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
