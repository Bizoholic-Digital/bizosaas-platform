'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

interface NewsPost {
    id: string;
    title: string;
    excerpt?: string;
    publishedAt?: string;
    slug?: string;
    coverImage?: string;
}

interface NewsSectionProps {
    posts: NewsPost[];
}

export function NewsSection({ posts }: NewsSectionProps) {
    if (!posts || posts.length === 0) {
        return (
            <div className="text-center py-12 bg-muted/20 rounded-xl">
                <h3 className="text-xl font-medium text-muted-foreground">More gaming news coming soon!</h3>
            </div>
        )
    }

    return (
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {posts.map((post) => (
                <article key={post.id} className="flex flex-col items-start justify-between bg-card border rounded-xl overflow-hidden hover:shadow-md transition-all">
                    <div className="relative w-full aspect-video bg-muted">
                        {/* Image placeholder or actual image if available */}
                        <div className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                            📰
                        </div>
                    </div>
                    <div className="p-6">
                        <div className="flex items-center gap-x-4 text-xs">
                            <time dateTime={post.publishedAt} className="text-muted-foreground">
                                {post.publishedAt ? new Date(post.publishedAt).toLocaleDateString() : 'Recently'}
                            </time>
                            <span className="relative z-10 rounded-full bg-accent px-3 py-1.5 font-medium text-accent-foreground">
                                Esports
                            </span>
                        </div>
                        <div className="group relative">
                            <h3 className="mt-3 text-lg font-semibold leading-6 text-foreground group-hover:text-primary transition-colors">
                                <Link href={`/news/${post.slug || '#'}`}>
                                    <span className="absolute inset-0" />
                                    {post.title}
                                </Link>
                            </h3>
                            <p className="mt-5 line-clamp-3 text-sm leading-6 text-muted-foreground">
                                {post.excerpt || 'Read the full story to learn more about this update...'}
                            </p>
                        </div>
                    </div>
                </article>
            ))}
        </div>
    );
}
