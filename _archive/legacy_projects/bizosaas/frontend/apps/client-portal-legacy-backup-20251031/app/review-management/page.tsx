"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Star,
  MessageSquare,
  TrendingUp,
  TrendingDown,
  Clock,
  CheckCircle,
  AlertCircle,
  Eye,
  Filter,
  Download,
  Settings,
  RefreshCw,
  BarChart3,
  Users,
  Globe,
  Zap
} from 'lucide-react';

// Components
import ReviewFeed from '@/components/review-management/ReviewFeed';
import ResponseAutomation from '@/components/review-management/ResponseAutomation';
import ReviewAnalytics from '@/components/review-management/ReviewAnalytics';
import ReputationMonitoring from '@/components/review-management/ReputationMonitoring';
import WorkflowStatus from '@/components/review-management/WorkflowStatus';

interface ReviewSummary {
  totalReviews: number;
  platformBreakdown: Record<string, number>;
  sentimentDistribution: Record<string, number>;
  averageRating: number;
  responseRate: number;
  recentActivity: Array<{
    id: string;
    platform: string;
    rating: number;
    sentiment: string;
    timestamp: string;
  }>;
}

interface ReputationScore {
  overallScore: number;
  platformScores: Record<string, number>;
  sentimentTrend: Array<{
    date: string;
    score: number;
  }>;
  keyMetrics: Record<string, number>;
  recommendations: string[];
}

