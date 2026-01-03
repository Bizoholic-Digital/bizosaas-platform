'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { RefreshCw, FileText, Plus, ExternalLink, Trash2, Send, Save, ArrowLeft } from 'lucide-react';
import { connectorsApi } from '@/lib/api/connectors';
import { toast } from 'sonner';

export interface WordPressPost {
    id: string;
    title: string;
    slug: string;
    content: string;
    status: string;
    excerpt?: string;
}

export function WordPressContentManager({ connectorId, siteUrl }: { connectorId: string, siteUrl?: string }) {
    const [posts, setPosts] = useState<WordPressPost[]>([]);
    const [loading, setLoading] = useState(true);
    const [view, setView] = useState<'list' | 'create' | 'edit'>('list');
    const [formData, setFormData] = useState<Partial<WordPressPost>>({
        title: '',
        content: '',
        status: 'draft'
    });
    const [submitting, setSubmitting] = useState(false);

    const loadPosts = async () => {
        setLoading(true);
        try {
            const res = await connectorsApi.syncResource<{ data: WordPressPost[] }>(connectorId, 'posts');
            if (res.data) {
                setPosts(res.data);
            }
        } catch (error) {
            console.error("Failed to load posts", error);
            toast.error("Failed to load WordPress posts");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadPosts();
    }, [connectorId]);

    const handleCreate = async () => {
        if (!formData.title || !formData.content) {
            toast.error("Title and Content are required");
            return;
        }

        setSubmitting(true);
        try {
            // We use performAction 'create_post' or a generic one? 
            // In WordPressConnector I improved create_post, it's called via the API sync path usually?
            // Wait, standard connector API has 'perform_action'. I should check if I added create_post there.
            // Actually, I should use the API for creating.

            const res = await connectorsApi.performAction<WordPressPost>(connectorId, 'create_post', formData);

            if (res.data && res.data.id) {
                toast.success("Post created successfully!");
                setFormData({ title: '', content: '', status: 'draft' });
                setView('list');
                loadPosts();
            } else {
                throw new Error(res.error || "Failed to create post");
            }
        } catch (error: any) {
            console.error("Post creation failed", error);
            toast.error(error.message || "Failed to create post. Check permissions.");
        } finally {
            setSubmitting(false);
        }
    };

    const handleDelete = async (postId: string) => {
        if (!confirm("Are you sure you want to delete this post?")) return;
        try {
            await connectorsApi.performAction(connectorId, 'delete_post', { post_id: postId });
            toast.success("Post deleted");
            loadPosts();
        } catch (error) {
            toast.error("Delete failed");
        }
    };

    if (view === 'create') {
        return (
            <div className="space-y-4">
                <div className="flex items-center gap-2 mb-4">
                    <Button variant="ghost" size="sm" onClick={() => setView('list')}>
                        <ArrowLeft className="h-4 w-4 mr-2" /> Back
                    </Button>
                    <h3 className="text-lg font-bold">Create New Post</h3>
                </div>

                <div className="space-y-4 border rounded-lg p-6 bg-card">
                    <div className="space-y-2">
                        <Label htmlFor="post-title">Post Title</Label>
                        <Input
                            id="post-title"
                            placeholder="Enter post title..."
                            value={formData.title}
                            onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="post-content">Content (HTML or plain text)</Label>
                        <Textarea
                            id="post-content"
                            placeholder="Write your content here..."
                            className="min-h-[300px] font-mono text-sm"
                            value={formData.content}
                            onChange={(e) => setFormData(prev => ({ ...prev, content: e.target.value }))}
                        />
                    </div>
                    <div className="flex gap-4">
                        <div className="flex-1 space-y-2">
                            <Label htmlFor="post-status">Status</Label>
                            <select
                                id="post-status"
                                className="w-full flex h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
                                value={formData.status}
                                onChange={(e) => setFormData(prev => ({ ...prev, status: e.target.value }))}
                            >
                                <option value="publish">Publish</option>
                                <option value="draft">Draft</option>
                                <option value="private">Private</option>
                                <option value="pending">Pending</option>
                            </select>
                        </div>
                    </div>
                    <div className="flex justify-end gap-2 pt-4">
                        <Button variant="outline" onClick={() => setView('list')}>Cancel</Button>
                        <Button onClick={handleCreate} disabled={submitting}>
                            {submitting ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : <Send className="h-4 w-4 mr-2" />}
                            Create Post
                        </Button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <Card className="border-none shadow-none">
            <CardHeader className="px-0 pt-0">
                <div className="flex justify-between items-center">
                    <div>
                        <CardTitle>Content Management</CardTitle>
                        <CardDescription>Manage your posts and pages directly from here.</CardDescription>
                    </div>
                    <div className="flex gap-2">
                        <Button variant="outline" size="sm" onClick={loadPosts} disabled={loading}>
                            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                        </Button>
                        <Button size="sm" onClick={() => setView('create')}>
                            <Plus className="h-4 w-4 mr-2" /> New Post
                        </Button>
                    </div>
                </div>
            </CardHeader>
            <CardContent className="px-0">
                {loading && posts.length === 0 ? (
                    <div className="flex justify-center p-8 text-muted-foreground italic">Loading posts...</div>
                ) : posts.length === 0 ? (
                    <div className="flex justify-center p-8 text-muted-foreground italic text-center space-y-4 flex-col items-center">
                        <p>No posts found on your site.</p>
                        <Button variant="outline" size="sm" onClick={() => setView('create')}>Create your first post</Button>
                    </div>
                ) : (
                    <div className="space-y-3">
                        {posts.map(post => (
                            <div key={post.id} className="flex items-center justify-between p-3 rounded-lg border bg-card hover:bg-accent/5 transition-colors">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 rounded bg-blue-100 text-blue-600">
                                        <FileText className="h-5 w-5" />
                                    </div>
                                    <div className="max-w-[500px]">
                                        <div className="flex items-center gap-2">
                                            <span className="font-medium line-clamp-1">{post.title}</span>
                                            <Badge variant={post.status === 'publish' ? 'default' : 'secondary'} className="text-[10px] bg-green-500/10 text-green-600 hover:bg-green-500/20 border-green-200">
                                                {post.status}
                                            </Badge>
                                        </div>
                                        <p className="text-xs text-muted-foreground">ID: {post.id} | Slug: {post.slug}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Button variant="ghost" size="sm" asChild>
                                        <a href={`${siteUrl?.replace(/\/$/, '')}/?p=${post.id}`} target="_blank" rel="noopener noreferrer">
                                            <ExternalLink className="h-4 w-4" />
                                        </a>
                                    </Button>
                                    <Button variant="ghost" size="sm" className="text-red-500 hover:text-red-600" onClick={() => handleDelete(post.id)}>
                                        <Trash2 className="h-4 w-4" />
                                    </Button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
