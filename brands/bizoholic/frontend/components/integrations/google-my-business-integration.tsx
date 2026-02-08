'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { 
  MapPin, 
  RefreshCw, 
  ExternalLink, 
  CheckCircle2,
  AlertCircle,
  Plus,
  Star,
  TrendingUp,
  Users,
  Phone,
  Globe,
  Settings,
  Edit,
  Eye,
  MessageSquare,
  ChevronRight,
  BarChart3,
  Clock,
  Image,
  Calendar,
  Send,
  Reply,
  Camera,
  Navigation,
  Search,
  ThumbsUp,
  Building
} from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'

interface GoogleMyBusinessLocation {
  name: string
  location_name: string
  primary_phone: string
  primary_category: string
  website_url?: string
  location_state: 'DRAFT' | 'PENDING_VERIFICATION' | 'VERIFIED' | 'SUSPENDED' | 'NEEDS_REVERIFICATION' | 'DUPLICATE'
  address: {
    addressLines?: string[]
    locality?: string
    administrativeArea?: string
    postalCode?: string
    regionCode?: string
  }
  lat_lng: {
    latitude: number
    longitude: number
  }
  open_info: {
    periods?: Array<{
      openDay: string
      openTime: string
      closeDay: string
      closeTime: string
    }>
  }
  store_code?: string
  labels?: string[]
}

interface GoogleMyBusinessPost {
  name: string
  topic_type: 'STANDARD' | 'EVENT' | 'OFFER' | 'PRODUCT'
  language_code: string
  summary: string
  call_to_action: {
    actionType?: string
    url?: string
  }
  state: 'DRAFT' | 'LIVE' | 'REJECTED'
  create_time: string
  update_time: string
  event?: {
    title: string
    schedule: {
      start_date: string
      start_time: string
      end_date: string
      end_time: string
    }
  }
  offer?: {
    coupon_type: string
    percent_off?: number
    terms_conditions: string
  }
  media?: Array<{
    media_format: string
    source_url: string
  }>
  search_url?: string
}

interface GoogleMyBusinessReview {
  name: string
  reviewer: {
    displayName: string
    profilePhotoUrl?: string
  }
  star_rating: number
  comment: string
  create_time: string
  update_time: string
  review_reply?: {
    comment: string
    update_time: string
  }
}

interface GoogleMyBusinessInsights {
  location_name: string
  time_zone: string
  location_metrics: Array<{
    metric: string
    total_value: {
      value: string
    }
  }>
}

interface GoogleMyBusinessAccount {
  name: string
  account_name: string
  type: string
  role: string
}

interface GoogleMyBusinessIntegrationProps {
  tenantId?: string
  onUpdate?: (status: string) => void
}

