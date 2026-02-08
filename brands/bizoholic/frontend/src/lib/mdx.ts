import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const contentDirectory = path.join(process.cwd(), 'content');

export type PostType = 'pages' | 'services' | 'case-studies' | 'blog' | 'docs';

export interface PostMetadata {
    title: string;
    description?: string;
    date?: string;
    slug: string;
    [key: string]: any;
}

export interface Post {
    metadata: PostMetadata;
    content: string;
}

export function getPostBySlug(slug: string, type: PostType = 'pages'): Post {
    const realSlug = slug.replace(/\.mdx$/, '');
    const fullPath = path.join(contentDirectory, type, `${realSlug}.mdx`);
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data, content } = matter(fileContents);

    return {
        metadata: {
            ...data,
            slug: realSlug,
        } as PostMetadata,
        content,
    };
}

export function getAllPosts(type: PostType = 'pages'): PostMetadata[] {
    const dirPath = path.join(contentDirectory, type);

    if (!fs.existsSync(dirPath)) {
        return [];
    }

    const filenames = fs.readdirSync(dirPath);
    const posts = filenames.map((filename) => {
        const slug = filename.replace(/\.mdx$/, '');
        const fullPath = path.join(dirPath, filename);
        const fileContents = fs.readFileSync(fullPath, 'utf8');
        const { data } = matter(fileContents);

        return {
            ...data,
            slug,
        } as PostMetadata;
    });

    // Sort posts by date if available
    return posts.sort((a, b) => {
        if (a.date && b.date) {
            return a.date > b.date ? -1 : 1;
        }
        return 0;
    });
}
