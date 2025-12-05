/**
 * WebSocket Hook for Real-time Market Data
 * Connects to QuantTrade backend WebSocket for live updates
 */

import { useEffect, useRef, useState, useCallback } from 'react'

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8012/ws'

export interface WebSocketMessage {
  type: string
  data: any
  timestamp: number
}

export interface UseWebSocketOptions {
  onMessage?: (message: WebSocketMessage) => void
  onConnect?: () => void
  onDisconnect?: () => void
  onError?: (error: Event) => void
  reconnect?: boolean
  reconnectInterval?: number
}

export function useWebSocket(channel: string, options: UseWebSocketOptions = {}) {
  const {
    onMessage,
    onConnect,
    onDisconnect,
    onError,
    reconnect = true,
    reconnectInterval = 3000,
  } = options

  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(`${WS_URL}/${channel}`)

      ws.onopen = () => {
        console.log(`WebSocket connected to ${channel}`)
        setIsConnected(true)
        onConnect?.()
      }

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          setLastMessage(message)
          onMessage?.(message)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        onError?.(error)
      }

      ws.onclose = () => {
        console.log(`WebSocket disconnected from ${channel}`)
        setIsConnected(false)
        onDisconnect?.()

        // Attempt reconnection
        if (reconnect) {
          reconnectTimeoutRef.current = setTimeout(() => {
            console.log(`Attempting to reconnect to ${channel}...`)
            connect()
          }, reconnectInterval)
        }
      }

      wsRef.current = ws
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
    }
  }, [channel, onConnect, onMessage, onDisconnect, onError, reconnect, reconnectInterval])

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
    }
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
  }, [])

  const sendMessage = useCallback((data: any) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    } else {
      console.warn('WebSocket is not connected')
    }
  }, [])

  useEffect(() => {
    connect()
    return () => {
      disconnect()
    }
  }, [connect, disconnect])

  return {
    isConnected,
    lastMessage,
    sendMessage,
    disconnect,
    reconnect: connect,
  }
}

/**
 * Hook for market data WebSocket
 */
export function useMarketDataWebSocket(symbol: string) {
  const [ticker, setTicker] = useState<any>(null)
  const [orderBook, setOrderBook] = useState<any>(null)
  const [trades, setTrades] = useState<any[]>([])

  const { isConnected, sendMessage } = useWebSocket('market-data', {
    onMessage: (message) => {
      switch (message.type) {
        case 'ticker':
          setTicker(message.data)
          break
        case 'orderbook':
          setOrderBook(message.data)
          break
        case 'trade':
          setTrades((prev) => [message.data, ...prev].slice(0, 50))
          break
      }
    },
    onConnect: () => {
      // Subscribe to symbol on connect
      sendMessage({ action: 'subscribe', symbol })
    },
  })

  useEffect(() => {
    if (isConnected) {
      sendMessage({ action: 'subscribe', symbol })
    }
  }, [symbol, isConnected, sendMessage])

  return {
    isConnected,
    ticker,
    orderBook,
    trades,
  }
}

/**
 * Hook for portfolio updates WebSocket
 */
export function usePortfolioWebSocket(accountId: string) {
  const [portfolio, setPortfolio] = useState<any>(null)
  const [positions, setPositions] = useState<any[]>([])
  const [recentTrades, setRecentTrades] = useState<any[]>([])

  const { isConnected } = useWebSocket('portfolio', {
    onMessage: (message) => {
      switch (message.type) {
        case 'portfolio_update':
          setPortfolio(message.data)
          break
        case 'position_update':
          setPositions(message.data.positions)
          break
        case 'trade_executed':
          setRecentTrades((prev) => [message.data, ...prev].slice(0, 20))
          break
      }
    },
  })

  return {
    isConnected,
    portfolio,
    positions,
    recentTrades,
  }
}

/**
 * Hook for trading signals WebSocket
 */
export function useTradingSignalsWebSocket() {
  const [signals, setSignals] = useState<any[]>([])
  const [alerts, setAlerts] = useState<any[]>([])

  const { isConnected } = useWebSocket('signals', {
    onMessage: (message) => {
      switch (message.type) {
        case 'trading_signal':
          setSignals((prev) => [message.data, ...prev].slice(0, 10))
          break
        case 'risk_alert':
          setAlerts((prev) => [message.data, ...prev].slice(0, 5))
          break
      }
    },
  })

  return {
    isConnected,
    signals,
    alerts,
  }
}
