/**
 * Multi-Platform Navigation Tabs Component
 * Provides seamless navigation between Bizoholic, CoreLDove, Directory, and Admin platforms
 * Supports role-based access control and real-time platform status
 */

import React, { useState, useEffect } from 'react';
import { 
  ChevronDownIcon, 
  DatabaseIcon, 
  LayoutDashboardIcon, 
  MegaphoneIcon,
  ShoppingCartIcon,
  BuildingIcon,
  MessageCircleIcon 
} from 'lucide-react';

interface Platform {
  id: string;
  name: string;
  url: string;
  description: string;
  icon: string;
  status: 'active' | 'inactive' | 'maintenance';
  current: boolean;
  features: string[];
  access_level: 'super_admin' | 'admin' | 'manager' | 'client';
  category: 'admin' | 'platform' | 'tools';
}

interface User {
  role: string;
  permissions: string[];
  tenant_id?: string;
}

interface PlatformTabsProps {
  user: User;
  currentPlatform?: string;
  onPlatformSwitch?: (platform: Platform) => void;
  apiBaseUrl?: string;
}

const ICON_MAP = {
  'database': DatabaseIcon,
  'layout-dashboard': LayoutDashboardIcon,
  'megaphone': MegaphoneIcon,
  'shopping-cart': ShoppingCartIcon,
  'building': BuildingIcon,
  'message-circle': MessageCircleIcon,
};

const STATUS_COLORS = {
  active: 'text-green-600 bg-green-100',
  inactive: 'text-red-600 bg-red-100', 
  maintenance: 'text-amber-600 bg-amber-100'
};

