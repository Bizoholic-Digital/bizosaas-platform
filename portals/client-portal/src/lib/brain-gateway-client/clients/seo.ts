import { BaseApiClient, type RequestOptions } from '../utils/base-client';

export interface SiteAuditRequest {
    url: string;
    max_pages?: number;
}

export interface KeywordResearchRequest {
    seed_keywords: string[];
    country_code?: string;
}

export interface BacklinkRequest {
    domain: string;
}

export interface RankTrackerScheduleRequest {
    domains: string[];
    keywords: string[];
    cron?: string;
}

export class SeoClient {
    constructor(private apiClient: BaseApiClient) { }

    async triggerSiteAudit(data: SiteAuditRequest, options?: RequestOptions) {
        return this.apiClient.post('/api/seo/audit', data, options);
    }

    async triggerKeywordResearch(data: KeywordResearchRequest, options?: RequestOptions) {
        return this.apiClient.post('/api/seo/keywords/research', data, options);
    }

    async triggerBacklinkMonitor(data: BacklinkRequest, options?: RequestOptions) {
        return this.apiClient.post('/api/seo/backlinks/monitor', data, options);
    }

    async scheduleRankTracker(data: RankTrackerScheduleRequest, options?: RequestOptions) {
        return this.apiClient.post('/api/seo/rank-tracker/schedule', data, options);
    }

    async getReport(reportId: string, options?: RequestOptions) {
        return this.apiClient.get(`/api/seo/reports/${reportId}`, options);
    }
}
