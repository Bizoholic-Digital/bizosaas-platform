'use client';

import React from 'react';
import { ConnectorsContent } from '@/components/ConnectorsContent';
import { PageHeader } from '@/components/dashboard/PageHeader';
import { useSearchParams } from 'next/navigation';

export default function AdminConnectorsPage() {
    const searchParams = useSearchParams();
    const activeCategory = searchParams.get('category');

    const categoryTitles: Record<string, string> = {
        crm: 'CRM & Marketing Automation',
        cms: 'Content Management Systems',
        ecommerce: 'E-commerce Platforms',
        analytics: 'Analytics & Search Console',
        marketing: 'Digital Marketing & Ads',
        all: 'All Data Connectors'
    };

    const categoryDescription: Record<string, string> = {
        crm: 'Manage your sales pipelines, contacts, and marketing automation.',
        cms: 'Connect your websites and blogs to sync content and media.',
        ecommerce: 'Sync products, orders, and customers from your online stores.',
        analytics: 'Monitor your website performance and SEO intelligence.',
        marketing: 'Manage your ad campaigns and social media presence.',
        all: 'Manage your integrations with external CMS, CRM, and E-commerce platforms.'
    };

    const currentTitle = activeCategory ? (categoryTitles[activeCategory] || 'Connectors') : 'Data Connectors';
    const currentDesc = activeCategory ? (categoryDescription[activeCategory] || 'Manage your integrations.') : 'Manage your integrations with external CMS, CRM, and E-commerce platforms.';

    return (
        <div className="flex flex-col min-h-full bg-slate-50 dark:bg-slate-950 p-6 space-y-6">
            <PageHeader
                title={currentTitle}
                description={currentDesc}
            />
            <ConnectorsContent />
        </div>
    );
}
