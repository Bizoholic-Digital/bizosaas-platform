'use client';

import React, { useState, useEffect } from 'react';
import { 
  ShoppingCart, Package, Search, Filter, Eye, 
  Download, Calendar, DollarSign, User, MapPin,
  Truck, CheckCircle, Clock, AlertCircle, X,
  Package2, CreditCard, RefreshCw, MoreHorizontal,
  ExternalLink, Printer
} from 'lucide-react';
import DashboardLayout from '../../components/ui/dashboard-layout';
import { useOrdersData } from '../../lib/hooks/useOrdersData';

interface OrderItem {
  id: string;
  productId: string;
  name: string;
  sku: string;
  quantity: number;
  price: number;
  total: number;
}

interface Order {
  id: string;
  orderNumber: string;
  customer: {
    id: string;
    firstName: string;
    lastName: string;
    email: string;
    phone?: string;
  };
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled' | 'refunded';
  paymentStatus: 'pending' | 'paid' | 'failed' | 'refunded';
  items: OrderItem[];
  subtotal: number;
  shipping: number;
  tax: number;
  total: number;
  shippingAddress: {
    street: string;
    city: string;
    state: string;
    zipCode: string;
    country: string;
  };
  createdAt: string;
  updatedAt: string;
  trackingNumber?: string;
}

