'use client';

import { useEffect, useState } from 'react';
import { 
  Building,
  Search,
  Filter,
  Plus,
  MoreHorizontal,
  Mail,
  Phone,
  Calendar,
  Star,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Users,
  Activity,
  CheckCircle,
  AlertTriangle,
  Clock,
  Eye,
  Edit,
  CreditCard,
  RefreshCw,
  Download,
  BarChart3,
  Target,
  MapPin,
  Globe,
  Award,
  Zap,
  ShoppingBag,
  FileText,
  UserCheck
} from 'lucide-react';

// Mock customers data - will be replaced with real API calls
const mockCustomers = [
  {
    id: '1',
    company_name: 'TechCorp Solutions',
    contact_name: 'Sarah Johnson',
    email: 'sarah.johnson@techcorp.com',
    phone: '+1 (555) 123-4567',
    industry: 'Technology',
    company_size: '50-100',
    location: 'San Francisco, CA',
    subscription_plan: 'Enterprise',
    monthly_recurring_revenue: 1250,
    total_revenue: 15000,
    contract_start: '2023-06-15',
    contract_end: '2024-06-14',
    status: 'active',
    health_score: 92,
    last_login: '2024-01-15T14:30:00Z',
    support_tickets: 3,
    success_manager: 'Alex Thompson',
    acquisition_channel: 'Google Ads',
    lifetime_value: 28500,
    churn_risk: 'low',
    renewal_date: '2024-06-14',
    features_used: ['CRM', 'Analytics', 'AI Agents', 'Automation'],
    onboarding_completion: 100,
    engagement_score: 89,
    nps_score: 9
  },
  {
    id: '2',
    company_name: 'StartupInc',
    contact_name: 'Michael Chen',
    email: 'mchen@startupinc.io',
    phone: '+1 (555) 987-6543',
    industry: 'Software',
    company_size: '10-50',
    location: 'Austin, TX',
    subscription_plan: 'Professional',
    monthly_recurring_revenue: 599,
    total_revenue: 7188,
    contract_start: '2023-02-01',
    contract_end: '2024-01-31',
    status: 'active',
    health_score: 78,
    last_login: '2024-01-14T10:45:00Z',
    support_tickets: 8,
    success_manager: 'Emma Wilson',
    acquisition_channel: 'LinkedIn Ads',
    lifetime_value: 14500,
    churn_risk: 'medium',
    renewal_date: '2024-01-31',
    features_used: ['CRM', 'Analytics', 'Automation'],
    onboarding_completion: 85,
    engagement_score: 72,
    nps_score: 7
  },
  {
    id: '3',
    company_name: 'Global Corp',
    contact_name: 'Emily Rodriguez',
    email: 'e.rodriguez@globalcorp.com',
    phone: '+1 (555) 456-7890',
    industry: 'Finance',
    company_size: '500+',
    location: 'New York, NY',
    subscription_plan: 'Enterprise Plus',
    monthly_recurring_revenue: 2499,
    total_revenue: 29988,
    contract_start: '2023-01-15',
    contract_end: '2025-01-14',
    status: 'active',
    health_score: 96,
    last_login: '2024-01-15T16:20:00Z',
    support_tickets: 1,
    success_manager: 'David Park',
    acquisition_channel: 'Direct Sales',
    lifetime_value: 65000,
    churn_risk: 'low',
    renewal_date: '2025-01-14',
    features_used: ['CRM', 'Analytics', 'AI Agents', 'Automation', 'White-label'],
    onboarding_completion: 100,
    engagement_score: 94,
    nps_score: 10
  },
  {
    id: '4',
    company_name: 'Thompson Consulting',
    contact_name: 'David Thompson',
    email: 'dthompson@consultingfirm.com',
    phone: '+1 (555) 321-0987',
    industry: 'Consulting',
    company_size: '10-50',
    location: 'Chicago, IL',
    subscription_plan: 'Professional',
    monthly_recurring_revenue: 899,
    total_revenue: 5394,
    contract_start: '2023-08-01',
    contract_end: '2024-07-31',
    status: 'active',
    health_score: 85,
    last_login: '2024-01-15T09:15:00Z',
    support_tickets: 5,
    success_manager: 'Lisa Chang',
    acquisition_channel: 'Organic Search',
    lifetime_value: 18500,
    churn_risk: 'low',
    renewal_date: '2024-07-31',
    features_used: ['CRM', 'Analytics', 'Reports'],
    onboarding_completion: 90,
    engagement_score: 81,
    nps_score: 8
  },
  {
    id: '5',
    company_name: 'Retail Chain Plus',
    contact_name: 'Robert Martinez',
    email: 'rmartinez@retailchain.com',
    phone: '+1 (555) 789-0123',
    industry: 'Retail',
    company_size: '500+',
    location: 'Miami, FL',
    subscription_plan: 'Enterprise',
    monthly_recurring_revenue: 1899,
    total_revenue: 11394,
    contract_start: '2023-07-01',
    contract_end: '2024-06-30',
    status: 'active',
    health_score: 73,
    last_login: '2024-01-13T11:30:00Z',
    support_tickets: 12,
    success_manager: 'Jennifer Kim',
    acquisition_channel: 'Partner Referral',
    lifetime_value: 42000,
    churn_risk: 'medium',
    renewal_date: '2024-06-30',
    features_used: ['CRM', 'Analytics', 'Automation', 'Multi-location'],
    onboarding_completion: 75,
    engagement_score: 68,
    nps_score: 6
  },
  {
    id: '6',
    company_name: 'HealthTech Innovations',
    contact_name: 'Lisa Wang',
    email: 'lwang@healthtech.org',
    phone: '+1 (555) 654-3210',
    industry: 'Healthcare',
    company_size: '100-500',
    location: 'Seattle, WA',
    subscription_plan: 'Starter',
    monthly_recurring_revenue: 199,
    total_revenue: 796,
    contract_start: '2023-11-01',
    contract_end: '2024-10-31',
    status: 'trial',
    health_score: 45,
    last_login: '2024-01-10T15:45:00Z',
    support_tickets: 15,
    success_manager: 'Marcus Johnson',
    acquisition_channel: 'Free Trial',
    lifetime_value: 2500,
    churn_risk: 'high',
    renewal_date: '2024-10-31',
    features_used: ['CRM'],
    onboarding_completion: 35,
    engagement_score: 42,
    nps_score: 4
  }
];

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};

