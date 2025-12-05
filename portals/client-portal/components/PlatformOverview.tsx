'use client';

import React, { useState, useEffect } from 'react';
import {
    Activity, Users, Server, Database, Cpu, HardDrive,
    TrendingUp, AlertCircle, CheckCircle, Clock, Zap, BarChart3
} from 'lucide-react';

interface PlatformMetrics {
    overview: {
        total_tenants: number;
        active_tenants: number;
        total_users: number;
        active_users: number;
        total_api_calls: number;
        avg_response_time: string;
        error_rate: string;
        uptime: string;
    };
    services: {
        [key: string]: {
            status: 'healthy' | 'degraded' | 'down';
            response_time: string;
        };
    };
    resources: {
        cpu_usage: string;
        memory_usage: string;
        disk_usage: string;
        database_connections: number;
        cache_hit_rate: string;
    };
    ai_agents: {
        total_agents: number;
        active_agents: number;
        total_requests: number;
        avg_processing_time: string;
    };
}

export const PlatformOverview: React.FC = () => {
    const [metrics, setMetrics] = useState<PlatformMetrics | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

    useEffect(() => {
        fetchMetrics();
        const interval = setInterval(fetchMetrics, 30000); // Refresh every 30 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchMetrics = async () => {
        try {
            const response = await fetch('/api/brain/admin/platform');
            if (response.ok) {
                const data = await response.json();
                setMetrics(data);
                setLastUpdated(new Date());
            }
        } catch (error) {
            console.error('Failed to fetch platform metrics:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'healthy':
                return 'text-green-600 bg-green-100 dark:bg-green-900/30';
            case 'degraded':
                return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30';
            case 'down':
                return 'text-red-600 bg-red-100 dark:bg-red-900/30';
            default:
                return 'text-gray-600 bg-gray-100 dark:bg-gray-900/30';
        }
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'healthy':
                return <CheckCircle className="w-4 h-4" />;
            case 'degraded':
                return <AlertCircle className="w-4 h-4" />;
            case 'down':
                return <AlertCircle className="w-4 h-4" />;
            default:
                return <Activity className="w-4 h-4" />;
        }
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (!metrics) {
        return (
            <div className="text-center text-gray-500 dark:text-gray-400 py-12">
                Failed to load platform metrics
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Platform Overview</h2>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                        Last updated: {lastUpdated.toLocaleTimeString()}
                    </p>
                </div>
                <button
                    onClick={fetchMetrics}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                    Refresh
                </button>
            </div>

            {/* Overview Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Tenants</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                                {metrics.overview.total_tenants}
                            </p>
                            <p className="text-xs text-green-600 mt-1">
                                {metrics.overview.active_tenants} active
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                            <Users className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Users</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                                {metrics.overview.total_users.toLocaleString()}
                            </p>
                            <p className="text-xs text-green-600 mt-1">
                                {metrics.overview.active_users.toLocaleString()} active
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                            <Activity className="w-6 h-6 text-green-600 dark:text-green-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">API Calls</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                                {(metrics.overview.total_api_calls / 1000000).toFixed(1)}M
                            </p>
                            <p className="text-xs text-gray-500 mt-1">
                                Avg: {metrics.overview.avg_response_time}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                            <Zap className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Uptime</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                                {metrics.overview.uptime}
                            </p>
                            <p className="text-xs text-gray-500 mt-1">
                                Error rate: {metrics.overview.error_rate}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                            <TrendingUp className="w-6 h-6 text-green-600 dark:text-green-400" />
                        </div>
                    </div>
                </div>
            </div>

            {/* Services Status */}
            <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800">
                <div className="p-6 border-b border-gray-200 dark:border-gray-800">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Services Health</h3>
                </div>
                <div className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        {Object.entries(metrics.services).map(([service, data]) => (
                            <div
                                key={service}
                                className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
                            >
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">
                                        {service.replace('_', ' ')}
                                    </span>
                                    <span className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${getStatusColor(data.status)}`}>
                                        {getStatusIcon(data.status)}
                                        {data.status}
                                    </span>
                                </div>
                                <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                                    <Clock className="w-3 h-3" />
                                    {data.response_time}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Resources & AI Agents */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Resources */}
                <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="p-6 border-b border-gray-200 dark:border-gray-800">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Resource Usage</h3>
                    </div>
                    <div className="p-6 space-y-4">
                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    <Cpu className="w-4 h-4 text-gray-500" />
                                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">CPU</span>
                                </div>
                                <span className="text-sm font-semibold text-gray-900 dark:text-white">
                                    {metrics.resources.cpu_usage}
                                </span>
                            </div>
                            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                                <div
                                    className="bg-blue-600 h-2 rounded-full"
                                    style={{ width: metrics.resources.cpu_usage }}
                                />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    <Server className="w-4 h-4 text-gray-500" />
                                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Memory</span>
                                </div>
                                <span className="text-sm font-semibold text-gray-900 dark:text-white">
                                    {metrics.resources.memory_usage}
                                </span>
                            </div>
                            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                                <div
                                    className="bg-green-600 h-2 rounded-full"
                                    style={{ width: metrics.resources.memory_usage }}
                                />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    <HardDrive className="w-4 h-4 text-gray-500" />
                                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Disk</span>
                                </div>
                                <span className="text-sm font-semibold text-gray-900 dark:text-white">
                                    {metrics.resources.disk_usage}
                                </span>
                            </div>
                            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                                <div
                                    className="bg-purple-600 h-2 rounded-full"
                                    style={{ width: metrics.resources.disk_usage }}
                                />
                            </div>
                        </div>

                        <div className="pt-4 border-t border-gray-200 dark:border-gray-800">
                            <div className="flex items-center justify-between text-sm">
                                <div className="flex items-center gap-2">
                                    <Database className="w-4 h-4 text-gray-500" />
                                    <span className="text-gray-700 dark:text-gray-300">DB Connections</span>
                                </div>
                                <span className="font-semibold text-gray-900 dark:text-white">
                                    {metrics.resources.database_connections}
                                </span>
                            </div>
                            <div className="flex items-center justify-between text-sm mt-2">
                                <div className="flex items-center gap-2">
                                    <BarChart3 className="w-4 h-4 text-gray-500" />
                                    <span className="text-gray-700 dark:text-gray-300">Cache Hit Rate</span>
                                </div>
                                <span className="font-semibold text-green-600">
                                    {metrics.resources.cache_hit_rate}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* AI Agents */}
                <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="p-6 border-b border-gray-200 dark:border-gray-800">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">AI Agents Performance</h3>
                    </div>
                    <div className="p-6">
                        <div className="grid grid-cols-2 gap-6">
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Agents</p>
                                <p className="text-3xl font-bold text-gray-900 dark:text-white">
                                    {metrics.ai_agents.total_agents}
                                </p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Active Agents</p>
                                <p className="text-3xl font-bold text-green-600">
                                    {metrics.ai_agents.active_agents}
                                </p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Requests</p>
                                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                                    {(metrics.ai_agents.total_requests / 1000).toFixed(1)}K
                                </p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg Processing</p>
                                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                                    {metrics.ai_agents.avg_processing_time}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
