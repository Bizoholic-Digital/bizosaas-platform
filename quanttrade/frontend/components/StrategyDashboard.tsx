/**
 * Strategy Dashboard Component
 * Manage and monitor trading strategies
 */

'use client'

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Play,
  Pause,
  Settings,
  TrendingUp,
  TrendingDown,
  Activity,
  Target,
  BarChart3,
} from 'lucide-react'
import apiClient from '@/utils/api-client'

interface Strategy {
  id: string
  name: string
  status: 'active' | 'paused' | 'stopped'
  performance: number
  totalTrades: number
  winRate: number
  sharpeRatio: number
  maxDrawdown: number
}

interface StrategyDashboardProps {
  accountId: string
}

export default function StrategyDashboard({ accountId }: StrategyDashboardProps) {
  const [strategies, setStrategies] = useState<Strategy[]>([
    {
      id: '1',
      name: 'RSI Momentum',
      status: 'active',
      performance: 12.4,
      totalTrades: 23,
      winRate: 78,
      sharpeRatio: 1.85,
      maxDrawdown: -4.2,
    },
    {
      id: '2',
      name: 'Mean Reversion',
      status: 'active',
      performance: 8.7,
      totalTrades: 15,
      winRate: 67,
      sharpeRatio: 1.42,
      maxDrawdown: -6.1,
    },
    {
      id: '3',
      name: 'Breakout Scanner',
      status: 'paused',
      performance: 5.2,
      totalTrades: 8,
      winRate: 63,
      sharpeRatio: 1.15,
      maxDrawdown: -8.3,
    },
  ])

  const toggleStrategy = async (strategyId: string) => {
    const strategy = strategies.find(s => s.id === strategyId)
    if (!strategy) return

    const newStatus = strategy.status === 'active' ? 'paused' : 'active'
    
    try {
      if (newStatus === 'active') {
        await apiClient.activateStrategy(strategyId)
      } else {
        await apiClient.deactivateStrategy(strategyId)
      }

      setStrategies(strategies.map(s =>
        s.id === strategyId ? { ...s, status: newStatus } : s
      ))
    } catch (error) {
      console.error('Failed to toggle strategy:', error)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-500/20 text-green-400 border-green-500'
      case 'paused':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500'
      case 'stopped':
        return 'bg-red-500/20 text-red-400 border-red-500'
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500'
    }
  }

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-white">AI Trading Strategies</h2>
        <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors">
          + New Strategy
        </button>
      </div>

      {/* Strategies Grid */}
      <div className="space-y-4">
        <AnimatePresence>
          {strategies.map((strategy, index) => {
            const isPositive = strategy.performance >= 0

            return (
              <motion.div
                key={strategy.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ delay: index * 0.1 }}
                className="bg-gray-800 rounded-lg border border-gray-700 p-6 hover:border-gray-600 transition-colors"
              >
                <div className="flex items-start justify-between mb-4">
                  {/* Strategy Info */}
                  <div className="flex items-start space-x-4">
                    <div className="p-3 bg-blue-500/20 rounded-lg">
                      <Activity className="w-6 h-6 text-blue-400" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-white mb-1">{strategy.name}</h3>
                      <div className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold border ${getStatusColor(strategy.status)}`}>
                        {strategy.status.toUpperCase()}
                      </div>
                    </div>
                  </div>

                  {/* Performance */}
                  <div className="text-right">
                    <div className={`text-2xl font-bold ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
                      {isPositive ? '+' : ''}{strategy.performance.toFixed(2)}%
                    </div>
                    <div className="text-sm text-gray-400">Total Return</div>
                  </div>
                </div>

                {/* Metrics Grid */}
                <div className="grid grid-cols-4 gap-4 mb-4">
                  <div className="bg-gray-900 rounded p-3">
                    <div className="flex items-center space-x-2 mb-1">
                      <BarChart3 className="w-4 h-4 text-gray-400" />
                      <span className="text-xs text-gray-400">Trades</span>
                    </div>
                    <div className="text-lg font-semibold text-white">{strategy.totalTrades}</div>
                  </div>
                  <div className="bg-gray-900 rounded p-3">
                    <div className="flex items-center space-x-2 mb-1">
                      <Target className="w-4 h-4 text-gray-400" />
                      <span className="text-xs text-gray-400">Win Rate</span>
                    </div>
                    <div className="text-lg font-semibold text-white">{strategy.winRate}%</div>
                  </div>
                  <div className="bg-gray-900 rounded p-3">
                    <div className="flex items-center space-x-2 mb-1">
                      <TrendingUp className="w-4 h-4 text-gray-400" />
                      <span className="text-xs text-gray-400">Sharpe</span>
                    </div>
                    <div className="text-lg font-semibold text-white">{strategy.sharpeRatio.toFixed(2)}</div>
                  </div>
                  <div className="bg-gray-900 rounded p-3">
                    <div className="flex items-center space-x-2 mb-1">
                      <TrendingDown className="w-4 h-4 text-gray-400" />
                      <span className="text-xs text-gray-400">Max DD</span>
                    </div>
                    <div className="text-lg font-semibold text-red-400">{strategy.maxDrawdown.toFixed(2)}%</div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => toggleStrategy(strategy.id)}
                    className={`flex-1 flex items-center justify-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-colors ${
                      strategy.status === 'active'
                        ? 'bg-yellow-500/20 text-yellow-400 hover:bg-yellow-500/30'
                        : 'bg-green-500/20 text-green-400 hover:bg-green-500/30'
                    }`}
                  >
                    {strategy.status === 'active' ? (
                      <>
                        <Pause className="w-4 h-4" />
                        <span>Pause</span>
                      </>
                    ) : (
                      <>
                        <Play className="w-4 h-4" />
                        <span>Activate</span>
                      </>
                    )}
                  </button>
                  <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold text-white transition-colors">
                    <Settings className="w-4 h-4" />
                  </button>
                  <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold text-white transition-colors">
                    View Details
                  </button>
                </div>
              </motion.div>
            )
          })}
        </AnimatePresence>
      </div>

      {/* Summary Stats */}
      <div className="mt-6 pt-6 border-t border-gray-800">
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-white">
              {strategies.filter(s => s.status === 'active').length}
            </div>
            <div className="text-sm text-gray-400">Active Strategies</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">
              +{strategies.reduce((sum, s) => sum + s.performance, 0).toFixed(2)}%
            </div>
            <div className="text-sm text-gray-400">Combined Return</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-white">
              {strategies.reduce((sum, s) => sum + s.totalTrades, 0)}
            </div>
            <div className="text-sm text-gray-400">Total Trades</div>
          </div>
        </div>
      </div>
    </div>
  )
}
