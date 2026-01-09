'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { FileText, File, Image as ImageIcon, Loader2, Plus, Edit, Trash2, MoreVertical, ExternalLink, FolderOpen, Upload, Package, Power, PowerOff, Download } from 'lucide-react';
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
    view_count?: number;
}

interface Category {
    id: string;
    name: string;
    slug: string;
    count: number;
}

interface MediaItem {
    id: string;
    title: string;
    source_url: string;
    mime_type: string;
}

interface Plugin {
    id: string;
    name: string;
    description: string;
    status: string; // active, inactive
    version: string;
    author: string;
    icon?: string;
    installed: boolean;
}

const RECOMMENDED_PLUGINS = [
    { id: 'woocommerce', name: 'WooCommerce', description: 'eCommerce for WordPress', icon: 'https://ps.w.org/woocommerce/assets/icon-128x128.png' },
    { id: 'elementor', name: 'Elementor', description: 'The most advanced frontend drag & drop page builder', icon: 'https://ps.w.org/elementor/assets/icon-128x128.png' },
    { id: 'wordpress-seo', name: 'Yoast SEO', description: 'Improve your WordPress SEO', icon: 'https://ps.w.org/wordpress-seo/assets/icon-128x128.png' },
    { id: 'contact-form-7', name: 'Contact Form 7', description: 'Just another contact form plugin', icon: 'https://ps.w.org/contact-form-7/assets/icon-128x128.png' }
];

