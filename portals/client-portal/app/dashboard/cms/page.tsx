'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { FileText, File, Image, Loader2, Plus } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';

interface Post {
    id: string;
    title: string;
    slug: string;
    status: string;
    excerpt?: string;
}

interface Page {
    id: string;
    title: string;
    slug: string;
    status: string;
}

export default function CMSPage() {
    const { isConnected, isLoading: statusLoading, connector } = useConnectorStatus('wordpress');
    const [posts, setPosts] = useState<Post[]>([]);
    const [pages, setPages] = useState<Page[]>([]);
    const [isLoadingData, setIsLoadingData] = useState(false);

    useEffect(() => {
        if (isConnected) {
            loadData();
        }
    }, [isConnected]);

    const loadData = async () => {
        setIsLoadingData(true);
        try {
            const [postsData, pagesData] = await Promise.all([
                brainApi.cms.getPosts().catch(() => []),
                brainApi.cms.getPages().catch(() => [])
            ]);

            setPosts(postsData || []);
            setPages(pagesData || []);
        } catch (error) {
            console.error('Failed to load CMS data:', error);
        } finally {
            setIsLoadingData(false);
        }
    };

    if (statusLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    if (!isConnected) {
        return (
            <ConnectionPrompt
                serviceName="WordPress"
                serviceIcon={<FileText className="w-8 h-8 text-blue-600" />}
                description="Connect your WordPress site to manage posts, pages, and media."
            />
        );
    }

    return (
        <div className="p-6 space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Content Management</h1>
                    <p className="text-muted-foreground mt-1">Manage your WordPress content</p>
                </div>
                <Badge variant="outline" className="bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 border-green-200 dark:border-green-800">
                    <div className="w-2 h-2 rounded-full bg-green-500 mr-2" />
                    Connected to {connector?.name}
                </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Total Posts</CardTitle>
                        <FileText className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{posts.length}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Total Pages</CardTitle>
                        <File className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{pages.length}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Media</CardTitle>
                        <Image className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">-</div>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle>Content</CardTitle>
                        <Button>
                            <Plus className="w-4 h-4 mr-2" />
                            New Post
                        </Button>
                    </div>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="posts" className="w-full">
                        <TabsList className="grid w-full grid-cols-2 mb-4">
                            <TabsTrigger value="posts">
                                <FileText className="w-4 h-4 mr-2" />
                                Posts ({posts.length})
                            </TabsTrigger>
                            <TabsTrigger value="pages">
                                <File className="w-4 h-4 mr-2" />
                                Pages ({pages.length})
                            </TabsTrigger>
                        </TabsList>

                        <TabsContent value="posts" className="space-y-2">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : posts.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">No posts found</div>
                            ) : (
                                posts.map((post) => (
                                    <div key={post.id} className="flex items-center justify-between p-4 rounded-lg border hover:bg-slate-50 dark:hover:bg-slate-800">
                                        <div className="flex items-center gap-4">
                                            <FileText className="w-5 h-5 text-blue-600" />
                                            <div>
                                                <p className="font-medium text-slate-900 dark:text-white">{post.title}</p>
                                                <p className="text-sm text-muted-foreground">/{post.slug}</p>
                                            </div>
                                        </div>
                                        <Badge variant={post.status === 'publish' ? 'default' : 'secondary'}>
                                            {post.status}
                                        </Badge>
                                    </div>
                                ))
                            )}
                        </TabsContent>

                        <TabsContent value="pages" className="space-y-2">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : pages.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">No pages found</div>
                            ) : (
                                pages.map((page) => (
                                    <div key={page.id} className="flex items-center justify-between p-4 rounded-lg border hover:bg-slate-50 dark:hover:bg-slate-800">
                                        <div className="flex items-center gap-4">
                                            <File className="w-5 h-5 text-green-600" />
                                            <div>
                                                <p className="font-medium text-slate-900 dark:text-white">{page.title}</p>
                                                <p className="text-sm text-muted-foreground">/{page.slug}</p>
                                            </div>
                                        </div>
                                        <Badge variant={page.status === 'publish' ? 'default' : 'secondary'}>
                                            {page.status}
                                        </Badge>
                                    </div>
                                ))
                            )}
                        </TabsContent>
                    </Tabs>
                </CardContent>
            </Card>
        </div>
    );
}