const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString();
};

const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'active':
      return 'text-green-600 bg-green-50 border-green-200';
    case 'trial':
      return 'text-blue-600 bg-blue-50 border-blue-200';
    case 'churned':
      return 'text-red-600 bg-red-50 border-red-200';
    case 'paused':
      return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
};

const getChurnRiskColor = (risk: string) => {
  switch (risk.toLowerCase()) {
    case 'low':
      return 'text-green-600 bg-green-100';
    case 'medium':
      return 'text-yellow-600 bg-yellow-100';
    case 'high':
      return 'text-red-600 bg-red-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
};

const getHealthScoreColor = (score: number) => {
  if (score >= 80) return 'text-green-600 bg-green-100';
  if (score >= 60) return 'text-yellow-600 bg-yellow-100';
  if (score >= 40) return 'text-orange-600 bg-orange-100';
  return 'text-red-600 bg-red-100';
};

const getPlanColor = (plan: string) => {
  switch (plan.toLowerCase()) {
    case 'starter':
      return 'bg-gray-100 text-gray-800';
    case 'professional':
      return 'bg-blue-100 text-blue-800';
    case 'enterprise':
      return 'bg-purple-100 text-purple-800';
    case 'enterprise plus':
      return 'bg-violet-100 text-violet-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export default function CustomersPage() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [refreshing, setRefreshing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterPlan, setFilterPlan] = useState('all');
  const [customers, setCustomers] = useState(mockCustomers);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    setRefreshing(false);
  };

  const filteredCustomers = customers.filter(customer => {
    const matchesSearch = customer.company_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         customer.contact_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         customer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         customer.industry.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || customer.status === filterStatus;
    const matchesPlan = filterPlan === 'all' || customer.subscription_plan === filterPlan;
    return matchesSearch && matchesStatus && matchesPlan;
  });

  const customerStats = {
    total: customers.length,
    active: customers.filter(c => c.status === 'active').length,
    trial: customers.filter(c => c.status === 'trial').length,
    churned: customers.filter(c => c.status === 'churned').length,
    totalMRR: customers.reduce((sum, customer) => sum + customer.monthly_recurring_revenue, 0),
    totalRevenue: customers.reduce((sum, customer) => sum + customer.total_revenue, 0),
    avgHealthScore: Math.round(customers.reduce((sum, customer) => sum + customer.health_score, 0) / customers.length),
    avgLTV: Math.round(customers.reduce((sum, customer) => sum + customer.lifetime_value, 0) / customers.length)
  };

  const uniquePlans = [...new Set(customers.map(customer => customer.subscription_plan))];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Sidebar */}
      <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg border-r border-gray-200">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-16 px-4 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Building className="h-8 w-8 text-violet-600" />
              <span className="text-xl font-bold text-gray-900">BizOSaaS</span>
            </div>
          </div>

          {/* Navigation Menu */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            <a href="/dashboard" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <BarChart3 className="mr-3 h-5 w-5" />
              Overview
            </a>
            <a href="/dashboard/ai-agents" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Activity className="mr-3 h-5 w-5" />
              AI Agents
            </a>
            <a href="/dashboard/leads" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Users className="mr-3 h-5 w-5" />
              Leads
            </a>
            <a href="/dashboard/customers" className="flex items-center px-3 py-2 text-sm font-medium text-violet-600 bg-violet-50 rounded-md">
              <Building className="mr-3 h-5 w-5" />
              Customers
            </a>
            <a href="/dashboard/campaigns" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Target className="mr-3 h-5 w-5" />
              Campaigns
            </a>
            <a href="/dashboard/analytics" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <TrendingUp className="mr-3 h-5 w-5" />
              Analytics
            </a>
          </nav>

          {/* Real-time Status */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center space-x-2 text-sm text-green-600">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>Real-time Connected</span>
            </div>
            <div className="text-xs text-gray-500 mt-1">
              Last updated: {currentTime.toLocaleTimeString()}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="pl-64">
        {/* Top Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Customer Management</h1>
                <p className="text-sm text-gray-600">Manage customer relationships and track success metrics</p>
              </div>
              <div className="flex items-center space-x-4">
                <button className="flex items-center space-x-2 px-3 py-2 bg-gray-50 text-gray-600 rounded-md hover:bg-gray-100">
                  <Download className="h-4 w-4" />
                  <span>Export</span>
                </button>
                
                <button
                  onClick={handleRefresh}
                  disabled={refreshing}
                  className="flex items-center space-x-2 px-3 py-2 bg-gray-50 text-gray-600 rounded-md hover:bg-gray-100 disabled:opacity-50"
                >
                  <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                  <span>{refreshing ? 'Refreshing...' : 'Refresh'}</span>
                </button>
                
                <button className="flex items-center space-x-2 px-4 py-2 bg-violet-600 text-white rounded-md hover:bg-violet-700">
                  <Plus className="h-4 w-4" />
                  <span>Add Customer</span>
                </button>
                
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Calendar className="h-4 w-4" />
                  <span>{currentTime.toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="p-6 space-y-6">
          {/* Customer Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Building className="h-8 w-8 text-violet-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{customerStats.total}</h3>
                  <p className="text-sm text-gray-600">Total Customers</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <DollarSign className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{formatCurrency(customerStats.totalMRR)}</h3>
                  <p className="text-sm text-gray-600">Monthly Recurring Revenue</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <TrendingUp className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{formatCurrency(customerStats.avgLTV)}</h3>
                  <p className="text-sm text-gray-600">Avg. Lifetime Value</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Star className="h-8 w-8 text-yellow-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{customerStats.avgHealthScore}%</h3>
                  <p className="text-sm text-gray-600">Avg. Health Score</p>
                </div>
              </div>
            </div>
          </div>

          {/* Filters and Search */}
          <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
              <div className="flex items-center space-x-4">
                {/* Search */}
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search customers..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
                  />
                </div>
                
                {/* Status Filter */}
                <div className="flex items-center space-x-2">
                  <Filter className="h-4 w-4 text-gray-500" />
                  <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value)}
                    className="border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-violet-500"
                  >
                    <option value="all">All Status</option>
                    <option value="active">Active</option>
                    <option value="trial">Trial</option>
                    <option value="churned">Churned</option>
                    <option value="paused">Paused</option>
                  </select>
                </div>

                {/* Plan Filter */}
                <select
                  value={filterPlan}
                  onChange={(e) => setFilterPlan(e.target.value)}
                  className="border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-violet-500"
                >
                  <option value="all">All Plans</option>
                  {uniquePlans.map(plan => (
                    <option key={plan} value={plan}>{plan}</option>
                  ))}
                </select>
              </div>

              <div className="text-sm text-gray-600">
                Showing {filteredCustomers.length} of {customers.length} customers
              </div>
            </div>
          </div>

          {/* Customers List */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <Building className="mr-2 h-5 w-5" />
                Customer Portfolio
              </h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {filteredCustomers.map((customer) => (
                  <div key={customer.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-start space-x-4">
                        <div className="flex-shrink-0">
                          <div className="w-12 h-12 bg-violet-100 rounded-lg flex items-center justify-center">
                            <Building className="h-6 w-6 text-violet-600" />
                          </div>
                        </div>
                        
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h3 className="text-lg font-semibold text-gray-900">{customer.company_name}</h3>
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getStatusColor(customer.status)}`}>
                              <span className="capitalize">{customer.status}</span>
                            </span>
                            <span className={`px-2 py-1 rounded-md text-xs font-medium ${getPlanColor(customer.subscription_plan)}`}>
                              {customer.subscription_plan}
                            </span>
                          </div>
                          
                          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                            <div className="flex items-center">
                              <UserCheck className="h-4 w-4 mr-1" />
                              {customer.contact_name}
                            </div>
                            <div className="flex items-center">
                              <MapPin className="h-4 w-4 mr-1" />
                              {customer.location}
                            </div>
                            <div className="flex items-center">
                              <Users className="h-4 w-4 mr-1" />
                              {customer.company_size} employees
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-4 text-sm text-gray-600">
                            <div className="flex items-center">
                              <Mail className="h-4 w-4 mr-1" />
                              {customer.email}
                            </div>
                            <div className="flex items-center">
                              <Phone className="h-4 w-4 mr-1" />
                              {customer.phone}
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <div className="text-lg font-semibold text-gray-900">
                            {formatCurrency(customer.monthly_recurring_revenue)}
                          </div>
                          <div className="text-xs text-gray-500">Monthly Revenue</div>
                        </div>
                        <div className="text-right">
                          <div className={`text-sm font-medium px-2 py-1 rounded-full ${getHealthScoreColor(customer.health_score)}`}>
                            {customer.health_score}%
                          </div>
                          <div className="text-xs text-gray-500 mt-1">Health Score</div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md">
                            <Eye className="h-4 w-4" />
                          </button>
                          <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md">
                            <Edit className="h-4 w-4" />
                          </button>
                          <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md">
                            <MoreHorizontal className="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    {/* Customer Metrics */}
                    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-4">
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatCurrency(customer.total_revenue)}</div>
                        <div className="text-xs text-gray-500">Total Revenue</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatCurrency(customer.lifetime_value)}</div>
                        <div className="text-xs text-gray-500">Lifetime Value</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{customer.onboarding_completion}%</div>
                        <div className="text-xs text-gray-500">Onboarded</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{customer.engagement_score}%</div>
                        <div className="text-xs text-gray-500">Engagement</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{customer.support_tickets}</div>
                        <div className="text-xs text-gray-500">Support Tickets</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{customer.nps_score}/10</div>
                        <div className="text-xs text-gray-500">NPS Score</div>
                      </div>
                    </div>
                    
                    {/* Customer Details */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div>
                        <div className="text-xs font-medium text-gray-500 mb-1">Contract Period</div>
                        <div className="text-sm text-gray-900">
                          {formatDate(customer.contract_start)} - {formatDate(customer.contract_end)}
                        </div>
                      </div>
                      
                      <div>
                        <div className="text-xs font-medium text-gray-500 mb-1">Success Manager</div>
                        <div className="text-sm text-gray-900">{customer.success_manager}</div>
                      </div>
                      
                      <div>
                        <div className="text-xs font-medium text-gray-500 mb-1">Churn Risk</div>
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getChurnRiskColor(customer.churn_risk)}`}>
                            {customer.churn_risk} risk
                          </span>
                          <span className="text-sm text-gray-600">
                            Renewal: {formatDate(customer.renewal_date)}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    {/* Features Used */}
                    <div className="mb-4">
                      <div className="text-xs font-medium text-gray-500 mb-2">Features Used</div>
                      <div className="flex flex-wrap gap-2">
                        {customer.features_used.map(feature => (
                          <span key={feature} className="px-2 py-1 bg-violet-100 text-violet-700 text-xs rounded-md">
                            {feature}
                          </span>
                        ))}
                      </div>
                    </div>
                    
                    {/* Timeline */}
                    <div className="border-t border-gray-100 pt-4">
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>Customer since: {formatDate(customer.contract_start)}</span>
                        <span>Last login: {formatDateTime(customer.last_login)}</span>
                        <span>Acquired via: {customer.acquisition_channel}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              {filteredCustomers.length === 0 && (
                <div className="text-center py-8">
                  <Building className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No customers found</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {searchTerm || filterStatus !== 'all' || filterPlan !== 'all'
                      ? 'Try adjusting your search or filter criteria.' 
                      : 'Get started by adding your first customer.'}
                  </p>
                  {!searchTerm && filterStatus === 'all' && filterPlan === 'all' && (
                    <div className="mt-6">
                      <button className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-violet-600 hover:bg-violet-700">
                        <Plus className="h-4 w-4 mr-2" />
                        Add Customer
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}