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
  ShoppingCart,
  FileText,
  BarChart3,
  CheckCircle
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { cn } from '@/lib/utils';
import { chatAPI, type ChatMessage, type ChatContext, type ChatResponse } from '@/lib/chat-api';

interface Message extends ChatMessage {
  id: string;
  suggestions?: string[];
  quickActions?: Array<{
    label: string;
    action: string;
    icon: React.ReactNode;
  }>;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI Assistant. I can help you with various tasks like managing leads, creating content, analyzing your business data, and navigating the platform. What would you like to do today?',
      timestamp: new Date(),
      quickActions: [
        { label: 'Show my leads', action: 'navigate:/leads', icon: <Users className="w-4 h-4" /> },
        { label: 'Create new content', action: 'navigate:/content?action=new', icon: <FileText className="w-4 h-4" /> },
        { label: 'View analytics', action: 'navigate:/analytics', icon: <BarChart3 className="w-4 h-4" /> },
        { label: 'Check orders', action: 'navigate:/orders', icon: <ShoppingCart className="w-4 h-4" /> }
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

  // Mock context - in real app, get from auth/session
  const context: ChatContext = {
    userId: 'current-user',
    tenantId: 'current-tenant',
    currentPage: '/chat',
    userProfile: { name: 'Admin User', email: 'admin@bizosaas.com' }
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

      // Create assistant message with operation results if available
      let content = apiResponse.message || 'I apologize, but I encountered an issue processing your request. Please try again.';
      
      // If operation was performed, include results in the message
      if (apiResponse.operation?.results) {
        const results = apiResponse.operation.results;
        if (results.leads) {
          content += `\n\n📊 **Lead Summary:**\n${results.total} leads found. Recent leads:\n${results.leads.slice(0, 3).map(lead => `• ${lead.name} (${lead.company}) - ${lead.status}`).join('\n')}`;
        }
        if (results.metrics) {
          const m = results.metrics;
          content += `\n\n📈 **Business Metrics:**\n• Leads: ${m.leads?.total} total (${m.leads?.conversion_rate}% conversion)\n• Revenue: $${m.sales?.revenue?.toLocaleString()} from ${m.sales?.orders} orders\n• Content: ${m.content?.views?.toLocaleString()} views, ${m.content?.engagement} avg engagement`;
        }
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content,
        timestamp: new Date(),
        suggestions: apiResponse.suggestions,
        quickActions: apiResponse.quickActions?.map(action => ({
          ...action,
          icon: getIconForAction(action.label)
        }))
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      // Update conversation ID if provided
      if (apiResponse.conversationId) {
        setConversationId(apiResponse.conversationId);
      }

      // Handle operation completion notifications
      if (apiResponse.operationCompleted) {
        console.log('AI Operation completed:', apiResponse.operation);
        // Could show a success notification here
      }

      // Handle confirmation requests
      if (apiResponse.needsConfirmation) {
        // The confirmation message will be in the next AI response
        console.log('Confirmation needed:', apiResponse.confirmationMessage);
      }

    } catch (error) {
      console.error('AI Assistant API error:', error);
      
      // Fallback to mock response only if API completely fails
      const mockResponse = generateMockResponse(message.trim());
      setMessages(prev => [...prev, mockResponse]);
    } finally {
      setIsTyping(false);
    }
  };

  // Generate mock AI response with CRUD operations for demo
  const generateMockResponse = (userMessage: string): Message => {
    const lowerMessage = userMessage.toLowerCase();
    
    let response = "I understand you're asking about: \"" + userMessage + "\". ";
    let quickActions: Message['quickActions'] = [];

    // CRUD Operations for Leads
    if (lowerMessage.includes('lead') || lowerMessage.includes('contact')) {
      if (lowerMessage.includes('create') || lowerMessage.includes('add') || lowerMessage.includes('new')) {
        response += "I'll help you create a new lead. You can add lead details, contact information, and set follow-up reminders.";
        quickActions = [
          { label: 'Create New Lead', action: 'crud:lead:create', icon: <Users className="w-4 h-4" /> },
          { label: 'View All Leads', action: 'navigate:/leads', icon: <Users className="w-4 h-4" /> }
        ];
      } else if (lowerMessage.includes('update') || lowerMessage.includes('edit') || lowerMessage.includes('modify')) {
        response += "I can help you update existing lead information. You currently have 247 leads. Which lead would you like to update?";
        quickActions = [
          { label: 'Update Lead', action: 'crud:lead:update', icon: <Users className="w-4 h-4" /> },
          { label: 'Search Leads', action: 'crud:lead:search', icon: <Users className="w-4 h-4" /> }
        ];
      } else if (lowerMessage.includes('delete') || lowerMessage.includes('remove')) {
        response += "I can help you remove leads. Please note this action is permanent. Which lead would you like to delete?";
        quickActions = [
          { label: 'Delete Lead', action: 'crud:lead:delete', icon: <Users className="w-4 h-4" /> },
          { label: 'View All Leads', action: 'navigate:/leads', icon: <Users className="w-4 h-4" /> }
        ];
      } else {
        response += "I can help you manage your leads (247 total, 3.2% conversion). You can create, view, update, or delete leads.";
        quickActions = [
          { label: 'Create Lead', action: 'crud:lead:create', icon: <Users className="w-4 h-4" /> },
          { label: 'View Leads', action: 'navigate:/leads', icon: <Users className="w-4 h-4" /> },
          { label: 'Update Lead', action: 'crud:lead:update', icon: <Users className="w-4 h-4" /> }
        ];
      }
    }
    // CRUD Operations for Content
    else if (lowerMessage.includes('content') || lowerMessage.includes('blog') || lowerMessage.includes('post') || lowerMessage.includes('page')) {
      if (lowerMessage.includes('create') || lowerMessage.includes('add') || lowerMessage.includes('new') || lowerMessage.includes('write')) {
        response += "I'll help you create new content. You can create blog posts, pages, or marketing materials with AI assistance.";
        quickActions = [
          { label: 'Create Blog Post', action: 'crud:content:create:blog', icon: <FileText className="w-4 h-4" /> },
          { label: 'Create Page', action: 'crud:content:create:page', icon: <FileText className="w-4 h-4" /> },
          { label: 'AI Content Generator', action: 'crud:content:ai-generate', icon: <Zap className="w-4 h-4" /> }
        ];
      } else if (lowerMessage.includes('update') || lowerMessage.includes('edit') || lowerMessage.includes('modify')) {
        response += "I can help you edit existing content. You have 8 published blog posts and 12 pages. Which content would you like to update?";
        quickActions = [
          { label: 'Edit Content', action: 'crud:content:update', icon: <FileText className="w-4 h-4" /> },
          { label: 'Content Library', action: 'navigate:/content', icon: <FileText className="w-4 h-4" /> }
        ];
      } else if (lowerMessage.includes('delete') || lowerMessage.includes('remove')) {
        response += "I can help you delete content. This will remove it from your website. Which content would you like to delete?";
        quickActions = [
          { label: 'Delete Content', action: 'crud:content:delete', icon: <FileText className="w-4 h-4" /> },
          { label: 'Content Library', action: 'navigate:/content', icon: <FileText className="w-4 h-4" /> }
        ];
      } else {
        response += "I can help you manage content (8 blog posts, 12 pages). You can create, edit, or delete content with AI assistance.";
        quickActions = [
          { label: 'Create Content', action: 'crud:content:create:blog', icon: <FileText className="w-4 h-4" /> },
          { label: 'Edit Content', action: 'crud:content:update', icon: <FileText className="w-4 h-4" /> },
          { label: 'AI Content Ideas', action: 'crud:content:ai-ideas', icon: <Zap className="w-4 h-4" /> }
        ];
      }
    }
    // CRUD Operations for Orders
    else if (lowerMessage.includes('order') || lowerMessage.includes('sale') || lowerMessage.includes('purchase')) {
      if (lowerMessage.includes('create') || lowerMessage.includes('add') || lowerMessage.includes('new')) {
        response += "I'll help you create a new order. You can add products, customer details, and payment information.";
        quickActions = [
          { label: 'Create Order', action: 'crud:order:create', icon: <ShoppingCart className="w-4 h-4" /> },
          { label: 'Add Customer', action: 'crud:customer:create', icon: <Users className="w-4 h-4" /> }
        ];
      } else if (lowerMessage.includes('update') || lowerMessage.includes('edit') || lowerMessage.includes('modify')) {
        response += "I can help you update order details, status, or shipping information. Which order would you like to update?";
        quickActions = [
          { label: 'Update Order', action: 'crud:order:update', icon: <ShoppingCart className="w-4 h-4" /> },
          { label: 'Order Status', action: 'crud:order:status', icon: <CheckCircle className="w-4 h-4" /> }
        ];
      } else {
        response += "You have 23 active orders ($31,200 revenue). I can help you create, view, update, or manage orders.";
        quickActions = [
          { label: 'View Orders', action: 'navigate:/orders', icon: <ShoppingCart className="w-4 h-4" /> },
          { label: 'Create Order', action: 'crud:order:create', icon: <ShoppingCart className="w-4 h-4" /> },
          { label: 'Order Analytics', action: 'navigate:/analytics/sales', icon: <TrendingUp className="w-4 h-4" /> }
        ];
      }
    }
    // Analytics and Reports
    else if (lowerMessage.includes('analytic') || lowerMessage.includes('report') || lowerMessage.includes('metric')) {
      response += "Your analytics: 12,500 content views, 247 leads, $31,200 revenue. I can generate custom reports and insights.";
      quickActions = [
        { label: 'View Analytics', action: 'navigate:/analytics', icon: <BarChart3 className="w-4 h-4" /> },
        { label: 'Generate Report', action: 'crud:report:generate', icon: <FileText className="w-4 h-4" /> },
        { label: 'AI Insights', action: 'crud:analytics:ai-insights', icon: <Zap className="w-4 h-4" /> }
      ];
    }
    // General CRUD Help
    else {
      response += "I can help you with comprehensive business management: create, view, update, and delete leads, content, orders, and more. What would you like to work on?";
      quickActions = [
        { label: 'Create Lead', action: 'crud:lead:create', icon: <Users className="w-4 h-4" /> },
        { label: 'Create Content', action: 'crud:content:create:blog', icon: <FileText className="w-4 h-4" /> },
        { label: 'Create Order', action: 'crud:order:create', icon: <ShoppingCart className="w-4 h-4" /> },
        { label: 'Dashboard', action: 'navigate:/', icon: <BarChart3 className="w-4 h-4" /> }
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

  // Get icon for action label
  const getIconForAction = (label: string): React.ReactNode => {
    const lowerLabel = label.toLowerCase();
    if (lowerLabel.includes('lead')) return <Users className="w-4 h-4" />;
    if (lowerLabel.includes('order')) return <ShoppingCart className="w-4 h-4" />;
    if (lowerLabel.includes('content') || lowerLabel.includes('blog')) return <FileText className="w-4 h-4" />;
    if (lowerLabel.includes('analytic') || lowerLabel.includes('insight')) return <BarChart3 className="w-4 h-4" />;
    if (lowerLabel.includes('dashboard')) return <TrendingUp className="w-4 h-4" />;
    return <Zap className="w-4 h-4" />;
  };

  // Handle quick actions including CRUD operations
  const handleQuickAction = (action: string) => {
    if (action.startsWith('navigate:')) {
      const path = action.replace('navigate:', '');
      window.location.href = path;
    } else if (action.startsWith('crud:')) {
      // Handle CRUD operations via conversational interface
      const crudAction = action.replace('crud:', '');
      const [entity, operation, type] = crudAction.split(':');
      
      let crudMessage = '';
      
      switch (operation) {
        case 'create':
          if (type) {
            crudMessage = `I want to create a new ${type} ${entity}. Please guide me through the process.`;
          } else {
            crudMessage = `I want to create a new ${entity}. Please guide me through the process.`;
          }
          break;
        case 'update':
          crudMessage = `I want to update an existing ${entity}. Please show me the options.`;
          break;
        case 'delete':
          crudMessage = `I want to delete a ${entity}. Please show me the list to choose from.`;
          break;
        case 'search':
          crudMessage = `Please help me search and find specific ${entity} records.`;
          break;
        case 'generate':
          crudMessage = `Please generate a new ${entity} for me.`;
          break;
        case 'ai-generate':
          crudMessage = `Please use AI to generate ${entity} content for me.`;
          break;
        case 'ai-insights':
          crudMessage = `Please provide AI insights for my ${entity} data.`;
          break;
        case 'ai-ideas':
          crudMessage = `Please give me AI-powered ideas for ${entity}.`;
          break;
        case 'status':
          crudMessage = `Please show me the status of ${entity} records.`;
          break;
        default:
          crudMessage = `I want to work with ${entity} records. Please help me.`;
      }
      
      sendMessage(crudMessage);
    } else if (action.startsWith('execute:')) {
      const command = action.replace('execute:', '');
      sendMessage(`Execute: ${command}`);
    }
  };

  // Clear conversation
  const clearConversation = () => {
    setMessages([{
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI Assistant. I can help you with various tasks like managing leads, creating content, analyzing your business data, and navigating the platform. What would you like to do today?',
      timestamp: new Date(),
      quickActions: [
        { label: 'Show my leads', action: 'navigate:/leads', icon: <Users className="w-4 h-4" /> },
        { label: 'Create new content', action: 'navigate:/content?action=new', icon: <FileText className="w-4 h-4" /> },
        { label: 'View analytics', action: 'navigate:/analytics', icon: <BarChart3 className="w-4 h-4" /> },
        { label: 'Check orders', action: 'navigate:/orders', icon: <ShoppingCart className="w-4 h-4" /> }
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
      sendMessage(`I've uploaded these files: ${fileNames}. How can you help me with them?`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <MessageSquare className="w-8 h-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-gray-900">AI Assistant</h1>
        </div>
        <p className="text-gray-600">Get intelligent help with platform management and admin tasks</p>
      </div>

      <div className="bg-white rounded-lg shadow h-[calc(100vh-200px)] flex flex-col">
        {/* Chat Header - Sticky */}
        <div className="sticky top-0 z-10 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="font-semibold text-gray-900 dark:text-white">AI Assistant</h2>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {isTyping ? 'AI is typing...' : 'Online and ready to help'}
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="text-xs">
                <CheckCircle className="w-3 h-3 mr-1" />
                Connected
              </Badge>
              <Button
                variant="outline"
                size="sm"
                onClick={clearConversation}
                className="h-8"
              >
                <Trash2 className="w-4 h-4 mr-1" />
                Clear
              </Button>
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 min-h-0">
          <div className="h-full overflow-y-auto scroll-smooth scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100 hover:scrollbar-thumb-gray-400 p-6">
            <div className="max-w-4xl mx-auto space-y-6">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={cn(
                    "flex gap-4",
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  )}
                >
                  {message.role === 'assistant' && (
                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                  )}
                  
                  <div className={cn(
                    "max-w-2xl",
                    message.role === 'user' ? 'flex flex-col items-end' : 'flex flex-col items-start'
                  )}>
                    <Card className={cn(
                      "shadow-sm",
                      message.role === 'user' 
                        ? 'bg-blue-600 text-white border-blue-600' 
                        : 'bg-white dark:bg-gray-800'
                    )}>
                      <CardContent className="p-4">
                        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                      </CardContent>
                    </Card>
                    
                    <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {message.timestamp.toLocaleTimeString()}
                    </div>

                    {/* Quick Actions */}
                    {message.quickActions && message.quickActions.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-3">
                        {message.quickActions.map((action, index) => (
                          <Button
                            key={index}
                            variant="outline"
                            size="sm"
                            onClick={() => handleQuickAction(action.action)}
                            className="h-8 text-xs"
                          >
                            {action.icon}
                            <span className="ml-1">{action.label}</span>
                          </Button>
                        ))}
                      </div>
                    )}
                  </div>
                  
                  {message.role === 'user' && (
                    <div className="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <User className="w-4 h-4 text-white" />
                    </div>
                  )}
                </div>
              ))}

              {/* Typing Indicator */}
              {isTyping && (
                <div className="flex gap-4">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <Card className="bg-white dark:bg-gray-800 shadow-sm">
                    <CardContent className="p-4">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          </div>
        </div>

        {/* Input Area */}
        <div className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 p-6">
          <div className="max-w-4xl mx-auto">
            <div className="relative">
              <Textarea
                ref={inputRef}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask me anything about your account, analytics, or platform features..."
                className="min-h-[80px] pr-32 resize-none"
                disabled={isTyping}
              />
              
              <div className="absolute bottom-3 right-3 flex items-center gap-2">
                {/* File Upload */}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => fileInputRef.current?.click()}
                  className="h-8 w-8 p-0"
                  title="Upload file"
                >
                  <Paperclip className="w-4 h-4" />
                </Button>
                
                {/* Voice Input */}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsVoiceRecording(!isVoiceRecording)}
                  className={cn(
                    "h-8 w-8 p-0",
                    isVoiceRecording && "bg-red-100 text-red-600"
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
                  className="h-8"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
            
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
              Press Enter to send, Shift+Enter for new line
            </p>
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
    </DashboardLayout>
  );
}