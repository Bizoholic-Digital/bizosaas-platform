export interface SentimentResult {
    score: number; // -1 to 1
    label: 'positive' | 'neutral' | 'negative';
    magnitude?: number;
    sentiment: string;
    confidence: number;
    empathy_trigger: boolean;
}

export class SentimentAnalyzer {
    analyzeSentiment(text: string): SentimentResult {
        const textLower = text.toLowerCase();

        // Basic keyword-based analysis
        const positiveWords = ['good', 'great', 'awesome', 'excellent', 'happy', 'thanks', 'thank', 'amazing', 'perfect', 'help'];
        const negativeWords = ['bad', 'error', 'fail', 'failed', 'broken', 'issue', 'problem', 'unhappy', 'slow', 'wrong', 'not working'];

        let score = 0;
        positiveWords.forEach(word => { if (textLower.includes(word)) score += 0.2; });
        negativeWords.forEach(word => { if (textLower.includes(word)) score -= 0.2; });

        score = Math.max(-1, Math.min(1, score));

        let label: 'positive' | 'neutral' | 'negative' = 'neutral';
        if (score > 0.2) label = 'positive';
        else if (score < -0.2) label = 'negative';

        return {
            score,
            label,
            sentiment: label,
            confidence: Math.abs(score),
            empathy_trigger: label === 'negative'
        };
    }

    generateEmpatheticResponse(sentiment: SentimentResult, input: string): string {
        if (sentiment.label === 'negative') {
            return "I'm sorry to hear you're experiencing some difficulties. Let me help you resolve this. ";
        }
        if (sentiment.label === 'positive' && (input.includes('thanks') || input.includes('thank'))) {
            return "You're very welcome! I'm happy to help. ";
        }
        return "";
    }

    adjustToneForSentiment(message: string, sentiment: SentimentResult): string {
        // In a real app, this might use AI or complex rules
        return message;
    }
}
