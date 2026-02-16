'use client';

import React, { useState, useEffect } from 'react';
import {
    Server, Activity, Database, Users, Settings,
    CheckCircle, XCircle, AlertTriangle, RefreshCw,
    Cpu, HardDrive, Network, Clock, TrendingUp
} from 'lucide-react';

interface AdminContentProps {
    activeTab: string;
}

interface ServiceStatus {
    name: string;
    status: 'healthy' | 'degraded' | 'down';
    uptime: string;
    lastCheck: string;
    responseTime: string;
    version: string;
}

export const AdminContent: React.FC<AdminContentProps> = ({ activeTab }) => {
    const [services, setServices] = useState<ServiceStatus[]>([
        { name: 'Brain API Gateway', status: 'healthy', uptime: '99.9%', lastCheck: 'Just now', responseTime: '45ms', version: 'v1.0.0' },
        { name: 'Django CRM', status: 'healthy', uptime: '99.8%', lastCheck: '1 min ago', responseTime: '120ms', version: 'v2.1.0' },
        { name: 'Wagtail CMS', status: 'healthy', uptime: '99.7%', lastCheck: '1 min ago', responseTime: '95ms', version: 'v5.2.0' },
        { name: 'Saleor E-commerce', status: 'healthy', uptime: '99.9%', lastCheck: '2 min ago', responseTime: '150ms', version: 'v3.15.0' },
        { name: 'Marketing Service', status: 'degraded', uptime: '98.5%', lastCheck: '3 min ago', responseTime: '250ms', version: 'v1.2.0' },
        { name: 'Analytics Service', status: 'healthy', uptime: '99.6%', lastCheck: '1 min ago', responseTime: '80ms', version: 'v1.1.0' },
        { name: 'Auth Service (SSO)', status: 'healthy', uptime: '99.9%', lastCheck: 'Just now', responseTime: '35ms', version: 'v1.0.5' },
        { name: 'PostgreSQL Database', status: 'healthy', uptime: '99.99%', lastCheck: 'Just now', responseTime: '5ms', version: 'v15.3' },
        { name: 'Redis Cache', status: 'healthy', uptime: '99.95%', lastCheck: 'Just now', responseTime: '2ms', version: 'v7.2' },
    ]);

    const [systemMetrics, setSystemMetrics] = useState({
        totalUsers: 1247,
        activeUsers: 89,
        totalRequests: 45231,
        avgResponseTime: '95ms',
        errorRate: '0.02%',
        cpuUsage: '45%',
        memoryUsage: '62%',
        diskUsage: '38%'
    });

    const refreshServices = () => {
        // Simulate refresh
        console.log('Refreshing service status...');
    };

    const renderServiceStatus = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Service Status</h2>
                <button
                    onClick={refreshServices}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
                >
                    <RefreshCw className="w-4 h-4" /> Refresh
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Healthy Services</p>
                            <p className="text-3xl font-bold text-green-600 mt-2">
                                {services.filter(s => s.status === 'healthy').length}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                            <CheckCircle className="w-6 h-6 text-green-600 dark:text-green-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Degraded</p>
                            <p className="text-3xl font-bold text-yellow-600 mt-2">
                                {services.filter(s => s.status === 'degraded').length}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg flex items-center justify-center">
                            <AlertTriangle className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Down</p>
                            <p className="text-3xl font-bold text-red-600 mt-2">
                                {services.filter(s => s.status === 'down').length}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center justify-center">
                            <XCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Avg Response</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{systemMetrics.avgResponseTime}</p>
                        </div>
                        <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                            <Activity className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50 dark:bg-gray-800">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Service</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Uptime</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Response Time</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Version</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Last Check</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
                            {services.map((service, index) => (
                                <tr key={index}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                        <div className="flex items-center gap-2">
                                            <Server className="w-4 h-4 text-gray-400" />
                                            {service.name}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${service.status === 'healthy' ? 'bg-green-100 text-green-800' :
                                                service.status === 'degraded' ? 'bg-yellow-100 text-yellow-800' :
                                                    'bg-red-100 text-red-800'
                                            }`}>
                                            {service.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{service.uptime}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{service.responseTime}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{service.version}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{service.lastCheck}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );

    const renderSystemMetrics = () => (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">System Metrics</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">CPU Usage</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{systemMetrics.cpuUsage}</p>
                        </div>
                        <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                            <Cpu className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Memory Usage</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{systemMetrics.memoryUsage}</p>
                        </div>
                        <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                            <Database className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Disk Usage</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{systemMetrics.diskUsage}</p>
                        </div>
                        <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                            <HardDrive className="w-6 h-6 text-green-600 dark:text-green-400" />
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Error Rate</p>
                            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{systemMetrics.errorRate}</p>
                        </div>
                        <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center justify-center">
                            <AlertTriangle className="w-6 h-6 text-red-600 dark:text-red-400" />
                        </div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">User Activity</h3>
                    <div className="space-y-3">
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-600 dark:text-gray-400">Total Users</span>
                            <span className="text-sm font-semibold text-gray-900 dark:text-white">{systemMetrics.totalUsers.toLocaleString()}</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-600 dark:text-gray-400">Active Now</span>
                            <span className="text-sm font-semibold text-green-600">{systemMetrics.activeUsers}</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-600 dark:text-gray-400">Total Requests (24h)</span>
                            <span className="text-sm font-semibold text-gray-900 dark:text-white">{systemMetrics.totalRequests.toLocaleString()}</span>
                        </div>
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h3>
                    <div className="space-y-2">
                        <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
                            Restart All Services
                        </button>
                        <button className="w-full px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 text-sm">
                            Clear Cache
                        </button>
                        <button className="w-full px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 text-sm">
                            View Logs
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderUsers = () => (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">User Management</h2>
            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                <p className="text-gray-600 dark:text-gray-400">User management interface will be implemented here.</p>
            </div>
        </div>
    );

    const renderSettings = () => (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Admin Settings</h2>
            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                <p className="text-gray-600 dark:text-gray-400">Admin configuration settings will be implemented here.</p>
            </div>
        </div>
    );

    if (activeTab === 'admin-services') return renderServiceStatus();
    if (activeTab === 'admin-metrics') return renderSystemMetrics();
    if (activeTab === 'admin-users') return renderUsers();
    if (activeTab === 'admin-settings') return renderSettings();

    // Default Admin overview
    return renderServiceStatus();
};
