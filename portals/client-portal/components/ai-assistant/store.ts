import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { 
  Message, 
  ConversationState, 
  ConversationContext, 
  QuickAction,
  AIAssistantConfig,
  ConversationSession 
} from './types';

interface AIAssistantStore {
  // State
  conversation: ConversationState | null;
  isOpen: boolean;
  isMinimized: boolean;
  isTyping: boolean;
  isConnected: boolean;
  config: AIAssistantConfig;
  sessions: ConversationSession[];
  
  // Actions
  openAssistant: () => void;
  closeAssistant: () => void;
  toggleMinimize: () => void;
  
  // Conversation management
  startConversation: (context: ConversationContext) => void;
  endConversation: () => void;
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void;
  updateMessage: (messageId: string, updates: Partial<Message>) => void;
  deleteMessage: (messageId: string) => void;
  clearHistory: () => void;
  
  // Connection management
  setConnectionStatus: (connected: boolean) => void;
  setTypingStatus: (typing: boolean) => void;
  
  // Configuration
  updateConfig: (config: Partial<AIAssistantConfig>) => void;
  
  // Session management
  createSession: () => string;
  endSession: (sessionId: string, satisfaction?: number) => void;
  getSessionHistory: () => ConversationSession[];
}

const defaultConfig: AIAssistantConfig = {
  apiEndpoint: process.env.NEXT_PUBLIC_AI_API_ENDPOINT || 'http://localhost:8001/ai',
  websocketUrl: process.env.NEXT_PUBLIC_AI_WS_URL || 'ws://localhost:8001/ai/ws',
  maxMessageHistory: 50,
  responseTimeout: 30000,
  enableVoiceInput: true,
  enableFileUpload: true,
  personality: {
    tone: 'professional',
    verbosity: 'detailed',
    proactivity: 'medium'
  }
};

export const useAIAssistantStore = create<AIAssistantStore>()(
  devtools(
    persist(
      (set, get) => ({
        // Initial state
        conversation: null,
        isOpen: false,
        isMinimized: false,
        isTyping: false,
        isConnected: false,
        config: defaultConfig,
        sessions: [],

        // UI Actions
        openAssistant: () => set({ isOpen: true, isMinimized: false }),
        closeAssistant: () => set({ isOpen: false }),
        toggleMinimize: () => set((state) => ({ isMinimized: !state.isMinimized })),

        // Conversation management
        startConversation: (context: ConversationContext) => {
          const conversationId = `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          const sessionId = get().createSession();
          
          set({
            conversation: {
              id: conversationId,
              messages: [{
                id: `msg_${Date.now()}_welcome`,
                type: 'assistant',
                content: `Hello! I'm your BizOSaaS AI Assistant. I'm here to help you with account management, technical support, analytics insights, and more. What can I assist you with today?`,
                timestamp: new Date(),
                metadata: {
                  actions: [
                    {
                      id: 'check_account',
                      label: 'Check Account Status',
                      type: 'command',
                      action: 'account_status',
                      icon: 'user',
                      variant: 'outline'
                    },
                    {
                      id: 'view_analytics',
                      label: 'View Analytics',
                      type: 'command',
                      action: 'analytics_overview',
                      icon: 'bar-chart',
                      variant: 'outline'
                    },
                    {
                      id: 'get_help',
                      label: 'Get Help',
                      type: 'command',
                      action: 'general_help',
                      icon: 'help-circle',
                      variant: 'outline'
                    }
                  ]
                }
              }],
              context,
              isTyping: false,
              isConnected: true,
              lastActivity: new Date()
            }
          });
        },

        endConversation: () => {
          const conversation = get().conversation;
          if (conversation) {
            // End current session if exists
            const currentSession = get().sessions.find(s => !s.endTime);
            if (currentSession) {
              get().endSession(currentSession.id);
            }
          }
          set({ conversation: null });
        },

        addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => {
          const conversation = get().conversation;
          if (!conversation) return;

          const newMessage: Message = {
            ...message,
            id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            timestamp: new Date()
          };

          const updatedMessages = [...conversation.messages, newMessage];
          
          // Limit message history
          const maxHistory = get().config.maxMessageHistory;
          if (updatedMessages.length > maxHistory) {
            updatedMessages.splice(0, updatedMessages.length - maxHistory);
          }

          set({
            conversation: {
              ...conversation,
              messages: updatedMessages,
              lastActivity: new Date()
            }
          });
        },

        updateMessage: (messageId: string, updates: Partial<Message>) => {
          const conversation = get().conversation;
          if (!conversation) return;

          const updatedMessages = conversation.messages.map(msg =>
            msg.id === messageId ? { ...msg, ...updates } : msg
          );

          set({
            conversation: {
              ...conversation,
              messages: updatedMessages,
              lastActivity: new Date()
            }
          });
        },

        deleteMessage: (messageId: string) => {
          const conversation = get().conversation;
          if (!conversation) return;

          const updatedMessages = conversation.messages.filter(msg => msg.id !== messageId);

          set({
            conversation: {
              ...conversation,
              messages: updatedMessages,
              lastActivity: new Date()
            }
          });
        },

        clearHistory: () => {
          const conversation = get().conversation;
          if (!conversation) return;

          set({
            conversation: {
              ...conversation,
              messages: [{
                id: `msg_${Date.now()}_cleared`,
                type: 'system',
                content: 'Conversation history cleared.',
                timestamp: new Date()
              }],
              lastActivity: new Date()
            }
          });
        },

        // Connection management
        setConnectionStatus: (connected: boolean) => {
          set({ isConnected: connected });
          
          const conversation = get().conversation;
          if (conversation) {
            set({
              conversation: {
                ...conversation,
                isConnected: connected
              }
            });
          }
        },

        setTypingStatus: (typing: boolean) => {
          set({ isTyping: typing });
          
          const conversation = get().conversation;
          if (conversation) {
            set({
              conversation: {
                ...conversation,
                isTyping: typing
              }
            });
          }
        },

        // Configuration
        updateConfig: (configUpdates: Partial<AIAssistantConfig>) => {
          set((state) => ({
            config: { ...state.config, ...configUpdates }
          }));
        },

        // Session management
        createSession: () => {
          const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          const newSession: ConversationSession = {
            id: sessionId,
            startTime: new Date(),
            messageCount: 0,
            resolved: false,
            escalated: false,
            tags: []
          };

          set((state) => ({
            sessions: [...state.sessions, newSession]
          }));

          return sessionId;
        },

        endSession: (sessionId: string, satisfaction?: number) => {
          set((state) => ({
            sessions: state.sessions.map(session =>
              session.id === sessionId
                ? {
                    ...session,
                    endTime: new Date(),
                    satisfaction,
                    resolved: !session.escalated
                  }
                : session
            )
          }));
        },

        getSessionHistory: () => {
          return get().sessions.slice(-10); // Return last 10 sessions
        }
      }),
      {
        name: 'ai-assistant-storage',
        partialize: (state) => ({
          config: state.config,
          sessions: state.sessions.slice(-5), // Only persist last 5 sessions
        }),
      }
    ),
    {
      name: 'ai-assistant-store',
    }
  )
);