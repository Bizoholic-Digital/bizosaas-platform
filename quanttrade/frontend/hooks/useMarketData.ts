'use client'

import { useState, useEffect } from 'react'

interface MarketQuote {
  symbol: string
  price: number
  change: number
  changePercent: number
  volume: number
  high: number
  low: number
  open: number
  previousClose: number
  marketCap?: string
  peRatio?: number
  divYield?: number
  high52Week: number
  low52Week: number
  avgVolume: number
  timestamp: number
}

interface MarketIndices {
  SPY: MarketQuote
  QQQ: MarketQuote
  IWM: MarketQuote
  DIA: MarketQuote
}

interface SectorPerformance {
  sector: string
  change: number
  changePercent: number
  topGainer: string
  topLoser: string
}

interface MarketData {
  indices: MarketIndices
  sectors: SectorPerformance[]
  quotes: Record<string, MarketQuote>
  lastUpdate: number
  marketStatus: 'open' | 'closed' | 'pre-market' | 'after-hours'
}

// Mock market data
const mockIndices: MarketIndices = {
  SPY: {
    symbol: 'SPY',
    price: 445.75,
    change: 2.35,
    changePercent: 0.53,
    volume: 45652340,
    high: 447.20,
    low: 443.80,
    open: 444.10,
    previousClose: 443.40,
    marketCap: '408.2B',
    high52Week: 479.98,
    low52Week: 348.11,
    avgVolume: 52340000,
    timestamp: Date.now()
  },
  QQQ: {
    symbol: 'QQQ',
    price: 378.90,
    change: 4.25,
    changePercent: 1.13,
    volume: 32145680,
    high: 380.15,
    low: 376.45,
    open: 377.20,
    previousClose: 374.65,
    marketCap: '189.5B',
    high52Week: 408.71,
    low52Week: 287.96,
    avgVolume: 35420000,
    timestamp: Date.now()
  },
  IWM: {
    symbol: 'IWM',
    price: 198.45,
    change: -1.15,
    changePercent: -0.58,
    volume: 28945630,
    high: 200.20,
    low: 198.10,
    open: 199.80,
    previousClose: 199.60,
    marketCap: '31.2B',
    high52Week: 224.94,
    low52Week: 166.25,
    avgVolume: 31240000,
    timestamp: Date.now()
  },
  DIA: {
    symbol: 'DIA',
    price: 345.80,
    change: 1.95,
    changePercent: 0.57,
    volume: 3845620,
    high: 346.50,
    low: 344.20,
    open: 344.85,
    previousClose: 343.85,
    marketCap: '24.8B',
    high52Week: 378.54,
    low52Week: 298.94,
    avgVolume: 4120000,
    timestamp: Date.now()
  }
}

const mockSectors: SectorPerformance[] = [
  {
    sector: 'Technology',
    change: 8.45,
    changePercent: 1.23,
    topGainer: 'NVDA',
    topLoser: 'GOOGL'
  },
  {
    sector: 'Healthcare',
    change: 2.15,
    changePercent: 0.45,
    topGainer: 'JNJ',
    topLoser: 'PFE'
  },
  {
    sector: 'Financial',
    change: -1.25,
    changePercent: -0.32,
    topGainer: 'GS',
    topLoser: 'WFC'
  },
  {
    sector: 'Consumer Discretionary',
    change: 3.80,
    changePercent: 0.89,
    topGainer: 'TSLA',
    topLoser: 'AMZN'
  },
  {
    sector: 'Energy',
    change: -2.45,
    changePercent: -1.15,
    topGainer: 'CVX',
    topLoser: 'XOM'
  },
  {
    sector: 'Industrials',
    change: 1.65,
    changePercent: 0.42,
    topGainer: 'BA',
    topLoser: 'CAT'
  }
]

export interface UseMarketDataReturn {
  marketData: MarketData | null
  loading: boolean
  error: string | null
  getQuote: (symbol: string) => MarketQuote | null
  refreshMarketData: () => Promise<void>
  subscribeToSymbol: (symbol: string) => void
  unsubscribeFromSymbol: (symbol: string) => void
}

