'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { MoreHorizontal, TrendingUp, Eye, MousePointer, DollarSign } from 'lucide-react'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts'

interface ChartData {
  name: string
  impressions: number
  clicks: number
  conversions: number
  revenue: number
  ctr: number
  cpc: number
}

const generateMockData = (): ChartData[] => {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  return days.map(day => ({
    name: day,
    impressions: Math.floor(Math.random() * 10000) + 5000,
    clicks: Math.floor(Math.random() * 500) + 200,
    conversions: Math.floor(Math.random() * 50) + 20,
    revenue: Math.floor(Math.random() * 2000) + 1000,
    ctr: (Math.random() * 3) + 2,
    cpc: (Math.random() * 2) + 1
  }))
}

export function CampaignMetrics() {
  const [data, setData] = useState<ChartData[]>([])
  const [activeTab, setActiveTab] = useState('performance')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 800))
      setData(generateMockData())
      setLoading(false)
    }

    fetchData()
    
    // Update data every minute for real-time feel
    const interval = setInterval(() => {
      setData(generateMockData())
    }, 60000)

    return () => clearInterval(interval)
  }, [])

  const totalImpressions = data.reduce((sum, item) => sum + item.impressions, 0)
  const totalClicks = data.reduce((sum, item) => sum + item.clicks, 0)
  const totalRevenue = data.reduce((sum, item) => sum + item.revenue, 0)
  const avgCTR = data.length > 0 ? (totalClicks / totalImpressions) * 100 : 0

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Campaign Performance</CardTitle>
          <CardDescription>Real-time campaign metrics and trends</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[300px] w-full animate-pulse bg-muted rounded" />
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Campaign Performance</CardTitle>
            <CardDescription>Real-time campaign metrics and trends</CardDescription>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant="outline" className="text-green-600 border-green-200">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse" />
              Live
            </Badge>
            <Button variant="ghost" size="icon">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="performance">Performance</TabsTrigger>
            <TabsTrigger value="revenue">Revenue</TabsTrigger>
            <TabsTrigger value="engagement">Engagement</TabsTrigger>
          </TabsList>
          
          {/* Summary Cards */}
          <div className="grid grid-cols-4 gap-4 mb-6">
            <div className="text-center">
              <div className="flex items-center justify-center mb-1">
                <Eye className="h-4 w-4 text-blue-500 mr-1" />
              </div>
              <div className="text-2xl font-bold">{totalImpressions.toLocaleString()}</div>
              <div className="text-xs text-muted-foreground">Impressions</div>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center mb-1">
                <MousePointer className="h-4 w-4 text-green-500 mr-1" />
              </div>
              <div className="text-2xl font-bold">{totalClicks.toLocaleString()}</div>
              <div className="text-xs text-muted-foreground">Clicks</div>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center mb-1">
                <TrendingUp className="h-4 w-4 text-purple-500 mr-1" />
              </div>
              <div className="text-2xl font-bold">{avgCTR.toFixed(2)}%</div>
              <div className="text-xs text-muted-foreground">CTR</div>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center mb-1">
                <DollarSign className="h-4 w-4 text-orange-500 mr-1" />
              </div>
              <div className="text-2xl font-bold">${totalRevenue.toLocaleString()}</div>
              <div className="text-xs text-muted-foreground">Revenue</div>
            </div>
          </div>

          <TabsContent value="performance" className="space-y-4">
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data}>
                  <defs>
                    <linearGradient id="impressions" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="clicks" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                  <XAxis dataKey="name" className="text-xs" />
                  <YAxis className="text-xs" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'hsl(var(--background))', 
                      border: '1px solid hsl(var(--border))' 
                    }} 
                  />
                  <Area
                    type="monotone"
                    dataKey="impressions"
                    stroke="#3b82f6"
                    fillOpacity={1}
                    fill="url(#impressions)"
                    name="Impressions"
                  />
                  <Area
                    type="monotone"
                    dataKey="clicks"
                    stroke="#10b981"
                    fillOpacity={1}
                    fill="url(#clicks)"
                    name="Clicks"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>
          
          <TabsContent value="revenue" className="space-y-4">
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                  <XAxis dataKey="name" className="text-xs" />
                  <YAxis className="text-xs" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'hsl(var(--background))', 
                      border: '1px solid hsl(var(--border))' 
                    }} 
                  />
                  <Bar dataKey="revenue" fill="#f59e0b" radius={[4, 4, 0, 0]} name="Revenue ($)" />
                  <Bar dataKey="conversions" fill="#8b5cf6" radius={[4, 4, 0, 0]} name="Conversions" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>
          
          <TabsContent value="engagement" className="space-y-4">
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                  <XAxis dataKey="name" className="text-xs" />
                  <YAxis className="text-xs" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'hsl(var(--background))', 
                      border: '1px solid hsl(var(--border))' 
                    }} 
                  />
                  <Line
                    type="monotone"
                    dataKey="ctr"
                    stroke="#ec4899"
                    strokeWidth={3}
                    dot={{ fill: '#ec4899', r: 6 }}
                    name="CTR (%)"
                  />
                  <Line
                    type="monotone"
                    dataKey="cpc"
                    stroke="#06b6d4"
                    strokeWidth={3}
                    dot={{ fill: '#06b6d4', r: 6 }}
                    name="CPC ($)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}