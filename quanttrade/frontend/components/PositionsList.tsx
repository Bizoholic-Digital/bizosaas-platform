/**
 * Enhanced Positions List Component
 * Real-time positions with Greeks and P&L tracking
 */

'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  TrendingUp,
  TrendingDown,
  X,
  ChevronDown,
  ChevronUp,
  Activity,
} from 'lucide-react'
import { usePortfolioWebSocket } from '@/hooks/useWebSocket'

interface PositionsListProps {
  accountId: string
}

export default function PositionsList({ accountId }: PositionsListProps) {
  const { positions, isConnected } = usePortfolioWebSocket(accountId)
  const [expandedPosition, setExpandedPosition] = useState<string | null>(null)
  const [sortBy, setSortBy] = useState<'symbol' | 'pnl' | 'size'>('pnl')

  const sortedPositions = React.useMemo(() => {
    if (!positions) return []
    
    return [...positions].sort((a, b) => {
      switch (sortBy) {
        case 'symbol':
          return a.symbol.localeCompare(b.symbol)
        case 'pnl':
          return (b.unrealized_pnl || 0) - (a.unrealized_pnl || 0)
        case 'size':
          return (b.quantity * b.current_price) - (a.quantity * a.current_price)
        default:
          return 0
      }
    })
  }, [positions, sortBy])

  const formatCurrency = (value: number) => {
    return `$${Math.abs(value).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
  }

  const formatPercent = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`
  }

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <h2 className="text-xl font-bold text-white">Open Positions</h2>
          <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-sm rounded">
            {positions?.length || 0}
          </span>
        </div>
        
        {/* Sort Options */}
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-400">Sort by:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="bg-gray-800 text-white text-sm rounded px-3 py-1 border border-gray-700 focus:outline-none focus:border-blue-500"
          >
            <option value="pnl">P&L</option>
            <option value="symbol">Symbol</option>
            <option value="size">Size</option>
          </select>
        </div>
      </div>

      {/* Positions List */}
      <div className="space-y-2">
        <AnimatePresence>
          {sortedPositions.map((position) => {
            const isExpanded = expandedPosition === position.id
            const isProfitable = (position.unrealized_pnl || 0) >= 0

            return (
              <motion.div
                key={position.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden hover:border-gray-600 transition-colors"
              >
                {/* Main Row */}
                <div
                  className="p-4 cursor-pointer"
                  onClick={() => setExpandedPosition(isExpanded ? null : position.id)}
                >
                  <div className="flex items-center justify-between">
                    {/* Symbol & Side */}
                    <div className="flex items-center space-x-3">
                      <div className={`px-2 py-1 rounded text-xs font-semibold ${
                        position.side === 'buy' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                      }`}>
                        {position.side.toUpperCase()}
                      </div>
                      <div>
                        <div className="font-semibold text-white">{position.symbol}</div>
                        <div className="text-sm text-gray-400">
                          {position.quantity} @ {formatCurrency(position.entry_price)}
                        </div>
                      </div>
                    </div>

                    {/* Current Price */}
                    <div className="text-center">
                      <div className="text-sm text-gray-400">Current</div>
                      <div className="font-semibold text-white">
                        {formatCurrency(position.current_price)}
                      </div>
                    </div>

                    {/* P&L */}
                    <div className="text-right">
                      <div className={`text-lg font-bold ${isProfitable ? 'text-green-400' : 'text-red-400'}`}>
                        {isProfitable ? '+' : ''}{formatCurrency(position.unrealized_pnl || 0)}
                      </div>
                      <div className={`text-sm ${isProfitable ? 'text-green-400' : 'text-red-400'}`}>
                        {formatPercent(position.unrealized_pnl_percent || 0)}
                      </div>
                    </div>

                    {/* Expand Icon */}
                    <div>
                      {isExpanded ? (
                        <ChevronUp className="w-5 h-5 text-gray-400" />
                      ) : (
                        <ChevronDown className="w-5 h-5 text-gray-400" />
                      )}
                    </div>
                  </div>
                </div>

                {/* Expanded Details */}
                <AnimatePresence>
                  {isExpanded && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="border-t border-gray-700"
                    >
                      <div className="p-4 space-y-3">
                        {/* Greeks (for options) */}
                        {position.delta !== null && (
                          <div>
                            <div className="text-sm font-semibold text-gray-400 mb-2">Greeks</div>
                            <div className="grid grid-cols-4 gap-4">
                              <div>
                                <div className="text-xs text-gray-500">Delta</div>
                                <div className="text-sm font-semibold text-white">
                                  {position.delta?.toFixed(4)}
                                </div>
                              </div>
                              <div>
                                <div className="text-xs text-gray-500">Gamma</div>
                                <div className="text-sm font-semibold text-white">
                                  {position.gamma?.toFixed(4)}
                                </div>
                              </div>
                              <div>
                                <div className="text-xs text-gray-500">Theta</div>
                                <div className="text-sm font-semibold text-white">
                                  {position.theta?.toFixed(4)}
                                </div>
                              </div>
                              <div>
                                <div className="text-xs text-gray-500">Vega</div>
                                <div className="text-sm font-semibold text-white">
                                  {position.vega?.toFixed(4)}
                                </div>
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Position Details */}
                        <div className="grid grid-cols-3 gap-4">
                          <div>
                            <div className="text-xs text-gray-500">Position Value</div>
                            <div className="text-sm font-semibold text-white">
                              {formatCurrency(position.quantity * position.current_price)}
                            </div>
                          </div>
                          <div>
                            <div className="text-xs text-gray-500">Opened</div>
                            <div className="text-sm font-semibold text-white">
                              {new Date(position.opened_at).toLocaleDateString()}
                            </div>
                          </div>
                          <div>
                            <div className="text-xs text-gray-500">IV</div>
                            <div className="text-sm font-semibold text-white">
                              {position.implied_volatility ? `${(position.implied_volatility * 100).toFixed(2)}%` : 'N/A'}
                            </div>
                          </div>
                        </div>

                        {/* Actions */}
                        <div className="flex items-center space-x-2 pt-2">
                          <button className="flex-1 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded font-semibold transition-colors">
                            Close Position
                          </button>
                          <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded font-semibold transition-colors">
                            Adjust
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )
          })}
        </AnimatePresence>

        {/* Empty State */}
        {(!positions || positions.length === 0) && (
          <div className="text-center py-12">
            <Activity className="w-12 h-12 text-gray-600 mx-auto mb-3" />
            <p className="text-gray-400">No open positions</p>
            <p className="text-sm text-gray-500 mt-1">
              Your positions will appear here when you open trades
            </p>
          </div>
        )}
      </div>
    </div>
  )
}