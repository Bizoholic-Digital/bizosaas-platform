'use client';

import React, { useState, useEffect } from 'react';
import { 
  Plus, Search, Filter, Edit, Trash2, Target, User, 
  CreditCard, Calendar, CheckCircle, TrendingUp, 
  BarChart3, FileText, Activity, UserPlus, Mail, Phone 
} from 'lucide-react';

interface CRMContentProps {
  activeTab: string;
}

export const CRMContent: React.FC<CRMContentProps> = ({ activeTab }) => {
  const [crmData, setCrmData] = useState({
    leads: [],
    contacts: [],
    deals: [],
    activities: [],
    tasks: [],
    opportunities: []
  });

  useEffect(() => {
    const fetchCRMData = async () => {
      try {
        const endpoints = {
          leads: '/api/brain/django-crm/leads',
          contacts: '/api/brain/django-crm/contacts', 
          deals: '/api/brain/django-crm/deals',
          activities: '/api/brain/django-crm/activities',
          tasks: '/api/brain/django-crm/tasks',
          opportunities: '/api/brain/django-crm/opportunities'
        };

        const responses = await Promise.all(
          Object.entries(endpoints).map(async ([key, endpoint]) => {
            try {
              const response = await fetch(endpoint);
              const data = await response.json();
              return [key, data];
            } catch {
              return [key, []];
            }
          })
        );

        setCrmData(Object.fromEntries(responses));
      } catch (error) {
        console.error('CRM data fetch error:', error);
        // Fallback data
        setCrmData({
          leads: [
            { id: 1, name: 'John Doe', email: 'john@example.com', status: 'New', score: 85, source: 'Website' },
            { id: 2, name: 'Jane Smith', email: 'jane@example.com', status: 'Qualified', score: 92, source: 'Referral' },
            { id: 3, name: 'Bob Johnson', email: 'bob@example.com', status: 'Contacted', score: 78, source: 'Social Media' }
          ],
          contacts: [
            { id: 1, name: 'Alice Cooper', company: 'TechCorp', email: 'alice@techcorp.com', phone: '+1-555-0123' },
            { id: 2, name: 'David Wilson', company: 'StartupXYZ', email: 'david@startupxyz.com', phone: '+1-555-0124' }
          ],
          deals: [
            { id: 1, title: 'Enterprise License', value: 50000, stage: 'Proposal', probability: 75, closeDate: '2024-02-15' },
            { id: 2, title: 'SaaS Subscription', value: 12000, stage: 'Negotiation', probability: 60, closeDate: '2024-01-30' }
          ],
          activities: [
            { id: 1, type: 'Call', description: 'Follow-up call with John Doe', date: '2024-01-15', status: 'Completed' },
            { id: 2, type: 'Email', description: 'Sent proposal to Jane Smith', date: '2024-01-14', status: 'Completed' }
          ],
          tasks: [
            { id: 1, title: 'Prepare contract for Enterprise deal', priority: 'High', dueDate: '2024-01-20', assignee: 'Sales Team' },
            { id: 2, title: 'Schedule demo for new prospect', priority: 'Medium', dueDate: '2024-01-18', assignee: 'John Smith' }
          ],
          opportunities: [
            { id: 1, title: 'Q1 Expansion Deal', value: 75000, stage: 'Discovery', company: 'MegaCorp Inc.' },
            { id: 2, title: 'Annual Renewal', value: 25000, stage: 'Proposal', company: 'Local Business LLC' }
          ]
        });
      }
    };

    fetchCRMData();
  }, [activeTab]);

  if (activeTab === 'crm-leads') {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Leads Management</h2>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700">
            <Plus className="w-4 h-4" /> Add Lead
          </button>
        </div>
        
        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
          <div className="p-4 border-b border-gray-200 dark:border-gray-800">
            <div className="flex gap-4">
              <div className="relative">
                <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input 
                  type="text" 
                  placeholder="Search leads..." 
                  className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800"
                />
              </div>
              <button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg flex items-center gap-2">
                <Filter className="w-4 h-4" /> Filter
              </button>
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Email</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Score</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Source</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
                {crmData.leads.map((lead: any) => (
                  <tr key={lead.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{lead.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{lead.email}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        lead.status === 'New' ? 'bg-blue-100 text-blue-800' :
                        lead.status === 'Qualified' ? 'bg-green-100 text-green-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {lead.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{lead.score}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{lead.source}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div className="flex gap-2">
                        <button className="text-blue-600 hover:text-blue-900"><Edit className="w-4 h-4" /></button>
                        <button className="text-red-600 hover:text-red-900"><Trash2 className="w-4 h-4" /></button>
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
  }

  // Default CRM overview
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">CRM Overview</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
              <Target className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Leads</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{crmData.leads.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
              <User className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Contacts</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{crmData.contacts.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
              <CreditCard className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Active Deals</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{crmData.deals.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-orange-600 dark:text-orange-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Opportunities</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{crmData.opportunities.length}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent Activities</h3>
          <div className="space-y-3">
            {crmData.activities.slice(0, 3).map((activity: any) => (
              <div key={activity.id} className="flex items-center gap-3">
                <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                  <Activity className="w-4 h-4 text-blue-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">{activity.description}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{activity.date}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Upcoming Tasks</h3>
          <div className="space-y-3">
            {crmData.tasks.slice(0, 3).map((task: any) => (
              <div key={task.id} className="flex items-center gap-3">
                <CheckCircle className="w-5 h-5 text-gray-400" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">{task.title}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Due: {task.dueDate}</p>
                </div>
                <span className={`px-2 py-1 text-xs rounded ${
                  task.priority === 'High' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {task.priority}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};