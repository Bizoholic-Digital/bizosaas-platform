'use client'

import React from 'react'
import { motion } from 'framer-motion'
import {
  DollarSign,
  TrendingUp,
  TrendingDown,
  Activity,
  PieChart,
  BarChart3
} from 'lucide-react'

interface Position {
  symbol: string
  quantity: number
  avgPrice: number
  currentPrice: number
  marketValue: number
  unrealizedPnL: number
  unrealizedPnLPercent: number
}

interface Portfolio {
  totalValue: number
  dailyChange: number
  dailyChangePercent: number
  dailyPnL: number
  dailyPnLPercent: number
  activePositions: number
  cashBalance: number
  buyingPower: number
  winRate: number
  positions?: Position[]
}

interface PortfolioSummaryProps {
  portfolio?: Portfolio | null
  loading: boolean
}

export default function PortfolioSummary({ portfolio, loading }: PortfolioSummaryProps) {
  if (loading) {
    return (
      <div className="trading-card">
        <h3 className="text-lg font-semibold text-white mb-4">Portfolio Summary</h3>
        <div className="space-y-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="loading-pulse h-16 rounded-lg" />
          ))}
        </div>
      </div>
    )
  }

  const portfolioData = portfolio || {
    totalValue: 125450.75,
    dailyChange: 2840.23,
    dailyChangePercent: 2.31,
    dailyPnL: 1250.80,
    dailyPnLPercent: 1.01,
    activePositions: 12,
    cashBalance: 15420.50,
    buyingPower: 45280.75,
    winRate: 68.5
  }

  const metrics = [
    {
      label: 'Total Value',
      value: `$${portfolioData.totalValue.toLocaleString()}`,
      change: portfolioData.dailyChange,
      changePercent: portfolioData.dailyChangePercent,
      icon: DollarSign,
      primary: true
    },
    {
      label: 'Today P&L',
      value: `$${portfolioData.dailyPnL >= 0 ? '+' : ''}${portfolioData.dailyPnL.toLocaleString()}`,
      change: portfolioData.dailyPnL,
      changePercent: portfolioData.dailyPnLPercent,
      icon: portfolioData.dailyPnL >= 0 ? TrendingUp : TrendingDown,
      primary: false
    },
    {
      label: 'Cash Balance',
      value: `$${portfolioData.cashBalance.toLocaleString()}`,
      change: 0,
      changePercent: 0,
      icon: Activity,
      primary: false
    },
    {
      label: 'Buying Power',
      value: `$${portfolioData.buyingPower.toLocaleString()}`,
      change: 0,
      changePercent: 0,
      icon: BarChart3,
      primary: false
    }
  ]

  const topPositions = portfolioData.positions?.slice(0, 5) || [
    { symbol: 'AAPL', quantity: 100, avgPrice: 175.50, currentPrice: 182.25, marketValue: 18225, unrealizedPnL: 675, unrealizedPnLPercent: 3.84 },
    { symbol: 'MSFT', quantity: 50, avgPrice: 325.80, currentPrice: 335.40, marketValue: 16770, unrealizedPnL: 480, unrealizedPnLPercent: 2.95 },
    { symbol: 'GOOGL', quantity: 25, avgPrice: 142.30, currentPrice: 138.75, marketValue: 3468.75, unrealizedPnL: -88.75, unrealizedPnLPercent: -2.49 },
    { symbol: 'TSLA', quantity: 30, avgPrice: 245.20, currentPrice: 252.10, marketValue: 7563, unrealizedPnL: 207, unrealizedPnLPercent: 2.81 },
    { symbol: 'NVDA', quantity: 15, avgPrice: 445.60, currentPrice: 458.90, marketValue: 6883.50, unrealizedPnL: 199.50, unrealizedPnLPercent: 2.98 }
  ]

  return (
    <div className="trading-card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
          <PieChart className="w-5 h-5 text-blue-400" />
          <span>Portfolio Summary</span>
        </h3>
        <div className="text-sm text-gray-400">
          {new Date().toLocaleDateString()}
        </div>
      </div>

      {/* Key Metrics */}
      <div className="space-y-3 mb-6">
        {metrics.map((metric, index) => (
          <motion.div
            key={metric.label}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className={`flex items-center justify-between p-3 rounded-lg ${
              metric.primary ? 'bg-gray-900 border border-gray-600' : 'bg-gray-900'
            }`}
          >
            <div className="flex items-center space-x-3">
              <div className="text-gray-400">
                <metric.icon className="w-4 h-4" />
              </div>
              <div>
                <p className="text-sm text-gray-400">{metric.label}</p>
                <p className={`font-semibold ${metric.primary ? 'text-xl text-white' : 'text-white'}`}>
                  {metric.value}
                </p>
              </div>
            </div>
            {metric.changePercent !== 0 && (
              <div className={`text-right ${
                metric.change >= 0 ? 'text-trading-green' : 'text-trading-red'
              }`}>
                <div className="flex items-center space-x-1 text-sm">
                  {metric.change >= 0 ? (
                    <TrendingUp className="w-3 h-3" />
                  ) : (
                    <TrendingDown className="w-3 h-3" />
                  )}
                  <span>{Math.abs(metric.changePercent).toFixed(2)}%</span>
                </div>
              </div>
            )}
          </motion.div>
        ))}
      </div>

      {/* Top Positions */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-md font-medium text-white">Top Positions</h4>
          <button className="text-blue-400 hover:text-blue-300 text-sm">
            View All
          </button>
        </div>

        <div className="space-y-2">
          {topPositions.map((position, index) => (
            <motion.div
              key={position.symbol}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="flex items-center justify-between p-2 rounded-lg bg-gray-900 hover:bg-gray-800 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
                  <span className="text-xs font-bold text-white">
                    {position.symbol.substring(0, 2)}
                  </span>
                </div>
                <div>
                  <p className="font-medium text-white text-sm">{position.symbol}</p>
                  <p className="text-xs text-gray-400">{position.quantity} shares</p>
                </div>
              </div>

              <div className="text-right">
                <p className="text-sm font-medium text-white">
                  ${position.marketValue.toLocaleString()}
                </p>
                <p className={`text-xs ${
                  position.unrealizedPnL >= 0 ? 'text-trading-green' : 'text-trading-red'
                }`}>
                  {position.unrealizedPnL >= 0 ? '+' : ''}${position.unrealizedPnL.toFixed(0)}
                  ({position.unrealizedPnLPercent >= 0 ? '+' : ''}{position.unrealizedPnLPercent.toFixed(2)}%)
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Portfolio Stats */}
      <div className="mt-4 pt-4 border-t border-gray-700">
        <div className="grid grid-cols-2 gap-4 text-center">
          <div>
            <p className="text-2xl font-bold text-white">{portfolioData.activePositions}</p>
            <p className="text-xs text-gray-400">Active Positions</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-purple-400">{portfolioData.winRate}%</p>
            <p className="text-xs text-gray-400">Win Rate</p>
          </div>
        </div>
      </div>
    </div>
  )
}