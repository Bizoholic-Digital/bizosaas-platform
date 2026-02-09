'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  TrendingUp, TrendingDown, DollarSign, BarChart3, Activity, 
  ExternalLink, RefreshCw, AlertCircle, CheckCircle,
  Plus, Edit, Eye, Settings, Zap, Star, Bot,
  LineChart, PieChart, Target, Shield, AlertTriangle
} from 'lucide-react'
import { FeatureGate } from '@/components/tenant/feature-gate'

interface Portfolio {
  id: string
  name: string
  value: number
  change: number
  changePercent: number
  allocation: number
  status: 'active' | 'paused' | 'stopped'
  algorithm: string
}

interface Trade {
  id: string
  symbol: string
  type: 'buy' | 'sell'
  quantity: number
  price: number
  timestamp: string
  status: 'executed' | 'pending' | 'cancelled'
  profit?: number
}

interface Strategy {
  id: string
  name: string
  type: 'momentum' | 'mean-reversion' | 'arbitrage' | 'ml-based'
  performance: number
  sharpeRatio: number
  maxDrawdown: number
  status: 'active' | 'backtesting' | 'optimization'
}

export default function QuantTradeDashboard() {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([])
  const [trades, setTrades] = useState<Trade[]>([])
  const [strategies, setStrategies] = useState<Strategy[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [aiStatus, setAiStatus] = useState<'connecting' | 'connected' | 'error'>('connecting')

  useEffect(() => {
    const loadData = async () => {
      try {
        // Simulate loading
        setTimeout(() => {
          setPortfolios([
            { id: '1', name: 'Momentum Alpha', value: 125000, change: 3420, changePercent: 2.81, allocation: 45, status: 'active', algorithm: 'ML-Enhanced Momentum' },
            { id: '2', name: 'Arbitrage Pro', value: 87500, change: 1200, changePercent: 1.39, allocation: 32, status: 'active', algorithm: 'Statistical Arbitrage' },
            { id: '3', name: 'Risk Parity', value: 62000, change: -850, changePercent: -1.35, allocation: 23, status: 'paused', algorithm: 'Risk Parity Model' },
          ])
          
          setTrades([
            { id: '1', symbol: 'AAPL', type: 'buy', quantity: 100, price: 185.25, timestamp: '2025-09-11 09:30:15', status: 'executed', profit: 425 },
            { id: '2', symbol: 'MSFT', type: 'sell', quantity: 75, price: 412.80, timestamp: '2025-09-11 09:45:22', status: 'executed', profit: 892 },
            { id: '3', symbol: 'GOOGL', type: 'buy', quantity: 50, price: 145.60, timestamp: '2025-09-11 10:15:08', status: 'pending' },
            { id: '4', symbol: 'TSLA', type: 'sell', quantity: 25, price: 258.40, timestamp: '2025-09-11 10:30:45', status: 'executed', profit: -125 },
          ])
          
          setStrategies([
            { id: '1', name: 'Deep Learning Alpha', type: 'ml-based', performance: 18.5, sharpeRatio: 1.85, maxDrawdown: 8.2, status: 'active' },
            { id: '2', name: 'Mean Reversion Plus', type: 'mean-reversion', performance: 12.3, sharpeRatio: 1.42, maxDrawdown: 12.1, status: 'active' },
            { id: '3', name: 'Crypto Arbitrage', type: 'arbitrage', performance: 24.7, sharpeRatio: 2.12, maxDrawdown: 5.8, status: 'backtesting' },
          ])
          
          setAiStatus('connected')
          setIsLoading(false)
        }, 1500)
      } catch (error) {
        console.error('Error loading QuantTrade data:', error)
        setAiStatus('error')
        setIsLoading(false)
      }
    }
    
    loadData()
  }, [])

  const stats = [
    { title: 'Total Portfolio Value', value: '$274,500', change: '+$3,770', icon: DollarSign, positive: true },
    { title: 'Daily P&L', value: '+$1,192', change: '+2.1%', icon: TrendingUp, positive: true },
    { title: 'Active Strategies', value: '8', change: '+2', icon: Bot, positive: true },
    { title: 'Sharpe Ratio', value: '1.67', change: '+0.12', icon: Target, positive: true },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold">QuantTrade Dashboard</h1>
          <p className="text-muted-foreground mt-2">
            AI-powered algorithmic trading and portfolio management
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            {aiStatus === 'connected' ? (
              <>
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm text-green-600">AI Trading Active</span>
              </>
            ) : aiStatus === 'connecting' ? (
              <>
                <RefreshCw className="h-4 w-4 text-blue-500 animate-spin" />
                <span className="text-sm text-blue-600">Connecting...</span>
              </>
            ) : (
              <>
                <AlertCircle className="h-4 w-4 text-red-500" />
                <span className="text-sm text-red-600">Connection Error</span>
              </>
            )}
          </div>
          <Button 
            variant="outline" 
            size="sm"
            onClick={() => window.open('http://localhost:3005', '_blank')}
          >
            <ExternalLink className="h-4 w-4 mr-2" />
            Trading Terminal
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className={`text-xs ${stat.positive ? 'text-green-600' : 'text-red-600'}`}>
                {stat.change} from yesterday
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="portfolios">Portfolios</TabsTrigger>
          <TabsTrigger value="strategies">AI Strategies</TabsTrigger>
          <TabsTrigger value="trades">Live Trades</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Active Portfolios */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <PieChart className="h-5 w-5 mr-2 text-purple-500" />
                  Active Portfolios
                </CardTitle>
                <CardDescription>Real-time portfolio performance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {portfolios.slice(0, 3).map((portfolio) => (
                    <div key={portfolio.id} className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-r from-purple-400 to-blue-400 rounded-full flex items-center justify-center">
                          <span className="text-white font-medium">{portfolio.name.charAt(0)}</span>
                        </div>
                        <div>
                          <p className="font-medium">{portfolio.name}</p>
                          <p className="text-sm text-muted-foreground">{portfolio.algorithm}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-medium">${portfolio.value.toLocaleString()}</div>
                        <div className={`text-sm flex items-center ${portfolio.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {portfolio.change >= 0 ? <TrendingUp className="h-3 w-3 mr-1" /> : <TrendingDown className="h-3 w-3 mr-1" />}
                          {portfolio.changePercent > 0 ? '+' : ''}{portfolio.changePercent}%
                        </div>
                        <Badge variant={portfolio.status === 'active' ? 'default' : 'secondary'}>
                          {portfolio.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Recent Trades */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Activity className="h-5 w-5 mr-2 text-green-500" />
                  Recent Trades
                </CardTitle>
                <CardDescription>Latest algorithmic trades and executions</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {trades.slice(0, 4).map((trade) => (
                    <div key={trade.id} className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium
                          ${trade.type === 'buy' ? 'bg-green-500' : 'bg-red-500'}`}>
                          {trade.type === 'buy' ? '↗' : '↘'}
                        </div>
                        <div>
                          <p className="font-medium">{trade.symbol}</p>
                          <p className="text-sm text-muted-foreground">
                            {trade.type.toUpperCase()} {trade.quantity} @ ${trade.price}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        {trade.profit !== undefined && (
                          <div className={`font-medium ${trade.profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {trade.profit >= 0 ? '+' : ''}${trade.profit}
                          </div>
                        )}
                        <Badge variant={trade.status === 'executed' ? 'default' : trade.status === 'pending' ? 'secondary' : 'destructive'}>
                          {trade.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="portfolios">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>Portfolio Management</CardTitle>
                <CardDescription>Manage your algorithmic trading portfolios</CardDescription>
              </div>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Create Portfolio
              </Button>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {portfolios.map((portfolio) => (
                  <div key={portfolio.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gradient-to-r from-purple-400 to-blue-400 rounded-full flex items-center justify-center">
                        <span className="text-white font-medium">{portfolio.name.charAt(0)}</span>
                      </div>
                      <div>
                        <h3 className="font-medium">{portfolio.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          {portfolio.algorithm} • {portfolio.allocation}% allocation
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <div className="font-bold text-lg">${portfolio.value.toLocaleString()}</div>
                        <div className={`text-sm flex items-center ${portfolio.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {portfolio.change >= 0 ? <TrendingUp className="h-3 w-3 mr-1" /> : <TrendingDown className="h-3 w-3 mr-1" />}
                          {portfolio.change >= 0 ? '+' : ''}${Math.abs(portfolio.change)} ({portfolio.changePercent > 0 ? '+' : ''}{portfolio.changePercent}%)
                        </div>
                        <Badge variant={portfolio.status === 'active' ? 'default' : 'secondary'}>
                          {portfolio.status}
                        </Badge>
                      </div>
                      <div className="flex gap-2">
                        <Button variant="ghost" size="sm">
                          <Eye className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Settings className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="strategies">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>AI Trading Strategies</CardTitle>
                <CardDescription>Advanced algorithmic trading strategies powered by AI</CardDescription>
              </div>
              <FeatureGate 
                feature="ai-trading" 
                subscriptionTier="enterprise"
                fallback={
                  <Button disabled>
                    <Bot className="h-4 w-4 mr-2" />
                    Deploy Strategy (Enterprise)
                  </Button>
                }
              >
                <Button>
                  <Bot className="h-4 w-4 mr-2" />
                  Deploy Strategy
                </Button>
              </FeatureGate>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {strategies.map((strategy) => (
                  <div key={strategy.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gradient-to-r from-indigo-400 to-purple-400 rounded-full flex items-center justify-center">
                        <Bot className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <h3 className="font-medium">{strategy.name}</h3>
                        <p className="text-sm text-muted-foreground capitalize">
                          {strategy.type.replace('-', ' ')} • Max DD: {strategy.maxDrawdown}%
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className="text-center">
                        <div className="text-sm text-muted-foreground">Performance</div>
                        <div className="font-bold text-green-600">+{strategy.performance}%</div>
                      </div>
                      <div className="text-center">
                        <div className="text-sm text-muted-foreground">Sharpe Ratio</div>
                        <div className="font-bold">{strategy.sharpeRatio}</div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant={
                          strategy.status === 'active' ? 'default' : 
                          strategy.status === 'backtesting' ? 'secondary' : 'outline'
                        }>
                          {strategy.status}
                        </Badge>
                        <Button variant="ghost" size="sm">
                          <Settings className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="trades">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>Live Trading Activity</CardTitle>
                <CardDescription>Real-time trade execution and monitoring</CardDescription>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Refresh
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {trades.map((trade) => (
                  <div key={trade.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-medium
                        ${trade.type === 'buy' ? 'bg-green-500' : 'bg-red-500'}`}>
                        {trade.type === 'buy' ? '↗' : '↘'}
                      </div>
                      <div>
                        <h3 className="font-medium">{trade.symbol}</h3>
                        <p className="text-sm text-muted-foreground">
                          {trade.type.toUpperCase()} {trade.quantity} shares @ ${trade.price}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className="text-center">
                        <div className="text-sm text-muted-foreground">Time</div>
                        <div className="font-medium">{trade.timestamp.split(' ')[1]}</div>
                      </div>
                      <div className="text-center">
                        <div className="text-sm text-muted-foreground">Value</div>
                        <div className="font-medium">${(trade.quantity * trade.price).toLocaleString()}</div>
                      </div>
                      {trade.profit !== undefined && (
                        <div className="text-center">
                          <div className="text-sm text-muted-foreground">P&L</div>
                          <div className={`font-bold ${trade.profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {trade.profit >= 0 ? '+' : ''}${trade.profit}
                          </div>
                        </div>
                      )}
                      <Badge variant={
                        trade.status === 'executed' ? 'default' : 
                        trade.status === 'pending' ? 'secondary' : 'destructive'
                      }>
                        {trade.status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Performance Analytics</CardTitle>
                <CardDescription>Comprehensive trading performance metrics</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span>Total Return (YTD)</span>
                    <span className="font-semibold text-green-600">+24.7%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Sharpe Ratio</span>
                    <span className="font-semibold">1.67</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Max Drawdown</span>
                    <span className="font-semibold text-red-600">-8.2%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Win Rate</span>
                    <span className="font-semibold">67.3%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Avg Trade Duration</span>
                    <span className="font-semibold">2.4 hours</span>
                  </div>
                  <div className="flex justify-between text-green-600">
                    <span>Risk-Adjusted Return</span>
                    <span className="font-semibold">18.5%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>AI Insights</CardTitle>
                <CardDescription>Machine learning recommendations and alerts</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="p-3 bg-green-50 rounded-lg border-l-4 border-green-400">
                    <p className="text-sm">📈 <strong>Market Opportunity:</strong> Tech sector showing strong momentum signals - consider increasing allocation</p>
                  </div>
                  <div className="p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                    <p className="text-sm">⚠️ <strong>Risk Alert:</strong> VIX spike detected - reducing position sizes by 15% automatically</p>
                  </div>
                  <div className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-400">
                    <p className="text-sm">🤖 <strong>Strategy Update:</strong> Deep Learning Alpha model retrained with 97.2% accuracy</p>
                  </div>
                  <div className="p-3 bg-purple-50 rounded-lg border-l-4 border-purple-400">
                    <p className="text-sm">💎 <strong>Backtesting:</strong> New crypto arbitrage strategy shows 31% annual return potential</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="settings">
          <Card>
            <CardHeader>
              <CardTitle>QuantTrade Settings</CardTitle>
              <CardDescription>Configure your trading parameters and risk management</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-medium mb-3 flex items-center">
                    <Shield className="h-4 w-4 mr-2" />
                    Risk Management
                  </h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Max Portfolio Risk</span>
                      <Badge variant="outline">2% per trade</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Stop Loss</span>
                      <Badge variant="outline">-5%</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Position Sizing</span>
                      <Badge variant="outline">Kelly Criterion</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Max Drawdown Alert</span>
                      <Badge variant="destructive">-10%</Badge>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="font-medium mb-3 flex items-center">
                    <Bot className="h-4 w-4 mr-2" />
                    AI Configuration
                  </h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Model Retraining</span>
                      <Badge variant="outline">Weekly</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Signal Confidence</span>
                      <Badge variant="outline">75%+</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Market Regime Detection</span>
                      <Badge variant="default">Enabled</Badge>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="font-medium mb-3">Quick Actions</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  <Button variant="outline" className="justify-start">
                    <Settings className="h-4 w-4 mr-2" />
                    Strategy Configuration
                  </Button>
                  <Button variant="outline" className="justify-start">
                    <Shield className="h-4 w-4 mr-2" />
                    Risk Parameters
                  </Button>
                  <Button variant="outline" className="justify-start">
                    <LineChart className="h-4 w-4 mr-2" />
                    Backtesting Lab
                  </Button>
                  <Button variant="outline" className="justify-start">
                    <ExternalLink className="h-4 w-4 mr-2" />
                    Trading Terminal
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}