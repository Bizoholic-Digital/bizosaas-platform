export interface ConversationMessage {
    id: string;
    type: 'user' | 'ai' | 'system' | 'action_result';
    content: string;
    timestamp: string;
    metadata?: any;
}

export interface ConversationSession {
    id: string;
    title: string;
    summary?: string;
    status: 'active' | 'completed' | 'archived';
    message_count: number;
    updated_at: string;
    tags: string[];
}

export class ConversationalMemoryManager {
    private apiUrl: string;
    private tenantId: string;
    private userId: string;
    private sessionId: string | null = null;
    private history: ConversationMessage[] = [];

    constructor(apiUrl: string, tenantId: string, userId: string) {
        this.apiUrl = apiUrl;
        this.tenantId = tenantId;
        this.userId = userId;
    }

    async initializeSession(sessionId?: string): Promise<string> {
        if (sessionId) {
            this.sessionId = sessionId;
            // In a real app, we might fetch history here
            return sessionId;
        }

        this.sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        return this.sessionId;
    }

    async addMessage(type: 'user' | 'ai' | 'system' | 'action_result', content: string, metadata?: any): Promise<void> {
        const message: ConversationMessage = {
            id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
            type,
            content,
            timestamp: new Date().toISOString(),
            metadata
        };

        this.history.push(message);

        // Persist to backend if needed
        try {
            await fetch(`${this.apiUrl}/api/ai/memory`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    tenant_id: this.tenantId,
                    user_id: this.userId,
                    message
                })
            });
        } catch (error) {
            console.warn('Failed to persist message to memory backend:', error);
        }
    }

    getRecentHistory(limit: number = 50): ConversationMessage[] {
        return this.history.slice(-limit);
    }

    generateContextualSuggestions(): string[] {
        // Simple logic based on history
        if (this.history.length === 0) return ["How can you help me?", "Show me my analytics"];

        const lastMessage = this.history[this.history.length - 1];
        if (lastMessage.content.toLowerCase().includes('marketing')) {
            return ["Start marketing campaign", "Check ad performance"];
        }
        if (lastMessage.content.toLowerCase().includes('sales')) {
            return ["Show sales forecast", "Audit pipeline"];
        }

        return ["What's next?", "Show more details", "Help with another task"];
    }

    async getConversationSessions(limit: number = 50): Promise<ConversationSession[]> {
        // Mock implementation
        await new Promise(resolve => setTimeout(resolve, 800));

        return [
            {
                id: 'sess_1',
                title: 'Strategic Marketing Discussion',
                summary: 'Discussed Q2 campaign objectives and platform selection.',
                status: 'active',
                message_count: 12,
                updated_at: new Date().toISOString(),
                tags: ['marketing', 'strategy']
            },
            {
                id: 'sess_2',
                title: 'SEO Audit Analysis',
                summary: 'Reviewed site performance and identified keyword opportunities.',
                status: 'completed',
                message_count: 8,
                updated_at: new Date(Date.now() - 86400000).toISOString(),
                tags: ['seo', 'audit']
            }
        ];
    }

    async searchConversations(query: string): Promise<ConversationMessage[]> {
        // Mock search implementation
        await new Promise(resolve => setTimeout(resolve, 600));

        return this.history.filter(m =>
            m.content.toLowerCase().includes(query.toLowerCase())
        );
    }

    getConversationContext(): any {
        return {
            session_id: this.sessionId,
            message_count: this.history.length,
            last_activity: this.history.length > 0 ? this.history[this.history.length - 1].timestamp : null
        };
    }

    clear(): void {
        this.history = [];
    }
}
