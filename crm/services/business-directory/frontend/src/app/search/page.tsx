'use client'

import React, { useEffect, useState, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import SearchBar from '@/components/search/search-bar'
import BusinessCard from '@/components/business/business-card'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import {
  MapPin,
  Filter,
  Grid,
  List,
  ChevronLeft,
  ChevronRight,
  AlertCircle,
  TrendingUp,
  Star,
  Users
} from 'lucide-react'
import { searchBusinesses, getCategories } from '@/lib/api'
import type {
  SearchFilters,
  SearchResults,
  BusinessCategory,
  BusinessListing
} from '@/types'

const SearchResultsContent = () => {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [isLoading, setIsLoading] = useState(true)
  const [searchResults, setSearchResults] = useState<SearchResults | null>(null)
  const [categories, setCategories] = useState<BusinessCategory[]>([])
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [currentPage, setCurrentPage] = useState(1)
  const [error, setError] = useState<string | null>(null)
  
  const itemsPerPage = 12

  // Parse search parameters
  const query = searchParams.get('q') || ''
  const location = searchParams.get('location') || ''
  const category = searchParams.get('category') || ''
  
  const initialFilters: SearchFilters = {
    query,
    city: location,
    category,
    limit: itemsPerPage,
    offset: 0,
  }

  const [filters, setFilters] = useState<SearchFilters>(initialFilters)

  // Load categories for filter dropdown
  useEffect(() => {
    const loadCategories = async () => {
      try {
        const categoriesData = await getCategories()
        setCategories(categoriesData)
      } catch (error) {
        console.error('Error loading categories:', error)
      }
    }
    loadCategories()
  }, [])

  // Perform search when filters change
  useEffect(() => {
    const performSearch = async () => {
      try {
        setIsLoading(true)
        setError(null)
        
        const searchFilters = {
          ...filters,
          limit: itemsPerPage,
          offset: (currentPage - 1) * itemsPerPage,
        }
        
        const results = await searchBusinesses(searchFilters)
        setSearchResults(results)
      } catch (error) {
        console.error('Error performing search:', error)
        setError('Failed to load search results. Please try again.')
      } finally {
        setIsLoading(false)
      }
    }

    performSearch()
  }, [filters, currentPage])

  const handleSearch = (searchQuery: string, searchFilters: SearchFilters) => {
    setFilters(searchFilters)
    setCurrentPage(1)
    
    // Update URL
    const params = new URLSearchParams()
    if (searchQuery) params.set('q', searchQuery)
    if (searchFilters.city) params.set('location', searchFilters.city)
    if (searchFilters.category) params.set('category', searchFilters.category)
    
    router.replace(`/search?${params.toString()}`)
  }

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const totalPages = searchResults 
    ? Math.ceil(searchResults.total_count / itemsPerPage)
    : 0

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Search Header */}
      <div className="bg-white shadow-sm sticky top-0 z-40">
        <div className="container mx-auto px-4 py-6">
          <SearchBar
            onSearch={handleSearch}
            initialQuery={query}
            initialLocation={location}
            showFilters={true}
            categories={categories.map(cat => cat.name)}
          />
        </div>
      </div>

      {/* Results Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Results Header */}
        {!isLoading && searchResults && (
          <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 space-y-4 md:space-y-0">
            <div className="space-y-1">
              <h1 className="text-2xl font-bold text-gray-900">
                {searchResults.total_count > 0 
                  ? `${searchResults.total_count.toLocaleString()} businesses found`
                  : 'No businesses found'
                }
              </h1>
              {(query || location || category) && (
                <div className="flex flex-wrap gap-2">
                  {query && (
                    <Badge variant="outline" className="text-sm">
                      Search: {query}
                    </Badge>
                  )}
                  {location && (
                    <Badge variant="outline" className="text-sm">
                      <MapPin className="w-3 h-3 mr-1" />
                      {location}
                    </Badge>
                  )}
                  {category && (
                    <Badge variant="outline" className="text-sm">
                      Category: {category}
                    </Badge>
                  )}
                </div>
              )}
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center space-x-4">
              <div className="flex bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 rounded-md transition-colors ${
                    viewMode === 'grid'
                      ? 'bg-white text-bizbook-primary shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Grid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 rounded-md transition-colors ${
                    viewMode === 'list'
                      ? 'bg-white text-bizbook-primary shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <List className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <Skeleton className="h-8 w-48" />
              <Skeleton className="h-10 w-24" />
            </div>
            <div className={`grid gap-6 ${
              viewMode === 'grid' 
                ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' 
                : 'grid-cols-1'
            }`}>
              {[...Array(6)].map((_, i) => (
                <Skeleton key={i} className={viewMode === 'grid' ? 'h-80' : 'h-32'} />
              ))}
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <Card className="p-8 text-center">
            <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Something went wrong
            </h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={() => window.location.reload()}>
              Try Again
            </Button>
          </Card>
        )}

        {/* No Results State */}
        {!isLoading && !error && searchResults && searchResults.total_count === 0 && (
          <Card className="p-12 text-center">
            <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <MapPin className="w-12 h-12 text-gray-400" />
            </div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              No businesses found
            </h2>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
              We couldn&apos;t find any businesses matching your search criteria. 
              Try adjusting your search terms or filters.
            </p>
            
            {/* Suggestions */}
            <div className="space-y-4">
              <p className="text-sm font-medium text-gray-700">Try these suggestions:</p>
              <div className="flex flex-wrap gap-2 justify-center">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleSearch('restaurants', { ...filters, category: 'restaurants' })}
                >
                  Restaurants
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleSearch('coffee', { ...filters, query: 'coffee' })}
                >
                  Coffee Shops
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleSearch('', { ...filters, query: '', category: '', city: '' })}
                >
                  Clear All Filters
                </Button>
              </div>
            </div>
            
            {/* Suggested locations/categories */}
            {searchResults.suggested_categories && searchResults.suggested_categories.length > 0 && (
              <div className="mt-8">
                <p className="text-sm font-medium text-gray-700 mb-3">
                  Related categories:
                </p>
                <div className="flex flex-wrap gap-2 justify-center">
                  {searchResults.suggested_categories.map((suggestedCategory) => (
                    <Button
                      key={suggestedCategory}
                      variant="outline"
                      size="sm"
                      onClick={() => handleSearch(query, { ...filters, category: suggestedCategory })}
                    >
                      {suggestedCategory}
                    </Button>
                  ))}
                </div>
              </div>
            )}
          </Card>
        )}

        {/* Results Grid/List */}
        {!isLoading && !error && searchResults && searchResults.total_count > 0 && (
          <>
            <div className={`grid gap-6 ${
              viewMode === 'grid' 
                ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' 
                : 'grid-cols-1'
            }`}>
              {searchResults.businesses.map((business) => (
                <BusinessCard
                  key={business.business_id}
                  business={business}
                  variant={viewMode === 'list' ? 'compact' : 'default'}
                  showFullDetails={viewMode === 'list'}
                  className={viewMode === 'list' ? 'w-full' : ''}
                />
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center space-x-4 mt-12">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                  className="flex items-center"
                >
                  <ChevronLeft className="w-4 h-4 mr-1" />
                  Previous
                </Button>
                
                <div className="flex items-center space-x-2">
                  {[...Array(Math.min(5, totalPages))].map((_, i) => {
                    const page = Math.max(1, Math.min(totalPages - 4, currentPage - 2)) + i
                    if (page > totalPages) return null
                    
                    return (
                      <Button
                        key={page}
                        variant={currentPage === page ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => handlePageChange(page)}
                        className="min-w-[40px]"
                      >
                        {page}
                      </Button>
                    )
                  })}
                </div>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  className="flex items-center"
                >
                  Next
                  <ChevronRight className="w-4 h-4 ml-1" />
                </Button>
              </div>
            )}

            {/* Results Info */}
            <div className="text-center mt-8 text-sm text-gray-500">
              Showing {((currentPage - 1) * itemsPerPage) + 1} to{' '}
              {Math.min(currentPage * itemsPerPage, searchResults.total_count)} of{' '}
              {searchResults.total_count.toLocaleString()} results
            </div>
          </>
        )}
      </div>
    </div>
  )
}

const SearchPage = () => {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <Skeleton className="h-20 w-full mb-8" />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Skeleton key={i} className="h-80" />
            ))}
          </div>
        </div>
      </div>
    }>
      <SearchResultsContent />
    </Suspense>
  )
}

export default SearchPage