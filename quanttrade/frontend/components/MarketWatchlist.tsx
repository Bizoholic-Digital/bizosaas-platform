/**
 * Market Watchlist Component
 * Multi-symbol tracking with real-time updates
 */

'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, X, TrendingUp, TrendingDown, Star, Search } from 'lucide-react'

interface WatchlistItem {
  symbol: string
  price: number
  change: number
  changePercent: number
  volume: number
}

interface MarketWatchlistProps {
  onSymbolSelect?: (symbol: string) => void
}

export default function MarketWatchlist({ onSymbolSelect }: MarketWatchlistProps) {
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([
    { symbol: 'BTCUSDT', price: 43250.50, change: 1250.30, changePercent: 2.98, volume: 125000000 },
    { symbol: 'ETHUSDT', price: 2280.75, change: -45.20, changePercent: -1.94, volume: 85000000 },
    { symbol: 'SOLUSDT', price: 98.45, change: 3.15, changePercent: 3.31, volume: 45000000 },
  ])
  const [searchQuery, setSearchQuery] = useState('')
  const [showAddSymbol, setShowAddSymbol] = useState(false)

  const addSymbol = (symbol: string) => {
    if (!watchlist.find(item => item.symbol === symbol)) {
      setWatchlist([...watchlist, {
        symbol,
        price: 0,
        change: 0,
        changePercent: 0,
        volume: 0
      }])
    }
    setShowAddSymbol(false)
    setSearchQuery('')
  }

  const removeSymbol = (symbol: string) => {
    setWatchlist(watchlist.filter(item => item.symbol !== symbol))
  }

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-white">Market Watchlist</h2>
        <button
          onClick={() => setShowAddSymbol(!showAddSymbol)}
          className="p-2 bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors"
        >
          <Plus className="w-4 h-4 text-white" />
        </button>
      </div>

      {/* Add Symbol Input */}
      <AnimatePresence>
        {showAddSymbol && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="mb-4 overflow-hidden"
          >
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value.toUpperCase())}
                onKeyPress={(e) => e.key === 'Enter' && searchQuery && addSymbol(searchQuery)}
                placeholder="Enter symbol (e.g., BTCUSDT)"
                className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Watchlist Items */}
      <div className="space-y-2">
        <AnimatePresence>
          {watchlist.map((item) => {
            const isPositive = item.change >= 0
            
            return (
              <motion.div
                key={item.symbol}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors cursor-pointer group"
                onClick={() => onSymbolSelect?.(item.symbol)}
              >
                <div className="flex items-center justify-between">
                  {/* Symbol */}
                  <div className="flex items-center space-x-3">
                    <Star className="w-4 h-4 text-yellow-500" />
                    <div>
                      <div className="font-semibold text-white">{item.symbol}</div>
                      <div className="text-xs text-gray-400">
                        Vol: {(item.volume / 1000000).toFixed(2)}M
                      </div>
                    </div>
                  </div>

                  {/* Price */}
                  <div className="text-center">
                    <div className="font-semibold text-white">
                      ${item.price.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    </div>
                    <div className={`flex items-center space-x-1 text-sm ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
                      {isPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                      <span>
                        {isPositive ? '+' : ''}{item.change.toFixed(2)}
                      </span>
                    </div>
                  </div>

                  {/* Change % */}
                  <div className="text-right">
                    <div className={`text-lg font-bold ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
                      {isPositive ? '+' : ''}{item.changePercent.toFixed(2)}%
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        removeSymbol(item.symbol)
                      }}
                      className="opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <X className="w-4 h-4 text-gray-400 hover:text-red-400" />
                    </button>
                  </div>
                </div>
              </motion.div>
            )
          })}
        </AnimatePresence>
      </div>

      {/* Empty State */}
      {watchlist.length === 0 && (
        <div className="text-center py-12">
          <Star className="w-12 h-12 text-gray-600 mx-auto mb-3" />
          <p className="text-gray-400">No symbols in watchlist</p>
          <p className="text-sm text-gray-500 mt-1">Click + to add symbols</p>
        </div>
      )}
    </div>
  )
}