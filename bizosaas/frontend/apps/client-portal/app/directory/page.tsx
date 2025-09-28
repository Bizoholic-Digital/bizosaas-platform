'use client';

import React, { useState, useEffect } from 'react';
import { 
  Building2, Tag, MessageSquare, TrendingUp, Plus, 
  Search, Filter, Download, RefreshCw, Edit, Eye, 
  Trash2, MoreHorizontal, Star, MapPin, Globe,
  Phone, Mail, Clock, Users, BarChart3
} from 'lucide-react';
import DashboardLayout from '../../components/ui/dashboard-layout';

interface DirectoryTabs {
  [key: string]: React.ReactNode;
}

const BusinessDirectoryPage = () => {
  const [activeTab, setActiveTab] = useState('businesses');
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const fetchDirectoryData = async () => {
      try {
        setLoading(true);
        // Mock API call - replace with actual Business Directory API calls through Brain Hub
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setData({
          businesses: [
            {
              id: '1',
              name: 'Acme Corporation',
              category: 'Technology',
              address: '123 Main St, New York, NY 10001',
              phone: '+1-555-0123',
              email: 'contact@acme.com',
              website: 'https://acme.com',
              rating: 4.5,
              reviews: 89,
              verified: true,
              status: 'active',
              owner: 'John Smith',
              lastUpdated: '2024-09-24T10:30:00Z'
            },
            {
              id: '2',
              name: 'Local Restaurant',
              category: 'Food & Beverage',
              address: '456 Oak Ave, Los Angeles, CA 90210',
              phone: '+1-555-0124',
              email: 'info@localrestaurant.com',
              website: 'https://localrestaurant.com',
              rating: 4.2,
              reviews: 234,
              verified: false,
              status: 'pending',
              owner: 'Maria Garcia',
              lastUpdated: '2024-09-23T15:45:00Z'
            },
            {
              id: '3',
              name: 'Design Studio Pro',
              category: 'Creative Services',
              address: '789 Creative Blvd, San Francisco, CA 94102',
              phone: '+1-555-0125',
              email: 'hello@designstudiopro.com',
              website: 'https://designstudiopro.com',
              rating: 4.8,
              reviews: 67,
              verified: true,
              status: 'active',
              owner: 'Sarah Johnson',
              lastUpdated: '2024-09-24T09:15:00Z'
            }
          ],
          categories: [
            {
              id: '1',
              name: 'Technology',
              businessCount: 45,
              description: 'Software, hardware, and IT services',
              icon: '💻',
              status: 'active'
            },
            {
              id: '2',
              name: 'Food & Beverage',
              businessCount: 78,
              description: 'Restaurants, cafes, and food services',
              icon: '🍕',
              status: 'active'
            },
            {
              id: '3',
              name: 'Creative Services',
              businessCount: 32,
              description: 'Design, marketing, and creative agencies',
              icon: '🎨',
              status: 'active'
            },
            {
              id: '4',
              name: 'Healthcare',
              businessCount: 56,
              description: 'Medical practices and health services',
              icon: '🏥',
              status: 'active'
            }
          ],
          reviews: [
            {
              id: '1',
              businessId: '1',
              businessName: 'Acme Corporation',
              reviewerName: 'Alice Smith',
              rating: 5,
              comment: 'Excellent service and professional team. Highly recommended!',
              date: '2024-09-24T14:20:00Z',
              status: 'approved',
              helpful: 12
            },
            {
              id: '2',
              businessId: '2',
              businessName: 'Local Restaurant',
              reviewerName: 'Bob Wilson',
              rating: 4,
              comment: 'Great food and atmosphere. Will definitely come back.',
              date: '2024-09-23T18:30:00Z',
              status: 'pending',
              helpful: 3
            },
            {
              id: '3',
              businessId: '3',
              businessName: 'Design Studio Pro',
              reviewerName: 'Carol Davis',
              rating: 5,
              comment: 'Amazing design work! They understood our vision perfectly.',
              date: '2024-09-22T11:45:00Z',
              status: 'approved',
              helpful: 8
            }
          ],
          metrics: {
            totalBusinesses: 245,
            verifiedBusinesses: 189,
            pendingBusinesses: 23,
            totalCategories: 18,
            totalReviews: 1840,
            averageRating: 4.3,
            monthlyViews: 25600
          }
        });
      } catch (error) {
        console.error('Failed to fetch directory data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDirectoryData();
  }, []);

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      active: { color: 'bg-green-100 text-green-800', label: 'Active' },
      pending: { color: 'bg-yellow-100 text-yellow-800', label: 'Pending' },
      inactive: { color: 'bg-red-100 text-red-800', label: 'Inactive' },
      approved: { color: 'bg-green-100 text-green-800', label: 'Approved' },
      rejected: { color: 'bg-red-100 text-red-800', label: 'Rejected' }
    };

    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.pending;
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const BusinessesTab = () => (
    <div className="space-y-6">
      {/* Businesses Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Business Listings</h2>
          <p className="text-sm text-gray-600 dark:text-gray-300">Manage business directory listings</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-600 dark:hover:bg-gray-700">
            <Filter className="w-4 h-4" />
            Filter
          </button>
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-600 dark:hover:bg-gray-700">
            <Download className="w-4 h-4" />
            Export
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <Plus className="w-4 h-4" />
            Add Business
          </button>
        </div>
      </div>

      {/* Business Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <Building2 className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Total Businesses</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.totalBusinesses}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
              <Star className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Verified</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.verifiedBusinesses}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-100 dark:bg-yellow-900 rounded-lg">
              <Clock className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Pending</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.pendingBusinesses}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <Eye className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Monthly Views</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.monthlyViews?.toLocaleString()}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Businesses Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">All Businesses</h3>
            <div className="flex items-center gap-3">
              <div className="relative">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search businesses..."
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
                  Business
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Rating
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Owner
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Last Updated
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {data?.businesses?.map((business: any) => (
                <tr key={business.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                          <Building2 className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="flex items-center gap-2">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">{business.name}</div>
                          {business.verified && (
                            <Star className="w-4 h-4 text-yellow-500 fill-current" />
                          )}
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
                          <MapPin className="w-3 h-3" />
                          {business.address}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {business.category}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`w-4 h-4 ${
                              i < Math.floor(business.rating) 
                                ? 'text-yellow-400 fill-current' 
                                : 'text-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                      <span className="ml-2 text-sm text-gray-600 dark:text-gray-400">
                        {business.rating} ({business.reviews})
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStatusBadge(business.status)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {business.owner}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {new Date(business.lastUpdated).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center gap-2 justify-end">
                      <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300">
                        <Edit className="w-4 h-4" />
                      </button>
                      <button className="text-purple-600 hover:text-purple-900 dark:text-purple-400 dark:hover:text-purple-300">
                        <Phone className="w-4 h-4" />
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
      </div>
    </div>
  );

  const CategoriesTab = () => (
    <div className="space-y-6">
      {/* Categories Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Business Categories</h2>
          <p className="text-sm text-gray-600 dark:text-gray-300">Organize businesses by industry and type</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          <Plus className="w-4 h-4" />
          Add Category
        </button>
      </div>

      {/* Categories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data?.categories?.map((category: any) => (
          <div key={category.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="text-2xl">{category.icon}</div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{category.name}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">{category.businessCount} businesses</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button className="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900 rounded-lg">
                  <Edit className="w-4 h-4" />
                </button>
                <button className="p-2 text-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg">
                  <MoreHorizontal className="w-4 h-4" />
                </button>
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">{category.description}</p>
            <div className="flex items-center justify-between">
              {getStatusBadge(category.status)}
              <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                View Businesses →
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const ReviewsTab = () => (
    <div className="space-y-6">
      {/* Reviews Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Customer Reviews</h2>
          <p className="text-sm text-gray-600 dark:text-gray-300">Moderate and manage customer feedback</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-600 dark:hover:bg-gray-700">
            <Filter className="w-4 h-4" />
            Filter
          </button>
        </div>
      </div>

      {/* Reviews List */}
      <div className="space-y-4">
        {data?.reviews?.map((review: any) => (
          <div key={review.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white">{review.businessName}</h3>
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-4 h-4 ${
                          i < review.rating 
                            ? 'text-yellow-400 fill-current' 
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  {getStatusBadge(review.status)}
                </div>
                <p className="text-gray-600 dark:text-gray-300 mb-3">{review.comment}</p>
                <div className="flex items-center gap-6 text-sm text-gray-500 dark:text-gray-400">
                  <div className="flex items-center gap-1">
                    <Users className="w-4 h-4" />
                    <span>{review.reviewerName}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    <span>{new Date(review.date).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <TrendingUp className="w-4 h-4" />
                    <span>{review.helpful} helpful</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2 ml-6">
                <button className="px-3 py-1 text-green-600 bg-green-50 hover:bg-green-100 rounded text-sm dark:bg-green-900 dark:hover:bg-green-800">
                  Approve
                </button>
                <button className="px-3 py-1 text-red-600 bg-red-50 hover:bg-red-100 rounded text-sm dark:bg-red-900 dark:hover:bg-red-800">
                  Reject
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

  const tabs: DirectoryTabs = {
    businesses: <BusinessesTab />,
    categories: <CategoriesTab />,
    reviews: <ReviewsTab />,
    analytics: <div className="p-6 text-center text-gray-500">Directory analytics coming soon...</div>
  };

  const tabItems = [
    { id: 'businesses', name: 'Businesses', icon: <Building2 className="w-4 h-4" />, badge: data?.businesses?.length },
    { id: 'categories', name: 'Categories', icon: <Tag className="w-4 h-4" />, badge: data?.categories?.length },
    { id: 'reviews', name: 'Reviews', icon: <MessageSquare className="w-4 h-4" />, badge: data?.reviews?.length },
    { id: 'analytics', name: 'Analytics', icon: <TrendingUp className="w-4 h-4" /> }
  ];

  if (loading) {
    return (
      <DashboardLayout title="Business Directory" description="Manage your business directory listings and reviews">
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
    <DashboardLayout title="Business Directory" description="Manage your business listings, categories, and customer reviews">
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

export default BusinessDirectoryPage;