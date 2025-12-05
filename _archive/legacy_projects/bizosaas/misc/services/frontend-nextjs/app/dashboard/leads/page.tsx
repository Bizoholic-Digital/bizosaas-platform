'use client';

import { useEffect, useState } from 'react';
import { 
  Users,
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
  Target,
  Activity,
  CheckCircle,
  AlertCircle,
  Clock,
  Eye,
  Edit,
  Trash2,
  RefreshCw,
  Download,
  BarChart3,
  UserPlus,
  MapPin,
  Globe,
  Building
} from 'lucide-react';

// Mock leads data - will be replaced with real API calls
const mockLeads = [
  {
    id: '1',
    first_name: 'Sarah',
    last_name: 'Johnson',
    email: 'sarah.johnson@techcorp.com',
    phone: '+1 (555) 123-4567',
    company: 'TechCorp Solutions',
    title: 'Marketing Director',
    source: 'Google Ads',
    campaign: 'Q4 Lead Generation',
    status: 'qualified',
    score: 85,
    estimated_value: 12500,
    location: 'San Francisco, CA',
    industry: 'Technology',
    employees: '50-100',
    created_at: '2024-01-15T10:30:00Z',
    last_contacted: '2024-01-15T14:20:00Z',
    next_follow_up: '2024-01-17T09:00:00Z',
    notes: 'Interested in enterprise plan, needs approval from CFO',
    tags: ['enterprise', 'high-priority', 'decision-maker']
  },
  {
    id: '2',
    first_name: 'Michael',
    last_name: 'Chen',
    email: 'mchen@startupinc.io',
    phone: '+1 (555) 987-6543',
    company: 'StartupInc',
    title: 'CEO',
    source: 'LinkedIn Ads',
    campaign: 'Product Launch - AI Tools',
    status: 'new',
    score: 72,
    estimated_value: 8900,
    location: 'Austin, TX',
    industry: 'Software',
    employees: '10-50',
    created_at: '2024-01-15T08:45:00Z',
    last_contacted: null,
    next_follow_up: '2024-01-16T10:00:00Z',
    notes: 'Downloaded product demo, showed high engagement',
    tags: ['startup', 'hot-lead', 'demo-requested']
  },
  {
    id: '3',
    first_name: 'Emily',
    last_name: 'Rodriguez',
    email: 'e.rodriguez@globalcorp.com',
    phone: '+1 (555) 456-7890',
    company: 'Global Corp',
    title: 'VP Operations',
    source: 'Facebook Ads',
    campaign: 'Holiday Season Promotion',
    status: 'nurturing',
    score: 68,
    estimated_value: 15200,
    location: 'New York, NY',
    industry: 'Finance',
    employees: '500+',
    created_at: '2024-01-14T16:20:00Z',
    last_contacted: '2024-01-15T11:30:00Z',
    next_follow_up: '2024-01-18T14:00:00Z',
    notes: 'Requires integration with existing CRM system',
    tags: ['enterprise', 'integration-needed', 'long-term']
  },
  {
    id: '4',
    first_name: 'David',
    last_name: 'Thompson',
    email: 'dthompson@consultingfirm.com',
    phone: '+1 (555) 321-0987',
    company: 'Thompson Consulting',
    title: 'Senior Consultant',
    source: 'Organic Search',
    campaign: 'Organic Traffic',
    status: 'contacted',
    score: 91,
    estimated_value: 22000,
    location: 'Chicago, IL',
    industry: 'Consulting',
    employees: '10-50',
    created_at: '2024-01-13T12:15:00Z',
    last_contacted: '2024-01-14T15:45:00Z',
    next_follow_up: '2024-01-16T16:30:00Z',
    notes: 'Very interested, requesting custom pricing proposal',
    tags: ['high-value', 'custom-pricing', 'urgent']
  },
  {
    id: '5',
    first_name: 'Lisa',
    last_name: 'Wang',
    email: 'lwang@healthtech.org',
    phone: '+1 (555) 654-3210',
    company: 'HealthTech Innovations',
    title: 'Product Manager',
    source: 'Retargeting',
    campaign: 'Retargeting - Website Visitors',
    status: 'unqualified',
    score: 34,
    estimated_value: 4500,
    location: 'Seattle, WA',
    industry: 'Healthcare',
    employees: '100-500',
    created_at: '2024-01-12T09:30:00Z',
    last_contacted: '2024-01-13T10:20:00Z',
    next_follow_up: null,
    notes: 'Budget constraints, not a fit for current offerings',
    tags: ['low-budget', 'not-ready']
  },
  {
    id: '6',
    first_name: 'Robert',
    last_name: 'Martinez',
    email: 'rmartinez@retailchain.com',
    phone: '+1 (555) 789-0123',
    company: 'Retail Chain Plus',
    title: 'IT Director',
    source: 'Google Ads',
    campaign: 'Q4 Lead Generation',
    status: 'qualified',
    score: 79,
    estimated_value: 18500,
    location: 'Miami, FL',
    industry: 'Retail',
    employees: '500+',
    created_at: '2024-01-11T14:45:00Z',
    last_contacted: '2024-01-15T09:15:00Z',
    next_follow_up: '2024-01-17T11:00:00Z',
    notes: 'Looking for multi-location deployment, Q2 timeline',
    tags: ['multi-location', 'enterprise', 'q2-timeline']
  }
];

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};

