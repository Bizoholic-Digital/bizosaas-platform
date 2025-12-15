'use client';

import React, { useState, useEffect } from 'react';
import {
    FileText, MessageSquare, Image, Layout, Plus, Search,
    Filter, Edit, Trash2, Eye, MoreVertical, CheckCircle, XCircle, RefreshCw
} from 'lucide-react';
import { PageForm } from './PageForm'; // Ensure this component is updated later
import { PostForm } from './PostForm'; // Ensure this component is updated later
import { cmsApi, CMSPage, CMSPost, CMSMedia } from '@/lib/api/cms';
import { toast } from 'sonner';

interface CMSContentProps {
    activeTab: string;
}

export const CMSContent: React.FC<CMSContentProps> = ({ activeTab }) => {
    const [pages, setPages] = useState<CMSPage[]>([]);
    const [posts, setPosts] = useState<CMSPost[]>([]);
    const [media, setMedia] = useState<CMSMedia[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    // Modal states
    const [showPageModal, setShowPageModal] = useState(false);
    const [showPostModal, setShowPostModal] = useState(false);
    const [selectedItem, setSelectedItem] = useState<any>(null);

    useEffect(() => {
        fetchData();
    }, [activeTab]);

    const fetchData = async () => {
        setIsLoading(true);
        try {
            if (activeTab === 'cms-pages') {
                const res = await cmsApi.getPages();
                if (res.data) setPages(res.data);
            } else if (activeTab === 'cms-posts') {
                const res = await cmsApi.getPosts();
                if (res.data) setPosts(res.data);
            } else if (activeTab === 'cms-media') {
                const res = await cmsApi.getMedia();
                if (res.data) setMedia(res.data);
            }
        } catch (error) {
            console.error('Failed to fetch CMS data:', error);
            // Default to empty array on error
            setPages([]);
            setPosts([]);
            setMedia([]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreate = () => {
        setSelectedItem(null);
        if (activeTab === 'cms-pages') setShowPageModal(true);
        if (activeTab === 'cms-posts') setShowPostModal(true);
    };

    const handleEdit = (item: any) => {
        setSelectedItem(item);
        if (activeTab === 'cms-pages') setShowPageModal(true);
        if (activeTab === 'cms-posts') setShowPostModal(true);
    };

    const handleDelete = async (id: string, type: 'page' | 'post' | 'media') => {
        if (!confirm('Are you sure you want to delete this item?')) return;

        try {
            let res;
            if (type === 'page') {
                res = await cmsApi.deletePage(id);
            } else {
                // Implement deletePost/deleteMedia in API client later if needed
                console.warn("Delete not fully implemented for posts/media yet");
                return;
            }

            if (res.status === 200 || res.data) {
                toast.success("Item deleted successfully");
                fetchData();
            } else {
                toast.error("Failed to delete item");
            }
        } catch (error) {
            console.error('Failed to delete item:', error);
            toast.error("An error occurred while deleting");
        }
    };

    const renderPages = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Pages</h2>
                <button
                    onClick={handleCreate}
                    className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-primary/90 transition-colors"
                >
                    <Plus className="w-4 h-4" /> Create Page
                </button>
            </div>

            <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden shadow-sm">
                <div className="p-4 border-b border-gray-200 dark:border-gray-800 flex gap-4">
                    <div className="relative flex-1">
                        <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                        <Input
                            placeholder="Search pages..."
                            className="pl-10"
                        />
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50 dark:bg-gray-800/50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Title</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Last Updated</th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                            {isLoading ? (
                                <tr>
                                    <td colSpan={4} className="px-6 py-12 text-center text-gray-500">
                                        <Loader />
                                    </td>
                                </tr>
                            ) : pages.length === 0 ? (
                                <tr>
                                    <td colSpan={4} className="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                                        No pages found.
                                    </td>
                                </tr>
                            ) : (
                                pages.map((page) => (
                                    <tr key={page.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="text-sm font-medium text-gray-900 dark:text-white">{page.title}</div>
                                            <div className="text-sm text-gray-500 dark:text-gray-400">/{page.slug}</div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <StatusBadge status={page.status} />
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                            {page.updated_at ? new Date(page.updated_at).toLocaleDateString() : '-'}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <div className="flex items-center justify-end gap-2">
                                                <button onClick={() => handleEdit(page)} className="p-2 text-gray-400 hover:text-blue-600 rounded-full hover:bg-blue-50 dark:hover:bg-blue-900/20">
                                                    <Edit className="w-4 h-4" />
                                                </button>
                                                <button onClick={() => handleDelete(page.id, 'page')} className="p-2 text-gray-400 hover:text-red-600 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20">
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );

    const renderPosts = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Blog Posts</h2>
                <button
                    onClick={handleCreate}
                    className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-primary/90 transition-colors"
                >
                    <Plus className="w-4 h-4" /> Create Post
                </button>
            </div>
            {/* Similar table structure for posts - reusing pattern */}
            <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden shadow-sm">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50 dark:bg-gray-800/50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Title</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                            {isLoading ? (
                                <tr><td colSpan={3} className="px-6 py-12 text-center text-gray-500"><Loader /></td></tr>
                            ) : posts.length === 0 ? (
                                <tr><td colSpan={3} className="px-6 py-12 text-center text-gray-500">No posts found.</td></tr>
                            ) : (
                                posts.map((post) => (
                                    <tr key={post.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="text-sm font-medium text-gray-900 dark:text-white">{post.title}</div>
                                            <div className="text-sm text-gray-500 dark:text-gray-400">{post.excerpt?.substring(0, 50)}...</div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap"><StatusBadge status={post.status} /></td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <div className="flex items-center justify-end gap-2">
                                                <button onClick={() => handleEdit(post)} className="p-2 text-gray-400 hover:text-blue-600 rounded-full hover:bg-blue-50 dark:hover:bg-blue-900/20"><Edit className="w-4 h-4" /></button>
                                                <button onClick={() => handleDelete(post.id, 'post')} className="p-2 text-gray-400 hover:text-red-600 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20"><Trash2 className="w-4 h-4" /></button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );

    const renderMedia = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Media Library</h2>
                <button className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-primary/90 transition-colors">
                    <Plus className="w-4 h-4" /> Upload
                </button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                {isLoading ? <Loader /> : media.length === 0 ? (
                    <div className="col-span-full py-12 text-center text-gray-500 border border-dashed rounded-lg">No media files.</div>
                ) : (
                    media.map((item) => (
                        <div key={item.id} className="group relative aspect-square bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
                            <img src={item.url} alt={item.title} className="w-full h-full object-cover" />
                        </div>
                    ))
                )}
            </div>
        </div>
    );

    const renderContent = () => {
        switch (activeTab) {
            case 'cms-pages': return renderPages();
            case 'cms-posts': return renderPosts();
            case 'cms-media': return renderMedia();
            default: return <div>Select a tab</div>;
        }
    };

    return (
        <>
            {renderContent()}
            {/* Assuming PageForm accepts initialData and handles API internally, or we update it */}
            <PageForm
                isOpen={showPageModal}
                onClose={() => setShowPageModal(false)}
                onSuccess={fetchData}
                initialData={selectedItem}
            />
            <PostForm
                isOpen={showPostModal}
                onClose={() => setShowPostModal(false)}
                onSuccess={fetchData}
                initialData={selectedItem}
            />
        </>
    );
};

// Helper Components
const Loader = () => <RefreshCw className="h-6 w-6 animate-spin mx-auto text-primary" />;

const Input = ({ className, ...props }: any) => (
    <input className={`w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 focus:ring-2 focus:ring-primary/50 outline-none ${className}`} {...props} />
);

const StatusBadge = ({ status }: { status: string }) => {
    const colors: any = {
        publish: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        draft: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        private: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300',
        trash: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
    };
    return (
        <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${colors[status] || colors.draft}`}>
            {status}
        </span>
    );
};
