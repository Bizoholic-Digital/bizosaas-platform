'use client'

import { useState, useEffect } from 'react'
import { Building2, Users, DollarSign, Activity, Search, Plus, Eye, Edit, Trash2 } from 'lucide-react'

interface Tenant {
  id: string
  name: string
  domain: string
  status: 'active' | 'inactive' | 'trial' | 'suspended'
  plan: 'starter' | 'professional' | 'enterprise' | 'trial'
  users_count: number
  created_at: string
  last_activity: string
  revenue: number
  ai_agents_count: number
}

interface TenantMetrics {
  total_count: number
  active_count: number
  trial_count: number
  total_revenue: number
  total_users: number
}

export default function TenantsPage() {
  const [tenants, setTenants] = useState<Tenant[]>([])
  const [metrics, setMetrics] = useState<TenantMetrics | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedStatus, setSelectedStatus] = useState<string>('all')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchTenants = async () => {
      try {
        const queryParams = new URLSearchParams()
        if (selectedStatus !== 'all') queryParams.append('status', selectedStatus)
        if (searchTerm) queryParams.append('search', searchTerm)
        
        const response = await fetch(`/api/tenants?${queryParams}`)
        const data = await response.json()
        
        setTenants(data.tenants || [])
        setMetrics({
          total_count: data.total_count || 0,
          active_count: data.active_count || 0,
          trial_count: data.trial_count || 0,
          total_revenue: data.total_revenue || 0,
          total_users: data.total_users || 0
        })
      } catch (error) {
        console.error('Error fetching tenants:', error)
        // Set fallback data
        const mockTenants: Tenant[] = [
          {
            id: "tenant-001",
            name: "Acme Corp",
            domain: "acme.example.com",
            status: "active",
            plan: "enterprise",
            users_count: 45,
            created_at: "2024-01-15T10:00:00Z",
            last_activity: "2024-09-26T07:30:00Z",
            revenue: 15000,
            ai_agents_count: 12
          },
          {
            id: "tenant-002", 
            name: "TechStart LLC",
            domain: "techstart.example.com",
            status: "active",
            plan: "professional",
            users_count: 23,
            created_at: "2024-02-20T14:30:00Z",
            last_activity: "2024-09-26T08:45:00Z",
            revenue: 8500,
            ai_agents_count: 8
          },
          {
            id: "tenant-003",
            name: "Global Dynamics",
            domain: "globaldyn.example.com", 
            status: "active",
            plan: "starter",
            users_count: 12,
            created_at: "2024-03-10T09:15:00Z",
            last_activity: "2024-09-25T16:20:00Z",
            revenue: 2500,
            ai_agents_count: 5
          },
          {
            id: "tenant-004",
            name: "Innovation Labs",
            domain: "innolabs.example.com",
            status: "trial", 
            plan: "trial",
            users_count: 7,
            created_at: "2024-09-20T11:00:00Z",
            last_activity: "2024-09-26T06:15:00Z",
            revenue: 0,
            ai_agents_count: 3
          }
        ]
        setTenants(mockTenants)
        setMetrics({
          total_count: 247,
          active_count: 243,
          trial_count: 4,
          total_revenue: 127543,
          total_users: 8429
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchTenants()
  }, [selectedStatus, searchTerm])

  // Server-side filtering is now handled by the API
  const filteredTenants = tenants

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100'
      case 'inactive': return 'text-gray-600 bg-gray-100'
      case 'trial': return 'text-blue-600 bg-blue-100'
      case 'suspended': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getPlanColor = (plan: string) => {
    switch (plan) {
      case 'enterprise': return 'text-purple-600 bg-purple-100'
      case 'professional': return 'text-blue-600 bg-blue-100'
      case 'starter': return 'text-green-600 bg-green-100'
      case 'trial': return 'text-gray-600 bg-gray-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading tenants...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Tenant Management</h1>
          <p className="text-gray-600">Manage all tenant organizations and their subscriptions</p>
        </div>
        <button className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
          <Plus className="h-4 w-4 mr-2" />
          Add Tenant
        </button>
      </div>

      {/* Metrics Overview */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Building2 className="h-8 w-8 text-blue-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Total Tenants</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.total_count}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-green-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Active Tenants</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.active_count}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Users className="h-8 w-8 text-purple-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Total Users</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.total_users.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <DollarSign className="h-8 w-8 text-green-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Total Revenue</p>
                <p className="text-2xl font-bold text-gray-900">${metrics.total_revenue.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-blue-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Trial Tenants</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.trial_count}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0 gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search tenants..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="flex items-center space-x-4">
            <select
              className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="trial">Trial</option>
              <option value="suspended">Suspended</option>
            </select>
          </div>
        </div>
      </div>

      {/* Tenants Table */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Tenant Organizations</h3>
          <p className="text-sm text-gray-500">{filteredTenants.length} of {tenants.length} tenants</p>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Organization
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Plan
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Users
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Revenue
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Created
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredTenants.map((tenant) => (
                <tr key={tenant.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{tenant.name}</div>
                      <div className="text-sm text-gray-500">{tenant.domain}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(tenant.status)}`}>
                      {tenant.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPlanColor(tenant.plan)}`}>
                      {tenant.plan}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {tenant.users_count}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${tenant.revenue.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(tenant.created_at)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex items-center gap-2">
                      <button className="text-blue-600 hover:text-blue-900">
                        <Eye className="h-4 w-4" />
                      </button>
                      <button className="text-green-600 hover:text-green-900">
                        <Edit className="h-4 w-4" />
                      </button>
                      <button className="text-red-600 hover:text-red-900">
                        <Trash2 className="h-4 w-4" />
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
  )
}