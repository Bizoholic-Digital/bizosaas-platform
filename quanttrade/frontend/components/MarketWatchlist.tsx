'use client'

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
  Search,
  Star,
  TrendingUp,
  TrendingDown,
  Plus,
  X,
  Activity,
  BarChart3,
  Eye,
  EyeOff
} from 'lucide-react'

interface WatchlistItem {
  symbol: string
  name: string
  price: number
  change: number
  changePercent: number
  volume: number
  marketCap?: string
  sector: string
  isWatched: boolean
  high52Week: number
  low52Week: number
}

const mockWatchlist: WatchlistItem[] = [
  {
    symbol: 'AAPL',
    name: 'Apple Inc.',
    price: 182.25,
    change: 2.15,
    changePercent: 1.19,
    volume: 52485730,
    marketCap: '2.85T',
    sector: 'Technology',
    isWatched: true,
    high52Week: 199.62,
    low52Week: 124.17
  },
  {
    symbol: 'MSFT',
    name: 'Microsoft Corporation',
    price: 335.40,
    change: -1.25,
    changePercent: -0.37,
    volume: 28652140,
    marketCap: '2.49T',
    sector: 'Technology',
    isWatched: true,
    high52Week: 384.52,
    low52Week: 213.43
  },
  {
    symbol: 'GOOGL',
    name: 'Alphabet Inc.',
    price: 138.75,
    change: -0.85,
    changePercent: -0.61,
    volume: 31247580,
    marketCap: '1.75T',
    sector: 'Technology',
    isWatched: true,
    high52Week: 153.78,
    low52Week: 83.45
  },
  {
    symbol: 'TSLA',
    name: 'Tesla Inc.',
    price: 252.10,
    change: 5.80,
    changePercent: 2.35,
    volume: 78965420,
    marketCap: '798.2B',
    sector: 'Automotive',
    isWatched: true,
    high52Week: 299.29,
    low52Week: 101.81
  },
  {
    symbol: 'NVDA',
    name: 'NVIDIA Corporation',
    price: 458.90,
    change: 12.40,
    changePercent: 2.78,
    volume: 45632180,
    marketCap: '1.13T',
    sector: 'Technology',
    isWatched: true,
    high52Week: 502.66,
    low52Week: 180.96
  },
  {
    symbol: 'AMZN',
    name: 'Amazon.com Inc.',
    price: 145.85,
    change: -2.35,
    changePercent: -1.58,
    volume: 38947210,
    marketCap: '1.51T',
    sector: 'Consumer Discretionary',
    isWatched: false,
    high52Week: 170.00,
    low52Week: 81.43
  },
  {
    symbol: 'META',
    name: 'Meta Platforms Inc.',
    price: 298.45,
    change: 4.20,
    changePercent: 1.43,
    volume: 22845630,
    marketCap: '758.3B',
    sector: 'Technology',
    isWatched: false,
    high52Week: 384.33,
    low52Week: 88.09
  },
  {
    symbol: 'AMD',
    name: 'Advanced Micro Devices',
    price: 142.75,
    change: -3.45,
    changePercent: -2.36,
    volume: 65432180,
    marketCap: '230.8B',
    sector: 'Technology',
    isWatched: false,
    high52Week: 227.30,
    low52Week: 93.12
  }
]

interface MarketWatchlistProps {
  onSymbolSelect: (symbol: string) => void
  selectedSymbol: string
}

