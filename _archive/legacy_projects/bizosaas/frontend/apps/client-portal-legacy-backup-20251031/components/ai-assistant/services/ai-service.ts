import { 
  AIResponse, 
  ConversationContext, 
  KnowledgeBaseQuery, 
  KnowledgeBaseResult,
  IntentType 
} from '../types';

export class AIService {
  private apiEndpoint: string;
  private websocket: WebSocket | null = null;
  private messageQueue: any[] = [];
  private isConnected = false;

  constructor(apiEndpoint: string, websocketUrl: string) {
    this.apiEndpoint = apiEndpoint;
    this.initWebSocket(websocketUrl);
  }

  private initWebSocket(websocketUrl: string) {
    try {
      this.websocket = new WebSocket(websocketUrl);
      
      this.websocket.onopen = () => {
        this.isConnected = true;
        console.log('AI Assistant WebSocket connected');
        
        // Send queued messages
        while (this.messageQueue.length > 0) {
          const message = this.messageQueue.shift();
          this.websocket?.send(JSON.stringify(message));
        }
      };

      this.websocket.onclose = () => {
        this.isConnected = false;
        console.log('AI Assistant WebSocket disconnected');
        
        // Attempt to reconnect after 5 seconds
        setTimeout(() => {
          this.initWebSocket(websocketUrl);
        }, 5000);
      };

      this.websocket.onerror = (error) => {
        console.error('AI Assistant WebSocket error:', error);
      };
    } catch (error) {
      console.error('Failed to initialize WebSocket:', error);
    }
  }

  async sendMessage(
    message: string, 
    context: ConversationContext,
    conversationId: string
  ): Promise<AIResponse> {
    try {
      const payload = {
        message,
        context,
        conversationId,
        timestamp: new Date().toISOString()
      };

      // Try WebSocket first for real-time communication
      if (this.websocket && this.isConnected) {
        return new Promise((resolve, reject) => {
          const messageId = `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          
          const handleResponse = (event: MessageEvent) => {
            const response = JSON.parse(event.data);
            if (response.messageId === messageId) {
              this.websocket?.removeEventListener('message', handleResponse);
              resolve(response.data);
            }
          };

          this.websocket.addEventListener('message', handleResponse);
          
          this.websocket.send(JSON.stringify({
            ...payload,
            messageId,
            type: 'chat_message'
          }));

          // Timeout after 30 seconds
          setTimeout(() => {
            this.websocket?.removeEventListener('message', handleResponse);
            reject(new Error('Response timeout'));
          }, 30000);
        });
      }

      // Fallback to HTTP API
      const response = await fetch(`${this.apiEndpoint}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`AI API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message to AI service:', error);
      return this.getErrorResponse(error as Error);
    }
  }

  async analyzeIntent(message: string, context: ConversationContext): Promise<{
    intent: IntentType;
    confidence: number;
    entities: Record<string, any>;
  }> {
    try {
      const response = await fetch(`${this.apiEndpoint}/analyze-intent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify({ message, context })
      });

      if (!response.ok) {
        throw new Error(`Intent analysis error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error analyzing intent:', error);
      return {
        intent: 'general_help',
        confidence: 0.5,
        entities: {}
      };
    }
  }

  async searchKnowledgeBase(query: KnowledgeBaseQuery): Promise<KnowledgeBaseResult[]> {
    try {
      const response = await fetch(`${this.apiEndpoint}/knowledge-base/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify(query)
      });

      if (!response.ok) {
        throw new Error(`Knowledge base search error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error searching knowledge base:', error);
      return [];
    }
  }

  async getAccountStatus(userId: string, tenantId: string): Promise<any> {
    try {
      const response = await fetch(`${this.apiEndpoint}/account-status`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify({ userId, tenantId })
      });

      if (!response.ok) {
        throw new Error(`Account status error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting account status:', error);
      return null;
    }
  }

  async getAnalyticsOverview(userId: string, tenantId: string, timeRange?: string): Promise<any> {
    try {
      const response = await fetch(`${this.apiEndpoint}/analytics-overview`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify({ userId, tenantId, timeRange })
      });

      if (!response.ok) {
        throw new Error(`Analytics overview error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting analytics overview:', error);
      return null;
    }
  }

  async escalateToHuman(
    conversationId: string, 
    reason: string, 
    context: ConversationContext
  ): Promise<{ ticketId: string; estimatedWaitTime: number }> {
    try {
      const response = await fetch(`${this.apiEndpoint}/escalate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify({
          conversationId,
          reason,
          context,
          timestamp: new Date().toISOString()
        })
      });

      if (!response.ok) {
        throw new Error(`Escalation error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error escalating to human:', error);
      return {
        ticketId: `ticket_${Date.now()}`,
        estimatedWaitTime: 15 // fallback wait time in minutes
      };
    }
  }

  async recordFeedback(
    conversationId: string,
    messageId: string,
    feedback: 'positive' | 'negative',
    comment?: string
  ): Promise<void> {
    try {
      await fetch(`${this.apiEndpoint}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify({
          conversationId,
          messageId,
          feedback,
          comment,
          timestamp: new Date().toISOString()
        })
      });
    } catch (error) {
      console.error('Error recording feedback:', error);
    }
  }

  onMessage(callback: (data: any) => void) {
    if (this.websocket) {
      this.websocket.addEventListener('message', (event) => {
        const data = JSON.parse(event.data);
        callback(data);
      });
    }
  }

  disconnect() {
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }
  }

  private getAuthToken(): string {
    // Get token from localStorage or context
    return localStorage.getItem('auth_token') || '';
  }

  private getErrorResponse(error: Error): AIResponse {
    return {
      message: "I apologize, but I'm experiencing technical difficulties. Please try again in a moment, or I can connect you with a human agent if you need immediate assistance.",
      intent: 'technical_support',
      confidence: 1.0,
      shouldEscalate: true,
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
          label: 'Speak to Human Agent',
          type: 'command',
          action: 'escalate_to_human',
          variant: 'primary'
        }
      ]
    };
  }
}

// Voice service for speech recognition
export class VoiceService {
  private recognition: any = null;
  private isListening = false;

  constructor() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      this.recognition = new SpeechRecognition();
      
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = 'en-US';
    }
  }

  isAvailable(): boolean {
    return this.recognition !== null;
  }

  startListening(): Promise<string> {
    return new Promise((resolve, reject) => {
      if (!this.recognition) {
        reject(new Error('Speech recognition not available'));
        return;
      }

      if (this.isListening) {
        reject(new Error('Already listening'));
        return;
      }

      this.recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        resolve(transcript);
      };

      this.recognition.onerror = (event: any) => {
        reject(new Error(`Speech recognition error: ${event.error}`));
      };

      this.recognition.onend = () => {
        this.isListening = false;
      };

      this.isListening = true;
      this.recognition.start();
    });
  }

  stopListening() {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
    }
  }
}