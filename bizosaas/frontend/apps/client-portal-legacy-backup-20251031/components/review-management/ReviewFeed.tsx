"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import {
  Star,
  MessageSquare,
  Clock,
  Filter,
  Search,
  Eye,
  Reply,
  ThumbsUp,
  ThumbsDown,
  AlertTriangle,
  ExternalLink,
  Calendar,
  User,
  Globe,
  MoreHorizontal,
  RefreshCw,
  CheckCircle,
  XCircle,
  Loader2
} from 'lucide-react';

interface Review {
  id: string;
  platform: string;
  platformReviewId: string;
  reviewUrl?: string;
  businessId: string;
  
  // Review content
  reviewerName: string;
  reviewerId?: string;
  rating: number;
  title?: string;
  content: string;
  
  // Analysis
  sentiment: 'positive' | 'neutral' | 'negative' | 'mixed';
  sentimentScore: number;
  keywords: string[];
  categories: string[];
  urgencyLevel: number;
  
  // Response status
  requiresResponse: boolean;
  responseGenerated: boolean;
  responsePosted: boolean;
  
  // Metadata
  platformCreatedAt: string;
  discoveredAt: string;
  processedAt?: string;
  updatedAt: string;
}

interface Response {
  id: string;
  reviewId: string;
  content: string;
  status: 'pending' | 'generated' | 'pending_approval' | 'approved' | 'posted' | 'failed' | 'rejected';
  aiGenerated: boolean;
  requiresApproval: boolean;
  approvedBy?: string;
  approvedAt?: string;
  postedAt?: string;
  generatedAt: string;
}

interface FilterState {
  platform: string;
  sentiment: string;
  rating: string;
  responseStatus: string;
  dateRange: string;
  searchQuery: string;
}

