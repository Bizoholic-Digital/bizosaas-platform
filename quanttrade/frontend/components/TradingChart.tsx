/**
 * Enhanced Trading Chart Component
 * Real-time candlestick chart with technical indicators
 */

'use client'

import React, { useEffect, useRef, useState } from 'react'
import { createChart, IChartApi, ISeriesApi, CandlestickData } from 'lightweight-charts'
import { useMarketDataWebSocket } from '@/hooks/useWebSocket'
import { TrendingUp, TrendingDown, Activity } from 'lucide-react'

interface TradingChartProps {
  symbol: string
  interval?: string
}

export default function TradingChart({ symbol, interval = '1h' }: TradingChartProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null)
  const chartRef = useRef<IChartApi | null>(null)
  const candlestickSeriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null)
  const volumeSeriesRef = useRef<ISeriesApi<'Histogram'> | null>(null)
  
  const { ticker, isConnected } = useMarketDataWebSocket(symbol)
  const [chartData, setChartData] = useState<CandlestickData[]>([])

  // Initialize chart
  useEffect(() => {
    if (!chartContainerRef.current) return

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 500,
      layout: {
        background: { color: '#1a1a1a' },
        textColor: '#d1d5db',
      },
      grid: {
        vertLines: { color: '#2a2a2a' },
        horzLines: { color: '#2a2a2a' },
      },
      crosshair: {
        mode: 1,
      },
      rightPriceScale: {
        borderColor: '#2a2a2a',
      },
      timeScale: {
        borderColor: '#2a2a2a',
        timeVisible: true,
        secondsVisible: false,
      },
    })

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#10b981',
      downColor: '#ef4444',
      borderUpColor: '#10b981',
      borderDownColor: '#ef4444',
      wickUpColor: '#10b981',
      wickDownColor: '#ef4444',
    })

    const volumeSeries = chart.addHistogramSeries({
      color: '#3b82f6',
      priceFormat: {
        type: 'volume',
      },
      priceScaleId: '',
    })

    volumeSeries.priceScale().applyOptions({
      scaleMargins: {
        top: 0.8,
        bottom: 0,
      },
    })

    chartRef.current = chart
    candlestickSeriesRef.current = candlestickSeries
    volumeSeriesRef.current = volumeSeries

    // Handle resize
    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        })
      }
    }

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      chart.remove()
    }
  }, [])

  // Update chart with real-time data
  useEffect(() => {
    if (ticker && candlestickSeriesRef.current) {
      const newCandle: CandlestickData = {
        time: Math.floor(Date.now() / 1000) as any,
        open: ticker.open || ticker.price,
        high: ticker.high || ticker.price,
        low: ticker.low || ticker.price,
        close: ticker.price,
      }

      candlestickSeriesRef.current.update(newCandle)
    }
  }, [ticker])

  const currentPrice = ticker?.price || 0
  const priceChange = ticker?.change || 0
  const priceChangePercent = ticker?.changePercent || 0

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-4">
          <h2 className="text-2xl font-bold text-white">{symbol}</h2>
          <div className="flex items-center space-x-2">
            <span className="text-3xl font-bold text-white">
              ${currentPrice.toLocaleString('en-US', { minimumFractionDigits: 2 })}
            </span>
            <div className={`flex items-center space-x-1 ${priceChange >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {priceChange >= 0 ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />}
              <span className="font-semibold">
                {priceChange >= 0 ? '+' : ''}{priceChange.toFixed(2)} ({priceChangePercent.toFixed(2)}%)
              </span>
            </div>
          </div>
        </div>

        {/* Connection Status */}
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`} />
          <span className="text-sm text-gray-400">{isConnected ? 'Live' : 'Disconnected'}</span>
        </div>
      </div>

      {/* Chart Stats */}
      <div className="grid grid-cols-4 gap-4 mb-4">
        <div className="bg-gray-800 rounded p-3">
          <div className="text-xs text-gray-400 mb-1">Open</div>
          <div className="text-sm font-semibold text-white">${ticker?.open?.toFixed(2) || '0.00'}</div>
        </div>
        <div className="bg-gray-800 rounded p-3">
          <div className="text-xs text-gray-400 mb-1">High</div>
          <div className="text-sm font-semibold text-green-400">${ticker?.high?.toFixed(2) || '0.00'}</div>
        </div>
        <div className="bg-gray-800 rounded p-3">
          <div className="text-xs text-gray-400 mb-1">Low</div>
          <div className="text-sm font-semibold text-red-400">${ticker?.low?.toFixed(2) || '0.00'}</div>
        </div>
        <div className="bg-gray-800 rounded p-3">
          <div className="text-xs text-gray-400 mb-1">Volume</div>
          <div className="text-sm font-semibold text-white">{ticker?.volume?.toLocaleString() || '0'}</div>
        </div>
      </div>

      {/* Chart Container */}
      <div ref={chartContainerRef} className="rounded-lg overflow-hidden bg-gray-950" />

      {/* Interval Selector */}
      <div className="flex items-center space-x-2 mt-4">
        <span className="text-sm text-gray-400">Interval:</span>
        {['1m', '5m', '15m', '1h', '4h', '1d'].map((int) => (
          <button
            key={int}
            className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
              interval === int
                ? 'bg-blue-500 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            {int}
          </button>
        ))}
      </div>
    </div>
  )
}