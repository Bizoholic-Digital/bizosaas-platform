'use client';

import React, { useState, useEffect } from 'react';
import {
  FileText, Package, Activity, Mail, Code, Plus, Search,
  Edit3, Trash2, Eye, Calendar, User, ExternalLink,
  Filter, Download, Upload, Settings
} from 'lucide-react';

interface CMSContentProps {
  activeTab: string;
}

interface Page {
  id: string;
  title: string;
  slug: string;
  status: 'published' | 'draft' | 'archived';
  created_at: string;
  updated_at: string;
  author: string;
  views: number;
  content_type: string;
}

interface Post {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  status: 'published' | 'draft';
  created_at: string;
  author: string;
  category: string;
  tags: string[];
  featured_image?: string;
}

interface MediaFile {
  id: string;
  name: string;
  type: 'image' | 'video' | 'document' | 'audio';
  size: number;
  url: string;
  uploaded_at: string;
  alt_text?: string;
}

interface Form {
  id: string;
  name: string;
  description: string;
  fields_count: number;
  submissions_count: number;
  status: 'active' | 'inactive';
  created_at: string;
}

interface Template {
  id: string;
  name: string;
  type: 'page' | 'post' | 'email';
  description: string;
  preview_url?: string;
  created_at: string;
  usage_count: number;
}

