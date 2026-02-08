'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { Grid, List, MapPin, Filter, Map as MapIcon } from 'lucide-react';
import { AdvancedSearchBar } from '@/components/search/advanced-search-bar';
import { BusinessCard } from '@/components/business/business-card';
<<<<<<< HEAD:portals/business-directory/business-directory/app/search/page.tsx
import { InteractiveMap } from '@/components/map/interactive-map';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
=======
import { Button, Card, CardContent } from '@/lib/ui';
>>>>>>> 689624bdacbb85634f44c01400300bc3ce37e57e:bizosaas/frontend/apps/business-directory/app/search/page.tsx
import { businessAPI } from '@/lib/api';
import { Business, SearchFilters, SearchResult } from '@/types/business';

function SearchPageContent() {
  const searchParams = useSearchParams();
  const [searchResult, setSearchResult] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list' | 'map'>('grid');
  const [showFilters, setShowFilters] = useState(false);

  const initialFilters: SearchFilters = {
    query: searchParams.get('q') || '',
    location: searchParams.get('location') || '',
    category: searchParams.get('category') || '',
  };

  const performSearch = async (filters: SearchFilters) => {
    // We don't want to show global loading for background "as you type" searches
    // but we need a visual indicator. For now let's keep it simple.
    try {
      const result = await businessAPI.searchBusinesses(filters);
      setSearchResult(result);

      // Update URL without page refresh only on explicit search or after debounce
      const params = new URLSearchParams();
      if (filters.query) params.set('q', filters.query);
      if (filters.location) params.set('location', filters.location);
      if (filters.category) params.set('category', filters.category);

      window.history.replaceState({}, '', `${window.location.pathname}?${params.toString()}`);
    } catch (error) {
      console.error('Error performing search:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    performSearch(initialFilters);
  }, [searchParams]);

  const handleSearch = async (filters: SearchFilters) => {
    performSearch(filters);
  };

  if (loading && !searchResult) {
    return (
      <div className="min-h-screen">
        <div className="bg-gray-50 dark:bg-gray-900 py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <AdvancedSearchBar onSearch={handleSearch} initialFilters={initialFilters} />
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-muted-foreground">Initializing search...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!searchResult) {
    return (
      <div className="min-h-screen">
        <div className="bg-gray-50 dark:bg-gray-900 py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <AdvancedSearchBar onSearch={handleSearch} initialFilters={initialFilters} />
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <p className="text-lg text-muted-foreground">No results found. Please try a different search.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Search Header */}
      <div className="bg-gray-50 dark:bg-gray-900 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AdvancedSearchBar
            onSearch={handleSearch}
            initialFilters={initialFilters}
          />
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Results Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Search Results
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              {searchResult.total.toLocaleString()} businesses found
              {searchResult.filters.query && ` for "${searchResult.filters.query}"`}
              {searchResult.filters.location && ` in ${searchResult.filters.location}`}
            </p>
          </div>

          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            {/* View Mode Toggle */}
            <div className="flex items-center bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
              <Button
                variant={viewMode === 'grid' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('grid')}
                className="p-2"
              >
                <Grid className="w-4 h-4" />
              </Button>
              <Button
                variant={viewMode === 'list' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('list')}
                className="p-2"
              >
                <List className="w-4 h-4" />
              </Button>
            </div>

            {/* Filters Toggle */}
            <Button
              variant="outline"
              onClick={() => setShowFilters(!showFilters)}
            >
              <Filter className="w-4 h-4 mr-2" />
              Filters
            </Button>

            {/* Map View */}
            <Button
              variant={viewMode === 'map' ? 'default' : 'outline'}
              onClick={() => setViewMode('map')}
            >
              <MapPin className="w-4 h-4 mr-2" />
              Map View
            </Button>
          </div>
        </div>

        {/* Active Filters */}
        {(searchResult.filters.query || searchResult.filters.location || searchResult.filters.category) && (
          <div className="flex flex-wrap gap-2 mb-6">
            <span className="text-sm text-gray-600 dark:text-gray-400">Active filters:</span>
            {searchResult.filters.query && (
              <span className="filter-badge">
                Search: {searchResult.filters.query}
              </span>
            )}
            {searchResult.filters.location && (
              <span className="filter-badge">
                Location: {searchResult.filters.location}
              </span>
            )}
            {searchResult.filters.category && (
              <span className="filter-badge">
                Category: {searchResult.filters.category}
              </span>
            )}
          </div>
        )}

        <div className="flex gap-8">
          {/* Sidebar Filters */}
          {showFilters && (
            <div className="w-64 flex-shrink-0">
              <Card>
                <CardContent className="p-6">
                  <h3 className="font-semibold mb-4">Refine Search</h3>

                  {/* Rating Filter */}
                  <div className="mb-6">
                    <h4 className="font-medium mb-2">Rating</h4>
                    <div className="space-y-2">
                      {[4, 3, 2, 1].map((rating) => (
                        <label key={rating} className="flex items-center">
                          <input
                            type="checkbox"
                            className="rounded border-gray-300 mr-2"
                          />
                          <span className="text-sm">
                            {rating}+ stars
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Price Range */}
                  <div className="mb-6">
                    <h4 className="font-medium mb-2">Price Range</h4>
                    <div className="space-y-2">
                      {['$', '$$', '$$$', '$$$$'].map((price) => (
                        <label key={price} className="flex items-center">
                          <input
                            type="checkbox"
                            className="rounded border-gray-300 mr-2"
                          />
                          <span className="text-sm">{price}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Features */}
                  <div className="mb-6">
                    <h4 className="font-medium mb-2">Features</h4>
                    <div className="space-y-2">
                      {['Open Now', 'Verified', 'Featured', 'Accepts Cards'].map((feature) => (
                        <label key={feature} className="flex items-center">
                          <input
                            type="checkbox"
                            className="rounded border-gray-300 mr-2"
                          />
                          <span className="text-sm">{feature}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Results Grid / Map */}
          <div className="flex-1">
            {searchResult.businesses.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-lg text-gray-600 dark:text-gray-400 mb-4">
                  No businesses found matching your criteria.
                </p>
                <Button onClick={() => handleSearch({ query: '', location: '' })}>
                  View All Businesses
                </Button>
              </div>
            ) : viewMode === 'map' ? (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[700px]">
                <div className="h-full overflow-y-auto pr-2 space-y-4">
                  {searchResult.businesses.map((business) => (
                    <BusinessCard
                      key={business.id}
                      business={business}
                      className="md:flex md:flex-row md:h-auto"
                    />
                  ))}
                </div>
                <div className="sticky top-8 h-full">
                  <InteractiveMap
                    businesses={searchResult.businesses}
                    height="100%"
                  />
                </div>
              </div>
            ) : (
              <div className={
                viewMode === 'grid'
                  ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
                  : 'space-y-6'
              }>
                {searchResult.businesses.map((business) => (
                  <BusinessCard
                    key={business.id}
                    business={business}
                    className={viewMode === 'list' ? 'md:flex md:flex-row md:h-auto' : ''}
                  />
                ))}
              </div>
            )}

            {/* Pagination */}
            {searchResult.total > searchResult.limit && (
              <div className="flex justify-center mt-8">
                <div className="flex items-center space-x-2">
                  <Button variant="outline" disabled>
                    Previous
                  </Button>
                  <span className="px-4 py-2 text-sm">
                    Page {searchResult.page} of {Math.ceil(searchResult.total / searchResult.limit)}
                  </span>
                  <Button variant="outline">
                    Next
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Suggestions */}
        {searchResult.suggestions && searchResult.suggestions.length > 0 && (
          <div className="mt-12 p-6 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <h3 className="font-semibold mb-3">Try searching for:</h3>
            <div className="flex flex-wrap gap-2">
              {searchResult.suggestions.map((suggestion) => (
                <Button
                  key={suggestion}
                  variant="outline"
                  size="sm"
                  onClick={() => handleSearch({ ...searchResult.filters, query: suggestion })}
                >
                  {suggestion}
                </Button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    }>
      <SearchPageContent />
    </Suspense>
  );
}