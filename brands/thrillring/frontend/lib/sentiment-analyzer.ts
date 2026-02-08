export class SentimentAnalyzer {
    async analyze(text: string) {
        console.warn("SentimentAnalyzer stub called");
        return { sentiment: "neutral", score: 0 };
    }
}

export const sentimentAnalyzer = new SentimentAnalyzer();
