'use client';

import React, { useState, useEffect } from 'react';
import {
  Building2,
  Search,
  Plus,
  MoreHorizontal,
  CheckCircle,
  XCircle,
  AlertCircle,
  Users,
  DollarSign,
  Activity
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface Tenant {
  id: string;
  name: string;
  domain: string;
  status: 'active' | 'suspended' | 'trial' | 'pending';
  plan: string;
  users_count: number;
  created_at: string;
  last_activity: string;
  revenue: number;
  ai_agents_count: number;
}

interface TenantStats {
  total_count: number;
  active_count: number;
  trial_count: number;
  suspended_count: number;
  total_revenue: number;
  total_users: number;
  growth_rate: number;
  churn_rate: number;
}

export default function TenantsPage() {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [stats, setStats] = useState<TenantStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchTenants();
  }, []);

  const fetchTenants = async () => {
    try {
      const response = await fetch('/api/tenants');
      const data = await response.json();
      if (data.tenants) {
        setTenants(data.tenants);
        setStats({
          total_count: data.total_count,
          active_count: data.active_count,
          trial_count: data.trial_count,
          suspended_count: data.suspended_count,
          total_revenue: data.total_revenue,
          total_users: data.total_users,
          growth_rate: data.growth_rate,
          churn_rate: data.churn_rate
        });
      }
    } catch (error) {
      console.error('Failed to fetch tenants:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredTenants = tenants.filter(tenant =>
    tenant.name.toLowerCase().includes(search.toLowerCase()) ||
    tenant.domain.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-8 space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white">Tenant Management</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-2">Manage all platform tenants, subscriptions, and access.</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700">
          <Plus className="mr-2 h-4 w-4" /> Create Tenant
        </Button>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <div className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="flex items-center justify-between space-y-0 pb-2">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Tenants</div>
              <Building2 className="h-4 w-4 text-gray-500" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total_count}</div>
            <p className="text-xs text-green-500 flex items-center mt-1">
              <Activity className="h-3 w-3 mr-1" /> +{stats.growth_rate}% from last month
            </p>
          </div>
          <div className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="flex items-center justify-between space-y-0 pb-2">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400">Active Subscriptions</div>
              <CheckCircle className="h-4 w-4 text-green-500" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">{stats.active_count}</div>
          </div>
          <div className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="flex items-center justify-between space-y-0 pb-2">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Users</div>
              <Users className="h-4 w-4 text-blue-500" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total_users.toLocaleString()}</div>
          </div>
          <div className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="flex items-center justify-between space-y-0 pb-2">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400">Monthly Revenue</div>
              <DollarSign className="h-4 w-4 text-green-500" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">${stats.total_revenue.toLocaleString()}</div>
          </div>
        </div>
      )}

      {/* Filters and Table */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <div className="relative w-72">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Search tenants..."
              className="pl-10"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="flex gap-2">
            <Button variant="outline">Filter</Button>
            <Button variant="outline">Export</Button>
          </div>
        </div>

        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Tenant Name</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Plan</TableHead>
              <TableHead>Users</TableHead>
              <TableHead>AI Agents</TableHead>
              <TableHead>Revenue</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={7} className="text-center py-10">Loading tenants...</TableCell>
              </TableRow>
            ) : filteredTenants.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="text-center py-10">No tenants found.</TableCell>
              </TableRow>
            ) : (
              filteredTenants.map((tenant) => (
                <TableRow key={tenant.id}>
                  <TableCell>
                    <div className="font-medium text-gray-900 dark:text-white">{tenant.name}</div>
                    <div className="text-sm text-gray-500">{tenant.domain}</div>
                  </TableCell>
                  <TableCell>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${tenant.status === 'active' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
                        tenant.status === 'suspended' ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' :
                          'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                      }`}>
                      {tenant.status === 'active' && <CheckCircle className="w-3 h-3 mr-1" />}
                      {tenant.status === 'suspended' && <XCircle className="w-3 h-3 mr-1" />}
                      {tenant.status === 'trial' && <AlertCircle className="w-3 h-3 mr-1" />}
                      {tenant.status.charAt(0).toUpperCase() + tenant.status.slice(1)}
                    </span>
                  </TableCell>
                  <TableCell className="capitalize">{tenant.plan}</TableCell>
                  <TableCell>{tenant.users_count}</TableCell>
                  <TableCell>{tenant.ai_agents_count}</TableCell>
                  <TableCell>${tenant.revenue.toLocaleString()}</TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <span className="sr-only">Open menu</span>
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem onClick={() => navigator.clipboard.writeText(tenant.id)}>
                          Copy Tenant ID
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>View Details</DropdownMenuItem>
                        <DropdownMenuItem>Manage Subscription</DropdownMenuItem>
                        <DropdownMenuItem className="text-red-600">Suspend Tenant</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}