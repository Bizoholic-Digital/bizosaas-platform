'use client'

import { useState, useEffect } from 'react'

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
  totalReturn: number
  totalReturnPercent: number
  positions: Position[]
  accountValue: number
  initialCapital: number
}

// Mock portfolio data
const mockPortfolio: Portfolio = {
  totalValue: 125450.75,
  dailyChange: 2840.23,
  dailyChangePercent: 2.31,
  dailyPnL: 1250.80,
  dailyPnLPercent: 1.01,
  activePositions: 12,
  cashBalance: 15420.50,
  buyingPower: 45280.75,
  winRate: 68.5,
  totalReturn: 25450.75,
  totalReturnPercent: 25.45,
  accountValue: 125450.75,
  initialCapital: 100000,
  positions: [
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
}

export interface UsePortfolioReturn {
  portfolio: Portfolio | null
  loading: boolean
  error: string | null
  refreshPortfolio: () => Promise<void>
  updatePosition: (positionId: string, updates: Partial<Position>) => Promise<void>
  closePosition: (positionId: string) => Promise<void>
}

export function usePortfolio(): UsePortfolioReturn {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const fetchPortfolio = async (): Promise<void> => {
    try {
      setLoading(true)
      setError(null)

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Try to fetch from QuantTrade backend API
      try {
        const response = await fetch('/api/portfolio', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
          },
        })

        if (response.ok) {
          const data = await response.json()
          setPortfolio(data)
        } else {
          throw new Error('Failed to fetch portfolio')
        }
      } catch (apiError) {
        // Fallback to mock data if API is not available
        console.warn('Portfolio API not available, using mock data:', apiError)

        // Add some realistic price fluctuations
        const fluctuatedPortfolio = {
          ...mockPortfolio,
          positions: mockPortfolio.positions.map(pos => ({
            ...pos,
            currentPrice: pos.currentPrice + (Math.random() - 0.5) * pos.currentPrice * 0.02,
            dayChange: pos.dayChange + (Math.random() - 0.5) * 2,
            dayChangePercent: pos.dayChangePercent + (Math.random() - 0.5) * 0.5
          }))
        }

        // Recalculate portfolio totals
        const totalUnrealizedPnL = fluctuatedPortfolio.positions.reduce(
          (sum, pos) => sum + (pos.currentPrice - pos.avgPrice) * pos.quantity * (pos.side === 'short' ? -1 : 1),
          0
        )
        const totalMarketValue = fluctuatedPortfolio.positions.reduce(
          (sum, pos) => sum + pos.currentPrice * pos.quantity,
          0
        )

        fluctuatedPortfolio.totalValue = totalMarketValue + fluctuatedPortfolio.cashBalance
        fluctuatedPortfolio.dailyPnL = totalUnrealizedPnL * 0.1 // Approximate daily P&L
        fluctuatedPortfolio.dailyPnLPercent = (fluctuatedPortfolio.dailyPnL / fluctuatedPortfolio.totalValue) * 100

        setPortfolio(fluctuatedPortfolio)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch portfolio')
      console.error('Portfolio fetch error:', err)
    } finally {
      setLoading(false)
    }
  }

  const updatePosition = async (positionId: string, updates: Partial<Position>): Promise<void> => {
    try {
      const response = await fetch(`/api/positions/${positionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
        },
        body: JSON.stringify(updates),
      })

      if (response.ok) {
        // Update local state
        setPortfolio(prev => {
          if (!prev) return prev
          return {
            ...prev,
            positions: prev.positions.map(pos =>
              pos.id === positionId ? { ...pos, ...updates } : pos
            )
          }
        })
      } else {
        throw new Error('Failed to update position')
      }
    } catch (err) {
      console.error('Position update error:', err)
      // For demo purposes, update locally anyway
      setPortfolio(prev => {
        if (!prev) return prev
        return {
          ...prev,
          positions: prev.positions.map(pos =>
            pos.id === positionId ? { ...pos, ...updates } : pos
          )
        }
      })
    }
  }

  const closePosition = async (positionId: string): Promise<void> => {
    try {
      const response = await fetch(`/api/positions/${positionId}/close`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
        },
      })

      if (response.ok) {
        // Remove position from local state
        setPortfolio(prev => {
          if (!prev) return prev
          return {
            ...prev,
            positions: prev.positions.filter(pos => pos.id !== positionId),
            activePositions: prev.activePositions - 1
          }
        })
      } else {
        throw new Error('Failed to close position')
      }
    } catch (err) {
      console.error('Position close error:', err)
      // For demo purposes, remove locally anyway
      setPortfolio(prev => {
        if (!prev) return prev
        return {
          ...prev,
          positions: prev.positions.filter(pos => pos.id !== positionId),
          activePositions: prev.activePositions - 1
        }
      })
    }
  }

  const refreshPortfolio = async (): Promise<void> => {
    await fetchPortfolio()
  }

  // Initial load
  useEffect(() => {
    fetchPortfolio()
  }, [])

  // Real-time updates simulation
  useEffect(() => {
    const interval = setInterval(() => {
      if (portfolio) {
        setPortfolio(prev => {
          if (!prev) return prev

          const updatedPositions = prev.positions.map(pos => {
            const priceChange = (Math.random() - 0.5) * pos.currentPrice * 0.005 // 0.5% max change
            const newPrice = Math.max(pos.currentPrice + priceChange, 0.01)
            const newUnrealizedPnL = (newPrice - pos.avgPrice) * pos.quantity * (pos.side === 'short' ? -1 : 1)
            const newUnrealizedPnLPercent = (newUnrealizedPnL / (pos.avgPrice * pos.quantity)) * 100

            return {
              ...pos,
              currentPrice: newPrice,
              marketValue: newPrice * pos.quantity,
              unrealizedPnL: newUnrealizedPnL,
              unrealizedPnLPercent: newUnrealizedPnLPercent,
              dayChange: pos.dayChange + priceChange * 0.5,
              dayChangePercent: pos.dayChangePercent + (priceChange / pos.currentPrice) * 100 * 0.5
            }
          })

          const totalMarketValue = updatedPositions.reduce((sum, pos) => sum + pos.marketValue, 0)
          const totalUnrealizedPnL = updatedPositions.reduce((sum, pos) => sum + pos.unrealizedPnL, 0)
          const newTotalValue = totalMarketValue + prev.cashBalance

          return {
            ...prev,
            positions: updatedPositions,
            totalValue: newTotalValue,
            dailyPnL: totalUnrealizedPnL * 0.1,
            dailyPnLPercent: (totalUnrealizedPnL * 0.1 / newTotalValue) * 100,
            dailyChange: newTotalValue - prev.initialCapital,
            dailyChangePercent: ((newTotalValue - prev.initialCapital) / prev.initialCapital) * 100
          }
        })
      }
    }, 3000) // Update every 3 seconds

    return () => clearInterval(interval)
  }, [portfolio])

  return {
    portfolio,
    loading,
    error,
    refreshPortfolio,
    updatePosition,
    closePosition
  }
}