export default function MarketWatchlist({ onSymbolSelect, selectedSymbol }: MarketWatchlistProps) {
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>(mockWatchlist)
  const [searchQuery, setSearchQuery] = useState('')
  const [showAll, setShowAll] = useState(false)
  const [sortBy, setSortBy] = useState<'symbol' | 'change' | 'volume'>('symbol')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc')

  // Filter and sort watchlist
  const filteredWatchlist = watchlist
    .filter(item => {
      if (!showAll && !item.isWatched) return false
      return item.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
             item.name.toLowerCase().includes(searchQuery.toLowerCase())
    })
    .sort((a, b) => {
      let comparison = 0
      switch (sortBy) {
        case 'symbol':
          comparison = a.symbol.localeCompare(b.symbol)
          break
        case 'change':
          comparison = a.changePercent - b.changePercent
          break
        case 'volume':
          comparison = a.volume - b.volume
          break
      }
      return sortOrder === 'asc' ? comparison : -comparison
    })

  const toggleWatchlist = (symbol: string) => {
    setWatchlist(prev => prev.map(item =>
      item.symbol === symbol
        ? { ...item, isWatched: !item.isWatched }
        : item
    ))
  }

  const handleSort = (field: 'symbol' | 'change' | 'volume') => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(field)
      setSortOrder('asc')
    }
  }

  // Simulate price updates
  useEffect(() => {
    const interval = setInterval(() => {
      setWatchlist(prev => prev.map(item => ({
        ...item,
        price: item.price + (Math.random() - 0.5) * 2,
        change: item.change + (Math.random() - 0.5) * 0.5,
        changePercent: item.changePercent + (Math.random() - 0.5) * 0.2
      })))
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const watchedCount = watchlist.filter(item => item.isWatched).length
  const gainers = filteredWatchlist.filter(item => item.change > 0).length
  const losers = filteredWatchlist.filter(item => item.change < 0).length

  return (
    <div className="trading-card">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-5 h-5 text-blue-400" />
          <h3 className="text-lg font-semibold text-white">Market Watch</h3>
          <div className="text-xs text-gray-400 bg-gray-700 px-2 py-1 rounded">
            {watchedCount} watched
          </div>
        </div>
        <button
          onClick={() => setShowAll(!showAll)}
          className={`p-2 rounded transition-colors ${
            showAll ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          {showAll ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
        </button>
      </div>

      {/* Search */}
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          placeholder="Search symbols..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full bg-gray-700 text-white pl-10 pr-4 py-2 rounded border border-gray-600 focus:border-blue-500 focus:outline-none text-sm"
        />
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-3 gap-2 mb-4 text-xs">
        <div className="bg-gray-900 rounded p-2 text-center">
          <p className="text-gray-400">Total</p>
          <p className="text-white font-medium">{filteredWatchlist.length}</p>
        </div>
        <div className="bg-gray-900 rounded p-2 text-center">
          <p className="text-gray-400">Gainers</p>
          <p className="text-trading-green font-medium">{gainers}</p>
        </div>
        <div className="bg-gray-900 rounded p-2 text-center">
          <p className="text-gray-400">Losers</p>
          <p className="text-trading-red font-medium">{losers}</p>
        </div>
      </div>

      {/* Sort Controls */}
      <div className="flex items-center space-x-2 mb-3 text-xs">
        <span className="text-gray-400">Sort by:</span>
        <button
          onClick={() => handleSort('symbol')}
          className={`px-2 py-1 rounded ${
            sortBy === 'symbol' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
          }`}
        >
          Symbol {sortBy === 'symbol' && (sortOrder === 'asc' ? '↑' : '↓')}
        </button>
        <button
          onClick={() => handleSort('change')}
          className={`px-2 py-1 rounded ${
            sortBy === 'change' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
          }`}
        >
          Change {sortBy === 'change' && (sortOrder === 'asc' ? '↑' : '↓')}
        </button>
        <button
          onClick={() => handleSort('volume')}
          className={`px-2 py-1 rounded ${
            sortBy === 'volume' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
          }`}
        >
          Volume {sortBy === 'volume' && (sortOrder === 'asc' ? '↑' : '↓')}
        </button>
      </div>

      {/* Watchlist Items */}
      <div className="space-y-1 max-h-96 overflow-y-auto">
        {filteredWatchlist.map((item, index) => (
          <motion.div
            key={item.symbol}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.03 }}
            className={`p-3 rounded-lg cursor-pointer transition-all duration-200 ${
              selectedSymbol === item.symbol
                ? 'bg-blue-600 bg-opacity-20 border border-blue-500'
                : 'bg-gray-900 hover:bg-gray-800'
            }`}
            onClick={() => onSymbolSelect(item.symbol)}
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-1">
                  <span className="font-semibold text-white">{item.symbol}</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      toggleWatchlist(item.symbol)
                    }}
                    className={`p-1 rounded transition-colors ${
                      item.isWatched
                        ? 'text-yellow-400 hover:text-yellow-300'
                        : 'text-gray-500 hover:text-gray-400'
                    }`}
                  >
                    <Star className={`w-3 h-3 ${item.isWatched ? 'fill-current' : ''}`} />
                  </button>
                </div>
                <p className="text-xs text-gray-400 truncate">{item.name}</p>
                <div className="flex items-center space-x-2 mt-1">
                  <span className="text-xs text-gray-500">{item.sector}</span>
                  {item.marketCap && (
                    <>
                      <span className="text-gray-600">•</span>
                      <span className="text-xs text-gray-500">{item.marketCap}</span>
                    </>
                  )}
                </div>
              </div>

              <div className="text-right">
                <p className="font-semibold text-white">${item.price.toFixed(2)}</p>
                <div className={`flex items-center justify-end space-x-1 text-sm ${
                  item.change >= 0 ? 'text-trading-green' : 'text-trading-red'
                }`}>
                  {item.change >= 0 ? (
                    <TrendingUp className="w-3 h-3" />
                  ) : (
                    <TrendingDown className="w-3 h-3" />
                  )}
                  <span>
                    {item.change >= 0 ? '+' : ''}${item.change.toFixed(2)}
                  </span>
                </div>
                <p className={`text-xs ${
                  item.changePercent >= 0 ? 'text-trading-green' : 'text-trading-red'
                }`}>
                  ({item.changePercent >= 0 ? '+' : ''}{item.changePercent.toFixed(2)}%)
                </p>
              </div>
            </div>

            {/* Additional Details for Selected Item */}
            {selectedSymbol === item.symbol && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="mt-3 pt-3 border-t border-gray-700"
              >
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <p className="text-gray-400">Volume</p>
                    <p className="text-white">{(item.volume / 1000000).toFixed(1)}M</p>
                  </div>
                  <div>
                    <p className="text-gray-400">52W Range</p>
                    <p className="text-white">
                      ${item.low52Week.toFixed(0)} - ${item.high52Week.toFixed(0)}
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>

      {filteredWatchlist.length === 0 && (
        <div className="text-center py-8">
          <Activity className="w-12 h-12 text-gray-600 mx-auto mb-3" />
          <p className="text-gray-400">No symbols found</p>
          <p className="text-sm text-gray-500 mt-1">
            {showAll ? 'Try adjusting your search' : 'Add symbols to watchlist or show all'}
          </p>
        </div>
      )}

      {/* Add Symbol Button */}
      <div className="mt-4 pt-4 border-t border-gray-700">
        <button className="w-full flex items-center justify-center space-x-2 p-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors text-sm">
          <Plus className="w-4 h-4" />
          <span>Add Symbol</span>
        </button>
      </div>
    </div>
  )
}