'use client';

import React, { useState, useEffect, useRef } from 'react';
import {
  MessageSquare, Send, Minimize2, Maximize2, X, Bot, User,
  Zap, Lightbulb, TrendingUp, Target, ShoppingCart, FileText,
  BarChart3, Settings, Loader, CheckCircle, AlertCircle,
  Copy, ThumbsUp, ThumbsDown, RefreshCw, Mic, MicOff, Globe
} from 'lucide-react';
import { useRouter } from 'next/navigation';

interface Message {
  id: string;
  type: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    suggestions?: string[];
    actions?: Array<{
      label: string;
      action: string;
      data?: any;
    }>;
    context?: any;
    confidence?: number;
  };
  status?: 'sending' | 'sent' | 'error';
}

interface AICapability {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType<any>;
  category: 'analysis' | 'automation' | 'optimization' | 'assistance';
  examples: string[];
}

interface AssistantConfig {
  personality: 'professional' | 'friendly' | 'expert' | 'casual';
  expertise: string[];
  proactiveMode: boolean;
  voiceEnabled: boolean;
  contextAware: boolean;
}

const AI_CAPABILITIES: AICapability[] = [
  {
    id: 'campaign-optimization',
    name: 'Campaign Optimization',
    description: 'Analyze and optimize marketing campaigns for better performance',
    icon: Target,
    category: 'optimization',
    examples: [
      'Optimize my Google Ads campaign',
      'Why is my email open rate low?',
      'Suggest improvements for my social media campaign'
    ]
  },
  {
    id: 'data-analysis',
    name: 'Data Analysis',
    description: 'Analyze business data and provide actionable insights',
    icon: BarChart3,
    category: 'analysis',
    examples: [
      'Analyze my sales performance this quarter',
      'What are my top performing products?',
      'Show me conversion trends'
    ]
  },
  {
    id: 'lead-management',
    name: 'Lead Management',
    description: 'Help manage and nurture leads effectively',
    icon: FileText,
    category: 'automation',
    examples: [
      'Score this lead for me',
      'Create a follow-up sequence',
      'Segment my leads by behavior'
    ]
  },
  {
    id: 'ecommerce-assistance',
    name: 'E-commerce Assistance',
    description: 'Optimize product listings and manage inventory',
    icon: ShoppingCart,
    category: 'assistance',
    examples: [
      'Optimize my product descriptions',
      'Manage inventory alerts',
      'Analyze shopping cart abandonment'
    ]
  },
  {
    id: 'domain-management',
    name: 'Domain & DNS Control',
    description: 'Find, register, and manage your domain names and DNS records',
    icon: Globe,
    category: 'assistance',
    examples: [
      'Search for a new domain name',
      'How do I map my domain to my directory listing?',
      'Check my domain renewal status'
    ]
  }
];

const QUICK_ACTIONS = [
  { label: 'Domain Search', query: 'Search for a new domain name for my brand' },
  { label: 'Directory SEO', query: 'How can I optimize my local directory listing?' },
  { label: 'Campaign Performance', query: 'Show me my campaign performance overview' },
  { label: 'Revenue Report', query: 'Generate a revenue report for this month' }
];

