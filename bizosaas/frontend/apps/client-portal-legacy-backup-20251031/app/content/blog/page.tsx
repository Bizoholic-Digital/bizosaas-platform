'use client';

import React, { useState, useEffect } from 'react';
import { 
  Newspaper, Plus, Search, Filter, Download, RefreshCw, 
  Edit, Eye, Trash2, MoreHorizontal, Calendar, User,
  Tag, MessageSquare, Heart, Share2, Globe, Clock,
  CheckCircle, AlertCircle, TrendingUp, BarChart3
} from 'lucide-react';
import Link from 'next/link';
import DashboardLayout from '../../../components/ui/dashboard-layout';

const BlogPage = () => {
  const [loading, setLoading] = useState(true);
  const [posts, setPosts] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true);
        // Mock API call - replace with actual Wagtail CMS API calls through Brain Hub
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setPosts([
          {
            id: '1',
            title: 'Digital Marketing Trends 2024',
            slug: 'digital-marketing-trends-2024',
            excerpt: 'Discover the latest trends shaping digital marketing in 2024, from AI-powered personalization to voice search optimization.',
            content: 'Lorem ipsum dolor sit amet...',
            status: 'published',
            category: 'Marketing',
            author: 'Marketing Team',
            authorAvatar: 'MT',
            publishDate: '2024-09-23T10:00:00Z',
            lastModified: '2024-09-24T08:30:00Z',
            featuredImage: '/images/blog/digital-trends-2024.jpg',
            views: 2340,
            uniqueViews: 1890,
            readTime: 8,
            likes: 45,
            shares: 23,
            comments: 15,
            tags: ['Marketing', 'Trends', 'Digital', 'AI'],
            seoScore: 92,
            wordCount: 1850,
            avgTimeOnPage: 245,
            bounceRate: 25
          },
          {
            id: '2',
            title: 'SEO Best Practices Guide',
            slug: 'seo-best-practices-guide',
            excerpt: 'A comprehensive guide to improving your search rankings with proven SEO strategies and techniques.',
            content: 'Lorem ipsum dolor sit amet...',
            status: 'published',
            category: 'SEO',
            author: 'SEO Specialist',
            authorAvatar: 'SS',
            publishDate: '2024-09-22T14:30:00Z',
            lastModified: '2024-09-22T14:45:00Z',
            featuredImage: '/images/blog/seo-guide.jpg',
            views: 1890,
            uniqueViews: 1520,
            readTime: 12,
            likes: 67,
            shares: 34,
            comments: 8,
            tags: ['SEO', 'Guide', 'Best Practices', 'Rankings'],
            seoScore: 88,
            wordCount: 2400,
            avgTimeOnPage: 312,
            bounceRate: 18
          },
          {
            id: '3',
            title: 'Social Media Strategy 2024',
            slug: 'social-media-strategy-2024',
            excerpt: 'How to create an effective social media strategy that drives engagement and builds brand awareness.',
            content: 'Lorem ipsum dolor sit amet...',
            status: 'draft',
            category: 'Social Media',
            author: 'Social Media Manager',
            authorAvatar: 'SM',
            publishDate: null,
            lastModified: '2024-09-24T11:15:00Z',
            featuredImage: null,
            views: 0,
            uniqueViews: 0,
            readTime: 6,
            likes: 0,
            shares: 0,
            comments: 0,
            tags: ['Social Media', 'Strategy', 'Engagement'],
            seoScore: 74,
            wordCount: 1200,
            avgTimeOnPage: 0,
            bounceRate: 0
          },
          {
            id: '4',
            title: 'Email Marketing Automation',
            slug: 'email-marketing-automation',
            excerpt: 'Learn how to set up effective email marketing automation campaigns that nurture leads and drive conversions.',
            content: 'Lorem ipsum dolor sit amet...',
            status: 'scheduled',
            category: 'Email Marketing',
            author: 'Email Specialist',
            authorAvatar: 'ES',
            publishDate: '2024-09-25T09:00:00Z',
            lastModified: '2024-09-23T16:20:00Z',
            featuredImage: '/images/blog/email-automation.jpg',
            views: 0,
            uniqueViews: 0,
            readTime: 10,
            likes: 0,
            shares: 0,
            comments: 0,
            tags: ['Email', 'Automation', 'Marketing', 'Conversions'],
            seoScore: 85,
            wordCount: 1950,
            avgTimeOnPage: 0,
            bounceRate: 0
          },
          {
            id: '5',
            title: 'Content Marketing ROI',
            slug: 'content-marketing-roi',
            excerpt: 'Measuring the return on investment of your content marketing efforts and optimizing for better results.',
            content: 'Lorem ipsum dolor sit amet...',
            status: 'published',
            category: 'Content Marketing',
            author: 'Content Strategist',
            authorAvatar: 'CS',
            publishDate: '2024-09-20T13:00:00Z',
            lastModified: '2024-09-21T09:30:00Z',
            featuredImage: '/images/blog/content-roi.jpg',
            views: 1456,
            uniqueViews: 1180,
            readTime: 9,
            likes: 38,
            shares: 19,
            comments: 12,
            tags: ['Content Marketing', 'ROI', 'Analytics', 'Strategy'],
            seoScore: 90,
            wordCount: 1680,
            avgTimeOnPage: 287,
            bounceRate: 22
          },
          {
            id: '6',
            title: 'PPC Campaign Optimization',
            slug: 'ppc-campaign-optimization',
            excerpt: 'Advanced techniques for optimizing your pay-per-click campaigns for maximum ROI and performance.',
            content: 'Lorem ipsum dolor sit amet...',
            status: 'published',
            category: 'PPC',
            author: 'PPC Expert',
            authorAvatar: 'PE',
            publishDate: '2024-09-19T11:00:00Z',
            lastModified: '2024-09-19T11:15:00Z',
            featuredImage: '/images/blog/ppc-optimization.jpg',
            views: 987,
            uniqueViews: 820,
            readTime: 7,
            likes: 29,
            shares: 14,
            comments: 6,
            tags: ['PPC', 'Google Ads', 'Optimization', 'ROI'],
            seoScore: 87,
            wordCount: 1420,
            avgTimeOnPage: 198,
            bounceRate: 28
          }
        ]);
      } catch (error) {
        console.error('Failed to fetch posts:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
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

  const getCategoryBadge = (category: string) => {
    const categoryColors = {
      'Marketing': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
      'SEO': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
      'Social Media': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
      'Email Marketing': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
      'Content Marketing': 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-300',
      'PPC': 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300'
    };

    const color = categoryColors[category as keyof typeof categoryColors] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${color}`}>
        {category}
      </span>
    );
  };

  const getSEOScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const filteredPosts = posts.filter(post => {
    const matchesSearch = post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         post.excerpt.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         post.author.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = selectedFilter === 'all' || post.status === selectedFilter;
    const matchesCategory = selectedCategory === 'all' || post.category === selectedCategory;
    return matchesSearch && matchesStatus && matchesCategory;
  });

  const stats = {
    total: posts.length,
    published: posts.filter(p => p.status === 'published').length,
    draft: posts.filter(p => p.status === 'draft').length,
    scheduled: posts.filter(p => p.status === 'scheduled').length,
    totalViews: posts.reduce((sum, p) => sum + p.views, 0),
    totalEngagement: posts.reduce((sum, p) => sum + p.likes + p.comments + p.shares, 0),
    avgSEOScore: posts.length > 0 ? Math.round(posts.reduce((sum, p) => sum + p.seoScore, 0) / posts.length) : 0
  };

  if (loading) {
    return (
      <DashboardLayout title="Blog Posts" description="Manage your blog content">
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
    <DashboardLayout title="Blog Posts" description="Manage your blog content and articles">
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Blog Management</h1>
            <p className="text-gray-600 dark:text-gray-300">Create, edit and manage your blog posts</p>
          </div>
          <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
              <Calendar className="w-4 h-4" />
              Schedule
            </button>
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
              <BarChart3 className="w-4 h-4" />
              Analytics
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              <Plus className="w-4 h-4" />
              New Post
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-7 gap-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <Newspaper className="w-6 h-6 text-blue-600 dark:text-blue-400" />
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
              <div className="p-3 bg-orange-100 dark:bg-orange-900 rounded-lg">
                <Heart className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Engagement</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.totalEngagement}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-indigo-100 dark:bg-indigo-900 rounded-lg">
                <TrendingUp className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Avg SEO</p>
                <p className={`text-2xl font-bold ${getSEOScoreColor(stats.avgSEOScore)}`}>{stats.avgSEOScore}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-pink-100 dark:bg-pink-900 rounded-lg">
                <Clock className="w-6 h-6 text-pink-600 dark:text-pink-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Scheduled</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.scheduled}</p>
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
                  placeholder="Search posts by title, content, or author..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 w-full border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            <select
              value={selectedFilter}
              onChange={(e) => setSelectedFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Status</option>
              <option value="published">Published</option>
              <option value="draft">Draft</option>
              <option value="scheduled">Scheduled</option>
              <option value="archived">Archived</option>
            </select>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Categories</option>
              <option value="Marketing">Marketing</option>
              <option value="SEO">SEO</option>
              <option value="Social Media">Social Media</option>
              <option value="Email Marketing">Email Marketing</option>
              <option value="Content Marketing">Content Marketing</option>
              <option value="PPC">PPC</option>
            </select>
            <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
              <RefreshCw className="w-4 h-4 text-gray-600 dark:text-gray-300" />
            </button>
          </div>
        </div>

        {/* Posts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredPosts.map((post) => (
            <div key={post.id} className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
              {/* Featured Image */}
              {post.featuredImage ? (
                <div className="h-48 bg-gray-200 dark:bg-gray-700 bg-cover bg-center" style={{ backgroundImage: `url(${post.featuredImage})` }}>
                </div>
              ) : (
                <div className="h-48 bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                  <Newspaper className="w-12 h-12 text-gray-400" />
                </div>
              )}

              <div className="p-6">
                {/* Header */}
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    {getCategoryBadge(post.category)}
                    {getStatusBadge(post.status)}
                  </div>
                  <div className="flex items-center gap-2">
                    <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                      <Eye className="w-4 h-4" />
                    </button>
                    <button className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300">
                      <Edit className="w-4 h-4" />
                    </button>
                    <button className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300">
                      <MoreHorizontal className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Title and Excerpt */}
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2">
                  {post.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-3">
                  {post.excerpt}
                </p>

                {/* Author and Date */}
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                    {post.authorAvatar}
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-900 dark:text-white">{post.author}</div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {post.publishDate 
                        ? new Date(post.publishDate).toLocaleDateString()
                        : `Modified ${new Date(post.lastModified).toLocaleDateString()}`
                      }
                    </div>
                  </div>
                </div>

                {/* Metrics */}
                <div className="grid grid-cols-4 gap-2 mb-4 text-center">
                  <div>
                    <div className="text-sm font-semibold text-gray-900 dark:text-white">
                      {post.views.toLocaleString()}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">Views</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-gray-900 dark:text-white">
                      {post.likes}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">Likes</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-gray-900 dark:text-white">
                      {post.comments}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">Comments</div>
                  </div>
                  <div>
                    <div className={`text-sm font-semibold ${getSEOScoreColor(post.seoScore)}`}>
                      {post.seoScore}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">SEO</div>
                  </div>
                </div>

                {/* Tags */}
                <div className="flex flex-wrap gap-1 mb-4">
                  {post.tags.slice(0, 3).map((tag: string) => (
                    <span key={tag} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded dark:bg-gray-700 dark:text-gray-300">
                      {tag}
                    </span>
                  ))}
                  {post.tags.length > 3 && (
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded dark:bg-gray-700 dark:text-gray-300">
                      +{post.tags.length - 3}
                    </span>
                  )}
                </div>

                {/* Read Time and Word Count */}
                <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                  <div className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    <span>{post.readTime} min read</span>
                  </div>
                  <div>{post.wordCount} words</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredPosts.length === 0 && (
          <div className="text-center py-12">
            <Newspaper className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No blog posts found</h3>
            <p className="text-gray-500 dark:text-gray-400">
              {searchTerm ? 'Try adjusting your search terms' : 'Get started by creating your first blog post'}
            </p>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default BlogPage;