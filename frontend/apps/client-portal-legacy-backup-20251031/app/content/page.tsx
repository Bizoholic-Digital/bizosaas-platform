'use client';

import React, { useState, useEffect } from 'react';
import { 
  FileText, Newspaper, Image, MessageSquare, Plus, 
  Search, Filter, Download, RefreshCw, Edit, Eye, 
  Trash2, MoreHorizontal, Calendar, User, Tag,
  Globe, Settings, Upload, Video, BookOpen
} from 'lucide-react';
import DashboardLayout from '../../components/ui/dashboard-layout';

interface ContentTabs {
  [key: string]: React.ReactNode;
}

const ContentManagementPage = () => {
  const [activeTab, setActiveTab] = useState('pages');
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const fetchContentData = async () => {
      try {
        setLoading(true);
        // Mock API call - replace with actual Wagtail CMS API calls through Brain Hub
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setData({
          pages: [
            {
              id: '1',
              title: 'About Us',
              slug: 'about-us',
              type: 'Standard Page',
              status: 'published',
              author: 'Admin User',
              lastModified: '2024-09-24T10:30:00Z',
              views: 1250,
              url: '/about-us'
            },
            {
              id: '2',
              title: 'Services Overview',
              slug: 'services-overview',
              type: 'Service Page',
              status: 'published',
              author: 'Content Editor',
              lastModified: '2024-09-23T15:45:00Z',
              views: 890,
              url: '/services'
            },
            {
              id: '3',
              title: 'Contact Information',
              slug: 'contact',
              type: 'Contact Page',
              status: 'draft',
              author: 'Admin User',
              lastModified: '2024-09-24T09:15:00Z',
              views: 0,
              url: '/contact'
            }
          ],
          blogPosts: [
            {
              id: '1',
              title: 'Digital Marketing Trends 2024',
              slug: 'digital-marketing-trends-2024',
              excerpt: 'Discover the latest trends shaping digital marketing...',
              status: 'published',
              author: 'Marketing Team',
              publishDate: '2024-09-23T10:00:00Z',
              views: 2340,
              comments: 15,
              tags: ['Marketing', 'Trends', 'Digital']
            },
            {
              id: '2',
              title: 'SEO Best Practices Guide',
              slug: 'seo-best-practices-guide',
              excerpt: 'A comprehensive guide to improving your search rankings...',
              status: 'published',
              author: 'SEO Specialist',
              publishDate: '2024-09-22T14:30:00Z',
              views: 1890,
              comments: 8,
              tags: ['SEO', 'Guide', 'Best Practices']
            },
            {
              id: '3',
              title: 'Social Media Strategy 2024',
              slug: 'social-media-strategy-2024',
              excerpt: 'How to create an effective social media strategy...',
              status: 'draft',
              author: 'Social Media Manager',
              publishDate: null,
              views: 0,
              comments: 0,
              tags: ['Social Media', 'Strategy']
            }
          ],
          media: [
            {
              id: '1',
              name: 'hero-banner.jpg',
              type: 'image',
              size: '2.4 MB',
              dimensions: '1920x1080',
              uploadDate: '2024-09-24T08:00:00Z',
              usedIn: 3,
              url: '/media/hero-banner.jpg'
            },
            {
              id: '2',
              name: 'company-logo.svg',
              type: 'image',
              size: '45 KB',
              dimensions: '500x500',
              uploadDate: '2024-09-23T12:00:00Z',
              usedIn: 8,
              url: '/media/company-logo.svg'
            }
          ],
          forms: [
            {
              id: '1',
              name: 'Contact Form',
              type: 'Contact',
              fields: 5,
              submissions: 67,
              conversionRate: 12.4,
              status: 'active',
              lastSubmission: '2024-09-24T16:20:00Z'
            },
            {
              id: '2',
              name: 'Newsletter Signup',
              type: 'Newsletter',
              fields: 2,
              submissions: 234,
              conversionRate: 8.7,
              status: 'active',
              lastSubmission: '2024-09-24T14:30:00Z'
            }
          ],
          metrics: {
            totalPages: 24,
            publishedPages: 18,
            draftPages: 6,
            totalBlogPosts: 45,
            publishedPosts: 38,
            totalViews: 15420,
            totalComments: 89
          }
        });
      } catch (error) {
        console.error('Failed to fetch content data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchContentData();
  }, []);

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      published: { color: 'bg-green-100 text-green-800', label: 'Published' },
      draft: { color: 'bg-yellow-100 text-yellow-800', label: 'Draft' },
      scheduled: { color: 'bg-blue-100 text-blue-800', label: 'Scheduled' },
      archived: { color: 'bg-gray-100 text-gray-800', label: 'Archived' },
      active: { color: 'bg-green-100 text-green-800', label: 'Active' },
      inactive: { color: 'bg-red-100 text-red-800', label: 'Inactive' }
    };

    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.draft;
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const PagesTab = () => (
    <div className="space-y-6">
      {/* Pages Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Pages Management</h2>
          <p className="text-sm text-gray-600 dark:text-gray-300">Create and manage your website pages</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-600 dark:hover:bg-gray-700">
            <Filter className="w-4 h-4" />
            Filter
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <Plus className="w-4 h-4" />
            New Page
          </button>
        </div>
      </div>

      {/* Pages Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <FileText className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Total Pages</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.totalPages}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
              <Globe className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Published</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.publishedPages}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-100 dark:bg-yellow-900 rounded-lg">
              <Edit className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Drafts</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.draftPages}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <Eye className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Total Views</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.totalViews?.toLocaleString()}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Pages Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">All Pages</h3>
            <div className="flex items-center gap-3">
              <div className="relative">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search pages..."
                  className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Page
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Author
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Views
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Last Modified
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {data?.pages?.map((page: any) => (
                <tr key={page.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">{page.title}</div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">/{page.slug}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {page.type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStatusBadge(page.status)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {page.author}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {page.views?.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {new Date(page.lastModified).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center gap-2 justify-end">
                      <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300">
                        <Edit className="w-4 h-4" />
                      </button>
                      <button className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300">
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

  const BlogTab = () => (
    <div className="space-y-6">
      {/* Blog Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Blog Management</h2>
          <p className="text-sm text-gray-600 dark:text-gray-300">Create and manage blog posts</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-600 dark:hover:bg-gray-700">
            <Calendar className="w-4 h-4" />
            Schedule
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <Plus className="w-4 h-4" />
            New Post
          </button>
        </div>
      </div>

      {/* Blog Posts */}
      <div className="grid gap-6">
        {data?.blogPosts?.map((post: any) => (
          <div key={post.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{post.title}</h3>
                  {getStatusBadge(post.status)}
                </div>
                <p className="text-gray-600 dark:text-gray-300 mb-4">{post.excerpt}</p>
                <div className="flex items-center gap-6 text-sm text-gray-500 dark:text-gray-400">
                  <div className="flex items-center gap-1">
                    <User className="w-4 h-4" />
                    <span>{post.author}</span>
                  </div>
                  {post.publishDate && (
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      <span>{new Date(post.publishDate).toLocaleDateString()}</span>
                    </div>
                  )}
                  <div className="flex items-center gap-1">
                    <Eye className="w-4 h-4" />
                    <span>{post.views?.toLocaleString()} views</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <MessageSquare className="w-4 h-4" />
                    <span>{post.comments} comments</span>
                  </div>
                </div>
                <div className="flex items-center gap-2 mt-3">
                  {post.tags?.map((tag: string) => (
                    <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full dark:bg-blue-900 dark:text-blue-300">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
              <div className="flex items-center gap-2 ml-6">
                <button className="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900 rounded-lg">
                  <Eye className="w-4 h-4" />
                </button>
                <button className="p-2 text-green-600 hover:bg-green-50 dark:hover:bg-green-900 rounded-lg">
                  <Edit className="w-4 h-4" />
                </button>
                <button className="p-2 text-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg">
                  <MoreHorizontal className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const tabs: ContentTabs = {
    pages: <PagesTab />,
    blog: <BlogTab />,
    media: <div className="p-6 text-center text-gray-500">Media library coming soon...</div>,
    forms: <div className="p-6 text-center text-gray-500">Forms management coming soon...</div>
  };

  const tabItems = [
    { id: 'pages', name: 'Pages', icon: <FileText className="w-4 h-4" />, badge: data?.pages?.length },
    { id: 'blog', name: 'Blog Posts', icon: <Newspaper className="w-4 h-4" />, badge: data?.blogPosts?.length },
    { id: 'media', name: 'Media', icon: <Image className="w-4 h-4" />, badge: data?.media?.length },
    { id: 'forms', name: 'Forms', icon: <MessageSquare className="w-4 h-4" />, badge: data?.forms?.length }
  ];

  if (loading) {
    return (
      <DashboardLayout title="Content Management" description="Manage your website content and media">
        <div className="p-6 animate-pulse">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
            ))}
          </div>
          <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Content Management" description="Manage your website content, blog posts, and media">
      <div className="flex flex-col h-full">
        {/* Tab Navigation */}
        <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
          <div className="px-6">
            <nav className="flex space-x-8">
              {tabItems.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                >
                  {tab.icon}
                  <span>{tab.name}</span>
                  {tab.badge && (
                    <span className="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full dark:bg-blue-900 dark:text-blue-300">
                      {tab.badge}
                    </span>
                  )}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-hidden">
          <div className="h-full overflow-y-auto p-6">
            {tabs[activeTab]}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ContentManagementPage;