export function AIAssistant() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: "Hi! I'm your AI business assistant. I can help you optimize campaigns, analyze data, manage leads, and much more. What would you like to work on today?",
      timestamp: new Date(),
      metadata: {
        suggestions: [
          'Show campaign performance',
          'Analyze my leads',
          'Optimize my ads',
          'Generate a report'
        ]
      }
    }
  ]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [config, setConfig] = useState<AssistantConfig>({
    personality: 'professional',
    expertise: ['marketing', 'analytics', 'automation'],
    proactiveMode: true,
    voiceEnabled: false,
    contextAware: true
  });
  const [isListening, setIsListening] = useState(false);
  const [showCapabilities, setShowCapabilities] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  useEffect(() => {
    if (isOpen && !isMinimized && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen, isMinimized]);

  // Simulate AI response
  const generateResponse = async (userMessage: string): Promise<Message> => {
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

    const lowerMessage = userMessage.toLowerCase();
    let response = '';
    let suggestions: string[] = [];
    let actions: any[] = [];
    let confidence = 85;

    if (lowerMessage.includes('domain') || lowerMessage.includes('search')) {
      response = `I can help you find and manage your domain portfolio! I've performed a quick search and found some great options for you:

🚀 **Domain Recommendations**
• YourBrand.com - $12.99/yr (Classic)
• YourBrand.ai - $59.99/yr (Trending for AI/Tech)
• LocalYourBrand.net - $9.99/yr (Great for local SEO)

I recommend mapping your domain to the **Business Directory** to immediately gain local SEO authority. Would you like to proceed with a purchase or check specific DNS records?`;

      suggestions = [
        'Search for more domains',
        'Check my existing domains',
        'How to map DNS records',
        'Domain pricing list'
      ];

      actions = [
        { label: 'Go to Portfolio', action: 'view_domains', data: {} },
        { label: 'Map to Directory', action: 'map_domain', data: { target: 'directory' } }
      ];
      confidence = 94;
    } else if (lowerMessage.includes('directory') || lowerMessage.includes('listing')) {
      response = `Your Business Directory listing is current active and optimized! Here's a quick status report:

📊 **Directory Performance**
• Status: 100% Optimized
• Visibility: Local Rank #3 for your primary keyword
• Citations: 42 active high-quality backlinks
• Reviews: 4.8 star average across synced platforms

I recommend adding 3-5 more high-quality photos and updating your service list to improve your "Claim to conversion" ratio.`;

      suggestions = [
        'Optimize my listing further',
        'Manage directory reviews',
        'View directory analytics',
        'Add service photos'
      ];

      actions = [
        { label: 'Manage Listing', action: 'view_directory', data: {} }
      ];
      confidence = 91;
    } else if (lowerMessage.includes('campaign') || lowerMessage.includes('marketing')) {
      response = `I can help you with campaign optimization! Based on your recent campaigns, I see opportunities to improve performance by 15-25%. Here are my key recommendations:

• **Audience Refinement**: Your target audience could be narrowed for better engagement
• **Ad Creative Testing**: Try A/B testing different headlines and visuals  
• **Budget Reallocation**: Shift budget from low-performing ads to high-converters
• **Timing Optimization**: Adjust ad scheduling based on peak engagement hours

Would you like me to implement any of these optimizations or analyze a specific campaign?`;

      suggestions = [
        'Analyze my Google Ads campaign',
        'Optimize my Facebook ads',
        'Create a new campaign',
        'Show me campaign ROI'
      ];

      actions = [
        { label: 'Optimize Campaign', action: 'optimize_campaign', data: { type: 'google_ads' } },
        { label: 'View Analytics', action: 'view_analytics', data: { type: 'campaigns' } }
      ];
      confidence = 92;
    } else if (lowerMessage.includes('lead') || lowerMessage.includes('crm')) {
      response = `Great! I can help with lead management. I've analyzed your recent leads and found some interesting patterns:

• **Lead Quality Score**: Average score of 73/100 (good quality)
• **Top Sources**: Website forms (45%), Social media (28%), Referrals (27%)
• **Conversion Rate**: 12.3% (above industry average of 9.8%)
• **Follow-up Opportunity**: 23 leads haven't been contacted in 48+ hours

I recommend setting up automated nurturing sequences for new leads and prioritizing the high-score leads for immediate follow-up.`;

      suggestions = [
        'Score my recent leads',
        'Set up lead automation',
        'Show lead conversion funnel',
        'Create follow-up templates'
      ];
      confidence = 89;
    } else if (lowerMessage.includes('analytics') || lowerMessage.includes('report') || lowerMessage.includes('performance')) {
      response = `I'll generate a comprehensive performance analysis for you:

📊 **Overall Performance (Last 30 Days)**
• Total Revenue: $47,350 (+18% vs previous month)
• Conversion Rate: 3.2% (+0.4% improvement)
• Customer Acquisition Cost: $32 (-15% optimization)
• Average Order Value: $156 (+8% growth)

🎯 **Top Performing Channels**
1. Google Ads: 35% of conversions, $18/CPA
2. Email Marketing: 28% of conversions, $8/CPA  
3. Social Media: 22% of conversions, $25/CPA

📈 **Key Insights & Recommendations**
• Email marketing shows the best ROI - consider increasing investment
• Mobile conversion rate is 40% lower than desktop - optimize mobile experience
• Cart abandonment rate is 68% - implement recovery sequences`;

      suggestions = [
        'Deep dive into revenue trends',
        'Analyze conversion funnels',
        'Compare channel performance',
        'Export detailed report'
      ];
      confidence = 95;
    } else if (lowerMessage.includes('optimize') || lowerMessage.includes('improve')) {
      response = `I've identified several optimization opportunities across your platform:

🚀 **Immediate Wins (1-2 days)**
• Update ad headlines with higher CTR variations (+12% potential lift)
• Adjust bid strategies on underperforming keywords
• Enable audience expansion on top campaigns

⚡ **Short-term Projects (1-2 weeks)**  
• Implement dynamic remarketing for e-commerce
• Set up advanced attribution modeling
• Create lookalike audiences from best customers

🎯 **Strategic Initiatives (1+ months)**
• Develop omnichannel customer journey mapping
• Implement predictive lead scoring
• Build automated competitive intelligence

Which optimization would you like to tackle first?`;

      actions = [
        { label: 'Start Quick Wins', action: 'implement_optimizations', data: { type: 'immediate' } },
        { label: 'Plan Projects', action: 'create_roadmap', data: { type: 'optimization' } }
      ];
      confidence = 87;
    } else {
      response = `I understand you're looking for help with "${userMessage}". I can assist with:

• **Campaign Management**: Create, optimize, and analyze marketing campaigns
• **Data Analysis**: Generate insights from your business data
• **Lead Management**: Score, nurture, and convert leads effectively
• **E-commerce**: Optimize product listings and manage inventory
• **Automation**: Set up workflows to save time and increase efficiency

What specific area would you like to explore? I'm here to help you grow your business!`;

      suggestions = [
        'Show me what you can do',
        'Help with campaign optimization',
        'Analyze my business data',
        'Set up automation'
      ];
    }

    return {
      id: Date.now().toString(),
      type: 'assistant',
      content: response,
      timestamp: new Date(),
      metadata: {
        suggestions,
        actions,
        confidence
      }
    };
  };

  const sendMessage = async (messageContent?: string) => {
    const content = messageContent || currentMessage.trim();
    if (!content) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content,
      timestamp: new Date(),
      status: 'sent'
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setIsTyping(true);

    try {
      const response = await generateResponse(content);
      setMessages(prev => [...prev, response]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'system',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleAction = (action: string, data?: any) => {
    switch (action) {
      case 'optimize_campaign':
        sendMessage(`Optimize my ${data?.type || 'marketing'} campaign with specific recommendations`);
        break;
      case 'view_analytics':
        sendMessage(`Show me detailed analytics for ${data?.type || 'overall performance'}`);
        break;
      case 'implement_optimizations':
        sendMessage(`Implement ${data?.type || 'all'} optimization recommendations`);
        break;
      case 'create_roadmap':
        sendMessage(`Create a ${data?.type || 'general'} roadmap with timelines and priorities`);
        break;
      case 'view_domains':
        router.push('/dashboard/domains');
        setIsOpen(false);
        break;
      case 'view_directory':
        router.push('/dashboard/directory');
        setIsOpen(false);
        break;
      default:
        console.log('Unknown action:', action);
    }
  };

  const startVoiceRecognition = () => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new (window as any).webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setCurrentMessage(transcript);
      };

      recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognition.start();
    } else {
      alert('Speech recognition not supported in this browser');
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full shadow-lg hover:shadow-xl transition-all flex items-center justify-center z-50"
      >
        <Bot size={24} />
      </button>
    );
  }

  return (
    <div className={`fixed bottom-6 right-6 z-50 transition-all ${isMinimized ? 'w-80 h-14' : 'w-96 h-[32rem]'
      }`}>
      <div className="bg-white rounded-lg shadow-2xl border border-gray-200 flex flex-col h-full">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-t-lg">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
              <Bot size={16} />
            </div>
            <div>
              <h3 className="font-semibold">AI Business Assistant</h3>
              {!isMinimized && (
                <p className="text-xs opacity-90">Ready to help optimize your business</p>
              )}
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowCapabilities(!showCapabilities)}
              className="p-1 hover:bg-white hover:bg-opacity-20 rounded"
              title="Show capabilities"
            >
              <Lightbulb size={16} />
            </button>
            <button
              onClick={() => setIsMinimized(!isMinimized)}
              className="p-1 hover:bg-white hover:bg-opacity-20 rounded"
            >
              {isMinimized ? <Maximize2 size={16} /> : <Minimize2 size={16} />}
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 hover:bg-white hover:bg-opacity-20 rounded"
            >
              <X size={16} />
            </button>
          </div>
        </div>

        {!isMinimized && (
          <>
            {/* Capabilities Panel */}
            {showCapabilities && (
              <div className="p-4 bg-gray-50 border-b border-gray-200 max-h-48 overflow-y-auto">
                <h4 className="font-medium text-gray-900 mb-2">What I can help you with:</h4>
                <div className="grid grid-cols-1 gap-2">
                  {AI_CAPABILITIES.map(capability => {
                    const Icon = capability.icon;
                    return (
                      <div key={capability.id} className="flex items-start space-x-2 p-2 bg-white rounded border">
                        <Icon size={16} className="text-blue-600 mt-1" />
                        <div>
                          <h5 className="text-sm font-medium text-gray-900">{capability.name}</h5>
                          <p className="text-xs text-gray-600">{capability.description}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map(message => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[80%] ${message.type === 'user'
                    ? 'bg-blue-600 text-white rounded-lg rounded-br-sm'
                    : message.type === 'system'
                      ? 'bg-red-100 text-red-800 rounded-lg'
                      : 'bg-gray-100 text-gray-900 rounded-lg rounded-bl-sm'
                    } p-3`}>
                    <div className="whitespace-pre-wrap text-sm">{message.content}</div>

                    {message.metadata?.confidence && (
                      <div className="mt-2 text-xs opacity-75">
                        Confidence: {message.metadata.confidence}%
                      </div>
                    )}

                    {message.metadata?.actions && (
                      <div className="mt-3 space-y-1">
                        {message.metadata.actions.map((action, idx) => (
                          <button
                            key={idx}
                            onClick={() => handleAction(action.action, action.data)}
                            className="block w-full text-left text-xs bg-white bg-opacity-20 hover:bg-opacity-30 px-2 py-1 rounded"
                          >
                            {action.label}
                          </button>
                        ))}
                      </div>
                    )}

                    {message.metadata?.suggestions && (
                      <div className="mt-3 flex flex-wrap gap-1">
                        {message.metadata.suggestions.map((suggestion, idx) => (
                          <button
                            key={idx}
                            onClick={() => sendMessage(suggestion)}
                            className="text-xs bg-white bg-opacity-20 hover:bg-opacity-30 px-2 py-1 rounded"
                          >
                            {suggestion}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg rounded-bl-sm p-3">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Quick Actions */}
            <div className="px-4 py-2 border-t border-gray-200 bg-gray-50">
              <div className="flex flex-wrap gap-1">
                {QUICK_ACTIONS.map((action, idx) => (
                  <button
                    key={idx}
                    onClick={() => sendMessage(action.query)}
                    className="text-xs bg-white border border-gray-200 hover:border-gray-300 px-2 py-1 rounded"
                  >
                    {action.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-200">
              <div className="flex space-x-2">
                <div className="flex-1 relative">
                  <input
                    ref={inputRef}
                    type="text"
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Ask me anything about your business..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                    disabled={isTyping}
                  />
                  {config.voiceEnabled && (
                    <button
                      onClick={startVoiceRecognition}
                      disabled={isListening}
                      className={`absolute right-2 top-1/2 transform -translate-y-1/2 p-1 rounded ${isListening ? 'text-red-500' : 'text-gray-400 hover:text-gray-600'
                        }`}
                    >
                      {isListening ? <MicOff size={16} /> : <Mic size={16} />}
                    </button>
                  )}
                </div>
                <button
                  onClick={() => sendMessage()}
                  disabled={!currentMessage.trim() || isTyping}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send size={16} />
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}