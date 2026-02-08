import { getPostBySlug, getAllPosts } from '@/lib/mdx';
import { MDXRemote } from 'next-mdx-remote/rsc';
import Link from 'next/link';
import { notFound } from 'next/navigation';

export async function generateStaticParams() {
    const posts = getAllPosts('services');
    return posts.map((post) => ({
        slug: post.slug,
    }));
}

export default function ServicePage({ params }: { params: { slug: string } }) {
    try {
        const { metadata, content } = getPostBySlug(params.slug, 'services');

        return (
            <article className="container max-w-3xl py-12 mx-auto">
                <div className="mb-8">
                    <Link
                        href="/"
                        className="text-sm text-muted-foreground hover:text-primary transition-colors"
                    >
                        ← Back to Home
                    </Link>
                </div>

                <header className="mb-12">
                    <h1 className="text-4xl font-bold tracking-tight mb-4">{metadata.title}</h1>
                    {metadata.description && (
                        <p className="text-xl text-muted-foreground">{metadata.description}</p>
                    )}
                </header>

                <div className="prose prose-lg dark:prose-invert max-w-none">
                    <MDXRemote source={content} />
                </div>
            </article>
        );
    } catch (error) {
        notFound();
    }
}
