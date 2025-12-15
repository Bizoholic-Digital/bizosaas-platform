'use client';

import React, { useState, useEffect } from 'react';
import {
    Plus, Search, Filter, Edit, Trash2, Package,
    ShoppingCart, Users, BarChart3, Target, MessageSquare, RefreshCw, AlertCircle
} from 'lucide-react';
import { ProductForm } from './ProductForm';
import { OrderForm } from './OrderForm';
import { CustomerForm } from './CustomerForm';
import { ecommerceApi, Product, Order } from '@/lib/api/ecommerce';
import { toast } from 'sonner';

interface EcommerceContentProps {
    activeTab: string;
}

export const EcommerceContent: React.FC<EcommerceContentProps> = ({ activeTab }) => {
    const [products, setProducts] = useState<Product[]>([]);
    const [orders, setOrders] = useState<Order[]>([]);

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Mock other data
    const [customers] = useState([]);
    const [inventory] = useState([]);

    // Modal States
    const [isProductModalOpen, setIsProductModalOpen] = useState(false);
    const [isOrderModalOpen, setIsOrderModalOpen] = useState(false);
    const [selectedItem, setSelectedItem] = useState<any>(null);

    useEffect(() => {
        if (activeTab === 'ecom-products') {
            fetchProducts();
        } else if (activeTab === 'ecom-orders') {
            fetchOrders();
        }
    }, [activeTab]);

    const fetchProducts = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const res = await ecommerceApi.getProducts();
            if (res.error) {
                setError(res.error);
                if (res.status === 404) toast.error("E-commerce connector not configured.");
            } else {
                setProducts(res.data || []);
            }
        } catch (err) {
            console.error("Failed to fetch products", err);
            setError("Failed to load products.");
        } finally {
            setIsLoading(false);
        }
    };

    const fetchOrders = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const res = await ecommerceApi.getOrders();
            if (res.error) {
                setError(res.error);
                if (res.status === 404) toast.error("E-commerce connector not configured.");
            } else {
                setOrders(res.data || []);
            }
        } catch (err) {
            console.error("Failed to fetch orders", err);
            setError("Failed to load orders.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreate = async () => {
        // Assume modal submission does API call
        if (activeTab === 'ecom-products') fetchProducts();
        if (activeTab === 'ecom-orders') fetchOrders();
    };


    const renderProducts = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Products</h2>
                <button
                    onClick={() => { setSelectedItem(null); setIsProductModalOpen(true); }}
                    className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-primary/90"
                >
                    <Plus className="w-4 h-4" /> Add Product
                </button>
                <ProductForm
                    isOpen={isProductModalOpen}
                    onClose={() => setIsProductModalOpen(false)}
                    onSubmit={handleCreate}
                    initialData={selectedItem}
                />
            </div>
            {error && (
                <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-lg flex items-center gap-2">
                    <AlertCircle className="h-5 w-5" />
                    {error}
                </div>
            )}
            <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden shadow-sm">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50 dark:bg-gray-800/50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Product</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">SKU</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Price</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Stock</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                            {isLoading ? (
                                <tr><td colSpan={6} className="px-6 py-12 text-center text-gray-500"><RefreshCw className="animate-spin h-6 w-6 mx-auto" /></td></tr>
                            ) : products.length === 0 && !error ? (
                                <tr><td colSpan={6} className="px-6 py-12 text-center text-gray-500">No products found.</td></tr>
                            ) : (
                                products.map((product) => (
                                    <tr key={product.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{product.name}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{product.sku || 'N/A'}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">${product.price || '0.00'}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{product.stock_quantity || 0}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${product.status === 'publish' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-gray-100 text-gray-800 dark:bg-gray-800'}`}>
                                                {product.status || 'Active'}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            <div className="flex gap-2">
                                                <button className="text-gray-400 hover:text-blue-600"><Edit className="w-4 h-4" /></button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
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
                <button
                    onClick={() => { setSelectedItem(null); setIsOrderModalOpen(true); }}
                    className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-primary/90"
                >
                    <Plus className="w-4 h-4" /> Add Order
                </button>
                <OrderForm
                    isOpen={isOrderModalOpen}
                    onClose={() => setIsOrderModalOpen(false)}
                    onSubmit={handleCreate}
                    initialData={selectedItem}
                />
            </div>
            {error && (
                <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-lg flex items-center gap-2">
                    <AlertCircle className="h-5 w-5" />
                    {error}
                </div>
            )}
            <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden shadow-sm">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50 dark:bg-gray-800/50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Order ID</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Customer</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Total</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Date</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                            {isLoading ? (
                                <tr><td colSpan={5} className="px-6 py-12 text-center text-gray-500"><RefreshCw className="animate-spin h-6 w-6 mx-auto" /></td></tr>
                            ) : orders.length === 0 && !error ? (
                                <tr><td colSpan={5} className="px-6 py-12 text-center text-gray-500">No orders found.</td></tr>
                            ) : (
                                orders.map((order) => (
                                    <tr key={order.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">#{order.number || order.id}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{order.customer_id || 'Guest'}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{order.total} {order.currency}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${order.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                                                {order.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{new Date(order.created_at).toLocaleDateString()}</td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );

    // Simplistic placeholder renderer for now
    const renderPlaceholder = (title: string) => (
        <div className="flex flex-col items-center justify-center p-12 text-center border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-lg">
            <Package className="h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">{title}</h3>
            <p className="text-gray-500 dark:text-gray-400">Feature not yet connected to active E-commerce provider.</p>
        </div>
    );

    if (activeTab === 'ecom-products') return renderProducts();
    if (activeTab === 'ecom-orders') return renderOrders();
    // Default or other tabs
    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">E-commerce Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200">
                    <h3 className="text-lg font-medium mb-2">Products</h3>
                    <p className="text-3xl font-bold">{products.length || 0}</p>
                    <button onClick={fetchProducts} className="text-primary text-sm mt-2">Refresh</button>
                </div>
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200">
                    <h3 className="text-lg font-medium mb-2">Orders</h3>
                    <p className="text-3xl font-bold">{orders.length || 0}</p>
                    <button onClick={fetchOrders} className="text-primary text-sm mt-2">Refresh</button>
                </div>
            </div>
            {activeTab !== 'ecom-overview' && renderPlaceholder(activeTab.replace('ecom-', ''))}
        </div>
    );
};
