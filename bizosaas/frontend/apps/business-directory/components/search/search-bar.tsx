'use client';

import React, { useState } from 'react';
import { Search, MapPin, Filter } from 'lucide-react';
import { Button, Input, Card } from '@bizoholic-digital/ui-components';
import { SearchFilters } from '@/types/business';

interface SearchBarProps {
  onSearch: (filters: SearchFilters) => void;
  initialFilters?: SearchFilters;
  className?: string;
}

export function SearchBar({ onSearch, initialFilters, className }: SearchBarProps) {
  const [filters, setFilters] = useState<SearchFilters>(
    initialFilters || {
      query: '',
      location: '',
    }
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(filters);
  };

  const handleInputChange = (field: keyof SearchFilters, value: string) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <Card className={`search-card ${className || ''}`}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search Query */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <Input
              type="text"
              placeholder="Search businesses, services, or products..."
              value={filters.query}
              onChange={(e) => handleInputChange('query', e.target.value)}
              className="pl-10"
            />
          </div>

          {/* Location */}
          <div className="relative md:w-64">
            <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <Input
              type="text"
              placeholder="Location"
              value={filters.location || ''}
              onChange={(e) => handleInputChange('location', e.target.value)}
              className="pl-10"
            />
          </div>

          {/* Search Button */}
          <Button type="submit" className="md:w-auto w-full">
            <Search className="w-4 h-4 mr-2" />
            Search
          </Button>
        </div>

        {/* Quick Filters */}
        <div className="flex flex-wrap gap-2">
          <span className="text-sm text-gray-600 dark:text-gray-400 self-center">
            Quick filters:
          </span>
          {['Restaurants', 'Healthcare', 'Retail', 'Services'].map((category) => (
            <Button
              key={category}
              type="button"
              variant="outline"
              size="sm"
              onClick={() => {
                setFilters(prev => ({ ...prev, category: category.toLowerCase() }));
                onSearch({ ...filters, category: category.toLowerCase() });
              }}
              className="text-xs"
            >
              {category}
            </Button>
          ))}
          
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => {
              setFilters(prev => ({ ...prev, openNow: !prev.openNow }));
              onSearch({ ...filters, openNow: !filters.openNow });
            }}
            className="text-xs"
          >
            <Clock className="w-3 h-3 mr-1" />
            Open Now
          </Button>
          
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => {
              setFilters(prev => ({ ...prev, featured: !prev.featured }));
              onSearch({ ...filters, featured: !filters.featured });
            }}
            className="text-xs"
          >
            Featured
          </Button>
        </div>

        {/* Advanced Filters Toggle */}
        <div className="border-t pt-4">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="text-sm text-gray-600 dark:text-gray-400"
          >
            <Filter className="w-4 h-4 mr-2" />
            Advanced Filters
          </Button>
        </div>
      </form>
    </Card>
  );
}

// Clock icon for "Open Now" filter
function Clock({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle cx="12" cy="12" r="10"></circle>
      <polyline points="12,6 12,12 16,14"></polyline>
    </svg>
  );
}