export const PlatformTabs: React.FC<PlatformTabsProps> = ({
  user,
  currentPlatform = 'tailadmin',
  onPlatformSwitch,
  apiBaseUrl = '/api'
}) => {
  const [platforms, setPlatforms] = useState<Platform[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAdminDropdown, setShowAdminDropdown] = useState(false);
  const [showPlatformsDropdown, setShowPlatformsDropdown] = useState(false);

  useEffect(() => {
    fetchPlatforms();
  }, [user]);

  const fetchPlatforms = async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/platforms`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setPlatforms(data.platforms || []);
      }
    } catch (error) {
      console.error('Failed to fetch platforms:', error);
      // Fallback to default platforms
      setPlatforms(getDefaultPlatforms());
    } finally {
      setLoading(false);
    }
  };

  const getDefaultPlatforms = (): Platform[] => {
    const base: Platform[] = [];
    
    // Admin platforms for admin users
    if (user.role === 'super_admin' || user.role === 'tenant_admin') {
      base.push({
        id: 'tailadmin',
        name: 'TailAdmin v2',
        url: 'http://localhost:3001/',
        description: 'Business Operations Dashboard',
        icon: 'layout-dashboard',
        status: 'active',
        current: currentPlatform === 'tailadmin',
        features: ['Analytics', 'User Management', 'AI Agents', 'System Monitor'],
        access_level: 'admin',
        category: 'admin'
      });
    }

    if (user.role === 'super_admin') {
      base.push({
        id: 'sqladmin',
        name: 'SQLAdmin',
        url: 'http://localhost:5000/',
        description: 'Infrastructure Management',
        icon: 'database',
        status: 'active',
        current: currentPlatform === 'sqladmin',
        features: ['Database Admin', 'System Health', 'Monitoring', 'Logs'],
        access_level: 'super_admin',
        category: 'admin'
      });
    }

    // Business platforms for manager+ users
    if (user.role === 'super_admin' || user.role === 'tenant_admin' || user.role === 'manager') {
      base.push(
        {
          id: 'bizoholic',
          name: 'Bizoholic',
          url: 'http://localhost:3000',
          description: 'AI Marketing Agency Platform',
          icon: 'megaphone',
          status: 'active',
          current: currentPlatform === 'bizoholic',
          features: ['Marketing Campaigns', 'AI Agents', 'Analytics', 'CRM'],
          access_level: 'manager',
          category: 'platform'
        },
        {
          id: 'coreldove',
          name: 'CoreLDove',
          url: 'http://localhost:3001',
          description: 'E-commerce & Dropshipping Platform',
          icon: 'shopping-cart',
          status: 'active',
          current: currentPlatform === 'coreldove',
          features: ['Product Sourcing', 'Inventory', 'Orders', 'Saleor Backend'],
          access_level: 'manager',
          category: 'platform'
        },
        {
          id: 'directory',
          name: 'Directory',
          url: 'http://localhost:8003/directories',
          description: 'Business Directory Management',
          icon: 'building',
          status: 'active',
          current: currentPlatform === 'directory',
          features: ['Business Listings', 'Directory Sync', 'Local SEO', 'Lead Gen'],
          access_level: 'manager',
          category: 'platform'
        }
      );
    }

    // AI tools for all authenticated users
    base.push({
      id: 'ai-chat',
      name: 'AI Assistant',
      url: 'http://localhost:3003',
      description: 'Universal AI Chat & Agent Management',
      icon: 'message-circle',
      status: 'active',
      current: currentPlatform === 'ai-chat',
      features: ['AI Chat', 'Agent Status', 'Automation', 'Analytics'],
      access_level: 'client',
      category: 'tools'
    });

    return base;
  };

  const handlePlatformClick = (platform: Platform) => {
    if (platform.current) return;
    
    if (onPlatformSwitch) {
      onPlatformSwitch(platform);
    } else {
      // Default behavior: open platform in new tab for external platforms
      if (platform.category === 'platform' || platform.category === 'tools') {
        window.open(platform.url, '_blank');
      } else {
        window.location.href = platform.url;
      }
    }
  };

  if (loading) {
    return <div className="animate-pulse bg-gray-200 rounded h-8 w-32"></div>;
  }

  const adminPlatforms = platforms.filter(p => p.category === 'admin' && !p.current);
  const businessPlatforms = platforms.filter(p => p.category === 'platform');
  const toolPlatforms = platforms.filter(p => p.category === 'tools');

  return (
    <div className="flex items-center space-x-2">
      {/* Admin Dashboards Dropdown */}
      {adminPlatforms.length > 0 && (
        <div className="relative">
          <button
            onClick={() => {
              setShowAdminDropdown(!showAdminDropdown);
              setShowPlatformsDropdown(false);
            }}
            className="bg-indigo-600 text-white px-3 py-1 rounded text-sm hover:bg-indigo-700 flex items-center space-x-1"
          >
            <span>Admin</span>
            <ChevronDownIcon className="w-4 h-4" />
          </button>
          
          {showAdminDropdown && (
            <div className="absolute right-0 mt-2 w-64 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 z-50">
              <div className="py-1">
                <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">
                  Admin Dashboards
                </div>
                {adminPlatforms.map((platform) => {
                  const IconComponent = ICON_MAP[platform.icon as keyof typeof ICON_MAP] || DatabaseIcon;
                  return (
                    <button
                      key={platform.id}
                      onClick={() => handlePlatformClick(platform)}
                      className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700 flex items-center space-x-2"
                    >
                      <div className={`w-2 h-2 rounded-full ${STATUS_COLORS[platform.status].split(' ')[1]}`}></div>
                      <IconComponent className="w-4 h-4" />
                      <div>
                        <div className="font-medium">{platform.name}</div>
                        <div className="text-xs text-gray-500">{platform.description}</div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Business Platforms Dropdown */}
      {businessPlatforms.length > 0 && (
        <div className="relative">
          <button
            onClick={() => {
              setShowPlatformsDropdown(!showPlatformsDropdown);
              setShowAdminDropdown(false);
            }}
            className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 flex items-center space-x-1"
          >
            <span>Platforms</span>
            <ChevronDownIcon className="w-4 h-4" />
          </button>
          
          {showPlatformsDropdown && (
            <div className="absolute right-0 mt-2 w-72 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 z-50">
              <div className="py-1">
                <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">
                  Business Platforms
                </div>
                {businessPlatforms.map((platform) => {
                  const IconComponent = ICON_MAP[platform.icon as keyof typeof ICON_MAP] || MegaphoneIcon;
                  return (
                    <button
                      key={platform.id}
                      onClick={() => handlePlatformClick(platform)}
                      className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700 flex items-center space-x-2"
                    >
                      <div className={`w-2 h-2 rounded-full ${STATUS_COLORS[platform.status].split(' ')[1]}`}></div>
                      <IconComponent className="w-4 h-4" />
                      <div className="flex-1">
                        <div className="font-medium">{platform.name}</div>
                        <div className="text-xs text-gray-500">{platform.description}</div>
                        <div className="text-xs text-blue-600 mt-1">
                          {platform.features.slice(0, 2).join(', ')}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {/* AI Tools Direct Link */}
      {toolPlatforms.length > 0 && (
        <button
          onClick={() => handlePlatformClick(toolPlatforms[0])}
          className="bg-emerald-600 text-white px-3 py-1 rounded text-sm hover:bg-emerald-700 flex items-center space-x-1"
        >
          <MessageCircleIcon className="w-4 h-4" />
          <span>AI Assistant</span>
        </button>
      )}
    </div>
  );
};

export default PlatformTabs;