export default function CMSPage() {
    const { isConnected, isLoading: statusLoading, connector } = useConnectorStatus('wordpress', 'cms');
    const [posts, setPosts] = useState<Post[]>([]);
    const [pages, setPages] = useState<Page[]>([]);
    const [categories, setCategories] = useState<Category[]>([]);
    const [media, setMedia] = useState<MediaItem[]>([]);
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
        slug: '',
        description: '', // for categories
        file: null as File | null
    });

    useEffect(() => {
        if (isConnected) {
            loadData();
        }
    }, [isConnected]);

    const loadData = async () => {
        setIsLoadingData(true);
        try {
            const [postsData, pagesData, categoriesData, mediaData, pluginsData] = await Promise.all([
                brainApi.cms.getPosts().catch(() => []),
                brainApi.cms.getPages().catch(() => []),
                brainApi.cms.getCategories().catch(() => []),
                brainApi.cms.listMedia().catch(() => []),
                brainApi.cms.getPlugins().catch(() => [])
            ]);

            setPosts(postsData || []);
            setPages(pagesData || []);
            setCategories(categoriesData || []);
            setMedia(mediaData || []);
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
            } else if (activeTab === 'pages') {
                await brainApi.cms.createPage(formData);
                toast.success('Page created successfully');
            } else if (activeTab === 'categories') {
                await brainApi.cms.createCategory(formData);
                toast.success('Category created successfully');
            } else if (activeTab === 'media') {
                if (formData.file) {
                    const data = new FormData();
                    data.append('file', formData.file);
                    // data.append('title', formData.title);
                    await brainApi.cms.uploadMedia(data);
                    toast.success('Media uploaded successfully');
                } else {
                    toast.error('Please select a file');
                    return;
                }
            }
            setIsCreateDialogOpen(false);
            resetForm();
            loadData();
        } catch (error) {
            toast.error('Failed to create content');
            console.error(error);
        }
    };

    const handleUpdate = async () => {
        try {
            if (activeTab === 'posts') {
                await brainApi.cms.updatePost(selectedItem.id, formData);
                toast.success('Post updated successfully');
            } else if (activeTab === 'pages') {
                await brainApi.cms.updatePage(selectedItem.id, formData);
                toast.success('Page updated successfully');
            } else if (activeTab === 'categories') {
                await brainApi.cms.updateCategory(selectedItem.id, formData);
                toast.success('Category updated successfully');
            }
            // Media update not supported deeply yet
            setIsCreateDialogOpen(false);
            resetForm();
            loadData();
        } catch (error) {
            toast.error('Failed to update content');
        }
    };

    const handleDelete = async (id: string, type: 'posts' | 'pages' | 'categories' | 'media') => {
        if (!confirm('Are you sure you want to delete this content?')) return;

        try {
            if (type === 'posts') {
                await brainApi.cms.deletePost(id);
            } else if (type === 'pages') {
                await brainApi.cms.deletePage(id);
            } else if (type === 'categories') {
                await brainApi.cms.deleteCategory(id);
            } else if (type === 'media') {
                await brainApi.cms.deleteMedia(id);
            }
            toast.success('Content deleted successfully');
            loadData();
        } catch (error) {
            toast.error('Failed to delete content');
        }
    };

    const togglePlugin = async (slug: string, currentStatus: string) => {
        try {
            if (currentStatus === 'active') {
                await brainApi.cms.deactivatePlugin(slug);
                toast.success('Plugin deactivated');
            } else {
                await brainApi.cms.activatePlugin(slug);
                toast.success('Plugin activated');
            }
            loadData();
        } catch (error) {
            toast.error('Failed to update plugin status');
        }
    };

    const installPlugin = async (slug: string) => {
        try {
            await brainApi.cms.installPlugin(slug);
            toast.success('Plugin installed successfully');
            loadData();
        } catch (error) {
            toast.error('Failed to install plugin');
        }
    };

    const resetForm = () => {
        setFormData({ title: '', content: '', status: 'draft', slug: '', description: '', file: null });
        setIsEditing(false);
        setSelectedItem(null);
    };

    const openEdit = (item: any) => {
        setSelectedItem(item);
        setFormData({
            title: item.title || item.name || '',
            content: item.content || '',
            status: item.status || 'draft',
            slug: item.slug || '',
            description: item.description || '',
            file: null
        });
        setIsEditing(true);
        setIsCreateDialogOpen(true);
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

            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
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
                        <CardTitle className="text-sm font-medium">Categories</CardTitle>
                        <FolderOpen className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{categories.length}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Media</CardTitle>
                        <ImageIcon className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{media.length}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Plugins</CardTitle>
                        <Package className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{plugins.length}</div>
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
                                <Button>
                                    <Plus className="w-4 h-4 mr-2" />
                                    New {activeTab === 'posts' ? 'Post' : activeTab === 'pages' ? 'Page' : activeTab === 'categories' ? 'Category' : 'Media'}
                                </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-[600px]">
                                <DialogHeader>
                                    <DialogTitle>{isEditing ? 'Edit' : 'Create New'} {activeTab.slice(0, -1)}</DialogTitle>
                                </DialogHeader>
                                <div className="space-y-4 py-4">
                                    {activeTab === 'media' ? (
                                        <>
                                            <div className="space-y-2">
                                                <label className="text-sm font-medium">File</label>
                                                <Input
                                                    type="file"
                                                    onChange={(e) => {
                                                        const file = e.target.files?.[0];
                                                        if (file) setFormData({ ...formData, file: file });
                                                    }}
                                                />
                                            </div>
                                            <div className="space-y-2">
                                                <label className="text-sm font-medium">Title (Optional)</label>
                                                <Input
                                                    placeholder="Enter media title..."
                                                    value={formData.title}
                                                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                                />
                                            </div>
                                        </>
                                    ) : (
                                        <>
                                            <div className="space-y-2">
                                                <label className="text-sm font-medium">Title/Name</label>
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
                                            {activeTab !== 'categories' && (
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
                                            )}
                                            <div className="space-y-2">
                                                <label className="text-sm font-medium">{activeTab === 'categories' ? 'Description' : 'Content'}</label>
                                                <Textarea
                                                    placeholder={activeTab === 'categories' ? "Enter description..." : "Write your content here..."}
                                                    className="min-h-[200px]"
                                                    value={activeTab === 'categories' ? formData.description : formData.content}
                                                    onChange={(e) => setFormData(activeTab === 'categories' ? { ...formData, description: e.target.value } : { ...formData, content: e.target.value })}
                                                />
                                            </div>
                                        </>
                                    )}
                                </div>
                                <DialogFooter>
                                    <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>Cancel</Button>
                                    <Button onClick={isEditing ? handleUpdate : handleCreate}>
                                        {isEditing ? 'Update' : activeTab === 'media' ? 'Upload' : 'Create'}
                                    </Button>
                                </DialogFooter>
                            </DialogContent>
                        </Dialog>
                    </div>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="posts" className="w-full" onValueChange={setActiveTab}>
                        <TabsList className="grid w-full grid-cols-5 mb-4">
                            <TabsTrigger value="posts">
                                <FileText className="w-4 h-4 mr-2" />
                                Posts ({posts.length})
                            </TabsTrigger>
                            <TabsTrigger value="pages">
                                <File className="w-4 h-4 mr-2" />
                                Pages ({pages.length})
                            </TabsTrigger>
                            <TabsTrigger value="categories">
                                <FolderOpen className="w-4 h-4 mr-2" />
                                Categories ({categories.length})
                            </TabsTrigger>
                            <TabsTrigger value="media">
                                <ImageIcon className="w-4 h-4 mr-2" />
                                Media ({media.length})
                            </TabsTrigger>
                            <TabsTrigger value="plugins">
                                <Package className="w-4 h-4 mr-2" />
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

                        <TabsContent value="categories" className="space-y-2">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : categories.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">No categories found</div>
                            ) : (
                                categories.map((cat) => (
                                    <div key={cat.id} className="flex items-center justify-between p-4 rounded-lg border hover:bg-slate-50 dark:hover:bg-slate-800">
                                        <div className="flex items-center gap-4">
                                            <FolderOpen className="w-5 h-5 text-yellow-600" />
                                            <div>
                                                <p className="font-medium text-slate-900 dark:text-white">{cat.name}</p>
                                                <p className="text-sm text-muted-foreground">/{cat.slug} • {cat.count} items</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <DropdownMenu>
                                                <DropdownMenuTrigger asChild>
                                                    <Button variant="ghost" size="icon">
                                                        <MoreVertical className="w-4 h-4" />
                                                    </Button>
                                                </DropdownMenuTrigger>
                                                <DropdownMenuContent align="end">
                                                    <DropdownMenuItem onClick={() => openEdit(cat)}>
                                                        <Edit className="w-4 h-4 mr-2" /> Edit
                                                    </DropdownMenuItem>
                                                    <DropdownMenuItem className="text-red-600" onClick={() => handleDelete(cat.id, 'categories')}>
                                                        <Trash2 className="w-4 h-4 mr-2" /> Delete
                                                    </DropdownMenuItem>
                                                </DropdownMenuContent>
                                            </DropdownMenu>
                                        </div>
                                    </div>
                                ))
                            )}
                        </TabsContent>

                        <TabsContent value="media" className="space-y-4">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : media.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">No media found</div>
                            ) : (
                                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                                    {media.map((item) => (
                                        <div key={item.id} className="group relative aspect-square rounded-lg border bg-slate-100 dark:bg-slate-800 overflow-hidden hover:ring-2 hover:ring-blue-500 transition-all cursor-pointer">
                                            {item.mime_type.startsWith('image/') ? (
                                                <img src={item.source_url} alt={item.title} className="w-full h-full object-cover" />
                                            ) : (
                                                <div className="w-full h-full flex flex-col items-center justify-center p-4 text-center">
                                                    <File className="w-8 h-8 text-slate-400 mb-2" />
                                                    <p className="text-xs text-slate-500 truncate w-full">{item.title}</p>
                                                </div>
                                            )}

                                            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                                                <a href={item.source_url} target="_blank" rel="noopener noreferrer" className="p-2 bg-white rounded-full hover:bg-gray-100" onClick={(e) => e.stopPropagation()}>
                                                    <ExternalLink className="w-4 h-4 text-black" />
                                                </a>
                                                <button className="p-2 bg-white rounded-full hover:bg-red-50" onClick={(e) => { e.stopPropagation(); handleDelete(item.id, 'media'); }}>
                                                    <Trash2 className="w-4 h-4 text-red-600" />
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </TabsContent>

                        <TabsContent value="plugins" className="space-y-6">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : (
                                <>
                                    <div className="space-y-4">
                                        <h3 className="text-lg font-medium">Installed Plugins</h3>
                                        {plugins.length === 0 ? (
                                            <div className="text-center py-8 text-muted-foreground border rounded-lg border-dashed">No plugins installed</div>
                                        ) : (
                                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                                {plugins.map((plugin) => (
                                                    <div key={plugin.id} className="flex flex-col justify-between p-4 rounded-lg border bg-white dark:bg-slate-900 shadow-sm">
                                                        <div className="space-y-2">
                                                            <div className="flex items-start justify-between">
                                                                <div className="flex items-center gap-3">
                                                                    <div className="w-10 h-10 rounded bg-slate-100 flex items-center justify-center overflow-hidden">
                                                                        {plugin.icon ? <img src={plugin.icon} alt={plugin.name} className="w-full h-full object-cover" /> : <Package className="w-6 h-6 text-slate-400" />}
                                                                    </div>
                                                                    <div>
                                                                        <h4 className="font-semibold text-sm">{plugin.name}</h4>
                                                                        <p className="text-xs text-muted-foreground">v{plugin.version} by {plugin.author}</p>
                                                                    </div>
                                                                </div>
                                                                <Badge variant={plugin.status === 'active' ? 'default' : 'secondary'} className={plugin.status === 'active' ? 'bg-green-500 hover:bg-green-600' : ''}>
                                                                    {plugin.status}
                                                                </Badge>
                                                            </div>
                                                            <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2 min-h-[40px]">{plugin.description}</p>
                                                        </div>
                                                        <div className="flex items-center gap-2 mt-4 pt-4 border-t">
                                                            <Button
                                                                variant="outline"
                                                                size="sm"
                                                                className="flex-1"
                                                                onClick={() => togglePlugin(plugin.id, plugin.status)}
                                                            >
                                                                {plugin.status === 'active' ? (
                                                                    <><PowerOff className="w-3 h-3 mr-2" /> Deactivate</>
                                                                ) : (
                                                                    <><Power className="w-3 h-3 mr-2" /> Activate</>
                                                                )}
                                                            </Button>
                                                            <Button
                                                                variant="ghost"
                                                                size="icon"
                                                                className="h-8 w-8 text-red-500 hover:text-red-700 hover:bg-red-50"
                                                                onClick={() => {
                                                                    if (confirm('Are you sure you want to delete this plugin?')) {
                                                                        brainApi.cms.deletePlugin(plugin.id).then(() => {
                                                                            toast.success('Plugin deleted');
                                                                            loadData();
                                                                        }).catch(() => {
                                                                            toast.error('Failed to delete plugin');
                                                                        });
                                                                    }
                                                                }}
                                                            >
                                                                <Trash2 className="w-4 h-4" />
                                                            </Button>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>

                                    <div className="space-y-4">
                                        <h3 className="text-lg font-medium">Marketplace Recommendations</h3>
                                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                                            {RECOMMENDED_PLUGINS.map((plugin) => {
                                                const isInstalled = plugins.some(p => p.id === plugin.id || p.id.includes(plugin.id));
                                                return (
                                                    <div key={plugin.id} className="flex flex-col justify-between p-4 rounded-lg border hover:border-blue-500 transition-colors">
                                                        <div className="space-y-3">
                                                            <div className="w-12 h-12 rounded bg-slate-100 mx-auto flex items-center justify-center overflow-hidden">
                                                                <img src={plugin.icon} alt={plugin.name} className="w-full h-full object-cover" />
                                                            </div>
                                                            <div className="text-center">
                                                                <h4 className="font-semibold text-sm">{plugin.name}</h4>
                                                                <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{plugin.description}</p>
                                                            </div>
                                                        </div>
                                                        <Button
                                                            className="w-full mt-4"
                                                            variant={isInstalled ? "secondary" : "default"}
                                                            disabled={isInstalled}
                                                            onClick={() => installPlugin(plugin.id)}
                                                        >
                                                            {isInstalled ? 'Installed' : (
                                                                <><Download className="w-3 h-3 mr-2" /> Install</>
                                                            )}
                                                        </Button>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>
                                </>
                            )}
                        </TabsContent>
                    </Tabs>
                </CardContent>
            </Card>
        </div>
    );
}
