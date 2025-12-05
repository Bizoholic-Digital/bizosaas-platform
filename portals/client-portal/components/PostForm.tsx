'use client';

import React, { useState, useEffect } from 'react';
import { X, Save, Loader2 } from 'lucide-react';
import { RichTextEditor } from './RichTextEditor';

interface PostFormProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
    initialData?: any;
}

export const PostForm: React.FC<PostFormProps> = ({ isOpen, onClose, onSuccess, initialData }) => {
    const [formData, setFormData] = useState({
        title: '',
        slug: '',
        content: '',
        excerpt: '',
        category: '',
        tags: '',
        status: 'draft',
        featured_image: ''
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (initialData) {
            setFormData({
                title: initialData.title || '',
                slug: initialData.slug || '',
                content: initialData.content || '',
                excerpt: initialData.excerpt || '',
                category: initialData.category || '',
                tags: initialData.tags ? initialData.tags.join(', ') : '',
                status: initialData.status || 'draft',
                featured_image: initialData.featured_image || ''
            });
        } else {
            setFormData({
                title: '',
                slug: '',
                content: '',
                excerpt: '',
                category: '',
                tags: '',
                status: 'draft',
                featured_image: ''
            });
        }
    }, [initialData, isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            const url = initialData
                ? `/api/brain/wagtail/posts?post_id=${initialData.id}`
                : '/api/brain/wagtail/posts';

            const method = initialData ? 'PUT' : 'POST';

            // Process tags
            const processedData = {
                ...formData,
                tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
            };

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(processedData),
            });

            if (!response.ok) {
                throw new Error('Failed to save post');
            }

            onSuccess();
            onClose();
        } catch (err) {
            setError('Failed to save post. Please try again.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-gray-900 rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto">
                <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-800 sticky top-0 bg-white dark:bg-gray-900 z-10">
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                        {initialData ? 'Edit Post' : 'Create New Post'}
                    </h2>
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
                        <X className="w-6 h-6" />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-6">
                    {error && (
                        <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-lg text-sm">
                            {error}
                        </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Post Title
                                </label>
                                <input
                                    type="text"
                                    required
                                    value={formData.title}
                                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Slug (URL)
                                </label>
                                <input
                                    type="text"
                                    required
                                    value={formData.slug}
                                    onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Status
                                </label>
                                <select
                                    value={formData.status}
                                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                                >
                                    <option value="draft">Draft</option>
                                    <option value="published">Published</option>
                                    <option value="archived">Archived</option>
                                </select>
                            </div>
                        </div>

                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Category
                                </label>
                                <select
                                    value={formData.category}
                                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                                >
                                    <option value="">Select Category</option>
                                    <option value="technology">Technology</option>
                                    <option value="business">Business</option>
                                    <option value="marketing">Marketing</option>
                                    <option value="news">News</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Tags (comma separated)
                                </label>
                                <input
                                    type="text"
                                    value={formData.tags}
                                    onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                                    placeholder="e.g. saas, ai, growth"
                                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Excerpt
                                </label>
                                <textarea
                                    rows={3}
                                    value={formData.excerpt}
                                    onChange={(e) => setFormData({ ...formData, excerpt: e.target.value })}
                                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                                />
                            </div>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Content
                        </label>
                        <RichTextEditor
                            value={formData.content}
                            onChange={(html) => setFormData({ ...formData, content: html })}
                            placeholder="Start writing your blog post..."
                        />
                    </div>

                    <div className="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-800">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
                        >
                            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                            {initialData ? 'Update Post' : 'Create Post'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};
