'use client';

import React, { useState, useEffect } from 'react';
import {
  ShoppingCart, Package, Users, BarChart3, Target, MessageSquare,
  Plus, Search, Edit3, Trash2, Eye, Calendar, User, ExternalLink,
  Filter, Download, Upload, Settings, DollarSign, TrendingUp,
  Star, AlertCircle, CheckCircle, Clock, Zap
} from 'lucide-react';

interface EcommerceContentProps {
  activeTab: string;
}

interface Product {
  id: string;
  name: string;
  sku: string;
  price: number;
  sale_price?: number;
  stock_quantity: number;
  status: 'active' | 'inactive' | 'out_of_stock';
  category: string;
  featured_image?: string;
  created_at: string;
  sales_count: number;
}

interface Order {
  id: string;
  order_number: string;
  customer_name: string;
  customer_email: string;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  total_amount: number;
  items_count: number;
  created_at: string;
  shipping_address: string;
}

interface Customer {
  id: string;
  name: string;
  email: string;
  phone?: string;
  total_orders: number;
  total_spent: number;
  status: 'active' | 'inactive';
  last_order_date?: string;
  created_at: string;
  location: string;
}

interface InventoryItem {
  id: string;
  product_name: string;
  sku: string;
  current_stock: number;
  reserved_stock: number;
  available_stock: number;
  reorder_level: number;
  status: 'in_stock' | 'low_stock' | 'out_of_stock';
  last_restocked: string;
  location: string;
}

interface Coupon {
  id: string;
  code: string;
  description: string;
  type: 'percentage' | 'fixed_amount' | 'free_shipping';
  value: number;
  usage_count: number;
  usage_limit?: number;
  status: 'active' | 'inactive' | 'expired';
  valid_from: string;
  valid_until: string;
}

interface Review {
  id: string;
  product_name: string;
  customer_name: string;
  rating: number;
  title: string;
  comment: string;
  status: 'approved' | 'pending' | 'rejected';
  created_at: string;
  verified_purchase: boolean;
  helpful_votes: number;
}

