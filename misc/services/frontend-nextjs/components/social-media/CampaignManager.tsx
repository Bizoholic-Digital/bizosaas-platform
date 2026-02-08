'use client';

import { useState } from 'react';
import { 
  Plus,
  Calendar,
  DollarSign,
  Target,
  Image,
  Video,
  FileText,
  Clock,
  Users,
  MapPin,
  Hash,
  BarChart3,
  Save,
  Play,
  Pause,
  Trash2,
  Copy,
  Edit3,
  ExternalLink,
  Facebook,
  Instagram,
  Twitter,
  Linkedin,
  Youtube,
  Globe,
  Settings,
  CheckCircle2,
  AlertCircle,
  TrendingUp,
  Eye,
  MessageCircle,
  Heart,
  Share2
} from 'lucide-react';

interface Campaign {
  id: string;
  name: string;
  description: string;
  status: 'draft' | 'active' | 'paused' | 'completed' | 'scheduled';
  platforms: string[];
  budget: {
    total: number;
    daily: number;
    spent: number;
  };
  targeting: {
    ageRange: { min: number; max: number };
    genders: string[];
    locations: string[];
    interests: string[];
    behaviors: string[];
  };
  schedule: {
    startDate: string;
    endDate: string;
    timezone: string;
  };
  content: {
    type: 'image' | 'video' | 'carousel' | 'text';
    title: string;
    description: string;
    media: string[];
    callToAction: string;
    link: string;
  };
  performance: {
    impressions: number;
    clicks: number;
    conversions: number;
    cost: number;
    ctr: number;
    cpc: number;
    cpm: number;
  };
  createdAt: string;
  updatedAt: string;
}

const socialPlatforms = [
  { id: 'facebook', name: 'Facebook', icon: Facebook, color: 'text-blue-600 bg-blue-50' },
  { id: 'instagram', name: 'Instagram', icon: Instagram, color: 'text-purple-600 bg-purple-50' },
  { id: 'twitter', name: 'Twitter/X', icon: Twitter, color: 'text-gray-800 bg-gray-50' },
  { id: 'linkedin', name: 'LinkedIn', icon: Linkedin, color: 'text-blue-700 bg-blue-50' },
  { id: 'tiktok', name: 'TikTok', icon: Video, color: 'text-pink-600 bg-pink-50' },
  { id: 'youtube', name: 'YouTube', icon: Youtube, color: 'text-red-600 bg-red-50' },
  { id: 'pinterest', name: 'Pinterest', icon: MapPin, color: 'text-red-500 bg-red-50' }
];

const campaignObjectives = [
  { id: 'awareness', name: 'Brand Awareness', description: 'Increase visibility and recognition' },
  { id: 'traffic', name: 'Website Traffic', description: 'Drive visitors to your website' },
  { id: 'engagement', name: 'Engagement', description: 'Increase likes, comments, and shares' },
  { id: 'leads', name: 'Lead Generation', description: 'Capture potential customer information' },
  { id: 'conversions', name: 'Conversions', description: 'Drive sales and specific actions' },
  { id: 'app_installs', name: 'App Installs', description: 'Promote mobile app downloads' }
];

const contentTypes = [
  { id: 'image', name: 'Image', icon: Image, description: 'Single image post' },
  { id: 'video', name: 'Video', icon: Video, description: 'Video content' },
  { id: 'carousel', name: 'Carousel', icon: Image, description: 'Multiple images/videos' },
  { id: 'text', name: 'Text Only', icon: FileText, description: 'Text-based post' }
];

