'use client';

import React, { useState, useEffect } from 'react';
import { 
  Filter, 
  X, 
  Star, 
  Clock, 
  MapPin, 
  DollarSign,
  Wifi,
  Car,
  CreditCard,
  Accessibility,
  Coffee,
  ShoppingBag
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, Button, Badge, Separator, Accordion, AccordionContent, AccordionItem, AccordionTrigger, Slider } from '@bizoholic-digital/ui-components';
import { SearchFilters, Category } from '@/types/business';
import { businessAPI } from '@/lib/api';
import { cn } from '@/lib/utils';

interface AdvancedFiltersProps {
  filters: SearchFilters;
  onFiltersChange: (filters: SearchFilters) => void;
  onClose?: () => void;
  className?: string;
  showClearAll?: boolean;
}

const AMENITIES_ICONS: { [key: string]: React.ReactNode } = {
  'wifi': <Wifi className="w-4 h-4" />,
  'parking': <Car className="w-4 h-4" />,
  'card_payment': <CreditCard className="w-4 h-4" />,
  'wheelchair_accessible': <Accessibility className="w-4 h-4" />,
  'outdoor_seating': <Coffee className="w-4 h-4" />,
  'delivery': <ShoppingBag className="w-4 h-4" />,
  'takeout': <ShoppingBag className="w-4 h-4" />,
};

const POPULAR_AMENITIES = [
  { key: 'wifi', label: 'Free WiFi' },
  { key: 'parking', label: 'Parking Available' },
  { key: 'card_payment', label: 'Card Payment' },
  { key: 'wheelchair_accessible', label: 'Wheelchair Accessible' },
  { key: 'outdoor_seating', label: 'Outdoor Seating' },
  { key: 'delivery', label: 'Delivery' },
  { key: 'takeout', label: 'Takeout' },
  { key: 'reservations', label: 'Reservations' },
  { key: '24_hours', label: '24 Hours' },
  { key: 'valet_parking', label: 'Valet Parking' },
  { key: 'private_dining', label: 'Private Dining' },
  { key: 'live_music', label: 'Live Music' },
];

