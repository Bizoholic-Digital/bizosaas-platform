'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { 
  Star, 
  MapPin, 
  Phone, 
  Mail, 
  ExternalLink, 
  Clock,
  Share,
  Heart,
  Navigation,
  Camera,
  MessageCircle
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { businessAPI } from '@/lib/api';
import { Business, Review } from '@/types/business';
import { cn, formatRating, formatPhoneNumber, isBusinessOpen, generateStars } from '@/lib/utils';

export default function BusinessDetailPage() {
  const params = useParams();
  const businessId = params.id as string;
  const [business, setBusiness] = useState<Business | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'reviews' | 'photos'>('overview');

  useEffect(() => {
    const loadBusinessData = async () => {
      try {
        const [businessData, reviewsData] = await Promise.all([
          businessAPI.getBusiness(businessId),
          businessAPI.getBusinessReviews(businessId)
        ]);
        
        setBusiness(businessData);
        setReviews(reviewsData);
      } catch (error) {
        console.error('Error loading business data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (businessId) {
      loadBusinessData();
    }
  }, [businessId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading business details...</p>
        </div>
      </div>
    );
  }

  if (!business) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Business Not Found
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            The business you're looking for doesn't exist or has been removed.
          </p>
          <Button asChild>
            <Link href="/">Back to Directory</Link>
          </Button>
        </div>
      </div>
    );
  }

  const isOpen = isBusinessOpen(business.hours);
  const stars = generateStars(business.rating);

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative h-64 md:h-96 overflow-hidden">
        <Image
          src={(business.images && business.images[0]) || '/placeholder-business.jpg'}
          alt={business.name}
          fill
          className="object-cover"
          priority
        />
        <div className="absolute inset-0 bg-black/40" />
        <div className="absolute bottom-0 left-0 right-0 p-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-end justify-between text-white">
              <div>
                <h1 className="text-3xl md:text-4xl font-bold mb-2">
                  {business.name}
                </h1>
                <div className="flex items-center space-x-4 text-sm md:text-base">
                  <div className="flex items-center">
                    <div className="rating-stars mr-2">
                      {stars.map((star, index) => (
                        <Star
                          key={index}
                          className={cn(
                            "rating-star",
                            star.filled ? "filled" : "empty"
                          )}
                        />
                      ))}
                    </div>
                    <span>{formatRating(business.rating)} ({business.reviewCount} reviews)</span>
                  </div>
                  <span className="text-sm">•</span>
                  <span>{business.category.name}</span>
                  <span className="text-sm">•</span>
                  <span className={cn(
                    isOpen ? 'text-green-300' : 'text-red-300'
                  )}>
                    {isOpen ? 'Open now' : 'Closed'}
                  </span>
                </div>
              </div>
              <div className="flex space-x-2">
                <Button variant="secondary" size="sm">
                  <Heart className="w-4 h-4 mr-2" />
                  Save
                </Button>
                <Button variant="secondary" size="sm">
                  <Share className="w-4 h-4 mr-2" />
                  Share
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Tabs */}
            <div className="border-b border-gray-200 dark:border-gray-700">
              <nav className="-mb-px flex space-x-8">
                {[
                  { id: 'overview', label: 'Overview' },
                  { id: 'reviews', label: `Reviews (${business.reviewCount})` },
                  { id: 'photos', label: `Photos (${business.images.length})` }
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={cn(
                      "whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm",
                      activeTab === tab.id
                        ? "border-primary text-primary"
                        : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300"
                    )}
                  >
                    {tab.label}
                  </button>
                ))}
              </nav>
            </div>

            {/* Tab Content */}
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* Description */}
                <Card>
                  <CardHeader>
                    <CardTitle>About {business.name}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                      {business.description}
                    </p>
                    
                    {/* Tags */}
                    <div className="flex flex-wrap gap-2 mt-4">
                      {(business.tags || []).map((tag) => (
                        <span key={tag} className="filter-badge">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Amenities */}
                {business.amenities && business.amenities.length > 0 && (
                  <Card>
                    <CardHeader>
                      <CardTitle>Amenities</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {business.amenities.map((amenity) => (
                          <div key={amenity} className="flex items-center text-sm">
                            <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                            {amenity}
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Hours */}
                <Card>
                  <CardHeader>
                    <CardTitle>Hours</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {business.hours ? Object.entries(business.hours).map(([day, hours]) => (
                        <div key={day} className="flex justify-between text-sm">
                          <span className="capitalize font-medium">
                            {day}
                          </span>
                          <span className={cn(
                            hours.closed ? 'text-red-600 dark:text-red-400' : 'text-gray-600 dark:text-gray-400'
                          )}>
                            {hours.closed ? 'Closed' : `${hours.open} - ${hours.close}`}
                          </span>
                        </div>
                      )) : (
                        <div className="text-center text-gray-500 dark:text-gray-400 py-4">
                          Hours not available
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {activeTab === 'reviews' && (
              <div className="space-y-6">
                {/* Review Stats */}
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold">Customer Reviews</h3>
                      <Button>
                        <MessageCircle className="w-4 h-4 mr-2" />
                        Write Review
                      </Button>
                    </div>
                    <div className="flex items-center space-x-6">
                      <div className="text-center">
                        <div className="text-3xl font-bold text-primary">
                          {formatRating(business.rating)}
                        </div>
                        <div className="rating-stars justify-center mb-1">
                          {stars.map((star, index) => (
                            <Star
                              key={index}
                              className={cn(
                                "rating-star",
                                star.filled ? "filled" : "empty"
                              )}
                            />
                          ))}
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          {business.reviewCount} reviews
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Reviews List */}
                <div className="space-y-4">
                  {reviews.map((review) => (
                    <Card key={review.id} className="review-card">
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <div className="font-medium text-gray-900 dark:text-white">
                              {review.authorName}
                            </div>
                            <div className="flex items-center mt-1">
                              <div className="rating-stars mr-2">
                                {generateStars(review.rating).map((star, index) => (
                                  <Star
                                    key={index}
                                    className={cn(
                                      "rating-star w-3 h-3",
                                      star.filled ? "filled" : "empty"
                                    )}
                                  />
                                ))}
                              </div>
                              <span className="text-sm text-gray-600 dark:text-gray-400">
                                {new Date(review.createdAt).toLocaleDateString()}
                              </span>
                            </div>
                          </div>
                          {review.verified && (
                            <span className="business-status verified text-xs">
                              Verified
                            </span>
                          )}
                        </div>
                        
                        {review.title && (
                          <h4 className="font-medium mb-2">{review.title}</h4>
                        )}
                        
                        <p className="text-gray-600 dark:text-gray-400 mb-3">
                          {review.content}
                        </p>
                        
                        {review.helpful > 0 && (
                          <div className="text-sm text-gray-500 dark:text-gray-500">
                            {review.helpful} people found this helpful
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'photos' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Photos</h3>
                  <Button>
                    <Camera className="w-4 h-4 mr-2" />
                    Add Photos
                  </Button>
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {business.images.map((image, index) => (
                    <div key={index} className="relative aspect-square overflow-hidden rounded-lg">
                      <Image
                        src={image}
                        alt={`${business.name} photo ${index + 1}`}
                        fill
                        className="object-cover hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Contact Info */}
            <Card>
              <CardHeader>
                <CardTitle>Contact Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center">
                  <Phone className="w-5 h-5 text-gray-400 mr-3" />
                  <a
                    href={`tel:${business.contact?.phone}`}
                    className="text-primary hover:underline"
                  >
                    {formatPhoneNumber(business.contact?.phone || '')}
                  </a>
                </div>
                
                {business.contact?.email && (
                  <div className="flex items-center">
                    <Mail className="w-5 h-5 text-gray-400 mr-3" />
                    <a
                      href={`mailto:${business.contact?.email}`}
                      className="text-primary hover:underline"
                    >
                      {business.contact?.email}
                    </a>
                  </div>
                )}
                
                {business.contact?.website && (
                  <div className="flex items-center">
                    <ExternalLink className="w-5 h-5 text-gray-400 mr-3" />
                    <a
                      href={business.contact?.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:underline"
                    >
                      Visit Website
                    </a>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Location */}
            <Card>
              <CardHeader>
                <CardTitle>Location</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start">
                  <MapPin className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
                  <div>
                    <div className="text-sm text-gray-900 dark:text-white">
                      {business.location?.address || 'Address not available'}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      {business.location?.city || 'City not available'}, {business.location?.state || 'State not available'} {business.location?.zipCode || ''}
                    </div>
                  </div>
                </div>
                
                <div className="map-container">
                  <div className="text-gray-500 dark:text-gray-400">
                    <MapPin className="w-8 h-8 mx-auto mb-2" />
                    <p className="text-sm">Interactive map coming soon</p>
                  </div>
                </div>
                
                <Button className="w-full">
                  <Navigation className="w-4 h-4 mr-2" />
                  Get Directions
                </Button>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardContent className="p-6">
                <div className="space-y-3">
                  <Button className="w-full" size="lg">
                    <Phone className="w-4 h-4 mr-2" />
                    Call Now
                  </Button>
                  <Button variant="outline" className="w-full">
                    <MessageCircle className="w-4 h-4 mr-2" />
                    Write Review
                  </Button>
                  <Button variant="outline" className="w-full">
                    <Share className="w-4 h-4 mr-2" />
                    Share Business
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}