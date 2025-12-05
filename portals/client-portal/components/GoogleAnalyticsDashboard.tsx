'use client';

import React, { useState, useEffect } from 'react';
import { 
  BarChart3, TrendingUp, TrendingDown, Eye, 
  Phone, Navigation, Star, Calendar, MapPin,
  Users, MousePointer, Clock, Filter, Download
} from 'lucide-react';

interface PeriodStats {
  current_period: number;
  previous_period: number;
  change_percent: number;
}

interface LocationPerformance {
  id: string;
  name: string;
  views: number;
  actions: number;
  rating: number;
  reviews: number;
}

interface AnalyticsOverview {
  total_locations: number;
  active_locations: number;
  verified_locations: number;
  total_views: number;
  total_actions: number;
  average_rating: number;
}

interface AnalyticsData {
  overview: AnalyticsOverview;
  period_stats: {
    views: PeriodStats;
    actions: PeriodStats;
    calls: PeriodStats;
    direction_requests: PeriodStats;
  };
  top_performing_locations: LocationPerformance[];
  source?: string;
}

export function GoogleAnalyticsDashboard() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState('30d');
  const [selectedMetric, setSelectedMetric] = useState('views');

  useEffect(() => {
    fetchAnalytics();
  }, [dateRange]);

  const fetchAnalytics = async () => {
    try {
      const response = await fetch(`/api/brain/business-directory/google/analytics/stats?period=${dateRange}`);
      const data: AnalyticsData = await response.json();
      setAnalytics(data);
    } catch (error) {
      console.error('Error fetching Google analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  const formatPercentage = (percent: number) => {
    const isPositive = percent >= 0;
    return {
      value: Math.abs(percent).toFixed(1),
      isPositive,
      color: isPositive ? 'text-green-600' : 'text-red-600',
      bgColor: isPositive ? 'bg-green-100 dark:bg-green-900/30' : 'bg-red-100 dark:bg-red-900/30',
      icon: isPositive ? TrendingUp : TrendingDown
    };
  };

  const MetricCard = ({ 
    title, 
    current, 
    previous, 
    change, 
    icon: Icon, 
    bgColor 
  }: { 
    title: string;
    current: number;
    previous: number;
    change: number;
    icon: any;
    bgColor: string;
  }) => {
    const changeData = formatPercentage(change);
    const ChangeIcon = changeData.icon;

    return (
      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-between mb-4">
          <div className={`w-12 h-12 ${bgColor} rounded-lg flex items-center justify-center`}>
            <Icon className="w-6 h-6" />
          </div>
          <div className={`flex items-center px-2 py-1 rounded-full text-xs font-medium ${changeData.bgColor} ${changeData.color}`}>
            <ChangeIcon className="w-3 h-3 mr-1" />
            {changeData.value}%
          </div>
        </div>
        
        <div className="space-y-2">
          <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</h3>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {formatNumber(current)}
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            vs {formatNumber(previous)} last period
          </p>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded mb-4"></div>
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                <div className="h-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 dark:text-gray-400">
          Failed to load Google analytics data
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header and Controls */}
      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Google Business Analytics
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Monitor your Google Business Profile performance and customer interactions.
            </p>
          </div>
          
          <div className="flex items-center space-x-3">
            <select 
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
              <option value="1y">Last year</option>
            </select>
            
            <button className="p-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
            <div className="flex items-center">
              <MapPin className="w-8 h-8 text-blue-600 dark:text-blue-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Locations
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {analytics.overview.total_locations}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
            <div className="flex items-center">
              <Eye className="w-8 h-8 text-green-600 dark:text-green-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Total Views
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {formatNumber(analytics.overview.total_views)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
            <div className="flex items-center">
              <MousePointer className="w-8 h-8 text-purple-600 dark:text-purple-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Actions
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {formatNumber(analytics.overview.total_actions)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
            <div className="flex items-center">
              <Star className="w-8 h-8 text-yellow-600 dark:text-yellow-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Avg Rating
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {analytics.overview.average_rating.toFixed(1)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg">
            <div className="flex items-center">
              <Users className="w-8 h-8 text-indigo-600 dark:text-indigo-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Active
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {analytics.overview.active_locations}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg">
            <div className="flex items-center">
              <Calendar className="w-8 h-8 text-orange-600 dark:text-orange-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Verified
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {analytics.overview.verified_locations}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Profile Views"
          current={analytics.period_stats.views.current_period}
          previous={analytics.period_stats.views.previous_period}
          change={analytics.period_stats.views.change_percent}
          icon={Eye}
          bgColor="bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400"
        />

        <MetricCard
          title="Customer Actions"
          current={analytics.period_stats.actions.current_period}
          previous={analytics.period_stats.actions.previous_period}
          change={analytics.period_stats.actions.change_percent}
          icon={MousePointer}
          bgColor="bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400"
        />

        <MetricCard
          title="Phone Calls"
          current={analytics.period_stats.calls.current_period}
          previous={analytics.period_stats.calls.previous_period}
          change={analytics.period_stats.calls.change_percent}
          icon={Phone}
          bgColor="bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400"
        />

        <MetricCard
          title="Direction Requests"
          current={analytics.period_stats.direction_requests.current_period}
          previous={analytics.period_stats.direction_requests.previous_period}
          change={analytics.period_stats.direction_requests.change_percent}
          icon={Navigation}
          bgColor="bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400"
        />
      </div>

      {/* Top Performing Locations */}
      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Top Performing Locations
          </h3>
          
          <select 
            value={selectedMetric}
            onChange={(e) => setSelectedMetric(e.target.value)}
            className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
          >
            <option value="views">By Views</option>
            <option value="actions">By Actions</option>
            <option value="rating">By Rating</option>
          </select>
        </div>

        <div className="space-y-4">
          {analytics.top_performing_locations.map((location, index) => (
            <div
              key={location.id}
              className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"
            >
              <div className="flex items-center space-x-4">
                <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                  <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">
                    {index + 1}
                  </span>
                </div>
                
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    {location.name}
                  </h4>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                    <div className="flex items-center">
                      <Eye className="w-4 h-4 mr-1" />
                      {formatNumber(location.views)} views
                    </div>
                    <div className="flex items-center">
                      <MousePointer className="w-4 h-4 mr-1" />
                      {formatNumber(location.actions)} actions
                    </div>
                  </div>
                </div>
              </div>

              <div className="text-right">
                <div className="flex items-center space-x-2 mb-1">
                  <Star className="w-4 h-4 text-yellow-400 fill-current" />
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {location.rating}
                  </span>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  {location.reviews} reviews
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Insights and Recommendations */}
      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Performance Insights
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
            <div className="flex items-center mb-3">
              <TrendingUp className="w-5 h-5 text-blue-600 dark:text-blue-400 mr-2" />
              <h4 className="font-medium text-blue-900 dark:text-blue-100">
                Growing Interest
              </h4>
            </div>
            <p className="text-sm text-blue-800 dark:text-blue-200">
              Your profile views increased by {analytics.period_stats.views.change_percent.toFixed(1)}% 
              compared to the previous period. Keep up the good work!
            </p>
          </div>

          <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
            <div className="flex items-center mb-3">
              <MousePointer className="w-5 h-5 text-green-600 dark:text-green-400 mr-2" />
              <h4 className="font-medium text-green-900 dark:text-green-100">
                Customer Engagement
              </h4>
            </div>
            <p className="text-sm text-green-800 dark:text-green-200">
              Customer actions are up {analytics.period_stats.actions.change_percent.toFixed(1)}%. 
              Your listings are driving more customer interactions.
            </p>
          </div>

          <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
            <div className="flex items-center mb-3">
              <Phone className="w-5 h-5 text-purple-600 dark:text-purple-400 mr-2" />
              <h4 className="font-medium text-purple-900 dark:text-purple-100">
                Direct Contact
              </h4>
            </div>
            <p className="text-sm text-purple-800 dark:text-purple-200">
              Phone calls increased by {analytics.period_stats.calls.change_percent.toFixed(1)}%. 
              Customers are actively seeking direct contact.
            </p>
          </div>

          <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg">
            <div className="flex items-center mb-3">
              <Navigation className="w-5 h-5 text-orange-600 dark:text-orange-400 mr-2" />
              <h4 className="font-medium text-orange-900 dark:text-orange-100">
                Foot Traffic
              </h4>
            </div>
            <p className="text-sm text-orange-800 dark:text-orange-200">
              Direction requests are up {analytics.period_stats.direction_requests.change_percent.toFixed(1)}%. 
              More customers are visiting your locations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}