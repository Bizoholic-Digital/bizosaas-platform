'use client'

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  TrendingUp,
  TrendingDown,
  MoreHorizontal,
  X,
  Target,
  Shield,
  Activity,
  DollarSign
} from 'lucide-react'

interface Position {
  id: string
  symbol: string
  side: 'long' | 'short'
  quantity: number
  avgPrice: number
  currentPrice: number
  marketValue: number
  unrealizedPnL: number
  unrealizedPnLPercent: number
  dayChange: number
  dayChangePercent: number
  stopLoss?: number
  takeProfit?: number
  openDate: string
  sector: string
}

const mockPositions: Position[] = [
  {
    id: '1',
    symbol: 'AAPL',
    side: 'long',
    quantity: 100,
    avgPrice: 175.50,
    currentPrice: 182.25,
    marketValue: 18225,
    unrealizedPnL: 675,
    unrealizedPnLPercent: 3.84,
    dayChange: 2.15,
    dayChangePercent: 1.19,
    stopLoss: 170.00,
    takeProfit: 190.00,
    openDate: '2024-01-15',
    sector: 'Technology'
  },
  {
    id: '2',
    symbol: 'MSFT',
    side: 'long',
    quantity: 50,
    avgPrice: 325.80,
    currentPrice: 335.40,
    marketValue: 16770,
    unrealizedPnL: 480,
    unrealizedPnLPercent: 2.95,
    dayChange: -1.25,
    dayChangePercent: -0.37,
    stopLoss: 310.00,
    takeProfit: 350.00,
    openDate: '2024-01-12',
    sector: 'Technology'
  },
  {
    id: '3',
    symbol: 'GOOGL',
    side: 'long',
    quantity: 25,
    avgPrice: 142.30,
    currentPrice: 138.75,
    marketValue: 3468.75,
    unrealizedPnL: -88.75,
    unrealizedPnLPercent: -2.49,
    dayChange: -0.85,
    dayChangePercent: -0.61,
    stopLoss: 135.00,
    openDate: '2024-01-18',
    sector: 'Technology'
  },
  {
    id: '4',
    symbol: 'TSLA',
    side: 'short',
    quantity: 30,
    avgPrice: 245.20,
    currentPrice: 252.10,
    marketValue: 7563,
    unrealizedPnL: -207,
    unrealizedPnLPercent: -2.81,
    dayChange: 5.80,
    dayChangePercent: 2.35,
    stopLoss: 260.00,
    openDate: '2024-01-20',
    sector: 'Automotive'
  },
  {
    id: '5',
    symbol: 'NVDA',
    side: 'long',
    quantity: 15,
    avgPrice: 445.60,
    currentPrice: 458.90,
    marketValue: 6883.50,
    unrealizedPnL: 199.50,
    unrealizedPnLPercent: 2.98,
    dayChange: 12.40,
    dayChangePercent: 2.78,
    takeProfit: 480.00,
    openDate: '2024-01-16',
    sector: 'Technology'
  }
]

