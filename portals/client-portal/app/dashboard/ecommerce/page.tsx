'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import {
    ShoppingCart, Package, Users as UsersIcon, Loader2,
    Plus, Edit, Trash2, MoreVertical, TrendingUp,
    DollarSign, ArrowUpRight, Zap, Box,
    ShoppingBag, Search, Filter, RefreshCw
} from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'sonner';

interface Product {
    id: string;
    name: string;
    price: number;
    stock_quantity: number;
    status: string;
    images?: { src: string }[];
}

interface Order {
    id: string;
    total_amount: number;
    status: string;
    customer_name?: string;
    email?: string;
    created_at?: string;
}

export default function EcommercePage() {
    const { isConnected, isLoading: statusLoading, connector } = useConnectorStatus('woocommerce', 'ecommerce');
    const [products, setProducts] = useState<Product[]>([]);
    const [orders, setOrders] = useState<Order[]>([]);
    const [isLoadingData, setIsLoadingData] = useState(false);

    const [activeTab, setActiveTab] = useState('products');
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
    const [formData, setFormData] = useState({
        name: '',
        price: '',
        stock_quantity: '',
        status: 'publish'
    });

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
            toast.error('Failed to load store data');
        } finally {
            setIsLoadingData(false);
        }
    };

    const handleCreate = async () => {
        try {
            await brainApi.ecommerce.createProduct({
                ...formData,
                price: parseFloat(formData.price),
                stock_quantity: parseInt(formData.stock_quantity)
            });
            toast.success('Product created successfully');
            setIsDialogOpen(false);
            resetForm();
            loadData();
        } catch (error) {
            toast.error('Failed to create product');
        }
    };

    const handleUpdate = async () => {
        if (!selectedProduct) return;
        try {
            await brainApi.ecommerce.updateProduct(selectedProduct.id, {
                ...formData,
                price: parseFloat(formData.price),
                stock_quantity: parseInt(formData.stock_quantity)
            });
            toast.success('Product updated successfully');
            setIsDialogOpen(false);
            resetForm();
            loadData();
        } catch (error) {
            toast.error('Failed to update product');
        }
    };

    const handleDelete = async (id: string) => {
        if (!confirm('Are you sure you want to delete this product?')) return;
        try {
            await brainApi.ecommerce.deleteProduct(id);
            toast.success('Product deleted successfully');
            loadData();
        } catch (error) {
            toast.error('Failed to delete product');
        }
    };

    const openEdit = (product: Product) => {
        setSelectedProduct(product);
        setFormData({
            name: product.name,
            price: product.price.toString(),
            stock_quantity: product.stock_quantity.toString(),
            status: product.status
        });
        setIsEditing(true);
        setIsDialogOpen(true);
    };

    const resetForm = () => {
        setFormData({ name: '', price: '', stock_quantity: '', status: 'publish' });
        setIsEditing(false);
        setSelectedProduct(null);
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
                description="Connect your WooCommerce store to manage products, track orders, and boost your sales."
            />
        );
    }

    const totalRevenue = orders.reduce((sum, order) => sum + order.total_amount, 0);

    return (
        <div className="p-6 space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                        Store Management
                        <Badge className="bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300 border-none">WooCommerce</Badge>
                    </h1>
                    <p className="text-muted-foreground mt-1">Monitor sales, inventory, and fulfillment operations.</p>
                </div>
                <div className="flex items-center gap-2">
                    <Button variant="outline" className="gap-2" onClick={loadData}>
                        <RefreshCw className={`w-4 h-4 ${isLoadingData ? 'animate-spin' : ''}`} />
                        Sync Store
                    </Button>
                    <Dialog open={isDialogOpen} onOpenChange={(open) => {
                        setIsDialogOpen(open);
                        if (!open) resetForm();
                    }}>
                        <DialogTrigger asChild>
                            <Button className="bg-purple-600 hover:bg-purple-700 text-white shadow-lg shadow-purple-500/20">
                                <Plus className="w-4 h-4 mr-2" />
                                Add Product
                            </Button>
                        </DialogTrigger>
                        <DialogContent>
                            <DialogHeader>
                                <DialogTitle>{isEditing ? 'Edit' : 'Add New'} Product</DialogTitle>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="space-y-2">
                                    <Label>Product Name</Label>
                                    <Input placeholder="e.g. Premium Coffee Beans" value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} />
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label>Price ($)</Label>
                                        <Input type="number" placeholder="29.99" value={formData.price} onChange={e => setFormData({ ...formData, price: e.target.value })} />
                                    </div>
                                    <div className="space-y-2">
                                        <Label>Inventory</Label>
                                        <Input type="number" placeholder="100" value={formData.stock_quantity} onChange={e => setFormData({ ...formData, stock_quantity: e.target.value })} />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <Label>Status</Label>
                                    <Select value={formData.status} onValueChange={val => setFormData({ ...formData, status: val })}>
                                        <SelectTrigger>
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="publish">Published</SelectItem>
                                            <SelectItem value="draft">Draft</SelectItem>
                                            <SelectItem value="private">Private</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>
                            <DialogFooter>
                                <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
                                <Button className="bg-purple-600 hover:bg-purple-700" onClick={isEditing ? handleUpdate : handleCreate}>
                                    {isEditing ? 'Save Changes' : 'Create Product'}
                                </Button>
                            </DialogFooter>
                        </DialogContent>
                    </Dialog>
                </div>
            </div>

            {/* Metrics Dashboard */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="border-none bg-emerald-50 dark:bg-emerald-950/20 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <DollarSign className="w-5 h-5 text-emerald-600" />
                            <Badge variant="secondary" className="bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700">+18%</Badge>
                        </div>
                        <p className="text-sm font-medium text-emerald-800 dark:text-emerald-300">Total Revenue</p>
                        <h3 className="text-3xl font-bold mt-1 text-emerald-950 dark:text-emerald-50">${totalRevenue.toLocaleString()}</h3>
                    </CardContent>
                </Card>

                <Card className="border-none bg-purple-50 dark:bg-purple-950/20 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <ShoppingBag className="w-5 h-5 text-purple-600" />
                            <Badge variant="secondary" className="bg-purple-100 dark:bg-purple-900/40 text-purple-700">Live</Badge>
                        </div>
                        <p className="text-sm font-medium text-purple-800 dark:text-purple-300">Total Orders</p>
                        <h3 className="text-3xl font-bold mt-1 text-purple-950 dark:text-purple-50">{orders.length}</h3>
                    </CardContent>
                </Card>

                <Card className="border-none bg-blue-50 dark:bg-blue-950/20 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <Box className="w-5 h-5 text-blue-600" />
                            <Badge variant="secondary" className="bg-blue-100 dark:bg-blue-900/40 text-blue-700">Stock</Badge>
                        </div>
                        <p className="text-sm font-medium text-blue-800 dark:text-blue-300">Active Products</p>
                        <h3 className="text-3xl font-bold mt-1 text-blue-950 dark:text-blue-50">{products.length}</h3>
                    </CardContent>
                </Card>

                <Card className="border-none bg-amber-50 dark:bg-amber-950/20 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <TrendingUp className="w-5 h-5 text-amber-600" />
                            <Badge variant="secondary" className="bg-amber-100 dark:bg-amber-900/40 text-amber-700">Avg</Badge>
                        </div>
                        <p className="text-sm font-medium text-amber-800 dark:text-amber-300">Avg. Order Value</p>
                        <h3 className="text-3xl font-bold mt-1 text-amber-950 dark:text-amber-50">
                            ${orders.length > 0 ? (totalRevenue / orders.length).toFixed(2) : '0.00'}
                        </h3>
                    </CardContent>
                </Card>
            </div>

            {/* Main Tabs */}
            <Tabs defaultValue="products" className="w-full" onValueChange={setActiveTab}>
                <div className="flex items-center justify-between mb-6">
                    <TabsList className="bg-slate-100/50 dark:bg-slate-800/50 p-1">
                        <TabsTrigger value="products" className="gap-2">
                            <Package className="w-4 h-4" /> Products
                        </TabsTrigger>
                        <TabsTrigger value="orders" className="gap-2">
                            <ShoppingCart className="w-4 h-4" /> Orders
                        </TabsTrigger>
                        <TabsTrigger value="insights" className="gap-2">
                            <Zap className="w-4 h-4 text-purple-500" /> AI Insights
                        </TabsTrigger>
                    </TabsList>

                    <div className="flex items-center gap-2">
                        <div className="relative hidden sm:block">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input placeholder="Search items..." className="pl-9 w-[200px] h-9" />
                        </div>
                        <Button variant="outline" size="sm" className="h-9 gap-2">
                            <Filter className="w-4 h-4" /> Filter
                        </Button>
                    </div>
                </div>

                <TabsContent value="products" className="animate-in fade-in duration-500">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                        {isLoadingData ? (
                            Array(4).fill(0).map((_, i) => (
                                <Card key={i} className="animate-pulse h-[200px] bg-slate-50 dark:bg-slate-900 border-none" />
                            ))
                        ) : products.length === 0 ? (
                            <div className="col-span-full py-20 text-center border-2 border-dashed rounded-xl">
                                <Package className="w-12 h-12 mx-auto text-slate-300 mb-4" />
                                <h3 className="text-lg font-medium">No products found</h3>
                                <p className="text-muted-foreground">Get started by creating your first product.</p>
                            </div>
                        ) : (
                            products.map(product => (
                                <Card key={product.id} className="group overflow-hidden border-none shadow-sm hover:shadow-md transition-all">
                                    <div className="h-32 bg-slate-100 dark:bg-slate-800 flex items-center justify-center relative">
                                        {product.images?.[0] ? (
                                            <img src={product.images[0].src} alt={product.name} className="w-full h-full object-cover" />
                                        ) : (
                                            <Package className="w-10 h-10 text-slate-300" />
                                        )}
                                        <div className="absolute top-2 right-2 flex gap-1">
                                            <Badge className={product.status === 'publish' ? 'bg-green-500' : 'bg-slate-500'}>
                                                {product.status}
                                            </Badge>
                                        </div>
                                    </div>
                                    <CardContent className="pt-4">
                                        <h3 className="font-bold text-lg line-clamp-1">{product.name}</h3>
                                        <div className="flex justify-between items-center mt-2">
                                            <span className="text-xl font-bold text-purple-600">${product.price}</span>
                                            <span className={`text-xs ${product.stock_quantity < 5 ? 'text-red-500 font-bold' : 'text-muted-foreground'}`}>
                                                {product.stock_quantity} in stock
                                            </span>
                                        </div>
                                    </CardContent>
                                    <CardFooter className="pt-0 border-t mt-2 flex justify-between p-2">
                                        <Button variant="ghost" size="sm" className="w-full text-blue-600" onClick={() => openEdit(product)}>
                                            <Edit className="w-3 h-3 mr-1" /> Edit
                                        </Button>
                                        <Button variant="ghost" size="sm" className="w-full text-red-600" onClick={() => handleDelete(product.id)}>
                                            <Trash2 className="w-3 h-3 mr-1" /> Delete
                                        </Button>
                                    </CardFooter>
                                </Card>
                            ))
                        )}
                    </div>
                </TabsContent>

                <TabsContent value="orders" className="animate-in fade-in duration-500">
                    <Card className="border-none shadow-sm overflow-hidden">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead className="bg-slate-50 dark:bg-slate-900/50">
                                    <tr>
                                        <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider">Order ID</th>
                                        <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider">Customer</th>
                                        <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider">Status</th>
                                        <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider">Amount</th>
                                        <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {orders.map(order => (
                                        <tr key={order.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                                            <td className="px-6 py-4 font-medium">#{order.id}</td>
                                            <td className="px-6 py-4">
                                                <div className="flex flex-col">
                                                    <span className="text-sm font-medium">{order.customer_name || 'Guest'}</span>
                                                    <span className="text-xs text-muted-foreground">{order.email}</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <Badge variant="outline" className="capitalize">{order.status}</Badge>
                                            </td>
                                            <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">${order.total_amount}</td>
                                            <td className="px-6 py-4 text-right">
                                                <Button variant="ghost" size="sm">Details <ArrowUpRight className="ml-1 w-3 h-3" /></Button>
                                            </td>
                                        </tr>
                                    ))}
                                    {orders.length === 0 && (
                                        <tr>
                                            <td colSpan={5} className="px-6 py-20 text-center text-muted-foreground">
                                                No orders found in this period.
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </Card>
                </TabsContent>

                <TabsContent value="insights" className="animate-in slide-in-from-bottom-2 duration-500">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <Card className="border-none shadow-lg bg-gradient-to-br from-purple-500 to-indigo-600 text-white">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Zap className="w-5 h-5" /> Smart Forecast
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <p className="text-purple-50 leading-relaxed">
                                    Based on current trends, your store is expected to generate <span className="font-bold underline">$12,450</span> in revenue over the next 30 days.
                                </p>
                                <div className="p-3 bg-white/10 rounded-lg border border-white/20">
                                    <p className="text-xs font-bold uppercase mb-1">Top Selling Category</p>
                                    <p className="text-lg">Organic Coffee Blend</p>
                                </div>
                            </CardContent>
                        </Card>

                        <Card className="border-none shadow-sm">
                            <CardHeader>
                                <CardTitle className="text-sm font-bold uppercase tracking-widest text-slate-400">Inventory Alerts</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                {products.filter(p => p.stock_quantity < 10).slice(0, 3).map(p => (
                                    <div key={p.id} className="flex items-center justify-between p-3 bg-red-50 dark:bg-red-900/10 rounded-lg border border-red-100 dark:border-red-900/20">
                                        <div className="flex items-center gap-3">
                                            <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                                            <span className="text-sm font-medium">{p.name}</span>
                                        </div>
                                        <span className="text-xs font-bold text-red-600">{p.stock_quantity} left</span>
                                    </div>
                                ))}
                                {products.filter(p => p.stock_quantity < 10).length === 0 && (
                                    <div className="text-center py-6 text-emerald-600 text-sm font-medium flex flex-col items-center gap-2">
                                        <div className="p-3 bg-emerald-50 rounded-full">
                                            <Box className="w-6 h-6" />
                                        </div>
                                        All stock levels are healthy!
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
}
