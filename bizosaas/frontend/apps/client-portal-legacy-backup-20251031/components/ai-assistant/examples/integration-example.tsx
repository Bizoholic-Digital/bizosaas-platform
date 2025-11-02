"use client";

import React from 'react';
import { AIAssistantProvider, useAIAssistantContext } from '../AIAssistantProvider';

// Example: Integration with existing Client Portal layout
export function ClientPortalWithAI({ children }: { children: React.ReactNode }) {
  // This would typically come from your auth context or user store
  const userContext = {
    userId: "user_123",
    tenantId: "tenant_456",
    userProfile: {
      id: "user_123",
      name: "John Doe",
      email: "john@example.com",
      role: "admin",
      subscription: {
        plan: "pro",
        status: "active",
        features: ["advanced_analytics", "api_access", "priority_support"]
      },
      preferences: {
        language: "en",
        timezone: "UTC",
        notifications: true
      }
    }
  };

  return (
    <AIAssistantProvider
      userContext={userContext}
      config={{
        apiEndpoint: process.env.NEXT_PUBLIC_AI_API_ENDPOINT || 'http://localhost:8001/ai',
        websocketUrl: process.env.NEXT_PUBLIC_AI_WS_URL || 'ws://localhost:8001/ai/ws',
        enableVoiceInput: true,
        enableFileUpload: true
      }}
    >
      {children}
    </AIAssistantProvider>
  );
}