const mockCampaigns: Campaign[] = [
  {
    id: '1',
    name: 'Summer Product Launch',
    description: 'Promoting our new summer collection with focus on millennials',
    status: 'active',
    platforms: ['facebook', 'instagram', 'twitter'],
    budget: { total: 5000, daily: 100, spent: 3240 },
    targeting: {
      ageRange: { min: 25, max: 45 },
      genders: ['all'],
      locations: ['United States', 'Canada', 'United Kingdom'],
      interests: ['Fashion', 'Lifestyle', 'Shopping'],
      behaviors: ['Online shoppers', 'Fashion enthusiasts']
    },
    schedule: {
      startDate: '2025-09-01',
      endDate: '2025-09-30',
      timezone: 'UTC'
    },
    content: {
      type: 'image',
      title: 'Summer Collection 2025',
      description: 'Discover our latest summer styles. Limited time offer - 30% off!',
      media: ['summer-collection.jpg'],
      callToAction: 'Shop Now',
      link: 'https://example.com/summer-collection'
    },
    performance: {
      impressions: 245893,
      clicks: 5834,
      conversions: 87,
      cost: 3240,
      ctr: 2.38,
      cpc: 0.56,
      cpm: 13.18
    },
    createdAt: '2025-08-25T10:00:00Z',
    updatedAt: '2025-09-14T15:30:00Z'
  },
  {
    id: '2',
    name: 'Brand Awareness Q4',
    description: 'Building brand recognition in professional networks',
    status: 'scheduled',
    platforms: ['linkedin', 'youtube'],
    budget: { total: 8000, daily: 150, spent: 0 },
    targeting: {
      ageRange: { min: 28, max: 55 },
      genders: ['all'],
      locations: ['United States', 'Canada'],
      interests: ['Business', 'Technology', 'Marketing'],
      behaviors: ['B2B decision makers', 'Business professionals']
    },
    schedule: {
      startDate: '2025-10-01',
      endDate: '2025-12-31',
      timezone: 'UTC'
    },
    content: {
      type: 'video',
      title: 'Innovation in Business Solutions',
      description: 'See how leading companies are transforming with our platform',
      media: ['brand-video.mp4'],
      callToAction: 'Learn More',
      link: 'https://example.com/solutions'
    },
    performance: {
      impressions: 0,
      clicks: 0,
      conversions: 0,
      cost: 0,
      ctr: 0,
      cpc: 0,
      cpm: 0
    },
    createdAt: '2025-09-10T14:00:00Z',
    updatedAt: '2025-09-10T14:00:00Z'
  }
];

interface CampaignManagerProps {
  onClose?: () => void;
}

