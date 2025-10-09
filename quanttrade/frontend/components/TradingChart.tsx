'use client'

import React, { useEffect, useRef, useState } from 'react'
import { useWebSocket } from '../hooks/useWebSocket'
import { useMarketData } from '../hooks/useMarketData'

interface TradingChartProps {
  symbol: string
  interval?: string
  enableRealTime?: boolean
  height?: string
}

declare global {
  interface Window {
    TradingView: any
  }
}

export default function TradingChart({
  symbol,
  interval = '1D',
  enableRealTime = true,
  height = '600px'
}: TradingChartProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const widgetRef = useRef<any>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [currentPrice, setCurrentPrice] = useState<number | null>(null)
  const [priceChange, setPriceChange] = useState<number>(0)

  // Real-time WebSocket connection
  const {
    isConnected: wsConnected,
    lastMessage,
    sendMessage
  } = useWebSocket(`ws://localhost:8012/ws/market/${symbol}`, enableRealTime)

  // Market data hook for additional data
  const { quote, isLoading } = useMarketData(symbol)

  // Handle real-time WebSocket messages
  useEffect(() => {
    if (!lastMessage || !enableRealTime) return

    try {
      const message = JSON.parse(lastMessage)

      if (message.type === 'quote' && message.data) {
        setCurrentPrice(message.data.price)
        setPriceChange(message.data.change)
        setIsConnected(true)

        // Update TradingView widget with real-time data if needed
        if (widgetRef.current && widgetRef.current.chart) {
          // Real-time price updates can be implemented here
          // TradingView widgets typically handle this automatically
        }
      }

      if (message.type === 'tick' && message.data) {
        // Handle individual tick updates
        console.log('Real-time tick:', message.data)
      }

      if (message.type === 'heartbeat') {
        setIsConnected(true)
      }

    } catch (error) {
      console.error('Error parsing WebSocket message:', error)
    }
  }, [lastMessage, enableRealTime])

  // Initialize TradingView widget
  useEffect(() => {
    if (!containerRef.current) return

    const loadTradingView = () => {
      if (typeof window !== 'undefined' && window.TradingView) {
        // Clean up existing widget
        if (widgetRef.current) {
          widgetRef.current.remove()
        }

        // Create new widget with enhanced configuration
        widgetRef.current = new window.TradingView.widget({
          autosize: true,
          symbol: symbol,
          interval: interval,
          timezone: 'Etc/UTC',
          theme: 'dark',
          style: '1',
          locale: 'en',
          toolbar_bg: '#1E222D',
          enable_publishing: false,
          hide_top_toolbar: false,
          hide_legend: false,
          save_image: true,
          container_id: containerRef.current?.id || 'tradingview_chart',
          studies: [
            'Volume@tv-basicstudies',
            'RSI@tv-basicstudies',
            'MACD@tv-basicstudies',
            'Moving Average@tv-basicstudies',
            'Bollinger Bands@tv-basicstudies'
          ],
          overrides: {
            // Dark theme customization
            'paneProperties.background': '#131722',
            'paneProperties.backgroundType': 'solid',
            'paneProperties.vertGridProperties.color': '#2A2E39',
            'paneProperties.vertGridProperties.style': 0,
            'paneProperties.horzGridProperties.color': '#2A2E39',
            'paneProperties.horzGridProperties.style': 0,
            'paneProperties.crossHairProperties.color': '#9598A1',
            'paneProperties.topMargin': 10,
            'paneProperties.bottomMargin': 10,

            // Symbol and watermark
            'symbolWatermarkProperties.transparency': 90,
            'symbolWatermarkProperties.color': '#2A2E39',

            // Scales
            'scalesProperties.textColor': '#AAA',
            'scalesProperties.fontSize': 12,
            'scalesProperties.backgroundColor': '#131722',

            // Main series (candlesticks)
            'mainSeriesProperties.candleStyle.upColor': '#00D084',
            'mainSeriesProperties.candleStyle.downColor': '#F7525F',
            'mainSeriesProperties.candleStyle.drawWick': true,
            'mainSeriesProperties.candleStyle.drawBorder': true,
            'mainSeriesProperties.candleStyle.borderColor': '#378658',
            'mainSeriesProperties.candleStyle.borderUpColor': '#00D084',
            'mainSeriesProperties.candleStyle.borderDownColor': '#F7525F',
            'mainSeriesProperties.candleStyle.wickUpColor': '#00D084',
            'mainSeriesProperties.candleStyle.wickDownColor': '#F7525F',

            // Volume
            'volumePaneSize': 'medium',
            'volume.volume.color.0': '#F7525F',
            'volume.volume.color.1': '#00D084',
            'volume.volume.transparency': 50,

            // Moving averages
            'studies.MA.ma.color': '#2196F3',
            'studies.MA.ma.linewidth': 2,
            'studies.MA.ma.transparency': 0,

            // RSI
            'studies.RSI.plot.color': '#9C27B0',
            'studies.RSI.plot.linewidth': 2,
            'studies.RSI.upper band.color': '#787B86',
            'studies.RSI.lower band.color': '#787B86',

            // MACD
            'studies.MACD.macd.color': '#2196F3',
            'studies.MACD.signal.color': '#FF9800',
            'studies.MACD.histogram.color': '#26A69A',

            // Bollinger Bands
            'studies.BB.upper.color': '#9C27B0',
            'studies.BB.lower.color': '#9C27B0',
            'studies.BB.median.color': '#FF6D00'
          },
          loading_screen: { backgroundColor: '#131722', foregroundColor: '#2A2E39' },
          custom_css_url: '/tradingview-custom.css',

          // Enhanced features
          allow_symbol_change: true,
          details: true,
          hotlist: true,
          calendar: true,
          show_popup_button: true,
          popup_width: '1000',
          popup_height: '650',

          // Real-time data configuration
          datafeed: enableRealTime ? {
            onReady: (callback: any) => {
              console.log('TradingView datafeed ready')
              callback({
                supports_search: true,
                supports_group_request: false,
                supported_resolutions: ['1', '5', '15', '30', '60', '240', '1D'],
                supports_marks: false,
                supports_timescale_marks: false
              })
            },
            searchSymbols: (userInput: string, exchange: string, symbolType: string, onResultReadyCallback: any) => {
              console.log('Symbol search:', userInput)
              onResultReadyCallback([])
            },
            resolveSymbol: (symbolName: string, onSymbolResolvedCallback: any, onResolveErrorCallback: any) => {
              console.log('Resolving symbol:', symbolName)
              onSymbolResolvedCallback({
                name: symbolName,
                ticker: symbolName,
                description: symbolName,
                type: 'stock',
                session: '0930-1600',
                timezone: 'America/New_York',
                exchange: 'NASDAQ',
                minmov: 1,
                pricescale: 100,
                has_intraday: true,
                intraday_multipliers: ['1', '5', '15', '30', '60'],
                supported_resolutions: ['1', '5', '15', '30', '60', '240', '1D'],
                volume_precision: 0,
                data_status: 'streaming'
              })
            },
            getBars: (symbolInfo: any, resolution: string, from: number, to: number, onHistoryCallback: any, onErrorCallback: any, firstDataRequest: boolean) => {
              console.log('Getting bars for:', symbolInfo.name, resolution, from, to)
              // This would integrate with our backend API
              fetch(`/api/market/history?symbol=${symbolInfo.name}&resolution=${resolution}&from=${from}&to=${to}`)
                .then(response => response.json())
                .then(data => {
                  onHistoryCallback(data.bars || [], { noData: !data.bars?.length })
                })
                .catch(error => {
                  console.error('Error fetching bars:', error)
                  onErrorCallback(error)
                })
            },
            subscribeBars: (symbolInfo: any, resolution: string, onRealtimeCallback: any, subscriberUID: string, onResetCacheNeededCallback: any) => {
              console.log('Subscribing to bars:', symbolInfo.name, resolution)
              // This would subscribe to our WebSocket feed
              // The real-time updates would call onRealtimeCallback
            },
            unsubscribeBars: (subscriberUID: string) => {
              console.log('Unsubscribing from bars:', subscriberUID)
            }
          } : undefined
        })
      }
    }

    // Check if TradingView is already loaded
    if (window.TradingView) {
      loadTradingView()
    } else {
      // Wait for TradingView to load
      const checkTradingView = setInterval(() => {
        if (window.TradingView) {
          clearInterval(checkTradingView)
          loadTradingView()
        }
      }, 100)

      // Cleanup interval after 10 seconds
      setTimeout(() => clearInterval(checkTradingView), 10000)
    }

    return () => {
      if (widgetRef.current) {
        try {
          widgetRef.current.remove()
        } catch (error) {
          console.log('TradingView widget cleanup error:', error)
        }
      }
    }
  }, [symbol, interval])

  // Helper function to request real-time data
  const requestQuote = () => {
    if (enableRealTime && sendMessage) {
      sendMessage(JSON.stringify({ type: 'get_quote' }))
    }
  }

  const requestOrderBook = () => {
    if (enableRealTime && sendMessage) {
      sendMessage(JSON.stringify({ type: 'get_order_book' }))
    }
  }

  const requestIntradayData = (intervalParam?: string) => {
    if (enableRealTime && sendMessage) {
      sendMessage(JSON.stringify({
        type: 'get_intraday',
        interval: intervalParam || interval,
        period: '1d'
      }))
    }
  }

  return (
    <div className="h-full w-full relative" style={{ height }}>
      {/* Real-time connection status bar */}
      {enableRealTime && (
        <div className="absolute top-2 right-2 z-10 flex items-center space-x-2">
          <div className={`flex items-center px-3 py-1 rounded-full text-xs font-medium ${
            wsConnected && isConnected
              ? 'bg-green-900/70 text-green-300 border border-green-500/30'
              : 'bg-red-900/70 text-red-300 border border-red-500/30'
          }`}>
            <div className={`w-2 h-2 rounded-full mr-2 ${
              wsConnected && isConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'
            }`} />
            {wsConnected && isConnected ? 'Live' : 'Disconnected'}
          </div>

          {/* Current price display */}
          {currentPrice && (
            <div className="bg-gray-900/70 border border-gray-500/30 px-3 py-1 rounded-full">
              <div className="flex items-center space-x-2">
                <span className="text-white font-bold">
                  ${currentPrice.toFixed(2)}
                </span>
                {priceChange !== 0 && (
                  <span className={`text-xs font-medium ${
                    priceChange > 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {priceChange > 0 ? '+' : ''}{priceChange.toFixed(2)}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Real-time control panel */}
      {enableRealTime && (
        <div className="absolute top-2 left-2 z-10">
          <div className="flex items-center space-x-2">
            <button
              onClick={requestQuote}
              className="bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded text-xs font-medium transition-colors"
              title="Get latest quote"
            >
              Quote
            </button>
            <button
              onClick={requestOrderBook}
              className="bg-purple-600 hover:bg-purple-700 text-white px-2 py-1 rounded text-xs font-medium transition-colors"
              title="Get order book"
            >
              Book
            </button>
            <button
              onClick={() => requestIntradayData()}
              className="bg-orange-600 hover:bg-orange-700 text-white px-2 py-1 rounded text-xs font-medium transition-colors"
              title="Refresh intraday data"
            >
              Refresh
            </button>
          </div>
        </div>
      )}

      {/* TradingView chart container */}
      <div
        ref={containerRef}
        id="tradingview_chart"
        className="h-full w-full"
      />

      {/* Loading state */}
      {isLoading && (
        <div className="absolute inset-0 bg-gray-900/50 flex items-center justify-center">
          <div className="text-center">
            <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
            <p className="text-gray-300 text-sm">Loading market data...</p>
          </div>
        </div>
      )}

      {/* Fallback chart simulation */}
      {!window?.TradingView && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-900 rounded-lg">
          <div className="text-center">
            <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-400">Loading TradingView Chart...</p>
            <p className="text-sm text-gray-500 mt-2">Symbol: {symbol}</p>
            <p className="text-xs text-gray-600 mt-1">
              Real-time: {enableRealTime ? 'Enabled' : 'Disabled'}
            </p>

            {/* Mock chart preview */}
            <div className="mt-6 p-4 bg-gray-800 rounded-lg max-w-sm">
              <div className="flex justify-between items-center mb-3">
                <span className="text-white font-bold">{symbol}</span>
                {quote && (
                  <span className="text-green-400">${quote.price?.toFixed(2)}</span>
                )}
              </div>
              <div className="h-32 bg-gradient-to-r from-green-900/20 to-blue-900/20 rounded flex items-end">
                {[...Array(20)].map((_, i) => (
                  <div
                    key={i}
                    className="flex-1 bg-blue-500/30 mx-px rounded-t"
                    style={{
                      height: `${Math.random() * 80 + 20}%`,
                    }}
                  />
                ))}
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Chart will load when TradingView library is ready
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Additional info panel (can be toggled) */}
      {quote && enableRealTime && (
        <div className="absolute bottom-2 left-2 z-10">
          <div className="bg-gray-900/70 border border-gray-500/30 rounded-lg p-2 text-xs">
            <div className="grid grid-cols-2 gap-2 min-w-[200px]">
              <div>
                <span className="text-gray-400">Open:</span>
                <span className="text-white ml-1">${quote.open?.toFixed(2)}</span>
              </div>
              <div>
                <span className="text-gray-400">High:</span>
                <span className="text-white ml-1">${quote.high?.toFixed(2)}</span>
              </div>
              <div>
                <span className="text-gray-400">Low:</span>
                <span className="text-white ml-1">${quote.low?.toFixed(2)}</span>
              </div>
              <div>
                <span className="text-gray-400">Vol:</span>
                <span className="text-white ml-1">{quote.volume?.toLocaleString()}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}