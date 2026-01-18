import React from 'react';
import { Header } from '@/components/layout/header';
import Link from 'next/link';
import { Card, CardContent } from '@/components/ui/card';
import { businessAPI } from '@/lib/api';

export default async function AllCategoriesPage() {
    const categories = await businessAPI.getCategories();

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
            <Header />
            <main className="max-w-7xl mx-auto px-4 py-12">
                <h1 className="text-3xl font-bold mb-8">All Categories</h1>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {categories.map((category) => (
                        <Link key={category.id} href={`/c/${category.slug}`}>
                            <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
                                <CardContent className="p-6 text-center">
                                    <div className="text-4xl mb-4">{category.icon}</div>
                                    <h3 className="text-lg font-semibold mb-2">{category.name}</h3>
                                    <p className="text-sm text-muted-foreground mb-4">{category.description}</p>
                                    <span className="text-sm text-primary font-medium">
                                        {category.businessCount} businesses
                                    </span>
                                </CardContent>
                            </Card>
                        </Link>
                    ))}
                </div>
            </main>
        </div>
    );
}