// Example: Custom trigger button in navigation
export function NavigationWithAITrigger() {
  const { openAssistant, isOpen } = useAIAssistantContext();

  return (
    <nav className="flex items-center justify-between p-4 border-b">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-semibold">Client Portal</h1>
        {/* Other navigation items */}
      </div>
      
      <div className="flex items-center gap-4">
        {/* Other nav buttons */}
        <button
          onClick={openAssistant}
          className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
            isOpen 
              ? 'bg-primary text-primary-foreground' 
              : 'bg-muted hover:bg-muted/80'
          }`}
        >
          🤖 AI Assistant
        </button>
      </div>
    </nav>
  );
}

// Example: Dashboard with contextual AI help
export function DashboardWithContextualAI() {
  const { openAssistant, sendMessage } = useAIAssistantContext();

  const handleQuickHelp = (topic: string) => {
    openAssistant();
    // Send a contextual message based on current page
    setTimeout(() => {
      sendMessage(`I need help with ${topic} on my dashboard`);
    }, 500);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Dashboard</h2>
        
        {/* Quick help buttons */}
        <div className="flex gap-2">
          <button
            onClick={() => handleQuickHelp('analytics')}
            className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200"
          >
            📊 Analytics Help
          </button>
          <button
            onClick={() => handleQuickHelp('account settings')}
            className="px-3 py-1 text-xs bg-green-100 text-green-700 rounded-full hover:bg-green-200"
          >
            ⚙️ Account Help
          </button>
        </div>
      </div>

      {/* Dashboard content */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Analytics Cards */}
        <div className="p-4 border rounded-lg">
          <h3 className="font-semibold mb-2">Monthly Revenue</h3>
          <p className="text-2xl font-bold text-green-600">$12,450</p>
          <button
            onClick={() => handleQuickHelp('revenue analytics and trends')}
            className="mt-2 text-xs text-muted-foreground hover:text-primary"
          >
            📈 Explain this metric
          </button>
        </div>

        <div className="p-4 border rounded-lg">
          <h3 className="font-semibold mb-2">Active Campaigns</h3>
          <p className="text-2xl font-bold text-blue-600">8</p>
          <button
            onClick={() => handleQuickHelp('campaign performance optimization')}
            className="mt-2 text-xs text-muted-foreground hover:text-primary"
          >
            🎯 Optimize campaigns
          </button>
        </div>

        <div className="p-4 border rounded-lg">
          <h3 className="font-semibold mb-2">Conversion Rate</h3>
          <p className="text-2xl font-bold text-purple-600">3.2%</p>
          <button
            onClick={() => handleQuickHelp('improving conversion rates')}
            className="mt-2 text-xs text-muted-foreground hover:text-primary"
          >
            📈 Improve conversions
          </button>
        </div>
      </div>

      {/* Recent Activity with AI insights */}
      <div className="border rounded-lg p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold">Recent Activity</h3>
          <button
            onClick={() => handleQuickHelp('understanding my recent activity and what actions I should take')}
            className="text-sm text-primary hover:underline"
          >
            🤔 What should I focus on?
          </button>
        </div>
        
        <div className="space-y-2">
          <div className="flex items-center justify-between p-2 bg-muted rounded">
            <span className="text-sm">New lead from Google Ads campaign</span>
            <span className="text-xs text-muted-foreground">2 hours ago</span>
          </div>
          <div className="flex items-center justify-between p-2 bg-muted rounded">
            <span className="text-sm">Email campaign completed - 23% open rate</span>
            <span className="text-xs text-muted-foreground">5 hours ago</span>
          </div>
          <div className="flex items-center justify-between p-2 bg-muted rounded">
            <span className="text-sm">Integration with CRM updated</span>
            <span className="text-xs text-muted-foreground">1 day ago</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// Example: Settings page with AI guidance
export function SettingsWithAIGuidance() {
  const { openAssistant, sendMessage } = useAIAssistantContext();

  const handleConfigurationHelp = (setting: string) => {
    openAssistant();
    setTimeout(() => {
      sendMessage(`I need help configuring ${setting}. Can you guide me through the best practices and setup?`);
    }, 500);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Account Settings</h2>
        <button
          onClick={() => {
            openAssistant();
            setTimeout(() => {
              sendMessage("I'm in my account settings. Can you help me optimize my configuration for better performance?");
            }, 500);
          }}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
        >
          🚀 Optimize Settings
        </button>
      </div>

      <div className="space-y-6">
        {/* API Configuration */}
        <div className="border rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">API Configuration</h3>
            <button
              onClick={() => handleConfigurationHelp('API keys and rate limits')}
              className="text-sm text-primary hover:underline"
            >
              ❓ Need help?
            </button>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">API Key</label>
              <input
                type="password"
                className="w-full p-2 border rounded-md"
                placeholder="sk-..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Rate Limit</label>
              <select className="w-full p-2 border rounded-md">
                <option>1000 requests/hour</option>
                <option>5000 requests/hour</option>
                <option>10000 requests/hour</option>
              </select>
            </div>
          </div>
        </div>

        {/* Notification Settings */}
        <div className="border rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">Notifications</h3>
            <button
              onClick={() => handleConfigurationHelp('notification preferences and best practices')}
              className="text-sm text-primary hover:underline"
            >
              ❓ Optimize notifications
            </button>
          </div>
          
          <div className="space-y-3">
            <label className="flex items-center gap-2">
              <input type="checkbox" defaultChecked />
              <span className="text-sm">Email notifications for new leads</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" defaultChecked />
              <span className="text-sm">SMS alerts for urgent issues</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" />
              <span className="text-sm">Weekly performance reports</span>
            </label>
          </div>
        </div>

        {/* Integration Settings */}
        <div className="border rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">Integrations</h3>
            <button
              onClick={() => handleConfigurationHelp('third-party integrations and troubleshooting connection issues')}
              className="text-sm text-primary hover:underline"
            >
              🔗 Integration help
            </button>
          </div>
          
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 border rounded-md">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  📧
                </div>
                <div>
                  <p className="font-medium">Email Marketing</p>
                  <p className="text-sm text-muted-foreground">Connected</p>
                </div>
              </div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            </div>
            
            <div className="flex items-center justify-between p-3 border rounded-md">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                  📊
                </div>
                <div>
                  <p className="font-medium">Analytics Platform</p>
                  <p className="text-sm text-muted-foreground">Connection error</p>
                </div>
              </div>
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Example: Error boundary with AI assistance
export function ErrorBoundaryWithAI({ 
  error, 
  reset 
}: { 
  error: Error; 
  reset: () => void; 
}) {
  const { openAssistant, sendMessage } = useAIAssistantContext();

  const handleGetHelp = () => {
    openAssistant();
    setTimeout(() => {
      sendMessage(`I encountered an error: "${error.message}". Can you help me understand what went wrong and how to fix it?`);
    }, 500);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] p-8 text-center">
      <div className="max-w-md">
        <h2 className="text-2xl font-bold text-red-600 mb-4">Something went wrong</h2>
        <p className="text-muted-foreground mb-6">
          We encountered an unexpected error. Our AI assistant can help you troubleshoot this issue.
        </p>
        
        <div className="flex flex-col gap-3">
          <button
            onClick={reset}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
          >
            Try Again
          </button>
          
          <button
            onClick={handleGetHelp}
            className="px-4 py-2 border border-primary text-primary rounded-md hover:bg-primary/10"
          >
            🤖 Get AI Help
          </button>
        </div>
        
        <details className="mt-6 text-left">
          <summary className="cursor-pointer text-sm text-muted-foreground hover:text-foreground">
            Technical Details
          </summary>
          <pre className="mt-2 p-3 bg-muted rounded text-xs overflow-auto">
            {error.message}
            {error.stack && `\n\n${error.stack}`}
          </pre>
        </details>
      </div>
    </div>
  );
}