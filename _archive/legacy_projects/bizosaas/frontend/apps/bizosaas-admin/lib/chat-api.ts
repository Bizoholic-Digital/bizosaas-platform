export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

export interface ChatContext {
  userId: string;
  tenantId: string;
  currentPage: string;
  userProfile: {
    name: string;
    email: string;
  };
  conversationId?: string;
  previousMessages?: ChatMessage[];
}

export interface QuickAction {
  label: string;
  action: string;
}

export interface ChatResponse {
  message: string;
  conversationId?: string;
  suggestions?: string[];
  quickActions?: QuickAction[];
  operationCompleted?: boolean;
  needsConfirmation?: boolean;
  confirmationMessage?: string;
  operation?: {
    results?: any;
  };
}

export const chatAPI = {
  sendMessage: async (message: string, context: ChatContext): Promise<ChatResponse> => {
    // Mock implementation
    return {
      message: `Echo: ${message}`,
      conversationId: 'mock-conv-id',
    };
  }
};