export function CMSContent({ activeTab }: CMSContentProps) {
  const [loading, setLoading] = useState(false);
  const [pages, setPages] = useState<Page[]>([]);
  const [posts, setPosts] = useState<Post[]>([]);
  const [media, setMedia] = useState<MediaFile[]>([]);
  const [forms, setForms] = useState<Form[]>([]);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadCMSData();
  }, [activeTab]);

  const loadCMSData = async () => {
    setLoading(true);
    try {
      const endpoint = getCMSEndpoint(activeTab);
      const response = await fetch(endpoint);

      if (!response.ok) {
        console.error('Failed to load CMS data:', response.status);
        // Load fallback data
        loadFallbackData();
      } else {
        const data = await response.json();
        updateStateBasedOnTab(data);
      }
    } catch (error) {
      console.error('Error loading CMS data:', error);
      loadFallbackData();
    } finally {
      setLoading(false);
    }
  };

  const getCMSEndpoint = (tab: string) => {
    const baseUrl = '/api/brain/wagtail';
    switch (tab) {
      case 'cms-pages': return `${baseUrl}/pages`;
      case 'cms-posts': return `${baseUrl}/posts`;
      case 'cms-media': return `${baseUrl}/media`;
      case 'cms-forms': return `${baseUrl}/forms`;
      case 'cms-templates': return `${baseUrl}/templates`;
      default: return `${baseUrl}/pages`;
    }
  };

  const updateStateBasedOnTab = (data: any) => {
    switch (activeTab) {
      case 'cms-pages': setPages(data.pages || []); break;
      case 'cms-posts': setPosts(data.posts || []); break;
      case 'cms-media': setMedia(data.media || []); break;
      case 'cms-forms': setForms(data.forms || []); break;
      case 'cms-templates': setTemplates(data.templates || []); break;
    }
  };

  const loadFallbackData = () => {
    switch (activeTab) {
      case 'cms-pages':
        setPages([
          {
            id: '1',
            title: 'Homepage',
            slug: 'home',
            status: 'published',
            created_at: '2024-01-15T10:00:00Z',
            updated_at: '2024-01-20T14:30:00Z',
            author: 'John Doe',
            views: 1245,
            content_type: 'homepage'
          },
          {
            id: '2',
            title: 'About Us',
            slug: 'about',
            status: 'published',
            created_at: '2024-01-10T09:00:00Z',
            updated_at: '2024-01-18T16:45:00Z',
            author: 'Jane Smith',
            views: 892,
            content_type: 'standard'
          },
          {
            id: '3',
            title: 'Services Overview',
            slug: 'services',
            status: 'draft',
            created_at: '2024-01-25T11:15:00Z',
            updated_at: '2024-01-25T11:15:00Z',
            author: 'Mike Johnson',
            views: 0,
            content_type: 'services'
          }
        ]);
        break;

      case 'cms-posts':
        setPosts([
          {
            id: '1',
            title: 'AI Marketing Trends for 2024',
            slug: 'ai-marketing-trends-2024',
            excerpt: 'Discover the latest AI marketing trends that are shaping the industry this year.',
            status: 'published',
            created_at: '2024-01-20T10:00:00Z',
            author: 'Sarah Wilson',
            category: 'Marketing',
            tags: ['AI', 'Marketing', 'Trends', '2024'],
            featured_image: '/blog/ai-marketing-trends.jpg'
          },
          {
            id: '2',
            title: 'Building Effective Email Campaigns',
            slug: 'building-effective-email-campaigns',
            excerpt: 'Learn how to create email campaigns that convert and engage your audience.',
            status: 'published',
            created_at: '2024-01-18T14:30:00Z',
            author: 'David Chen',
            category: 'Email Marketing',
            tags: ['Email', 'Campaigns', 'Conversion'],
            featured_image: '/blog/email-campaigns.jpg'
          },
          {
            id: '3',
            title: 'Social Media Strategy Guide',
            slug: 'social-media-strategy-guide',
            excerpt: 'A comprehensive guide to developing winning social media strategies.',
            status: 'draft',
            created_at: '2024-01-25T09:15:00Z',
            author: 'Lisa Park',
            category: 'Social Media',
            tags: ['Social Media', 'Strategy', 'Guide'],
          }
        ]);
        break;

      case 'cms-media':
        setMedia([
          {
            id: '1',
            name: 'hero-banner.jpg',
            type: 'image',
            size: 2048576,
            url: '/media/hero-banner.jpg',
            uploaded_at: '2024-01-15T10:00:00Z',
            alt_text: 'Hero banner showing AI marketing concept'
          },
          {
            id: '2',
            name: 'company-video.mp4',
            type: 'video',
            size: 15728640,
            url: '/media/company-video.mp4',
            uploaded_at: '2024-01-18T14:30:00Z',
            alt_text: 'Company introduction video'
          },
          {
            id: '3',
            name: 'case-study.pdf',
            type: 'document',
            size: 1048576,
            url: '/media/case-study.pdf',
            uploaded_at: '2024-01-20T09:45:00Z',
            alt_text: 'Client success case study document'
          }
        ]);
        break;

      case 'cms-forms':
        setForms([
          {
            id: '1',
            name: 'Contact Form',
            description: 'Main contact form for client inquiries',
            fields_count: 5,
            submissions_count: 127,
            status: 'active',
            created_at: '2024-01-10T10:00:00Z'
          },
          {
            id: '2',
            name: 'Newsletter Signup',
            description: 'Email newsletter subscription form',
            fields_count: 2,
            submissions_count: 324,
            status: 'active',
            created_at: '2024-01-15T14:30:00Z'
          },
          {
            id: '3',
            name: 'Consultation Request',
            description: 'Free consultation booking form',
            fields_count: 8,
            submissions_count: 67,
            status: 'active',
            created_at: '2024-01-20T09:15:00Z'
          }
        ]);
        break;

      case 'cms-templates':
        setTemplates([
          {
            id: '1',
            name: 'Landing Page Template',
            type: 'page',
            description: 'High-converting landing page template with hero section and CTA',
            preview_url: '/templates/preview/landing-page',
            created_at: '2024-01-10T10:00:00Z',
            usage_count: 12
          },
          {
            id: '2',
            name: 'Blog Post Template',
            type: 'post',
            description: 'Standard blog post template with featured image and social sharing',
            preview_url: '/templates/preview/blog-post',
            created_at: '2024-01-15T14:30:00Z',
            usage_count: 28
          },
          {
            id: '3',
            name: 'Email Newsletter Template',
            type: 'email',
            description: 'Responsive email template for newsletters and promotions',
            preview_url: '/templates/preview/email-newsletter',
            created_at: '2024-01-20T09:15:00Z',
            usage_count: 45
          }
        ]);
        break;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getStatusBadge = (status: string) => {
    const colors = {
      published: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
      draft: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
      archived: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400',
      active: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
      inactive: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
    };

    return (
      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${colors[status as keyof typeof colors] || colors.draft}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  const renderContent = () => {
    if (loading) {
      return (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          <span className="ml-3 text-gray-600 dark:text-gray-400">Loading CMS data...</span>
        </div>
      );
    }

    switch (activeTab) {
      case 'cms-pages':
        return renderPages();
      case 'cms-posts':
        return renderPosts();
      case 'cms-media':
        return renderMedia();
      case 'cms-forms':
        return renderForms();
      case 'cms-templates':
        return renderTemplates();
      default:
        return renderPages();
    }
  };

  const renderPages = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Pages</h2>
        <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
          <Plus className="w-4 h-4" />
          New Page
        </button>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search pages..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>
            <button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 flex items-center gap-2">
              <Filter className="w-4 h-4" />
              Filter
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Page
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Author
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Views
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Updated
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {pages.map((page) => (
                <tr key={page.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                  <td className="px-6 py-4">
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        {page.title}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        /{page.slug}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    {getStatusBadge(page.status)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                    {page.author}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                    {page.views.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {formatDate(page.updated_at)}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <button className="p-1 text-gray-400 hover:text-blue-600">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="p-1 text-gray-400 hover:text-green-600">
                        <Edit3 className="w-4 h-4" />
                      </button>
                      <button className="p-1 text-gray-400 hover:text-red-600">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
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
        <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
          <Plus className="w-4 h-4" />
          New Post
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {posts.map((post) => (
          <div key={post.id} className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden hover:shadow-lg transition-shadow">
            {post.featured_image && (
              <div className="h-48 bg-gray-200 dark:bg-gray-700"></div>
            )}
            <div className="p-6">
              <div className="flex items-center justify-between mb-2">
                {getStatusBadge(post.status)}
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {post.category}
                </span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {post.title}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                {post.excerpt}
              </p>
              <div className="flex flex-wrap gap-1 mb-4">
                {post.tags.map((tag) => (
                  <span key={tag} className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded">
                    {tag}
                  </span>
                ))}
              </div>
              <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
                <span>{post.author}</span>
                <span>{formatDate(post.created_at)}</span>
              </div>
              <div className="flex items-center gap-2 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                <button className="flex-1 py-1 px-3 text-sm border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-800">
                  Edit
                </button>
                <button className="p-1 text-gray-400 hover:text-blue-600">
                  <ExternalLink className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderMedia = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Media Library</h2>
        <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
          <Upload className="w-4 h-4" />
          Upload Files
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {media.map((file) => (
          <div key={file.id} className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden hover:shadow-lg transition-shadow">
            <div className="h-32 bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
              {file.type === 'image' && <Package className="w-8 h-8 text-gray-400" />}
              {file.type === 'video' && <Activity className="w-8 h-8 text-gray-400" />}
              {file.type === 'document' && <FileText className="w-8 h-8 text-gray-400" />}
              {file.type === 'audio' && <Mail className="w-8 h-8 text-gray-400" />}
            </div>
            <div className="p-4">
              <h3 className="text-sm font-medium text-gray-900 dark:text-white truncate">
                {file.name}
              </h3>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                {formatFileSize(file.size)}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {formatDate(file.uploaded_at)}
              </p>
              <div className="flex items-center gap-2 mt-3">
                <button className="flex-1 py-1 px-2 text-xs border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-800">
                  Download
                </button>
                <button className="p-1 text-gray-400 hover:text-red-600">
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderForms = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Forms</h2>
        <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
          <Plus className="w-4 h-4" />
          Create Form
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {forms.map((form) => (
          <div key={form.id} className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <Mail className="w-8 h-8 text-purple-600" />
              {getStatusBadge(form.status)}
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {form.name}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              {form.description}
            </p>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">{form.fields_count}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400">Fields</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{form.submissions_count}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400">Submissions</div>
              </div>
            </div>
            <div className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Created {formatDate(form.created_at)}
            </div>
            <div className="flex items-center gap-2">
              <button className="flex-1 py-2 px-3 text-sm bg-purple-600 text-white rounded hover:bg-purple-700">
                Edit Form
              </button>
              <button className="p-2 text-gray-400 hover:text-blue-600">
                <Download className="w-4 h-4" />
              </button>
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <Settings className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderTemplates = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Templates</h2>
        <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
          <Plus className="w-4 h-4" />
          New Template
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {templates.map((template) => (
          <div key={template.id} className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden hover:shadow-lg transition-shadow">
            <div className="h-32 bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
              <Code className="w-8 h-8 text-gray-400" />
            </div>
            <div className="p-6">
              <div className="flex items-center justify-between mb-2">
                <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 rounded-full">
                  {template.type}
                </span>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {template.usage_count} uses
                </span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {template.name}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                {template.description}
              </p>
              <div className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                Created {formatDate(template.created_at)}
              </div>
              <div className="flex items-center gap-2">
                <button className="flex-1 py-2 px-3 text-sm bg-purple-600 text-white rounded hover:bg-purple-700">
                  Use Template
                </button>
                {template.preview_url && (
                  <button className="p-2 text-gray-400 hover:text-blue-600">
                    <Eye className="w-4 h-4" />
                  </button>
                )}
                <button className="p-2 text-gray-400 hover:text-green-600">
                  <Edit3 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {renderContent()}
    </div>
  );
}