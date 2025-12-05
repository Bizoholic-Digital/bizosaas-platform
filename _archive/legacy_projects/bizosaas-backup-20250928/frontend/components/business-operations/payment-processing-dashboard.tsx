"use client";

import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { DataTable } from "@/components/ui/data-table";
import { toast } from "sonner";
import {
  CreditCard,
  DollarSign,
  TrendingUp,
  TrendingDown,
  RefreshCw,
  Plus,
  Settings,
  AlertCircle,
  CheckCircle2,
  Clock,
  ExternalLink,
  Download,
  Eye,
  MoreHorizontal,
  Filter,
  Search
} from "lucide-react";
import { paymentGateways, subscriptionPlans, PaymentGateway, paymentUtils } from "@/lib/payments";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { ColumnDef } from "@tanstack/react-table";
import { formatDistanceToNow } from "date-fns";

interface PaymentTransaction {
  id: string;
  orderId: string;
  amount: number;
  currency: string;
  gateway: PaymentGateway;
  status: 'pending' | 'completed' | 'failed' | 'refunded';
  customerEmail: string;
  planId?: string;
  createdAt: string;
  updatedAt: string;
  gatewayTransactionId?: string;
}

interface PaymentStats {
  totalRevenue: number;
  monthlyRevenue: number;
  transactionCount: number;
  successRate: number;
  avgTransactionValue: number;
  gatewayStats: Record<PaymentGateway, {
    count: number;
    revenue: number;
    successRate: number;
  }>;
}

