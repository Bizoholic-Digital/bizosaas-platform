'use client';

import React, { useState, useEffect } from 'react';
import {
  Plus, Search, Filter, Edit, Trash2, Target, User,
  CreditCard, Calendar, CheckCircle, TrendingUp,
  BarChart3, FileText, Activity, UserPlus, Mail, Phone, RefreshCw, AlertCircle
} from 'lucide-react';
import { LeadForm } from './LeadForm'; // Keep for now
import { ContactForm } from './ContactForm'; // Need to update to use crmApi if possible
import { DealForm } from './DealForm';
import { ActivityForm } from './ActivityForm';
import { TaskForm } from './TaskForm';
import { OpportunityForm } from './OpportunityForm';
import { crmApi, CRMContact } from '@/lib/api/crm';
import { toast } from 'sonner';

interface CRMContentProps {
  activeTab: string;
}

export const CRMContent: React.FC<CRMContentProps> = ({ activeTab }) => {
  const [contacts, setContacts] = useState<CRMContact[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Modal States
  const [isContactModalOpen, setIsContactModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState<any>(null);

  // Other tabs are mock/hidden for MVP of FluentCRM
  const [mockDeals] = useState([]);
  const [mockTasks] = useState([]);

  useEffect(() => {
    if (activeTab === 'crm-contacts') {
      fetchContacts();
    }
  }, [activeTab]);

  const fetchContacts = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await crmApi.getContacts();
      if (res.error) {
        setError(res.error);
        // If error is 404/500, likely no connector
        if (res.status === 404) {
          toast.error("CRM connector not configured or contacts unavailable.");
        }
      } else {
        setContacts(res.data || []);
      }
    } catch (err) {
      console.error("Failed to fetch contacts", err);
      setError("Failed to load contacts.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateContact = async (data: any) => {
    try {
      const res = await crmApi.createContact(data);

      if (res.error) {
        toast.error(res.error);
      } else {
        toast.success("Contact created successfully");
        fetchContacts();
        setIsContactModalOpen(false);
      }
    } catch (e: any) {
      toast.error("Failed to create contact");
      console.error(e);
    }
  };

  const handleUpdateContact = async (data: any) => {
    if (!selectedItem?.id) return;

    try {
      const res = await crmApi.updateContact(selectedItem.id, data);

      if (res.error) {
        toast.error(res.error);
      } else {
        toast.success("Contact updated successfully");
        fetchContacts();
        setIsContactModalOpen(false);
      }
    } catch (e: any) {
      toast.error("Failed to update contact");
      console.error(e);
    }
  };

  const handleDeleteContact = async (id: string) => {
    if (!confirm("Are you sure you want to delete this contact?")) return;

    try {
      const res = await crmApi.deleteContact(id);

      if (res.error) {
        toast.error(res.error);
      } else {
        toast.success("Contact deleted successfully");
        fetchContacts();
      }
    } catch (e: any) {
      toast.error("Failed to delete contact");
      console.error(e);
    }
  };

  const renderContacts = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Contacts Management</h2>
        <button
          onClick={() => { setSelectedItem(null); setIsContactModalOpen(true); }}
          className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-primary/90"
        >
          <Plus className="w-4 h-4" /> Add Contact
        </button>
        <ContactForm
          isOpen={isContactModalOpen}
          onClose={() => setIsContactModalOpen(false)}
          onSubmit={selectedItem ? handleUpdateContact : handleCreateContact}
          initialData={selectedItem}
        />
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-lg flex items-center gap-2">
          <AlertCircle className="h-5 w-5" />
          {error}
        </div>
      )}

      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Phone</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
              {isLoading ? (
                <tr><td colSpan={5} className="px-6 py-12 text-center text-gray-500"><RefreshCw className="animate-spin h-6 w-6 mx-auto" /></td></tr>
              ) : contacts.length === 0 && !error ? (
                <tr><td colSpan={5} className="px-6 py-12 text-center text-gray-500">No contacts found. Sync or add a new contact.</td></tr>
              ) : (
                contacts.map((contact) => (
                  <tr key={contact.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                      {contact.first_name} {contact.last_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{contact.email}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{contact.phone || '-'}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                        {contact.status || 'Active'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-500">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => { setSelectedItem(contact); setIsContactModalOpen(true); }}
                          className="p-2 text-gray-400 hover:text-blue-600 rounded-full hover:bg-blue-50 dark:hover:bg-blue-900/20"
                          title="Edit contact"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteContact(contact.id)}
                          className="p-2 text-gray-400 hover:text-red-600 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20"
                          title="Delete contact"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderPlaceholder = (title: string) => (
    <div className="flex flex-col items-center justify-center p-12 text-center border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-lg bg-gray-50 dark:bg-gray-900/50">
      <Target className="h-12 w-12 text-gray-400 mb-4" />
      <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">{title}</h3>
      <p className="text-gray-500 dark:text-gray-400 max-w-sm mb-6">
        This module is not supported by the currently active CRM connector (FluentCRM/WordPress).
      </p>
      <button disabled className="px-4 py-2 bg-gray-200 dark:bg-gray-800 text-gray-500 rounded-lg cursor-not-allowed">
        Feature Unavailable
      </button>
    </div>
  );

  // Conditional Rendering
  if (activeTab === 'crm-contacts') return renderContacts();
  if (activeTab === 'crm-deals') return renderPlaceholder("Deals Pipeline");
  if (activeTab === 'crm-leads') return renderPlaceholder("Leads Management");
  if (activeTab === 'crm-tasks') return renderPlaceholder("Tasks");

  // Dashboard / Overview
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">CRM Overview</h2>

      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="flex items-center">
          <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
            <User className="w-6 h-6 text-green-600 dark:text-green-400" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Contacts</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">{contacts.length || '-'}</p>
          </div>
        </div>
        <div className="mt-4">
          <button onClick={() => fetchContacts()} className="text-sm text-primary hover:underline flex items-center gap-1">
            View All Contacts
          </button>
        </div>
      </div>
    </div>
  );
};