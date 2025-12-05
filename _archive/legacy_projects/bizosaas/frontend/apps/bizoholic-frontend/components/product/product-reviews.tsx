"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { cn } from "@/lib/utils"
import { Star, ThumbsUp, ThumbsDown, MessageSquare, User, CheckCircle } from "lucide-react"

interface Review {
  id: string
  userId: string
  userName: string
  userAvatar?: string
  rating: number
  title: string
  comment: string
  createdAt: string
  verified: boolean
  helpful: number
  notHelpful: number
  images?: string[]
}

interface ProductReviewsProps {
  productId: string
  rating: number
  reviewCount: number
  className?: string
}

// Mock reviews data
const mockReviews: Review[] = [
  {
    id: "1",
    userId: "user1",
    userName: "Sarah Johnson",
    rating: 5,
    title: "Excellent product, exceeded expectations!",
    comment: "I've been using this for about a month now and it's fantastic. The quality is top-notch and it arrived exactly as described. Highly recommend!",
    createdAt: "2024-01-15T10:00:00Z",
    verified: true,
    helpful: 12,
    notHelpful: 1
  },
  {
    id: "2",
    userId: "user2",
    userName: "Mike Chen",
    rating: 4,
    title: "Good value for money",
    comment: "Solid product overall. The build quality is good and it does exactly what it's supposed to do. Only minor complaint is the packaging could be better.",
    createdAt: "2024-01-12T14:30:00Z",
    verified: true,
    helpful: 8,
    notHelpful: 0
  },
  {
    id: "3",
    userId: "user3",
    userName: "Emma Davis",
    rating: 5,
    title: "Perfect for my needs",
    comment: "This is exactly what I was looking for. Fast shipping, great quality, and excellent customer service. Will definitely buy from this seller again.",
    createdAt: "2024-01-10T09:15:00Z",
    verified: false,
    helpful: 15,
    notHelpful: 2
  }
]

function ReviewStars({ rating, size = "sm" }: { rating: number; size?: "sm" | "md" | "lg" }) {
  const starSize = size === "sm" ? "h-4 w-4" : size === "md" ? "h-5 w-5" : "h-6 w-6"
  
  return (
    <div className="flex items-center gap-1">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          className={cn(
            starSize,
            star <= rating ? "text-yellow-400 fill-current" : "text-gray-300"
          )}
        />
      ))}
    </div>
  )
}

