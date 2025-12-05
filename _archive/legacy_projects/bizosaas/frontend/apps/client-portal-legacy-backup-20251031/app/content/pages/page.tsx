'use client';

import React, { useState, useEffect } from 'react';
import { 
  FileText, Plus, Search, Filter, Download, RefreshCw, 
  Edit, Eye, Trash2, MoreHorizontal, Globe, Calendar,
  User, Tag, Copy, Share2, Settings, Star, Clock,
  CheckCircle, AlertCircle, Layout, Code, Image
} from 'lucide-react';
import Link from 'next/link';
import DashboardLayout from '../../../components/ui/dashboard-layout';

const PagesPage = () => {
  const [loading, setLoading] = useState(true);
  const [pages, setPages] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');

  useEffect(() => {
    const fetchPages = async () => {
      try {
        setLoading(true);
        // Mock API call - replace with actual Wagtail CMS API calls through Brain Hub
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setPages([
          {
            id: '1',
            title: 'About Us',
            slug: 'about-us',
            type: 'Standard Page',
            template: 'standard_page.html',
            status: 'published',
            featured: true,
            author: 'Admin User',
            lastModified: '2024-09-24T10:30:00Z',
            publishDate: '2024-09-01T09:00:00Z',
            views: 1250,
            uniqueViews: 980,
            avgTimeOnPage: 145,
            bounceRate: 32,
            url: '/about-us',
            metaDescription: 'Learn more about our company, mission, and values.',
            tags: ['About', 'Company'],
            seoScore: 85,
            wordCount: 650
          },
          {
            id: '2',
            title: 'Services Overview',
            slug: 'services-overview',
            type: 'Service Page',
            template: 'service_page.html',
            status: 'published',
            featured: false,
            author: 'Content Editor',
            lastModified: '2024-09-23T15:45:00Z',
            publishDate: '2024-08-15T14:00:00Z',
            views: 890,
            uniqueViews: 720,
            avgTimeOnPage: 198,
            bounceRate: 28,
            url: '/services',
            metaDescription: 'Discover our comprehensive range of digital marketing services.',
            tags: ['Services', 'Marketing'],
            seoScore: 92,
            wordCount: 1200
          },
          {
            id: '3',
            title: 'Contact Information',
            slug: 'contact',
            type: 'Contact Page',
            template: 'contact_page.html',
            status: 'draft',
            featured: false,
            author: 'Admin User',
            lastModified: '2024-09-24T09:15:00Z',
            publishDate: null,
            views: 0,
            uniqueViews: 0,
            avgTimeOnPage: 0,
            bounceRate: 0,
            url: '/contact',
            metaDescription: 'Get in touch with our team for inquiries and support.',
            tags: ['Contact', 'Support'],
            seoScore: 78,
            wordCount: 320
          },
          {
            id: '4',
            title: 'Pricing Plans',
            slug: 'pricing',
            type: 'Pricing Page',
            template: 'pricing_page.html',
            status: 'published',
            featured: true,
            author: 'Marketing Team',
            lastModified: '2024-09-22T11:20:00Z',
            publishDate: '2024-09-01T08:00:00Z',
            views: 2340,
            uniqueViews: 1890,
            avgTimeOnPage: 234,
            bounceRate: 22,
            url: '/pricing',
            metaDescription: 'Choose the perfect plan for your business needs.',
            tags: ['Pricing', 'Plans', 'Business'],
            seoScore: 88,
            wordCount: 850
          },
          {
            id: '5',
            title: 'Privacy Policy',
            slug: 'privacy-policy',
            type: 'Legal Page',
            template: 'legal_page.html',
            status: 'published',
            featured: false,
            author: 'Legal Team',
            lastModified: '2024-09-20T16:30:00Z',
            publishDate: '2024-08-01T10:00:00Z',
            views: 456,
            uniqueViews: 398,
            avgTimeOnPage: 89,
            bounceRate: 65,
            url: '/privacy-policy',
            metaDescription: 'Our privacy policy and data protection practices.',
            tags: ['Legal', 'Privacy'],
            seoScore: 72,
            wordCount: 2200
          },
          {
            id: '6',
            title: 'Blog Homepage',
            slug: 'blog',
            type: 'Blog Index',
            template: 'blog_index.html',
            status: 'published',
            featured: false,
            author: 'Content Team',
            lastModified: '2024-09-21T12:00:00Z',
            publishDate: '2024-07-01T09:00:00Z',
            views: 3450,
            uniqueViews: 2100,
            avgTimeOnPage: 167,
            bounceRate: 38,
            url: '/blog',
            metaDescription: 'Stay updated with our latest insights and industry news.',
            tags: ['Blog', 'Content'],
            seoScore: 90,
            wordCount: 450
          }
        ]);
      } catch (error) {
        console.error('Failed to fetch pages:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPages();
  }, []);

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      published: { color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300', icon: <CheckCircle className="w-3 h-3" />, label: 'Published' },
      draft: { color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300', icon: <Edit className="w-3 h-3" />, label: 'Draft' },
      scheduled: { color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300', icon: <Clock className="w-3 h-3" />, label: 'Scheduled' },
      archived: { color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300', icon: <AlertCircle className="w-3 h-3" />, label: 'Archived' }
    };

    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.draft;
    
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {config.icon}
        {config.label}
      </span>
    );
  };

  const getTypeBadge = (type: string) => {
    const typeConfig = {
      'Standard Page': { color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300' },
      'Service Page': { color: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300' },
      'Contact Page': { color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' },
      'Pricing Page': { color: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300' },
      'Legal Page': { color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300' },
      'Blog Index': { color: 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-300' }
    };

    const config = typeConfig[type as keyof typeof typeConfig] || { color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300' };
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {type}
      </span>
    );
  };

  const getSEOScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const filteredPages = pages.filter(page => {
    const matchesSearch = page.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         page.slug.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         page.type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = selectedStatus === 'all' || page.status === selectedStatus;
    const matchesFilter = selectedFilter === 'all' || 
                         (selectedFilter === 'featured' && page.featured) ||
                         (selectedFilter === 'type' && page.type === selectedFilter);
    return matchesSearch && matchesStatus && matchesFilter;
  });

  const stats = {
    total: pages.length,
    published: pages.filter(p => p.status === 'published').length,
    draft: pages.filter(p => p.status === 'draft').length,
    scheduled: pages.filter(p => p.status === 'scheduled').length,
    totalViews: pages.reduce((sum, p) => sum + p.views, 0),
    avgSEOScore: pages.length > 0 ? Math.round(pages.reduce((sum, p) => sum + p.seoScore, 0) / pages.length) : 0
  };

  if (loading) {
    return (
      <DashboardLayout title="Pages" description="Manage your website pages">
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
    <DashboardLayout title="Pages" description="Manage your website pages and content">
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Page Management</h1>
            <p className="text-gray-600 dark:text-gray-300">Create, edit and manage your website pages</p>
          </div>
          <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
              <Layout className="w-4 h-4" />
              Templates
            </button>
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
              <Download className="w-4 h-4" />
              Export
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              <Plus className="w-4 h-4" />
              Create Page
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-6 gap-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <FileText className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Total</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total}</p>
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
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.published}</p>
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
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.draft}</p>
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
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.totalViews.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-indigo-100 dark:bg-indigo-900 rounded-lg">
                <Settings className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Avg SEO Score</p>
                <p className={`text-2xl font-bold ${getSEOScoreColor(stats.avgSEOScore)}`}>{stats.avgSEOScore}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-orange-100 dark:bg-orange-900 rounded-lg">
                <Star className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Featured</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{pages.filter(p => p.featured).length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search pages by title, slug, or type..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 w-full border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Status</option>
              <option value="published">Published</option>
              <option value="draft">Draft</option>
              <option value="scheduled">Scheduled</option>
              <option value="archived">Archived</option>
            </select>
            <select
              value={selectedFilter}
              onChange={(e) => setSelectedFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Types</option>
              <option value="featured">Featured Only</option>
              <option value="Standard Page">Standard Pages</option>
              <option value="Service Page">Service Pages</option>
              <option value="Legal Page">Legal Pages</option>
            </select>
            <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
              <RefreshCw className="w-4 h-4 text-gray-600 dark:text-gray-300" />
            </button>
          </div>
        </div>

        {/* Pages Table */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
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
                    Performance
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    SEO Score
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
                {filteredPages.map((page) => (
                  <tr key={page.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {page.featured && (
                          <Star className="w-4 h-4 text-yellow-500 mr-2" />
                        )}
                        <div>
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {page.title}
                          </div>
                          <div className="text-sm text-gray-500 dark:text-gray-400">
                            /{page.slug}
                          </div>
                          <div className="flex items-center gap-2 mt-1">
                            {page.tags.map((tag: string) => (
                              <span key={tag} className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded dark:bg-gray-700 dark:text-gray-300">
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {getTypeBadge(page.type)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {getStatusBadge(page.status)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900 dark:text-white">
                        {page.views.toLocaleString()} views
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {page.avgTimeOnPage}s avg time
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <div className={`text-sm font-medium ${getSEOScoreColor(page.seoScore)}`}>
                          {page.seoScore}/100
                        </div>
                        <div className="w-16 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${
                              page.seoScore >= 80 ? 'bg-green-500' : 
                              page.seoScore >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                            }`}
                            style={{ width: `${page.seoScore}%` }}
                          ></div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900 dark:text-white">
                        {new Date(page.lastModified).toLocaleDateString()}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        by {page.author}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center gap-2 justify-end">
                        {page.status === 'published' && (
                          <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                            <Globe className="w-4 h-4" />
                          </button>
                        )}
                        <Link
                          href={`/pages/${page.slug}/edit`}
                          className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300"
                        >
                          <Edit className="w-4 h-4" />
                        </Link>
                        <button className="text-purple-600 hover:text-purple-900 dark:text-purple-400 dark:hover:text-purple-300">
                          <Copy className="w-4 h-4" />
                        </button>
                        <button className="text-orange-600 hover:text-orange-900 dark:text-orange-400 dark:hover:text-orange-300">
                          <Share2 className="w-4 h-4" />
                        </button>
                        <button className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300">
                          <MoreHorizontal className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredPages.length === 0 && (
            <div className="text-center py-12">
              <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No pages found</h3>
              <p className="text-gray-500 dark:text-gray-400">
                {searchTerm ? 'Try adjusting your search terms' : 'Get started by creating your first page'}
              </p>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default PagesPage;