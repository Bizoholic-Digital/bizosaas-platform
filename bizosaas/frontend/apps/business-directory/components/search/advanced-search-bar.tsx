'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Search, MapPin, Filter, X, Clock, Star, DollarSign } from 'lucide-react';
import { useDebounce } from 'use-debounce';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { SearchFilters, SearchSuggestion } from '@/types/business';
import { businessAPI } from '@/lib/api';
import { cn } from '@/lib/utils';

interface AdvancedSearchBarProps {
  onSearch: (filters: SearchFilters) => void;
  initialFilters?: SearchFilters;
  className?: string;
  showAdvancedFilters?: boolean;
}

export function AdvancedSearchBar({ 
  onSearch, 
  initialFilters, 
  className,
  showAdvancedFilters = false 
}: AdvancedSearchBarProps) {
  const [filters, setFilters] = useState<SearchFilters>(
    initialFilters || {
      query: '',
      location: '',
      sortBy: 'relevance',
      sortOrder: 'desc'
    }
  );

  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loading, setLoading] = useState(false);
  const [debouncedQuery] = useDebounce(filters.query, 300);
  const [debouncedLocation] = useDebounce(filters.location, 300);
  const [recentSearches, setRecentSearches] = useState<string[]>([]);
  const [showAdvanced, setShowAdvanced] = useState(showAdvancedFilters);
  
  const searchRef = useRef<HTMLDivElement>(null);
  const queryInputRef = useRef<HTMLInputElement>(null);

  // Load recent searches from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('recent-searches');
    if (saved) {
      try {
        setRecentSearches(JSON.parse(saved));
      } catch (error) {
        console.error('Error loading recent searches:', error);
      }
    }
  }, []);

  // Get search suggestions
  useEffect(() => {
    if (debouncedQuery.length >= 2) {
      setLoading(true);
      businessAPI.getSearchSuggestions(debouncedQuery, debouncedLocation)
        .then((data) => {
          setSuggestions(data);
          setShowSuggestions(true);
        })
        .catch((error) => {
          console.error('Error fetching suggestions:', error);
          setSuggestions([]);
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  }, [debouncedQuery, debouncedLocation]);

  // Handle click outside to close suggestions
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    performSearch(filters);
  };

  const performSearch = (searchFilters: SearchFilters) => {
    onSearch(searchFilters);
    setShowSuggestions(false);
    
    // Save to recent searches
    if (searchFilters.query && searchFilters.query.trim()) {
      const newRecentSearches = [
        searchFilters.query.trim(),
        ...recentSearches.filter(s => s !== searchFilters.query.trim())
      ].slice(0, 5);
      
      setRecentSearches(newRecentSearches);
      localStorage.setItem('recent-searches', JSON.stringify(newRecentSearches));
    }
  };

  const handleInputChange = (field: keyof SearchFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSuggestionClick = (suggestion: SearchSuggestion) => {
    const newFilters = { ...filters };
    
    switch (suggestion.type) {
      case 'business':
        if (suggestion.metadata?.businessId) {
          window.location.href = `/business/${suggestion.metadata.businessId}`;
          return;
        }
        break;
      case 'category':
        newFilters.category = suggestion.metadata?.categorySlug || suggestion.text;
        break;
      case 'location':
        newFilters.location = suggestion.text;
        if (suggestion.metadata?.coordinates) {
          newFilters.latitude = suggestion.metadata.coordinates.lat;
          newFilters.longitude = suggestion.metadata.coordinates.lng;
        }
        break;
      case 'query':
      default:
        newFilters.query = suggestion.text;
        break;
    }
    
    setFilters(newFilters);
    performSearch(newFilters);
  };

  const clearFilter = (field: keyof SearchFilters) => {
    const newFilters = { ...filters };
    delete newFilters[field];
    setFilters(newFilters);
  };

  const getActiveFiltersCount = () => {
    let count = 0;
    if (filters.category) count++;
    if (filters.rating) count++;
    if (filters.priceRange && filters.priceRange.length > 0) count++;
    if (filters.distance) count++;
    if (filters.openNow) count++;
    if (filters.verified) count++;
    if (filters.amenities && filters.amenities.length > 0) count++;
    return count;
  };

  return (
    <div ref={searchRef} className={cn("relative", className)}>
      <Card className="search-card">
        <CardContent className="p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Main Search Row */}
            <div className="flex flex-col md:flex-row gap-4">
              {/* Search Query with Suggestions */}
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 z-10" />
                <Input
                  ref={queryInputRef}
                  type="text"
                  placeholder="Search businesses, services, or products..."
                  value={filters.query}
                  onChange={(e) => handleInputChange('query', e.target.value)}
                  onFocus={() => {
                    if (suggestions.length > 0 || recentSearches.length > 0) {
                      setShowSuggestions(true);
                    }
                  }}
                  className="pl-10 pr-10"
                />
                {filters.query && (
                  <button
                    type="button"
                    onClick={() => handleInputChange('query', '')}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
                
                {/* Search Suggestions Dropdown */}
                {showSuggestions && (
                  <div className="absolute top-full left-0 right-0 z-50 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-96 overflow-y-auto dark:bg-gray-900 dark:border-gray-700">
                    {loading && (
                      <div className="p-4 text-center">
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mx-auto"></div>
                        <p className="mt-2 text-sm text-muted-foreground">Searching...</p>
                      </div>
                    )}
                    
                    {!loading && suggestions.length > 0 && (
                      <div>
                        <div className="px-3 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider border-b border-gray-100 dark:border-gray-800">
                          Suggestions
                        </div>
                        {suggestions.map((suggestion) => (
                          <button
                            key={suggestion.id}
                            type="button"
                            onClick={() => handleSuggestionClick(suggestion)}
                            className="w-full px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800 flex items-center space-x-3"
                          >
                            <div className="flex-shrink-0">
                              {suggestion.type === 'business' && <Search className="w-4 h-4 text-blue-500" />}
                              {suggestion.type === 'category' && <Filter className="w-4 h-4 text-green-500" />}
                              {suggestion.type === 'location' && <MapPin className="w-4 h-4 text-red-500" />}
                              {suggestion.type === 'query' && <Search className="w-4 h-4 text-gray-400" />}
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                                {suggestion.text}
                              </p>
                              <p className="text-xs text-gray-500 dark:text-gray-400 capitalize">
                                {suggestion.type}
                              </p>
                            </div>
                          </button>
                        ))}
                      </div>
                    )}
                    
                    {!loading && suggestions.length === 0 && recentSearches.length > 0 && (
                      <div>
                        <div className="px-3 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider border-b border-gray-100 dark:border-gray-800">
                          Recent Searches
                        </div>
                        {recentSearches.map((search, index) => (
                          <button
                            key={index}
                            type="button"
                            onClick={() => {
                              handleInputChange('query', search);
                              performSearch({ ...filters, query: search });
                            }}
                            className="w-full px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800 flex items-center space-x-3"
                          >
                            <Clock className="w-4 h-4 text-gray-400 flex-shrink-0" />
                            <span className="text-sm text-gray-700 dark:text-gray-300 truncate">
                              {search}
                            </span>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Location */}
              <div className="relative md:w-64">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <Input
                  type="text"
                  placeholder="Location"
                  value={filters.location || ''}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  className="pl-10 pr-10"
                />
                {filters.location && (
                  <button
                    type="button"
                    onClick={() => handleInputChange('location', '')}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              {/* Search Button */}
              <Button type="submit" className="md:w-auto w-full">
                <Search className="w-4 h-4 mr-2" />
                Search
              </Button>
            </div>

            {/* Quick Filters */}
            <div className="flex flex-wrap gap-2 items-center">
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Quick filters:
              </span>
              
              {/* Category Filters */}
              {['Restaurants', 'Healthcare', 'Retail', 'Services'].map((category) => (
                <Button
                  key={category}
                  type="button"
                  variant={filters.category === category.toLowerCase() ? "default" : "outline"}
                  size="sm"
                  onClick={() => {
                    const newCategory = filters.category === category.toLowerCase() ? undefined : category.toLowerCase();
                    const newFilters = { ...filters, category: newCategory };
                    setFilters(newFilters);
                    performSearch(newFilters);
                  }}
                  className="text-xs"
                >
                  {category}
                </Button>
              ))}
              
              {/* Open Now Filter */}
              <Button
                type="button"
                variant={filters.openNow ? "default" : "outline"}
                size="sm"
                onClick={() => {
                  const newFilters = { ...filters, openNow: !filters.openNow };
                  setFilters(newFilters);
                  performSearch(newFilters);
                }}
                className="text-xs"
              >
                <Clock className="w-3 h-3 mr-1" />
                Open Now
              </Button>
              
              {/* Verified Filter */}
              <Button
                type="button"
                variant={filters.verified ? "default" : "outline"}
                size="sm"
                onClick={() => {
                  const newFilters = { ...filters, verified: !filters.verified };
                  setFilters(newFilters);
                  performSearch(newFilters);
                }}
                className="text-xs"
              >
                <Star className="w-3 h-3 mr-1" />
                Verified
              </Button>
            </div>

            {/* Advanced Filters Toggle */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="text-sm text-gray-600 dark:text-gray-400"
              >
                <Filter className="w-4 h-4 mr-2" />
                Advanced Filters
                {getActiveFiltersCount() > 0 && (
                  <Badge variant="secondary" className="ml-2">
                    {getActiveFiltersCount()}
                  </Badge>
                )}
              </Button>
              
              {/* Active Filters */}
              {getActiveFiltersCount() > 0 && (
                <div className="flex flex-wrap gap-1">
                  {filters.rating && (
                    <Badge variant="outline" className="text-xs">
                      {filters.rating}+ stars
                      <button
                        type="button"
                        onClick={() => clearFilter('rating')}
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
                        type="button"
                        onClick={() => clearFilter('priceRange')}
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
                        type="button"
                        onClick={() => clearFilter('distance')}
                        className="ml-1 hover:text-red-500"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </Badge>
                  )}
                </div>
              )}
            </div>

            {/* Advanced Filters Panel */}
            {showAdvanced && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4 border-t border-gray-200 dark:border-gray-700">
                {/* Rating Filter */}
                <div>
                  <h4 className="font-medium mb-3 text-sm">Rating</h4>
                  <div className="space-y-2">
                    {[4, 3, 2, 1].map((rating) => (
                      <label key={rating} className="flex items-center cursor-pointer">
                        <input
                          type="radio"
                          name="rating"
                          checked={filters.rating === rating}
                          onChange={() => handleInputChange('rating', rating)}
                          className="rounded border-gray-300 mr-2"
                        />
                        <span className="text-sm flex items-center">
                          {rating}+ <Star className="w-3 h-3 ml-1 text-yellow-400 fill-current" />
                        </span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Price Range */}
                <div>
                  <h4 className="font-medium mb-3 text-sm">Price Range</h4>
                  <div className="space-y-2">
                    {['$', '$$', '$$$', '$$$$'].map((price) => (
                      <label key={price} className="flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={filters.priceRange?.includes(price) || false}
                          onChange={(e) => {
                            const current = filters.priceRange || [];
                            const newPriceRange = e.target.checked
                              ? [...current, price]
                              : current.filter(p => p !== price);
                            handleInputChange('priceRange', newPriceRange);
                          }}
                          className="rounded border-gray-300 mr-2"
                        />
                        <span className="text-sm flex items-center">
                          <DollarSign className="w-3 h-3 mr-1" />
                          {price}
                        </span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Distance */}
                <div>
                  <h4 className="font-medium mb-3 text-sm">Distance</h4>
                  <div className="space-y-2">
                    {[1, 5, 10, 25].map((distance) => (
                      <label key={distance} className="flex items-center cursor-pointer">
                        <input
                          type="radio"
                          name="distance"
                          checked={filters.distance === distance}
                          onChange={() => handleInputChange('distance', distance)}
                          className="rounded border-gray-300 mr-2"
                        />
                        <span className="text-sm">
                          Within {distance}km
                        </span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </form>
        </CardContent>
      </Card>
    </div>
  );
}