/**
 * Lighthouse Service
 * 
 * Integrates with Google PageSpeed Insights API to provide
 * performance, SEO, and accessibility metrics.
 */

export interface LighthouseResult {
    score: number;
    performance: number;
    accessibility: number;
    bestPractices: number;
    seo: number;
    metrics: {
        firstContentfulPaint: string;
        speedIndex: string;
        largestContentfulPaint: string;
        interactive: string;
        totalBlockingTime: string;
        cumulativeLayoutShift: string;
    };
    opportunities: Array<{
        title: string;
        description: string;
        score: number;
    }>;
}

export const lighthouseService = {
    /**
     * Run a Lighthouse audit for a specific URL
     */
    audit: async (url: string, category: string[] = ['performance', 'seo', 'accessibility', 'best-practices']): Promise<LighthouseResult> => {
        const apiKey = process.env.NEXT_PUBLIC_GOOGLE_PAGESPEED_API_KEY || '';
        const categoriesSet = new Set(category);

        const params = new URLSearchParams({
            url,
            key: apiKey,
        });

        category.forEach(cat => params.append('category', cat));

        try {
            const response = await fetch(
                `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?${params.toString()}`
            );

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error?.message || 'Failed to run Lighthouse audit');
            }

            const data = await response.json();
            const lighthouse = data.lighthouseResult;

            return {
                score: (lighthouse.categories.performance.score + lighthouse.categories.seo.score + lighthouse.categories.accessibility.score) / 3 * 100,
                performance: lighthouse.categories.performance.score * 100,
                accessibility: lighthouse.categories.accessibility.score * 100,
                bestPractices: lighthouse.categories['best-practices'].score * 100,
                seo: lighthouse.categories.seo.score * 100,
                metrics: {
                    firstContentfulPaint: lighthouse.audits['first-contentful-paint'].displayValue,
                    speedIndex: lighthouse.audits['speed-index'].displayValue,
                    largestContentfulPaint: lighthouse.audits['largest-contentful-paint'].displayValue,
                    interactive: lighthouse.audits.interactive.displayValue,
                    totalBlockingTime: lighthouse.audits['total-blocking-time'].displayValue,
                    cumulativeLayoutShift: lighthouse.audits['cumulative-layout-shift'].displayValue,
                },
                opportunities: Object.values(lighthouse.audits)
                    .filter((audit: any) => audit.details?.type === 'opportunity' && audit.score < 1)
                    .sort((a: any, b: any) => a.score - b.score)
                    .slice(0, 5)
                    .map((opportunity: any) => ({
                        title: opportunity.title,
                        description: opportunity.description,
                        score: opportunity.score,
                    })),
            };
        } catch (error) {
            console.error('Lighthouse audit error:', error);
            throw error;
        }
    }
};
