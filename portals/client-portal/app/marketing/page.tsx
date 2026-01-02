'use client';

import React, { useState, useEffect } from 'react';
import {
  Zap, Plus, Search, Filter, Download, RefreshCw,
  Play, Pause, Square, Calendar, Users, Mail,
  Eye, Edit, Trash2, MoreHorizontal, Target, TrendingUp,
  BarChart3, Activity, Clock, CheckCircle, AlertCircle, Megaphone
} from 'lucide-react';
import DashboardLayout from '../../components/ui/dashboard-layout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { brainApi } from '@/lib/brain-api';

const MarketingPage = () => {
  const [loading, setLoading] = useState(true);
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        setLoading(true);
        // In a real app, we'd fetch from brainApi.campaigns.list()
        // For now, using enhanced mock data to show the potential
        await new Promise(resolve => setTimeout(resolve, 800));

        const mockCampaigns = [
          {
            id: '1',
            name: 'Q4 Lead Generation',
            type: 'email',
            status: 'active',
            channel: 'Email Marketing',
            startDate: '2024-10-01T00:00:00Z',
            endDate: '2024-12-31T23:59:59Z',
            budget: 15000,
            spent: 9240,
            audience: 2500,
            sent: 2500,
            opened: 1245,
            clicked: 432,
            converted: 86,
            revenue: 142000,
            ctr: 34.7,
            conversionRate: 19.9,
            roas: 15.37,
            progress: 61.6
          },
          {
            id: '2',
            name: 'Google Discovery Ads',
            type: 'ppc',
            status: 'active',
            channel: 'Google Ads',
            startDate: '2024-11-01T00:00:00Z',
            endDate: '2024-11-30T23:59:59Z',
            budget: 5000,
            spent: 2150,
            audience: 12000,
            sent: 0,
            opened: 0,
            clicked: 840,
            converted: 24,
            revenue: 35000,
            ctr: 7.0,
            conversionRate: 2.8,
            roas: 16.27,
            progress: 43
          },
          {
            id: '3',
            name: 'Holiday Sale - Meta',
            type: 'social',
            status: 'scheduled',
            channel: 'Facebook Ads',
            startDate: '2024-12-15T00:00:00Z',
            endDate: '2025-01-05T23:59:59Z',
            budget: 10000,
            spent: 0,
            audience: 25000,
            sent: 0,
            opened: 0,
            clicked: 0,
            converted: 0,
            revenue: 0,
            ctr: 0,
            conversionRate: 0,
            roas: 0,
            progress: 0
          }
        ];

        setCampaigns(mockCampaigns);
      } catch (error) {
        console.error('Failed to fetch campaigns:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCampaigns();
  }, []);

  const getStatusBadge = (status: string) => {
    const statusConfig: any = {
      active: { color: 'bg-green-100 text-green-800 border-green-200', icon: <Play className="w-3 h-3" />, label: 'Active' },
      paused: { color: 'bg-yellow-100 text-yellow-800 border-yellow-200', icon: <Pause className="w-3 h-3" />, label: 'Paused' },
      completed: { color: 'bg-blue-100 text-blue-800 border-blue-200', icon: <CheckCircle className="w-3 h-3" />, label: 'Completed' },
      scheduled: { color: 'bg-purple-100 text-purple-800 border-purple-200', icon: <Clock className="w-3 h-3" />, label: 'Scheduled' },
      draft: { color: 'bg-gray-100 text-gray-800 border-gray-200', icon: <Edit className="w-3 h-3" />, label: 'Draft' }
    };

    const config = statusConfig[status] || statusConfig.draft;

    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold border ${config.color}`}>
        {config.icon}
        {config.label}
      </span>
    );
  };

  const filteredCampaigns = campaigns.filter(campaign => {
    const matchesSearch = campaign.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      campaign.channel.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = selectedFilter === 'all' || campaign.status === selectedFilter;
    return matchesSearch && matchesFilter;
  });

  if (loading) {
    return (
      <DashboardLayout title="Marketing & Campaigns">
        <div className="p-8 animate-pulse space-y-8">
          <div className="h-10 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="h-32 bg-gray-200 rounded-xl"></div>
            <div className="h-32 bg-gray-200 rounded-xl"></div>
            <div className="h-32 bg-gray-200 rounded-xl"></div>
          </div>
          <div className="h-96 bg-gray-200 rounded-xl"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Marketing Platform" description="Manage and track your omnichannel marketing campaigns">
      <div className="p-8 space-y-8 bg-gray-50/50 min-h-screen">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">Marketing Campaigns</h1>
            <p className="text-lg text-gray-500 mt-1">Monitor performance across all your marketing channels.</p>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" className="gap-2">
              <Download className="w-4 h-4" /> Export Data
            </Button>
            <Button className="gap-2 bg-blue-600 hover:bg-blue-700 shadow-lg">
              <Plus className="w-4 h-4" /> New Campaign
            </Button>
          </div>
        </div>

        {/* High-Level Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="border-0 shadow-sm overflow-hidden">
            <CardContent className="p-6 flex items-center gap-4">
              <div className="p-4 bg-blue-100 rounded-2xl">
                <Target className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <p className="text-sm font-bold text-gray-500 uppercase tracking-widest">Active Campaigns</p>
                <p className="text-3xl font-black text-gray-900">{campaigns.filter(c => c.status === 'active').length}</p>
                <p className="text-xs text-green-600 font-bold mt-1">↑ 2 from last month</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-sm overflow-hidden">
            <CardContent className="p-6 flex items-center gap-4">
              <div className="p-4 bg-green-100 rounded-2xl">
                <TrendingUp className="w-8 h-8 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-bold text-gray-500 uppercase tracking-widest">Total Revenue</p>
                <p className="text-3xl font-black text-gray-900">$177.0k</p>
                <p className="text-xs text-green-600 font-bold mt-1">↑ 14.2% increase</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-sm overflow-hidden">
            <CardContent className="p-6 flex items-center gap-4">
              <div className="p-4 bg-purple-100 rounded-2xl">
                <BarChart3 className="w-8 h-8 text-purple-600" />
              </div>
              <div>
                <p className="text-sm font-bold text-gray-500 uppercase tracking-widest">Avg. ROAS</p>
                <p className="text-3xl font-black text-gray-900">15.8x</p>
                <p className="text-xs text-purple-600 font-bold mt-1">Top 5% industry avg</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters and Controls */}
        <div className="flex flex-col md:flex-row gap-4 items-center bg-white p-4 rounded-2xl shadow-sm border border-gray-100">
          <div className="relative flex-1 w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <Input
              placeholder="Search campaigns..."
              className="pl-11 h-12 border-0 bg-gray-50/50 focus-visible:ring-1 focus-visible:ring-blue-100"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="flex items-center gap-3 w-full md:w-auto">
            <select
              className="h-12 px-4 rounded-xl border border-gray-200 bg-white text-sm font-medium focus:ring-2 focus:ring-blue-500"
              value={selectedFilter}
              onChange={(e) => setSelectedFilter(e.target.value)}
            >
              <option value="all">All Status</option>
              <option value="active">Active Only</option>
              <option value="scheduled">Scheduled</option>
              <option value="completed">Completed</option>
            </select>
            <Button variant="ghost" size="icon" className="h-12 w-12 rounded-xl">
              <RefreshCw className="w-5 h-5 text-gray-500" />
            </Button>
          </div>
        </div>

        {/* Campaign List */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {filteredCampaigns.map(campaign => (
            <Card key={campaign.id} className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden group">
              <div className="h-2 bg-blue-600 w-full opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <CardContent className="p-8">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-2xl font-bold text-gray-900">{campaign.name}</h3>
                      {getStatusBadge(campaign.status)}
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-500 font-medium capitalize">
                      <Zap className="w-4 h-4 text-blue-500" />
                      {campaign.channel}
                    </div>
                  </div>
                  <div className="flex gap-1">
                    <Button variant="ghost" size="icon" className="text-gray-400 hover:text-blue-600"><Eye className="w-5 h-5" /></Button>
                    <Button variant="ghost" size="icon" className="text-gray-400 hover:text-green-600"><Edit className="w-5 h-5" /></Button>
                    <Button variant="ghost" size="icon" className="text-gray-400 hover:text-red-500"><Trash2 className="w-5 h-5" /></Button>
                  </div>
                </div>

                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 bg-gray-50 rounded-2xl">
                      <p className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Return (ROAS)</p>
                      <p className="text-2xl font-black text-gray-900">{campaign.roas > 0 ? `${campaign.roas}x` : 'N/A'}</p>
                    </div>
                    <div className="p-4 bg-green-50 rounded-2xl">
                      <p className="text-xs font-bold text-green-700 uppercase tracking-wider mb-1">Generated Rev.</p>
                      <p className="text-2xl font-black text-green-900">${(campaign.revenue / 1000).toFixed(1)}k</p>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between text-sm font-bold">
                      <span className="text-gray-500">Budget Spent: ${campaign.spent.toLocaleString()}</span>
                      <span className="text-blue-600">{campaign.progress}%</span>
                    </div>
                    <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-600 rounded-full transition-all duration-1000"
                        style={{ width: `${campaign.progress}%` }}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-4 gap-2 pt-4 border-t border-gray-100">
                    <div className="text-center">
                      <p className="text-[10px] font-bold text-gray-400 uppercase">Clicks</p>
                      <p className="font-bold">{campaign.clicked.toLocaleString()}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-[10px] font-bold text-gray-400 uppercase">CTR</p>
                      <p className="font-bold">{campaign.ctr}%</p>
                    </div>
                    <div className="text-center">
                      <p className="text-[10px] font-bold text-gray-400 uppercase">Conv.</p>
                      <p className="font-bold">{campaign.converted}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-[10px] font-bold text-gray-400 uppercase">C-Rate</p>
                      <p className="font-bold">{campaign.conversionRate}%</p>
                    </div>
                  </div>
                </div>

                <div className="mt-8 flex items-center justify-between">
                  <div className="flex items-center gap-2 text-xs text-gray-400 font-bold uppercase tracking-widest">
                    <Calendar className="w-3 h-3" />
                    Ends {new Date(campaign.endDate).toLocaleDateString()}
                  </div>
                  <Button variant="link" className="text-blue-600 font-bold p-0 h-auto">View Details →</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredCampaigns.length === 0 && (
          <div className="text-center py-20 bg-white rounded-3xl shadow-sm border border-dashed border-gray-300">
            <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <Megaphone className="w-10 h-10 text-gray-400" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">No campaigns found</h2>
            <p className="text-gray-500 mt-2 max-w-sm mx-auto">
              There are no campaigns matching your criteria. Start a new campaign to reach your customers.
            </p>
            <Button className="mt-8 bg-blue-600 hover:bg-blue-700 px-8 h-12 text-lg rounded-xl">
              Launch Campaign 🚀
            </Button>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default MarketingPage;
