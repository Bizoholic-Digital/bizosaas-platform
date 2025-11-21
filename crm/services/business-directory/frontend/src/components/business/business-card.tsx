'use client'

import React from 'react'
import Link from 'next/link'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  Star, 
  MapPin, 
  Phone, 
  Globe, 
  Heart,
  Eye,
  Verified,
  Crown,
  Clock,
  ArrowRight
} from 'lucide-react'
import { BusinessListing } from '@/types'
import { 
  formatRating, 
  formatReviewCount, 
  formatPhoneNumber,
  formatAddress,
  generateStars,
  isBusinessOpen,
  formatBusinessHours,
  truncateText,
  cn
} from '@/lib/utils'

interface BusinessCardProps {
  business: BusinessListing
  showFullDetails?: boolean
  showActions?: boolean
  className?: string
  variant?: 'default' | 'compact' | 'featured'
}

const BusinessCard = ({ 
  business, 
  showFullDetails = false, 
  showActions = true, 
  className,
  variant = 'default'
}: BusinessCardProps) => {
  const { full, half, empty } = generateStars(business.rating)
  const isOpen = isBusinessOpen(business.hours)
  
  const cardContent = (
    <CardContent className="p-0">
      {/* Business Image */}
      <div className="relative">
        <div className="aspect-video bg-gradient-to-br from-gray-100 to-gray-200 rounded-t-lg flex items-center justify-center">
          {business.images && business.images.length > 0 ? (
            <img
              src={business.images[0]}
              alt={business.name}
              className="w-full h-full object-cover rounded-t-lg"
            />
          ) : (
            <div className="text-gray-400 text-4xl font-bold">
              {business.name.charAt(0)}
            </div>
          )}
        </div>
        
        {/* Badges */}
        <div className="absolute top-3 left-3 flex flex-wrap gap-1">
          {business.verification_status === 'verified' && (
            <Badge variant="success" className="text-xs">
              <Verified className="w-3 h-3 mr-1" />
              Verified
            </Badge>
          )}
          {business.premium_status === 'premium' && (
            <Badge variant="warning" className="text-xs">
              <Crown className="w-3 h-3 mr-1" />
              Premium
            </Badge>
          )}
          {business.ai_enhanced && (
            <Badge variant="info" className="text-xs">
              AI Enhanced
            </Badge>
          )}
        </div>

        {/* Heart Icon */}
        {showActions && (
          <button className="absolute top-3 right-3 p-2 bg-white/90 hover:bg-white rounded-full shadow-md transition-colors">
            <Heart className="w-4 h-4 text-gray-600 hover:text-red-500" />
          </button>
        )}

        {/* Open/Closed Status */}
        <div className="absolute bottom-3 right-3">
          <Badge variant={isOpen ? "success" : "destructive"} className="text-xs">
            <Clock className="w-3 h-3 mr-1" />
            {isOpen ? "Open" : "Closed"}
          </Badge>
        </div>
      </div>

      {/* Business Details */}
      <div className="p-4 space-y-3">
        {/* Header */}
        <div className="space-y-1">
          <h3 className="font-semibold text-lg text-gray-900 line-clamp-1">
            {business.name}
          </h3>
          <p className="text-sm text-bizbook-primary font-medium">
            {business.category}
          </p>
        </div>

        {/* Rating & Reviews */}
        <div className="flex items-center space-x-2">
          <div className="flex items-center">
            {[...Array(full)].map((_, i) => (
              <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
            ))}
            {half && <Star className="w-4 h-4 fill-yellow-400/50 text-yellow-400" />}
            {[...Array(empty)].map((_, i) => (
              <Star key={i} className="w-4 h-4 text-gray-300" />
            ))}
          </div>
          <span className="text-sm font-medium text-gray-900">
            {formatRating(business.rating)}
          </span>
          <span className="text-sm text-gray-500">
            ({formatReviewCount(business.review_count)})
          </span>
        </div>

        {/* Description */}
        <p className="text-sm text-gray-600 line-clamp-2">
          {truncateText(business.description, 100)}
        </p>

        {/* Location */}
        <div className="flex items-start space-x-2 text-sm text-gray-600">
          <MapPin className="w-4 h-4 mt-0.5 flex-shrink-0" />
          <span className="line-clamp-1">
            {formatAddress(
              business.address, 
              business.location?.city, 
              business.location?.state
            )}
          </span>
        </div>

        {/* Contact Info */}
        {showFullDetails && (
          <div className="space-y-2 pt-2 border-t">
            {business.phone && (
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Phone className="w-4 h-4" />
                <span>{formatPhoneNumber(business.phone)}</span>
              </div>
            )}
            {business.website && (
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Globe className="w-4 h-4" />
                <span className="truncate">{business.website}</span>
              </div>
            )}
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Clock className="w-4 h-4" />
              <span>{formatBusinessHours(business.hours)}</span>
            </div>
          </div>
        )}

        {/* Features */}
        {business.features && business.features.length > 0 && (
          <div className="flex flex-wrap gap-1 pt-2">
            {business.features.slice(0, 3).map((feature, index) => (
              <Badge key={index} variant="outline" className="text-xs">
                {feature}
              </Badge>
            ))}
            {business.features.length > 3 && (
              <Badge variant="outline" className="text-xs">
                +{business.features.length - 3} more
              </Badge>
            )}
          </div>
        )}

        {/* Action Buttons */}
        {showActions && (
          <div className="flex space-x-2 pt-3">
            <Button size="sm" className="flex-1" asChild>
              <Link href={`/business/${business.business_id}`}>
                <Eye className="w-4 h-4 mr-1" />
                View Details
              </Link>
            </Button>
            {business.website && (
              <Button variant="outline" size="sm" asChild>
                <a 
                  href={business.website} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center"
                >
                  <Globe className="w-4 h-4 mr-1" />
                  Website
                </a>
              </Button>
            )}
          </div>
        )}
      </div>
    </CardContent>
  )

  if (variant === 'compact') {
    return (
      <Card className={cn("hover:shadow-lg transition-shadow cursor-pointer", className)}>
        <Link href={`/business/${business.business_id}`}>
          <div className="p-4 flex items-center space-x-4">
            <div className="w-16 h-16 bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg flex items-center justify-center flex-shrink-0">
              {business.images && business.images.length > 0 ? (
                <img
                  src={business.images[0]}
                  alt={business.name}
                  className="w-full h-full object-cover rounded-lg"
                />
              ) : (
                <div className="text-gray-400 text-xl font-bold">
                  {business.name.charAt(0)}
                </div>
              )}
            </div>
            <div className="flex-1 min-w-0 space-y-1">
              <h3 className="font-medium text-gray-900 truncate">{business.name}</h3>
              <p className="text-sm text-bizbook-primary">{business.category}</p>
              <div className="flex items-center space-x-2">
                <div className="flex items-center">
                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  <span className="text-sm font-medium text-gray-900 ml-1">
                    {formatRating(business.rating)}
                  </span>
                </div>
                <span className="text-sm text-gray-500">
                  ({business.review_count})
                </span>
              </div>
            </div>
            <ArrowRight className="w-5 h-5 text-gray-400" />
          </div>
        </Link>
      </Card>
    )
  }

  if (variant === 'featured') {
    return (
      <Card className={cn("overflow-hidden shadow-lg hover:shadow-xl transition-shadow", className)}>
        <Link href={`/business/${business.business_id}`}>
          {cardContent}
        </Link>
      </Card>
    )
  }

  return (
    <Card className={cn("overflow-hidden card-hover", className)}>
      <Link href={`/business/${business.business_id}`}>
        {cardContent}
      </Link>
    </Card>
  )
}

export default BusinessCard