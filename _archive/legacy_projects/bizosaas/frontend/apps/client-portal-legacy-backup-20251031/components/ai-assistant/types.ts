export interface Message {
  id: string;
  type: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    intent?: string;
    entities?: Record<string, any>;
    confidence?: number;
    actions?: QuickAction[];
    attachments?: MessageAttachment[];
  };
}

export interface QuickAction {
  id: string;
  label: string;
  type: 'button' | 'link' | 'command';
  action: string;
  icon?: string;
  variant?: 'default' | 'primary' | 'secondary' | 'outline';
}

export interface MessageAttachment {
  id: string;
  type: 'image' | 'file' | 'chart' | 'table';
  url?: string;
  data?: any;
  caption?: string;
}

export interface ConversationState {
  id: string;
  messages: Message[];
  context: ConversationContext;
  isTyping: boolean;
  isConnected: boolean;
  lastActivity: Date;
}

export interface ConversationContext {
  userId: string;
  tenantId: string;
  currentPage?: string;
  userProfile?: UserProfile;
  recentActions?: string[];
  platformContext?: PlatformContext;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: string;
  subscription: {
    plan: string;
    status: string;
    features: string[];
  };
  preferences: {
    language: string;
    timezone: string;
    notifications: boolean;
  };
}

export interface PlatformContext {
  currentService?: string;
  activeFeatures?: string[];
  recentAlerts?: string[];
  accountStatus?: {
    health: 'good' | 'warning' | 'critical';
    issues?: string[];
  };
}

export interface AIResponse {
  message: string;
  intent: string;
  confidence: number;
  actions?: QuickAction[];
  data?: any;
  shouldEscalate?: boolean;
  followUpQuestions?: string[];
}

export interface ConversationSession {
  id: string;
  startTime: Date;
  endTime?: Date;
  messageCount: number;
  resolved: boolean;
  escalated: boolean;
  satisfaction?: number;
  tags: string[];
}

export type IntentType = 
  | 'account_inquiry'
  | 'billing_question' 
  | 'technical_support'
  | 'performance_analysis'
  | 'feature_request'
  | 'general_help'
  | 'troubleshooting'
  | 'automation_help'
  | 'reporting_request'
  | 'integration_support';

export interface AIAssistantConfig {
  apiEndpoint: string;
  websocketUrl: string;
  maxMessageHistory: number;
  responseTimeout: number;
  enableVoiceInput: boolean;
  enableFileUpload: boolean;
  personality: {
    tone: 'professional' | 'friendly' | 'casual';
    verbosity: 'concise' | 'detailed' | 'comprehensive';
    proactivity: 'low' | 'medium' | 'high';
  };
}

export interface KnowledgeBaseQuery {
  query: string;
  context?: string[];
  filters?: {
    category?: string;
    tags?: string[];
    dateRange?: {
      start: Date;
      end: Date;
    };
  };
}

export interface KnowledgeBaseResult {
  id: string;
  title: string;
  content: string;
  relevanceScore: number;
  category: string;
  tags: string[];
  lastUpdated: Date;
  url?: string;
}