export function PaymentProcessingDashboard() {
  const [selectedGateway, setSelectedGateway] = useState<PaymentGateway>('razorpay');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isRefreshingStats, setIsRefreshingStats] = useState(false);

  // Mock data for demonstration
  const mockStats: PaymentStats = {
    totalRevenue: 125600,
    monthlyRevenue: 42300,
    transactionCount: 1247,
    successRate: 98.2,
    avgTransactionValue: 100.7,
    gatewayStats: {
      razorpay: { count: 623, revenue: 62300, successRate: 99.1 },
      paypal: { count: 312, revenue: 31200, successRate: 97.8 },
      payu: { count: 203, revenue: 20300, successRate: 98.5 },
      stripe: { count: 109, revenue: 11800, successRate: 96.3 }
    }
  };

  const mockTransactions: PaymentTransaction[] = [
    {
      id: 'txn_001',
      orderId: 'order_BzL001',
      amount: 69990,
      currency: 'INR',
      gateway: 'razorpay',
      status: 'completed',
      customerEmail: 'customer@example.com',
      planId: 'professional',
      createdAt: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
      updatedAt: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
      gatewayTransactionId: 'pay_BzL123ABC'
    },
    {
      id: 'txn_002',
      orderId: 'order_BzL002',
      amount: 29990,
      currency: 'INR',
      gateway: 'payu',
      status: 'pending',
      customerEmail: 'user@startup.com',
      planId: 'starter',
      createdAt: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
      updatedAt: new Date(Date.now() - 1000 * 60 * 40).toISOString(),
      gatewayTransactionId: 'payu_xyz789'
    }
  ];

  // Payment transaction columns
  const columns: ColumnDef<PaymentTransaction>[] = [
    {
      accessorKey: "orderId",
      header: "Order ID",
      cell: ({ row }) => (
        <div className="flex items-center space-x-2">
          <code className="text-sm bg-muted px-2 py-1 rounded">{row.getValue("orderId")}</code>
        </div>
      ),
    },
    {
      accessorKey: "amount",
      header: "Amount",
      cell: ({ row }) => {
        const amount = parseFloat(row.getValue("amount"));
        const currency = row.original.currency;
        return (
          <div className="font-medium">
            {paymentUtils.formatPrice(amount, currency as any)}
          </div>
        );
      },
    },
    {
      accessorKey: "gateway",
      header: "Gateway",
      cell: ({ row }) => {
        const gateway = row.getValue("gateway") as PaymentGateway;
        return (
          <Badge variant="outline">
            {paymentUtils.getGatewayDisplayName(gateway)}
          </Badge>
        );
      },
    },
    {
      accessorKey: "status",
      header: "Status",
      cell: ({ row }) => {
        const status = row.getValue("status") as string;
        const statusConfig = {
          pending: { variant: "secondary" as const, icon: Clock, color: "text-yellow-600" },
          completed: { variant: "default" as const, icon: CheckCircle2, color: "text-green-600" },
          failed: { variant: "destructive" as const, icon: AlertCircle, color: "text-red-600" },
          refunded: { variant: "outline" as const, icon: RefreshCw, color: "text-blue-600" }
        };
        const config = statusConfig[status as keyof typeof statusConfig];
        const IconComponent = config.icon;
        
        return (
          <div className="flex items-center space-x-2">
            <IconComponent className={`h-4 w-4 ${config.color}`} />
            <Badge variant={config.variant}>
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </Badge>
          </div>
        );
      },
    },
    {
      accessorKey: "customerEmail",
      header: "Customer",
      cell: ({ row }) => (
        <div className="text-sm">{row.getValue("customerEmail")}</div>
      ),
    },
    {
      accessorKey: "createdAt",
      header: "Created",
      cell: ({ row }) => (
        <div className="text-sm text-muted-foreground">
          {formatDistanceToNow(new Date(row.getValue("createdAt")), { addSuffix: true })}
        </div>
      ),
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const transaction = row.original;
        
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <span className="sr-only">Open menu</span>
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuItem onClick={() => navigator.clipboard.writeText(transaction.id)}>
                Copy transaction ID
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <Eye className="mr-2 h-4 w-4" />
                View details
              </DropdownMenuItem>
              <DropdownMenuItem>
                <ExternalLink className="mr-2 h-4 w-4" />
                View in gateway
              </DropdownMenuItem>
              {transaction.status === 'completed' && (
                <DropdownMenuItem className="text-red-600">
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Issue refund
                </DropdownMenuItem>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ];

  const handleRefreshStats = async () => {
    setIsRefreshingStats(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsRefreshingStats(false);
    toast.success("Payment statistics refreshed");
  };

  const handleCreatePayment = () => {
    // This would integrate with payment gateway APIs
    toast.success("Payment order created successfully");
    setIsCreateDialogOpen(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Payment Processing</h2>
          <p className="text-muted-foreground">
            Multi-gateway payment management with real-time analytics
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefreshStats}
            disabled={isRefreshingStats}
          >
            <RefreshCw className={`mr-2 h-4 w-4 ${isRefreshingStats ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button size="sm">
                <Plus className="mr-2 h-4 w-4" />
                Create Payment
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Create Payment Order</DialogTitle>
                <DialogDescription>
                  Create a new payment order for a customer
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="amount" className="text-right">
                    Amount
                  </Label>
                  <Input id="amount" placeholder="1000.00" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="gateway" className="text-right">
                    Gateway
                  </Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select gateway" />
                    </SelectTrigger>
                    <SelectContent>
                      {Object.entries(paymentGateways).map(([key, gateway]) => (
                        <SelectItem key={key} value={key} disabled={!gateway.enabled}>
                          {paymentUtils.getGatewayDisplayName(key as PaymentGateway)}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="email" className="text-right">
                    Customer Email
                  </Label>
                  <Input id="email" type="email" placeholder="customer@example.com" className="col-span-3" />
                </div>
              </div>
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={handleCreatePayment}>
                  Create Payment
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Payment Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {paymentUtils.formatPrice(mockStats.totalRevenue * 100, 'INR')}
            </div>
            <p className="text-xs text-muted-foreground">
              {paymentUtils.formatPrice(mockStats.monthlyRevenue * 100, 'INR')} this month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Transactions</CardTitle>
            <CreditCard className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.transactionCount.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Avg: {paymentUtils.formatPrice(mockStats.avgTransactionValue * 100, 'INR')}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.successRate}%</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="inline h-3 w-3 text-green-500 mr-1" />
              +2.1% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Gateways</CardTitle>
            <Settings className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4</div>
            <p className="text-xs text-muted-foreground">
              Multi-gateway support active
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="transactions" className="space-y-4">
        <TabsList>
          <TabsTrigger value="transactions">Transactions</TabsTrigger>
          <TabsTrigger value="gateways">Gateway Analytics</TabsTrigger>
          <TabsTrigger value="subscriptions">Subscription Plans</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>

        <TabsContent value="transactions" className="space-y-4">
          {/* Filters */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Filter className="h-4 w-4" />
              <Label>Filter by status:</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Statuses</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="failed">Failed</SelectItem>
                  <SelectItem value="refunded">Refunded</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex-1" />
            <Button variant="outline" size="sm">
              <Download className="mr-2 h-4 w-4" />
              Export
            </Button>
          </div>

          {/* Transactions Table */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Transactions</CardTitle>
              <CardDescription>
                Complete transaction history across all payment gateways
              </CardDescription>
            </CardHeader>
            <CardContent>
              <DataTable columns={columns} data={mockTransactions} />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="gateways" className="space-y-4">
          {/* Gateway Performance */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Object.entries(mockStats.gatewayStats).map(([gateway, stats]) => {
              const gatewayConfig = paymentGateways[gateway as PaymentGateway];
              return (
                <Card key={gateway}>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      {paymentUtils.getGatewayDisplayName(gateway as PaymentGateway)}
                    </CardTitle>
                    <Badge variant={gatewayConfig.enabled ? "default" : "secondary"}>
                      {gatewayConfig.enabled ? "Active" : "Inactive"}
                    </Badge>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {paymentUtils.formatPrice(stats.revenue * 100, 'INR')}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {stats.count} transactions • {stats.successRate}% success
                    </p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        <TabsContent value="subscriptions" className="space-y-4">
          {/* Subscription Plans */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {subscriptionPlans.map((plan) => (
              <Card key={plan.id} className={plan.popular ? "border-primary" : ""}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>{plan.name}</CardTitle>
                    {plan.popular && <Badge>Popular</Badge>}
                  </div>
                  <CardDescription>{plan.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="text-3xl font-bold">
                        {paymentUtils.formatPrice(plan.pricing.INR.monthly, 'INR')}
                      </div>
                      <p className="text-sm text-muted-foreground">per month</p>
                    </div>
                    <ul className="space-y-2 text-sm">
                      {plan.features.slice(0, 3).map((feature, index) => (
                        <li key={index} className="flex items-center">
                          <CheckCircle2 className="mr-2 h-4 w-4 text-green-500" />
                          {feature}
                        </li>
                      ))}
                      {plan.features.length > 3 && (
                        <li className="text-muted-foreground">
                          +{plan.features.length - 3} more features
                        </li>
                      )}
                    </ul>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="reports" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Payment Reports</CardTitle>
              <CardDescription>
                Generate comprehensive payment analytics reports
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p className="text-muted-foreground">
                  Advanced reporting features coming soon. Export transaction data for now.
                </p>
                <Button variant="outline">
                  <Download className="mr-2 h-4 w-4" />
                  Export All Transactions
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}