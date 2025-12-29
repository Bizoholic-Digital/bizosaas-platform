'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { ShoppingCart, Package, Users as UsersIcon, Loader2, Plus } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';

interface Product {
    id: string;
    name: string;
    price: number;
    stock_quantity: number;
    status: string;
}

interface Order {
    id: string;
    total_amount: number;
    status: string;
    email?: string;
    created_at?: string;
}

export default function EcommercePage() {
    const { isConnected, isLoading: statusLoading, connector } = useConnectorStatus('woocommerce');
    const [products, setProducts] = useState<Product[]>([]);
    const [orders, setOrders] = useState<Order[]>([]);
    const [isLoadingData, setIsLoadingData] = useState(false);

    useEffect(() => {
        if (isConnected) {
            loadData();
        }
    }, [isConnected]);

    const loadData = async () => {
        setIsLoadingData(true);
        try {
            const [productsData, ordersData] = await Promise.all([
                brainApi.ecommerce.getProducts().catch(() => ({ data: [] })),
                brainApi.ecommerce.getOrders().catch(() => ({ data: [] }))
            ]);

            setProducts(productsData.data || []);
            setOrders(ordersData.data || []);
        } catch (error) {
            console.error('Failed to load e-commerce data:', error);
        } finally {
            setIsLoadingData(false);
        }
    };

    if (statusLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    if (!isConnected) {
        return (
            <ConnectionPrompt
                serviceName="WooCommerce"
                serviceIcon={<ShoppingCart className="w-8 h-8 text-purple-600" />}
                description="Connect your WooCommerce store to manage products and orders."
            />
        );
    }

    const totalRevenue = orders.reduce((sum, order) => sum + order.total_amount, 0);

    return (
        <div className="p-6 space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white">E-commerce</h1>
                    <p className="text-muted-foreground mt-1">Manage your online store</p>
                </div>
                <Badge variant="outline" className="bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 border-green-200 dark:border-green-800">
                    <div className="w-2 h-2 rounded-full bg-green-500 mr-2" />
                    Connected to {connector?.name}
                </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Total Products</CardTitle>
                        <Package className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{products.length}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Total Orders</CardTitle>
                        <ShoppingCart className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{orders.length}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Revenue</CardTitle>
                        <UsersIcon className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">${totalRevenue.toLocaleString()}</div>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle>Store Data</CardTitle>
                        <Button>
                            <Plus className="w-4 h-4 mr-2" />
                            Add Product
                        </Button>
                    </div>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="products" className="w-full">
                        <TabsList className="grid w-full grid-cols-2 mb-4">
                            <TabsTrigger value="products">
                                <Package className="w-4 h-4 mr-2" />
                                Products ({products.length})
                            </TabsTrigger>
                            <TabsTrigger value="orders">
                                <ShoppingCart className="w-4 h-4 mr-2" />
                                Orders ({orders.length})
                            </TabsTrigger>
                        </TabsList>

                        <TabsContent value="products" className="space-y-2">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : products.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">No products found</div>
                            ) : (
                                products.map((product) => (
                                    <div key={product.id} className="flex items-center justify-between p-4 rounded-lg border hover:bg-slate-50 dark:hover:bg-slate-800">
                                        <div className="flex items-center gap-4">
                                            <Package className="w-5 h-5 text-purple-600" />
                                            <div>
                                                <p className="font-medium text-slate-900 dark:text-white">{product.name}</p>
                                                <p className="text-sm text-muted-foreground">Stock: {product.stock_quantity}</p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <p className="font-semibold text-slate-900 dark:text-white">${product.price}</p>
                                            <Badge variant={product.status === 'publish' ? 'default' : 'secondary'}>
                                                {product.status}
                                            </Badge>
                                        </div>
                                    </div>
                                ))
                            )}
                        </TabsContent>

                        <TabsContent value="orders" className="space-y-2">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : orders.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">No orders found</div>
                            ) : (
                                orders.map((order) => (
                                    <div key={order.id} className="flex items-center justify-between p-4 rounded-lg border hover:bg-slate-50 dark:hover:bg-slate-800">
                                        <div className="flex items-center gap-4">
                                            <ShoppingCart className="w-5 h-5 text-green-600" />
                                            <div>
                                                <p className="font-medium text-slate-900 dark:text-white">Order #{order.id}</p>
                                                <p className="text-sm text-muted-foreground">{order.email || 'No email'}</p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <p className="font-semibold text-slate-900 dark:text-white">${order.total_amount}</p>
                                            <Badge>{order.status}</Badge>
                                        </div>
                                    </div>
                                ))
                            )}
                        </TabsContent>
                    </Tabs>
                </CardContent>
            </Card>
        </div>
    );
}
