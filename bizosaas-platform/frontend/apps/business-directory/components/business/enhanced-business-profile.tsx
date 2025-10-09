'use client';

import React, { useState, useEffect } from 'react';
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
  Directions,
  Camera,
  MessageCircle,
  Calendar,
  ShoppingBag,
  Tag,
  ThumbsUp,
  Flag,
  Copy,
  Facebook,
  Twitter,
  Instagram,
  MoreHorizontal
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { InteractiveMap } from '@/components/map/interactive-map';
import { Business, Review, BusinessEvent, BusinessProduct, BusinessCoupon } from '@/types/business';
import { businessAPI } from '@/lib/api';
import { cn, formatRating, formatPhoneNumber, isBusinessOpen, generateStars } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

interface EnhancedBusinessProfileProps {
  business: Business;
  className?: string;
}

export function EnhancedBusinessProfile({ business, className }: EnhancedBusinessProfileProps) {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [events, setEvents] = useState<BusinessEvent[]>([]);
  const [products, setProducts] = useState<BusinessProduct[]>([]);
  const [coupons, setCoupons] = useState<BusinessCoupon[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeImageIndex, setActiveImageIndex] = useState(0);
  const [showAllPhotos, setShowAllPhotos] = useState(false);
  const [showShareMenu, setShowShareMenu] = useState(false);
  const [isFavorited, setIsFavorited] = useState(false);

  const isOpen = isBusinessOpen(business.hours);
  const stars = generateStars(business.rating);

  useEffect(() => {
    const loadAdditionalData = async () => {
      setLoading(true);
      try {
        const [reviewsData, eventsData, productsData, couponsData] = await Promise.all([
          businessAPI.getBusinessReviews(business.id),
          businessAPI.getBusinessEvents(business.id),
          businessAPI.getBusinessProducts(business.id),
          businessAPI.getBusinessCoupons(business.id)
        ]);
        
        setReviews(reviewsData);
        setEvents(eventsData);
        setProducts(productsData);
        setCoupons(couponsData);
      } catch (error) {
        console.error('Error loading additional business data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadAdditionalData();
  }, [business.id]);

  const handleShare = (platform?: string) => {
    const url = window.location.href;
    const text = `Check out ${business.name} on BizDirectory`;
    
    switch (platform) {
      case 'facebook':
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`);
        break;
      case 'twitter':
        window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`);
        break;
      case 'copy':
        navigator.clipboard.writeText(url);
        // Show toast notification
        break;
      default:
        setShowShareMenu(!showShareMenu);
    }
  };

  const handleCallBusiness = () => {
    if (business.contact?.phone) {
      window.open(`tel:${business.contact.phone}`);
    }
  };

  const handleGetDirections = () => {
    if (business.location?.coordinates) {
      const { lat, lng } = business.location.coordinates;
      window.open(`https://maps.google.com/maps?daddr=${lat},${lng}`, '_blank');
    }
  };

  return (
    <div className={cn("space-y-8", className)}>
      {/* Hero Section with Image Gallery */}
      <div className="relative">
        <div className="relative h-96 lg:h-[500px] overflow-hidden rounded-xl">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeImageIndex}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="absolute inset-0"
            >
              <Image
                src={(business.images && business.images[activeImageIndex]) || '/placeholder-business.jpg'}
                alt={`${business.name} - Image ${activeImageIndex + 1}`}
                fill
                className="object-cover"
                priority
              />
            </motion.div>
          </AnimatePresence>
          
          {/* Image Navigation */}
          {business.images.length > 1 && (
            <>
              <button
                onClick={() => setActiveImageIndex(Math.max(0, activeImageIndex - 1))}
                className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-black/50 text-white p-2 rounded-full hover:bg-black/70 transition-colors"
                disabled={activeImageIndex === 0}
              >
                ←
              </button>
              <button
                onClick={() => setActiveImageIndex(Math.min(business.images.length - 1, activeImageIndex + 1))}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-black/50 text-white p-2 rounded-full hover:bg-black/70 transition-colors"
                disabled={activeImageIndex === business.images.length - 1}
              >
                →
              </button>
              
              {/* Image Indicators */}
              <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
                {business.images.map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setActiveImageIndex(index)}
                    className={cn(
                      "w-2 h-2 rounded-full transition-colors",
                      index === activeImageIndex ? "bg-white" : "bg-white/50"
                    )}
                  />
                ))}
              </div>
            </>
          )}
          
          {/* Action Buttons */}
          <div className="absolute top-4 right-4 flex space-x-2">
            <Button
              onClick={() => setIsFavorited(!isFavorited)}
              variant="secondary"
              size="sm"
              className="bg-white/90 hover:bg-white"
            >
              <Heart className={cn("w-4 h-4", isFavorited ? "fill-red-500 text-red-500" : "")} />
            </Button>
            
            <div className="relative">
              <Button
                onClick={() => handleShare()}
                variant="secondary"
                size="sm"
                className="bg-white/90 hover:bg-white"
              >
                <Share className="w-4 h-4" />
              </Button>
              
              {showShareMenu && (
                <div className="absolute top-full right-0 mt-2 bg-white rounded-lg shadow-lg border p-2 z-10">
                  <div className="flex flex-col space-y-1">
                    <Button
                      onClick={() => handleShare('facebook')}
                      variant="ghost"
                      size="sm"
                      className="justify-start"
                    >
                      <Facebook className="w-4 h-4 mr-2" />
                      Facebook
                    </Button>
                    <Button
                      onClick={() => handleShare('twitter')}
                      variant="ghost"
                      size="sm"
                      className="justify-start"
                    >
                      <Twitter className="w-4 h-4 mr-2" />
                      Twitter
                    </Button>
                    <Button
                      onClick={() => handleShare('copy')}
                      variant="ghost"
                      size="sm"
                      className="justify-start"
                    >
                      <Copy className="w-4 h-4 mr-2" />
                      Copy Link
                    </Button>
                  </div>
                </div>
              )}
            </div>
            
            <Button
              onClick={() => setShowAllPhotos(true)}
              variant="secondary"
              size="sm"
              className="bg-white/90 hover:bg-white"
            >
              <Camera className="w-4 h-4 mr-1" />
              {business.images.length}
            </Button>
          </div>
          
          {/* Status Badges */}
          <div className="absolute top-4 left-4 flex flex-col space-y-2">
            {business.featured && (
              <Badge className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white">
                Featured
              </Badge>
            )}
            {business.verified && (
              <Badge className="bg-blue-500 text-white">
                ✓ Verified
              </Badge>
            )}
            <Badge className={cn(
              isOpen ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
            )}>
              {isOpen ? 'Open Now' : 'Closed'}
            </Badge>
          </div>
        </div>
        
        {/* Photo Grid Preview */}
        {business.images.length > 1 && (
          <div className="grid grid-cols-4 gap-2 mt-4">
            {business.images.slice(0, 4).map((image, index) => (
              <button
                key={index}
                onClick={() => setActiveImageIndex(index)}
                className={cn(
                  "relative aspect-square overflow-hidden rounded-lg border-2 transition-all",
                  index === activeImageIndex 
                    ? "border-primary ring-2 ring-primary/20" 
                    : "border-gray-200 hover:border-gray-300"
                )}
              >
                <Image
                  src={image}
                  alt={`${business.name} thumbnail ${index + 1}`}
                  fill
                  className="object-cover"
                />
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Business Header */}
      <div className="space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
          <div className="space-y-2">
            <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white">
              {business.name}
            </h1>
            
            <div className="flex flex-wrap items-center gap-4 text-gray-600 dark:text-gray-400">
              <div className="flex items-center">
                <div className="rating-stars mr-2">
                  {stars.map((star, index) => (
                    <Star
                      key={index}
                      className={cn(
                        "rating-star w-5 h-5",
                        star.filled ? "filled text-yellow-400" : "empty text-gray-300"
                      )}
                    />
                  ))}
                </div>
                <span className="font-medium">{formatRating(business.rating)}</span>
                <span className="text-gray-500 ml-1">({business.reviewCount} reviews)</span>
              </div>
              
              <span>•</span>
              <span>{business.category.name}</span>
              <span>•</span>
              <span className="pricing-display">{business.pricing?.range || 'Price not available'}</span>
            </div>
            
            <p className="text-gray-700 dark:text-gray-300 max-w-3xl">
              {business.description}
            </p>
            
            {/* Tags */}
            <div className="flex flex-wrap gap-2">
              {(business.tags || []).map((tag) => (
                <Badge key={tag} variant="outline" className="text-xs">
                  {tag}
                </Badge>
              ))}
            </div>
          </div>
          
          {/* Quick Actions */}
          <div className="flex flex-col space-y-2 lg:w-48">
            <Button onClick={handleCallBusiness} size="lg" className="w-full">
              <Phone className="w-4 h-4 mr-2" />
              Call Now
            </Button>
            <Button onClick={handleGetDirections} variant="outline" className="w-full">
              <Directions className="w-4 h-4 mr-2" />
              Get Directions
            </Button>
            <Button variant="outline" className="w-full">
              <MessageCircle className="w-4 h-4 mr-2" />
              Write Review
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5 lg:grid-cols-6">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="reviews">Reviews ({reviews.length})</TabsTrigger>
          <TabsTrigger value="photos">Photos ({business.images.length})</TabsTrigger>
          {products.length > 0 && (
            <TabsTrigger value="menu">Menu ({products.length})</TabsTrigger>
          )}
          {events.length > 0 && (
            <TabsTrigger value="events">Events ({events.length})</TabsTrigger>
          )}
          {coupons.length > 0 && (
            <TabsTrigger value="offers">Offers ({coupons.length})</TabsTrigger>
          )}
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Info */}
            <div className="lg:col-span-2 space-y-6">
              {/* Business Hours */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Clock className="w-5 h-5 mr-2" />
                    Business Hours
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {business.hours ? Object.entries(business.hours).map(([day, hours]) => (
                      <div key={day} className="flex justify-between items-center">
                        <span className="capitalize font-medium text-gray-900 dark:text-white">
                          {day}
                        </span>
                        <span className={cn(
                          "text-sm",
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

              {/* Amenities */}
              {business.amenities && business.amenities.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Amenities & Features</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 gap-3">
                      {business.amenities.map((amenity) => (
                        <div key={amenity} className="flex items-center text-sm">
                          <span className="w-2 h-2 bg-green-500 rounded-full mr-3 flex-shrink-0"></span>
                          <span className="capitalize">{amenity.replace('_', ' ')}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Special Offers */}
              {coupons.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Tag className="w-5 h-5 mr-2" />
                      Special Offers
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {coupons.slice(0, 3).map((coupon) => (
                        <div key={coupon.id} className="border rounded-lg p-4 bg-gradient-to-r from-orange-50 to-red-50 dark:from-orange-900/20 dark:to-red-900/20">
                          <div className="flex items-center justify-between">
                            <div>
                              <h4 className="font-medium text-gray-900 dark:text-white">{coupon.title}</h4>
                              <p className="text-sm text-gray-600 dark:text-gray-400">{coupon.description}</p>
                              {coupon.code && (
                                <div className="mt-2">
                                  <Badge variant="outline" className="font-mono text-xs">
                                    Code: {coupon.code}
                                  </Badge>
                                </div>
                              )}
                            </div>
                            <div className="text-right">
                              <div className="text-lg font-bold text-orange-600">
                                {coupon.discountType === 'percentage' ? `${coupon.discountValue}% OFF` : `$${coupon.discountValue} OFF`}
                              </div>
                              <div className="text-xs text-gray-500">
                                Valid until {new Date(coupon.validUntil).toLocaleDateString()}
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Contact Information */}
              <Card>
                <CardHeader>
                  <CardTitle>Contact Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center">
                    <Phone className="w-5 h-5 text-gray-400 mr-3" />
                    <a
                      href={`tel:${business.contact?.phone}`}
                      className="text-primary hover:underline font-medium"
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
                </CardContent>
              </Card>

              {/* Map */}
              <Card>
                <CardHeader>
                  <CardTitle>Location</CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                  <InteractiveMap
                    businesses={[business]}
                    center={business.location?.coordinates || { lat: 0, lng: 0 }}
                    zoom={15}
                    height="200px"
                    showControls={false}
                    clustered={false}
                  />
                </CardContent>
              </Card>

              {/* Social Media */}
              {Object.keys(business.socialMedia).length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Follow Us</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex space-x-3">
                      {business.socialMedia.facebook && (
                        <a
                          href={business.socialMedia.facebook}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-700"
                        >
                          <Facebook className="w-6 h-6" />
                        </a>
                      )}
                      {business.socialMedia.twitter && (
                        <a
                          href={business.socialMedia.twitter}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-400 hover:text-blue-500"
                        >
                          <Twitter className="w-6 h-6" />
                        </a>
                      )}
                      {business.socialMedia.instagram && (
                        <a
                          href={business.socialMedia.instagram}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-pink-600 hover:text-pink-700"
                        >
                          <Instagram className="w-6 h-6" />
                        </a>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </TabsContent>

        {/* Reviews Tab */}
        <TabsContent value="reviews" className="space-y-6">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold">Customer Reviews</h2>
              <p className="text-gray-600 dark:text-gray-400">
                {reviews.length} reviews • Average rating {formatRating(business.rating)}
              </p>
            </div>
            <Button>
              <MessageCircle className="w-4 h-4 mr-2" />
              Write a Review
            </Button>
          </div>

          <div className="space-y-6">
            {reviews.map((review) => (
              <Card key={review.id} className="review-card">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                        <span className="text-sm font-medium text-gray-600">
                          {review.authorName.charAt(0).toUpperCase()}
                        </span>
                      </div>
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
                                  "rating-star w-4 h-4",
                                  star.filled ? "filled text-yellow-400" : "empty text-gray-300"
                                )}
                              />
                            ))}
                          </div>
                          <span className="text-sm text-gray-600 dark:text-gray-400">
                            {new Date(review.createdAt).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    {review.verified && (
                      <Badge variant="outline" className="text-xs">
                        Verified
                      </Badge>
                    )}
                  </div>
                  
                  {review.title && (
                    <h4 className="font-medium mb-2 text-gray-900 dark:text-white">
                      {review.title}
                    </h4>
                  )}
                  
                  <p className="text-gray-700 dark:text-gray-300 mb-4">
                    {review.content}
                  </p>
                  
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <button className="flex items-center hover:text-gray-700">
                      <ThumbsUp className="w-4 h-4 mr-1" />
                      Helpful ({review.helpful})
                    </button>
                    <button className="flex items-center hover:text-gray-700">
                      <Flag className="w-4 h-4 mr-1" />
                      Report
                    </button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Other tabs content would go here... */}
      </Tabs>
    </div>
  );
}