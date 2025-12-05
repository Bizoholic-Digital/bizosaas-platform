'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Star, MapPin, Phone, Clock, ExternalLink } from 'lucide-react';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Business } from '@/types/business';
import { cn, formatRating, formatPhoneNumber, isBusinessOpen } from '@/lib/utils';

interface BusinessCardProps {
  business: Business;
  featured?: boolean;
  className?: string;
}

export function BusinessCard({ business, featured = false, className }: BusinessCardProps) {
  const isOpen = isBusinessOpen(business.hours);
  const hasHoursData = business.hours && typeof business.hours === 'object';
  
  return (
    <Card className={cn(
      featured ? 'featured-business' : 'business-card',
      className
    )}>
      <div className="relative aspect-video overflow-hidden rounded-t-lg">
        <Image
          src={(business.images && business.images[0]) || '/placeholder-business.jpg'}
          alt={business.name}
          fill
          className="object-cover transition-transform duration-300 hover:scale-105"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
        {featured && (
          <div className="absolute top-2 left-2">
            <span className="bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium">
              Featured
            </span>
          </div>
        )}
        {business.verified && (
          <div className="absolute top-2 right-2">
            <span className="business-status verified">
              ✓ Verified
            </span>
          </div>
        )}
      </div>
      
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-semibold text-lg text-gray-900 dark:text-white line-clamp-1">
            {business.name}
          </h3>
          <div className="flex items-center space-x-1 ml-2">
            <Star className="w-4 h-4 text-yellow-400 fill-current" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {formatRating(business.rating)}
            </span>
            <span className="text-sm text-gray-500 dark:text-gray-400">
              ({business.reviewCount})
            </span>
          </div>
        </div>
        
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
          {business.description}
        </p>
        
        <div className="space-y-2">
          <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
            <MapPin className="w-4 h-4 mr-2 flex-shrink-0" />
            <span className="line-clamp-1">
              {business.location?.address || 'Address not available'}, {business.location?.city || 'City not available'}
            </span>
          </div>
          
          <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
            <Phone className="w-4 h-4 mr-2 flex-shrink-0" />
            <span>{formatPhoneNumber(business.contact?.phone || 'Phone not available')}</span>
          </div>
          
          <div className="flex items-center text-sm">
            <Clock className="w-4 h-4 mr-2 flex-shrink-0" />
            <span className={cn(
              hasHoursData
                ? isOpen 
                  ? 'text-green-600 dark:text-green-400' 
                  : 'text-red-600 dark:text-red-400'
                : 'text-gray-500 dark:text-gray-400'
            )}>
              {hasHoursData 
                ? (isOpen ? 'Open now' : 'Closed')
                : 'Hours not available'
              }
            </span>
          </div>
        </div>
        
        <div className="flex items-center justify-between mt-3">
          <div className="flex flex-wrap gap-1">
            {(business.tags || []).slice(0, 2).map((tag) => (
              <span
                key={tag}
                className="filter-badge text-xs"
              >
                {tag}
              </span>
            ))}
          </div>
          
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            {business.pricing?.range || 'Price not available'}
          </span>
        </div>
      </CardContent>
      
      <CardFooter className="p-4 pt-0 flex space-x-2">
        <Button asChild className="flex-1">
          <Link href={`/business/${business.id}`}>
            View Details
          </Link>
        </Button>
        
        {business.contact?.website && (
          <Button
            variant="outline"
            size="icon"
            asChild
          >
            <a
              href={business.contact?.website}
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Visit website"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}