"use client";

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
    Zap,
    Search,
    Globe,
    Activity,
    CheckCircle2,
    AlertTriangle,
    ArrowRight,
    Loader2
} from "lucide-react";
import { lighthouseService, LighthouseResult } from "@/lib/services/lighthouse-service";

export default function SiteAuditPage() {
    const [url, setUrl] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<LighthouseResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleAudit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!url) return;

        setIsLoading(true);
        setError(null);
        try {
            // Basic URL validation
            const formattedUrl = url.startsWith('http') ? url : `https://${url}`;
            const data = await lighthouseService.audit(formattedUrl);
            setResult(data);
        } catch (err: any) {
            setError(err.message || 'Audit failed. Please check the URL and try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const getScoreColor = (score: number) => {
        if (score >= 90) return 'text-green-500';
        if (score >= 50) return 'text-yellow-500';
        return 'text-red-500';
    };

    return (
        <div className="space-y-6 p-6">
            <div className="flex flex-col space-y-1">
                <h1 className="text-3xl font-bold tracking-tight">Site Audit</h1>
                <p className="text-muted-foreground">
                    Analyze your website performance, SEO, and accessibility using Google Lighthouse.
                </p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Run New Audit</CardTitle>
                    <CardDescription>Enter a URL to start a comprehensive site analysis.</CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleAudit} className="flex gap-4">
                        <div className="relative flex-1">
                            <Globe className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                            <Input
                                placeholder="https://example.com"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                className="pl-10"
                                disabled={isLoading}
                            />
                        </div>
                        <Button type="submit" disabled={isLoading || !url}>
                            {isLoading ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    Analyzing...
                                </>
                            ) : (
                                <>
                                    <Search className="mr-2 h-4 w-4" />
                                    Run Audit
                                </>
                            )}
                        </Button>
                    </form>
                    {error && <p className="mt-2 text-sm text-red-500">{error}</p>}
                </CardContent>
            </Card>

            {result && (
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                    <ScoreCard title="Performance" score={result.performance} icon={<Zap className="h-4 w-4" />} />
                    <ScoreCard title="SEO" score={result.seo} icon={<Search className="h-4 w-4" />} />
                    <ScoreCard title="Accessibility" score={result.accessibility} icon={<CheckCircle2 className="h-4 w-4" />} />
                    <ScoreCard title="Best Practices" score={result.bestPractices} icon={<Activity className="h-4 w-4" />} />
                </div>
            )}

            {result && (
                <div className="grid gap-6 md:grid-cols-2">
                    <Card>
                        <CardHeader>
                            <CardTitle>Core Web Vitals</CardTitle>
                            <CardDescription>Field and lab data for page performance</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <MetricItem label="First Contentful Paint" value={result.metrics.firstContentfulPaint} />
                            <MetricItem label="Largest Contentful Paint" value={result.metrics.largestContentfulPaint} />
                            <MetricItem label="Cumulative Layout Shift" value={result.metrics.cumulativeLayoutShift} />
                            <MetricItem label="Speed Index" value={result.metrics.speedIndex} />
                            <MetricItem label="Total Blocking Time" value={result.metrics.totalBlockingTime} />
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>Top Opportunities</CardTitle>
                            <CardDescription>Most impactful changes to improve scores</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {result.opportunities.map((opt, i) => (
                                <div key={i} className="flex items-start justify-between border-b pb-2 last:border-0">
                                    <div className="space-y-1">
                                        <p className="text-sm font-medium">{opt.title}</p>
                                        <p className="text-xs text-muted-foreground line-clamp-1">{opt.description}</p>
                                    </div>
                                    <Badge variant={opt.score < 0.5 ? "destructive" : "secondary"}>
                                        {Math.round(opt.score * 100)}%
                                    </Badge>
                                </div>
                            ))}
                        </CardContent>
                    </Card>
                </div>
            )}
        </div>
    );
}

function ScoreCard({ title, score, icon }: { title: string; score: number; icon: React.ReactNode }) {
    const color = score >= 90 ? 'text-green-500' : score >= 50 ? 'text-yellow-500' : 'text-red-500';
    const bgColor = score >= 90 ? 'bg-green-500/10' : score >= 50 ? 'bg-yellow-500/10' : 'bg-red-500/10';

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                <CardTitle className="text-sm font-medium">{title}</CardTitle>
                <div className={`p-2 rounded-full ${bgColor} ${color}`}>
                    {icon}
                </div>
            </CardHeader>
            <CardContent>
                <div className={`text-2xl font-bold ${color}`}>{Math.round(score)}</div>
                <Progress value={score} className="h-1 mt-2" />
            </CardContent>
        </Card>
    );
}

function MetricItem({ label, value }: { label: string; value: string }) {
    return (
        <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">{label}</span>
            <span className="text-sm font-mono font-medium">{value}</span>
        </div>
    );
}