export default function ReviewManagementPage() {
  const [activeTab, setActiveTab] = useState('overview');
  const [reviewSummary, setReviewSummary] = useState<ReviewSummary | null>(null);
  const [reputationScore, setReputationScore] = useState<ReputationScore | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch review summary
      const summaryResponse = await fetch('/api/brain/review-management/summary');
      const summaryData = await summaryResponse.json();
      setReviewSummary(summaryData);
      
      // Fetch reputation score
      const reputationResponse = await fetch('/api/brain/review-management/reputation');
      const reputationData = await reputationResponse.json();
      setReputationScore(reputationData);
      
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchDashboardData();
    setRefreshing(false);
  };

  const startReviewCollection = async () => {
    try {
      const response = await fetch('/api/brain/review-management/collect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          platforms: ['google_business', 'yelp', 'facebook'],
          business_ids: ['main_location'],
          force_collection: true
        }),
      });
      
      const result = await response.json();
      console.log('Collection started:', result);
      
      // Show success message and refresh data
      setTimeout(handleRefresh, 2000);
      
    } catch (error) {
      console.error('Failed to start collection:', error);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment.toLowerCase()) {
      case 'positive': return 'text-green-600';
      case 'negative': return 'text-red-600';
      case 'neutral': return 'text-yellow-600';
      default: return 'text-gray-600';
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment.toLowerCase()) {
      case 'positive': return <TrendingUp className="h-4 w-4" />;
      case 'negative': return <TrendingDown className="h-4 w-4" />;
      default: return <BarChart3 className="h-4 w-4" />;
    }
  };

  if (loading && !reviewSummary) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p>Loading review management dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Review Management</h1>
          <p className="text-muted-foreground">
            AI-powered review monitoring and response automation
          </p>
        </div>
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            onClick={handleRefresh}
            disabled={refreshing}
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button onClick={startReviewCollection}>
            <Download className="h-4 w-4 mr-2" />
            Collect Reviews
          </Button>
          <Button variant="outline">
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </Button>
        </div>
      </div>

      {/* Key Metrics Overview */}
      {reviewSummary && reputationScore && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Overall Rating</CardTitle>
              <Star className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {reputationScore.overallScore.toFixed(1)}
              </div>
              <p className="text-xs text-muted-foreground">
                Based on {reviewSummary.totalReviews} reviews
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Reviews</CardTitle>
              <MessageSquare className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{reviewSummary.totalReviews}</div>
              <p className="text-xs text-muted-foreground">
                {reviewSummary.recentActivity.length} new this week
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Response Rate</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {(reviewSummary.responseRate * 100).toFixed(0)}%
              </div>
              <p className="text-xs text-muted-foreground">
                {(reputationScore.keyMetrics.response_time_hours || 0).toFixed(1)}h avg response time
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Sentiment Score</CardTitle>
              <TrendingUp className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {(Object.values(reviewSummary.sentimentDistribution).reduce((acc, val, idx) => 
                  acc + val * [1, 0, -1][idx], 0) / reviewSummary.totalReviews * 100).toFixed(0)}%
              </div>
              <p className="text-xs text-muted-foreground">
                Positive sentiment trend
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Platform Breakdown */}
      {reviewSummary && (
        <Card>
          <CardHeader>
            <CardTitle>Platform Distribution</CardTitle>
            <CardDescription>
              Review distribution across platforms
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.entries(reviewSummary.platformBreakdown).map(([platform, count]) => (
                <div key={platform} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center gap-2">
                    <Globe className="h-4 w-4" />
                    <span className="capitalize">{platform.replace('_', ' ')}</span>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold">{count}</div>
                    <div className="text-xs text-muted-foreground">
                      {((count / reviewSummary.totalReviews) * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Sentiment Analysis */}
      {reviewSummary && (
        <Card>
          <CardHeader>
            <CardTitle>Sentiment Analysis</CardTitle>
            <CardDescription>
              Customer sentiment breakdown across all reviews
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(reviewSummary.sentimentDistribution).map(([sentiment, count]) => {
                const percentage = (count / reviewSummary.totalReviews) * 100;
                return (
                  <div key={sentiment} className="space-y-2">
                    <div className="flex justify-between items-center">
                      <div className={`flex items-center gap-2 ${getSentimentColor(sentiment)}`}>
                        {getSentimentIcon(sentiment)}
                        <span className="capitalize font-medium">{sentiment}</span>
                      </div>
                      <span className="text-sm font-medium">{count} ({percentage.toFixed(0)}%)</span>
                    </div>
                    <Progress value={percentage} className="h-2" />
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Main Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="reviews">Reviews</TabsTrigger>
          <TabsTrigger value="responses">Responses</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="monitoring">Monitoring</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>
                Latest reviews and responses across all platforms
              </CardDescription>
            </CardHeader>
            <CardContent>
              {reviewSummary?.recentActivity.length ? (
                <div className="space-y-4">
                  {reviewSummary.recentActivity.slice(0, 5).map((activity) => (
                    <div key={activity.id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className="flex items-center gap-1">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`h-4 w-4 ${
                                i < activity.rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'
                              }`}
                            />
                          ))}
                        </div>
                        <Badge variant={activity.sentiment === 'positive' ? 'default' : 
                                     activity.sentiment === 'negative' ? 'destructive' : 'secondary'}>
                          {activity.platform}
                        </Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {new Date(activity.timestamp).toLocaleDateString()}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  <MessageSquare className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>No recent activity found</p>
                  <Button className="mt-4" onClick={startReviewCollection}>
                    <Download className="h-4 w-4 mr-2" />
                    Collect Reviews
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Recommendations */}
          {reputationScore?.recommendations.length && (
            <Card>
              <CardHeader>
                <CardTitle>AI Recommendations</CardTitle>
                <CardDescription>
                  Actionable insights to improve your online reputation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {reputationScore.recommendations.map((recommendation, index) => (
                    <div key={index} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                      <Zap className="h-5 w-5 text-blue-600 mt-0.5" />
                      <p className="text-sm">{recommendation}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="reviews">
          <ReviewFeed />
        </TabsContent>

        <TabsContent value="responses">
          <ResponseAutomation />
        </TabsContent>

        <TabsContent value="analytics">
          <ReviewAnalytics />
        </TabsContent>

        <TabsContent value="monitoring">
          <ReputationMonitoring />
        </TabsContent>
      </Tabs>

      {/* Workflow Status */}
      <WorkflowStatus />
    </div>
  );
}