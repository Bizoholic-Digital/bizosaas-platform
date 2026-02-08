/**
 * API Client for QuantTrade Backend
 * Handles all HTTP requests to the FastAPI backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8012'

export interface ApiResponse<T> {
  data?: T
  error?: string
  success: boolean
}

class ApiClient {
  private baseUrl: string
  private token: string | null = null

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  setToken(token: string) {
    this.token = token
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(this.token && { Authorization: `Bearer ${this.token}` }),
      ...options.headers,
    }

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          success: false,
          error: data.detail || 'Request failed',
        }
      }

      return {
        success: true,
        data,
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      }
    }
  }

  // Portfolio endpoints
  async getPortfolio(accountId: string) {
    return this.request(`/api/portfolio/${accountId}`, { method: 'GET' })
  }

  async getPositions(accountId: string) {
    return this.request(`/api/portfolio/${accountId}/positions`, { method: 'GET' })
  }

  async getTrades(accountId: string, limit: number = 50) {
    return this.request(`/api/portfolio/${accountId}/trades?limit=${limit}`, { method: 'GET' })
  }

  // Market data endpoints
  async getMarketData(symbol: string, interval: string = '1h', limit: number = 100) {
    return this.request(`/api/market-data/${symbol}?interval=${interval}&limit=${limit}`, { method: 'GET' })
  }

  async getTicker(symbol: string) {
    return this.request(`/api/market-data/${symbol}/ticker`, { method: 'GET' })
  }

  async getOrderBook(symbol: string, depth: number = 20) {
    return this.request(`/api/market-data/${symbol}/orderbook?depth=${depth}`, { method: 'GET' })
  }

  // Trading endpoints
  async placeOrder(orderData: {
    symbol: string
    side: 'buy' | 'sell'
    type: 'market' | 'limit'
    quantity: number
    price?: number
  }) {
    return this.request('/api/trading/orders', {
      method: 'POST',
      body: JSON.stringify(orderData),
    })
  }

  async cancelOrder(orderId: string) {
    return this.request(`/api/trading/orders/${orderId}`, { method: 'DELETE' })
  }

  async getOpenOrders(accountId: string) {
    return this.request(`/api/trading/orders/${accountId}/open`, { method: 'GET' })
  }

  // Strategy endpoints
  async getStrategies(accountId: string) {
    return this.request(`/api/strategies/${accountId}`, { method: 'GET' })
  }

  async activateStrategy(strategyId: string) {
    return this.request(`/api/strategies/${strategyId}/activate`, { method: 'POST' })
  }

  async deactivateStrategy(strategyId: string) {
    return this.request(`/api/strategies/${strategyId}/deactivate`, { method: 'POST' })
  }

  async getStrategyPerformance(strategyId: string) {
    return this.request(`/api/strategies/${strategyId}/performance`, { method: 'GET' })
  }

  // Backtesting endpoints
  async runBacktest(backtestData: {
    strategy_id: string
    start_date: string
    end_date: string
    initial_capital: number
  }) {
    return this.request('/api/backtest/run', {
      method: 'POST',
      body: JSON.stringify(backtestData),
    })
  }

  async getBacktestResults(backtestId: string) {
    return this.request(`/api/backtest/${backtestId}/results`, { method: 'GET' })
  }

  // Risk endpoints
  async getRiskMetrics(accountId: string) {
    return this.request(`/api/risk/${accountId}/metrics`, { method: 'GET' })
  }

  async getRiskLimits(accountId: string) {
    return this.request(`/api/risk/${accountId}/limits`, { method: 'GET' })
  }

  async updateRiskLimits(accountId: string, limits: any) {
    return this.request(`/api/risk/${accountId}/limits`, {
      method: 'PUT',
      body: JSON.stringify(limits),
    })
  }

  // AI Agents endpoints
  async getAgentStatus() {
    return this.request('/api/agents/status', { method: 'GET' })
  }

  async triggerAgent(agentName: string, params: any) {
    return this.request(`/api/agents/${agentName}/trigger`, {
      method: 'POST',
      body: JSON.stringify(params),
    })
  }
}

export const apiClient = new ApiClient()
export default apiClient
