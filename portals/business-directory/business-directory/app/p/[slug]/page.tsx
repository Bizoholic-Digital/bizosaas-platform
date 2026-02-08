import React from 'react';
import { Header } from '@/components/layout/header';

interface Props {
    params: Promise<{ slug: string }>;
}

export default async function ProductPage({ params }: Props) {
    const { slug } = await params;

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
            <Header />
            <main className="max-w-7xl mx-auto px-4 py-12">
                <h1 className="text-3xl font-bold capitalize mb-4">{slug.replace(/-/g, ' ')}</h1>
                <p className="text-muted-foreground">Product details.</p>
                <div className="mt-8 p-6 bg-white dark:bg-slate-900 rounded-lg border border-dashed text-center">
                    <p>Product functionality coming soon.</p>
                </div>
            </main>
        </div>
    );
}
