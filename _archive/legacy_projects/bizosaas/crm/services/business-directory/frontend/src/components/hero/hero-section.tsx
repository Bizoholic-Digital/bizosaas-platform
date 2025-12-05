'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import { Search, MapPin, TrendingUp, Users, Star, ArrowRight } from 'lucide-react'

interface HeroSectionProps {
  onSearch: (query: string, location: string) => void
  totalBusinesses?: number
  totalCategories?: number
  totalReviews?: number
}

const HeroSection = ({ 
  onSearch, 
  totalBusinesses = 0, 
  totalCategories = 0, 
  totalReviews = 0 
}: HeroSectionProps) => {
  const [searchQuery, setSearchQuery] = useState('')
  const [location, setLocation] = useState('')

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    onSearch(searchQuery, location)
  }

  const popularSearches = [
    'Restaurants', 'Coffee Shops', 'Gyms', 'Beauty Salons', 
    'Auto Repair', 'Dentists', 'Hotels', 'Shopping'
  ]

  return (
    <section className="relative bg-gradient-to-br from-bizbook-primary via-blue-600 to-purple-700 text-white overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-black/20">
        <div className="absolute inset-0" style={{backgroundImage: "url('data:image/svg+xml,%3Csvg width=\"60\" height=\"60\" viewBox=\"0 0 60 60\" xmlns=\"http://www.w3.org/2000/svg\"%3E%3Cg fill=\"none\" fill-rule=\"evenodd\"%3E%3Cg fill=\"%23ffffff\" fill-opacity=\"0.1\"%3E%3Ccircle cx=\"7\" cy=\"7\" r=\"1\"/%3E%3Ccircle cx=\"27\" cy=\"7\" r=\"1\"/%3E%3Ccircle cx=\"47\" cy=\"7\" r=\"1\"/%3E%3Ccircle cx=\"7\" cy=\"27\" r=\"1\"/%3E%3Ccircle cx=\"27\" cy=\"27\" r=\"1\"/%3E%3Ccircle cx=\"47\" cy=\"27\" r=\"1\"/%3E%3Ccircle cx=\"7\" cy=\"47\" r=\"1\"/%3E%3Ccircle cx=\"27\" cy=\"47\" r=\"1\"/%3E%3Ccircle cx=\"47\" cy=\"47\" r=\"1\"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')", opacity: 0.2}} />
      </div>

      <div className="container mx-auto px-4 relative">
        <div className="py-20 lg:py-32">
          <div className="max-w-4xl mx-auto text-center">
            {/* Main Heading */}
            <div className="space-y-6 mb-12">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
                Discover Amazing
                <span className="block text-bizbook-secondary">Local Businesses</span>
              </h1>
              <p className="text-xl md:text-2xl text-blue-100 max-w-3xl mx-auto">
                Find the perfect local business for your needs. Explore reviews, compare services, 
                and connect with trusted businesses in your community.
              </p>
            </div>

            {/* Search Form */}
            <Card className="p-6 bg-white/95 backdrop-blur-sm shadow-2xl max-w-4xl mx-auto mb-12">
              <form onSubmit={handleSearch} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* What are you looking for? */}
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <Input
                      type="text"
                      placeholder="What are you looking for?"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10 h-12 text-gray-900 border-gray-200 focus:border-bizbook-primary"
                    />
                  </div>

                  {/* Location */}
                  <div className="relative">
                    <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <Input
                      type="text"
                      placeholder="Enter location"
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                      className="pl-10 h-12 text-gray-900 border-gray-200 focus:border-bizbook-primary"
                    />
                  </div>

                  {/* Search Button */}
                  <Button 
                    type="submit" 
                    size="lg" 
                    className="h-12 bg-bizbook-primary hover:bg-blue-700 text-white font-semibold"
                  >
                    <Search className="w-5 h-5 mr-2" />
                    Search Now
                  </Button>
                </div>

                {/* Popular Searches */}
                <div className="text-left">
                  <p className="text-sm text-gray-600 mb-2">Popular searches:</p>
                  <div className="flex flex-wrap gap-2">
                    {popularSearches.map((term, index) => (
                      <button
                        key={index}
                        type="button"
                        onClick={() => setSearchQuery(term)}
                        className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-bizbook-primary hover:text-white transition-colors"
                      >
                        {term}
                      </button>
                    ))}
                  </div>
                </div>
              </form>
            </Card>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  <TrendingUp className="w-8 h-8 text-bizbook-secondary mr-2" />
                </div>
                <div className="text-3xl font-bold text-white mb-1">
                  {totalBusinesses.toLocaleString()}+
                </div>
                <p className="text-blue-100">Registered Businesses</p>
              </div>
              
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  <Users className="w-8 h-8 text-bizbook-secondary mr-2" />
                </div>
                <div className="text-3xl font-bold text-white mb-1">
                  {totalCategories}+
                </div>
                <p className="text-blue-100">Business Categories</p>
              </div>
              
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  <Star className="w-8 h-8 text-bizbook-secondary mr-2" />
                </div>
                <div className="text-3xl font-bold text-white mb-1">
                  {totalReviews.toLocaleString()}+
                </div>
                <p className="text-blue-100">Customer Reviews</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Wave */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1200 120" preserveAspectRatio="none" className="w-full h-12">
          <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" className="fill-white"></path>
          <path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" className="fill-white"></path>
          <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" className="fill-white"></path>
        </svg>
      </div>
    </section>
  )
}

export default HeroSection