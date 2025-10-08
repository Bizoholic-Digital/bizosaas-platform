'use client';

import React, { useState, useEffect, useCallback } from 'react';
import {
  Trophy, Star, Users, TrendingUp, Target, Award,
  Share2, ExternalLink, Copy, CheckCircle, Crown,
  Calendar, BarChart3, Zap, Gift, MessageSquare,
  ChevronRight, RefreshCw, Download, Eye, Heart,
  Menu, X, Home, ShoppingCart, FileText, LinkIcon,
  Settings, Bell, CreditCard, User, Bot, Moon, Sun,
  Mail, Activity, Key, Shield, Terminal, Database, Grid, Code,
  Package, ChevronDown
} from 'lucide-react';

interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  points: number;
  category: string;
  unlocked_at?: string;
  platform: string;
}

interface ProgressAchievement {
  achievement_id: string;
  name: string;
  description: string;
  current_value: number;
  target_value: number;
  progress_percentage: number;
  icon: string;
  category: string;
}

interface LeaderboardEntry {
  rank: number;
  user_id: string;
  display_name: string;
  company: string;
  score: number;
  achievements_count: number;
  platform: string;
  avatar: string;
  badges: string[];
  last_activity: string;
}

interface ReferralData {
  referral_code: string;
  tracking_url: string;
  share_templates: {
    email: string;
    twitter: string;
    linkedin: string;
    facebook: string;
  };
  reward_structure: {
    referrer_reward: {
      type: string;
      amount: number;
      description: string;
    };
    referee_reward: {
      type: string;
      amount: number;
      description: string;
    };
  };
  analytics_dashboard_url: string;
  expires_at: string;
}

