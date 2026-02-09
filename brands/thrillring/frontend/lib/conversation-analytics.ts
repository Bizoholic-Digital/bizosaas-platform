export class ConversationAnalytics {
    async trackConversation(data: any) {
        console.warn("ConversationAnalytics stub called");
        return true;
    }

    async getStats() {
        return { totalConversations: 0, avgDuration: 0 };
    }
}

export const conversationAnalytics = new ConversationAnalytics();
export const ConversationAnalyticsManager = conversationAnalytics;
