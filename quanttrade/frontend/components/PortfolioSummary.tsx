/**
 * Enhanced Portfolio Summary Component
 * Real-time portfolio metrics with live updates
 */

'use client'

import React from 'react'
import { motion } from 'framer-motion'
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Activity,
  Target,
  Shield,
  AlertTriangle,
} from 'lucide-react'
import { usePortfolioWebSocket } from '@/hooks/useWebSocket'

interface PortfolioSummaryProps {
  accountId: string
}

export default function PortfolioSummary({ accountId }: PortfolioSummaryProps) {
  const { portfolio, isConnected } = usePortfolioWebSocket(accountId)

  const metrics = [
    {
      label: 'Portfolio Value',
      value: portfolio?.total_value || 0,
      format: 'currency',
      icon: DollarSign,
      color: 'text-blue-400',
    },
    {
      label: 'Total P&L',
      value: portfolio?.total_pnl || 0,
      format: 'currency',
      icon: portfolio?.total_pnl >= 0 ? TrendingUp : TrendingDown,
      color: portfolio?.total_pnl >= 0 ? 'text-green-400' : 'text-red-400',
    },
    {
      label: 'Today P&L',
      value: portfolio?.daily_pnl || 0,
      format: 'currency',
      icon: Activity,
      color: portfolio?.daily_pnl >= 0 ? 'text-green-400' : 'text-red-400',
    },
    {
      label: 'Win Rate',
      value: portfolio?.win_rate || 0,
      format: 'percent',
      icon: Target,
      color: 'text-purple-400',
    },
    {
      label: 'Sharpe Ratio',
      value: portfolio?.sharpe_ratio || 0,
      format: 'number',
      icon: Shield,
      color: 'text-cyan-400',
    },
    {
      label: 'Max Drawdown',
      value: portfolio?.max_drawdown || 0,
      format: 'percent',
      icon: AlertTriangle,
      color: 'text-orange-400',
    },
  ]

  const formatValue = (value: number, format: string) => {
    switch (format) {
      case 'currency':
        return `$${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
      case 'percent':
        return `${value.toFixed(2)}%`
      case 'number':
        return value.toFixed(2)
      default:
        return value.toString()
    }
  }

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-white">Portfolio Summary</h2>
        <div className="flex items-center space-x-2">
          <div
            className={`w-2 h-2 rounded-full ${
              isConnected ? 'bg-green-500' : 'bg-red-500'
            } animate-pulse`}
          />
          <span className="text-sm text-gray-400">
            {isConnected ? 'Live' : 'Disconnected'}
          </span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {metrics.map((metric, index) => {
          const Icon = metric.icon
          return (
            <motion.div
              key={metric.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-400">{metric.label}</span>
                <Icon className={`w-4 h-4 ${metric.color}`} />
              </div>
              <div className={`text-2xl font-bold ${metric.color}`}>
                {formatValue(metric.value, metric.format)}
              </div>
              {metric.format === 'currency' && metric.value !== 0 && (
                <div className="mt-1 text-xs text-gray-500">
                  {metric.value >= 0 ? '+' : ''}
                  {((metric.value / (portfolio?.total_value || 1)) * 100).toFixed(2)}%
                </div>
              )}
            </motion.div>
          )
        })}
      </div>

      {/* Additional Stats */}
      <div className="mt-6 pt-6 border-t border-gray-800">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-sm text-gray-400 mb-1">Active Positions</div>
            <div className="text-lg font-semibold text-white">
              {portfolio?.active_positions || 0}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-400 mb-1">Total Trades</div>
            <div className="text-lg font-semibold text-white">
              {portfolio?.total_trades || 0}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-400 mb-1">Profit Factor</div>
            <div className="text-lg font-semibold text-white">
              {portfolio?.profit_factor?.toFixed(2) || '0.00'}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}