const formatDate = (dateString: string | null) => {
  if (!dateString) return 'Never';
  return new Date(dateString).toLocaleDateString();
};

const formatDateTime = (dateString: string | null) => {
  if (!dateString) return 'Not scheduled';
  return new Date(dateString).toLocaleString();
};

const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'new':
      return 'text-blue-600 bg-blue-50 border-blue-200';
    case 'contacted':
      return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    case 'qualified':
      return 'text-green-600 bg-green-50 border-green-200';
    case 'nurturing':
      return 'text-purple-600 bg-purple-50 border-purple-200';
    case 'unqualified':
      return 'text-red-600 bg-red-50 border-red-200';
    case 'converted':
      return 'text-emerald-600 bg-emerald-50 border-emerald-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
};

const getStatusIcon = (status: string) => {
  switch (status.toLowerCase()) {
    case 'new':
      return <UserPlus className="h-4 w-4" />;
    case 'contacted':
      return <Phone className="h-4 w-4" />;
    case 'qualified':
      return <CheckCircle className="h-4 w-4" />;
    case 'nurturing':
      return <Target className="h-4 w-4" />;
    case 'unqualified':
      return <AlertCircle className="h-4 w-4" />;
    case 'converted':
      return <CheckCircle className="h-4 w-4" />;
    default:
      return <Clock className="h-4 w-4" />;
  }
};

const getScoreColor = (score: number) => {
  if (score >= 80) return 'text-green-600 bg-green-100';
  if (score >= 60) return 'text-yellow-600 bg-yellow-100';
  if (score >= 40) return 'text-orange-600 bg-orange-100';
  return 'text-red-600 bg-red-100';
};

