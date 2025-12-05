"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  CreditCard,
  MessageSquare,
  Search,
  TrendingUp,
  DollarSign,
  Users,
  Globe,
  BarChart3,
  Mail,
  Phone,
  Megaphone,
  Target,
  Activity,
  CheckCircle2,
  AlertCircle,
  Clock,
  Zap
} from "lucide-react";

// Import business operation components
import { PaymentProcessingDashboard } from "@/components/business-operations/payment-processing-dashboard";
import { CommunicationCenter } from "@/components/business-operations/communication-center";
import { SEOSuiteDashboard } from "@/components/business-operations/seo-suite-dashboard";
import { BusinessAnalyticsCenter } from "@/components/business-operations/business-analytics-center";

export default function BusinessOperationsPage() {
  const [activeTab, setActiveTab] = useState("overview");

  // Mock data for overview stats
  const operationsStats = {
    payments: {
      totalRevenue: 125600,
      monthlyGrowth: 18.5,
      activeGateways: 4,
      successRate: 98.2
    },
    communications: {
      totalCampaigns: 48,
      deliveryRate: 94.7,
      openRate: 27.3,
      activeChannels: 5
    },
    seo: {
      avgRanking: 12.4,
      organicTraffic: 15420,
      indexedPages: 1247,
      domainAuthority: 68
    },
    analytics: {
      totalVisitors: 42580,
      conversionRate: 4.2,
      avgSessionTime: "3m 24s",
      bounceRate: 32.1
    }
  };

  const quickActions = [
    {
      title: "Process Payment",
      description: "Create new payment order",
      icon: CreditCard,
      action: () => setActiveTab("payments"),
      badge: "4 Gateways"
    },
    {
      title: "Send Campaign",
      description: "Launch marketing campaign",
      icon: Megaphone,
      action: () => setActiveTab("communications"),
      badge: "5 Channels"
    },
    {
      title: "SEO Analysis",
      description: "Run comprehensive SEO audit",
      icon: Search,
      action: () => setActiveTab("seo"),
      badge: "6 Engines"
    },
    {
      title: "View Analytics",
      description: "Access business insights",
      icon: BarChart3,
      action: () => setActiveTab("analytics"),
      badge: "Real-time"
    }
  ];

  return (
    <div className="container mx-auto py-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col space-y-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Business Operations</h1>
          <p className="text-muted-foreground">
            Comprehensive business management hub with payment processing, communications, SEO, and analytics
          </p>
        </div>

        {/* System Status */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="h-4 w-4 text-green-500" />
            <span className="text-sm text-green-600">All Systems Operational</span>
          </div>
          <Separator orientation="vertical" className="h-4" />
          <div className="flex items-center space-x-2">
            <Activity className="h-4 w-4 text-blue-500" />
            <span className="text-sm text-blue-600">Real-time Monitoring Active</span>
          </div>
          <Separator orientation="vertical" className="h-4" />
          <div className="flex items-center space-x-2">
            <Zap className="h-4 w-4 text-yellow-500" />
            <span className="text-sm text-yellow-600">Auto-optimization Enabled</span>
          </div>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="payments">Payments</TabsTrigger>
          <TabsTrigger value="communications">Communications</TabsTrigger>
          <TabsTrigger value="seo">SEO Suite</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {quickActions.map((action, index) => {
              const IconComponent = action.icon;
              return (
                <Card key={index} className="hover:shadow-md transition-shadow cursor-pointer" onClick={action.action}>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">{action.title}</CardTitle>
                    <IconComponent className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <p className="text-xs text-muted-foreground mb-2">{action.description}</p>
                    <Badge variant="secondary" className="text-xs">{action.badge}</Badge>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Operations Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Payments Overview */}
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Payment Processing</CardTitle>
                <CreditCard className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  ${operationsStats.payments.totalRevenue.toLocaleString()}
                </div>
                <p className="text-xs text-muted-foreground">
                  +{operationsStats.payments.monthlyGrowth}% from last month
                </p>
                <div className="flex items-center justify-between mt-2">
                  <span className="text-xs">Success Rate</span>
                  <span className="text-xs font-medium">{operationsStats.payments.successRate}%</span>
                </div>
              </CardContent>
            </Card>

            {/* Communications Overview */}
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Communications</CardTitle>
                <MessageSquare className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{operationsStats.communications.totalCampaigns}</div>
                <p className="text-xs text-muted-foreground">Active campaigns</p>
                <div className="flex items-center justify-between mt-2">
                  <span className="text-xs">Delivery Rate</span>
                  <span className="text-xs font-medium">{operationsStats.communications.deliveryRate}%</span>
                </div>
              </CardContent>
            </Card>

            {/* SEO Overview */}
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">SEO Performance</CardTitle>
                <Search className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{operationsStats.seo.avgRanking}</div>
                <p className="text-xs text-muted-foreground">Average ranking position</p>
                <div className="flex items-center justify-between mt-2">
                  <span className="text-xs">Organic Traffic</span>
                  <span className="text-xs font-medium">{operationsStats.seo.organicTraffic.toLocaleString()}</span>
                </div>
              </CardContent>
            </Card>

            {/* Analytics Overview */}
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Business Analytics</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{operationsStats.analytics.totalVisitors.toLocaleString()}</div>
                <p className="text-xs text-muted-foreground">Total visitors this month</p>
                <div className="flex items-center justify-between mt-2">
                  <span className="text-xs">Conversion Rate</span>
                  <span className="text-xs font-medium">{operationsStats.analytics.conversionRate}%</span>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Business Activity</CardTitle>
              <CardDescription>Latest operations across all business functions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  {
                    icon: CreditCard,
                    title: "Payment processed via Razorpay",
                    description: "$1,299 subscription payment for Enterprise plan",
                    time: "2 minutes ago",
                    status: "success"
                  },
                  {
                    icon: Mail,
                    title: "Email campaign launched",
                    description: "Product announcement sent to 5,420 subscribers",
                    time: "15 minutes ago",
                    status: "active"
                  },
                  {
                    icon: Search,
                    title: "SEO audit completed",
                    description: "Identified 12 optimization opportunities",
                    time: "1 hour ago",
                    status: "completed"
                  },
                  {
                    icon: BarChart3,
                    title: "Analytics report generated",
                    description: "Weekly performance summary ready for review",
                    time: "2 hours ago",
                    status: "ready"
                  }
                ].map((activity, index) => {
                  const IconComponent = activity.icon;
                  return (
                    <div key={index} className="flex items-center space-x-4">
                      <div className="p-2 bg-muted rounded-full">
                        <IconComponent className="h-4 w-4" />
                      </div>
                      <div className="flex-1 space-y-1">
                        <p className="text-sm font-medium leading-none">{activity.title}</p>
                        <p className="text-sm text-muted-foreground">{activity.description}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Clock className="h-3 w-3 text-muted-foreground" />
                        <span className="text-xs text-muted-foreground">{activity.time}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Payment Processing Tab */}
        <TabsContent value="payments">
          <PaymentProcessingDashboard />
        </TabsContent>

        {/* Communications Tab */}
        <TabsContent value="communications">
          <CommunicationCenter />
        </TabsContent>

        {/* SEO Suite Tab */}
        <TabsContent value="seo">
          <SEOSuiteDashboard />
        </TabsContent>

        {/* Analytics Tab */}
        <TabsContent value="analytics">
          <BusinessAnalyticsCenter />
        </TabsContent>
      </Tabs>
    </div>
  );
}