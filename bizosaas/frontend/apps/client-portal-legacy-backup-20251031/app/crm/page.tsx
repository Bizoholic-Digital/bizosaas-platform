'use client';

import React, { useState, useEffect } from 'react';
import { 
  Users, Target, Zap, BarChart3, Plus, Filter, 
  Search, Download, RefreshCw, TrendingUp, DollarSign,
  Phone, Mail, Calendar, Eye, Edit, Trash2, MoreHorizontal,
  CheckCircle, Clock, AlertCircle, Star
} from 'lucide-react';
import DashboardLayout from '../../components/ui/dashboard-layout';

interface CRMTabs {
  [key: string]: React.ReactNode;
}

const CRMManagementPage = () => {
  const [activeTab, setActiveTab] = useState('leads');
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const fetchCRMData = async () => {
      try {
        setLoading(true);
        // Mock API call - replace with actual Brain Hub API calls
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setData({
          leads: [
            {
              id: '1',
              name: 'John Smith',
              company: 'Acme Corp',
              email: 'john@acme.com',
              phone: '+1-555-0123',
              status: 'new',
              score: 85,
              value: 50000,
              source: 'Website',
              assignedTo: 'Sarah Wilson',
              createdAt: '2024-09-23T10:30:00Z',
              lastActivity: '2024-09-24T14:20:00Z'
            },
            {
              id: '2',
              name: 'Jane Doe',
              company: 'TechStart Inc',
              email: 'jane@techstart.com',
              phone: '+1-555-0124',
              status: 'qualified',
              score: 92,
              value: 75000,
              source: 'Google Ads',
              assignedTo: 'Mike Johnson',
              createdAt: '2024-09-22T15:45:00Z',
              lastActivity: '2024-09-24T09:15:00Z'
            },
            {
              id: '3',
              name: 'Bob Wilson',
              company: 'Local Business',
              email: 'bob@localbiz.com',
              phone: '+1-555-0125',
              status: 'contacted',
              score: 67,
              value: 25000,
              source: 'Referral',
              assignedTo: 'Sarah Wilson',
              createdAt: '2024-09-21T11:20:00Z',
              lastActivity: '2024-09-23T16:30:00Z'
            }
          ],
          contacts: [
            {
              id: '1',
              name: 'Alice Johnson',
              company: 'Design Studio',
              email: 'alice@designstudio.com',
              phone: '+1-555-0126',
              type: 'customer',
              tags: ['VIP', 'Design'],
              lastContact: '2024-09-24T12:00:00Z'
            }
          ],
          campaigns: [
            {
              id: '1',
              name: 'Q4 Lead Generation',
              type: 'email',
              status: 'active',
              sent: 2500,
              opened: 875,
              clicked: 234,
              converted: 43,
              startDate: '2024-09-01',
              endDate: '2024-12-31'
            }
          ],
          metrics: {
            totalLeads: 247,
            qualifiedLeads: 89,
            conversionRate: 18.5,
            avgDealValue: 42500,
            totalRevenue: 1250000,
            activeCampaigns: 5
          }
        });
      } catch (error) {
        console.error('Failed to fetch CRM data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCRMData();
  }, []);

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      new: { color: 'bg-blue-100 text-blue-800', label: 'New' },
      qualified: { color: 'bg-green-100 text-green-800', label: 'Qualified' },
      contacted: { color: 'bg-yellow-100 text-yellow-800', label: 'Contacted' },
      converted: { color: 'bg-purple-100 text-purple-800', label: 'Converted' },
      lost: { color: 'bg-red-100 text-red-800', label: 'Lost' },
      active: { color: 'bg-green-100 text-green-800', label: 'Active' },
      paused: { color: 'bg-gray-100 text-gray-800', label: 'Paused' },
      completed: { color: 'bg-blue-100 text-blue-800', label: 'Completed' }
    };

    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.new;
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const LeadsTab = () => (
    <div className="space-y-6">
      {/* Leads Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Leads Management</h2>
          <p className="text-sm text-gray-600 dark:text-gray-300">Track and manage your sales leads</p>
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
            Add Lead
          </button>
        </div>
      </div>

      {/* Leads Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <Users className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Total Leads</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.totalLeads}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
              <Target className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Qualified</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.qualifiedLeads}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <TrendingUp className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Conversion Rate</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.metrics.conversionRate}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-orange-100 dark:bg-orange-900 rounded-lg">
              <DollarSign className="w-6 h-6 text-orange-600 dark:text-orange-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Avg Deal Value</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">${data?.metrics.avgDealValue?.toLocaleString()}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Leads Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Recent Leads</h3>
            <div className="flex items-center gap-3">
              <div className="relative">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search leads..."
                  className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
                <RefreshCw className="w-4 h-4 text-gray-600 dark:text-gray-300" />
              </button>
            </div>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Lead
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Value
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Source
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Assigned To
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {data?.leads?.map((lead: any) => (
                <tr key={lead.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">{lead.name}</div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">{lead.company}</div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">{lead.email}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStatusBadge(lead.status)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="text-sm font-medium text-gray-900 dark:text-white">{lead.score}</div>
                      <div className="ml-2 flex">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`w-3 h-3 ${
                              i < Math.floor(lead.score / 20) 
                                ? 'text-yellow-400 fill-current' 
                                : 'text-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    ${lead.value?.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {lead.source}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {lead.assignedTo}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center gap-2 justify-end">
                      <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300">
                        <Phone className="w-4 h-4" />
                      </button>
                      <button className="text-purple-600 hover:text-purple-900 dark:text-purple-400 dark:hover:text-purple-300">
                        <Mail className="w-4 h-4" />
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

  const tabs: CRMTabs = {
    leads: <LeadsTab />,
    contacts: <div className="p-6 text-center text-gray-500">Contacts tab coming soon...</div>,
    campaigns: <div className="p-6 text-center text-gray-500">Campaigns tab coming soon...</div>,
    reports: <div className="p-6 text-center text-gray-500">Reports tab coming soon...</div>
  };

  const tabItems = [
    { id: 'leads', name: 'Leads', icon: <Target className="w-4 h-4" />, badge: data?.leads?.length },
    { id: 'contacts', name: 'Contacts', icon: <Users className="w-4 h-4" />, badge: data?.contacts?.length },
    { id: 'campaigns', name: 'Campaigns', icon: <Zap className="w-4 h-4" />, badge: data?.campaigns?.length },
    { id: 'reports', name: 'Reports', icon: <BarChart3 className="w-4 h-4" /> }
  ];

  if (loading) {
    return (
      <DashboardLayout title="CRM Management" description="Manage your customer relationships">
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
    <DashboardLayout title="CRM Management" description="Manage your customer relationships and sales pipeline">
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

export default CRMManagementPage;