"use client"

import { useState, useEffect, useCallback, useMemo } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { 
  Search, 
  MapPin, 
  Star, 
  Globe, 
  Phone, 
  Clock, 
  Filter, 
  ChevronDown,
  ChevronUp,
  Zap,
  Shield,
  Award,
  AlertCircle,
  Loader2
} from "lucide-react"
import { 
  BusinessListing,
  searchBusinesses,
  getBusinessFacets,
  getBusinessSuggestions,
  initializeMeilisearch,
  indexBusinessListings,
  mockBusinessListings
} from "@/lib/meilisearch"
import { useDebounce } from "@/hooks/use-debounce"

interface BusinessDirectoryProps {
  initialListings?: BusinessListing[]
  enableMockData?: boolean
}

export function BusinessDirectory({ initialListings, enableMockData = true }: BusinessDirectoryProps) {
  // State management
  const [searchQuery, setSearchQuery] = useState("")
  const [businesses, setBusinesses] = useState<BusinessListing[]>([])
  const [filteredBusinesses, setFilteredBusinesses] = useState<BusinessListing[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isInitializing, setIsInitializing] = useState(true)
  const [error, setError] = useState<string>("")
  const [suggestions, setSuggestions] = useState<any[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [facets, setFacets] = useState<any>({})
  
  // Filters
  const [selectedCategory, setSelectedCategory] = useState<string>("")
  const [onlyVerified, setOnlyVerified] = useState(false)
  const [onlyPremium, setOnlyPremium] = useState(false)
  const [onlyAiEnhanced, setOnlyAiEnhanced] = useState(false)
  const [minRating, setMinRating] = useState<number>(0)
  const [showFilters, setShowFilters] = useState(false)
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1)
  const [totalHits, setTotalHits] = useState(0)
  const [processingTime, setProcessingTime] = useState(0)
  const itemsPerPage = 10

  // Debounced search query
  const debouncedSearchQuery = useDebounce(searchQuery, 300)

  // Categories for filtering
  const categories = [
    "All Categories",
    "Restaurants",
    "Technology", 
    "Health & Beauty",
    "Cafes",
    "Automotive",
    "Retail",
    "Professional Services",
    "Entertainment",
    "Real Estate"
  ]

  // Initialize Meilisearch and load data
  useEffect(() => {
    const initializeSearch = async () => {
      try {
        setIsInitializing(true)
        setError("")

        if (enableMockData) {
          // Use mock data for development
          console.log("Using mock business data")
          setBusinesses(mockBusinessListings)
          setFilteredBusinesses(mockBusinessListings)
          setTotalHits(mockBusinessListings.length)
        } else {
          // Initialize Meilisearch
          const initialized = await initializeMeilisearch()
          
          if (initialized) {
            // Index initial data if provided
            if (initialListings && initialListings.length > 0) {
              await indexBusinessListings(initialListings)
            } else if (mockBusinessListings.length > 0) {
              await indexBusinessListings(mockBusinessListings)
            }
            
            // Load facets
            const facetData = await getBusinessFacets()
            setFacets(facetData)
            
            // Perform initial search
            await performSearch("")
          } else {
            throw new Error("Failed to initialize search service")
          }
        }
      } catch (err) {
        console.error("Initialization error:", err)
        setError("Failed to initialize search. Using offline mode.")
        // Fallback to mock data
        setBusinesses(mockBusinessListings)
        setFilteredBusinesses(mockBusinessListings)
        setTotalHits(mockBusinessListings.length)
      } finally {
        setIsInitializing(false)
      }
    }

    initializeSearch()
  }, [initialListings, enableMockData])

  // Perform search with Meilisearch or local filtering
  const performSearch = useCallback(async (query: string, page = 1) => {
    try {
      setIsLoading(true)
      setError("")

      if (enableMockData) {
        // Local filtering for mock data
        let filtered = mockBusinessListings

        // Text search
        if (query.trim()) {
          const searchTerm = query.toLowerCase()
          filtered = filtered.filter(business => 
            business.name.toLowerCase().includes(searchTerm) ||
            business.description.toLowerCase().includes(searchTerm) ||
            business.address.toLowerCase().includes(searchTerm) ||
            business.category.toLowerCase().includes(searchTerm) ||
            business.tags?.some(tag => tag.toLowerCase().includes(searchTerm))
          )
        }

        // Category filter
        if (selectedCategory && selectedCategory !== "All Categories") {
          filtered = filtered.filter(business => 
            business.category === selectedCategory
          )
        }

        // Other filters
        if (onlyVerified) {
          filtered = filtered.filter(business => business.verified)
        }
        
        if (onlyPremium) {
          filtered = filtered.filter(business => business.premium)
        }
        
        if (onlyAiEnhanced) {
          filtered = filtered.filter(business => business.aiEnhanced)
        }
        
        if (minRating > 0) {
          filtered = filtered.filter(business => business.rating >= minRating)
        }

        // Sort: premium first, then by rating
        filtered.sort((a, b) => {
          if (a.premium && !b.premium) return -1
          if (!a.premium && b.premium) return 1
          return b.rating - a.rating
        })

        setFilteredBusinesses(filtered)
        setTotalHits(filtered.length)
        setProcessingTime(Math.random() * 50) // Mock processing time
      } else {
        // Use Meilisearch
        const results = await searchBusinesses({
          query,
          category: selectedCategory && selectedCategory !== "All Categories" ? selectedCategory : undefined,
          verified: onlyVerified || undefined,
          premium: onlyPremium || undefined,
          aiEnhanced: onlyAiEnhanced || undefined,
          minRating: minRating > 0 ? minRating : undefined,
          limit: itemsPerPage,
          offset: (page - 1) * itemsPerPage
        })

        setFilteredBusinesses(results.hits)
        setTotalHits(results.totalHits)
        setProcessingTime(results.processingTimeMs)
      }
    } catch (err) {
      console.error("Search error:", err)
      setError("Search failed. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }, [selectedCategory, onlyVerified, onlyPremium, onlyAiEnhanced, minRating, itemsPerPage, enableMockData])

  // Handle search suggestions
  const handleSuggestions = useCallback(async (query: string) => {
    if (!query || query.length < 2 || enableMockData) {
      setSuggestions([])
      return
    }

    try {
      const suggestionResults = await getBusinessSuggestions(query)
      setSuggestions(suggestionResults)
    } catch (err) {
      console.error("Suggestions error:", err)
      setSuggestions([])
    }
  }, [enableMockData])

  // Effect for debounced search
  useEffect(() => {
    if (!isInitializing) {
      performSearch(debouncedSearchQuery, 1)
      setCurrentPage(1)
    }
  }, [debouncedSearchQuery, performSearch, isInitializing])

  // Effect for filters
  useEffect(() => {
    if (!isInitializing) {
      performSearch(debouncedSearchQuery, 1)
      setCurrentPage(1)
    }
  }, [selectedCategory, onlyVerified, onlyPremium, onlyAiEnhanced, minRating, performSearch, isInitializing])

  // Handle search input
  const handleSearchChange = (value: string) => {
    setSearchQuery(value)
    if (value.length >= 2) {
      handleSuggestions(value)
      setShowSuggestions(true)
    } else {
      setShowSuggestions(false)
    }
  }

  // Handle suggestion selection
  const handleSuggestionSelect = (suggestion: any) => {
    setSearchQuery(suggestion.name)
    setShowSuggestions(false)
  }

  // Clear all filters
  const clearFilters = () => {
    setSelectedCategory("")
    setOnlyVerified(false)
    setOnlyPremium(false)
    setOnlyAiEnhanced(false)
    setMinRating(0)
    setSearchQuery("")
  }

  // Pagination
  const totalPages = Math.ceil(totalHits / itemsPerPage)
  const handlePageChange = (page: number) => {
    setCurrentPage(page)
    performSearch(debouncedSearchQuery, page)
  }

  // Loading skeleton
  const LoadingSkeleton = () => (
    <div className="space-y-4">
      {Array.from({ length: 5 }).map((_, i) => (
        <Card key={i}>
          <CardHeader>
            <Skeleton className="h-6 w-1/3" />
            <Skeleton className="h-4 w-1/4" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-3/4" />
          </CardContent>
        </Card>
      ))}
    </div>
  )

  if (isInitializing) {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-2" />
          <p className="text-muted-foreground">Initializing business directory...</p>
        </div>
        <LoadingSkeleton />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Search Header */}
      <div className="space-y-4">
        {error && (
          <Alert>
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Search Bar */}
        <div className="relative">
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search businesses, services, locations..."
              value={searchQuery}
              onChange={(e) => handleSearchChange(e.target.value)}
              className="pl-10"
            />
          </div>
          
          {/* Search Suggestions */}
          {showSuggestions && suggestions.length > 0 && (
            <div className="absolute z-10 w-full mt-1 bg-white border rounded-md shadow-lg">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion.id}
                  onClick={() => handleSuggestionSelect(suggestion)}
                  className="w-full px-4 py-2 text-left hover:bg-gray-50 border-b last:border-b-0"
                >
                  <div className="font-medium" dangerouslySetInnerHTML={{ __html: suggestion.highlighted }} />
                  <div className="text-sm text-muted-foreground">{suggestion.category}</div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Filters */}
        <div className="flex items-center justify-between">
          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
            className="gap-2"
          >
            <Filter className="h-4 w-4" />
            Filters
            {showFilters ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </Button>
          
          <div className="text-sm text-muted-foreground">
            {totalHits} results {processingTime > 0 && `in ${processingTime.toFixed(1)}ms`}
          </div>
        </div>

        {/* Filter Panel */}
        {showFilters && (
          <Card>
            <CardContent className="p-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Category Filter */}
                <div className="space-y-2">
                  <Label htmlFor="category">Category</Label>
                  <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                    <SelectTrigger>
                      <SelectValue placeholder="All Categories" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((category) => (
                        <SelectItem key={category} value={category === "All Categories" ? "" : category}>
                          {category}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Rating Filter */}
                <div className="space-y-2">
                  <Label htmlFor="rating">Minimum Rating</Label>
                  <Select value={minRating.toString()} onValueChange={(value) => setMinRating(Number(value))}>
                    <SelectTrigger>
                      <SelectValue placeholder="Any Rating" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0">Any Rating</SelectItem>
                      <SelectItem value="3">3+ Stars</SelectItem>
                      <SelectItem value="4">4+ Stars</SelectItem>
                      <SelectItem value="4.5">4.5+ Stars</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Checkboxes */}
                <div className="space-y-2">
                  <Label>Features</Label>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="verified"
                        checked={onlyVerified}
                        onCheckedChange={(checked) => setOnlyVerified(checked === true)}
                      />
                      <Label htmlFor="verified" className="text-sm">Verified</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="premium"
                        checked={onlyPremium}
                        onCheckedChange={(checked) => setOnlyPremium(checked === true)}
                      />
                      <Label htmlFor="premium" className="text-sm">Premium</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="ai-enhanced"
                        checked={onlyAiEnhanced}
                        onCheckedChange={(checked) => setOnlyAiEnhanced(checked === true)}
                      />
                      <Label htmlFor="ai-enhanced" className="text-sm">AI Enhanced</Label>
                    </div>
                  </div>
                </div>

                {/* Clear Filters */}
                <div className="space-y-2">
                  <Label>&nbsp;</Label>
                  <Button variant="outline" onClick={clearFilters} className="w-full">
                    Clear Filters
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Business Listings */}
      <div className="space-y-4">
        {isLoading ? (
          <LoadingSkeleton />
        ) : filteredBusinesses.length === 0 ? (
          <div className="text-center py-12">
            <Search className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No businesses found</h3>
            <p className="text-muted-foreground">Try adjusting your search or filters</p>
          </div>
        ) : (
          filteredBusinesses.map((business) => (
            <Card key={business.id} className="hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <CardTitle className="text-lg">{business.name}</CardTitle>
                      {business.verified && (
                        <Badge variant="secondary" className="text-xs">
                          <Shield className="w-3 h-3 mr-1" />
                          Verified
                        </Badge>
                      )}
                      {business.premium && (
                        <Badge className="text-xs bg-gradient-to-r from-yellow-400 to-orange-500">
                          <Award className="w-3 h-3 mr-1" />
                          Premium
                        </Badge>
                      )}
                      {business.aiEnhanced && (
                        <Badge variant="outline" className="text-xs">
                          <Zap className="w-3 h-3 mr-1" />
                          AI Enhanced
                        </Badge>
                      )}
                    </div>
                    <CardDescription className="flex items-center gap-4">
                      <span className="font-medium">{business.category}</span>
                      <div className="flex items-center gap-1">
                        <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                        <span>{business.rating}</span>
                        <span className="text-muted-foreground">({business.reviews} reviews)</span>
                      </div>
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">{business.description}</p>
                
                <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <MapPin className="w-4 h-4" />
                    {business.address}
                  </div>
                  <div className="flex items-center gap-1">
                    <Phone className="w-4 h-4" />
                    {business.phone}
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    {business.hours}
                  </div>
                  {business.website && (
                    <div className="flex items-center gap-1">
                      <Globe className="w-4 h-4" />
                      <a 
                        href={business.website} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-primary hover:underline"
                      >
                        Visit Website
                      </a>
                    </div>
                  )}
                </div>

                {business.tags && business.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-3">
                    {business.tags.map((tag) => (
                      <Badge key={tag} variant="outline" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage <= 1}
          >
            Previous
          </Button>
          
          <div className="flex items-center gap-1">
            {Array.from({ length: Math.min(totalPages, 5) }).map((_, i) => {
              const page = i + 1
              return (
                <Button
                  key={page}
                  variant={currentPage === page ? "default" : "outline"}
                  size="sm"
                  onClick={() => handlePageChange(page)}
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
            disabled={currentPage >= totalPages}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  )
}