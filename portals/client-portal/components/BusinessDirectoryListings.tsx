'use client';

import React, { useState, useEffect } from 'react';
import { Store, Star, Eye, Phone, Globe, MapPin, Edit, ExternalLink, Plus } from 'lucide-react';

interface BusinessListing {
  id: string;
  name: string;
  description: string;
  category: {
    id: string;
    name: string;
    slug: string;
  };
  subcategory: string;
  location: {
    address: string;
    city: string;
    state: string;
    zipCode: string;
    country: string;
  };
  contact: {
    phone: string;
    email: string;
    website?: string;
  };
  rating: number;
  reviewCount: number;
  status: string;
  verified: boolean;
  featured: boolean;
  images: string[];
  tags: string[];
  analytics: {
    views: number;
    clicks: number;
    callClicks: number;
    websiteClicks: number;
    directionsClicks: number;
  };
  lastUpdated: string;
  createdAt: string;
}

interface ListingsData {
  listings: BusinessListing[];
  total: number;
  page: number;
  limit: number;
}

export function BusinessDirectoryListings() {
  const [data, setData] = useState<ListingsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const response = await fetch('/api/brain/business-directory/listings');
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('Error fetching business listings:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchListings();
  }, []);

  const getStatusBadge = (status: string) => {
    const statusStyles = {
      active: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
      pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
      inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400',
      suspended: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
    };

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusStyles[status as keyof typeof statusStyles] || statusStyles.inactive}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="flex justify-between items-center">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-48"></div>
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-36"></div>
        </div>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
              <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 dark:text-gray-400">
          Failed to load business listings
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">My Business Listings</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {data.total} total listings
          </p>
        </div>
        <div className="flex space-x-3">
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="pending">Pending</option>
            <option value="inactive">Inactive</option>
          </select>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center">
            <Plus className="w-4 h-4 mr-2" />
            Add New Listing
          </button>
        </div>
      </div>

      <div className="grid gap-6">
        {data.listings.map((listing) => (
          <div key={listing.id} className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-start space-x-4">
                <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Store className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{listing.name}</h3>
                    {listing.verified && (
                      <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                        Verified
                      </span>
                    )}
                    {listing.featured && (
                      <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded-full">
                        Featured
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {listing.subcategory} • {listing.location.city}, {listing.location.state}
                  </p>
                  <div className="flex items-center space-x-4 text-sm">
                    <div className="flex items-center">
                      <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
                      <span className="font-medium">{listing.rating}</span>
                      <span className="text-gray-500 dark:text-gray-400 ml-1">({listing.reviewCount} reviews)</span>
                    </div>
                    <div className="flex items-center">
                      <Eye className="w-4 h-4 text-gray-400 mr-1" />
                      <span>{listing.analytics.views.toLocaleString()} views</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex space-x-2">
                <button className="text-blue-600 hover:text-blue-700 dark:text-blue-400 text-sm p-2 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded">
                  <Edit className="w-4 h-4" />
                </button>
                <button className="text-gray-600 hover:text-gray-700 dark:text-gray-400 text-sm p-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded">
                  <ExternalLink className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
              {listing.description}
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="flex items-center text-sm">
                <span className="text-gray-500 dark:text-gray-400 mr-2">Status:</span>
                {getStatusBadge(listing.status)}
              </div>
              <div className="flex items-center text-sm">
                <Phone className="w-4 h-4 text-gray-400 mr-2" />
                <span className="text-gray-600 dark:text-gray-400">{listing.contact.phone}</span>
              </div>
              {listing.contact.website && (
                <div className="flex items-center text-sm">
                  <Globe className="w-4 h-4 text-gray-400 mr-2" />
                  <a 
                    href={listing.contact.website} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-700 dark:text-blue-400 truncate"
                  >
                    {listing.contact.website.replace(/^https?:\/\//, '')}
                  </a>
                </div>
              )}
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded">
                <div className="text-gray-500 dark:text-gray-400 text-xs">Total Clicks</div>
                <div className="font-semibold text-gray-900 dark:text-white">{listing.analytics.clicks}</div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded">
                <div className="text-gray-500 dark:text-gray-400 text-xs">Phone Clicks</div>
                <div className="font-semibold text-gray-900 dark:text-white">{listing.analytics.callClicks}</div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded">
                <div className="text-gray-500 dark:text-gray-400 text-xs">Website Clicks</div>
                <div className="font-semibold text-gray-900 dark:text-white">{listing.analytics.websiteClicks}</div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded">
                <div className="text-gray-500 dark:text-gray-400 text-xs">Directions</div>
                <div className="font-semibold text-gray-900 dark:text-white">{listing.analytics.directionsClicks}</div>
              </div>
            </div>

            <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div className="flex flex-wrap gap-2">
                {listing.tags.slice(0, 3).map((tag) => (
                  <span key={tag} className="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 text-xs rounded">
                    {tag}
                  </span>
                ))}
                {listing.tags.length > 3 && (
                  <span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 text-xs rounded">
                    +{listing.tags.length - 3} more
                  </span>
                )}
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Updated {new Date(listing.lastUpdated).toLocaleDateString()}
              </div>
            </div>
          </div>
        ))}
      </div>

      {data.total === 0 && (
        <div className="text-center py-12">
          <Store className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No listings yet</h3>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Create your first business listing to get started in the directory.
          </p>
          <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 flex items-center mx-auto">
            <Plus className="w-5 h-5 mr-2" />
            Create Your First Listing
          </button>
        </div>
      )}
    </div>
  );
}