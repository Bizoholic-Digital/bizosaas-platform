'use client';

import React, { useState, useEffect } from 'react';
import {
    BarChart3, TrendingUp, Target, Activity, Lightbulb,
    Users, Eye, MousePointer, Clock, DollarSign
} from 'lucide-react';

interface AnalyticsContentProps {
    activeTab: string;
}

export const AnalyticsContent: React.FC<AnalyticsContentProps> = ({ activeTab }) => {
    const [analyticsData, setAnalyticsData] = useState({
        dashboards: [],
        metrics: {
            pageViews: 0,
            uniqueVisitors: 0,
            avgSessionDuration: '0m',
            bounceRate: '0%',
            conversions: 0,
            revenue: 0
        }
    });

    useEffect(() => {
        const fetchAnalyticsData = async () => {
            try {
                const endpoints = {
                    dashboards: '/api/brain/analytics/dashboards',
                    dashboard: '/api/brain/analytics/dashboard'
                };

                const responses = await Promise.all(
                    Object.entries(endpoints).map(async ([key, endpoint]) => {
                        try {
                            const response = await fetch(endpoint);
                            const data = await response.json();
                            return [key, data];
                        } catch {
                            return [key, key === 'dashboards' ? [] : {}];
                        }
                    })
                );

                const data = Object.fromEntries(responses) as any;
                setAnalyticsData({
                    dashboards: Array.isArray(data.dashboards) ? data.dashboards : [],
                    metrics: data.dashboard?.metrics || analyticsData.metrics
                });
            } catch (error) {
                console.error('Analytics data fetch error:', error);
            }
        };

        fetchAnalyticsData();
    }, [activeTab]);

    const renderOverview = () => (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Analytics Overview</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Page Views</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{analyticsData.metrics.pageViews.toLocaleString()}</p>
                            <p className="text-sm text-green-600 mt-1">+12% from last month</p>
                        </div>
                        <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                            <Eye className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Unique Visitors</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{analyticsData.metrics.uniqueVisitors.toLocaleString()}</p>
                            <p className="text-sm text-green-600 mt-1">+8% from last month</p>
                        </div>
                        <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                            <Users className="w-6 h-6 text-green-600 dark:text-green-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Avg. Session</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{analyticsData.metrics.avgSessionDuration}</p>
                            <p className="text-sm text-red-600 mt-1">-3% from last month</p>
                        </div>
                        <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                            <Clock className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Bounce Rate</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{analyticsData.metrics.bounceRate}</p>
                            <p className="text-sm text-green-600 mt-1">-5% from last month</p>
                        </div>
                        <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
                            <TrendingUp className="w-6 h-6 text-orange-600 dark:text-orange-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Conversions</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{analyticsData.metrics.conversions}</p>
                            <p className="text-sm text-green-600 mt-1">+15% from last month</p>
                        </div>
                        <div className="w-12 h-12 bg-pink-100 dark:bg-pink-900/30 rounded-lg flex items-center justify-center">
                            <Target className="w-6 h-6 text-pink-600 dark:text-pink-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Revenue</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">${analyticsData.metrics.revenue.toLocaleString()}</p>
                            <p className="text-sm text-green-600 mt-1">+22% from last month</p>
                        </div>
                        <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg flex items-center justify-center">
                            <DollarSign className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Traffic Overview</h3>
                <div className="h-64 flex items-center justify-center text-gray-500 dark:text-gray-400">
                    <p>Traffic chart will be displayed here</p>
                </div>
            </div>
        </div>
    );

    const renderTraffic = () => (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Traffic Analytics</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Traffic Sources</h3>
                    <div className="space-y-3">
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-600 dark:text-gray-400">Direct</span>
                            <span className="text-sm font-semibold text-gray-900 dark:text-white">0%</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-600 dark:text-gray-400">Organic Search</span>
                            <span className="text-sm font-semibold text-gray-900 dark:text-white">0%</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-600 dark:text-gray-400">Social Media</span>
                            <span className="text-sm font-semibold text-gray-900 dark:text-white">0%</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-600 dark:text-gray-400">Referral</span>
                            <span className="text-sm font-semibold text-gray-900 dark:text-white">0%</span>
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Top Pages</h3>
                    <div className="space-y-3">
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-600 dark:text-gray-400">/</span>
                            <span className="text-sm font-semibold text-gray-900 dark:text-white">0 views</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderConversions = () => (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Conversion Analytics</h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center">
                        <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                            <Target className="w-6 h-6 text-green-600 dark:text-green-400" />
                        </div>
                        <div className="ml-4">
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Conversion Rate</p>
                            <p className="text-2xl font-bold text-gray-900 dark:text-white">0%</p>
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center">
                        <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                            <MousePointer className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                        </div>
                        <div className="ml-4">
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Conversions</p>
                            <p className="text-2xl font-bold text-gray-900 dark:text-white">0</p>
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center">
                        <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                            <DollarSign className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                        </div>
                        <div className="ml-4">
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Conversion Value</p>
                            <p className="text-2xl font-bold text-gray-900 dark:text-white">$0</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderPerformance = () => (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Performance Metrics</h2>
            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Page Load Times</h3>
                <p className="text-gray-600 dark:text-gray-400">Performance metrics will be displayed here</p>
            </div>
        </div>
    );

    const renderGoals = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Goals & Targets</h2>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                    Create Goal
                </button>
            </div>
            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                <p className="text-gray-600 dark:text-gray-400">No goals configured. Create your first goal to track progress.</p>
            </div>
        </div>
    );

    const renderInsights = () => (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">AI-Powered Insights</h2>
            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Lightbulb className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Recommendations</h3>
                        <p className="text-gray-600 dark:text-gray-400">AI insights will appear here based on your analytics data.</p>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderRealtime = () => (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Real-time Analytics</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Active Users</p>
                    <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">0</p>
                </div>
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Page Views/min</p>
                    <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">0</p>
                </div>
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Top Page</p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white mt-2">/</p>
                </div>
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Top Source</p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white mt-2">Direct</p>
                </div>
            </div>
        </div>
    );

    const renderCustom = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Custom Reports</h2>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                    Create Report
                </button>
            </div>
            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                <p className="text-gray-600 dark:text-gray-400">Create custom reports to track specific metrics and KPIs.</p>
            </div>
        </div>
    );

    if (activeTab === 'analytics-overview') return renderOverview();
    if (activeTab === 'analytics-traffic') return renderTraffic();
    if (activeTab === 'analytics-conversions') return renderConversions();
    if (activeTab === 'analytics-performance') return renderPerformance();
    if (activeTab === 'analytics-goals') return renderGoals();
    if (activeTab === 'analytics-insights') return renderInsights();
    if (activeTab === 'analytics-real-time') return renderRealtime();
    if (activeTab === 'analytics-custom') return renderCustom();

    // Default Analytics overview
    return renderOverview();
};