export default function GamificationDashboard() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [activeGamificationTab, setActiveGamificationTab] = useState('achievements');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [theme, setTheme] = useState(() => {
    if (typeof window === "undefined") return "light";
    try {
      return localStorage.getItem("theme") || "light";
    } catch {
      return "light";
    }
  });
  const [expandedSections, setExpandedSections] = useState<{[key: string]: boolean}>({});

  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [progressAchievements, setProgressAchievements] = useState<ProgressAchievement[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [referralData, setReferralData] = useState<ReferralData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (typeof window === "undefined") return;

    try {
      document.documentElement.classList.toggle("dark", theme === "dark");
    } catch (e) {
      console.warn("Cannot set theme class");
    }

    setExpandedSections({
      "crm": false,
      "cms": false,
      "ecommerce": false,
      "marketing": false,
      "analytics": false,
      "billing": false,
      "gamification": true, // Keep gamification expanded
      "ai-agents": false,
      "integrations": false,
      "settings": false
    });
  }, [theme]);

  const toggleTheme = useCallback(() => {
    const newTheme = theme === "light" ? "dark" : "light";
    setTheme(newTheme);
    try {
      localStorage.setItem("theme", newTheme);
      document.documentElement.classList.toggle("dark", newTheme === "dark");
    } catch (e) {
      console.warn("localStorage not available");
    }
  }, [theme]);

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionId]: !prev[sectionId]
    }));
  };

  const sidebarItems = [
    {
      id: 'dashboard',
      icon: Home,
      label: 'Dashboard',
      children: []
    },
    {
      id: 'crm',
      icon: Users,
      label: 'CRM',
      children: [
        { id: 'crm-leads', label: 'Leads', icon: Target },
        { id: 'crm-contacts', label: 'Contacts', icon: User },
        { id: 'crm-deals', label: 'Deals', icon: CreditCard },
        { id: 'crm-activities', label: 'Activities', icon: Calendar },
        { id: 'crm-tasks', label: 'Tasks', icon: Activity },
        { id: 'crm-opportunities', label: 'Opportunities', icon: TrendingUp },
        { id: 'crm-pipeline', label: 'Pipeline', icon: BarChart3 },
        { id: 'crm-reports', label: 'Reports', icon: FileText }
      ]
    },
    {
      id: 'cms',
      icon: FileText,
      label: 'CMS',
      children: [
        { id: 'cms-pages', label: 'Pages', icon: FileText },
        { id: 'cms-posts', label: 'Posts', icon: Package },
        { id: 'cms-media', label: 'Media', icon: Activity },
        { id: 'cms-forms', label: 'Forms', icon: Mail },
        { id: 'cms-templates', label: 'Templates', icon: Code }
      ]
    },
    {
      id: 'ecommerce',
      icon: ShoppingCart,
      label: 'E-commerce',
      children: [
        { id: 'ecom-products', label: 'Products', icon: Package },
        { id: 'ecom-orders', label: 'Orders', icon: ShoppingCart },
        { id: 'ecom-customers', label: 'Customers', icon: Users },
        { id: 'ecom-inventory', label: 'Inventory', icon: BarChart3 },
        { id: 'ecom-coupons', label: 'Coupons', icon: Target },
        { id: 'ecom-reviews', label: 'Reviews', icon: MessageSquare }
      ]
    },
    {
      id: 'marketing',
      icon: Target,
      label: 'Marketing',
      children: [
        { id: 'marketing-campaigns', label: 'Campaigns', icon: Target },
        { id: 'marketing-email', label: 'Email Marketing', icon: Mail },
        { id: 'marketing-social', label: 'Social Media', icon: Share2 },
        { id: 'marketing-automation', label: 'Automation', icon: Zap },
        { id: 'marketing-leads', label: 'Lead Generation', icon: Users },
        { id: 'marketing-seo', label: 'SEO Tools', icon: TrendingUp }
      ]
    },
    {
      id: 'analytics',
      icon: BarChart3,
      label: 'Analytics',
      children: [
        { id: 'analytics-overview', label: 'Overview', icon: BarChart3 },
        { id: 'analytics-traffic', label: 'Traffic', icon: TrendingUp },
        { id: 'analytics-conversions', label: 'Conversions', icon: Target },
        { id: 'analytics-performance', label: 'Performance', icon: Activity },
        { id: 'analytics-goals', label: 'Goals', icon: Target },
        { id: 'analytics-insights', label: 'AI Insights', icon: Zap },
        { id: 'analytics-real-time', label: 'Real-time', icon: Activity },
        { id: 'analytics-custom', label: 'Custom Reports', icon: Settings }
      ]
    },
    {
      id: 'billing',
      icon: CreditCard,
      label: 'Billing',
      children: [
        { id: 'billing-overview', label: 'Overview', icon: BarChart3 },
        { id: 'billing-subscriptions', label: 'Subscriptions', icon: CreditCard },
        { id: 'billing-invoices', label: 'Invoices', icon: FileText },
        { id: 'billing-payment-methods', label: 'Payment Methods', icon: CreditCard },
        { id: 'billing-usage', label: 'Usage & Limits', icon: Activity },
        { id: 'billing-history', label: 'Billing History', icon: Activity },
        { id: 'billing-tax', label: 'Tax Settings', icon: Settings }
      ]
    },
    {
      id: 'gamification',
      icon: Trophy,
      label: 'Gamification',
      children: [
        { id: 'gamification-overview', label: 'Overview', icon: Trophy },
        { id: 'gamification-achievements', label: 'Achievements', icon: Award },
        { id: 'gamification-leaderboard', label: 'Leaderboard', icon: Crown },
        { id: 'gamification-referrals', label: 'Referrals', icon: Share2 },
        { id: 'gamification-portfolio', label: 'Portfolio Showcase', icon: Gift }
      ]
    },
    {
      id: 'ai-agents',
      icon: Bot,
      label: 'AI Agents',
      children: [
        { id: 'ai-agents-overview', label: 'Overview', icon: BarChart3 },
        { id: 'ai-agents-crews', label: 'Agent Crews', icon: Users },
        { id: 'ai-agents-tasks', label: 'Active Tasks', icon: Activity },
        { id: 'ai-agents-tools', label: 'Tools & Integrations', icon: Settings }
      ]
    },
    {
      id: 'integrations',
      icon: LinkIcon,
      label: 'Integrations',
      children: [
        { id: 'integrations-overview', label: 'Overview', icon: LinkIcon },
        { id: 'integrations-webhooks', label: 'Webhooks', icon: Activity },
        { id: 'integrations-api-keys', label: 'API Keys', icon: Key },
        { id: 'integrations-third-party', label: 'Third-party Apps', icon: Grid },
        { id: 'integrations-automation', label: 'Automation Rules', icon: Zap },
        { id: 'integrations-logs', label: 'Logs', icon: FileText },
        { id: 'integrations-marketplace', label: 'Marketplace', icon: ShoppingCart }
      ]
    },
    {
      id: 'settings',
      icon: Settings,
      label: 'Settings',
      children: [
        { id: 'settings-general', label: 'General', icon: Settings },
        { id: 'settings-notifications', label: 'Notifications', icon: Bell },
        { id: 'settings-security', label: 'Security', icon: Shield },
        { id: 'settings-team', label: 'Team Management', icon: Users },
        { id: 'settings-preferences', label: 'Preferences', icon: User },
        { id: 'settings-advanced', label: 'Advanced', icon: Code },
        { id: 'settings-backup', label: 'Backup & Restore', icon: Database },
        { id: 'settings-api', label: 'API Configuration', icon: Terminal }
      ]
    }
  ];

  useEffect(() => {
    loadGamificationData();
  }, []);

  const loadGamificationData = async () => {
    setLoading(true);
    try {
      // Load achievements, leaderboard, and referral data
      await Promise.all([
        loadAchievements(),
        loadLeaderboard(),
        loadReferralData()
      ]);
    } catch (error) {
      console.error('Error loading gamification data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadAchievements = async () => {
    try {
      const response = await fetch('/api/brain/gamification/achievements?tenant_id=acme&platform=bizoholic');
      if (response.ok) {
        const data = await response.json();
        setAchievements(data.unlocked_achievements || []);
        setProgressAchievements(data.progress_achievements || []);
      }
    } catch (error) {
      console.error('Error loading achievements:', error);
      // Set fallback data
      setAchievements([
        {
          id: '1',
          name: 'First Campaign',
          description: 'Successfully launched your first marketing campaign',
          icon: '🚀',
          points: 100,
          category: 'Marketing',
          unlocked_at: '2024-01-15T10:00:00Z',
          platform: 'bizoholic'
        }
      ]);
    }
  };

  const loadLeaderboard = async () => {
    try {
      const response = await fetch('/api/brain/gamification/leaderboards?platform=bizoholic&type=performance&period=monthly');
      if (response.ok) {
        const data = await response.json();
        setLeaderboard(data.leaderboard || []);
      }
    } catch (error) {
      console.error('Error loading leaderboard:', error);
      // Set fallback data
      setLeaderboard([
        {
          rank: 1,
          user_id: 'user1',
          display_name: 'Sarah Wilson',
          company: 'TechStart Inc.',
          score: 2847,
          achievements_count: 23,
          platform: 'bizoholic',
          avatar: '/avatars/sarah.jpg',
          badges: ['top-performer', 'campaign-master'],
          last_activity: '2024-01-25T15:30:00Z'
        }
      ]);
    }
  };

  const loadReferralData = async () => {
    try {
      const response = await fetch('/api/brain/gamification/referrals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tenant_id: 'acme', platform: 'bizoholic' })
      });
      if (response.ok) {
        const data = await response.json();
        setReferralData(data);
      }
    } catch (error) {
      console.error('Error loading referral data:', error);
    }
  };

  const renderSidebarItem = (item: any, level = 0) => {
    const Icon = item.icon;
    const isActive = activeTab === item.id || (item.id === 'gamification' && activeTab.startsWith('gamification'));
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedSections[item.id];

    return (
      <div key={item.id}>
        <button
          onClick={() => {
            if (hasChildren) {
              toggleSection(item.id);
              setActiveTab(item.id);
            } else {
              setActiveTab(item.id);
              if (item.id.startsWith('gamification-')) {
                setActiveGamificationTab(item.id.replace('gamification-', ''));
              }
            }
          }}
          className={`w-full flex items-center px-3 py-2 text-left rounded-lg transition-colors ${
            isActive
              ? 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400'
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
          } ${level > 0 ? 'ml-4' : ''}`}
        >
          <Icon className="w-4 h-4 mr-3 flex-shrink-0" />
          {isSidebarOpen && (
            <>
              <span className="flex-1">{item.label}</span>
              {hasChildren && (
                isExpanded
                  ? <ChevronDown className="w-4 h-4" />
                  : <ChevronRight className="w-4 h-4" />
              )}
            </>
          )}
        </button>
        {hasChildren && isExpanded && isSidebarOpen && (
          <div className="mt-1 space-y-1">
            {item.children.map((child: any) => renderSidebarItem(child, level + 1))}
          </div>
        )}
      </div>
    );
  };

  const renderGamificationContent = () => {
    if (loading) {
      return (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          <span className="ml-3 text-gray-600 dark:text-gray-400">Loading gamification data...</span>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        {/* Gamification Tab Navigation */}
        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex space-x-1 p-1">
            {[
              { id: 'achievements', label: 'Achievements', icon: Award },
              { id: 'leaderboard', label: 'Leaderboard', icon: Crown },
              { id: 'referrals', label: 'Referrals', icon: Share2 },
              { id: 'portfolio', label: 'Portfolio', icon: Gift }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveGamificationTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                    activeGamificationTab === tab.id
                      ? 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400'
                      : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Gamification Content */}
        {activeGamificationTab === 'achievements' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Your Achievements</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {achievements.map((achievement) => (
                <div key={achievement.id} className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-6 hover:shadow-lg transition-shadow">
                  <div className="flex items-center justify-between mb-4">
                    <div className="text-3xl">{achievement.icon}</div>
                    <span className="bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400 px-2 py-1 rounded-full text-sm font-medium">
                      {achievement.points} pts
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {achievement.name}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
                    {achievement.description}
                  </p>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500 dark:text-gray-400">{achievement.category}</span>
                    {achievement.unlocked_at && (
                      <span className="text-green-600 dark:text-green-400">Unlocked!</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeGamificationTab === 'leaderboard' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Leaderboard</h2>
            <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 dark:bg-gray-800">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Rank
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        User
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Score
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Achievements
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                    {leaderboard.map((entry) => (
                      <tr key={entry.user_id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            {entry.rank === 1 && <Crown className="w-5 h-5 text-yellow-500 mr-2" />}
                            {entry.rank === 2 && <Award className="w-5 h-5 text-gray-400 mr-2" />}
                            {entry.rank === 3 && <Award className="w-5 h-5 text-orange-500 mr-2" />}
                            <span className="text-sm font-medium text-gray-900 dark:text-white">
                              #{entry.rank}
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="h-10 w-10 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center">
                              <User className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                            </div>
                            <div className="ml-4">
                              <div className="text-sm font-medium text-gray-900 dark:text-white">
                                {entry.display_name}
                              </div>
                              <div className="text-sm text-gray-500 dark:text-gray-400">
                                {entry.company}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                          {entry.score.toLocaleString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                          {entry.achievements_count}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeGamificationTab === 'referrals' && referralData && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Referral Program</h2>
            <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-6">
              <div className="text-center mb-6">
                <Share2 className="w-12 h-12 text-purple-600 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Your Referral Code</h3>
                <div className="flex items-center justify-center space-x-2">
                  <code className="bg-gray-100 dark:bg-gray-800 px-4 py-2 rounded-lg text-lg font-mono">
                    {referralData.referral_code}
                  </code>
                  <button className="p-2 text-gray-400 hover:text-blue-600">
                    <Copy className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                  <h4 className="font-semibold text-green-800 dark:text-green-400 mb-2">Your Reward</h4>
                  <p className="text-green-600 dark:text-green-300">
                    {referralData.reward_structure.referrer_reward.description}
                  </p>
                </div>
                <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-800 dark:text-blue-400 mb-2">Friend's Reward</h4>
                  <p className="text-blue-600 dark:text-blue-300">
                    {referralData.reward_structure.referee_reward.description}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeGamificationTab === 'portfolio' && (
          <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-8 text-center">
            <Award className="w-12 h-12 text-purple-600 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">AI Portfolio Showcase</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Generate a professional portfolio showcasing your achievements and success stories
            </p>
            <button className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 flex items-center space-x-2 mx-auto">
              <Zap className="w-5 h-5" />
              <span>Generate Portfolio</span>
            </button>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex">
      {/* Sidebar */}
      <div className={`${isSidebarOpen ? 'w-64' : 'w-16'} transition-all duration-300 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col`}>
        {/* Header */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between">
            {isSidebarOpen && (
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">CP</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Client Portal</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">BizOSaaS Platform</p>
                </div>
              </div>
            )}
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              {isSidebarOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {sidebarItems.map((item) => renderSidebarItem(item))}
        </nav>

        {/* User Info */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-800">
          {isSidebarOpen && (
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">AC</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                  Acme Corporation
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Premium Plan
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <header className="bg-white shadow-sm border-b border-gray-200 dark:bg-gray-900 dark:border-gray-800 p-4">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
              Gamification Hub
            </h1>
            <div className="flex items-center space-x-4">
              <button
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors relative"
                title="Notifications"
              >
                <Bell className="w-5 h-5" />
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full text-xs flex items-center justify-center">
                  <span className="w-2 h-2 bg-white rounded-full"></span>
                </span>
              </button>
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
              >
                {theme === 'light' ? (
                  <Moon className="w-5 h-5" />
                ) : (
                  <Sun className="w-5 h-5" />
                )}
              </button>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 p-6">
          {renderGamificationContent()}
        </main>
      </div>
    </div>
  );
}