export default function CampaignManager({ onClose }: CampaignManagerProps) {
  const [activeTab, setActiveTab] = useState<'campaigns' | 'create' | 'analytics'>('campaigns');
  const [selectedCampaign, setSelectedCampaign] = useState<Campaign | null>(null);
  const [campaigns] = useState<Campaign[]>(mockCampaigns);
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Form state for campaign creation
  const [newCampaign, setNewCampaign] = useState({
    name: '',
    description: '',
    objective: '',
    platforms: [] as string[],
    budget: { total: 1000, daily: 50 },
    targeting: {
      ageRange: { min: 18, max: 65 },
      genders: ['all'],
      locations: ['United States'],
      interests: [] as string[],
      behaviors: [] as string[]
    },
    schedule: {
      startDate: new Date().toISOString().split('T')[0],
      endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      timezone: 'UTC'
    },
    content: {
      type: 'image' as const,
      title: '',
      description: '',
      media: [] as string[],
      callToAction: 'Learn More',
      link: ''
    }
  });

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(2)}%`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'scheduled':
        return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'paused':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'completed':
        return 'text-gray-600 bg-gray-50 border-gray-200';
      case 'draft':
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getPlatformIcon = (platformId: string) => {
    const platform = socialPlatforms.find(p => p.id === platformId);
    return platform ? platform.icon : Globe;
  };

  const handleCreateCampaign = () => {
    // Here you would typically send the campaign data to your API
    console.log('Creating campaign:', newCampaign);
    setShowCreateModal(false);
    // Reset form
    setNewCampaign({
      name: '',
      description: '',
      objective: '',
      platforms: [],
      budget: { total: 1000, daily: 50 },
      targeting: {
        ageRange: { min: 18, max: 65 },
        genders: ['all'],
        locations: ['United States'],
        interests: [],
        behaviors: []
      },
      schedule: {
        startDate: new Date().toISOString().split('T')[0],
        endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        timezone: 'UTC'
      },
      content: {
        type: 'image',
        title: '',
        description: '',
        media: [],
        callToAction: 'Learn More',
        link: ''
      }
    });
  };

  const togglePlatform = (platformId: string) => {
    setNewCampaign(prev => ({
      ...prev,
      platforms: prev.platforms.includes(platformId)
        ? prev.platforms.filter(p => p !== platformId)
        : [...prev.platforms, platformId]
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold text-gray-900 flex items-center">
            <Target className="mr-2 h-6 w-6" />
            Campaign Manager
          </h2>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowCreateModal(true)}
              className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="mr-2 h-4 w-4" />
              Create Campaign
            </button>
            {onClose && (
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            )}
          </div>
        </div>
        
        {/* Tabs */}
        <div className="flex space-x-6 mt-4">
          <button
            onClick={() => setActiveTab('campaigns')}
            className={`pb-2 px-1 border-b-2 font-medium text-sm transition-colors ${
              activeTab === 'campaigns'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            All Campaigns
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`pb-2 px-1 border-b-2 font-medium text-sm transition-colors ${
              activeTab === 'analytics'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            Performance Analytics
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {activeTab === 'campaigns' && (
          <div className="space-y-6">
            {/* Campaign List */}
            <div className="grid gap-6">
              {campaigns.map((campaign) => (
                <div
                  key={campaign.id}
                  className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <h3 className="text-xl font-semibold text-gray-900">{campaign.name}</h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(campaign.status)}`}>
                        {campaign.status.charAt(0).toUpperCase() + campaign.status.slice(1)}
                      </span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                        <Edit3 className="h-4 w-4" />
                      </button>
                      <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                        <Copy className="h-4 w-4" />
                      </button>
                      <button className="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50">
                        <Play className="h-4 w-4" />
                      </button>
                      <button className="p-2 text-gray-400 hover:text-yellow-600 rounded-lg hover:bg-yellow-50">
                        <Pause className="h-4 w-4" />
                      </button>
                      <button className="p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50">
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  
                  <p className="text-gray-600 mb-4">{campaign.description}</p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-4">
                    {/* Platforms */}
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Platforms</h4>
                      <div className="flex items-center space-x-2">
                        {campaign.platforms.map(platformId => {
                          const IconComponent = getPlatformIcon(platformId);
                          const platform = socialPlatforms.find(p => p.id === platformId);
                          return (
                            <div
                              key={platformId}
                              className={`p-2 rounded-lg ${platform?.color || 'text-gray-600 bg-gray-50'}`}
                            >
                              <IconComponent className="h-4 w-4" />
                            </div>
                          );
                        })}
                      </div>
                    </div>
                    
                    {/* Budget */}
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Budget</h4>
                      <div className="text-sm text-gray-600">
                        <div>Total: {formatCurrency(campaign.budget.total)}</div>
                        <div>Spent: {formatCurrency(campaign.budget.spent)}</div>
                        <div>Daily: {formatCurrency(campaign.budget.daily)}</div>
                      </div>
                    </div>
                    
                    {/* Schedule */}
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Schedule</h4>
                      <div className="text-sm text-gray-600">
                        <div>Start: {new Date(campaign.schedule.startDate).toLocaleDateString()}</div>
                        <div>End: {new Date(campaign.schedule.endDate).toLocaleDateString()}</div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Performance Metrics */}
                  {campaign.performance.impressions > 0 && (
                    <div className="grid grid-cols-2 md:grid-cols-7 gap-4 pt-4 border-t border-gray-200">
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatNumber(campaign.performance.impressions)}</div>
                        <div className="text-xs text-gray-600">Impressions</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatNumber(campaign.performance.clicks)}</div>
                        <div className="text-xs text-gray-600">Clicks</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{campaign.performance.conversions}</div>
                        <div className="text-xs text-gray-600">Conversions</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatPercentage(campaign.performance.ctr)}</div>
                        <div className="text-xs text-gray-600">CTR</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatCurrency(campaign.performance.cpc)}</div>
                        <div className="text-xs text-gray-600">CPC</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatCurrency(campaign.performance.cpm)}</div>
                        <div className="text-xs text-gray-600">CPM</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatCurrency(campaign.performance.cost)}</div>
                        <div className="text-xs text-gray-600">Total Cost</div>
                      </div>
                    </div>
                  )}
                  
                  {/* Budget Progress */}
                  <div className="mt-4">
                    <div className="flex items-center justify-between text-sm text-gray-600 mb-1">
                      <span>Budget Progress</span>
                      <span>{formatPercentage((campaign.budget.spent / campaign.budget.total) * 100)}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                        style={{ width: `${Math.min((campaign.budget.spent / campaign.budget.total) * 100, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="space-y-6">
            {/* Performance Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-blue-50 p-6 rounded-lg">
                <div className="flex items-center">
                  <Eye className="h-8 w-8 text-blue-600" />
                  <div className="ml-4">
                    <h3 className="text-2xl font-bold text-gray-900">245.9K</h3>
                    <p className="text-sm text-gray-600">Total Impressions</p>
                  </div>
                </div>
              </div>
              <div className="bg-green-50 p-6 rounded-lg">
                <div className="flex items-center">
                  <MessageCircle className="h-8 w-8 text-green-600" />
                  <div className="ml-4">
                    <h3 className="text-2xl font-bold text-gray-900">5.8K</h3>
                    <p className="text-sm text-gray-600">Total Clicks</p>
                  </div>
                </div>
              </div>
              <div className="bg-purple-50 p-6 rounded-lg">
                <div className="flex items-center">
                  <Target className="h-8 w-8 text-purple-600" />
                  <div className="ml-4">
                    <h3 className="text-2xl font-bold text-gray-900">87</h3>
                    <p className="text-sm text-gray-600">Conversions</p>
                  </div>
                </div>
              </div>
              <div className="bg-yellow-50 p-6 rounded-lg">
                <div className="flex items-center">
                  <DollarSign className="h-8 w-8 text-yellow-600" />
                  <div className="ml-4">
                    <h3 className="text-2xl font-bold text-gray-900">$3,240</h3>
                    <p className="text-sm text-gray-600">Total Spent</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Platform Performance */}
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Platform Performance</h3>
              <div className="space-y-3">
                {socialPlatforms.slice(0, 4).map((platform, index) => {
                  const IconComponent = platform.icon;
                  const performance = [2.38, 1.94, 3.12, 1.76][index];
                  return (
                    <div key={platform.id} className="flex items-center justify-between p-3 bg-white rounded-lg">
                      <div className="flex items-center space-x-3">
                        <IconComponent className="h-5 w-5" />
                        <span className="font-medium">{platform.name}</span>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold">{formatPercentage(performance)}</div>
                        <div className="text-sm text-gray-600">CTR</div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Create Campaign Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-semibold text-gray-900">Create New Campaign</h3>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ×
                </button>
              </div>
            </div>
            
            <div className="p-6 space-y-6">
              {/* Campaign Basic Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Campaign Name</label>
                  <input
                    type="text"
                    value={newCampaign.name}
                    onChange={(e) => setNewCampaign(prev => ({ ...prev, name: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter campaign name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Campaign Objective</label>
                  <select
                    value={newCampaign.objective}
                    onChange={(e) => setNewCampaign(prev => ({ ...prev, objective: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Select objective</option>
                    {campaignObjectives.map(objective => (
                      <option key={objective.id} value={objective.id}>{objective.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  value={newCampaign.description}
                  onChange={(e) => setNewCampaign(prev => ({ ...prev, description: e.target.value }))}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows={3}
                  placeholder="Describe your campaign goals and strategy"
                />
              </div>

              {/* Platform Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Select Platforms</label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {socialPlatforms.map(platform => {
                    const IconComponent = platform.icon;
                    const isSelected = newCampaign.platforms.includes(platform.id);
                    return (
                      <button
                        key={platform.id}
                        onClick={() => togglePlatform(platform.id)}
                        className={`flex items-center space-x-2 p-3 rounded-lg border transition-all ${
                          isSelected
                            ? 'bg-blue-50 border-blue-300 text-blue-700'
                            : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        <IconComponent className="h-5 w-5" />
                        <span className="text-sm font-medium">{platform.name}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Budget Settings */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Total Budget ($)</label>
                  <input
                    type="number"
                    value={newCampaign.budget.total}
                    onChange={(e) => setNewCampaign(prev => ({
                      ...prev,
                      budget: { ...prev.budget, total: Number(e.target.value) }
                    }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="1000"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Daily Budget ($)</label>
                  <input
                    type="number"
                    value={newCampaign.budget.daily}
                    onChange={(e) => setNewCampaign(prev => ({
                      ...prev,
                      budget: { ...prev.budget, daily: Number(e.target.value) }
                    }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="50"
                  />
                </div>
              </div>

              {/* Schedule */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                  <input
                    type="date"
                    value={newCampaign.schedule.startDate}
                    onChange={(e) => setNewCampaign(prev => ({
                      ...prev,
                      schedule: { ...prev.schedule, startDate: e.target.value }
                    }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
                  <input
                    type="date"
                    value={newCampaign.schedule.endDate}
                    onChange={(e) => setNewCampaign(prev => ({
                      ...prev,
                      schedule: { ...prev.schedule, endDate: e.target.value }
                    }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
              <button
                onClick={() => setShowCreateModal(false)}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateCampaign}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Create Campaign
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}