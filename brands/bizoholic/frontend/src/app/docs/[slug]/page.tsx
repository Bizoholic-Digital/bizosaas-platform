import Link from 'next/link';
import { getPostBySlug } from '@/lib/mdx';
import { MDXRemote } from 'next-mdx-remote/rsc';
import { notFound } from 'next/navigation';

export function generateStaticParams() {
    // In a real app we'd fetch all docs slugs here
    // For now return empty or standard ones
    return [];
}

export default function DocPage({ params }: { params: { slug: string } }) {
    try {
        const { metadata, content } = getPostBySlug(params.slug, 'docs');

        return (
            <div className="container max-w-7xl mx-auto py-12 flex gap-12">
                <aside className="w-64 hidden lg:block border-r pr-8">
                    <nav className="space-y-4">
                        <h3 className="font-semibold text-lg">Documentation</h3>
                        <ul className="space-y-2">
                            <li>
                                <Link href="/docs/welcome" className="text-muted-foreground hover:text-primary">
                                    Welcome
                                </Link>
                            </li>
                            <li>
                                <Link href="/docs/getting-started" className="text-muted-foreground hover:text-primary">
                                    Getting Started
                                </Link>
                            </li>
                        </ul>
                    </nav>
                </aside>

                <article className="flex-1 min-w-0">
                    <header className="mb-8">
                        <h1 className="text-3xl font-bold tracking-tight mb-2">{metadata.title}</h1>
                        {metadata.description && (
                            <p className="text-lg text-muted-foreground">{metadata.description}</p>
                        )}
                    </header>

                    <div className="prose dark:prose-invert max-w-none">
                        <MDXRemote source={content} />
                    </div>
                </article>
            </div>
        );
    } catch (error) {
        notFound();
    }
}
