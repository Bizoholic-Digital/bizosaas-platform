'use client';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { ShoppingCart, Package, TrendingUp, DollarSign, Loader2 } from 'lucide-react';
import { useAuth } from '@/components/auth/AuthProvider';
import { gql, useQuery } from 'urql';
import React from 'react';

const GET_ECOMMERCE_DATA = gql`
  query GetEcommerceData($tenantId: String!) {
    ecommerceStats(tenantId: $tenantId) {
      totalSales
      totalOrders
      totalProducts
    }
  }
`;

export default function EcommercePage() {
  const { user } = useAuth();

  const [result] = useQuery({
    query: GET_ECOMMERCE_DATA,
    variables: { tenantId: user?.tenant || 'default' },
    pause: !user,
  });

  const { data, fetching, error } = result;

  const stats = data?.ecommerceStats || {
    totalSales: 0,
    totalOrders: 0,
    totalProducts: 0
  };

  return (
    <DashboardLayout
      title="E-commerce"
      description="Manage your online store and products"
    >
      <div className="p-6">
        {fetching && (
          <div className="flex justify-center mb-6">
            <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Sales</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  ${stats.totalSales?.toLocaleString()}
                </p>
              </div>
              <DollarSign className="w-8 h-8 text-green-600" />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Products</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats.totalProducts}
                </p>
              </div>
              <Package className="w-8 h-8 text-blue-600" />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Orders</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats.totalOrders}
                </p>
              </div>
              <ShoppingCart className="w-8 h-8 text-purple-600" />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Conversion</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats.totalOrders > 0 ? '2.4%' : '0%'}
                </p>
              </div>
              <TrendingUp className="w-8 h-8 text-orange-600" />
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="text-center py-12">
            <ShoppingCart className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
              E-commerce Dashboard
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              {stats.totalProducts > 0
                ? "Your store is connected and synced. manage your products and orders below."
                : "Connect your WooCommerce store to view sales and manage products."}
            </p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