function ReviewItem({ review }: { review: Review }) {
  const [helpfulVotes, setHelpfulVotes] = useState({ helpful: review.helpful, notHelpful: review.notHelpful })
  const [userVote, setUserVote] = useState<'helpful' | 'not-helpful' | null>(null)
  
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }
  
  const handleVote = (type: 'helpful' | 'not-helpful') => {
    if (userVote === type) return // Already voted
    
    setHelpfulVotes(prev => ({
      helpful: type === 'helpful' ? prev.helpful + 1 : prev.helpful,
      notHelpful: type === 'not-helpful' ? prev.notHelpful + 1 : prev.notHelpful
    }))
    setUserVote(type)
  }
  
  return (
    <div className="space-y-4">
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0">
          <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
            <User className="h-5 w-5 text-red-600" />
          </div>
        </div>
        
        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-2">
            <span className="font-medium text-gray-900 dark:text-white">{review.userName}</span>
            {review.verified && (
              <Badge className="bg-green-100 text-green-800 text-xs">
                <CheckCircle className="h-3 w-3 mr-1" />
                Verified Purchase
              </Badge>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            <ReviewStars rating={review.rating} />
            <span className="text-sm text-gray-500">{formatDate(review.createdAt)}</span>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-1">{review.title}</h4>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">{review.comment}</p>
          </div>
          
          <div className="flex items-center gap-4 pt-2">
            <span className="text-sm text-gray-500">Was this helpful?</span>
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                className={cn(
                  "text-xs",
                  userVote === 'helpful' && "text-green-600 bg-green-50"
                )}
                onClick={() => handleVote('helpful')}
                disabled={userVote !== null}
              >
                <ThumbsUp className="h-3 w-3 mr-1" />
                Yes ({helpfulVotes.helpful})
              </Button>
              <Button
                variant="ghost"
                size="sm"
                className={cn(
                  "text-xs",
                  userVote === 'not-helpful' && "text-red-600 bg-red-50"
                )}
                onClick={() => handleVote('not-helpful')}
                disabled={userVote !== null}
              >
                <ThumbsDown className="h-3 w-3 mr-1" />
                No ({helpfulVotes.notHelpful})
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function WriteReviewForm({ productId }: { productId: string }) {
  const [isOpen, setIsOpen] = useState(false)
  const [rating, setRating] = useState(0)
  const [hoveredRating, setHoveredRating] = useState(0)
  const [title, setTitle] = useState('')
  const [comment, setComment] = useState('')
  const [name, setName] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (rating === 0 || !title.trim() || !comment.trim() || !name.trim()) return
    
    setIsSubmitting(true)
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Reset form
      setRating(0)
      setTitle('')
      setComment('')
      setName('')
      setIsOpen(false)
      
      // In a real implementation, you'd refresh the reviews list
      console.log('Review submitted:', { productId, rating, title, comment, name })
    } catch (error) {
      console.error('Failed to submit review:', error)
    } finally {
      setIsSubmitting(false)
    }
  }
  
  if (!isOpen) {
    return (
      <Button 
        onClick={() => setIsOpen(true)}
        className="bg-red-600 hover:bg-red-700"
      >
        <MessageSquare className="h-4 w-4 mr-2" />
        Write a Review
      </Button>
    )
  }
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>Write a Review</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label>Rating *</Label>
            <div className="flex items-center gap-1 mt-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  className="p-1"
                  onMouseEnter={() => setHoveredRating(star)}
                  onMouseLeave={() => setHoveredRating(0)}
                  onClick={() => setRating(star)}
                >
                  <Star
                    className={cn(
                      "h-6 w-6 transition-colors",
                      star <= (hoveredRating || rating) 
                        ? "text-yellow-400 fill-current" 
                        : "text-gray-300 hover:text-yellow-200"
                    )}
                  />
                </button>
              ))}
            </div>
          </div>
          
          <div>
            <Label htmlFor="name">Name *</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your name"
              required
            />
          </div>
          
          <div>
            <Label htmlFor="title">Review Title *</Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Summarize your experience"
              required
            />
          </div>
          
          <div>
            <Label htmlFor="comment">Review *</Label>
            <Textarea
              id="comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Tell us about your experience with this product"
              rows={4}
              required
            />
          </div>
          
          <div className="flex gap-3">
            <Button 
              type="submit" 
              disabled={isSubmitting || rating === 0 || !title.trim() || !comment.trim() || !name.trim()}
              className="bg-red-600 hover:bg-red-700"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Review'}
            </Button>
            <Button 
              type="button" 
              variant="outline" 
              onClick={() => setIsOpen(false)}
            >
              Cancel
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export function ProductReviews({ productId, rating, reviewCount, className }: ProductReviewsProps) {
  const [reviews, setReviews] = useState<Review[]>(mockReviews)
  const [sortBy, setSortBy] = useState<'recent' | 'helpful' | 'rating'>('recent')
  const [filterRating, setFilterRating] = useState<number | null>(null)
  
  // Calculate rating distribution
  const ratingDistribution = [5, 4, 3, 2, 1].map(stars => {
    const count = reviews.filter(review => review.rating === stars).length
    const percentage = reviewCount > 0 ? (count / reviewCount) * 100 : 0
    return { stars, count, percentage }
  })
  
  // Sort and filter reviews
  const filteredAndSortedReviews = reviews
    .filter(review => filterRating ? review.rating === filterRating : true)
    .sort((a, b) => {
      switch (sortBy) {
        case 'helpful':
          return b.helpful - a.helpful
        case 'rating':
          return b.rating - a.rating
        case 'recent':
        default:
          return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      }
    })
  
  return (
    <div className={cn("space-y-6", className)}>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <MessageSquare className="h-5 w-5" />
            Customer Reviews
          </CardTitle>
        </CardHeader>
        <CardContent>
          {/* Rating Summary */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="text-center">
              <div className="text-4xl font-bold text-gray-900 dark:text-white mb-2">{rating}</div>
              <ReviewStars rating={rating} size="lg" />
              <p className="text-sm text-gray-500 mt-1">Based on {reviewCount.toLocaleString()} reviews</p>
            </div>
            
            <div className="space-y-2">
              {ratingDistribution.map(({ stars, count, percentage }) => (
                <div key={stars} className="flex items-center gap-3 text-sm">
                  <button
                    onClick={() => setFilterRating(filterRating === stars ? null : stars)}
                    className={cn(
                      "flex items-center gap-1 hover:text-red-600 transition-colors",
                      filterRating === stars && "text-red-600 font-medium"
                    )}
                  >
                    <span>{stars}</span>
                    <Star className="h-3 w-3 text-yellow-400 fill-current" />
                  </button>
                  <Progress value={percentage} className="flex-1 h-2" />
                  <span className="text-gray-500 w-8">{count}</span>
                </div>
              ))}
            </div>
          </div>
          
          <Separator className="my-6" />
          
          {/* Review Controls */}
          <div className="flex flex-col sm:flex-row justify-between gap-4 mb-6">
            <div className="flex items-center gap-4">
              <span className="text-sm font-medium">Sort by:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <option value="recent">Most Recent</option>
                <option value="helpful">Most Helpful</option>
                <option value="rating">Highest Rating</option>
              </select>
              
              {filterRating && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setFilterRating(null)}
                >
                  Clear Filter
                </Button>
              )}
            </div>
            
            <WriteReviewForm productId={productId} />
          </div>
          
          {/* Reviews List */}
          <div className="space-y-6">
            {filteredAndSortedReviews.length > 0 ? (
              filteredAndSortedReviews.map((review, index) => (
                <div key={review.id}>
                  <ReviewItem review={review} />
                  {index < filteredAndSortedReviews.length - 1 && (
                    <Separator className="mt-6" />
                  )}
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                {filterRating ? (
                  <p>No reviews found for {filterRating} star rating.</p>
                ) : (
                  <p>No reviews yet. Be the first to review this product!</p>
                )}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}