export default function PositionsList() {
  const [selectedTab, setSelectedTab] = useState<'all' | 'long' | 'short'>('all')
  const [selectedPosition, setSelectedPosition] = useState<Position | null>(null)

  const filteredPositions = mockPositions.filter(position =>
    selectedTab === 'all' ? true : position.side === selectedTab
  )

  const totalPnL = mockPositions.reduce((sum, pos) => sum + pos.unrealizedPnL, 0)
  const totalValue = mockPositions.reduce((sum, pos) => sum + pos.marketValue, 0)

  const handleClosePosition = (positionId: string) => {
    // Handle position closing logic
    console.log(`Closing position: ${positionId}`)
    setSelectedPosition(null)
  }

  return (
    <div className="px-6 py-4">
      <div className="trading-card">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-4">
            <h3 className="text-lg font-semibold text-white">Open Positions</h3>

            {/* Tab Filters */}
            <div className="flex items-center space-x-1 bg-gray-900 rounded-lg p-1">
              {[
                { key: 'all', label: 'All' },
                { key: 'long' as const, label: 'Long' },
                { key: 'short' as const, label: 'Short' }
              ].map((tab) => (
                <button
                  key={tab.key}
                  onClick={() => setSelectedTab(tab.key)}
                  className={`px-3 py-1 rounded text-sm transition-colors ${
                    selectedTab === tab.key
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-400 hover:text-white hover:bg-gray-700'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Summary Stats */}
          <div className="flex items-center space-x-6 text-sm">
            <div className="text-center">
              <p className="text-gray-400">Total P&L</p>
              <p className={`font-semibold ${totalPnL >= 0 ? 'text-trading-green' : 'text-trading-red'}`}>
                {totalPnL >= 0 ? '+' : ''}${totalPnL.toFixed(2)}
              </p>
            </div>
            <div className="text-center">
              <p className="text-gray-400">Total Value</p>
              <p className="font-semibold text-white">${totalValue.toLocaleString()}</p>
            </div>
            <div className="text-center">
              <p className="text-gray-400">Positions</p>
              <p className="font-semibold text-white">{filteredPositions.length}</p>
            </div>
          </div>
        </div>

        {/* Positions Table */}
        <div className="overflow-x-auto">
          <table className="portfolio-table">
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Side</th>
                <th>Quantity</th>
                <th>Avg Price</th>
                <th>Current Price</th>
                <th>Market Value</th>
                <th>Day Change</th>
                <th>Unrealized P&L</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredPositions.map((position, index) => (
                <motion.tr
                  key={position.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  className="hover:bg-gray-800 transition-colors"
                >
                  <td>
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
                        <span className="text-xs font-bold text-white">
                          {position.symbol.substring(0, 2)}
                        </span>
                      </div>
                      <div>
                        <p className="font-medium text-white">{position.symbol}</p>
                        <p className="text-xs text-gray-400">{position.sector}</p>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      position.side === 'long'
                        ? 'bg-green-900 text-green-400'
                        : 'bg-red-900 text-red-400'
                    }`}>
                      {position.side.toUpperCase()}
                    </span>
                  </td>
                  <td className="text-white font-medium">
                    {position.quantity}
                  </td>
                  <td className="text-white">
                    ${position.avgPrice.toFixed(2)}
                  </td>
                  <td className="text-white font-medium">
                    ${position.currentPrice.toFixed(2)}
                  </td>
                  <td className="text-white font-medium">
                    ${position.marketValue.toLocaleString()}
                  </td>
                  <td>
                    <div className={`flex items-center space-x-1 ${
                      position.dayChange >= 0 ? 'text-trading-green' : 'text-trading-red'
                    }`}>
                      {position.dayChange >= 0 ? (
                        <TrendingUp className="w-3 h-3" />
                      ) : (
                        <TrendingDown className="w-3 h-3" />
                      )}
                      <span className="text-sm">
                        {position.dayChange >= 0 ? '+' : ''}${position.dayChange.toFixed(2)}
                        ({position.dayChangePercent >= 0 ? '+' : ''}{position.dayChangePercent.toFixed(2)}%)
                      </span>
                    </div>
                  </td>
                  <td>
                    <div className={`${
                      position.unrealizedPnL >= 0 ? 'text-trading-green' : 'text-trading-red'
                    }`}>
                      <p className="font-medium">
                        {position.unrealizedPnL >= 0 ? '+' : ''}${position.unrealizedPnL.toFixed(2)}
                      </p>
                      <p className="text-sm">
                        ({position.unrealizedPnLPercent >= 0 ? '+' : ''}{position.unrealizedPnLPercent.toFixed(2)}%)
                      </p>
                    </div>
                  </td>
                  <td>
                    <div className="flex items-center space-x-2">
                      {position.stopLoss && (
                        <div className="text-xs text-gray-400 flex items-center space-x-1">
                          <Shield className="w-3 h-3" />
                          <span>${position.stopLoss}</span>
                        </div>
                      )}
                      {position.takeProfit && (
                        <div className="text-xs text-gray-400 flex items-center space-x-1">
                          <Target className="w-3 h-3" />
                          <span>${position.takeProfit}</span>
                        </div>
                      )}
                      <button
                        onClick={() => setSelectedPosition(position)}
                        className="p-1 rounded hover:bg-gray-700 transition-colors"
                      >
                        <MoreHorizontal className="w-4 h-4 text-gray-400" />
                      </button>
                    </div>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredPositions.length === 0 && (
          <div className="text-center py-8">
            <Activity className="w-12 h-12 text-gray-600 mx-auto mb-3" />
            <p className="text-gray-400">No {selectedTab} positions found</p>
            <p className="text-sm text-gray-500 mt-1">
              Your {selectedTab === 'all' ? '' : selectedTab} positions will appear here
            </p>
          </div>
        )}
      </div>

      {/* Position Details Modal */}
      {selectedPosition && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">
                {selectedPosition.symbol} Position Details
              </h3>
              <button
                onClick={() => setSelectedPosition(null)}
                className="p-1 rounded hover:bg-gray-700"
              >
                <X className="w-5 h-5 text-gray-400" />
              </button>
            </div>

            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-400">Position Size</p>
                  <p className="text-white font-medium">{selectedPosition.quantity} shares</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Side</p>
                  <p className={`font-medium ${
                    selectedPosition.side === 'long' ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {selectedPosition.side.toUpperCase()}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Avg Price</p>
                  <p className="text-white font-medium">${selectedPosition.avgPrice.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Current Price</p>
                  <p className="text-white font-medium">${selectedPosition.currentPrice.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Market Value</p>
                  <p className="text-white font-medium">${selectedPosition.marketValue.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Open Date</p>
                  <p className="text-white font-medium">{new Date(selectedPosition.openDate).toLocaleDateString()}</p>
                </div>
              </div>

              {(selectedPosition.stopLoss || selectedPosition.takeProfit) && (
                <div className="border-t border-gray-700 pt-4">
                  <p className="text-sm text-gray-400 mb-2">Risk Management</p>
                  <div className="grid grid-cols-2 gap-4">
                    {selectedPosition.stopLoss && (
                      <div className="flex items-center space-x-2">
                        <Shield className="w-4 h-4 text-red-400" />
                        <div>
                          <p className="text-xs text-gray-400">Stop Loss</p>
                          <p className="text-red-400 font-medium">${selectedPosition.stopLoss.toFixed(2)}</p>
                        </div>
                      </div>
                    )}
                    {selectedPosition.takeProfit && (
                      <div className="flex items-center space-x-2">
                        <Target className="w-4 h-4 text-green-400" />
                        <div>
                          <p className="text-xs text-gray-400">Take Profit</p>
                          <p className="text-green-400 font-medium">${selectedPosition.takeProfit.toFixed(2)}</p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              <div className="border-t border-gray-700 pt-4">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm text-gray-400">Unrealized P&L</p>
                  <div className={`text-right ${
                    selectedPosition.unrealizedPnL >= 0 ? 'text-trading-green' : 'text-trading-red'
                  }`}>
                    <p className="font-bold">
                      {selectedPosition.unrealizedPnL >= 0 ? '+' : ''}${selectedPosition.unrealizedPnL.toFixed(2)}
                    </p>
                    <p className="text-sm">
                      ({selectedPosition.unrealizedPnLPercent >= 0 ? '+' : ''}{selectedPosition.unrealizedPnLPercent.toFixed(2)}%)
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex space-x-3 pt-4">
                <button className="btn-secondary flex-1">
                  Edit Position
                </button>
                <button
                  onClick={() => handleClosePosition(selectedPosition.id)}
                  className="btn-danger flex-1"
                >
                  Close Position
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  )
}