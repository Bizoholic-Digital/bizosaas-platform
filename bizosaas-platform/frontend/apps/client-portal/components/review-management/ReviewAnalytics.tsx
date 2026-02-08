"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Progress } from '@/components/ui/progress';
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Star,
  MessageSquare,
  Calendar,
  Download,
  Filter,
  RefreshCw,
  Users,
  Globe,
  Clock,
  Target
} from 'lucide-react';

interface AnalyticsData {
  overview: {
    totalReviews: number;
    averageRating: number;
    responseRate: number;
    sentimentScore: number;
    trendsComparison: {
      reviews: number;
      rating: number;
      sentiment: number;
    };
  };
  platforms: Array<{
    name: string;
    reviews: number;
    rating: number;
    responseRate: number;
    sentiment: number;
  }>;
  trends: Array<{
    date: string;
    reviews: number;
    rating: number;
    sentiment: number;
  }>;
  sentimentBreakdown: {
    positive: number;
    neutral: number;
    negative: number;
    mixed: number;
  };
  responseMetrics: {
    averageResponseTime: number;
    automationRate: number;
    approvalRate: number;
    successRate: number;
  };
  competitorComparison: Array<{
    name: string;
    rating: number;
    reviews: number;
    responseRate: number;
  }>;
}

export default function ReviewAnalytics() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('30');

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/brain/review-management/analytics?days=${timeRange}`);
      const data = await response.json();
      setAnalyticsData(data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTrendIcon = (value: number) => {
    if (value > 0) return <TrendingUp className="h-4 w-4 text-green-600" />;
    if (value < 0) return <TrendingDown className="h-4 w-4 text-red-600" />;
    return <BarChart3 className="h-4 w-4 text-gray-600" />;
  };

  const getTrendColor = (value: number) => {
    if (value > 0) return 'text-green-600';
    if (value < 0) return 'text-red-600';
    return 'text-gray-600';
  };

  if (loading || !analyticsData) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Review Analytics</h2>
          <p className="text-muted-foreground">
            Comprehensive insights into your review performance
          </p>
        </div>
        <div className="flex gap-2">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7">Last 7 days</SelectItem>
              <SelectItem value="30">Last 30 days</SelectItem>
              <SelectItem value="90">Last 90 days</SelectItem>
              <SelectItem value="365">Last year</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" onClick={fetchAnalytics}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button>
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Key Metrics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Reviews</CardTitle>
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analyticsData.overview.totalReviews}</div>
            <div className="flex items-center text-xs text-muted-foreground">
              {getTrendIcon(analyticsData.overview.trendsComparison.reviews)}
              <span className={`ml-1 ${getTrendColor(analyticsData.overview.trendsComparison.reviews)}`}>
                {analyticsData.overview.trendsComparison.reviews > 0 ? '+' : ''}
                {analyticsData.overview.trendsComparison.reviews}% from last period
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Rating</CardTitle>
            <Star className="h-4 w-4 text-yellow-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analyticsData.overview.averageRating.toFixed(1)}</div>
            <div className="flex items-center text-xs text-muted-foreground">
              {getTrendIcon(analyticsData.overview.trendsComparison.rating)}
              <span className={`ml-1 ${getTrendColor(analyticsData.overview.trendsComparison.rating)}`}>
                {analyticsData.overview.trendsComparison.rating > 0 ? '+' : ''}
                {analyticsData.overview.trendsComparison.rating.toFixed(1)} from last period
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Response Rate</CardTitle>
            <Target className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(analyticsData.overview.responseRate * 100).toFixed(0)}%
            </div>
            <div className="text-xs text-muted-foreground">
              Industry average: 65%
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Sentiment Score</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(analyticsData.overview.sentimentScore * 100).toFixed(0)}%
            </div>
            <div className="flex items-center text-xs text-muted-foreground">
              {getTrendIcon(analyticsData.overview.trendsComparison.sentiment)}
              <span className={`ml-1 ${getTrendColor(analyticsData.overview.trendsComparison.sentiment)}`}>
                {analyticsData.overview.trendsComparison.sentiment > 0 ? '+' : ''}
                {analyticsData.overview.trendsComparison.sentiment.toFixed(1)}% from last period
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Platform Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Platform Performance</CardTitle>
          <CardDescription>
            Performance breakdown across review platforms
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {analyticsData.platforms.map((platform, index) => (
              <div key={platform.name} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <Globe className="h-5 w-5" />
                  <div>
                    <h4 className="font-medium">{platform.name}</h4>
                    <p className="text-sm text-muted-foreground">
                      {platform.reviews} reviews • {platform.rating.toFixed(1)} avg rating
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-center">
                    <div className="text-sm font-medium">Response Rate</div>
                    <div className="text-xs text-muted-foreground">
                      {(platform.responseRate * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-medium">Sentiment</div>
                    <div className="text-xs text-muted-foreground">
                      {(platform.sentiment * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Sentiment Analysis */}
      <Card>
        <CardHeader>
          <CardTitle>Sentiment Distribution</CardTitle>
          <CardDescription>
            Breakdown of customer sentiment across all reviews
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-green-700">Positive</span>
                <span className="text-sm">{analyticsData.sentimentBreakdown.positive} reviews</span>
              </div>
              <Progress 
                value={(analyticsData.sentimentBreakdown.positive / analyticsData.overview.totalReviews) * 100} 
                className="h-2"
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-yellow-700">Neutral</span>
                <span className="text-sm">{analyticsData.sentimentBreakdown.neutral} reviews</span>
              </div>
              <Progress 
                value={(analyticsData.sentimentBreakdown.neutral / analyticsData.overview.totalReviews) * 100} 
                className="h-2"
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-red-700">Negative</span>
                <span className="text-sm">{analyticsData.sentimentBreakdown.negative} reviews</span>
              </div>
              <Progress 
                value={(analyticsData.sentimentBreakdown.negative / analyticsData.overview.totalReviews) * 100} 
                className="h-2"
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-purple-700">Mixed</span>
                <span className="text-sm">{analyticsData.sentimentBreakdown.mixed} reviews</span>
              </div>
              <Progress 
                value={(analyticsData.sentimentBreakdown.mixed / analyticsData.overview.totalReviews) * 100} 
                className="h-2"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Response Automation Metrics */}
        <Card>
          <CardHeader>
            <CardTitle>Response Automation</CardTitle>
            <CardDescription>
              AI automation performance metrics
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <div>
                  <div className="text-sm font-medium">Average Response Time</div>
                  <div className="text-xs text-muted-foreground">Time to first response</div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold">
                    {analyticsData.responseMetrics.averageResponseTime.toFixed(1)}h
                  </div>
                  <Badge className="bg-green-100 text-green-800">Excellent</Badge>
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <div>
                  <div className="text-sm font-medium">Automation Rate</div>
                  <div className="text-xs text-muted-foreground">Responses generated by AI</div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold">
                    {(analyticsData.responseMetrics.automationRate * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <div>
                  <div className="text-sm font-medium">Approval Rate</div>
                  <div className="text-xs text-muted-foreground">AI responses approved without edits</div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold">
                    {(analyticsData.responseMetrics.approvalRate * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <div>
                  <div className="text-sm font-medium">Success Rate</div>
                  <div className="text-xs text-muted-foreground">Responses posted successfully</div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold">
                    {(analyticsData.responseMetrics.successRate * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Competitor Comparison */}
        <Card>
          <CardHeader>
            <CardTitle>Competitive Analysis</CardTitle>
            <CardDescription>
              How you compare to competitors
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {analyticsData.competitorComparison.map((competitor, index) => (
                <div key={competitor.name} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${index === 0 ? 'bg-green-500' : 'bg-gray-400'}`} />
                    <div>
                      <h4 className="font-medium">{competitor.name}</h4>
                      <p className="text-xs text-muted-foreground">
                        {competitor.reviews} reviews
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 text-sm">
                    <div className="text-center">
                      <div className="font-medium">{competitor.rating.toFixed(1)}</div>
                      <div className="text-xs text-muted-foreground">Rating</div>
                    </div>
                    <div className="text-center">
                      <div className="font-medium">{(competitor.responseRate * 100).toFixed(0)}%</div>
                      <div className="text-xs text-muted-foreground">Response</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Trends Chart Placeholder */}
      <Card>
        <CardHeader>
          <CardTitle>Performance Trends</CardTitle>
          <CardDescription>
            Review volume, rating, and sentiment trends over time
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-64 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg">
            <div className="text-center">
              <BarChart3 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">Interactive chart would be displayed here</p>
              <p className="text-xs text-muted-foreground mt-2">
                Showing data for the last {timeRange} days
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}