export interface ConversationMetrics {
    conversationId: string;
    sessionId: string;
    startTime: number;
    messagesCount: number;
    successfulResponses: number;
    errors: number;
    averageResponseTime: number;
}

export class ConversationAnalyticsManager {
    private apiUrl: string;
    private tenantId: string;
    private userId: string;
    private currentMetrics: ConversationMetrics | null = null;

    constructor(apiUrl: string, tenantId: string, userId: string) {
        this.apiUrl = apiUrl;
        this.tenantId = tenantId;
        this.userId = userId;
    }

    startConversationTracking(conversationId: string, sessionId: string) {
        this.currentMetrics = {
            conversationId,
            sessionId,
            startTime: Date.now(),
            messagesCount: 0,
            successfulResponses: 0,
            errors: 0,
            averageResponseTime: 0
        };
    }

    trackMessage(role: 'user' | 'ai', responseTime?: number, sentimentScore?: number) {
        if (!this.currentMetrics) return;

        this.currentMetrics.messagesCount++;

        if (role === 'ai' && responseTime !== undefined) {
            this.currentMetrics.successfulResponses++;
            const totalResponseTime = (this.currentMetrics.averageResponseTime * (this.currentMetrics.successfulResponses - 1)) + responseTime;
            this.currentMetrics.averageResponseTime = totalResponseTime / this.currentMetrics.successfulResponses;
        }

        // Send to backend
        this.logEvent('message_tracked', { role, responseTime, sentimentScore });
    }

    trackCommand(intent: string, success: boolean, responseTime: number) {
        this.logEvent('command_executed', { intent, success, responseTime });
    }

    trackError(errorType: string, payload: any) {
        if (this.currentMetrics) this.currentMetrics.errors++;
        this.logEvent('error_occurred', { errorType, ...payload });
    }

    async submitFeedback(feedback: Omit<UserFeedback, 'id' | 'timestamp' | 'resolved' | 'priority' | 'tenantId' | 'userId'>): Promise<boolean> {
        return this.logEvent('feedback_submitted', {
            ...feedback,
            id: `fb_${Date.now()}`,
            timestamp: new Date().toISOString(),
            resolved: false,
            priority: feedback.type === 'bug_report' ? 'high' : 'medium'
        });
    }

    async getConversationInsights(timeframe: 'day' | 'week' | 'month' | 'all'): Promise<ConversationInsights> {
        // Mock implementation for analytics dashboard
        await new Promise(resolve => setTimeout(resolve, 500));

        return {
            totalConversations: 1250,
            averageMessageCount: 8.4,
            averageDuration: 450000,
            performanceMetrics: {
                averageResponseTime: 450,
                completionRate: 92.5,
                errorRate: 1.2
            },
            averageSatisfactionScore: 4.8,
            userEngagement: {
                dailyActiveUsers: 85,
                weeklyActiveUsers: 320,
                monthlyActiveUsers: 850,
                retentionRate: 72.5
            },
            mostCommonCommands: [
                { command: '/create-campaign', count: 450, successRate: 98.2 },
                { command: '/analyze-leads', count: 320, successRate: 95.5 },
                { command: '/schedule-post', count: 280, successRate: 99.1 }
            ],
            mostCommonErrors: [],
            sentimentTrends: []
        };
    }

    getCurrentMetrics(): ConversationMetrics | null {
        return this.currentMetrics;
    }

    private async logEvent(eventType: string, data: any): Promise<boolean> {
        try {
            const response = await fetch(`${this.apiUrl}/api/analytics/log`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tenant_id: this.tenantId,
                    user_id: this.userId,
                    event_type: eventType,
                    payload: data,
                    timestamp: new Date().toISOString()
                })
            });
            return response.ok;
        } catch (error) {
            console.warn('Analytics logging failed:', error);
            return false;
        }
    }
}

export interface ConversationInsights {
    totalConversations: number;
    averageMessageCount: number;
    averageDuration: number;
    performanceMetrics: {
        averageResponseTime: number;
        completionRate: number;
        errorRate: number;
    };
    averageSatisfactionScore: number;
    userEngagement: {
        dailyActiveUsers: number;
        weeklyActiveUsers: number;
        monthlyActiveUsers: number;
        retentionRate: number;
    };
    mostCommonCommands: {
        command: string;
        count: number;
        successRate: number;
    }[];
    mostCommonErrors: {
        error: string;
        count: number;
        lastOccurred: string;
    }[];
    sentimentTrends: {
        date: string;
        positive: number;
        neutral: number;
        negative: number;
    }[];
}

export interface UserFeedback {
    id: string;
    conversationId: string;
    messageId?: string;
    userId: string;
    tenantId: string;
    type: 'satisfaction' | 'quality' | 'helpfulness' | 'accuracy' | 'speed' | 'bug_report' | 'feature_request';
    rating: number;
    comment?: string;
    category: string;
    context?: {
        userMessage?: string;
        aiResponse?: string;
        responseTime?: number;
    };
    timestamp: string;
    resolved: boolean;
    priority: 'low' | 'medium' | 'high' | 'critical';
}
