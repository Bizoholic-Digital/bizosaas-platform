'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import { 
  Search, 
  MapPin, 
  Filter,
  X,
  Star,
  Clock,
  DollarSign,
  Verified
} from 'lucide-react'
import { SearchFilters } from '@/types'
import { Badge } from '@/components/ui/badge'

interface SearchBarProps {
  onSearch: (query: string, filters: SearchFilters) => void
  initialQuery?: string
  initialLocation?: string
  placeholder?: string
  showFilters?: boolean
  categories?: string[]
  className?: string
}

const SearchBar = ({ 
  onSearch, 
  initialQuery = '',
  initialLocation = '',
  placeholder = "What are you looking for?",
  showFilters = true,
  categories = [],
  className
}: SearchBarProps) => {
  const [searchQuery, setSearchQuery] = useState(initialQuery)
  const [location, setLocation] = useState(initialLocation)
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false)
  const [filters, setFilters] = useState<SearchFilters>({
    query: initialQuery,
    city: initialLocation,
  })

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    const searchFilters: SearchFilters = {
      ...filters,
      query: searchQuery,
      city: location,
    }
    onSearch(searchQuery, searchFilters)
  }

  const handleFilterChange = (key: keyof SearchFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const clearFilters = () => {
    setFilters({
      query: searchQuery,
      city: location,
    })
    setShowAdvancedFilters(false)
  }

  const getActiveFiltersCount = () => {
    const { query, city, ...otherFilters } = filters
    return Object.values(otherFilters).filter(Boolean).length
  }

  const priceRanges = [
    { value: '$', label: '$ (Budget)' },
    { value: '$$', label: '$$ (Moderate)' },
    { value: '$$$', label: '$$$ (Expensive)' },
    { value: '$$$$', label: '$$$$ (Luxury)' },
  ]

  const sortOptions = [
    { value: 'relevance', label: 'Relevance' },
    { value: 'rating', label: 'Highest Rated' },
    { value: 'distance', label: 'Distance' },
    { value: 'name', label: 'Name (A-Z)' },
  ]

  return (
    <div className={className}>
      <Card className="p-4 bg-white shadow-lg">
        {/* Main Search Form */}
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
            {/* Search Query */}
            <div className="relative md:col-span-5">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <Input
                type="text"
                placeholder={placeholder}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 h-12 border-gray-200 focus:border-bizbook-primary"
              />
            </div>

            {/* Location */}
            <div className="relative md:col-span-4">
              <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <Input
                type="text"
                placeholder="Enter location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="pl-10 h-12 border-gray-200 focus:border-bizbook-primary"
              />
            </div>

            {/* Search Button & Filters */}
            <div className="md:col-span-3 flex space-x-2">
              <Button 
                type="submit" 
                className="flex-1 h-12 bg-bizbook-primary hover:bg-blue-700"
              >
                <Search className="w-5 h-5 mr-2" />
                Search
              </Button>
              
              {showFilters && (
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
                  className="h-12 px-3 relative"
                >
                  <Filter className="w-5 h-5" />
                  {getActiveFiltersCount() > 0 && (
                    <Badge 
                      variant="destructive" 
                      className="absolute -top-2 -right-2 w-5 h-5 rounded-full p-0 flex items-center justify-center text-xs"
                    >
                      {getActiveFiltersCount()}
                    </Badge>
                  )}
                </Button>
              )}
            </div>
          </div>

          {/* Advanced Filters */}
          {showAdvancedFilters && (
            <div className="border-t pt-4 space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="font-semibold text-gray-900">Filters</h3>
                <div className="flex space-x-2">
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={clearFilters}
                  >
                    <X className="w-4 h-4 mr-1" />
                    Clear All
                  </Button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Category Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Category
                  </label>
                  <select
                    value={filters.category || ''}
                    onChange={(e) => handleFilterChange('category', e.target.value || undefined)}
                    className="w-full p-2 border border-gray-200 rounded-md focus:border-bizbook-primary focus:ring-1 focus:ring-bizbook-primary"
                  >
                    <option value="">All Categories</option>
                    {categories.map((category) => (
                      <option key={category} value={category}>
                        {category}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Rating Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Minimum Rating
                  </label>
                  <select
                    value={filters.rating_min || ''}
                    onChange={(e) => handleFilterChange('rating_min', e.target.value ? Number(e.target.value) : undefined)}
                    className="w-full p-2 border border-gray-200 rounded-md focus:border-bizbook-primary focus:ring-1 focus:ring-bizbook-primary"
                  >
                    <option value="">Any Rating</option>
                    <option value="4.5">4.5+ Stars</option>
                    <option value="4.0">4.0+ Stars</option>
                    <option value="3.5">3.5+ Stars</option>
                    <option value="3.0">3.0+ Stars</option>
                  </select>
                </div>

                {/* Price Range Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Price Range
                  </label>
                  <select
                    value={filters.price_range || ''}
                    onChange={(e) => handleFilterChange('price_range', e.target.value || undefined)}
                    className="w-full p-2 border border-gray-200 rounded-md focus:border-bizbook-primary focus:ring-1 focus:ring-bizbook-primary"
                  >
                    <option value="">Any Price</option>
                    {priceRanges.map((range) => (
                      <option key={range.value} value={range.value}>
                        {range.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Sort By */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Sort By
                  </label>
                  <select
                    value={filters.sort_by || 'relevance'}
                    onChange={(e) => handleFilterChange('sort_by', e.target.value as any)}
                    className="w-full p-2 border border-gray-200 rounded-md focus:border-bizbook-primary focus:ring-1 focus:ring-bizbook-primary"
                  >
                    {sortOptions.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Additional Filters */}
              <div className="space-y-3">
                <h4 className="font-medium text-gray-700">Additional Options</h4>
                <div className="flex flex-wrap gap-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={filters.open_now || false}
                      onChange={(e) => handleFilterChange('open_now', e.target.checked)}
                      className="rounded border-gray-300 text-bizbook-primary focus:ring-bizbook-primary"
                    />
                    <span className="text-sm text-gray-700 flex items-center">
                      <Clock className="w-4 h-4 mr-1" />
                      Open Now
                    </span>
                  </label>

                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={filters.premium_only || false}
                      onChange={(e) => handleFilterChange('premium_only', e.target.checked)}
                      className="rounded border-gray-300 text-bizbook-primary focus:ring-bizbook-primary"
                    />
                    <span className="text-sm text-gray-700 flex items-center">
                      <Star className="w-4 h-4 mr-1" />
                      Premium Only
                    </span>
                  </label>

                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={filters.verification_status === 'verified'}
                      onChange={(e) => handleFilterChange('verification_status', e.target.checked ? 'verified' : undefined)}
                      className="rounded border-gray-300 text-bizbook-primary focus:ring-bizbook-primary"
                    />
                    <span className="text-sm text-gray-700 flex items-center">
                      <Verified className="w-4 h-4 mr-1" />
                      Verified Only
                    </span>
                  </label>
                </div>
              </div>
            </div>
          )}
        </form>
      </Card>
    </div>
  )
}

export default SearchBar