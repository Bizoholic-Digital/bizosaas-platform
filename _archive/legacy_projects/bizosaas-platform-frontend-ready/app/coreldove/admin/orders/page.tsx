"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Search, Filter, Eye, Package, Truck, AlertTriangle, CheckCircle,
  Clock, DollarSign, User, MapPin, Calendar, ShieldAlert, Brain,
  TrendingUp, Download, RefreshCw, MoreHorizontal, Phone, Mail
} from 'lucide-react';
import Link from 'next/link';

interface OrderItem {
  id: string;
  product_id: string;
  sku: string;
  title: string;
  quantity: number;
  unit_price: number;
  total_price: number;
}

interface FraudAnalysis {
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  risk_score: number;
  verification_required: boolean;
  flags: string[];
  recommendations: string[];
}

interface Order {
  id: string;
  tenant_id: number;
  order_number: string;
  customer_email: string;
  customer_name: string;
  customer_phone?: string;
  shipping_address: {
    street: string;
    city: string;
    state: string;
    postal_code: string;
    country: string;
  };
  billing_address?: {
    street: string;
    city: string;
    state: string;
    postal_code: string;
    country: string;
  };
  items: OrderItem[];
  subtotal: number;
  shipping_cost: number;
  tax_amount: number;
  total_amount: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled' | 'refunded';
  payment_status: 'pending' | 'paid' | 'failed' | 'refunded';
  fraud_analysis: FraudAnalysis;
  created_at: string;
  updated_at: string;
  tracking_number?: string;
  estimated_delivery?: string;
  notes?: string;
}