export default function GoogleMyBusinessIntegration({ tenantId = "demo", onUpdate }: GoogleMyBusinessIntegrationProps) {
  const [isConnected, setIsConnected] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  
  // Data states
  const [accounts, setAccounts] = useState<GoogleMyBusinessAccount[]>([])
  const [locations, setLocations] = useState<GoogleMyBusinessLocation[]>([])
  const [selectedLocation, setSelectedLocation] = useState<GoogleMyBusinessLocation | null>(null)
  const [posts, setPosts] = useState<GoogleMyBusinessPost[]>([])
  const [reviews, setReviews] = useState<GoogleMyBusinessReview[]>([])
  const [insights, setInsights] = useState<GoogleMyBusinessInsights | null>(null)
  
  // UI states
  const [activeTab, setActiveTab] = useState('overview')
  const [showCreateLocation, setShowCreateLocation] = useState(false)
  const [showCreatePost, setShowCreatePost] = useState(false)
  const [showReplyToReview, setShowReplyToReview] = useState<string | null>(null)
  
  // Form states
  const [newLocation, setNewLocation] = useState({
    title: '',
    primaryPhone: '',
    primaryCategory: 'Restaurant',
    websiteUri: '',
    address: {
      addressLines: [''],
      locality: '',
      administrativeArea: '',
      postalCode: '',
      regionCode: 'US'
    }
  })
  
  const [newPost, setNewPost] = useState({
    topicType: 'STANDARD',
    languageCode: 'en-US',
    summary: '',
    callToAction: {
      actionType: 'LEARN_MORE',
      url: ''
    },
    media: []
  })
  
  const [reviewReply, setReviewReply] = useState('')

  const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8001'

  useEffect(() => {
    checkConnectionStatus()
  }, [tenantId])

  const checkConnectionStatus = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(
        `${BRAIN_API_URL}/api/integrations/google-my-business?tenant_id=${tenantId}&type=status`
      )
      const data = await response.json()
      
      if (data.success !== false) {
        setIsConnected(data.status === 'connected')
        if (data.status === 'connected') {
          setAccounts(data.accounts || [])
          setLocations(data.locations || [])
          if (data.locations?.length > 0) {
            setSelectedLocation(data.locations[0])
          }
        }
        onUpdate?.(data.status)
      } else {
        setError(data.error)
      }
    } catch (err) {
      setError(`Failed to check connection status: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const initiateOAuthFlow = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${BRAIN_API_URL}/api/integrations/google-my-business/oauth`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'start',
          tenant_id: tenantId
        })
      })
      
      const data = await response.json()
      
      if (data.success) {
        // Redirect to Google OAuth
        window.location.href = data.auth_url
      } else {
        setError(data.error)
      }
    } catch (err) {
      setError(`Failed to start OAuth flow: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchLocations = async () => {
    if (!isConnected) return
    
    setIsLoading(true)
    try {
      const response = await fetch(
        `${BRAIN_API_URL}/api/integrations/google-my-business/locations?tenant_id=${tenantId}`
      )
      const data = await response.json()
      
      if (data.success) {
        setLocations(data.locations)
        if (data.locations.length > 0 && !selectedLocation) {
          setSelectedLocation(data.locations[0])
        }
      } else {
        setError(data.error)
      }
    } catch (err) {
      setError(`Failed to fetch locations: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchPosts = async (locationName: string) => {
    if (!isConnected || !locationName) return
    
    setIsLoading(true)
    try {
      const response = await fetch(
        `${BRAIN_API_URL}/api/integrations/google-my-business/locations/${encodeURIComponent(locationName)}/posts?tenant_id=${tenantId}`
      )
      const data = await response.json()
      
      if (data.success) {
        setPosts(data.posts)
      } else {
        setError(data.error)
      }
    } catch (err) {
      setError(`Failed to fetch posts: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchReviews = async (locationName: string) => {
    if (!isConnected || !locationName) return
    
    setIsLoading(true)
    try {
      const response = await fetch(
        `${BRAIN_API_URL}/api/integrations/google-my-business/locations/${encodeURIComponent(locationName)}/reviews?tenant_id=${tenantId}`
      )
      const data = await response.json()
      
      if (data.success) {
        setReviews(data.reviews)
      } else {
        setError(data.error)
      }
    } catch (err) {
      setError(`Failed to fetch reviews: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchInsights = async (locationName: string) => {
    if (!isConnected || !locationName) return
    
    setIsLoading(true)
    try {
      const response = await fetch(
        `${BRAIN_API_URL}/api/integrations/google-my-business/locations/${encodeURIComponent(locationName)}/insights`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            tenant_id: tenantId,
            metric_requests: [
              { metric: 'QUERIES_DIRECT' },
              { metric: 'QUERIES_INDIRECT' },
              { metric: 'VIEWS_MAPS' },
              { metric: 'VIEWS_SEARCH' },
              { metric: 'ACTIONS_WEBSITE' },
              { metric: 'ACTIONS_PHONE' },
              { metric: 'ACTIONS_DRIVING_DIRECTIONS' }
            ]
          })
        }
      )
      const data = await response.json()
      
      if (data.success) {
        setInsights(data.insights)
      } else {
        setError(data.error)
      }
    } catch (err) {
      setError(`Failed to fetch insights: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const createLocation = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(
        `${BRAIN_API_URL}/api/integrations/google-my-business/locations`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            tenant_id: tenantId,
            ...newLocation
          })
        }
      )
      
      const data = await response.json()
      
      if (data.success) {
        setSuccess('Location created successfully!')
        setShowCreateLocation(false)
        fetchLocations()
        // Reset form
        setNewLocation({
          title: '',
          primaryPhone: '',
          primaryCategory: 'Restaurant',
          websiteUri: '',
          address: {
            addressLines: [''],
            locality: '',
            administrativeArea: '',
            postalCode: '',
            regionCode: 'US'
          }
        })
      } else {
        setError(data.error)
      }
    } catch (err) {
      setError(`Failed to create location: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const createPost = async () => {
    if (!selectedLocation) return
    
    setIsLoading(true)
    try {
      const response = await fetch(
        `${BRAIN_API_URL}/api/integrations/google-my-business/locations/${encodeURIComponent(selectedLocation.name)}/posts`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            tenant_id: tenantId,
            ...newPost
          })
        }
      )
      
      const data = await response.json()
      
      if (data.success) {
        setSuccess('Post created successfully!')
        setShowCreatePost(false)
        fetchPosts(selectedLocation.name)
        // Reset form
        setNewPost({
          topicType: 'STANDARD',
          languageCode: 'en-US',
          summary: '',
          callToAction: {
            actionType: 'LEARN_MORE',
            url: ''
          },
          media: []
        })
      } else {
        setError(data.error)
      }
    } catch (err) {
      setError(`Failed to create post: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const replyToReview = async (reviewName: string) => {
    setIsLoading(true)
    try {
      const response = await fetch(
        `${BRAIN_API_URL}/api/integrations/google-my-business/reviews/${encodeURIComponent(reviewName)}/reply`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            tenant_id: tenantId,
            reply: reviewReply
          })
        }
      )
      
      const data = await response.json()
      
      if (data.success) {
        setSuccess('Review reply posted successfully!')
        setShowReplyToReview(null)
        setReviewReply('')
        if (selectedLocation) {
          fetchReviews(selectedLocation.name)
        }
      } else {
        setError(data.error)
      }
    } catch (err) {
      setError(`Failed to reply to review: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  // Effect to fetch data when location changes
  useEffect(() => {
    if (selectedLocation && isConnected) {
      fetchPosts(selectedLocation.name)
      fetchReviews(selectedLocation.name)
      fetchInsights(selectedLocation.name)
    }
  }, [selectedLocation, isConnected])

  const getLocationStateColor = (state: string) => {
    switch (state) {
      case 'VERIFIED': return 'bg-green-100 text-green-800'
      case 'PENDING_VERIFICATION': return 'bg-yellow-100 text-yellow-800'
      case 'SUSPENDED': return 'bg-red-100 text-red-800'
      case 'DRAFT': return 'bg-gray-100 text-gray-800'
      default: return 'bg-blue-100 text-blue-800'
    }
  }

  const getPostStateColor = (state: string) => {
    switch (state) {
      case 'LIVE': return 'bg-green-100 text-green-800'
      case 'DRAFT': return 'bg-yellow-100 text-yellow-800'
      case 'REJECTED': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }).map((_, i) => (
      <Star
        key={i}
        className={`h-4 w-4 ${i < rating ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}`}
      />
    ))
  }

  // Clear messages after 5 seconds
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 5000)
      return () => clearTimeout(timer)
    }
  }, [error])

  useEffect(() => {
    if (success) {
      const timer = setTimeout(() => setSuccess(null), 5000)
      return () => clearTimeout(timer)
    }
  }, [success])

  if (!isConnected) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MapPin className="h-5 w-5 text-red-500" />
            Google My Business Integration
          </CardTitle>
          <CardDescription>
            Connect your Google My Business account to manage business locations, posts, reviews, and insights
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          
          <div className="text-center py-8">
            <MapPin className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Connect Google My Business</h3>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
              Manage your business locations, create posts, respond to reviews, and track local search performance
            </p>
            <Button 
              onClick={initiateOAuthFlow}
              disabled={isLoading}
              size="lg"
              className="bg-blue-600 hover:bg-blue-700"
            >
              {isLoading ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Connecting...
                </>
              ) : (
                <>
                  <MapPin className="h-4 w-4 mr-2" />
                  Connect Google My Business
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      
      {success && (
        <Alert>
          <CheckCircle2 className="h-4 w-4" />
          <AlertDescription>{success}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="h-5 w-5 text-green-500" />
              Google My Business Integration
              <Badge variant="secondary" className="bg-green-100 text-green-800">
                Connected
              </Badge>
            </CardTitle>
            <CardDescription>
              Managing {locations.length} location{locations.length !== 1 ? 's' : ''} across {accounts.length} account{accounts.length !== 1 ? 's' : ''}
            </CardDescription>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={checkConnectionStatus}
              disabled={isLoading}
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowCreateLocation(true)}
            >
              <Plus className="h-4 w-4 mr-2" />
              Add Location
            </Button>
          </div>
        </CardHeader>
      </Card>

      {/* Location Selector */}
      {locations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Select Business Location</CardTitle>
            <CardDescription>Choose a location to manage</CardDescription>
          </CardHeader>
          <CardContent>
            <Select 
              value={selectedLocation?.name || ''} 
              onValueChange={(value) => {
                const location = locations.find(l => l.name === value)
                setSelectedLocation(location || null)
              }}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select a business location..." />
              </SelectTrigger>
              <SelectContent>
                {locations.map((location) => (
                  <SelectItem key={location.name} value={location.name}>
                    <div className="flex items-center gap-2">
                      <Building className="h-4 w-4" />
                      <span>{location.location_name}</span>
                      <Badge className={getLocationStateColor(location.location_state)}>
                        {location.location_state}
                      </Badge>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </CardContent>
        </Card>
      )}

      {selectedLocation && (
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="posts">Posts</TabsTrigger>
            <TabsTrigger value="reviews">Reviews</TabsTrigger>
            <TabsTrigger value="insights">Insights</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Building className="h-5 w-5" />
                    Location Details
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label className="text-sm font-medium">Business Name</Label>
                    <p className="text-sm text-gray-600">{selectedLocation.location_name}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Category</Label>
                    <p className="text-sm text-gray-600">{selectedLocation.primary_category}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Phone</Label>
                    <p className="text-sm text-gray-600">{selectedLocation.primary_phone}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Website</Label>
                    <p className="text-sm text-gray-600">{selectedLocation.website_url || 'Not provided'}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Status</Label>
                    <Badge className={getLocationStateColor(selectedLocation.location_state)}>
                      {selectedLocation.location_state}
                    </Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    Quick Stats
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-3 bg-blue-50 rounded-lg">
                      <MessageSquare className="h-6 w-6 text-blue-600 mx-auto mb-1" />
                      <p className="text-2xl font-bold text-blue-600">{posts.length}</p>
                      <p className="text-xs text-blue-600">Posts</p>
                    </div>
                    <div className="text-center p-3 bg-yellow-50 rounded-lg">
                      <Star className="h-6 w-6 text-yellow-600 mx-auto mb-1" />
                      <p className="text-2xl font-bold text-yellow-600">{reviews.length}</p>
                      <p className="text-xs text-yellow-600">Reviews</p>
                    </div>
                  </div>
                  {reviews.length > 0 && (
                    <div className="text-center p-3 bg-green-50 rounded-lg">
                      <div className="flex justify-center gap-1 mb-1">
                        {renderStars(Math.round(reviews.reduce((sum, r) => sum + r.star_rating, 0) / reviews.length))}
                      </div>
                      <p className="text-2xl font-bold text-green-600">
                        {(reviews.reduce((sum, r) => sum + r.star_rating, 0) / reviews.length).toFixed(1)}
                      </p>
                      <p className="text-xs text-green-600">Average Rating</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="posts" className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold">Location Posts</h3>
              <Button onClick={() => setShowCreatePost(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Create Post
              </Button>
            </div>

            {posts.length === 0 ? (
              <Card>
                <CardContent className="py-8 text-center">
                  <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">No posts found. Create your first post to engage with customers.</p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {posts.map((post) => (
                  <Card key={post.name}>
                    <CardContent className="pt-6">
                      <div className="flex justify-between items-start mb-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <Badge className={getPostStateColor(post.state)}>
                              {post.state}
                            </Badge>
                            <Badge variant="outline">{post.topic_type}</Badge>
                          </div>
                          <p className="text-sm text-gray-900 mb-2">{post.summary}</p>
                          <p className="text-xs text-gray-500">
                            Created: {formatDate(post.create_time)}
                            {post.create_time !== post.update_time && 
                              ` • Updated: ${formatDate(post.update_time)}`
                            }
                          </p>
                        </div>
                        {post.search_url && (
                          <Button variant="outline" size="sm" asChild>
                            <a href={post.search_url} target="_blank" rel="noopener noreferrer">
                              <ExternalLink className="h-4 w-4" />
                            </a>
                          </Button>
                        )}
                      </div>
                      {post.call_to_action?.url && (
                        <div className="mt-2 p-2 bg-gray-50 rounded">
                          <p className="text-xs text-gray-600">Call to Action: {post.call_to_action.actionType}</p>
                          {post.call_to_action.url && (
                            <p className="text-xs text-blue-600">{post.call_to_action.url}</p>
                          )}
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="reviews" className="space-y-4">
            <h3 className="text-lg font-semibold">Customer Reviews</h3>

            {reviews.length === 0 ? (
              <Card>
                <CardContent className="py-8 text-center">
                  <Star className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">No reviews yet. Encourage customers to leave reviews!</p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {reviews.map((review) => (
                  <Card key={review.name}>
                    <CardContent className="pt-6">
                      <div className="flex justify-between items-start mb-4">
                        <div className="flex items-start gap-3 flex-1">
                          <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                            {review.reviewer.profilePhotoUrl ? (
                              <img
                                src={review.reviewer.profilePhotoUrl}
                                alt={review.reviewer.displayName}
                                className="w-full h-full rounded-full object-cover"
                              />
                            ) : (
                              <Users className="h-5 w-5 text-gray-500" />
                            )}
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <span className="font-medium text-sm">{review.reviewer.displayName}</span>
                              <div className="flex gap-1">
                                {renderStars(review.star_rating)}
                              </div>
                            </div>
                            <p className="text-sm text-gray-900 mb-2">{review.comment}</p>
                            <p className="text-xs text-gray-500">{formatDate(review.create_time)}</p>
                          </div>
                        </div>
                        {!review.review_reply && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setShowReplyToReview(review.name)}
                          >
                            <Reply className="h-4 w-4 mr-2" />
                            Reply
                          </Button>
                        )}
                      </div>
                      
                      {review.review_reply && (
                        <div className="ml-13 mt-4 p-3 bg-blue-50 rounded-lg border-l-4 border-blue-200">
                          <div className="flex items-center gap-2 mb-1">
                            <Building className="h-4 w-4 text-blue-600" />
                            <span className="font-medium text-sm text-blue-900">Business Reply</span>
                          </div>
                          <p className="text-sm text-blue-800 mb-1">{review.review_reply.comment}</p>
                          <p className="text-xs text-blue-600">{formatDate(review.review_reply.update_time)}</p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="insights" className="space-y-4">
            <h3 className="text-lg font-semibold">Business Insights</h3>
            
            {insights ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {insights.location_metrics.map((metric) => (
                  <Card key={metric.metric}>
                    <CardContent className="pt-6">
                      <div className="text-center">
                        <div className="mb-2">
                          {metric.metric === 'QUERIES_DIRECT' && <Search className="h-6 w-6 text-blue-600 mx-auto" />}
                          {metric.metric === 'QUERIES_INDIRECT' && <Globe className="h-6 w-6 text-green-600 mx-auto" />}
                          {metric.metric === 'VIEWS_MAPS' && <MapPin className="h-6 w-6 text-red-600 mx-auto" />}
                          {metric.metric === 'VIEWS_SEARCH' && <Eye className="h-6 w-6 text-purple-600 mx-auto" />}
                          {metric.metric === 'ACTIONS_WEBSITE' && <Globe className="h-6 w-6 text-blue-600 mx-auto" />}
                          {metric.metric === 'ACTIONS_PHONE' && <Phone className="h-6 w-6 text-green-600 mx-auto" />}
                          {metric.metric === 'ACTIONS_DRIVING_DIRECTIONS' && <Navigation className="h-6 w-6 text-orange-600 mx-auto" />}
                        </div>
                        <p className="text-2xl font-bold mb-1">{metric.total_value.value}</p>
                        <p className="text-xs text-gray-600 capitalize">
                          {metric.metric.toLowerCase().replace(/_/g, ' ')}
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : (
              <Card>
                <CardContent className="py-8 text-center">
                  <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">Insights data will appear here once available.</p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="settings" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Integration Settings</CardTitle>
                <CardDescription>Manage your Google My Business integration</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Connection Status</p>
                    <p className="text-sm text-gray-600">Your Google My Business account is connected</p>
                  </div>
                  <Badge className="bg-green-100 text-green-800">Connected</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Auto-sync</p>
                    <p className="text-sm text-gray-600">Automatically sync data every hour</p>
                  </div>
                  <Button variant="outline" size="sm">Configure</Button>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Notifications</p>
                    <p className="text-sm text-gray-600">Get notified about new reviews</p>
                  </div>
                  <Button variant="outline" size="sm">Settings</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      )}

      {/* Create Location Dialog */}
      <Dialog open={showCreateLocation} onOpenChange={setShowCreateLocation}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Create New Business Location</DialogTitle>
            <DialogDescription>
              Add a new business location to your Google My Business account
            </DialogDescription>
          </DialogHeader>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="location-name">Business Name</Label>
              <Input
                id="location-name"
                value={newLocation.title}
                onChange={(e) => setNewLocation({...newLocation, title: e.target.value})}
                placeholder="Your Business Name"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone">Phone Number</Label>
              <Input
                id="phone"
                value={newLocation.primaryPhone}
                onChange={(e) => setNewLocation({...newLocation, primaryPhone: e.target.value})}
                placeholder="+1 (555) 123-4567"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="category">Primary Category</Label>
              <Select
                value={newLocation.primaryCategory}
                onValueChange={(value) => setNewLocation({...newLocation, primaryCategory: value})}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Restaurant">Restaurant</SelectItem>
                  <SelectItem value="Retail Store">Retail Store</SelectItem>
                  <SelectItem value="Medical Practice">Medical Practice</SelectItem>
                  <SelectItem value="Professional Service">Professional Service</SelectItem>
                  <SelectItem value="Auto Service">Auto Service</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="website">Website</Label>
              <Input
                id="website"
                value={newLocation.websiteUri}
                onChange={(e) => setNewLocation({...newLocation, websiteUri: e.target.value})}
                placeholder="https://yourbusiness.com"
              />
            </div>
            <div className="space-y-2 col-span-2">
              <Label htmlFor="address">Street Address</Label>
              <Input
                id="address"
                value={newLocation.address.addressLines[0]}
                onChange={(e) => setNewLocation({
                  ...newLocation, 
                  address: {...newLocation.address, addressLines: [e.target.value]}
                })}
                placeholder="123 Main Street"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="city">City</Label>
              <Input
                id="city"
                value={newLocation.address.locality}
                onChange={(e) => setNewLocation({
                  ...newLocation, 
                  address: {...newLocation.address, locality: e.target.value}
                })}
                placeholder="New York"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="state">State</Label>
              <Input
                id="state"
                value={newLocation.address.administrativeArea}
                onChange={(e) => setNewLocation({
                  ...newLocation, 
                  address: {...newLocation.address, administrativeArea: e.target.value}
                })}
                placeholder="NY"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="zip">ZIP Code</Label>
              <Input
                id="zip"
                value={newLocation.address.postalCode}
                onChange={(e) => setNewLocation({
                  ...newLocation, 
                  address: {...newLocation.address, postalCode: e.target.value}
                })}
                placeholder="10001"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreateLocation(false)}>
              Cancel
            </Button>
            <Button onClick={createLocation} disabled={isLoading}>
              {isLoading ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Creating...
                </>
              ) : (
                'Create Location'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Create Post Dialog */}
      <Dialog open={showCreatePost} onOpenChange={setShowCreatePost}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Create New Post</DialogTitle>
            <DialogDescription>
              Create a post for {selectedLocation?.location_name}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="post-type">Post Type</Label>
              <Select
                value={newPost.topicType}
                onValueChange={(value) => setNewPost({...newPost, topicType: value as any})}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="STANDARD">Standard</SelectItem>
                  <SelectItem value="EVENT">Event</SelectItem>
                  <SelectItem value="OFFER">Offer</SelectItem>
                  <SelectItem value="PRODUCT">Product</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="post-content">Post Content</Label>
              <Textarea
                id="post-content"
                value={newPost.summary}
                onChange={(e) => setNewPost({...newPost, summary: e.target.value})}
                placeholder="What's happening at your business?"
                rows={4}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="cta-url">Call to Action URL (optional)</Label>
              <Input
                id="cta-url"
                value={newPost.callToAction.url}
                onChange={(e) => setNewPost({
                  ...newPost, 
                  callToAction: {...newPost.callToAction, url: e.target.value}
                })}
                placeholder="https://yourbusiness.com/special-offer"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreatePost(false)}>
              Cancel
            </Button>
            <Button onClick={createPost} disabled={isLoading}>
              {isLoading ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Creating...
                </>
              ) : (
                'Create Post'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Reply to Review Dialog */}
      <Dialog open={!!showReplyToReview} onOpenChange={(open) => !open && setShowReplyToReview(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Reply to Review</DialogTitle>
            <DialogDescription>
              Respond professionally to this customer review
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="reply">Your Reply</Label>
              <Textarea
                id="reply"
                value={reviewReply}
                onChange={(e) => setReviewReply(e.target.value)}
                placeholder="Thank you for your feedback..."
                rows={4}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowReplyToReview(null)}>
              Cancel
            </Button>
            <Button 
              onClick={() => showReplyToReview && replyToReview(showReplyToReview)} 
              disabled={isLoading || !reviewReply.trim()}
            >
              {isLoading ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Sending...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4 mr-2" />
                  Send Reply
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}