const getSourceColor = (source: string) => {
  switch (source.toLowerCase()) {
    case 'google ads':
      return 'bg-blue-100 text-blue-800';
    case 'facebook ads':
      return 'bg-blue-600 text-white';
    case 'linkedin ads':
      return 'bg-blue-800 text-white';
    case 'organic search':
      return 'bg-green-100 text-green-800';
    case 'retargeting':
      return 'bg-purple-100 text-purple-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export default function LeadsPage() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [refreshing, setRefreshing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterSource, setFilterSource] = useState('all');
  const [leads, setLeads] = useState(mockLeads);

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

  const filteredLeads = leads.filter(lead => {
    const matchesSearch = lead.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.company.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || lead.status === filterStatus;
    const matchesSource = filterSource === 'all' || lead.source === filterSource;
    return matchesSearch && matchesStatus && matchesSource;
  });

  const leadStats = {
    total: leads.length,
    new: leads.filter(l => l.status === 'new').length,
    qualified: leads.filter(l => l.status === 'qualified').length,
    nurturing: leads.filter(l => l.status === 'nurturing').length,
    converted: leads.filter(l => l.status === 'converted').length,
    totalValue: leads.reduce((sum, lead) => sum + lead.estimated_value, 0),
    avgScore: Math.round(leads.reduce((sum, lead) => sum + lead.score, 0) / leads.length)
  };

  const uniqueSources = [...new Set(leads.map(lead => lead.source))];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Sidebar */}
      <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg border-r border-gray-200">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-16 px-4 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Users className="h-8 w-8 text-violet-600" />
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
            <a href="/dashboard/leads" className="flex items-center px-3 py-2 text-sm font-medium text-violet-600 bg-violet-50 rounded-md">
              <Users className="mr-3 h-5 w-5" />
              Leads
            </a>
            <a href="/dashboard/customers" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
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
                <h1 className="text-2xl font-bold text-gray-900">Lead Management</h1>
                <p className="text-sm text-gray-600">Track and nurture your sales prospects</p>
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
                  <span>Add Lead</span>
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
          {/* Lead Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Users className="h-8 w-8 text-violet-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{leadStats.total}</h3>
                  <p className="text-sm text-gray-600">Total Leads</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <CheckCircle className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{leadStats.qualified}</h3>
                  <p className="text-sm text-gray-600">Qualified Leads</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <DollarSign className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{formatCurrency(leadStats.totalValue)}</h3>
                  <p className="text-sm text-gray-600">Pipeline Value</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Star className="h-8 w-8 text-yellow-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{leadStats.avgScore}%</h3>
                  <p className="text-sm text-gray-600">Avg. Score</p>
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
                    placeholder="Search leads..."
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
                    <option value="new">New</option>
                    <option value="contacted">Contacted</option>
                    <option value="qualified">Qualified</option>
                    <option value="nurturing">Nurturing</option>
                    <option value="unqualified">Unqualified</option>
                    <option value="converted">Converted</option>
                  </select>
                </div>

                {/* Source Filter */}
                <select
                  value={filterSource}
                  onChange={(e) => setFilterSource(e.target.value)}
                  className="border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-violet-500"
                >
                  <option value="all">All Sources</option>
                  {uniqueSources.map(source => (
                    <option key={source} value={source}>{source}</option>
                  ))}
                </select>
              </div>

              <div className="text-sm text-gray-600">
                Showing {filteredLeads.length} of {leads.length} leads
              </div>
            </div>
          </div>

          {/* Leads List */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <Users className="mr-2 h-5 w-5" />
                Lead Pipeline
              </h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {filteredLeads.map((lead) => (
                  <div key={lead.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-start space-x-4">
                        <div className="flex-shrink-0">
                          <div className="w-12 h-12 bg-violet-100 rounded-full flex items-center justify-center">
                            <span className="text-violet-600 font-medium text-sm">
                              {lead.first_name[0]}{lead.last_name[0]}
                            </span>
                          </div>
                        </div>
                        
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h3 className="text-lg font-semibold text-gray-900">
                              {lead.first_name} {lead.last_name}
                            </h3>
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getStatusColor(lead.status)}`}>
                              {getStatusIcon(lead.status)}
                              <span className="ml-1 capitalize">{lead.status}</span>
                            </span>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getScoreColor(lead.score)}`}>
                              {lead.score}% match
                            </span>
                          </div>
                          
                          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                            <div className="flex items-center">
                              <Building className="h-4 w-4 mr-1" />
                              {lead.title} at {lead.company}
                            </div>
                            <div className="flex items-center">
                              <MapPin className="h-4 w-4 mr-1" />
                              {lead.location}
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-4 text-sm text-gray-600">
                            <div className="flex items-center">
                              <Mail className="h-4 w-4 mr-1" />
                              {lead.email}
                            </div>
                            <div className="flex items-center">
                              <Phone className="h-4 w-4 mr-1" />
                              {lead.phone}
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <div className="text-right">
                          <div className="text-lg font-semibold text-gray-900">
                            {formatCurrency(lead.estimated_value)}
                          </div>
                          <div className="text-xs text-gray-500">Est. Value</div>
                        </div>
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
                    
                    {/* Lead Details */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div>
                        <div className="text-xs font-medium text-gray-500 mb-1">Source & Campaign</div>
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 rounded-md text-xs font-medium ${getSourceColor(lead.source)}`}>
                            {lead.source}
                          </span>
                          <span className="text-sm text-gray-600">{lead.campaign}</span>
                        </div>
                      </div>
                      
                      <div>
                        <div className="text-xs font-medium text-gray-500 mb-1">Company Info</div>
                        <div className="text-sm text-gray-900">
                          {lead.industry} • {lead.employees} employees
                        </div>
                      </div>
                      
                      <div>
                        <div className="text-xs font-medium text-gray-500 mb-1">Follow-up</div>
                        <div className="text-sm text-gray-900">
                          {lead.next_follow_up ? formatDateTime(lead.next_follow_up) : 'Not scheduled'}
                        </div>
                      </div>
                    </div>
                    
                    {/* Notes and Tags */}
                    {(lead.notes || lead.tags.length > 0) && (
                      <div className="border-t border-gray-100 pt-4">
                        {lead.notes && (
                          <div className="mb-3">
                            <div className="text-xs font-medium text-gray-500 mb-1">Notes</div>
                            <p className="text-sm text-gray-700">{lead.notes}</p>
                          </div>
                        )}
                        
                        {lead.tags.length > 0 && (
                          <div>
                            <div className="text-xs font-medium text-gray-500 mb-1">Tags</div>
                            <div className="flex flex-wrap gap-2">
                              {lead.tags.map(tag => (
                                <span key={tag} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-md">
                                  {tag}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                    
                    {/* Timeline */}
                    <div className="border-t border-gray-100 pt-4 mt-4">
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>Created: {formatDate(lead.created_at)}</span>
                        <span>Last contacted: {formatDate(lead.last_contacted)}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              {filteredLeads.length === 0 && (
                <div className="text-center py-8">
                  <Users className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No leads found</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {searchTerm || filterStatus !== 'all' || filterSource !== 'all'
                      ? 'Try adjusting your search or filter criteria.' 
                      : 'Get started by adding your first lead.'}
                  </p>
                  {!searchTerm && filterStatus === 'all' && filterSource === 'all' && (
                    <div className="mt-6">
                      <button className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-violet-600 hover:bg-violet-700">
                        <Plus className="h-4 w-4 mr-2" />
                        Add Lead
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