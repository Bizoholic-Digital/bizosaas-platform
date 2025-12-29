'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { ShoppingCart, Package, Users as UsersIcon, Loader2, Plus, Edit, Trash2, MoreVertical } from 'lucide-react';
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
}

interface Order {
    id: string;
    total_amount: number;
    status: string;
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
                        <Dialog open={isDialogOpen} onOpenChange={(open) => {
                            setIsDialogOpen(open);
                            if (!open) resetForm();
                        }}>
                            <DialogTrigger asChild>
                                <Button>
                                    <Plus className="w-4 h-4 mr-2" />
                                    Add Product
                                </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-[425px]">
                                <DialogHeader>
                                    <DialogTitle>{isEditing ? 'Edit' : 'Add New'} Product</DialogTitle>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="name">Product Name</Label>
                                        <Input
                                            id="name"
                                            value={formData.name}
                                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        />
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <Label htmlFor="price">Price</Label>
                                            <Input
                                                id="price"
                                                type="number"
                                                step="0.01"
                                                value={formData.price}
                                                onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                                            />
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="stock">Stock</Label>
                                            <Input
                                                id="stock"
                                                type="number"
                                                value={formData.stock_quantity}
                                                onChange={(e) => setFormData({ ...formData, stock_quantity: e.target.value })}
                                            />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="status">Status</Label>
                                        <Select
                                            value={formData.status}
                                            onValueChange={(val) => setFormData({ ...formData, status: val })}
                                        >
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select status" />
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
                                    <Button onClick={isEditing ? handleUpdate : handleCreate}>
                                        {isEditing ? 'Save Changes' : 'Add Product'}
                                    </Button>
                                </DialogFooter>
                            </DialogContent>
                        </Dialog>
                    </div>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="products" className="w-full" onValueChange={setActiveTab}>
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
                                        <div className="flex items-center gap-6">
                                            <div className="text-right">
                                                <p className="font-semibold text-slate-900 dark:text-white">${product.price}</p>
                                                <Badge variant={product.status === 'publish' ? 'default' : 'secondary'}>
                                                    {product.status}
                                                </Badge>
                                            </div>
                                            <DropdownMenu>
                                                <DropdownMenuTrigger asChild>
                                                    <Button variant="ghost" size="icon">
                                                        <MoreVertical className="w-4 h-4" />
                                                    </Button>
                                                </DropdownMenuTrigger>
                                                <DropdownMenuContent align="end">
                                                    <DropdownMenuItem onClick={() => openEdit(product)}>
                                                        <Edit className="w-4 h-4 mr-2" /> Edit
                                                    </DropdownMenuItem>
                                                    <DropdownMenuItem className="text-red-600" onClick={() => handleDelete(product.id)}>
                                                        <Trash2 className="w-4 h-4 mr-2" /> Delete
                                                    </DropdownMenuItem>
                                                </DropdownMenuContent>
                                            </DropdownMenu>
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
