'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { FileText, File, Image, Loader2, Plus, Edit, Trash2, MoreVertical, ExternalLink, Zap } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';

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

interface Plugin {
    id: string;
    name: string;
    slug: string;
    version: string;
    status: 'active' | 'inactive';
    description?: string;
    author?: string;
}

export default function CMSPage() {
    const { isConnected, isLoading: statusLoading, connector } = useConnectorStatus('wordpress', 'cms');
    const [posts, setPosts] = useState<Post[]>([]);
    const [pages, setPages] = useState<Page[]>([]);
    const [plugins, setPlugins] = useState<Plugin[]>([]);
    const [isLoadingData, setIsLoadingData] = useState(false);

    const [activeTab, setActiveTab] = useState('posts');
    const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [selectedItem, setSelectedItem] = useState<any>(null);
    const [formData, setFormData] = useState({
        title: '',
        content: '',
        status: 'draft',
        slug: ''
    });

    useEffect(() => {
        if (isConnected) {
            loadData();
        }
    }, [isConnected]);

    const loadData = async () => {
        setIsLoadingData(true);
        try {
            const [postsData, pagesData, pluginsData] = await Promise.all([
                brainApi.cms.getPosts().catch(() => []),
                brainApi.cms.getPages().catch(() => []),
                brainApi.cms.getPlugins().catch(() => [])
            ]);

            setPosts(postsData || []);
            setPages(pagesData || []);
            setPlugins(pluginsData || []);
        } catch (error) {
            console.error('Failed to load CMS data:', error);
            toast.error('Failed to load CMS data');
        } finally {
            setIsLoadingData(false);
        }
    };

    const handleCreate = async () => {
        try {
            if (activeTab === 'posts') {
                await brainApi.cms.createPost(formData);
                toast.success('Post created successfully');
            } else {
                await brainApi.cms.createPage(formData);
                toast.success('Page created successfully');
            }
            setIsCreateDialogOpen(false);
            resetForm();
            loadData();
        } catch (error) {
            toast.error('Failed to create content');
        }
    };

    const handleUpdate = async () => {
        try {
            if (activeTab === 'posts') {
                await brainApi.cms.updatePost(selectedItem.id, formData);
                toast.success('Post updated successfully');
            } else {
                await brainApi.cms.updatePage(selectedItem.id, formData);
                toast.success('Page updated successfully');
            }
            setIsCreateDialogOpen(false);
            resetForm();
            loadData();
        } catch (error) {
            toast.error('Failed to update content');
        }
    };

    const handleDelete = async (id: string, type: 'posts' | 'pages') => {
        if (!confirm('Are you sure you want to delete this content?')) return;

        try {
            if (type === 'posts') {
                await brainApi.cms.deletePost(id);
            } else {
                await brainApi.cms.deletePage(id);
            }
            toast.success('Content deleted successfully');
            loadData();
        } catch (error) {
            toast.error('Failed to delete content');
        }
    };

    const resetForm = () => {
        setFormData({ title: '', content: '', status: 'draft', slug: '' });
        setIsEditing(false);
        setSelectedItem(null);
    };

    const openEdit = (item: any) => {
        setSelectedItem(item);
        setFormData({
            title: item.title,
            content: item.content || '',
            status: item.status,
            slug: item.slug
        });
        setIsEditing(true);
        setIsCreateDialogOpen(true);
    };

    const handleTogglePlugin = async (slug: string, currentStatus: string) => {
        const newActive = currentStatus !== 'active';
        try {
            await brainApi.cms.togglePlugin(slug, newActive);
            toast.success(`Plugin ${newActive ? 'activated' : 'deactivated'} successfully`);
            loadData();
        } catch (error) {
            toast.error('Failed to toggle plugin');
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
                        <CardTitle className="text-sm font-medium">Plugins</CardTitle>
                        <Zap className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{plugins.filter(p => p.status === 'active').length}/{plugins.length}</div>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle>Content</CardTitle>
                        <Dialog open={isCreateDialogOpen} onOpenChange={(open) => {
                            setIsCreateDialogOpen(open);
                            if (!open) resetForm();
                        }}>
                            <DialogTrigger asChild>
                                <Button disabled={activeTab === 'plugins'}>
                                    <Plus className="w-4 h-4 mr-2" />
                                    New {activeTab === 'posts' ? 'Post' : activeTab === 'pages' ? 'Page' : 'Content'}
                                </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-[600px]">
                                <DialogHeader>
                                    <DialogTitle>{isEditing ? 'Edit' : 'Create New'} {activeTab === 'posts' ? 'Post' : 'Page'}</DialogTitle>
                                </DialogHeader>
                                <div className="space-y-4 py-4">
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium">Title</label>
                                        <Input
                                            placeholder="Enter title..."
                                            value={formData.title}
                                            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium">Slug</label>
                                        <Input
                                            placeholder="url-friendly-slug"
                                            value={formData.slug}
                                            onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium">Status</label>
                                        <Select
                                            value={formData.status}
                                            onValueChange={(val) => setFormData({ ...formData, status: val })}
                                        >
                                            <SelectTrigger>
                                                <SelectValue />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="publish">Published</SelectItem>
                                                <SelectItem value="draft">Draft</SelectItem>
                                                <SelectItem value="pending">Pending</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium">Content</label>
                                        <Textarea
                                            placeholder="Write your content here..."
                                            className="min-h-[200px]"
                                            value={formData.content}
                                            onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                                        />
                                    </div>
                                </div>
                                <DialogFooter>
                                    <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>Cancel</Button>
                                    <Button onClick={isEditing ? handleUpdate : handleCreate}>
                                        {isEditing ? 'Update' : 'Create'}
                                    </Button>
                                </DialogFooter>
                            </DialogContent>
                        </Dialog>
                    </div>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="posts" className="w-full" onValueChange={setActiveTab}>
                        <TabsList className="grid w-full grid-cols-3 mb-4">
                            <TabsTrigger value="posts">
                                <FileText className="w-4 h-4 mr-2" />
                                Posts ({posts.length})
                            </TabsTrigger>
                            <TabsTrigger value="pages">
                                <File className="w-4 h-4 mr-2" />
                                Pages ({pages.length})
                            </TabsTrigger>
                            <TabsTrigger value="plugins">
                                <Zap className="w-4 h-4 mr-2" />
                                Plugins ({plugins.length})
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
                                        <div className="flex items-center gap-4">
                                            <Badge variant={post.status === 'publish' ? 'default' : 'secondary'}>
                                                {post.status}
                                            </Badge>
                                            <DropdownMenu>
                                                <DropdownMenuTrigger asChild>
                                                    <Button variant="ghost" size="icon">
                                                        <MoreVertical className="w-4 h-4" />
                                                    </Button>
                                                </DropdownMenuTrigger>
                                                <DropdownMenuContent align="end">
                                                    <DropdownMenuItem onClick={() => openEdit(post)}>
                                                        <Edit className="w-4 h-4 mr-2" /> Edit
                                                    </DropdownMenuItem>
                                                    <DropdownMenuItem className="text-red-600" onClick={() => handleDelete(post.id, 'posts')}>
                                                        <Trash2 className="w-4 h-4 mr-2" /> Delete
                                                    </DropdownMenuItem>
                                                </DropdownMenuContent>
                                            </DropdownMenu>
                                        </div>
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
                                        <div className="flex items-center gap-4">
                                            <Badge variant={page.status === 'publish' ? 'default' : 'secondary'}>
                                                {page.status}
                                            </Badge>
                                            <DropdownMenu>
                                                <DropdownMenuTrigger asChild>
                                                    <Button variant="ghost" size="icon">
                                                        <MoreVertical className="w-4 h-4" />
                                                    </Button>
                                                </DropdownMenuTrigger>
                                                <DropdownMenuContent align="end">
                                                    <DropdownMenuItem onClick={() => openEdit(page)}>
                                                        <Edit className="w-4 h-4 mr-2" /> Edit
                                                    </DropdownMenuItem>
                                                    <DropdownMenuItem className="text-red-600" onClick={() => handleDelete(page.id, 'pages')}>
                                                        <Trash2 className="w-4 h-4 mr-2" /> Delete
                                                    </DropdownMenuItem>
                                                </DropdownMenuContent>
                                            </DropdownMenu>
                                        </div>
                                    </div>
                                ))
                            )}
                        </TabsContent>
                        <TabsContent value="plugins" className="space-y-4">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : plugins.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">No plugins found</div>
                            ) : (
                                <div className="grid grid-cols-1 gap-4">
                                    {plugins.map((plugin) => (
                                        <div key={plugin.id} className="flex items-center justify-between p-4 rounded-lg border bg-card hover:shadow-sm transition-shadow">
                                            <div className="flex items-center gap-4">
                                                <div className={`p-2 rounded-lg ${plugin.status === 'active' ? 'bg-blue-50 text-blue-600' : 'bg-slate-50 text-slate-400'}`}>
                                                    <Zap className="w-5 h-5" />
                                                </div>
                                                <div>
                                                    <div className="flex items-center gap-2">
                                                        <p className="font-semibold text-slate-900 dark:text-white">{plugin.name}</p>
                                                        <span className="text-xs text-muted-foreground text-opacity-70">v{plugin.version}</span>
                                                    </div>
                                                    <p className="text-sm text-muted-foreground line-clamp-1 max-w-md">{plugin.description?.replace(/<[^>]*>?/gm, '')}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-4">
                                                <Badge variant={plugin.status === 'active' ? 'default' : 'secondary'} className={plugin.status === 'active' ? 'bg-green-100 text-green-700 hover:bg-green-100 border-none' : ''}>
                                                    {plugin.status === 'active' ? 'Active' : 'Inactive'}
                                                </Badge>
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    onClick={() => handleTogglePlugin(plugin.id, plugin.status)}
                                                >
                                                    {plugin.status === 'active' ? 'Deactivate' : 'Activate'}
                                                </Button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </TabsContent>
                    </Tabs>
                </CardContent>
            </Card>
        </div>
    );
}
