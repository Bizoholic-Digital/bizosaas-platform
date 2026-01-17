import React from 'react';
import { Metadata, ResolvingMetadata } from 'next';
import { notFound } from 'next/navigation';
import { businessAPI } from '@/lib/api';
import { EnhancedBusinessProfile } from '@/components/business/enhanced-business-profile';
import Header from '@/components/layout/header';

interface Props {
    params: { slug: string };
    searchParams: { [key: string]: string | string[] | undefined };
}

export async function generateMetadata(
    { params }: Props,
    parent: ResolvingMetadata
): Promise<Metadata> {
    const business = await businessAPI.getBusinessBySlug(params.slug);

    if (!business) {
        return {
            title: 'Business Not Found | BizDirectory',
        };
    }

    const previousImages = (await parent).openGraph?.images || [];

    return {
        title: `${business.name} | ${business.category.name} in ${business.location.city} | BizDirectory`,
        description: business.description || `View details, contact info, and reviews for ${business.name} in ${business.location.city}.`,
        openGraph: {
            title: business.name,
            description: business.description,
            url: `https://directory.bizoholic.net/business/${business.slug}`,
            siteName: 'BizDirectory',
            images: [
                business.images[0] || '/og-image.jpg',
                ...previousImages,
            ],
            type: 'website',
        },
        twitter: {
            card: 'summary_large_image',
            title: business.name,
            description: business.description,
            images: [business.images[0] || '/og-image.jpg'],
        },
        alternates: {
            canonical: `https://directory.bizoholic.net/business/${business.slug}`,
        },
    };
}

export default async function BusinessProfilePage({ params }: Props) {
    const business = await businessAPI.getBusinessBySlug(params.slug);

    if (!business) {
        notFound();
    }

    // Generate JSON-LD for LocalBusiness
    const jsonLd = {
        '@context': 'https://schema.org',
        '@type': 'LocalBusiness',
        name: business.name,
        image: business.images,
        '@id': `https://directory.bizoholic.net/business/${business.slug}`,
        url: `https://directory.bizoholic.net/business/${business.slug}`,
        telephone: business.contact.phone,
        address: {
            '@type': 'PostalAddress',
            streetAddress: business.location.address,
            addressLocality: business.location.city,
            addressRegion: business.location.state,
            postalCode: business.location.zipCode,
            addressCountry: business.location.country,
        },
        geo: {
            '@type': 'GeoCoordinates',
            latitude: business.location.coordinates?.lat,
            longitude: business.location.coordinates?.lng,
        },
        description: business.description,
        openingHoursSpecification: business.hours ? Object.entries(business.hours).map(([day, hours]) => ({
            '@type': 'OpeningHoursSpecification',
            dayOfWeek: day.charAt(0).toUpperCase() + day.slice(1),
            opens: hours.closed ? '00:00' : hours.open,
            closes: hours.closed ? '00:00' : hours.close,
        })) : undefined,
        aggregateRating: {
            '@type': 'AggregateRating',
            ratingValue: business.rating,
            reviewCount: business.reviewCount,
        },
    };

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
            />

            <Header />

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <EnhancedBusinessProfile business={business} />
            </main>

            <footer className="bg-white dark:bg-slate-900 border-t mt-20 py-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <p className="text-muted-foreground mb-4">
                        Is this your business? <a href={`/claim/${business.id}`} className="text-primary font-medium hover:underline">Claim this profile</a> to update your information.
                    </p>
                    <div className="flex justify-center space-x-4">
                        <a href="/" className="text-sm text-gray-500 hover:text-primary">Home</a>
                        <a href="/search" className="text-sm text-gray-500 hover:text-primary">Search Directory</a>
                        <a href="/categories" className="text-sm text-gray-500 hover:text-primary">Browse Categories</a>
                    </div>
                </div>
            </footer>
        </div>
    );
}
