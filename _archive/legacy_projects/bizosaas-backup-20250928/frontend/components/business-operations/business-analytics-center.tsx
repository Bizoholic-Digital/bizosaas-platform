"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { toast } from "sonner";
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Users,
  DollarSign,
  ShoppingCart,
  Clock,
  Target,
  Eye,
  MousePointer,
  RefreshCw,
  Download,
  Filter,
  Calendar,
  PieChart,
  LineChart,
  Activity,
  Globe,
  Smartphone,
  Monitor,
  Tablet
} from "lucide-react";
import { ResponsiveContainer, LineChart as RechartsLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart as RechartsBarChart, Bar, PieChart as RechartsPieChart, Pie, Cell, AreaChart, Area } from "recharts";

interface AnalyticsMetrics {
  totalVisitors: number;
  uniqueVisitors: number;
  pageViews: number;
  bounceRate: number;
  avgSessionDuration: string;
  conversionRate: number;
  revenue: number;
  goalCompletions: number;
}

interface TrafficSource {
  source: string;
  visitors: number;
  percentage: number;
  conversionRate: number;
}

interface DeviceStats {
  device: string;
  sessions: number;
  percentage: number;
  bounceRate: number;
}

interface GeographicData {
  country: string;
  sessions: number;
  percentage: number;
  revenue: number;
}

