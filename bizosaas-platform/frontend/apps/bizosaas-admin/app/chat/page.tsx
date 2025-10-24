'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { 
  MessageSquare, 
  Send, 
  Trash2, 
  Bot, 
  User,
  Mic,
  MicOff,
  Paperclip,
  RefreshCw,
  Zap,
  TrendingUp,
  Users,
  Building2,
  Activity,
  DollarSign,
  Database,
  Shield,
  AlertCircle,
  CheckCircle,
  Settings,
  Workflow
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { cn } from '@/lib/utils';
import { adminChatAPI, type AdminChatMessage, type AdminChatContext, type AdminChatResponse } from '../../lib/admin-chat-api';

interface Message extends AdminChatMessage {
  id: string;
  suggestions?: string[];
  quickActions?: Array<{
    label: string;
    action: string;
    icon: React.ReactNode;
  }>;
}

export default function AdminChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI Administrator Assistant. I can help you manage the platform, monitor system health, analyze tenant metrics, manage users, and execute administrative tasks. What would you like to do today?',
      timestamp: new Date(),
      quickActions: [
        { label: 'Platform Health', action: 'navigate:/system-health', icon: <Activity className="w-4 h-4" /> },
        { label: 'Tenant Management', action: 'navigate:/tenants', icon: <Building2 className="w-4 h-4" /> },
        { label: 'User Analytics', action: 'navigate:/users', icon: <Users className="w-4 h-4" /> },
        { label: 'Revenue Report', action: 'navigate:/revenue', icon: <DollarSign className="w-4 h-4" /> },
        { label: 'AI Agents Monitor', action: 'navigate:/ai-agents', icon: <Workflow className="w-4 h-4" /> },
        { label: 'Security Audit', action: 'navigate:/security', icon: <Shield className="w-4 h-4" /> }
      ]
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isVoiceRecording, setIsVoiceRecording] = useState(false);
  const [conversationId, setConversationId] = useState<string>('');
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Mock admin context - in real app, get from auth/session
  const context: AdminChatContext = {
    userId: 'super-admin',
    tenantId: 'platform',
    currentPage: '/chat',
    userProfile: { name: 'Super Admin', email: 'admin@bizosaas.com' },
    adminLevel: 'super'
  };

  // Auto-scroll to bottom
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Handle sending messages
  const sendMessage = async (message: string) => {
    if (!message.trim() || isTyping) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: message.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    try {
      // Use the intelligent AI assistant API
      const response = await fetch('/api/ai-assistant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          context: {
            ...context,
            conversationId,
            previousMessages: messages.slice(-5).map(m => ({
              role: m.role,
              content: m.content,
              timestamp: m.timestamp
            }))
          }
        })
      });

      if (!response.ok) {
        throw new Error(`AI Assistant API error: ${response.status}`);
      }

      const apiResponse = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: apiResponse.message || 'I apologize, but I encountered an issue processing your request. Please try again.',
        timestamp: new Date(),
        suggestions: apiResponse.suggestions,
        quickActions: apiResponse.quickActions?.map((action: any) => ({
          ...action,
          icon: getIconForAdminAction(action.label)
        }))
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      // Update conversation ID if provided
      if (apiResponse.conversationId) {
        setConversationId(apiResponse.conversationId);
      }

      // Handle operation results if any
      if (apiResponse.operation) {
        console.log('AI Operation executed:', apiResponse.operation);
        // You can handle specific operations here (e.g., show results, update UI)
      }

    } catch (error) {
      console.error('AI Assistant API error:', error);
      
      // Fallback to mock response only if API completely fails
      const mockResponse = generateMockAdminResponse(message.trim());
      setMessages(prev => [...prev, mockResponse]);
    } finally {
      setIsTyping(false);
    }
  };

  // Generate mock admin AI response for demo
  const generateMockAdminResponse = (userMessage: string): Message => {
    const lowerMessage = userMessage.toLowerCase();
    
    let response = "As your platform administrator, I'll help you with: \"" + userMessage + "\". ";
    let quickActions: Message['quickActions'] = [];

    if (lowerMessage.includes('tenant') || lowerMessage.includes('organization')) {
      response += "Currently managing 47 active tenants across the platform. Revenue is $125,400/month with 98.2% uptime. Top tenants: TechCorp, Bizoholic, StartupXYZ.";
      quickActions = [
        { label: 'Tenant Dashboard', action: 'navigate:/tenants', icon: <Building2 className="w-4 h-4" /> },
        { label: 'Revenue Analytics', action: 'navigate:/revenue', icon: <DollarSign className="w-4 h-4" /> }
      ];
    } else if (lowerMessage.includes('user') || lowerMessage.includes('account')) {
      response += "Platform has 1,247 active users across all tenants. 34 new signups this week. User activity is 15% above average.";
      quickActions = [
        { label: 'User Management', action: 'navigate:/users', icon: <Users className="w-4 h-4" /> },
        { label: 'Activity Analytics', action: 'navigate:/api-analytics', icon: <Activity className="w-4 h-4" /> }
      ];
    } else if (lowerMessage.includes('health') || lowerMessage.includes('system') || lowerMessage.includes('status')) {
      response += "System health is optimal: All services running (Brain Hub: ✅, CRM: ✅, CMS: ✅, E-commerce: ✅). CPU: 23%, Memory: 67%, Disk: 45%.";
      quickActions = [
        { label: 'System Health', action: 'navigate:/system-health', icon: <Activity className="w-4 h-4" /> },
        { label: 'Infrastructure', action: 'navigate:/integrations', icon: <Database className="w-4 h-4" /> }
      ];
    } else if (lowerMessage.includes('ai') || lowerMessage.includes('agent') || lowerMessage.includes('workflow')) {
      response += "AI Agents processed 2,847 tasks today with 96% success rate. Most active: Marketing Automation (847 runs), CRM Sync (623 runs), Analytics (445 runs).";
      quickActions = [
        { label: 'AI Agents Monitor', action: 'navigate:/ai-agents', icon: <Workflow className="w-4 h-4" /> },
        { label: 'Workflow Management', action: 'navigate:/workflows', icon: <Zap className="w-4 h-4" /> }
      ];
    } else if (lowerMessage.includes('security') || lowerMessage.includes('audit') || lowerMessage.includes('log')) {
      response += "Security status: 12 login attempts blocked today, SSL certificates valid, no suspicious activity detected. Last security audit: 3 days ago.";
      quickActions = [
        { label: 'Security Dashboard', action: 'navigate:/security', icon: <Shield className="w-4 h-4" /> },
        { label: 'Audit Logs', action: 'navigate:/security#audit', icon: <AlertCircle className="w-4 h-4" /> }
      ];
    } else if (lowerMessage.includes('revenue') || lowerMessage.includes('billing') || lowerMessage.includes('subscription')) {
      response += "Platform revenue: $125,400/month (+8.3% vs last month). Active subscriptions: 47 tenants. Churn rate: 2.1%. Top plan: Business Pro (67% of revenue).";
      quickActions = [
        { label: 'Revenue Analytics', action: 'navigate:/revenue', icon: <DollarSign className="w-4 h-4" /> },
        { label: 'Subscription Management', action: 'navigate:/tenants#billing', icon: <TrendingUp className="w-4 h-4" /> }
      ];
    } else {
      response += "I can help you with platform administration including: tenant management, user oversight, system monitoring, AI agent supervision, security auditing, and revenue analysis.";
      quickActions = [
        { label: 'Dashboard Overview', action: 'navigate:/', icon: <Activity className="w-4 h-4" /> },
        { label: 'Platform Health', action: 'navigate:/system-health', icon: <CheckCircle className="w-4 h-4" /> },
        { label: 'Tenant Management', action: 'navigate:/tenants', icon: <Building2 className="w-4 h-4" /> },
        { label: 'Security Center', action: 'navigate:/security', icon: <Shield className="w-4 h-4" /> }
      ];
    }

    return {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: response,
      timestamp: new Date(),
      quickActions
    };
  };

  // Get icon for admin action label
  const getIconForAdminAction = (label: string): React.ReactNode => {
    const lowerLabel = label.toLowerCase();
    if (lowerLabel.includes('tenant') || lowerLabel.includes('organization')) return <Building2 className="w-4 h-4" />;
    if (lowerLabel.includes('user') || lowerLabel.includes('account')) return <Users className="w-4 h-4" />;
    if (lowerLabel.includes('health') || lowerLabel.includes('system')) return <Activity className="w-4 h-4" />;
    if (lowerLabel.includes('revenue') || lowerLabel.includes('billing')) return <DollarSign className="w-4 h-4" />;
    if (lowerLabel.includes('security') || lowerLabel.includes('audit')) return <Shield className="w-4 h-4" />;
    if (lowerLabel.includes('ai') || lowerLabel.includes('agent') || lowerLabel.includes('workflow')) return <Workflow className="w-4 h-4" />;
    if (lowerLabel.includes('database') || lowerLabel.includes('infrastructure')) return <Database className="w-4 h-4" />;
    if (lowerLabel.includes('dashboard') || lowerLabel.includes('overview')) return <TrendingUp className="w-4 h-4" />;
    return <Settings className="w-4 h-4" />;
  };

  // Handle quick actions
  const handleQuickAction = (action: string) => {
    if (action.startsWith('navigate:')) {
      const path = action.replace('navigate:', '');
      window.location.href = path;
    } else if (action.startsWith('execute:')) {
      const command = action.replace('execute:', '');
      sendMessage(`Execute admin command: ${command}`);
    }
  };

  // Clear conversation
  const clearConversation = () => {
    setMessages([{
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI Administrator Assistant. I can help you manage the platform, monitor system health, analyze tenant metrics, manage users, and execute administrative tasks. What would you like to do today?',
      timestamp: new Date(),
      quickActions: [
        { label: 'Platform Health', action: 'navigate:/system-health', icon: <Activity className="w-4 h-4" /> },
        { label: 'Tenant Management', action: 'navigate:/tenants', icon: <Building2 className="w-4 h-4" /> },
        { label: 'User Analytics', action: 'navigate:/users', icon: <Users className="w-4 h-4" /> },
        { label: 'Revenue Report', action: 'navigate:/revenue', icon: <DollarSign className="w-4 h-4" /> },
        { label: 'AI Agents Monitor', action: 'navigate:/ai-agents', icon: <Workflow className="w-4 h-4" /> },
        { label: 'Security Audit', action: 'navigate:/security', icon: <Shield className="w-4 h-4" /> }
      ]
    }]);
    setConversationId('');
  };

  // Handle keyboard shortcuts
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(inputText);
    }
  };

  // Handle file upload (mock)
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const fileNames = Array.from(files).map(f => f.name).join(', ');
      sendMessage(`I've uploaded these admin files: ${fileNames}. Please help me analyze them.`);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Chat Header - Sticky */}
      <div className="sticky top-0 z-10 bg-white shadow-sm border-b border-gray-200 p-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
              <Bot className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">AI Administrator Assistant</h1>
              <p className="text-gray-600">
                {isTyping ? 'AI is analyzing your request...' : 'Platform management and administrative support'}
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <Badge variant="outline" className="text-sm px-3 py-1">
              <CheckCircle className="w-4 h-4 mr-2 text-green-500" />
              Super Admin Access
            </Badge>
            <Badge variant="default" className="text-sm px-3 py-1">
              <Activity className="w-4 h-4 mr-2" />
              System Online
            </Badge>
            <Button
              variant="outline"
              onClick={clearConversation}
              className="flex items-center gap-2"
            >
              <Trash2 className="w-4 h-4" />
              New Conversation
            </Button>
          </div>
        </div>
      </div>

      {/* Messages Area - Scrollable */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full overflow-y-auto scroll-smooth scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100 hover:scrollbar-thumb-gray-400">
          <div className="max-w-7xl mx-auto p-6 space-y-6 min-h-full">
            {messages.map((message) => (
              <div
                key={message.id}
                className={cn(
                  "flex gap-4",
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                )}
              >
                {message.role === 'assistant' && (
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-white" />
                  </div>
                )}
                
                <div className={cn(
                  "max-w-3xl",
                  message.role === 'user' ? 'flex flex-col items-end' : 'flex flex-col items-start'
                )}>
                  <Card className={cn(
                    "shadow-sm",
                    message.role === 'user' 
                      ? 'bg-blue-600 text-white border-blue-600' 
                      : 'bg-white border-gray-200'
                  )}>
                    <CardContent className="p-4">
                      <p className="text-sm whitespace-pre-wrap leading-relaxed">{message.content}</p>
                    </CardContent>
                  </Card>
                  
                  <div className="text-xs text-gray-500 mt-1">
                    {message.timestamp.toLocaleTimeString()}
                  </div>

                  {/* Quick Actions */}
                  {message.quickActions && message.quickActions.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-3 max-w-3xl">
                      {message.quickActions.map((action, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          size="sm"
                          onClick={() => handleQuickAction(action.action)}
                          className="h-8 text-xs flex items-center gap-2"
                        >
                          {action.icon}
                          <span>{action.label}</span>
                        </Button>
                      ))}
                    </div>
                  )}
                </div>
                
                {message.role === 'user' && (
                  <div className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center flex-shrink-0">
                    <User className="w-5 h-5 text-white" />
                  </div>
                )}
              </div>
            ))}

            {/* Typing Indicator */}
            {isTyping && (
              <div className="flex gap-4">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <Card className="bg-white border-gray-200 shadow-sm">
                  <CardContent className="p-4">
                    <div className="flex gap-2 items-center">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                      </div>
                      <span className="text-sm text-gray-500 ml-2">Processing admin request...</span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>

      {/* Input Area - Sticky Bottom */}
      <div className="sticky bottom-0 z-10 bg-white border-t border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto p-6">
          <div className="relative">
            <Textarea
              ref={inputRef}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about platform health, tenant management, revenue analytics, system administration..."
              className="min-h-[100px] pr-36 resize-none text-base"
              disabled={isTyping}
            />
            
            <div className="absolute bottom-4 right-4 flex items-center gap-2">
              {/* File Upload */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => fileInputRef.current?.click()}
                className="h-9 w-9 p-0"
                title="Upload admin files"
              >
                <Paperclip className="w-4 h-4" />
              </Button>
              
              {/* Voice Input */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsVoiceRecording(!isVoiceRecording)}
                className={cn(
                  "h-9 w-9 p-0",
                  isVoiceRecording && "bg-red-100 text-red-600 hover:bg-red-100"
                )}
                title="Voice input"
              >
                {isVoiceRecording ? (
                  <MicOff className="w-4 h-4" />
                ) : (
                  <Mic className="w-4 h-4" />
                )}
              </Button>
              
              {/* Send Button */}
              <Button
                onClick={() => sendMessage(inputText)}
                disabled={!inputText.trim() || isTyping}
                size="sm"
                className="h-9 px-4 bg-blue-600 hover:bg-blue-700"
              >
                <Send className="w-4 h-4 mr-2" />
                Send
              </Button>
            </div>
          </div>
          
          <div className="flex items-center justify-between mt-3">
            <p className="text-xs text-gray-500">
              Press Enter to send, Shift+Enter for new line
            </p>
            <p className="text-xs text-gray-500">
              Powered by AI • Super Admin Mode • Secure Connection
            </p>
          </div>
        </div>
      </div>

      {/* Hidden File Input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        onChange={handleFileUpload}
        className="hidden"
        accept="*/*"
      />
    </div>
  );
}