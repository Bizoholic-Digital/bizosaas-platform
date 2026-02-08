"use client";

import React, { createContext, useContext, useEffect } from 'react';
import { useAIAssistantStore } from './store';
import { AIAssistant } from './AIAssistant';
import { ConversationContext } from './types';

interface AIAssistantContextType {
  openAssistant: () => void;
  closeAssistant: () => void;
  sendMessage: (message: string) => void;
  isOpen: boolean;
}

const AIAssistantContext = createContext<AIAssistantContextType | null>(null);

interface AIAssistantProviderProps {
  children: React.ReactNode;
  userContext: {
    userId: string;
    tenantId: string;
    userProfile?: any;
  };
  config?: {
    apiEndpoint?: string;
    websocketUrl?: string;
    enableVoiceInput?: boolean;
    enableFileUpload?: boolean;
  };
}

export function AIAssistantProvider({ 
  children, 
  userContext,
  config = {}
}: AIAssistantProviderProps) {
  const store = useAIAssistantStore();

  // Update configuration if provided
  useEffect(() => {
    if (Object.keys(config).length > 0) {
      store.updateConfig(config);
    }
  }, [config, store]);

  const contextValue: AIAssistantContextType = {
    openAssistant: store.openAssistant,
    closeAssistant: store.closeAssistant,
    sendMessage: async (message: string) => {
      // This would be handled by the useAIAssistant hook
      console.log('Send message:', message);
    },
    isOpen: store.isOpen
  };

  return (
    <AIAssistantContext.Provider value={contextValue}>
      {children}
      <AIAssistant 
        initialContext={{
          userId: userContext.userId,
          tenantId: userContext.tenantId,
          userProfile: userContext.userProfile,
          currentPage: typeof window !== 'undefined' ? window.location.pathname : undefined
        }}
      />
    </AIAssistantContext.Provider>
  );
}

export function useAIAssistantContext() {
  const context = useContext(AIAssistantContext);
  if (!context) {
    throw new Error('useAIAssistantContext must be used within an AIAssistantProvider');
  }
  return context;
}