interface OrderFilters {
  search: string;
  status: string;
  payment_status: string;
  fraud_risk: string;
  date_range: string;
  amount_range: [number, number];
}

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [filteredOrders, setFilteredOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [filters, setFilters] = useState<OrderFilters>({
    search: '',
    status: 'all',
    payment_status: 'all',
    fraud_risk: 'all',
    date_range: 'all',
    amount_range: [0, 1000]
  });

  // Mock data - Replace with actual API call
  useEffect(() => {
    const mockOrders: Order[] = [
      {
        id: '1',
        tenant_id: 1,
        order_number: 'ORD-20250105-0001',
        customer_email: 'sarah.johnson@email.com',
        customer_name: 'Sarah Johnson',
        customer_phone: '+1-555-0123',
        shipping_address: {
          street: '123 Fitness Ave',
          city: 'San Francisco',
          state: 'CA',
          postal_code: '94105',
          country: 'USA'
        },
        items: [
          {
            id: '1',
            product_id: '1',
            sku: 'FIT-001',
            title: 'Smart Fitness Tracker with Heart Rate Monitor',
            quantity: 2,
            unit_price: 84.99,
            total_price: 169.98
          }
        ],
        subtotal: 169.98,
        shipping_cost: 9.99,
        tax_amount: 14.40,
        total_amount: 194.37,
        status: 'processing',
        payment_status: 'paid',
        fraud_analysis: {
          risk_level: 'LOW',
          risk_score: 0.15,
          verification_required: false,
          flags: [],
          recommendations: ['Standard processing approved']
        },
        created_at: '2025-01-05T14:30:00Z',
        updated_at: '2025-01-05T15:45:00Z',
        tracking_number: 'TRK123456789',
        estimated_delivery: '2025-01-08T18:00:00Z'
      },
      {
        id: '2',
        tenant_id: 1,
        order_number: 'ORD-20250105-0002',
        customer_email: 'mike.davidson@email.com',
        customer_name: 'Mike Davidson',
        customer_phone: '+1-555-0456',
        shipping_address: {
          street: '456 Tech Street',
          city: 'Austin',
          state: 'TX',
          postal_code: '73301',
          country: 'USA'
        },
        items: [
          {
            id: '2',
            product_id: '2',
            sku: 'HOME-002',
            title: 'LED Strip Lights Kit with Smart Control',
            quantity: 3,
            unit_price: 44.99,
            total_price: 134.97
          }
        ],
        subtotal: 134.97,
        shipping_cost: 12.99,
        tax_amount: 11.84,
        total_amount: 159.80,
        status: 'shipped',
        payment_status: 'paid',
        fraud_analysis: {
          risk_level: 'MEDIUM',
          risk_score: 0.45,
          verification_required: true,
          flags: ['High quantity order', 'New customer'],
          recommendations: ['Enhanced monitoring recommended', 'Verify shipping address']
        },
        created_at: '2025-01-04T10:15:00Z',
        updated_at: '2025-01-05T09:20:00Z',
        tracking_number: 'TRK987654321',
        estimated_delivery: '2025-01-07T16:00:00Z'
      },
      {
        id: '3',
        tenant_id: 1,
        order_number: 'ORD-20250104-0003',
        customer_email: 'suspicious@temp-mail.org',
        customer_name: 'John Doe',
        shipping_address: {
          street: '789 Random St',
          city: 'Miami',
          state: 'FL',
          postal_code: '33101',
          country: 'USA'
        },
        items: [
          {
            id: '3',
            product_id: '1',
            sku: 'FIT-001',
            title: 'Smart Fitness Tracker with Heart Rate Monitor',
            quantity: 10,
            unit_price: 84.99,
            total_price: 849.90
          }
        ],
        subtotal: 849.90,
        shipping_cost: 0.00,
        tax_amount: 67.99,
        total_amount: 917.89,
        status: 'pending',
        payment_status: 'pending',
        fraud_analysis: {
          risk_level: 'HIGH',
          risk_score: 0.85,
          verification_required: true,
          flags: ['Suspicious email domain', 'Large quantity order', 'Mismatched billing/shipping', 'New customer'],
          recommendations: ['Manual review required', 'Verify customer identity', 'Consider order hold']
        },
        created_at: '2025-01-04T16:22:00Z',
        updated_at: '2025-01-04T16:22:00Z'
      }
    ];

    setTimeout(() => {
      setOrders(mockOrders);
      setFilteredOrders(mockOrders);
      setLoading(false);
    }, 1000);
  }, []);

  // Filter orders
  useEffect(() => {
    let filtered = orders.filter(order => {
      const matchesSearch = order.order_number.toLowerCase().includes(filters.search.toLowerCase()) ||
                           order.customer_name.toLowerCase().includes(filters.search.toLowerCase()) ||
                           order.customer_email.toLowerCase().includes(filters.search.toLowerCase());
      
      const matchesStatus = filters.status === 'all' || order.status === filters.status;
      const matchesPaymentStatus = filters.payment_status === 'all' || order.payment_status === filters.payment_status;
      const matchesFraudRisk = filters.fraud_risk === 'all' || order.fraud_analysis.risk_level === filters.fraud_risk;
      
      const matchesAmount = order.total_amount >= filters.amount_range[0] &&
                           order.total_amount <= filters.amount_range[1];

      return matchesSearch && matchesStatus && matchesPaymentStatus && matchesFraudRisk && matchesAmount;
    });

    setFilteredOrders(filtered);
  }, [orders, filters]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'processing': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'shipped': return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'delivered': return 'bg-green-100 text-green-800 border-green-200';
      case 'cancelled': return 'bg-red-100 text-red-800 border-red-200';
      case 'refunded': return 'bg-gray-100 text-gray-800 border-gray-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending': return <Clock className="w-3 h-3" />;
      case 'processing': return <Package className="w-3 h-3" />;
      case 'shipped': return <Truck className="w-3 h-3" />;
      case 'delivered': return <CheckCircle className="w-3 h-3" />;
      case 'cancelled': return <AlertTriangle className="w-3 h-3" />;
      default: return <Clock className="w-3 h-3" />;
    }
  };

  const getFraudRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'LOW': return 'bg-green-100 text-green-800 border-green-200';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'HIGH': return 'bg-red-100 text-red-800 border-red-200';
      case 'CRITICAL': return 'bg-red-200 text-red-900 border-red-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const OrderCard = ({ order }: { order: Order }) => (
    <Card className="hover:shadow-lg transition-all duration-300 cursor-pointer" onClick={() => setSelectedOrder(order)}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <h3 className="font-semibold text-lg">{order.order_number}</h3>
            <p className="text-sm text-gray-600">{order.customer_name}</p>
            <p className="text-xs text-gray-500">{order.customer_email}</p>
          </div>
          <div className="text-right space-y-2">
            <p className="font-bold text-lg text-orange-600">
              ${order.total_amount.toFixed(2)}
            </p>
            <div className="flex gap-1">
              <Badge className={getStatusColor(order.status)} variant="outline">
                {getStatusIcon(order.status)}
                {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
              </Badge>
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Order Items Summary */}
        <div className="space-y-2">
          <h4 className="font-medium text-sm">Items ({order.items.length})</h4>
          {order.items.slice(0, 2).map((item, index) => (
            <div key={item.id} className="flex justify-between items-center text-sm">
              <span className="truncate flex-1 mr-2">
                {item.quantity}x {item.title}
              </span>
              <span className="font-medium">${item.total_price.toFixed(2)}</span>
            </div>
          ))}
          {order.items.length > 2 && (
            <p className="text-xs text-gray-500">+{order.items.length - 2} more items</p>
          )}
        </div>

        {/* Fraud Analysis */}
        <div className="space-y-2 pt-2 border-t">
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4 text-purple-500" />
            <span className="text-sm font-medium">Fraud Analysis</span>
            <Badge className={getFraudRiskColor(order.fraud_analysis.risk_level)} variant="outline">
              <ShieldAlert className="w-3 h-3 mr-1" />
              {order.fraud_analysis.risk_level} RISK
            </Badge>
          </div>
          
          <div className="text-xs text-gray-600">
            <p>Risk Score: {(order.fraud_analysis.risk_score * 100).toFixed(1)}%</p>
            {order.fraud_analysis.flags.length > 0 && (
              <p className="text-red-600">Flags: {order.fraud_analysis.flags.slice(0, 2).join(', ')}</p>
            )}
          </div>

          {order.fraud_analysis.verification_required && (
            <Alert className="border-yellow-200 bg-yellow-50">
              <AlertTriangle className="w-4 h-4 text-yellow-600" />
              <AlertDescription className="text-yellow-700">
                Manual verification required before processing
              </AlertDescription>
            </Alert>
          )}
        </div>

        {/* Shipping Info */}
        <div className="flex items-center justify-between text-xs text-gray-500 pt-2 border-t">
          <div className="flex items-center gap-1">
            <MapPin className="w-3 h-3" />
            <span>{order.shipping_address.city}, {order.shipping_address.state}</span>
          </div>
          <div className="flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            <span>{new Date(order.created_at).toLocaleDateString()}</span>
          </div>
        </div>

        {/* Tracking Info */}
        {order.tracking_number && (
          <div className="bg-gray-50 rounded p-2">
            <div className="flex justify-between items-center text-xs">
              <span className="text-gray-600">Tracking:</span>
              <span className="font-mono font-medium">{order.tracking_number}</span>
            </div>
            {order.estimated_delivery && (
              <div className="flex justify-between items-center text-xs mt-1">
                <span className="text-gray-600">Est. Delivery:</span>
                <span>{new Date(order.estimated_delivery).toLocaleDateString()}</span>
              </div>
            )}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-2 pt-2">
          <Button size="sm" variant="outline" className="flex-1">
            <Eye className="w-3 h-3 mr-1" />
            View Details
          </Button>
          <Button size="sm" variant="outline">
            <MoreHorizontal className="w-3 h-3" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-orange-100 p-6">
        <div className="container mx-auto space-y-6">
          <div className="space-y-4">
            <Skeleton className="h-8 w-64" />
            <Skeleton className="h-4 w-96" />
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="space-y-4">
                <Skeleton className="h-64 w-full" />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-orange-100">
      <div className="container mx-auto p-6 space-y-8">
        {/* Header */}
        <div className="space-y-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Order Management</h1>
              <p className="text-gray-600 mt-1">
                Monitor and manage orders with AI-powered fraud detection
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Button variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Export Orders
              </Button>
              <Button variant="outline">
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </Button>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Package className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-blue-600">
                      {orders.length}
                    </p>
                    <p className="text-sm text-gray-600">Total Orders</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-yellow-100 rounded-lg">
                    <Clock className="w-5 h-5 text-yellow-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-yellow-600">
                      {orders.filter(o => o.status === 'pending' || o.status === 'processing').length}
                    </p>
                    <p className="text-sm text-gray-600">Processing</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-red-100 rounded-lg">
                    <ShieldAlert className="w-5 h-5 text-red-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-red-600">
                      {orders.filter(o => o.fraud_analysis.risk_level === 'HIGH' || o.fraud_analysis.risk_level === 'CRITICAL').length}
                    </p>
                    <p className="text-sm text-gray-600">High Risk</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <DollarSign className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-green-600">
                      {orders.filter(o => o.payment_status === 'paid').reduce((sum, o) => sum + o.total_amount, 0).toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })}
                    </p>
                    <p className="text-sm text-gray-600">Revenue</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <TrendingUp className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-purple-600">
                      {Math.round((orders.reduce((sum, o) => sum + o.fraud_analysis.risk_score, 0) / orders.length) * 100) || 0}%
                    </p>
                    <p className="text-sm text-gray-600">Avg Risk Score</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Filters */}
        <Card>
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
              <div className="md:col-span-2">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <Input 
                    placeholder="Search orders..." 
                    className="pl-10"
                    value={filters.search}
                    onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
                  />
                </div>
              </div>
              
              <Select value={filters.status} onValueChange={(value) => setFilters(prev => ({ ...prev, status: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="processing">Processing</SelectItem>
                  <SelectItem value="shipped">Shipped</SelectItem>
                  <SelectItem value="delivered">Delivered</SelectItem>
                  <SelectItem value="cancelled">Cancelled</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={filters.payment_status} onValueChange={(value) => setFilters(prev => ({ ...prev, payment_status: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Payment Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Payment Status</SelectItem>
                  <SelectItem value="pending">Payment Pending</SelectItem>
                  <SelectItem value="paid">Paid</SelectItem>
                  <SelectItem value="failed">Failed</SelectItem>
                  <SelectItem value="refunded">Refunded</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={filters.fraud_risk} onValueChange={(value) => setFilters(prev => ({ ...prev, fraud_risk: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Fraud Risk" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Risk Levels</SelectItem>
                  <SelectItem value="LOW">Low Risk</SelectItem>
                  <SelectItem value="MEDIUM">Medium Risk</SelectItem>
                  <SelectItem value="HIGH">High Risk</SelectItem>
                  <SelectItem value="CRITICAL">Critical Risk</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={filters.date_range} onValueChange={(value) => setFilters(prev => ({ ...prev, date_range: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Date Range" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Time</SelectItem>
                  <SelectItem value="today">Today</SelectItem>
                  <SelectItem value="week">This Week</SelectItem>
                  <SelectItem value="month">This Month</SelectItem>
                  <SelectItem value="quarter">This Quarter</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="flex items-center justify-between pt-4 border-t">
              <span className="text-sm text-gray-600">
                {filteredOrders.length} of {orders.length} orders
              </span>
              <div className="flex items-center gap-2">
                {orders.filter(o => o.fraud_analysis.verification_required).length > 0 && (
                  <Badge variant="destructive">
                    {orders.filter(o => o.fraud_analysis.verification_required).length} require verification
                  </Badge>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* High Risk Orders Alert */}
        {orders.filter(o => o.fraud_analysis.risk_level === 'HIGH' || o.fraud_analysis.risk_level === 'CRITICAL').length > 0 && (
          <Alert className="border-red-200 bg-red-50">
            <ShieldAlert className="w-4 h-4 text-red-600" />
            <AlertDescription className="text-red-700">
              <strong>{orders.filter(o => o.fraud_analysis.risk_level === 'HIGH' || o.fraud_analysis.risk_level === 'CRITICAL').length} high-risk orders</strong> require immediate attention. 
              Review fraud analysis and verify customer information before processing.
            </AlertDescription>
          </Alert>
        )}

        {/* Orders Grid */}
        {filteredOrders.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No orders found</h3>
              <p className="text-gray-600 mb-6">
                No orders match your current filters. Try adjusting your search criteria.
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredOrders.map((order) => (
              <OrderCard key={order.id} order={order} />
            ))}
          </div>
        )}

        {/* Load More */}
        {filteredOrders.length > 0 && (
          <div className="text-center">
            <Button variant="outline" size="lg">
              <Clock className="w-4 h-4 mr-2" />
              Load More Orders
            </Button>
          </div>
        )}
      </div>

      {/* Order Detail Modal */}
      {selectedOrder && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <CardHeader className="flex flex-row items-center justify-between pb-4">
              <div>
                <CardTitle className="text-xl">{selectedOrder.order_number}</CardTitle>
                <p className="text-gray-600">{selectedOrder.customer_name}</p>
              </div>
              <Button variant="ghost" size="sm" onClick={() => setSelectedOrder(null)}>
                ×
              </Button>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Customer Info */}
              <div className="space-y-4">
                <h3 className="font-semibold">Customer Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-gray-400" />
                    <span>{selectedOrder.customer_name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Mail className="w-4 h-4 text-gray-400" />
                    <span>{selectedOrder.customer_email}</span>
                  </div>
                  {selectedOrder.customer_phone && (
                    <div className="flex items-center gap-2">
                      <Phone className="w-4 h-4 text-gray-400" />
                      <span>{selectedOrder.customer_phone}</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Shipping Address */}
              <div className="space-y-4">
                <h3 className="font-semibold">Shipping Address</h3>
                <div className="text-sm text-gray-600">
                  <p>{selectedOrder.shipping_address.street}</p>
                  <p>{selectedOrder.shipping_address.city}, {selectedOrder.shipping_address.state} {selectedOrder.shipping_address.postal_code}</p>
                  <p>{selectedOrder.shipping_address.country}</p>
                </div>
              </div>

              {/* Fraud Analysis Details */}
              <div className="space-y-4">
                <h3 className="font-semibold">Fraud Analysis</h3>
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Badge className={getFraudRiskColor(selectedOrder.fraud_analysis.risk_level)} variant="outline">
                      <ShieldAlert className="w-3 h-3 mr-1" />
                      {selectedOrder.fraud_analysis.risk_level} RISK
                    </Badge>
                    <span className="text-sm">Score: {(selectedOrder.fraud_analysis.risk_score * 100).toFixed(1)}%</span>
                  </div>
                  
                  {selectedOrder.fraud_analysis.flags.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-red-600 mb-2">Risk Flags:</p>
                      <ul className="list-disc list-inside text-sm text-red-600 space-y-1">
                        {selectedOrder.fraud_analysis.flags.map((flag, index) => (
                          <li key={index}>{flag}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {selectedOrder.fraud_analysis.recommendations.length > 0 && (
                    <div>
                      <p className="text-sm font-medium mb-2">Recommendations:</p>
                      <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                        {selectedOrder.fraud_analysis.recommendations.map((rec, index) => (
                          <li key={index}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>

              {/* Order Items */}
              <div className="space-y-4">
                <h3 className="font-semibold">Order Items</h3>
                <div className="space-y-3">
                  {selectedOrder.items.map((item) => (
                    <div key={item.id} className="flex justify-between items-start p-3 bg-gray-50 rounded">
                      <div className="space-y-1">
                        <p className="font-medium">{item.title}</p>
                        <p className="text-sm text-gray-600">SKU: {item.sku}</p>
                        <p className="text-sm text-gray-600">Qty: {item.quantity} × ${item.unit_price.toFixed(2)}</p>
                      </div>
                      <p className="font-bold">${item.total_price.toFixed(2)}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Order Summary */}
              <div className="space-y-2 pt-4 border-t">
                <div className="flex justify-between text-sm">
                  <span>Subtotal:</span>
                  <span>${selectedOrder.subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Shipping:</span>
                  <span>${selectedOrder.shipping_cost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Tax:</span>
                  <span>${selectedOrder.tax_amount.toFixed(2)}</span>
                </div>
                <div className="flex justify-between font-bold text-lg pt-2 border-t">
                  <span>Total:</span>
                  <span>${selectedOrder.total_amount.toFixed(2)}</span>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3 pt-4 border-t">
                <Button className="flex-1 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600">
                  Process Order
                </Button>
                <Button variant="outline" className="flex-1">
                  Mark as Verified
                </Button>
                <Button variant="destructive" className="flex-1">
                  Hold for Review
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}