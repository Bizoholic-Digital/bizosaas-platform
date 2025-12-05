'use client';

import React, { useState, useEffect } from 'react';
import {
    FileText, MessageSquare, Image, Layout, Plus, Search,
    Filter, Edit, Trash2, Eye, MoreVertical, CheckCircle, XCircle
} from 'lucide-react';
import { PageForm } from './PageForm';
import { PostForm } from './PostForm';

interface CMSContentProps {
    activeTab: string;
}

export const CMSContent: React.FC<CMSContentProps> = ({ activeTab }) => {
    const [pages, setPages] = useState([]);
    const [posts, setPosts] = useState([]);
    const [media, setMedia] = useState([]);
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
            // New logic: fetch via Brain Gateway -> WordPress Connector
            let data: any = { data: [] };

            if (activeTab === 'cms-pages') {
                // In a real app we'd get the connector ID dynamically.
                // For MVP, we pass 'wordpress' type or assume first active WP connector
                // This call should go to something like `/api/brain/connectors/proxy/wordpress/pages`
                // But since we are client-side, we use the brainApi lib helper we will assume exists or mocked here
                // For now, let's keep it mocked until we wire the exact proxy endpoint in next step
                // data = await brainApi.connectors.sync('wordpress', 'pages'); 
                setPages([]);
            } else if (activeTab === 'cms-posts') {
                // data = await brainApi.connectors.sync('wordpress', 'posts');
                setPosts([]);
            } else if (activeTab === 'cms-media') {
                setMedia([]);
            }
        } catch (error) {
            console.error('Failed to fetch CMS data:', error);
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
            const endpoint = type === 'page' ? 'pages' : type === 'post' ? 'posts' : 'media';
            const param = type === 'page' ? 'page_id' : type === 'post' ? 'post_id' : 'media_id';

            const response = await fetch(`/api/brain/wagtail/${endpoint}?${param}=${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                fetchData();
            }
        } catch (error) {
            console.error('Failed to delete item:', error);
        }
    };

    const renderPages = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Pages</h2>
                <button
                    onClick={handleCreate}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
                >
                    <Plus className="w-4 h-4" /> Create Page
                </button>
            </div>

            <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
                <div className="p-4 border-b border-gray-200 dark:border-gray-800 flex gap-4">
                    <div className="relative flex-1">
                        <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search pages..."
                            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800"
                        />
                    </div>
                    <button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg flex items-center gap-2">
                        <Filter className="w-4 h-4" /> Filter
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50 dark:bg-gray-800">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Title</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Last Updated</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Author</th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                            {pages.length === 0 ? (
                                <tr>
                                    <td colSpan={5} className="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                                        No pages found. Create your first page to get started.
                                    </td>
                                </tr>
                            ) : (
                                pages.map((page: any) => (
                                    <tr key={page.id}>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="text-sm font-medium text-gray-900 dark:text-white">{page.title}</div>
                                            <div className="text-sm text-gray-500 dark:text-gray-400">{page.slug}</div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${page.status === 'published'
                                                ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                                                : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                                                }`}>
                                                {page.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                            {new Date(page.updated_at).toLocaleDateString()}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                            {page.author}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <div className="flex items-center justify-end gap-2">
                                                <button
                                                    onClick={() => handleEdit(page)}
                                                    className="text-gray-400 hover:text-blue-600"
                                                >
                                                    <Edit className="w-4 h-4" />
                                                </button>
                                                <button
                                                    onClick={() => handleDelete(page.id, 'page')}
                                                    className="text-gray-400 hover:text-red-600"
                                                >
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
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
                >
                    <Plus className="w-4 h-4" /> Create Post
                </button>
            </div>

            <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
                <div className="p-4 border-b border-gray-200 dark:border-gray-800 flex gap-4">
                    <div className="relative flex-1">
                        <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search posts..."
                            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800"
                        />
                    </div>
                    <button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg flex items-center gap-2">
                        <Filter className="w-4 h-4" /> Filter
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50 dark:bg-gray-800">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Title</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Category</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Published</th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                            {posts.length === 0 ? (
                                <tr>
                                    <td colSpan={5} className="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                                        No posts found. Start writing your first blog post.
                                    </td>
                                </tr>
                            ) : (
                                posts.map((post: any) => (
                                    <tr key={post.id}>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="text-sm font-medium text-gray-900 dark:text-white">{post.title}</div>
                                            <div className="text-sm text-gray-500 dark:text-gray-400 truncate max-w-xs">{post.excerpt}</div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
                                                {post.category}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${post.status === 'published'
                                                ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                                                : 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
                                                }`}>
                                                {post.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                            {new Date(post.published_at).toLocaleDateString()}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <div className="flex items-center justify-end gap-2">
                                                <button
                                                    onClick={() => handleEdit(post)}
                                                    className="text-gray-400 hover:text-blue-600"
                                                >
                                                    <Edit className="w-4 h-4" />
                                                </button>
                                                <button
                                                    onClick={() => handleDelete(post.id, 'post')}
                                                    className="text-gray-400 hover:text-red-600"
                                                >
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

    const renderMedia = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Media Library</h2>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700">
                    <Plus className="w-4 h-4" /> Upload Media
                </button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                {media.length === 0 ? (
                    <div className="col-span-full py-12 text-center text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 border-dashed">
                        <Image className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                        <p>No media files uploaded yet.</p>
                        <button className="mt-4 text-blue-600 hover:underline">Upload your first file</button>
                    </div>
                ) : (
                    media.map((item: any) => (
                        <div key={item.id} className="group relative aspect-square bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
                            <img
                                src={item.url}
                                alt={item.title}
                                className="w-full h-full object-cover"
                            />
                            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                                <button className="p-2 bg-white rounded-full text-gray-900 hover:bg-gray-100">
                                    <Eye className="w-4 h-4" />
                                </button>
                                <button
                                    onClick={() => handleDelete(item.id, 'media')}
                                    className="p-2 bg-red-600 rounded-full text-white hover:bg-red-700"
                                >
                                    <Trash2 className="w-4 h-4" />
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );

    const renderContent = () => {
        switch (activeTab) {
            case 'cms-pages':
                return renderPages();
            case 'cms-posts':
                return renderPosts();
            case 'cms-media':
                return renderMedia();
            default:
                return (
                    <div className="flex items-center justify-center h-96 text-gray-500 dark:text-gray-400">
                        CMS module: {activeTab.replace('cms-', '')} coming soon
                    </div>
                );
        }
    };

    return (
        <>
            {renderContent()}

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