export function AdvancedFilters({
  filters,
  onFiltersChange,
  onClose,
  className,
  showClearAll = true
}: AdvancedFiltersProps) {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedSubcategories, setSelectedSubcategories] = useState<string[]>([]);
  const [ratingRange, setRatingRange] = useState<number[]>([
    filters.rating || 0
  ]);
  const [distanceRange, setDistanceRange] = useState<number[]>([
    filters.distance || 25
  ]);

  // Load categories
  useEffect(() => {
    setLoading(true);
    businessAPI.getCategories()
      .then(setCategories)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleFilterChange = (key: keyof SearchFilters, value: any) => {
    const newFilters = { ...filters, [key]: value };
    onFiltersChange(newFilters);
  };

  const handleArrayFilterToggle = (key: keyof SearchFilters, value: string) => {
    const currentArray = (filters[key] as string[]) || [];
    const newArray = currentArray.includes(value)
      ? currentArray.filter(item => item !== value)
      : [...currentArray, value];
    
    handleFilterChange(key, newArray.length > 0 ? newArray : undefined);
  };

  const handleSubcategoryToggle = (subcategorySlug: string) => {
    const newSubcategories = selectedSubcategories.includes(subcategorySlug)
      ? selectedSubcategories.filter(s => s !== subcategorySlug)
      : [...selectedSubcategories, subcategorySlug];
    
    setSelectedSubcategories(newSubcategories);
    handleFilterChange('subcategory', newSubcategories.join(','));
  };

  const clearAllFilters = () => {
    const clearedFilters: SearchFilters = {
      query: filters.query || '',
      location: filters.location || '',
      sortBy: filters.sortBy || 'relevance',
      sortOrder: filters.sortOrder || 'desc'
    };
    
    setSelectedSubcategories([]);
    setRatingRange([0]);
    setDistanceRange([25]);
    onFiltersChange(clearedFilters);
  };

  const getActiveFiltersCount = () => {
    let count = 0;
    if (filters.category) count++;
    if (filters.subcategory) count++;
    if (filters.rating && filters.rating > 0) count++;
    if (filters.priceRange && filters.priceRange.length > 0) count++;
    if (filters.distance && filters.distance < 25) count++;
    if (filters.openNow) count++;
    if (filters.verified) count++;
    if (filters.featured) count++;
    if (filters.amenities && filters.amenities.length > 0) count++;
    return count;
  };

  return (
    <Card className={cn("advanced-filters", className)}>
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold flex items-center">
            <Filter className="w-5 h-5 mr-2" />
            Filters
            {getActiveFiltersCount() > 0 && (
              <Badge variant="secondary" className="ml-2">
                {getActiveFiltersCount()}
              </Badge>
            )}
          </CardTitle>
          <div className="flex items-center space-x-2">
            {showClearAll && getActiveFiltersCount() > 0 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={clearAllFilters}
                className="text-xs"
              >
                Clear All
              </Button>
            )}
            {onClose && (
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
                className="p-1"
              >
                <X className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        <Accordion type="multiple" defaultValue={["categories", "rating", "price"]} className="w-full">
          {/* Categories */}
          <AccordionItem value="categories">
            <AccordionTrigger className="text-sm font-medium">
              Categories
            </AccordionTrigger>
            <AccordionContent className="space-y-3">
              {loading ? (
                <div className="text-center py-4">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mx-auto"></div>
                </div>
              ) : (
                <div className="space-y-3">
                  {categories.map((category) => (
                    <div key={category.id} className="space-y-2">
                      <label className="flex items-center cursor-pointer">
                        <input
                          type="radio"
                          name="category"
                          checked={filters.category === category.slug}
                          onChange={() => handleFilterChange('category', 
                            filters.category === category.slug ? undefined : category.slug
                          )}
                          className="rounded border-gray-300 mr-3"
                        />
                        <div className="flex items-center flex-1">
                          <span className="text-lg mr-2">{category.icon}</span>
                          <div>
                            <div className="text-sm font-medium">{category.name}</div>
                            <div className="text-xs text-gray-500">
                              {category.businessCount.toLocaleString()} businesses
                            </div>
                          </div>
                        </div>
                      </label>
                      
                      {/* Subcategories */}
                      {filters.category === category.slug && category.subcategories.length > 0 && (
                        <div className="ml-8 space-y-1">
                          {category.subcategories.map((subcategory) => (
                            <label key={subcategory.id} className="flex items-center cursor-pointer">
                              <input
                                type="checkbox"
                                checked={selectedSubcategories.includes(subcategory.slug)}
                                onChange={() => handleSubcategoryToggle(subcategory.slug)}
                                className="rounded border-gray-300 mr-2 text-xs"
                              />
                              <div className="text-xs">
                                <div>{subcategory.name}</div>
                                <div className="text-gray-500">
                                  {subcategory.businessCount.toLocaleString()}
                                </div>
                              </div>
                            </label>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </AccordionContent>
          </AccordionItem>

          {/* Rating */}
          <AccordionItem value="rating">
            <AccordionTrigger className="text-sm font-medium">
              Rating
            </AccordionTrigger>
            <AccordionContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span>Minimum Rating</span>
                  <div className="flex items-center">
                    <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
                    <span className="font-medium">{ratingRange[0].toFixed(1)}+</span>
                  </div>
                </div>
                <Slider
                  value={ratingRange}
                  onValueChange={(value) => {
                    setRatingRange(value);
                    handleFilterChange('rating', value[0] > 0 ? value[0] : undefined);
                  }}
                  max={5}
                  min={0}
                  step={0.5}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500">
                  <span>Any</span>
                  <span>5★</span>
                </div>
              </div>
              
              {/* Quick Rating Buttons */}
              <div className="grid grid-cols-2 gap-2">
                {[4, 3, 2, 1].map((rating) => (
                  <Button
                    key={rating}
                    variant={filters.rating === rating ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleFilterChange('rating', 
                      filters.rating === rating ? undefined : rating
                    )}
                    className="text-xs justify-start"
                  >
                    <Star className="w-3 h-3 text-yellow-400 fill-current mr-1" />
                    {rating}+ stars
                  </Button>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Price Range */}
          <AccordionItem value="price">
            <AccordionTrigger className="text-sm font-medium">
              Price Range
            </AccordionTrigger>
            <AccordionContent>
              <div className="grid grid-cols-2 gap-2">
                {['$', '$$', '$$$', '$$$$'].map((price) => (
                  <Button
                    key={price}
                    variant={filters.priceRange?.includes(price) ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleArrayFilterToggle('priceRange', price)}
                    className="text-xs justify-start"
                  >
                    <DollarSign className="w-3 h-3 mr-1" />
                    {price}
                  </Button>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Distance */}
          <AccordionItem value="distance">
            <AccordionTrigger className="text-sm font-medium">
              Distance
            </AccordionTrigger>
            <AccordionContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span>Maximum Distance</span>
                  <div className="flex items-center">
                    <MapPin className="w-4 h-4 text-blue-500 mr-1" />
                    <span className="font-medium">
                      {distanceRange[0] >= 25 ? 'Any' : `${distanceRange[0]}km`}
                    </span>
                  </div>
                </div>
                <Slider
                  value={distanceRange}
                  onValueChange={(value) => {
                    setDistanceRange(value);
                    handleFilterChange('distance', value[0] < 25 ? value[0] : undefined);
                  }}
                  max={25}
                  min={1}
                  step={1}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500">
                  <span>1km</span>
                  <span>25km+</span>
                </div>
              </div>
              
              {/* Quick Distance Buttons */}
              <div className="grid grid-cols-3 gap-2">
                {[1, 5, 10].map((distance) => (
                  <Button
                    key={distance}
                    variant={filters.distance === distance ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleFilterChange('distance', 
                      filters.distance === distance ? undefined : distance
                    )}
                    className="text-xs"
                  >
                    {distance}km
                  </Button>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Features */}
          <AccordionItem value="features">
            <AccordionTrigger className="text-sm font-medium">
              Features
            </AccordionTrigger>
            <AccordionContent className="space-y-3">
              <div className="space-y-2">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.openNow || false}
                    onChange={(e) => handleFilterChange('openNow', e.target.checked ? true : undefined)}
                    className="rounded border-gray-300 mr-3"
                  />
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 text-green-500 mr-2" />
                    <span className="text-sm">Open Now</span>
                  </div>
                </label>
                
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.verified || false}
                    onChange={(e) => handleFilterChange('verified', e.target.checked ? true : undefined)}
                    className="rounded border-gray-300 mr-3"
                  />
                  <div className="flex items-center">
                    <Star className="w-4 h-4 text-blue-500 mr-2" />
                    <span className="text-sm">Verified Business</span>
                  </div>
                </label>
                
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.featured || false}
                    onChange={(e) => handleFilterChange('featured', e.target.checked ? true : undefined)}
                    className="rounded border-gray-300 mr-3"
                  />
                  <div className="flex items-center">
                    <Star className="w-4 h-4 text-yellow-500 mr-2 fill-current" />
                    <span className="text-sm">Featured Business</span>
                  </div>
                </label>
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Amenities */}
          <AccordionItem value="amenities">
            <AccordionTrigger className="text-sm font-medium">
              Amenities
            </AccordionTrigger>
            <AccordionContent>
              <div className="grid grid-cols-1 gap-2">
                {POPULAR_AMENITIES.map((amenity) => (
                  <label key={amenity.key} className="flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={filters.amenities?.includes(amenity.key) || false}
                      onChange={() => handleArrayFilterToggle('amenities', amenity.key)}
                      className="rounded border-gray-300 mr-3"
                    />
                    <div className="flex items-center">
                      {AMENITIES_ICONS[amenity.key] || <div className="w-4 h-4 mr-2" />}
                      <span className="text-sm ml-2">{amenity.label}</span>
                    </div>
                  </label>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Sort Options */}
          <AccordionItem value="sort">
            <AccordionTrigger className="text-sm font-medium">
              Sort By
            </AccordionTrigger>
            <AccordionContent>
              <div className="space-y-2">
                {[
                  { value: 'relevance', label: 'Relevance' },
                  { value: 'rating', label: 'Highest Rated' },
                  { value: 'distance', label: 'Distance' },
                  { value: 'name', label: 'Name (A-Z)' },
                  { value: 'newest', label: 'Newest First' }
                ].map((option) => (
                  <label key={option.value} className="flex items-center cursor-pointer">
                    <input
                      type="radio"
                      name="sortBy"
                      checked={filters.sortBy === option.value}
                      onChange={() => handleFilterChange('sortBy', option.value)}
                      className="rounded border-gray-300 mr-3"
                    />
                    <span className="text-sm">{option.label}</span>
                  </label>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>
        </Accordion>

        {/* Active Filters Summary */}
        {getActiveFiltersCount() > 0 && (
          <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
            <div className="text-sm font-medium mb-2">Active Filters:</div>
            <div className="flex flex-wrap gap-1">
              {filters.category && (
                <Badge variant="outline" className="text-xs">
                  {categories.find(c => c.slug === filters.category)?.name || filters.category}
                  <button
                    onClick={() => handleFilterChange('category', undefined)}
                    className="ml-1 hover:text-red-500"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </Badge>
              )}
              {filters.rating && (
                <Badge variant="outline" className="text-xs">
                  {filters.rating}+ stars
                  <button
                    onClick={() => handleFilterChange('rating', undefined)}
                    className="ml-1 hover:text-red-500"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </Badge>
              )}
              {filters.priceRange && filters.priceRange.length > 0 && (
                <Badge variant="outline" className="text-xs">
                  {filters.priceRange.join(', ')}
                  <button
                    onClick={() => handleFilterChange('priceRange', undefined)}
                    className="ml-1 hover:text-red-500"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </Badge>
              )}
              {filters.distance && (
                <Badge variant="outline" className="text-xs">
                  Within {filters.distance}km
                  <button
                    onClick={() => handleFilterChange('distance', undefined)}
                    className="ml-1 hover:text-red-500"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </Badge>
              )}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}