const OrdersPage = () => {
  const [filterPayment, setFilterPayment] = useState('all');
  const {
    orders,
    pagination,
    filter,
    statistics,
    isLoading: loading,
    error,
    updateFilter,
    goToPage,
    refresh,
    updateOrderStatus
  } = useOrdersData();

  // Mock data - replace with actual API call to /api/brain/saleor/
  const mockOrders: Order[] = [
    {
      id: '1',
      orderNumber: 'ORD-2024-001',
      customer: {
        id: 'cust1',
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@example.com',
        phone: '+1 (555) 123-4567'
      },
      status: 'shipped',
      paymentStatus: 'paid',
      items: [
        {
          id: '1',
          productId: 'prod1',
          name: 'Premium Business Package',
          sku: 'PBP-001',
          quantity: 1,
          price: 299.00,
          total: 299.00
        }
      ],
      subtotal: 299.00,
      shipping: 19.99,
      tax: 23.92,
      total: 342.91,
      shippingAddress: {
        street: '123 Business Ave',
        city: 'New York',
        state: 'NY',
        zipCode: '10001',
        country: 'USA'
      },
      createdAt: '2024-01-15T10:30:00Z',
      updatedAt: '2024-01-16T14:20:00Z',
      trackingNumber: 'TRK123456789'
    },
    {
      id: '2',
      orderNumber: 'ORD-2024-002',
      customer: {
        id: 'cust2',
        firstName: 'Jane',
        lastName: 'Smith',
        email: 'jane.smith@company.com'
      },
      status: 'processing',
      paymentStatus: 'paid',
      items: [
        {
          id: '2',
          productId: 'prod2',
          name: 'Starter Marketing Kit',
          sku: 'SMK-001',
          quantity: 2,
          price: 149.00,
          total: 298.00
        },
        {
          id: '3',
          productId: 'prod3',
          name: 'SEO Audit Service',
          sku: 'SEO-001',
          quantity: 1,
          price: 199.00,
          total: 199.00
        }
      ],
      subtotal: 497.00,
      shipping: 0.00,
      tax: 39.76,
      total: 536.76,
      shippingAddress: {
        street: '456 Corporate Blvd',
        city: 'Los Angeles',
        state: 'CA',
        zipCode: '90210',
        country: 'USA'
      },
      createdAt: '2024-01-14T09:15:00Z',
      updatedAt: '2024-01-15T11:30:00Z'
    },
    {
      id: '3',
      orderNumber: 'ORD-2024-003',
      customer: {
        id: 'cust3',
        firstName: 'Mike',
        lastName: 'Johnson',
        email: 'mike.j@startup.com',
        phone: '+1 (555) 987-6543'
      },
      status: 'pending',
      paymentStatus: 'pending',
      items: [
        {
          id: '4',
          productId: 'prod4',
          name: 'Enterprise Solution',
          sku: 'ENT-001',
          quantity: 1,
          price: 999.00,
          total: 999.00
        }
      ],
      subtotal: 999.00,
      shipping: 0.00,
      tax: 79.92,
      total: 1078.92,
      shippingAddress: {
        street: '789 Innovation Dr',
        city: 'Austin',
        state: 'TX',
        zipCode: '78701',
        country: 'USA'
      },
      createdAt: '2024-01-13T16:45:00Z',
      updatedAt: '2024-01-13T16:45:00Z'
    }
  ];

  useEffect(() => {
    // Simulate API call
    const fetchOrders = async () => {
      try {
        setLoading(true);
        // Replace with actual API call to /api/brain/saleor/orders
        await new Promise(resolve => setTimeout(resolve, 1000));
        setOrders(mockOrders);
      } catch (err) {
        setError('Failed to fetch orders');
        console.error('Error fetching orders:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  const getStatusColor = (status: string) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      processing: 'bg-blue-100 text-blue-800',
      shipped: 'bg-purple-100 text-purple-800',
      delivered: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800',
      refunded: 'bg-gray-100 text-gray-800'
    };
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const getStatusIcon = (status: string) => {
    const icons = {
      pending: <Clock className="w-4 h-4" />,
      processing: <RefreshCw className="w-4 h-4" />,
      shipped: <Truck className="w-4 h-4" />,
      delivered: <CheckCircle className="w-4 h-4" />,
      cancelled: <X className="w-4 h-4" />,
      refunded: <RefreshCw className="w-4 h-4" />
    };
    return icons[status as keyof typeof icons] || <Clock className="w-4 h-4" />;
  };

  const getPaymentStatusColor = (status: string) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      paid: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
      refunded: 'bg-gray-100 text-gray-800'
    };
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const filteredOrders = orders.filter(order => {
    const matchesSearch = order.orderNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         `${order.customer.firstName} ${order.customer.lastName}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         order.customer.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || order.status === filterStatus;
    const matchesPayment = filterPayment === 'all' || order.paymentStatus === filterPayment;
    return matchesSearch && matchesStatus && matchesPayment;
  });

  if (loading) {
    return (
      <DashboardLayout title="Orders Management" description="Track and manage your e-commerce orders">
        <div className="p-6">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-6"></div>
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-32 bg-gray-200 dark:bg-gray-700 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Orders Management" description="Track and manage your e-commerce orders">
      <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Orders</h1>
          <p className="text-gray-600 mt-1">Track and manage your e-commerce orders</p>
        </div>
        <div className="flex gap-3">
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            <Download className="w-4 h-4" />
            Export Orders
          </button>
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            <RefreshCw className="w-4 h-4" />
            Sync Orders
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600">Total Orders</p>
              <p className="text-2xl font-bold">{orders.length}</p>
            </div>
            <ShoppingCart className="w-8 h-8 text-blue-600" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600">Pending</p>
              <p className="text-2xl font-bold text-yellow-600">
                {orders.filter(o => o.status === 'pending').length}
              </p>
            </div>
            <Clock className="w-8 h-8 text-yellow-600" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600">Total Revenue</p>
              <p className="text-2xl font-bold text-green-600">
                ${orders.reduce((sum, o) => sum + o.total, 0).toLocaleString()}
              </p>
            </div>
            <DollarSign className="w-8 h-8 text-green-600" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600">Avg Order Value</p>
              <p className="text-2xl font-bold text-purple-600">
                ${orders.length > 0 ? (orders.reduce((sum, o) => sum + o.total, 0) / orders.length).toFixed(2) : '0.00'}
              </p>
            </div>
            <Package className="w-8 h-8 text-purple-600" />
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search orders..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Status</option>
            <option value="pending">Pending</option>
            <option value="processing">Processing</option>
            <option value="shipped">Shipped</option>
            <option value="delivered">Delivered</option>
            <option value="cancelled">Cancelled</option>
          </select>
          <select
            value={filterPayment}
            onChange={(e) => setFilterPayment(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Payments</option>
            <option value="paid">Paid</option>
            <option value="pending">Payment Pending</option>
            <option value="failed">Payment Failed</option>
            <option value="refunded">Refunded</option>
          </select>
        </div>
      </div>

      {/* Orders List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="space-y-0">
          {filteredOrders.map((order, index) => (
            <div key={order.id} className={`p-6 ${index !== filteredOrders.length - 1 ? 'border-b border-gray-200' : ''} hover:bg-gray-50`}>
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{order.orderNumber}</h3>
                    <p className="text-sm text-gray-500">
                      {new Date(order.createdAt).toLocaleDateString()} at {new Date(order.createdAt).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}>
                    {getStatusIcon(order.status)}
                    {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                  </span>
                  <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getPaymentStatusColor(order.paymentStatus)}`}>
                    <CreditCard className="w-3 h-3" />
                    {order.paymentStatus.charAt(0).toUpperCase() + order.paymentStatus.slice(1)}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Customer Info */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Customer</h4>
                  <div className="text-sm text-gray-600 space-y-1">
                    <div className="flex items-center gap-2">
                      <User className="w-4 h-4" />
                      {order.customer.firstName} {order.customer.lastName}
                    </div>
                    <div className="flex items-center gap-2">
                      <CreditCard className="w-4 h-4" />
                      {order.customer.email}
                    </div>
                    {order.customer.phone && (
                      <div className="flex items-center gap-2">
                        <CreditCard className="w-4 h-4" />
                        {order.customer.phone}
                      </div>
                    )}
                  </div>
                </div>

                {/* Order Items */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Items ({order.items.length})</h4>
                  <div className="space-y-2">
                    {order.items.map((item) => (
                      <div key={item.id} className="flex justify-between text-sm">
                        <div>
                          <span className="text-gray-900">{item.name}</span>
                          <span className="text-gray-500 ml-2">×{item.quantity}</span>
                        </div>
                        <span className="text-gray-900">${item.total.toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Order Total & Actions */}
                <div className="lg:text-right">
                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between lg:justify-end text-sm">
                      <span className="text-gray-600 lg:mr-8">Subtotal:</span>
                      <span className="text-gray-900">${order.subtotal.toFixed(2)}</span>
                    </div>
                    {order.shipping > 0 && (
                      <div className="flex justify-between lg:justify-end text-sm">
                        <span className="text-gray-600 lg:mr-8">Shipping:</span>
                        <span className="text-gray-900">${order.shipping.toFixed(2)}</span>
                      </div>
                    )}
                    <div className="flex justify-between lg:justify-end text-sm">
                      <span className="text-gray-600 lg:mr-8">Tax:</span>
                      <span className="text-gray-900">${order.tax.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between lg:justify-end text-base font-semibold border-t pt-2">
                      <span className="text-gray-900 lg:mr-8">Total:</span>
                      <span className="text-gray-900">${order.total.toFixed(2)}</span>
                    </div>
                  </div>

                  <div className="flex gap-2 justify-end">
                    <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                      <Eye className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                      <Printer className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                      <ExternalLink className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                      <MoreHorizontal className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>

              {order.trackingNumber && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="flex items-center gap-2 text-sm">
                    <Truck className="w-4 h-4 text-blue-600" />
                    <span className="text-gray-600">Tracking:</span>
                    <span className="font-mono text-blue-600">{order.trackingNumber}</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {filteredOrders.length === 0 && (
          <div className="text-center py-12">
            <ShoppingCart className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No orders found</h3>
            <p className="text-gray-500">
              {searchTerm || filterStatus !== 'all' || filterPayment !== 'all' 
                ? 'Try adjusting your search or filter criteria'
                : 'Orders will appear here once customers start purchasing'
              }
            </p>
          </div>
        )}
      </div>

        {error && (
          <div className="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
            <div className="flex items-center">
              <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
              <span className="text-red-700 dark:text-red-300">{error}</span>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default OrdersPage;