export function useMarketData(): UseMarketDataReturn {
  const [marketData, setMarketData] = useState<MarketData | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const [subscribedSymbols, setSubscribedSymbols] = useState<Set<string>>(new Set())

  const determineMarketStatus = (): 'open' | 'closed' | 'pre-market' | 'after-hours' => {
    const now = new Date()
    const hour = now.getHours()
    const day = now.getDay()

    // Weekend
    if (day === 0 || day === 6) return 'closed'

    // Market hours: 9:30 AM - 4:00 PM EST
    if (hour >= 9.5 && hour < 16) return 'open'
    if (hour >= 4 && hour < 20) return 'after-hours'
    if (hour >= 4 && hour < 9.5) return 'pre-market'

    return 'closed'
  }

  const generateMockQuote = (symbol: string): MarketQuote => {
    const basePrice = 100 + Math.random() * 400
    const change = (Math.random() - 0.5) * basePrice * 0.05
    const changePercent = (change / basePrice) * 100

    return {
      symbol,
      price: basePrice,
      change,
      changePercent,
      volume: Math.floor(Math.random() * 50000000),
      high: basePrice + Math.abs(change) * 0.5,
      low: basePrice - Math.abs(change) * 0.5,
      open: basePrice - change * 0.3,
      previousClose: basePrice - change,
      marketCap: `${Math.floor(Math.random() * 1000)}B`,
      peRatio: 15 + Math.random() * 25,
      divYield: Math.random() * 4,
      high52Week: basePrice * 1.5,
      low52Week: basePrice * 0.5,
      avgVolume: Math.floor(Math.random() * 30000000),
      timestamp: Date.now()
    }
  }

  const fetchMarketData = async (): Promise<void> => {
    try {
      setLoading(true)
      setError(null)

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 500))

      // Try to fetch from market data API
      try {
        const response = await fetch('/api/market/data', {
          headers: {
            'Content-Type': 'application/json',
          },
        })

        if (response.ok) {
          const data = await response.json()
          setMarketData(data)
        } else {
          throw new Error('Failed to fetch market data')
        }
      } catch (apiError) {
        // Fallback to mock data if API is not available
        console.warn('Market data API not available, using mock data:', apiError)

        // Generate quotes for subscribed symbols
        const quotes: Record<string, MarketQuote> = {}
        subscribedSymbols.forEach(symbol => {
          quotes[symbol] = generateMockQuote(symbol)
        })

        // Add some default symbols
        const defaultSymbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'AMZN', 'META']
        defaultSymbols.forEach(symbol => {
          if (!quotes[symbol]) {
            quotes[symbol] = generateMockQuote(symbol)
          }
        })

        const mockData: MarketData = {
          indices: mockIndices,
          sectors: mockSectors,
          quotes,
          lastUpdate: Date.now(),
          marketStatus: determineMarketStatus()
        }

        setMarketData(mockData)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch market data')
      console.error('Market data fetch error:', err)
    } finally {
      setLoading(false)
    }
  }

  const getQuote = (symbol: string): MarketQuote | null => {
    return marketData?.quotes[symbol] || null
  }

  const refreshMarketData = async (): Promise<void> => {
    await fetchMarketData()
  }

  const subscribeToSymbol = (symbol: string): void => {
    setSubscribedSymbols(prev => new Set([...prev, symbol]))
  }

  const unsubscribeFromSymbol = (symbol: string): void => {
    setSubscribedSymbols(prev => {
      const newSet = new Set(prev)
      newSet.delete(symbol)
      return newSet
    })
  }

  // Initial load
  useEffect(() => {
    fetchMarketData()
  }, [])

  // Real-time updates simulation
  useEffect(() => {
    const interval = setInterval(() => {
      if (marketData && marketData.marketStatus === 'open') {
        setMarketData(prev => {
          if (!prev) return prev

          // Update indices
          const updatedIndices = { ...prev.indices }
          Object.keys(updatedIndices).forEach(key => {
            const index = updatedIndices[key as keyof MarketIndices]
            const priceChange = (Math.random() - 0.5) * index.price * 0.002 // 0.2% max change
            const newPrice = Math.max(index.price + priceChange, 0.01)
            const newChange = index.change + priceChange
            const newChangePercent = (newChange / index.previousClose) * 100

            updatedIndices[key as keyof MarketIndices] = {
              ...index,
              price: newPrice,
              change: newChange,
              changePercent: newChangePercent,
              high: Math.max(index.high, newPrice),
              low: Math.min(index.low, newPrice),
              volume: index.volume + Math.floor(Math.random() * 100000),
              timestamp: Date.now()
            }
          })

          // Update quotes
          const updatedQuotes = { ...prev.quotes }
          Object.keys(updatedQuotes).forEach(symbol => {
            const quote = updatedQuotes[symbol]
            const priceChange = (Math.random() - 0.5) * quote.price * 0.005 // 0.5% max change
            const newPrice = Math.max(quote.price + priceChange, 0.01)
            const newChange = quote.change + priceChange
            const newChangePercent = (newChange / quote.previousClose) * 100

            updatedQuotes[symbol] = {
              ...quote,
              price: newPrice,
              change: newChange,
              changePercent: newChangePercent,
              high: Math.max(quote.high, newPrice),
              low: Math.min(quote.low, newPrice),
              volume: quote.volume + Math.floor(Math.random() * 50000),
              timestamp: Date.now()
            }
          })

          return {
            ...prev,
            indices: updatedIndices,
            quotes: updatedQuotes,
            lastUpdate: Date.now(),
            marketStatus: determineMarketStatus()
          }
        })
      }
    }, 2000) // Update every 2 seconds during market hours

    return () => clearInterval(interval)
  }, [marketData])

  // Re-fetch when subscribed symbols change
  useEffect(() => {
    if (subscribedSymbols.size > 0) {
      fetchMarketData()
    }
  }, [subscribedSymbols.size])

  return {
    marketData,
    loading,
    error,
    getQuote,
    refreshMarketData,
    subscribeToSymbol,
    unsubscribeFromSymbol
  }
}