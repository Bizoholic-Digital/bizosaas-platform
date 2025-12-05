"use client"

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import {
  ThumbsUp, ThumbsDown, Star, MessageSquare, Bug, Lightbulb,
  Send, CheckCircle, AlertCircle, Clock
} from 'lucide-react'
import { UserFeedback } from '@/lib/conversation-analytics'

interface FeedbackWidgetProps {
  conversationId?: string
  messageId?: string
  messageContent?: string
  aiResponse?: string
  onSubmitFeedback?: (feedback: Omit<UserFeedback, 'id' | 'timestamp' | 'resolved' | 'priority' | 'tenantId' | 'userId'>) => Promise<boolean>
  className?: string
}

export function FeedbackWidget({ 
  conversationId, 
  messageId, 
  messageContent, 
  aiResponse,
  onSubmitFeedback,
  className = "" 
}: FeedbackWidgetProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [feedbackType, setFeedbackType] = useState<UserFeedback['type']>('satisfaction')
  const [rating, setRating] = useState<number>(0)
  const [comment, setComment] = useState('')
  const [category, setCategory] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  const feedbackTypes = [
    { value: 'satisfaction', label: 'Overall Satisfaction', icon: Star, color: 'text-yellow-500' },
    { value: 'quality', label: 'Response Quality', icon: MessageSquare, color: 'text-blue-500' },
    { value: 'helpfulness', label: 'Helpfulness', icon: ThumbsUp, color: 'text-green-500' },
    { value: 'accuracy', label: 'Accuracy', icon: CheckCircle, color: 'text-emerald-500' },
    { value: 'speed', label: 'Response Speed', icon: Clock, color: 'text-orange-500' },
    { value: 'bug_report', label: 'Bug Report', icon: Bug, color: 'text-red-500' },
    { value: 'feature_request', label: 'Feature Request', icon: Lightbulb, color: 'text-purple-500' }
  ] as const

  const categories = [
    'General',
    'Command Processing',
    'Voice Interface',
    'Document Processing',
    'Analytics',
    'User Management',
    'Workflow Creation',
    'AI Agents',
    'Platform Integration',
    'Performance',
    'User Experience',
    'Mobile Interface'
  ]

  const handleQuickFeedback = async (type: 'positive' | 'negative') => {
    const quickRating = type === 'positive' ? 5 : 2
    const quickFeedback = {
      conversationId: conversationId || '',
      messageId,
      type: 'satisfaction' as const,
      rating: quickRating,
      category: 'General',
      context: {
        userMessage: messageContent,
        aiResponse: aiResponse
      }
    }

    if (onSubmitFeedback) {
      const success = await onSubmitFeedback(quickFeedback)
      if (success) {
        setSubmitted(true)
        setTimeout(() => setSubmitted(false), 3000)
      }
    }
  }

  const handleDetailedSubmit = async () => {
    if (!onSubmitFeedback || rating === 0 || !category) return

    setIsSubmitting(true)

    const feedback = {
      conversationId: conversationId || '',
      messageId,
      type: feedbackType,
      rating,
      comment: comment.trim() || undefined,
      category,
      context: {
        userMessage: messageContent,
        aiResponse: aiResponse,
        responseTime: undefined // Could be passed as prop
      }
    }

    try {
      const success = await onSubmitFeedback(feedback)
      if (success) {
        setSubmitted(true)
        setIsOpen(false)
        // Reset form
        setRating(0)
        setComment('')
        setFeedbackType('satisfaction')
        setCategory('')
      }
    } catch (error) {
      console.error('Failed to submit feedback:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const selectedFeedbackType = feedbackTypes.find(type => type.value === feedbackType)

  if (submitted) {
    return (
      <div className={`flex items-center space-x-2 text-green-600 ${className}`}>
        <CheckCircle className="w-4 h-4" />
        <span className="text-sm">Thank you for your feedback!</span>
      </div>
    )
  }

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      {/* Quick Feedback Buttons */}
      <div className="flex items-center space-x-1">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => handleQuickFeedback('positive')}
          className="h-7 px-2 hover:bg-green-50 hover:text-green-600"
        >
          <ThumbsUp className="w-3 h-3" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => handleQuickFeedback('negative')}
          className="h-7 px-2 hover:bg-red-50 hover:text-red-600"
        >
          <ThumbsDown className="w-3 h-3" />
        </Button>
      </div>

      {/* Detailed Feedback Dialog */}
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>
          <Button variant="ghost" size="sm" className="h-7 px-2 text-muted-foreground">
            <MessageSquare className="w-3 h-3 mr-1" />
            Feedback
          </Button>
        </DialogTrigger>
        
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center space-x-2">
              <MessageSquare className="w-5 h-5" />
              <span>Provide Feedback</span>
            </DialogTitle>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* Feedback Type Selection */}
            <div className="space-y-2">
              <Label>Feedback Type</Label>
              <Select value={feedbackType} onValueChange={(value: UserFeedback['type']) => setFeedbackType(value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {feedbackTypes.map((type) => {
                    const Icon = type.icon
                    return (
                      <SelectItem key={type.value} value={type.value}>
                        <div className="flex items-center space-x-2">
                          <Icon className={`w-4 h-4 ${type.color}`} />
                          <span>{type.label}</span>
                        </div>
                      </SelectItem>
                    )
                  })}
                </SelectContent>
              </Select>
            </div>

            {/* Rating */}
            <div className="space-y-2">
              <Label>Rating</Label>
              <div className="flex items-center space-x-1">
                {[1, 2, 3, 4, 5].map((star) => (
                  <Button
                    key={star}
                    variant="ghost"
                    size="sm"
                    onClick={() => setRating(star)}
                    className="p-1 h-auto"
                  >
                    <Star
                      className={`w-5 h-5 ${
                        star <= rating ? 'text-yellow-500 fill-current' : 'text-gray-300'
                      }`}
                    />
                  </Button>
                ))}
                <span className="ml-2 text-sm text-muted-foreground">
                  {rating > 0 && (
                    <Badge variant="outline">
                      {rating === 1 && 'Very Poor'}
                      {rating === 2 && 'Poor'}
                      {rating === 3 && 'Average'}
                      {rating === 4 && 'Good'}
                      {rating === 5 && 'Excellent'}
                    </Badge>
                  )}
                </span>
              </div>
            </div>

            {/* Category */}
            <div className="space-y-2">
              <Label>Category</Label>
              <Select value={category} onValueChange={setCategory}>
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((cat) => (
                    <SelectItem key={cat} value={cat}>
                      {cat}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Comment */}
            <div className="space-y-2">
              <Label>Additional Comments (Optional)</Label>
              <Textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Share your thoughts, suggestions, or describe any issues..."
                rows={3}
              />
              <div className="text-xs text-muted-foreground">
                {comment.length}/500 characters
              </div>
            </div>

            {/* Context Preview */}
            {(messageContent || aiResponse) && (
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Context</CardTitle>
                </CardHeader>
                <CardContent className="text-xs space-y-2">
                  {messageContent && (
                    <div>
                      <Label className="font-medium">Your Message:</Label>
                      <div className="text-muted-foreground truncate">
                        {messageContent.length > 100 ? `${messageContent.substring(0, 100)}...` : messageContent}
                      </div>
                    </div>
                  )}
                  {aiResponse && (
                    <div>
                      <Label className="font-medium">AI Response:</Label>
                      <div className="text-muted-foreground truncate">
                        {aiResponse.length > 100 ? `${aiResponse.substring(0, 100)}...` : aiResponse}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Submit Button */}
            <div className="flex items-center justify-between pt-2">
              <Button variant="outline" onClick={() => setIsOpen(false)}>
                Cancel
              </Button>
              <Button
                onClick={handleDetailedSubmit}
                disabled={rating === 0 || !category || isSubmitting}
              >
                {isSubmitting ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
                    <span>Submitting...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <Send className="w-4 h-4" />
                    <span>Submit Feedback</span>
                  </div>
                )}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}