export default function ReviewFeed() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [responses, setResponses] = useState<Record<string, Response>>({});
  const [loading, setLoading] = useState(true);
  const [selectedReview, setSelectedReview] = useState<Review | null>(null);
  const [generatingResponse, setGeneratingResponse] = useState<string | null>(null);
  const [filters, setFilters] = useState<FilterState>({
    platform: 'all',
    sentiment: 'all',
    rating: 'all',
    responseStatus: 'all',
    dateRange: '30',
    searchQuery: ''
  });

  useEffect(() => {
    fetchReviews();
  }, [filters]);

  const fetchReviews = async () => {
    try {
      setLoading(true);
      
      const params = new URLSearchParams();
      if (filters.platform !== 'all') params.append('platform', filters.platform);
      if (filters.sentiment !== 'all') params.append('sentiment', filters.sentiment);
      if (filters.rating !== 'all') params.append('rating', filters.rating);
      if (filters.responseStatus !== 'all') params.append('response_status', filters.responseStatus);
      if (filters.dateRange !== 'all') params.append('days', filters.dateRange);
      if (filters.searchQuery) params.append('search', filters.searchQuery);
      
      const response = await fetch(`/api/brain/review-management/reviews?${params}`);
      const data = await response.json();
      
      setReviews(data.reviews || []);
      setResponses(data.responses || {});
      
    } catch (error) {
      console.error('Failed to fetch reviews:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateResponse = async (reviewId: string) => {
    try {
      setGeneratingResponse(reviewId);
      
      const response = await fetch('/api/brain/review-management/respond', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          review_id: reviewId,
          tone: 'professional',
          language: 'en'
        }),
      });
      
      const result = await response.json();
      console.log('Response generation started:', result);
      
      // Refresh reviews after a short delay to get updated status
      setTimeout(fetchReviews, 2000);
      
    } catch (error) {
      console.error('Failed to generate response:', error);
    } finally {
      setGeneratingResponse(null);
    }
  };

  const approveResponse = async (responseId: string, approved: boolean) => {
    try {
      const response = await fetch('/api/brain/review-management/approve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          response_id: responseId,
          approved,
          approver: 'current_user',
          notes: approved ? 'Approved via dashboard' : 'Rejected via dashboard'
        }),
      });
      
      const result = await response.json();
      console.log('Response approval:', result);
      
      // Refresh to get updated status
      fetchReviews();
      
    } catch (error) {
      console.error('Failed to approve response:', error);
    }
  };

  const getPlatformIcon = (platform: string) => {
    switch (platform.toLowerCase()) {
      case 'google_business':
      case 'google':
        return '🟢';
      case 'yelp':
        return '🔴';
      case 'facebook':
        return '🔵';
      case 'tripadvisor':
        return '🟡';
      default:
        return '⭐';
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'bg-green-100 text-green-800';
      case 'negative': return 'bg-red-100 text-red-800';
      case 'neutral': return 'bg-yellow-100 text-yellow-800';
      case 'mixed': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getResponseStatusColor = (status: string) => {
    switch (status) {
      case 'posted': return 'bg-green-100 text-green-800';
      case 'approved': return 'bg-blue-100 text-blue-800';
      case 'pending_approval': return 'bg-yellow-100 text-yellow-800';
      case 'generated': return 'bg-indigo-100 text-indigo-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'rejected': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getUrgencyIcon = (level: number) => {
    if (level >= 4) return <AlertTriangle className="h-4 w-4 text-red-500" />;
    if (level >= 3) return <Clock className="h-4 w-4 text-yellow-500" />;
    return <CheckCircle className="h-4 w-4 text-green-500" />;
  };

  const filteredReviews = reviews.filter(review => {
    if (filters.searchQuery) {
      const query = filters.searchQuery.toLowerCase();
      return (
        review.content.toLowerCase().includes(query) ||
        review.reviewerName.toLowerCase().includes(query) ||
        review.keywords.some(keyword => keyword.toLowerCase().includes(query))
      );
    }
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filters
          </CardTitle>
          <CardDescription>
            Filter and search through your reviews
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div className="space-y-2">
              <Label htmlFor="search">Search</Label>
              <div className="relative">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  id="search"
                  placeholder="Search reviews..."
                  value={filters.searchQuery}
                  onChange={(e) => setFilters(prev => ({...prev, searchQuery: e.target.value}))}
                  className="pl-8"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="platform">Platform</Label>
              <Select value={filters.platform} onValueChange={(value) => setFilters(prev => ({...prev, platform: value}))}>
                <SelectTrigger>
                  <SelectValue placeholder="All platforms" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Platforms</SelectItem>
                  <SelectItem value="google_business">Google Business</SelectItem>
                  <SelectItem value="yelp">Yelp</SelectItem>
                  <SelectItem value="facebook">Facebook</SelectItem>
                  <SelectItem value="tripadvisor">TripAdvisor</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="sentiment">Sentiment</Label>
              <Select value={filters.sentiment} onValueChange={(value) => setFilters(prev => ({...prev, sentiment: value}))}>
                <SelectTrigger>
                  <SelectValue placeholder="All sentiment" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Sentiment</SelectItem>
                  <SelectItem value="positive">Positive</SelectItem>
                  <SelectItem value="neutral">Neutral</SelectItem>
                  <SelectItem value="negative">Negative</SelectItem>
                  <SelectItem value="mixed">Mixed</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="rating">Rating</Label>
              <Select value={filters.rating} onValueChange={(value) => setFilters(prev => ({...prev, rating: value}))}>
                <SelectTrigger>
                  <SelectValue placeholder="All ratings" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Ratings</SelectItem>
                  <SelectItem value="5">5 Stars</SelectItem>
                  <SelectItem value="4">4 Stars</SelectItem>
                  <SelectItem value="3">3 Stars</SelectItem>
                  <SelectItem value="2">2 Stars</SelectItem>
                  <SelectItem value="1">1 Star</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="response-status">Response Status</Label>
              <Select value={filters.responseStatus} onValueChange={(value) => setFilters(prev => ({...prev, responseStatus: value}))}>
                <SelectTrigger>
                  <SelectValue placeholder="All statuses" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Statuses</SelectItem>
                  <SelectItem value="needs_response">Needs Response</SelectItem>
                  <SelectItem value="pending_approval">Pending Approval</SelectItem>
                  <SelectItem value="posted">Responded</SelectItem>
                  <SelectItem value="no_response">No Response Needed</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="date-range">Date Range</Label>
              <Select value={filters.dateRange} onValueChange={(value) => setFilters(prev => ({...prev, dateRange: value}))}>
                <SelectTrigger>
                  <SelectValue placeholder="Select range" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7">Last 7 days</SelectItem>
                  <SelectItem value="30">Last 30 days</SelectItem>
                  <SelectItem value="90">Last 90 days</SelectItem>
                  <SelectItem value="365">Last year</SelectItem>
                  <SelectItem value="all">All time</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex justify-between items-center mt-4">
            <p className="text-sm text-muted-foreground">
              Showing {filteredReviews.length} of {reviews.length} reviews
            </p>
            <Button variant="outline" onClick={fetchReviews} disabled={loading}>
              <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Reviews List */}
      <div className="space-y-4">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin" />
            <span className="ml-2">Loading reviews...</span>
          </div>
        ) : filteredReviews.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <MessageSquare className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No reviews found</h3>
              <p className="text-muted-foreground text-center mb-4">
                {filters.searchQuery || filters.platform !== 'all' || filters.sentiment !== 'all' 
                  ? 'Try adjusting your filters to see more reviews.'
                  : 'No reviews have been collected yet.'}
              </p>
              <Button onClick={() => setFilters({
                platform: 'all',
                sentiment: 'all',
                rating: 'all',
                responseStatus: 'all',
                dateRange: '30',
                searchQuery: ''
              })}>
                Clear Filters
              </Button>
            </CardContent>
          </Card>
        ) : (
          filteredReviews.map((review) => {
            const response = responses[review.id];
            return (
              <Card key={review.id} className="overflow-hidden">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div className="flex items-start gap-3">
                      <div className="text-2xl">{getPlatformIcon(review.platform)}</div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h4 className="font-semibold">{review.reviewerName}</h4>
                          <Badge variant="outline" className="text-xs">
                            {review.platform.replace('_', ' ')}
                          </Badge>
                          {getUrgencyIcon(review.urgencyLevel)}
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="flex items-center">
                            {[...Array(5)].map((_, i) => (
                              <Star
                                key={i}
                                className={`h-4 w-4 ${
                                  i < review.rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'
                                }`}
                              />
                            ))}
                          </div>
                          <Badge className={getSentimentColor(review.sentiment)}>
                            {review.sentiment}
                          </Badge>
                          <span className="text-sm text-muted-foreground">
                            {new Date(review.platformCreatedAt).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {review.reviewUrl && (
                        <Button variant="ghost" size="sm" asChild>
                          <a href={review.reviewUrl} target="_blank" rel="noopener noreferrer">
                            <ExternalLink className="h-4 w-4" />
                          </a>
                        </Button>
                      )}
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button variant="ghost" size="sm" onClick={() => setSelectedReview(review)}>
                            <Eye className="h-4 w-4" />
                          </Button>
                        </DialogTrigger>
                        <DialogContent className="max-w-2xl">
                          <DialogHeader>
                            <DialogTitle>Review Details</DialogTitle>
                            <DialogDescription>
                              Full review content and analysis
                            </DialogDescription>
                          </DialogHeader>
                          {selectedReview && (
                            <div className="space-y-4">
                              <div className="grid grid-cols-2 gap-4">
                                <div>
                                  <Label>Platform</Label>
                                  <p className="text-sm">{selectedReview.platform.replace('_', ' ')}</p>
                                </div>
                                <div>
                                  <Label>Rating</Label>
                                  <div className="flex items-center">
                                    {[...Array(5)].map((_, i) => (
                                      <Star
                                        key={i}
                                        className={`h-4 w-4 ${
                                          i < selectedReview.rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'
                                        }`}
                                      />
                                    ))}
                                  </div>
                                </div>
                                <div>
                                  <Label>Sentiment</Label>
                                  <Badge className={getSentimentColor(selectedReview.sentiment)}>
                                    {selectedReview.sentiment} ({selectedReview.sentimentScore.toFixed(2)})
                                  </Badge>
                                </div>
                                <div>
                                  <Label>Urgency Level</Label>
                                  <p className="text-sm">{selectedReview.urgencyLevel}/5</p>
                                </div>
                              </div>
                              
                              {selectedReview.title && (
                                <div>
                                  <Label>Title</Label>
                                  <p className="text-sm font-medium">{selectedReview.title}</p>
                                </div>
                              )}
                              
                              <div>
                                <Label>Review Content</Label>
                                <p className="text-sm whitespace-pre-wrap">{selectedReview.content}</p>
                              </div>
                              
                              {selectedReview.keywords.length > 0 && (
                                <div>
                                  <Label>Keywords</Label>
                                  <div className="flex flex-wrap gap-1 mt-1">
                                    {selectedReview.keywords.map((keyword, index) => (
                                      <Badge key={index} variant="secondary" className="text-xs">
                                        {keyword}
                                      </Badge>
                                    ))}
                                  </div>
                                </div>
                              )}
                              
                              {selectedReview.categories.length > 0 && (
                                <div>
                                  <Label>Categories</Label>
                                  <div className="flex flex-wrap gap-1 mt-1">
                                    {selectedReview.categories.map((category, index) => (
                                      <Badge key={index} variant="outline" className="text-xs">
                                        {category}
                                      </Badge>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </div>
                          )}
                        </DialogContent>
                      </Dialog>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent className="pt-0">
                  {review.title && (
                    <h5 className="font-medium mb-2">{review.title}</h5>
                  )}
                  <p className="text-sm text-muted-foreground mb-3 line-clamp-3">
                    {review.content}
                  </p>
                  
                  {review.keywords.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-3">
                      {review.keywords.slice(0, 5).map((keyword, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {keyword}
                        </Badge>
                      ))}
                      {review.keywords.length > 5 && (
                        <Badge variant="secondary" className="text-xs">
                          +{review.keywords.length - 5} more
                        </Badge>
                      )}
                    </div>
                  )}
                  
                  {/* Response Section */}
                  <div className="border-t pt-3">
                    {response ? (
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <div className="flex items-center gap-2">
                            <MessageSquare className="h-4 w-4" />
                            <span className="text-sm font-medium">AI Response</span>
                            <Badge className={getResponseStatusColor(response.status)}>
                              {response.status.replace('_', ' ')}
                            </Badge>
                          </div>
                          {response.status === 'pending_approval' && (
                            <div className="flex gap-2">
                              <Button 
                                size="sm" 
                                variant="outline"
                                onClick={() => approveResponse(response.id, false)}
                              >
                                <XCircle className="h-4 w-4 mr-1" />
                                Reject
                              </Button>
                              <Button 
                                size="sm"
                                onClick={() => approveResponse(response.id, true)}
                              >
                                <CheckCircle className="h-4 w-4 mr-1" />
                                Approve
                              </Button>
                            </div>
                          )}
                        </div>
                        <div className="bg-gray-50 p-3 rounded-lg">
                          <p className="text-sm">{response.content}</p>
                        </div>
                        <div className="text-xs text-muted-foreground">
                          Generated {new Date(response.generatedAt).toLocaleString()}
                          {response.approvedAt && (
                            <span> • Approved {new Date(response.approvedAt).toLocaleString()}</span>
                          )}
                          {response.postedAt && (
                            <span> • Posted {new Date(response.postedAt).toLocaleString()}</span>
                          )}
                        </div>
                      </div>
                    ) : review.requiresResponse ? (
                      <div className="flex justify-between items-center">
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <Reply className="h-4 w-4" />
                          <span>Response needed</span>
                        </div>
                        <Button
                          size="sm"
                          onClick={() => generateResponse(review.id)}
                          disabled={generatingResponse === review.id}
                        >
                          {generatingResponse === review.id ? (
                            <>
                              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                              Generating...
                            </>
                          ) : (
                            <>
                              <Reply className="h-4 w-4 mr-2" />
                              Generate Response
                            </>
                          )}
                        </Button>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <CheckCircle className="h-4 w-4" />
                        <span>No response needed</span>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            );
          })
        )}
      </div>
    </div>
  );
}