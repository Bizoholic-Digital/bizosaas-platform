'use client';

import React, { useState, useEffect } from 'react';
import { 
  MessageSquare, Plus, Search, Filter, Download, RefreshCw, 
  Edit, Eye, Trash2, MoreHorizontal, Copy, Share2, Settings,
  Calendar, User, BarChart3, TrendingUp, Activity, CheckCircle,
  AlertCircle, Clock, Mail, Phone, Globe, MousePointer
} from 'lucide-react';
import Link from 'next/link';
import DashboardLayout from '../../../components/ui/dashboard-layout';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const FormsPage = () => {
  const [loading, setLoading] = useState(true);
  const [forms, setForms] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');

  useEffect(() => {
    const fetchForms = async () => {
      try {
        setLoading(true);
        // Mock API call - replace with actual Wagtail Forms API calls through Brain Hub
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setForms([
          {
            id: '1',
            name: 'Contact Form',
            slug: 'contact-form',
            type: 'Contact',
            description: 'Main contact form for customer inquiries',
            status: 'active',
            fields: [
              { name: 'name', type: 'text', required: true },
              { name: 'email', type: 'email', required: true },
              { name: 'phone', type: 'tel', required: false },
              { name: 'company', type: 'text', required: false },
              { name: 'message', type: 'textarea', required: true }
            ],
            submissions: 67,
            submissionsThisMonth: 23,
            conversionRate: 12.4,
            avgCompletionTime: 145,
            views: 540,
            abandonment: 18.5,
            lastSubmission: '2024-09-24T16:20:00Z',
            createdDate: '2024-08-01T10:00:00Z',
            author: 'Marketing Team',
            embedCode: '<iframe src="/forms/contact-form" width="100%" height="500"></iframe>',
            successMessage: 'Thank you for contacting us! We\'ll get back to you soon.',
            redirectUrl: '/thank-you',
            notificationEmail: 'admin@bizosaas.com',
            isSpamProtected: true,
            submissionTrend: [
              { month: 'Jun', submissions: 45 },
              { month: 'Jul', submissions: 52 },
              { month: 'Aug', submissions: 48 },
              { month: 'Sep', submissions: 67 }
            ]
          },
          {
            id: '2',
            name: 'Newsletter Signup',
            slug: 'newsletter-signup',
            type: 'Newsletter',
            description: 'Email newsletter subscription form',
            status: 'active',
            fields: [
              { name: 'email', type: 'email', required: true },
              { name: 'first_name', type: 'text', required: false },
              { name: 'interests', type: 'checkbox', required: false }
            ],
            submissions: 234,
            submissionsThisMonth: 89,
            conversionRate: 8.7,
            avgCompletionTime: 45,
            views: 2690,
            abandonment: 12.3,
            lastSubmission: '2024-09-24T14:30:00Z',
            createdDate: '2024-07-15T14:00:00Z',
            author: 'Content Team',
            embedCode: '<iframe src="/forms/newsletter-signup" width="100%" height="200"></iframe>',
            successMessage: 'Welcome to our newsletter!',
            redirectUrl: null,
            notificationEmail: 'newsletter@bizosaas.com',
            isSpamProtected: true,
            submissionTrend: [
              { month: 'Jun', submissions: 0 },
              { month: 'Jul', submissions: 32 },
              { month: 'Aug', submissions: 78 },
              { month: 'Sep', submissions: 124 }
            ]
          },
          {
            id: '3',
            name: 'Demo Request',
            slug: 'demo-request',
            type: 'Lead Generation',
            description: 'Product demo request form for qualified leads',
            status: 'active',
            fields: [
              { name: 'full_name', type: 'text', required: true },
              { name: 'email', type: 'email', required: true },
              { name: 'phone', type: 'tel', required: true },
              { name: 'company', type: 'text', required: true },
              { name: 'company_size', type: 'select', required: true },
              { name: 'role', type: 'select', required: true },
              { name: 'use_case', type: 'textarea', required: true },
              { name: 'timeline', type: 'select', required: false }
            ],
            submissions: 45,
            submissionsThisMonth: 18,
            conversionRate: 24.8,
            avgCompletionTime: 320,
            views: 181,
            abandonment: 35.2,
            lastSubmission: '2024-09-24T11:45:00Z',
            createdDate: '2024-08-15T09:00:00Z',
            author: 'Sales Team',
            embedCode: '<iframe src="/forms/demo-request" width="100%" height="650"></iframe>',
            successMessage: 'Thank you! Our sales team will contact you within 24 hours.',
            redirectUrl: '/demo-scheduled',
            notificationEmail: 'sales@bizosaas.com',
            isSpamProtected: true,
            submissionTrend: [
              { month: 'Jun', submissions: 0 },
              { month: 'Jul', submissions: 0 },
              { month: 'Aug', submissions: 12 },
              { month: 'Sep', submissions: 33 }
            ]
          },
          {
            id: '4',
            name: 'Support Ticket',
            slug: 'support-ticket',
            type: 'Support',
            description: 'Customer support request form',
            status: 'active',
            fields: [
              { name: 'name', type: 'text', required: true },
              { name: 'email', type: 'email', required: true },
              { name: 'priority', type: 'select', required: true },
              { name: 'category', type: 'select', required: true },
              { name: 'subject', type: 'text', required: true },
              { name: 'description', type: 'textarea', required: true },
              { name: 'attachment', type: 'file', required: false }
            ],
            submissions: 128,
            submissionsThisMonth: 34,
            conversionRate: 18.9,
            avgCompletionTime: 280,
            views: 678,
            abandonment: 22.1,
            lastSubmission: '2024-09-24T13:15:00Z',
            createdDate: '2024-07-01T08:00:00Z',
            author: 'Support Team',
            embedCode: '<iframe src="/forms/support-ticket" width="100%" height="600"></iframe>',
            successMessage: 'Support ticket created. We\'ll respond within 4 hours.',
            redirectUrl: '/support/ticket-created',
            notificationEmail: 'support@bizosaas.com',
            isSpamProtected: true,
            submissionTrend: [
              { month: 'Jun', submissions: 0 },
              { month: 'Jul', submissions: 28 },
              { month: 'Aug', submissions: 42 },
              { month: 'Sep', submissions: 58 }
            ]
          },
          {
            id: '5',
            name: 'Feedback Survey',
            slug: 'feedback-survey',
            type: 'Survey',
            description: 'Customer satisfaction feedback survey',
            status: 'draft',
            fields: [
              { name: 'rating', type: 'rating', required: true },
              { name: 'experience', type: 'radio', required: true },
              { name: 'improvements', type: 'checkbox', required: false },
              { name: 'comments', type: 'textarea', required: false },
              { name: 'recommend', type: 'radio', required: true }
            ],
            submissions: 0,
            submissionsThisMonth: 0,
            conversionRate: 0,
            avgCompletionTime: 0,
            views: 0,
            abandonment: 0,
            lastSubmission: null,
            createdDate: '2024-09-20T15:30:00Z',
            author: 'Product Team',
            embedCode: '<iframe src="/forms/feedback-survey" width="100%" height="550"></iframe>',
            successMessage: 'Thank you for your feedback!',
            redirectUrl: null,
            notificationEmail: 'feedback@bizosaas.com',
            isSpamProtected: true,
            submissionTrend: [
              { month: 'Jun', submissions: 0 },
              { month: 'Jul', submissions: 0 },
              { month: 'Aug', submissions: 0 },
              { month: 'Sep', submissions: 0 }
            ]
          }
        ]);
      } catch (error) {
        console.error('Failed to fetch forms:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchForms();
  }, []);

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      active: { color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300', icon: <CheckCircle className="w-3 h-3" />, label: 'Active' },
      inactive: { color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300', icon: <AlertCircle className="w-3 h-3" />, label: 'Inactive' },
      draft: { color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300', icon: <Edit className="w-3 h-3" />, label: 'Draft' },
      archived: { color: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300', icon: <AlertCircle className="w-3 h-3" />, label: 'Archived' }
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
      'Contact': { color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300' },
      'Newsletter': { color: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300' },
      'Lead Generation': { color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' },
      'Support': { color: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300' },
      'Survey': { color: 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-300' }
    };

    const config = typeConfig[type as keyof typeof typeConfig] || { color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300' };
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {type}
      </span>
    );
  };

  const getConversionColor = (rate: number) => {
    if (rate >= 20) return 'text-green-600';
    if (rate >= 10) return 'text-yellow-600';
    return 'text-red-600';
  };

  const filteredForms = forms.filter(form => {
    const matchesSearch = form.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         form.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         form.type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = selectedStatus === 'all' || form.status === selectedStatus;
    const matchesFilter = selectedFilter === 'all' || form.type === selectedFilter;
    return matchesSearch && matchesStatus && matchesFilter;
  });

  const stats = {
    total: forms.length,
    active: forms.filter(f => f.status === 'active').length,
    draft: forms.filter(f => f.status === 'draft').length,
    totalSubmissions: forms.reduce((sum, f) => sum + f.submissions, 0),
    totalViews: forms.reduce((sum, f) => sum + f.views, 0),
    avgConversionRate: forms.length > 0 ? (forms.reduce((sum, f) => sum + f.conversionRate, 0) / forms.length) : 0,
    thisMonthSubmissions: forms.reduce((sum, f) => sum + f.submissionsThisMonth, 0)
  };

  if (loading) {
    return (
      <DashboardLayout title="Forms" description="Manage your website forms">
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
    <DashboardLayout title="Forms" description="Manage your website forms and submissions">
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Form Management</h1>
            <p className="text-gray-600 dark:text-gray-300">Create, manage and analyze your website forms</p>
          </div>
          <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
              <BarChart3 className="w-4 h-4" />
              Analytics
            </button>
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
              <Download className="w-4 h-4" />
              Export Data
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              <Plus className="w-4 h-4" />
              Create Form
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-7 gap-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <MessageSquare className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Total Forms</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Active</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.active}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-lg">
                <Activity className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Submissions</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.totalSubmissions}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-orange-100 dark:bg-orange-900 rounded-lg">
                <Calendar className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">This Month</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.thisMonthSubmissions}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-indigo-100 dark:bg-indigo-900 rounded-lg">
                <Eye className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Total Views</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.totalViews.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-pink-100 dark:bg-pink-900 rounded-lg">
                <TrendingUp className="w-6 h-6 text-pink-600 dark:text-pink-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Avg Conversion</p>
                <p className={`text-2xl font-bold ${getConversionColor(stats.avgConversionRate)}`}>
                  {stats.avgConversionRate.toFixed(1)}%
                </p>
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
        </div>

        {/* Filters and Search */}
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search forms by name, description, or type..."
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
              <option value="active">Active</option>
              <option value="draft">Draft</option>
              <option value="inactive">Inactive</option>
              <option value="archived">Archived</option>
            </select>
            <select
              value={selectedFilter}
              onChange={(e) => setSelectedFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Types</option>
              <option value="Contact">Contact</option>
              <option value="Newsletter">Newsletter</option>
              <option value="Lead Generation">Lead Generation</option>
              <option value="Support">Support</option>
              <option value="Survey">Survey</option>
            </select>
            <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
              <RefreshCw className="w-4 h-4 text-gray-600 dark:text-gray-300" />
            </button>
          </div>
        </div>

        {/* Forms Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredForms.map((form) => (
            <div key={form.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{form.name}</h3>
                    {getStatusBadge(form.status)}
                  </div>
                  <div className="flex items-center gap-2 mb-3">
                    {getTypeBadge(form.type)}
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {form.fields.length} fields
                    </span>
                  </div>
                  <p className="text-gray-600 dark:text-gray-300 text-sm">{form.description}</p>
                </div>
                <div className="flex items-center gap-2 ml-4">
                  <button className="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900 rounded-lg">
                    <Eye className="w-4 h-4" />
                  </button>
                  <button className="p-2 text-green-600 hover:bg-green-50 dark:hover:bg-green-900 rounded-lg">
                    <Edit className="w-4 h-4" />
                  </button>
                  <button className="p-2 text-purple-600 hover:bg-purple-50 dark:hover:bg-purple-900 rounded-lg">
                    <Settings className="w-4 h-4" />
                  </button>
                  <button className="p-2 text-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg">
                    <MoreHorizontal className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Metrics */}
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">{form.submissions}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">Total Submissions</div>
                  <div className="text-xs text-green-600 dark:text-green-400 mt-1">
                    +{form.submissionsThisMonth} this month
                  </div>
                </div>
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                  <div className={`text-2xl font-bold ${getConversionColor(form.conversionRate)}`}>
                    {form.conversionRate.toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">Conversion Rate</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {form.views} views
                  </div>
                </div>
              </div>

              {/* Additional Metrics */}
              <div className="grid grid-cols-3 gap-3 mb-4 text-center text-sm">
                <div>
                  <div className="font-semibold text-gray-900 dark:text-white">
                    {Math.floor(form.avgCompletionTime / 60)}m {form.avgCompletionTime % 60}s
                  </div>
                  <div className="text-gray-500 dark:text-gray-400">Avg Time</div>
                </div>
                <div>
                  <div className="font-semibold text-gray-900 dark:text-white">
                    {form.abandonment.toFixed(1)}%
                  </div>
                  <div className="text-gray-500 dark:text-gray-400">Abandonment</div>
                </div>
                <div>
                  <div className="font-semibold text-gray-900 dark:text-white">
                    {form.isSpamProtected ? 'Protected' : 'Unprotected'}
                  </div>
                  <div className="text-gray-500 dark:text-gray-400">Spam Filter</div>
                </div>
              </div>

              {/* Submission Trend */}
              {form.submissionTrend && form.submissionTrend.some((d: any) => d.submissions > 0) && (
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Submission Trend</h4>
                  <ResponsiveContainer width="100%" height={80}>
                    <LineChart data={form.submissionTrend}>
                      <Line 
                        type="monotone" 
                        dataKey="submissions" 
                        stroke="#3B82F6" 
                        strokeWidth={2}
                        dot={{ fill: '#3B82F6', r: 3 }}
                      />
                      <XAxis dataKey="month" hide />
                      <YAxis hide />
                      <Tooltip />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}

              {/* Footer */}
              <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-400">
                  <div className="flex items-center gap-1">
                    <User className="w-4 h-4" />
                    <span>{form.author}</span>
                  </div>
                  {form.lastSubmission && (
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      <span>Last: {new Date(form.lastSubmission).toLocaleDateString()}</span>
                    </div>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300 text-sm">
                    <Copy className="w-4 h-4" />
                  </button>
                  <button className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300 text-sm">
                    <Share2 className="w-4 h-4" />
                  </button>
                  <button className="text-purple-600 hover:text-purple-900 dark:text-purple-400 dark:hover:text-purple-300 text-sm">
                    <Download className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredForms.length === 0 && (
          <div className="text-center py-12">
            <MessageSquare className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No forms found</h3>
            <p className="text-gray-500 dark:text-gray-400">
              {searchTerm ? 'Try adjusting your search terms' : 'Get started by creating your first form'}
            </p>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default FormsPage;