export function BusinessAnalyticsCenter() {
  const [timeRange, setTimeRange] = useState<string>('30d');
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Mock data
  const mockMetrics: AnalyticsMetrics = {
    totalVisitors: 42580,
    uniqueVisitors: 38420,
    pageViews: 127350,
    bounceRate: 32.1,
    avgSessionDuration: "3m 24s",
    conversionRate: 4.2,
    revenue: 125600,
    goalCompletions: 1789
  };

  const trafficSources: TrafficSource[] = [
    { source: "Organic Search", visitors: 18520, percentage: 43.5, conversionRate: 5.2 },
    { source: "Direct", visitors: 12340, percentage: 29.0, conversionRate: 6.8 },
    { source: "Social Media", visitors: 6850, percentage: 16.1, conversionRate: 2.9 },
    { source: "Paid Search", visitors: 3210, percentage: 7.5, conversionRate: 8.1 },
    { source: "Email", visitors: 1660, percentage: 3.9, conversionRate: 12.3 }
  ];

  const deviceStats: DeviceStats[] = [
    { device: "Desktop", sessions: 19780, percentage: 46.4, bounceRate: 28.5 },
    { device: "Mobile", sessions: 17650, percentage: 41.4, bounceRate: 35.2 },
    { device: "Tablet", sessions: 5150, percentage: 12.1, bounceRate: 31.8 }
  ];

  const geographicData: GeographicData[] = [
    { country: "India", sessions: 28340, percentage: 66.6, revenue: 83720 },
    { country: "United States", sessions: 6420, percentage: 15.1, revenue: 25340 },
    { country: "United Kingdom", sessions: 3210, percentage: 7.5, revenue: 8920 },
    { country: "Canada", sessions: 2150, percentage: 5.0, revenue: 4850 },
    { country: "Australia", sessions: 1460, percentage: 3.4, revenue: 2770 },
    { country: "Others", sessions: 1000, percentage: 2.3, revenue: 1000 }
  ];

  // Mock time series data
  const visitorTrend = [
    { date: "2024-01-01", visitors: 1420, pageViews: 3850, revenue: 4200 },
    { date: "2024-01-02", visitors: 1680, pageViews: 4200, revenue: 5100 },
    { date: "2024-01-03", visitors: 1520, pageViews: 3950, revenue: 4650 },
    { date: "2024-01-04", visitors: 1890, pageViews: 4850, revenue: 6200 },
    { date: "2024-01-05", visitors: 2100, pageViews: 5200, revenue: 7800 },
    { date: "2024-01-06", visitors: 1750, pageViews: 4100, revenue: 5850 },
    { date: "2024-01-07", visitors: 1650, pageViews: 3800, revenue: 4950 }
  ];

  const conversionFunnel = [
    { stage: "Visitors", count: 42580, percentage: 100 },
    { stage: "Product Views", count: 21290, percentage: 50 },
    { stage: "Add to Cart", count: 8516, percentage: 20 },
    { stage: "Checkout", count: 2129, percentage: 5 },
    { stage: "Purchase", count: 1789, percentage: 4.2 }
  ];

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1'];

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsRefreshing(false);
    toast.success("Analytics data refreshed");
  };

  const handleExport = () => {
    toast.success("Analytics report exported");
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Business Analytics Center</h2>
          <p className="text-muted-foreground">
            Comprehensive business intelligence and performance analytics
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-[120px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">Last 7 days</SelectItem>
              <SelectItem value="30d">Last 30 days</SelectItem>
              <SelectItem value="90d">Last 90 days</SelectItem>
              <SelectItem value="1y">Last year</SelectItem>
            </SelectContent>
          </Select>
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={isRefreshing}
          >
            <RefreshCw className={`mr-2 h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button variant="outline" size="sm" onClick={handleExport}>
            <Download className="mr-2 h-4 w-4" />
            Export
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Visitors</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockMetrics.totalVisitors.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="inline h-3 w-3 text-green-500 mr-1" />
              +12.5% from last period
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₹{mockMetrics.revenue.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="inline h-3 w-3 text-green-500 mr-1" />
              +18.7% from last period
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockMetrics.conversionRate}%</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="inline h-3 w-3 text-green-500 mr-1" />
              +0.8% from last period
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Bounce Rate</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockMetrics.bounceRate}%</div>
            <p className="text-xs text-muted-foreground">
              <TrendingDown className="inline h-3 w-3 text-green-500 mr-1" />
              -2.3% from last period
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="traffic">Traffic Sources</TabsTrigger>
          <TabsTrigger value="audience">Audience</TabsTrigger>
          <TabsTrigger value="conversions">Conversions</TabsTrigger>
          <TabsTrigger value="ecommerce">E-commerce</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          {/* Visitor Trend Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Visitor Trends</CardTitle>
              <CardDescription>Daily visitors, page views, and revenue over time</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={visitorTrend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="visitors" stackId="1" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                  <Area type="monotone" dataKey="pageViews" stackId="2" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Additional Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Session Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Page Views</span>
                    <span className="font-medium">{mockMetrics.pageViews.toLocaleString()}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Avg. Session Duration</span>
                    <span className="font-medium">{mockMetrics.avgSessionDuration}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Pages per Session</span>
                    <span className="font-medium">2.99</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Goal Completions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="text-2xl font-bold">{mockMetrics.goalCompletions}</div>
                    <p className="text-sm text-muted-foreground">Total completions</p>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Contact Form</span>
                      <span>892</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Newsletter Signup</span>
                      <span>567</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Demo Request</span>
                      <span>330</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Real-time Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-sm">247 active users</span>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Top Page</span>
                      <span>/services</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Top Source</span>
                      <span>Google</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Avg. Load Time</span>
                      <span>1.8s</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="traffic" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Traffic Sources Table */}
            <Card>
              <CardHeader>
                <CardTitle>Traffic Sources</CardTitle>
                <CardDescription>Where your visitors are coming from</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {trafficSources.map((source, index) => (
                    <div key={source.source} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="space-y-1">
                        <div className="font-medium">{source.source}</div>
                        <div className="text-sm text-muted-foreground">
                          {source.visitors.toLocaleString()} visitors ({source.percentage}%)
                        </div>
                      </div>
                      <div className="text-right space-y-1">
                        <div className="text-sm font-medium">{source.conversionRate}% CVR</div>
                        <Progress value={source.percentage} className="w-20 h-2" />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Traffic Sources Pie Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Traffic Distribution</CardTitle>
                <CardDescription>Visual breakdown of traffic sources</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RechartsPieChart>
                    <Pie
                      data={trafficSources}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ percentage }) => `${percentage.toFixed(1)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="visitors"
                    >
                      {trafficSources.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </RechartsPieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="audience" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Device Statistics */}
            <Card>
              <CardHeader>
                <CardTitle>Device Categories</CardTitle>
                <CardDescription>User sessions by device type</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {deviceStats.map((device) => {
                    const deviceIcons = {
                      Desktop: Monitor,
                      Mobile: Smartphone,
                      Tablet: Tablet
                    };
                    const IconComponent = deviceIcons[device.device as keyof typeof deviceIcons];
                    
                    return (
                      <div key={device.device} className="flex items-center justify-between p-3 border rounded-lg">
                        <div className="flex items-center space-x-3">
                          <IconComponent className="h-5 w-5 text-muted-foreground" />
                          <div>
                            <div className="font-medium">{device.device}</div>
                            <div className="text-sm text-muted-foreground">
                              {device.sessions.toLocaleString()} sessions
                            </div>
                          </div>
                        </div>
                        <div className="text-right space-y-1">
                          <div className="text-sm font-medium">{device.percentage}%</div>
                          <div className="text-xs text-muted-foreground">
                            {device.bounceRate}% bounce
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>

            {/* Geographic Data */}
            <Card>
              <CardHeader>
                <CardTitle>Geographic Distribution</CardTitle>
                <CardDescription>Sessions and revenue by country</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {geographicData.map((geo) => (
                    <div key={geo.country} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="space-y-1">
                        <div className="font-medium">{geo.country}</div>
                        <div className="text-sm text-muted-foreground">
                          {geo.sessions.toLocaleString()} sessions ({geo.percentage}%)
                        </div>
                      </div>
                      <div className="text-right space-y-1">
                        <div className="text-sm font-medium">₹{geo.revenue.toLocaleString()}</div>
                        <Progress value={geo.percentage} className="w-20 h-2" />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="conversions" className="space-y-6">
          {/* Conversion Funnel */}
          <Card>
            <CardHeader>
              <CardTitle>Conversion Funnel</CardTitle>
              <CardDescription>User journey from visitor to customer</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {conversionFunnel.map((stage, index) => (
                  <div key={stage.stage} className="relative">
                    <div className="flex items-center justify-between p-4 border rounded-lg bg-gradient-to-r from-blue-50 to-transparent">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-medium">
                          {index + 1}
                        </div>
                        <div>
                          <div className="font-medium">{stage.stage}</div>
                          <div className="text-sm text-muted-foreground">
                            {stage.count.toLocaleString()} users
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold">{stage.percentage}%</div>
                        {index > 0 && (
                          <div className="text-sm text-muted-foreground">
                            {((stage.count / conversionFunnel[index - 1].count) * 100).toFixed(1)}% conversion
                          </div>
                        )}
                      </div>
                    </div>
                    {index < conversionFunnel.length - 1 && (
                      <div className="absolute left-4 top-full w-px h-4 bg-border"></div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="ecommerce" className="space-y-6">
          {/* E-commerce Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Revenue Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="text-2xl font-bold">₹{mockMetrics.revenue.toLocaleString()}</div>
                    <p className="text-sm text-muted-foreground">Total revenue</p>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Avg. Order Value</span>
                      <span>₹703</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Total Orders</span>
                      <span>1,789</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Revenue per Visitor</span>
                      <span>₹2.95</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Product Performance</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Top Product</span>
                      <span>AI Pro Plan</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Units Sold</span>
                      <span>542</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Revenue</span>
                      <span>₹37,940</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Shopping Behavior</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Cart Abandonment</span>
                      <span>67.2%</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Checkout Completion</span>
                      <span>32.8%</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Return Rate</span>
                      <span>3.4%</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}