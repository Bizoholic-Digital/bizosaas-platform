'use client';

import React, { useState, useEffect } from 'react';
import {
  Plus, Search, Filter, Edit, Trash2, Target, User,
  CreditCard, Calendar, CheckCircle, TrendingUp,
  BarChart3, FileText, Activity, UserPlus, Mail, Phone
} from 'lucide-react';
import { LeadForm } from './LeadForm';
import { ContactForm } from './ContactForm';
import { DealForm } from './DealForm';
import { ActivityForm } from './ActivityForm';
import { TaskForm } from './TaskForm';
import { OpportunityForm } from './OpportunityForm';

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

  // Modal States
  const [isLeadModalOpen, setIsLeadModalOpen] = useState(false);
  const [isContactModalOpen, setIsContactModalOpen] = useState(false);
  const [isDealModalOpen, setIsDealModalOpen] = useState(false);
  const [isActivityModalOpen, setIsActivityModalOpen] = useState(false);
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
  const [isOpportunityModalOpen, setIsOpportunityModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState<any>(null);

  // Mock function to represent fetching from Brain Gateway -> FluentCRM
  // In future, this will be: `const data = await brainApi.connectors.sync('fluentcrm', 'contacts');`
  const refreshData = async () => {
    try {
      // Placeholder for Connector-based fetching
      console.log('Fetching CRM data via Brain Gateway...');

      // We are "stubbing" this out because the detailed wiring requires
      // the Backend Proxy endpoint `/api/brain/connectors/proxy/...` to be fully ready.
      // For now, we clear the data or set it to mock to show the UI is "Active" but needs a connection.

      // If no connection, maybe show empty or a prompt?
      // For this refactor, let's keep the mock data fallback or empty to prove wiring structure.

      if (activeTab === 'crm-leads') {
        // fetch leads...
      }

    } catch (error) {
      console.error('Error refreshing data:', error);
    }
  };

  const handleCreate = async (type: string, data: any) => {
    // Placeholder for `brainApi.connectors.performAction('fluentcrm', 'create_contact', data)`
    console.log(`Creating ${type} in CRM via Connector`, data);
    await refreshData();
  };

  const handleUpdate = async (type: string, id: string, data: any) => {
    console.log(`Updating ${type} ${id} in CRM via Connector`, data);
    await refreshData();
  };

  useEffect(() => {
    // Initial fetch on tab change
    refreshData();
  }, [activeTab]);

  const renderLeads = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Leads Management</h2>
        <button
          onClick={() => { setSelectedItem(null); setIsLeadModalOpen(true); }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
        >
          <Plus className="w-4 h-4" /> Add Lead
        </button>
        <LeadForm
          isOpen={isLeadModalOpen}
          onClose={() => setIsLeadModalOpen(false)}
          onSubmit={(data) => selectedItem ? handleUpdate('leads', selectedItem.id, data) : handleCreate('leads', data)}
          initialData={selectedItem}
        />
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
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${lead.status === 'New' ? 'bg-blue-100 text-blue-800' :
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
                      <button
                        onClick={() => { setSelectedItem(lead); setIsLeadModalOpen(true); }}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
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

  const renderContacts = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Contacts Management</h2>
        <button
          onClick={() => { setSelectedItem(null); setIsContactModalOpen(true); }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
        >
          <Plus className="w-4 h-4" /> Add Contact
        </button>
        <ContactForm
          isOpen={isContactModalOpen}
          onClose={() => setIsContactModalOpen(false)}
          onSubmit={(data) => selectedItem ? handleUpdate('contacts', selectedItem.id, data) : handleCreate('contacts', data)}
          initialData={selectedItem}
        />
      </div>
      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Company</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Phone</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
              {crmData.contacts.map((contact: any) => (
                <tr key={contact.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{contact.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{contact.company}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{contact.email}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{contact.phone}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <div className="flex gap-2">
                      <button
                        onClick={() => { setSelectedItem(contact); setIsContactModalOpen(true); }}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
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

  const renderDeals = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Deals Pipeline</h2>
        <button
          onClick={() => { setSelectedItem(null); setIsDealModalOpen(true); }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
        >
          <Plus className="w-4 h-4" /> Add Deal
        </button>
        <DealForm
          isOpen={isDealModalOpen}
          onClose={() => setIsDealModalOpen(false)}
          onSubmit={(data) => selectedItem ? handleUpdate('deals', selectedItem.id, data) : handleCreate('deals', data)}
          initialData={selectedItem}
        />
      </div>
      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Value</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Stage</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Probability</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Close Date</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
              {crmData.deals.map((deal: any) => (
                <tr key={deal.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{deal.title}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">${deal.value.toLocaleString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-800">
                      {deal.stage}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{deal.probability}%</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{deal.closeDate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderActivities = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Activities</h2>
        <button
          onClick={() => { setSelectedItem(null); setIsActivityModalOpen(true); }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
        >
          <Plus className="w-4 h-4" /> Add Activity
        </button>
      </div>
      <ActivityForm
        isOpen={isActivityModalOpen}
        onClose={() => setIsActivityModalOpen(false)}
        onSubmit={(data) => selectedItem ? handleUpdate('activities', selectedItem.id, data) : handleCreate('activities', data)}
        initialData={selectedItem}
      />
      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Description</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
              {crmData.activities.map((activity: any) => (
                <tr key={activity.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{activity.type}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{activity.description}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{activity.date}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                      {activity.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderTasks = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Tasks</h2>
        <button
          onClick={() => { setSelectedItem(null); setIsTaskModalOpen(true); }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
        >
          <Plus className="w-4 h-4" /> Add Task
        </button>
        <TaskForm
          isOpen={isTaskModalOpen}
          onClose={() => setIsTaskModalOpen(false)}
          onSubmit={(data) => selectedItem ? handleUpdate('tasks', selectedItem.id, data) : handleCreate('tasks', data)}
          initialData={selectedItem}
        />
      </div>
      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Priority</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Due Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Assignee</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
              {crmData.tasks.map((task: any) => (
                <tr key={task.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{task.title}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${task.priority === 'High' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                      }`}>
                      {task.priority}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{task.dueDate}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{task.assignee}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderOpportunities = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Opportunities</h2>
        <button
          onClick={() => { setSelectedItem(null); setIsOpportunityModalOpen(true); }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
        >
          <Plus className="w-4 h-4" /> Add Opportunity
        </button>
        <OpportunityForm
          isOpen={isOpportunityModalOpen}
          onClose={() => setIsOpportunityModalOpen(false)}
          onSubmit={(data) => selectedItem ? handleUpdate('opportunities', selectedItem.id, data) : handleCreate('opportunities', data)}
          initialData={selectedItem}
        />
      </div>
      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Company</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Value</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Stage</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
              {crmData.opportunities.map((opp: any) => (
                <tr key={opp.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{opp.title}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{opp.company}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">${opp.value.toLocaleString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                      {opp.stage}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  if (activeTab === 'crm-leads') return renderLeads();
  if (activeTab === 'crm-contacts') return renderContacts();
  if (activeTab === 'crm-deals') return renderDeals();
  if (activeTab === 'crm-activities') return renderActivities();
  if (activeTab === 'crm-tasks') return renderTasks();
  if (activeTab === 'crm-opportunities') return renderOpportunities();

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
                <span className={`px-2 py-1 text-xs rounded ${task.priority === 'High' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
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