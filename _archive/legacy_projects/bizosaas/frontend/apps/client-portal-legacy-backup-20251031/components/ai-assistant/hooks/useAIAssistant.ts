import { useEffect, useRef, useCallback } from 'react';
import { useAIAssistantStore } from '../store';
import { AIService, VoiceService } from '../services/ai-service';
import { ConversationContext, Message, QuickAction } from '../types';

export function useAIAssistant() {
  const store = useAIAssistantStore();
  const aiServiceRef = useRef<AIService | null>(null);
  const voiceServiceRef = useRef<VoiceService | null>(null);

  // Initialize services
  useEffect(() => {
    if (!aiServiceRef.current) {
      aiServiceRef.current = new AIService(
        store.config.apiEndpoint,
        store.config.websocketUrl
      );

      // Set up WebSocket message handler
      aiServiceRef.current.onMessage((data) => {
        if (data.type === 'assistant_message') {
          store.addMessage({
            type: 'assistant',
            content: data.message,
            metadata: data.metadata
          });
        } else if (data.type === 'typing_indicator') {
          store.setTypingStatus(data.isTyping);
        } else if (data.type === 'connection_status') {
          store.setConnectionStatus(data.connected);
        }
      });
    }

    if (!voiceServiceRef.current && store.config.enableVoiceInput) {
      voiceServiceRef.current = new VoiceService();
    }

    return () => {
      aiServiceRef.current?.disconnect();
    };
  }, [store.config]);

  const sendMessage = useCallback(async (content: string) => {
    if (!store.conversation || !aiServiceRef.current) return;

    // Add user message immediately
    store.addMessage({
      type: 'user',
      content
    });

    // Set typing indicator
    store.setTypingStatus(true);

    try {
      const response = await aiServiceRef.current.sendMessage(
        content,
        store.conversation.context,
        store.conversation.id
      );

      // Add AI response
      store.addMessage({
        type: 'assistant',
        content: response.message,
        metadata: {
          intent: response.intent,
          confidence: response.confidence,
          actions: response.actions,
          followUpQuestions: response.followUpQuestions
        }
      });

      // Handle escalation if needed
      if (response.shouldEscalate) {
        await handleEscalation('AI suggested escalation');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      store.addMessage({
        type: 'assistant',
        content: "I'm sorry, I encountered an error. Please try again or contact support if the issue persists.",
        metadata: {
          actions: [
            {
              id: 'retry',
              label: 'Try Again',
              type: 'command',
              action: 'retry_last_message',
              variant: 'outline'
            },
            {
              id: 'escalate',
              label: 'Contact Support',
              type: 'command',
              action: 'escalate_to_human',
              variant: 'primary'
            }
          ]
        }
      });
    } finally {
      store.setTypingStatus(false);
    }
  }, [store]);

  const handleQuickAction = useCallback(async (action: QuickAction) => {
    if (!store.conversation || !aiServiceRef.current) return;

    switch (action.action) {
      case 'account_status':
        await handleAccountStatus();
        break;
      case 'analytics_overview':
        await handleAnalyticsOverview();
        break;
      case 'general_help':
        await sendMessage("I need help with using the platform");
        break;
      case 'escalate_to_human':
        await handleEscalation('User requested human agent');
        break;
      case 'retry_last_message':
        const lastUserMessage = store.conversation.messages
          .filter(m => m.type === 'user')
          .pop();
        if (lastUserMessage) {
          await sendMessage(lastUserMessage.content);
        }
        break;
      default:
        await sendMessage(`Please help me with: ${action.label}`);
    }
  }, [store, sendMessage]);

  const handleAccountStatus = useCallback(async () => {
    if (!store.conversation || !aiServiceRef.current) return;

    store.setTypingStatus(true);

    try {
      const accountData = await aiServiceRef.current.getAccountStatus(
        store.conversation.context.userId,
        store.conversation.context.tenantId
      );

      if (accountData) {
        const statusMessage = formatAccountStatus(accountData);
        store.addMessage({
          type: 'assistant',
          content: statusMessage,
          metadata: {
            intent: 'account_inquiry',
            data: accountData
          }
        });
      } else {
        store.addMessage({
          type: 'assistant',
          content: "I'm unable to retrieve your account status at the moment. Please try again later."
        });
      }
    } catch (error) {
      console.error('Error getting account status:', error);
    } finally {
      store.setTypingStatus(false);
    }
  }, [store]);

  const handleAnalyticsOverview = useCallback(async () => {
    if (!store.conversation || !aiServiceRef.current) return;

    store.setTypingStatus(true);

    try {
      const analyticsData = await aiServiceRef.current.getAnalyticsOverview(
        store.conversation.context.userId,
        store.conversation.context.tenantId,
        'last_30_days'
      );

      if (analyticsData) {
        const analyticsMessage = formatAnalyticsData(analyticsData);
        store.addMessage({
          type: 'assistant',
          content: analyticsMessage,
          metadata: {
            intent: 'performance_analysis',
            data: analyticsData,
            actions: [
              {
                id: 'detailed_report',
                label: 'View Detailed Report',
                type: 'link',
                action: '/analytics',
                variant: 'primary'
              }
            ]
          }
        });
      } else {
        store.addMessage({
          type: 'assistant',
          content: "I'm unable to retrieve your analytics data at the moment. Please try again later."
        });
      }
    } catch (error) {
      console.error('Error getting analytics overview:', error);
    } finally {
      store.setTypingStatus(false);
    }
  }, [store]);

  const handleEscalation = useCallback(async (reason: string) => {
    if (!store.conversation || !aiServiceRef.current) return;

    try {
      const escalationResult = await aiServiceRef.current.escalateToHuman(
        store.conversation.id,
        reason,
        store.conversation.context
      );

      store.addMessage({
        type: 'assistant',
        content: `I've escalated your request to a human agent. Your ticket ID is ${escalationResult.ticketId}. Estimated wait time is ${escalationResult.estimatedWaitTime} minutes. You'll receive an email notification when an agent is available.`,
        metadata: {
          intent: 'technical_support',
          data: escalationResult
        }
      });

      // Mark session as escalated
      const currentSession = store.sessions.find(s => !s.endTime);
      if (currentSession) {
        store.endSession(currentSession.id);
      }
    } catch (error) {
      console.error('Error escalating to human:', error);
      store.addMessage({
        type: 'assistant',
        content: "I'm unable to connect you to a human agent right now. Please try contacting support directly or try again later."
      });
    }
  }, [store]);

  const startVoiceInput = useCallback(async (): Promise<string | null> => {
    if (!voiceServiceRef.current?.isAvailable()) {
      throw new Error('Voice input not available');
    }

    try {
      const transcript = await voiceServiceRef.current.startListening();
      return transcript;
    } catch (error) {
      console.error('Voice input error:', error);
      return null;
    }
  }, []);

  const provideFeedback = useCallback(async (
    messageId: string, 
    feedback: 'positive' | 'negative', 
    comment?: string
  ) => {
    if (!store.conversation || !aiServiceRef.current) return;

    try {
      await aiServiceRef.current.recordFeedback(
        store.conversation.id,
        messageId,
        feedback,
        comment
      );

      // Update message with feedback
      store.updateMessage(messageId, {
        metadata: {
          ...store.conversation.messages.find(m => m.id === messageId)?.metadata,
          feedback: { type: feedback, comment, timestamp: new Date() }
        }
      });
    } catch (error) {
      console.error('Error providing feedback:', error);
    }
  }, [store]);

  return {
    // State
    conversation: store.conversation,
    isOpen: store.isOpen,
    isMinimized: store.isMinimized,
    isTyping: store.isTyping,
    isConnected: store.isConnected,
    
    // Actions
    openAssistant: store.openAssistant,
    closeAssistant: store.closeAssistant,
    toggleMinimize: store.toggleMinimize,
    startConversation: store.startConversation,
    endConversation: store.endConversation,
    clearHistory: store.clearHistory,
    
    // Message handling
    sendMessage,
    handleQuickAction,
    startVoiceInput,
    provideFeedback,
    
    // Utilities
    isVoiceAvailable: voiceServiceRef.current?.isAvailable() || false
  };
}

// Helper functions
function formatAccountStatus(accountData: any): string {
  const status = accountData.subscription?.status || 'unknown';
  const plan = accountData.subscription?.plan || 'unknown';
  const usage = accountData.usage || {};

  return `**Account Status Overview:**

**Subscription:** ${plan} (${status})
**Usage This Month:**
- API Calls: ${usage.apiCalls || 0} / ${usage.apiLimit || 'Unlimited'}
- Storage Used: ${usage.storageUsed || 0}GB / ${usage.storageLimit || 'Unlimited'}GB
- Active Campaigns: ${usage.activeCampaigns || 0}

${status === 'active' ? '✅ Everything looks good!' : '⚠️ Please check your billing information.'}

Is there anything specific about your account you'd like me to help you with?`;
}

function formatAnalyticsData(analyticsData: any): string {
  const metrics = analyticsData.metrics || {};
  const trends = analyticsData.trends || {};

  return `**Analytics Overview (Last 30 Days):**

**Key Metrics:**
- Total Visitors: ${metrics.visitors || 0} ${getTrendIndicator(trends.visitors)}
- Conversion Rate: ${metrics.conversionRate || 0}% ${getTrendIndicator(trends.conversionRate)}
- Revenue: $${metrics.revenue || 0} ${getTrendIndicator(trends.revenue)}
- Avg. Session Duration: ${metrics.sessionDuration || 0}min ${getTrendIndicator(trends.sessionDuration)}

**Top Performing Campaigns:**
${analyticsData.topCampaigns?.map((campaign: any, index: number) => 
  `${index + 1}. ${campaign.name} - ${campaign.performance}% performance`
).join('\n') || 'No campaign data available'}

Would you like me to dive deeper into any specific metric or campaign?`;
}

function getTrendIndicator(trend: number): string {
  if (trend > 0) return `📈 (+${trend}%)`;
  if (trend < 0) return `📉 (${trend}%)`;
  return '➖ (0%)';
}