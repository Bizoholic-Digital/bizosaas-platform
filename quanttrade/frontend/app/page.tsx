'use client'

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
  TrendingUp,
  TrendingDown,
  BarChart3,
  PieChart,
  Activity,
  DollarSign,
  Clock,
  Settings,
  Bell,
  User,
  Play,
  Pause,
  RotateCcw,
  Brain,
  Target,
  Shield
} from 'lucide-react'
import TradingChart from '@/components/TradingChart'
import PortfolioSummary from '@/components/PortfolioSummary'
import PositionsList from '@/components/PositionsList'
import MarketWatchlist from '@/components/MarketWatchlist'
import { usePortfolio } from '@/hooks/usePortfolio'
import { useMarketData } from '@/hooks/useMarketData'

export default function TradingDashboard() {
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL')
  const [isAutoTrading, setIsAutoTrading] = useState(false)
  const { portfolio, loading: portfolioLoading } = usePortfolio()
  const { marketData, loading: marketLoading } = useMarketData()

  const quickStats = [
    {
      title: 'Portfolio Value',
      value: portfolio?.totalValue ? `$${portfolio.totalValue.toLocaleString()}` : '$0',
      change: portfolio?.dailyChange || 0,
      changePercent: portfolio?.dailyChangePercent || 0,
      icon: DollarSign,
      color: portfolio?.dailyChange >= 0 ? 'text-trading-green' : 'text-trading-red'
    },
    {
      title: 'Today P&L',
      value: portfolio?.dailyPnL ? `$${portfolio.dailyPnL.toLocaleString()}` : '$0',
      change: portfolio?.dailyPnL || 0,
      changePercent: portfolio?.dailyPnLPercent || 0,
      icon: TrendingUp,
      color: portfolio?.dailyPnL >= 0 ? 'text-trading-green' : 'text-trading-red'
    },
    {
      title: 'Active Positions',
      value: portfolio?.activePositions?.toString() || '0',
      change: 0,
      changePercent: 0,
      icon: BarChart3,
      color: 'text-blue-400'
    },
    {
      title: 'Win Rate',
      value: portfolio?.winRate ? `${portfolio.winRate}%` : '0%',
      change: 0,
      changePercent: 0,
      icon: Target,
      color: 'text-purple-400'
    }
  ]

  const aiStrategies = [
    {
      name: 'Momentum Scanner',
      status: 'active',
      performance: '+12.4%',
      trades: 23,
      winRate: '78%'
    },
    {
      name: 'Mean Reversion',
      status: 'active',
      performance: '+8.7%',
      trades: 15,
      winRate: '67%'
    },
    {
      name: 'News Sentiment',
      status: 'paused',
      performance: '+5.2%',
      trades: 8,
      winRate: '63%'
    }
  ]

  return (
    <div className="min-h-screen bg-trading-dark">
      {/* Header */}
      <header className="bg-gray-900 border-b border-gray-800 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-bold text-white">QuantTrade</h1>
            </div>

            <div className="flex items-center space-x-2 text-sm">
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-trading-green rounded-full animate-pulse" />
                <span className="text-gray-400">Market Open</span>
              </div>
              <span className="text-gray-600">|</span>
              <span className="text-gray-400">
                {new Date().toLocaleString()}
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setIsAutoTrading(!isAutoTrading)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                  isAutoTrading
                    ? 'bg-trading-green text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {isAutoTrading ? (
                  <>
                    <Pause className="w-4 h-4" />
                    <span>Pause AI</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" />
                    <span>Start AI</span>
                  </>
                )}
              </button>

              <button className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors">
                <Bell className="w-5 h-5 text-gray-300" />
              </button>

              <button className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors">
                <Settings className="w-5 h-5 text-gray-300" />
              </button>

              <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Quick Stats */}
      <div className="px-6 py-4 border-b border-gray-800">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickStats.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="trading-card"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-400">{stat.title}</p>
                  <p className="text-2xl font-bold text-white">{stat.value}</p>
                  {stat.changePercent !== 0 && (
                    <p className={`text-sm ${stat.color} flex items-center space-x-1`}>
                      {stat.change >= 0 ? (
                        <TrendingUp className="w-4 h-4" />
                      ) : (
                        <TrendingDown className="w-4 h-4" />
                      )}
                      <span>{Math.abs(stat.changePercent).toFixed(2)}%</span>
                    </p>
                  )}
                </div>
                <div className={`${stat.color}`}>
                  <stat.icon className="w-8 h-8" />
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Main Trading Interface */}
      <div className="flex-1 p-6">
        <div className="grid grid-cols-12 gap-6 h-full">
          {/* Left Sidebar - Watchlist & AI Strategies */}
          <div className="col-span-12 lg:col-span-3 space-y-6">
            <MarketWatchlist
              onSymbolSelect={setSelectedSymbol}
              selectedSymbol={selectedSymbol}
            />

            {/* AI Strategies */}
            <div className="trading-card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
                  <Brain className="w-5 h-5 text-purple-400" />
                  <span>AI Strategies</span>
                </h3>
                <button className="text-blue-400 hover:text-blue-300 text-sm">
                  Manage
                </button>
              </div>

              <div className="space-y-3">
                {aiStrategies.map((strategy, index) => (
                  <div key={strategy.name} className="p-3 bg-gray-900 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-white font-medium">{strategy.name}</span>
                      <div className={`px-2 py-1 rounded text-xs ${
                        strategy.status === 'active'
                          ? 'bg-green-900 text-green-400'
                          : 'bg-yellow-900 text-yellow-400'
                      }`}>
                        {strategy.status}
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-2 text-xs">
                      <div>
                        <span className="text-gray-400">Performance</span>
                        <div className="text-trading-green font-medium">{strategy.performance}</div>
                      </div>
                      <div>
                        <span className="text-gray-400">Trades</span>
                        <div className="text-white">{strategy.trades}</div>
                      </div>
                      <div>
                        <span className="text-gray-400">Win Rate</span>
                        <div className="text-white">{strategy.winRate}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Center - Chart */}
          <div className="col-span-12 lg:col-span-6">
            <div className="trading-card h-full">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">
                  {selectedSymbol} Chart
                </h3>
                <div className="flex items-center space-x-2">
                  <select className="bg-gray-700 text-white px-3 py-1 rounded text-sm">
                    <option>1D</option>
                    <option>5D</option>
                    <option>1M</option>
                    <option>3M</option>
                    <option>1Y</option>
                  </select>
                  <button className="p-1 rounded bg-gray-700 hover:bg-gray-600">
                    <RotateCcw className="w-4 h-4 text-gray-300" />
                  </button>
                </div>
              </div>

              <TradingChart symbol={selectedSymbol} />
            </div>
          </div>

          {/* Right Sidebar - Portfolio & News */}
          <div className="col-span-12 lg:col-span-3 space-y-6">
            <PortfolioSummary portfolio={portfolio} loading={portfolioLoading} />

            {/* Quick Trade */}
            <div className="trading-card">
              <h3 className="text-lg font-semibold text-white mb-4">Quick Trade</h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Symbol</label>
                  <input
                    type="text"
                    value={selectedSymbol}
                    onChange={(e) => setSelectedSymbol(e.target.value)}
                    className="w-full bg-gray-700 text-white px-3 py-2 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                  />
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-sm text-gray-400 mb-1">Quantity</label>
                    <input
                      type="number"
                      placeholder="100"
                      className="w-full bg-gray-700 text-white px-3 py-2 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-400 mb-1">Price</label>
                    <input
                      type="number"
                      placeholder="Market"
                      className="w-full bg-gray-700 text-white px-3 py-2 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <button className="btn-success">
                    BUY
                  </button>
                  <button className="btn-danger">
                    SELL
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Panel - Positions */}
      <div className="border-t border-gray-800">
        <PositionsList />
      </div>
    </div>
  )
}