export function EcommerceContent({ activeTab }: EcommerceContentProps) {
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState<Product[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [coupons, setCoupons] = useState<Coupon[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadEcommerceData();
  }, [activeTab]);

  const loadEcommerceData = async () => {
    setLoading(true);
    try {
      const endpoint = getEcommerceEndpoint(activeTab);
      const response = await fetch(endpoint);

      if (!response.ok) {
        console.error('Failed to load e-commerce data:', response.status);
        // Load fallback data
        loadFallbackData();
      } else {
        const data = await response.json();
        updateStateBasedOnTab(data);
      }
    } catch (error) {
      console.error('Error loading e-commerce data:', error);
      loadFallbackData();
    } finally {
      setLoading(false);
    }
  };

  const getEcommerceEndpoint = (tab: string) => {
    const baseUrl = '/api/brain/saleor';
    switch (tab) {
      case 'ecom-products': return `${baseUrl}/products`;
      case 'ecom-orders': return `${baseUrl}/orders`;
      case 'ecom-customers': return `${baseUrl}/customers`;
      case 'ecom-inventory': return `${baseUrl}/inventory`;
      case 'ecom-coupons': return `${baseUrl}/coupons`;
      case 'ecom-reviews': return `${baseUrl}/reviews`;
      default: return `${baseUrl}/products`;
    }
  };

  const updateStateBasedOnTab = (data: any) => {
    switch (activeTab) {
      case 'ecom-products': setProducts(data.products || []); break;
      case 'ecom-orders': setOrders(data.orders || []); break;
      case 'ecom-customers': setCustomers(data.customers || []); break;
      case 'ecom-inventory': setInventory(data.inventory || []); break;
      case 'ecom-coupons': setCoupons(data.coupons || []); break;
      case 'ecom-reviews': setReviews(data.reviews || []); break;
    }
  };

  const loadFallbackData = () => {
    switch (activeTab) {
      case 'ecom-products':
        setProducts([
          {
            id: '1',
            name: 'AI Marketing Course',
            sku: 'AMC-001',
            price: 299.99,
            sale_price: 199.99,
            stock_quantity: 100,
            status: 'active',
            category: 'Digital Products',
            featured_image: '/products/ai-marketing-course.jpg',
            created_at: '2024-01-15T10:00:00Z',
            sales_count: 245
          },
          {
            id: '2',
            name: 'Marketing Automation Templates',
            sku: 'MAT-002',
            price: 49.99,
            stock_quantity: 500,
            status: 'active',
            category: 'Templates',
            featured_image: '/products/automation-templates.jpg',
            created_at: '2024-01-18T14:30:00Z',
            sales_count: 432
          },
          {
            id: '3',
            name: 'Social Media Strategy Bundle',
            sku: 'SMS-003',
            price: 149.99,
            stock_quantity: 0,
            status: 'out_of_stock',
            category: 'Digital Products',
            featured_image: '/products/social-strategy.jpg',
            created_at: '2024-01-20T09:15:00Z',
            sales_count: 187
          }
        ]);
        break;

      case 'ecom-orders':
        setOrders([
          {
            id: '1',
            order_number: 'ORD-2024-001',
            customer_name: 'John Smith',
            customer_email: 'john.smith@email.com',
            status: 'delivered',
            total_amount: 199.99,
            items_count: 1,
            created_at: '2024-01-25T10:30:00Z',
            shipping_address: '123 Main St, City, State 12345'
          },
          {
            id: '2',
            order_number: 'ORD-2024-002',
            customer_name: 'Sarah Johnson',
            customer_email: 'sarah.j@email.com',
            status: 'processing',
            total_amount: 349.98,
            items_count: 3,
            created_at: '2024-01-26T14:15:00Z',
            shipping_address: '456 Oak Ave, Town, State 67890'
          },
          {
            id: '3',
            order_number: 'ORD-2024-003',
            customer_name: 'Mike Wilson',
            customer_email: 'mike.wilson@email.com',
            status: 'pending',
            total_amount: 49.99,
            items_count: 1,
            created_at: '2024-01-27T09:45:00Z',
            shipping_address: '789 Pine St, Village, State 11111'
          }
        ]);
        break;

      case 'ecom-customers':
        setCustomers([
          {
            id: '1',
            name: 'John Smith',
            email: 'john.smith@email.com',
            phone: '+1-555-0123',
            total_orders: 3,
            total_spent: 599.97,
            status: 'active',
            last_order_date: '2024-01-25T10:30:00Z',
            created_at: '2024-01-10T09:00:00Z',
            location: 'New York, NY'
          },
          {
            id: '2',
            name: 'Sarah Johnson',
            email: 'sarah.j@email.com',
            phone: '+1-555-0456',
            total_orders: 5,
            total_spent: 1299.95,
            status: 'active',
            last_order_date: '2024-01-26T14:15:00Z',
            created_at: '2024-01-05T15:30:00Z',
            location: 'Los Angeles, CA'
          },
          {
            id: '3',
            name: 'Mike Wilson',
            email: 'mike.wilson@email.com',
            total_orders: 1,
            total_spent: 49.99,
            status: 'active',
            last_order_date: '2024-01-27T09:45:00Z',
            created_at: '2024-01-20T11:20:00Z',
            location: 'Chicago, IL'
          }
        ]);
        break;

      case 'ecom-inventory':
        setInventory([
          {
            id: '1',
            product_name: 'AI Marketing Course',
            sku: 'AMC-001',
            current_stock: 100,
            reserved_stock: 5,
            available_stock: 95,
            reorder_level: 20,
            status: 'in_stock',
            last_restocked: '2024-01-15T10:00:00Z',
            location: 'Digital Warehouse'
          },
          {
            id: '2',
            product_name: 'Marketing Automation Templates',
            sku: 'MAT-002',
            current_stock: 15,
            reserved_stock: 3,
            available_stock: 12,
            reorder_level: 20,
            status: 'low_stock',
            last_restocked: '2024-01-18T14:30:00Z',
            location: 'Digital Warehouse'
          },
          {
            id: '3',
            product_name: 'Social Media Strategy Bundle',
            sku: 'SMS-003',
            current_stock: 0,
            reserved_stock: 0,
            available_stock: 0,
            reorder_level: 10,
            status: 'out_of_stock',
            last_restocked: '2024-01-01T00:00:00Z',
            location: 'Digital Warehouse'
          }
        ]);
        break;

      case 'ecom-coupons':
        setCoupons([
          {
            id: '1',
            code: 'SAVE20',
            description: '20% off all courses',
            type: 'percentage',
            value: 20,
            usage_count: 45,
            usage_limit: 100,
            status: 'active',
            valid_from: '2024-01-01T00:00:00Z',
            valid_until: '2024-12-31T23:59:59Z'
          },
          {
            id: '2',
            code: 'FREESHIP',
            description: 'Free shipping on orders over $100',
            type: 'free_shipping',
            value: 0,
            usage_count: 23,
            status: 'active',
            valid_from: '2024-01-15T00:00:00Z',
            valid_until: '2024-06-30T23:59:59Z'
          },
          {
            id: '3',
            code: 'WELCOME10',
            description: '$10 off first purchase',
            type: 'fixed_amount',
            value: 10,
            usage_count: 156,
            usage_limit: 500,
            status: 'active',
            valid_from: '2024-01-01T00:00:00Z',
            valid_until: '2024-12-31T23:59:59Z'
          }
        ]);
        break;

      case 'ecom-reviews':
        setReviews([
          {
            id: '1',
            product_name: 'AI Marketing Course',
            customer_name: 'John Smith',
            rating: 5,
            title: 'Excellent course!',
            comment: 'This course completely transformed my understanding of AI marketing. Highly recommended!',
            status: 'approved',
            created_at: '2024-01-25T15:30:00Z',
            verified_purchase: true,
            helpful_votes: 12
          },
          {
            id: '2',
            product_name: 'Marketing Automation Templates',
            customer_name: 'Sarah Johnson',
            rating: 4,
            title: 'Great templates',
            comment: 'Good collection of templates, saved me a lot of time. Could use a few more variations.',
            status: 'approved',
            created_at: '2024-01-26T10:15:00Z',
            verified_purchase: true,
            helpful_votes: 8
          },
          {
            id: '3',
            product_name: 'AI Marketing Course',
            customer_name: 'Mike Wilson',
            rating: 5,
            title: 'Best investment I made',
            comment: 'The strategies taught in this course helped me increase my ROI by 300%.',
            status: 'pending',
            created_at: '2024-01-27T09:45:00Z',
            verified_purchase: true,
            helpful_votes: 0
          }
        ]);
        break;
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getStatusBadge = (status: string, type: string = 'default') => {
    const colorSchemes = {
      product: {
        active: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400',
        out_of_stock: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
      },
      order: {
        pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        processing: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
        shipped: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400',
        delivered: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        cancelled: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
      },
      inventory: {
        in_stock: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        low_stock: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        out_of_stock: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
      },
      review: {
        approved: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        rejected: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
      },
      default: {
        active: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
      }
    };

    const colors = colorSchemes[type as keyof typeof colorSchemes] || colorSchemes.default;
    const colorClass = colors[status as keyof typeof colors] || colors.active;

    return (
      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${colorClass}`}>
        {status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')}
      </span>
    );
  };

  const renderStarRating = (rating: number) => {
    return (
      <div className="flex items-center">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`w-4 h-4 ${
              star <= rating
                ? 'text-yellow-400 fill-current'
                : 'text-gray-300 dark:text-gray-600'
            }`}
          />
        ))}
        <span className="ml-1 text-sm text-gray-600 dark:text-gray-400">({rating})</span>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
        <span className="ml-3 text-gray-600 dark:text-gray-400">Loading e-commerce data...</span>
      </div>
    );
  }

  const renderContent = () => {
    switch (activeTab) {
      case 'ecom-products':
        return renderProducts();
      case 'ecom-orders':
        return renderOrders();
      case 'ecom-customers':
        return renderCustomers();
      case 'ecom-inventory':
        return renderInventory();
      case 'ecom-coupons':
        return renderCoupons();
      case 'ecom-reviews':
        return renderReviews();
      default:
        return renderProducts();
    }
  };

  const renderProducts = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Products</h2>
        <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
          <Plus className="w-4 h-4" />
          Add Product
        </button>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>
            <button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 flex items-center gap-2">
              <Filter className="w-4 h-4" />
              Filter
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Product
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Price
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Stock
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Sales
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {products.map((product) => (
                <tr key={product.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <div className="h-10 w-10 bg-gray-200 dark:bg-gray-700 rounded-lg mr-3"></div>
                      <div>
                        <div className="text-sm font-medium text-gray-900 dark:text-white">
                          {product.name}
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          SKU: {product.sku}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900 dark:text-white">
                      {product.sale_price ? (
                        <>
                          <span className="line-through text-gray-500">
                            {formatCurrency(product.price)}
                          </span>
                          <span className="ml-2 text-red-600 font-medium">
                            {formatCurrency(product.sale_price)}
                          </span>
                        </>
                      ) : (
                        formatCurrency(product.price)
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                    {product.stock_quantity}
                  </td>
                  <td className="px-6 py-4">
                    {getStatusBadge(product.status, 'product')}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                    {product.sales_count.toLocaleString()}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <button className="p-1 text-gray-400 hover:text-blue-600">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="p-1 text-gray-400 hover:text-green-600">
                        <Edit3 className="w-4 h-4" />
                      </button>
                      <button className="p-1 text-gray-400 hover:text-red-600">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderOrders = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Orders</h2>
        <div className="flex items-center gap-3">
          <button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 flex items-center gap-2">
            <Download className="w-4 h-4" />
            Export
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white dark:bg-gray-900 p-4 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
              <ShoppingCart className="w-4 h-4 text-blue-600 dark:text-blue-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Orders</p>
              <p className="text-lg font-bold text-gray-900 dark:text-white">1,234</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-900 p-4 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
              <DollarSign className="w-4 h-4 text-green-600 dark:text-green-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Revenue</p>
              <p className="text-lg font-bold text-gray-900 dark:text-white">$45,231</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-900 p-4 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-purple-600 dark:text-purple-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Avg. Order</p>
              <p className="text-lg font-bold text-gray-900 dark:text-white">$156</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-900 p-4 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
              <Clock className="w-4 h-4 text-orange-600 dark:text-orange-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Pending</p>
              <p className="text-lg font-bold text-gray-900 dark:text-white">23</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Order
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Customer
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Total
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {orders.map((order) => (
                <tr key={order.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                  <td className="px-6 py-4">
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        {order.order_number}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {order.items_count} items
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        {order.customer_name}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {order.customer_email}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    {getStatusBadge(order.status, 'order')}
                  </td>
                  <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">
                    {formatCurrency(order.total_amount)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {formatDate(order.created_at)}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <button className="p-1 text-gray-400 hover:text-blue-600">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="p-1 text-gray-400 hover:text-green-600">
                        <Edit3 className="w-4 h-4" />
                      </button>
                      <button className="p-1 text-gray-400 hover:text-purple-600">
                        <ExternalLink className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderCustomers = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Customers</h2>
        <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
          <Plus className="w-4 h-4" />
          Add Customer
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {customers.map((customer) => (
          <div key={customer.id} className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center">
                  <User className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {customer.name}
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {customer.location}
                  </p>
                </div>
              </div>
              {getStatusBadge(customer.status)}
            </div>

            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Email:</span>
                <span className="text-gray-900 dark:text-white">{customer.email}</span>
              </div>
              {customer.phone && (
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Phone:</span>
                  <span className="text-gray-900 dark:text-white">{customer.phone}</span>
                </div>
              )}
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Total Orders:</span>
                <span className="text-gray-900 dark:text-white font-medium">
                  {customer.total_orders}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Total Spent:</span>
                <span className="text-gray-900 dark:text-white font-medium">
                  {formatCurrency(customer.total_spent)}
                </span>
              </div>
              {customer.last_order_date && (
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Last Order:</span>
                  <span className="text-gray-900 dark:text-white">
                    {formatDate(customer.last_order_date)}
                  </span>
                </div>
              )}
            </div>

            <div className="flex items-center gap-2 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <button className="flex-1 py-2 px-3 text-sm bg-purple-600 text-white rounded hover:bg-purple-700">
                View Details
              </button>
              <button className="p-2 text-gray-400 hover:text-blue-600">
                <Mail className="w-4 h-4" />
              </button>
              <button className="p-2 text-gray-400 hover:text-green-600">
                <Edit3 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderInventory = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Inventory</h2>
        <div className="flex items-center gap-3">
          <button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 flex items-center gap-2">
            <Upload className="w-4 h-4" />
            Bulk Update
          </button>
          <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
            <Plus className="w-4 h-4" />
            Add Stock
          </button>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Product
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Current Stock
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Available
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Last Restocked
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {inventory.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                  <td className="px-6 py-4">
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        {item.product_name}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        SKU: {item.sku}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900 dark:text-white">
                      {item.current_stock}
                      {item.current_stock <= item.reorder_level && (
                        <AlertCircle className="w-4 h-4 text-orange-500 ml-1 inline" />
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                    {item.available_stock}
                    <span className="text-gray-500 dark:text-gray-400">
                      ({item.reserved_stock} reserved)
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {getStatusBadge(item.status, 'inventory')}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {formatDate(item.last_restocked)}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <button className="p-1 text-gray-400 hover:text-blue-600">
                        <Plus className="w-4 h-4" />
                      </button>
                      <button className="p-1 text-gray-400 hover:text-green-600">
                        <Edit3 className="w-4 h-4" />
                      </button>
                      <button className="p-1 text-gray-400 hover:text-orange-600">
                        <AlertCircle className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderCoupons = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Coupons</h2>
        <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
          <Plus className="w-4 h-4" />
          Create Coupon
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {coupons.map((coupon) => (
          <div key={coupon.id} className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center">
                  <Target className="w-5 h-5 text-green-600 dark:text-green-400" />
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white font-mono">
                    {coupon.code}
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {coupon.type.replace('_', ' ')}
                  </p>
                </div>
              </div>
              {getStatusBadge(coupon.status)}
            </div>

            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              {coupon.description}
            </p>

            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Value:</span>
                <span className="text-gray-900 dark:text-white font-medium">
                  {coupon.type === 'percentage'
                    ? `${coupon.value}%`
                    : coupon.type === 'fixed_amount'
                    ? formatCurrency(coupon.value)
                    : 'Free Shipping'
                  }
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Usage:</span>
                <span className="text-gray-900 dark:text-white">
                  {coupon.usage_count}
                  {coupon.usage_limit && ` / ${coupon.usage_limit}`}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Valid Until:</span>
                <span className="text-gray-900 dark:text-white">
                  {formatDate(coupon.valid_until)}
                </span>
              </div>
            </div>

            <div className="flex items-center gap-2 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <button className="flex-1 py-2 px-3 text-sm bg-purple-600 text-white rounded hover:bg-purple-700">
                Edit Coupon
              </button>
              <button className="p-2 text-gray-400 hover:text-blue-600">
                <ExternalLink className="w-4 h-4" />
              </button>
              <button className="p-2 text-gray-400 hover:text-red-600">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderReviews = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Reviews</h2>
        <div className="flex items-center gap-3">
          <button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 flex items-center gap-2">
            <Filter className="w-4 h-4" />
            Filter
          </button>
          <button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 flex items-center gap-2">
            <Download className="w-4 h-4" />
            Export
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {reviews.map((review) => (
          <div key={review.id} className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-start">
                <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                  <User className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="ml-3">
                  <div className="flex items-center gap-2">
                    <h4 className="text-sm font-medium text-gray-900 dark:text-white">
                      {review.customer_name}
                    </h4>
                    {review.verified_purchase && (
                      <span className="inline-flex px-2 py-1 text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 rounded-full">
                        <CheckCircle className="w-3 h-3 mr-1" />
                        Verified
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {review.product_name}
                  </p>
                  {renderStarRating(review.rating)}
                </div>
              </div>
              <div className="flex items-center gap-2">
                {getStatusBadge(review.status, 'review')}
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {formatDate(review.created_at)}
                </span>
              </div>
            </div>

            <div className="mb-4">
              <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
                {review.title}
              </h5>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {review.comment}
              </p>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {review.helpful_votes} found helpful
                </span>
              </div>
              <div className="flex items-center gap-2">
                {review.status === 'pending' && (
                  <>
                    <button className="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700">
                      Approve
                    </button>
                    <button className="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700">
                      Reject
                    </button>
                  </>
                )}
                <button className="p-1 text-gray-400 hover:text-blue-600">
                  <ExternalLink className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {renderContent()}
    </div>
  );
}