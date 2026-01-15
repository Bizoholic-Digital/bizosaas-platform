'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import {
    Search,
    ExternalLink,
    Save,
    Edit2,
    Star,
    TrendingUp,
    Package,
    Plus,
    Trash2,
    AlertCircle
} from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";

interface Mcp {
    id: string;
    name: string;
    slug: string;
    description: string;
    category_id: string;
    vendor_name?: string;
    affiliate_link?: string;
    sort_order: number;
    is_featured: boolean;
    is_official: boolean;
    capabilities: string[];
}

interface Category {
    id: string;
    name: string;
    slug: string;
    icon: string;
}

export default function McpManagementPage() {
    const [mcps, setMcps] = useState<Mcp[]>([]);
    const [categories, setCategories] = useState<Category[]>([]);
    const [selectedCategory, setSelectedCategory] = useState<string>('all');
    const [searchQuery, setSearchQuery] = useState('');
    const [editingMcp, setEditingMcp] = useState<Mcp | null>(null);
    const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
    const [newMcp, setNewMcp] = useState<Partial<Mcp>>({
        name: '',
        slug: '',
        category_id: '',
        description: '',
        vendor_name: '',
        affiliate_link: '',
        is_official: false,
        is_featured: false,
        sort_order: 0,
        capabilities: []
    });
    const [loading, setLoading] = useState(true);
    const { toast } = useToast();

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            setLoading(true);
            const [mcpsRes, categoriesRes] = await Promise.all([
                fetch('/api/brain/mcp/registry'),
                fetch('/api/brain/mcp/categories')
            ]);

            if (mcpsRes.ok && categoriesRes.ok) {
                const mcpsData = await mcpsRes.json();
                const categoriesData = await categoriesRes.json();
                setMcps(mcpsData);
                setCategories(categoriesData);

                // Set default category for "Add" dialog
                if (categoriesData.length > 0 && !newMcp.category_id) {
                    setNewMcp(prev => ({ ...prev, category_id: categoriesData[0].id }));
                }
            }
        } catch (error) {
            console.error('Failed to fetch MCP data:', error);
            toast({
                title: 'Error',
                description: 'Failed to load MCP data',
                variant: 'destructive'
            });
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async (mcp: Mcp) => {
        try {
            const response = await fetch(`/api/brain/mcp/${mcp.id}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    vendor_name: mcp.vendor_name,
                    affiliate_link: mcp.affiliate_link,
                    sort_order: mcp.sort_order,
                    is_featured: mcp.is_featured,
                    description: mcp.description
                })
            });

            if (response.ok) {
                toast({
                    title: 'Success',
                    description: `${mcp.name} updated successfully`
                });
                setEditingMcp(null);
                fetchData();
            } else {
                throw new Error('Failed to update MCP');
            }
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to update MCP',
                variant: 'destructive'
            });
        }
    };

    const handleAdd = async () => {
        if (!newMcp.name || !newMcp.slug || !newMcp.category_id) {
            toast({
                title: 'Validation Error',
                description: 'Please fill in all required fields',
                variant: 'destructive'
            });
            return;
        }

        try {
            const response = await fetch('/api/brain/mcp/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ...newMcp,
                    mcp_config: { type: 'standard' } // Default config
                })
            });

            if (response.ok) {
                toast({
                    title: 'Success',
                    description: `${newMcp.name} added to marketplace`
                });
                setIsAddDialogOpen(false);
                setNewMcp({
                    name: '',
                    slug: '',
                    category_id: categories[0]?.id || '',
                    description: '',
                    vendor_name: '',
                    affiliate_link: '',
                    is_official: false,
                    is_featured: false,
                    sort_order: 0,
                    capabilities: []
                });
                fetchData();
            } else {
                const err = await response.json();
                throw new Error(err.detail || 'Failed to add MCP');
            }
        } catch (error: any) {
            toast({
                title: 'Error',
                description: error.message,
                variant: 'destructive'
            });
        }
    };

    const handleDelete = async (mcpId: string, mcpName: string) => {
        if (!confirm(`Are you sure you want to delete ${mcpName}? This action cannot be undone.`)) {
            return;
        }

        try {
            const response = await fetch(`/api/brain/mcp/${mcpId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                toast({
                    title: 'Deleted',
                    description: `${mcpName} has been removed from the platform`
                });
                fetchData();
            } else {
                throw new Error('Failed to delete MCP');
            }
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to delete MCP',
                variant: 'destructive'
            });
        }
    };

    const filteredMcps = mcps.filter(mcp => {
        const matchesCategory = selectedCategory === 'all' || mcp.category_id === selectedCategory;
        const matchesSearch = mcp.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            mcp.slug.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesCategory && matchesSearch;
    });

    return (
        <div className="max-w-7xl mx-auto space-y-6 p-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold">MCP Marketplace</h1>
                    <p className="text-muted-foreground">
                        Manage the platform's tool inventory, affiliate programs, and feature visibility
                    </p>
                </div>
                <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
                    <DialogTrigger asChild>
                        <Button className="bg-blue-600 hover:bg-blue-700">
                            <Plus className="h-4 w-4 mr-2" />
                            Add New MCP
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[600px]">
                        <DialogHeader>
                            <DialogTitle>Add New MCP to Marketplace</DialogTitle>
                            <DialogDescription>
                                Register a new tool or service to make it available for client selection.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Name *</Label>
                                    <Input
                                        placeholder="e.g. ActiveCampaign"
                                        value={newMcp.name}
                                        onChange={e => setNewMcp({ ...newMcp, name: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label>Slug *</Label>
                                    <Input
                                        placeholder="e.g. activecampaign"
                                        value={newMcp.slug}
                                        onChange={e => setNewMcp({ ...newMcp, slug: e.target.value })}
                                    />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <Label>Category *</Label>
                                <select
                                    className="w-full p-2 border rounded-md"
                                    value={newMcp.category_id}
                                    onChange={e => setNewMcp({ ...newMcp, category_id: e.target.value })}
                                >
                                    {categories.map(cat => (
                                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                                    ))}
                                </select>
                            </div>
                            <div className="space-y-2">
                                <Label>Description</Label>
                                <Textarea
                                    placeholder="Brief description of the service"
                                    value={newMcp.description}
                                    onChange={e => setNewMcp({ ...newMcp, description: e.target.value })}
                                />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Vendor Name</Label>
                                    <Input
                                        placeholder="Company Name"
                                        value={newMcp.vendor_name}
                                        onChange={e => setNewMcp({ ...newMcp, vendor_name: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label>Affiliate Link</Label>
                                    <Input
                                        placeholder="https://partner-link.com"
                                        value={newMcp.affiliate_link}
                                        onChange={e => setNewMcp({ ...newMcp, affiliate_link: e.target.value })}
                                    />
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <div className="flex items-center space-x-2">
                                    <Switch
                                        checked={newMcp.is_official}
                                        onCheckedChange={checked => setNewMcp({ ...newMcp, is_official: checked })}
                                    />
                                    <Label>Official</Label>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <Switch
                                        checked={newMcp.is_featured}
                                        onCheckedChange={checked => setNewMcp({ ...newMcp, is_featured: checked })}
                                    />
                                    <Label>Featured</Label>
                                </div>
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={() => setIsAddDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleAdd}>Create MCP</Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Marketplace Size</CardTitle>
                        <Package className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{mcps.length} Tools</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Featured</CardTitle>
                        <Star className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {mcps.filter(m => m.is_featured).length}
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Affiliate Links</CardTitle>
                        <ExternalLink className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {mcps.filter(m => m.affiliate_link).length}
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Categories</CardTitle>
                        <TrendingUp className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{categories.length}</div>
                    </CardContent>
                </Card>
            </div>

            {/* Filters */}
            <Card>
                <CardContent className="pt-6">
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="flex-1">
                            <div className="relative">
                                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <Input
                                    placeholder="Search marketplace..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="pl-10"
                                />
                            </div>
                        </div>
                        <Tabs value={selectedCategory} onValueChange={setSelectedCategory} className="w-full md:w-auto">
                            <TabsList>
                                <TabsTrigger value="all">All</TabsTrigger>
                                {categories.slice(0, 5).map(cat => (
                                    <TabsTrigger key={cat.id} value={cat.id}>
                                        {cat.name}
                                    </TabsTrigger>
                                ))}
                            </TabsList>
                        </Tabs>
                    </div>
                </CardContent>
            </Card>

            {/* MCP List */}
            <div className="grid grid-cols-1 gap-4">
                {loading ? (
                    <Card>
                        <CardContent className="pt-6">
                            <p className="text-center text-muted-foreground text-sm flex items-center justify-center">
                                <TrendingUp className="h-4 w-4 mr-2 animate-spin" />
                                Analyzing Marketplace...
                            </p>
                        </CardContent>
                    </Card>
                ) : filteredMcps.length === 0 ? (
                    <Card>
                        <CardContent className="pt-6">
                            <div className="text-center py-6">
                                <AlertCircle className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
                                <p className="text-muted-foreground font-medium">No services found match your criteria</p>
                                <Button variant="link" onClick={() => { setSearchQuery(''); setSelectedCategory('all'); }}>Clear all filters</Button>
                            </div>
                        </CardContent>
                    </Card>
                ) : (
                    filteredMcps.map(mcp => (
                        <Card key={mcp.id} className="group hover:border-blue-200 transition-colors">
                            <CardHeader>
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2">
                                            <CardTitle>{mcp.name}</CardTitle>
                                            {mcp.is_featured && (
                                                <Badge variant="secondary" className="bg-yellow-50 text-yellow-700 border-yellow-200">
                                                    <Star className="h-3 w-3 mr-1 fill-yellow-500" />
                                                    Featured
                                                </Badge>
                                            )}
                                            {mcp.is_official && (
                                                <Badge className="bg-blue-50 text-blue-700 border-blue-200">Official Partner</Badge>
                                            )}
                                        </div>
                                        <CardDescription className="mt-1 line-clamp-2">{mcp.description}</CardDescription>
                                    </div>
                                    <div className="flex gap-2">
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            className="text-red-500 hover:text-red-700 hover:bg-red-50"
                                            onClick={() => handleDelete(mcp.id, mcp.name)}
                                        >
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => setEditingMcp(editingMcp?.id === mcp.id ? null : mcp)}
                                        >
                                            <Edit2 className="h-4 w-4 mr-2" />
                                            {editingMcp?.id === mcp.id ? 'Cancel' : 'Manage'}
                                        </Button>
                                    </div>
                                </div>
                            </CardHeader>

                            {editingMcp?.id === mcp.id && (
                                <CardContent className="space-y-4 border-t pt-4 bg-slate-50/50">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <Label>Vendor Information</Label>
                                            <Input
                                                value={editingMcp.vendor_name || ''}
                                                onChange={(e) => setEditingMcp({ ...editingMcp, vendor_name: e.target.value })}
                                                placeholder="e.g., Zoho Corporation"
                                                className="bg-white"
                                            />
                                        </div>
                                        <div className="space-y-2">
                                            <Label>Marketplace Position (Sort Order)</Label>
                                            <Input
                                                type="number"
                                                value={editingMcp.sort_order}
                                                onChange={(e) => setEditingMcp({ ...editingMcp, sort_order: parseInt(e.target.value) })}
                                                className="bg-white"
                                            />
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <Label>Strategic Partner Link (Affiliate)</Label>
                                        <Input
                                            value={editingMcp.affiliate_link || ''}
                                            onChange={(e) => setEditingMcp({ ...editingMcp, affiliate_link: e.target.value })}
                                            placeholder="https://partner-portal.com/ref/bizosaas"
                                            className="bg-white"
                                        />
                                        <p className="text-xs text-muted-foreground flex items-center">
                                            <ExternalLink className="h-3 w-3 mr-1" />
                                            This link generates revenue when users sign up for {mcp.name}
                                        </p>
                                    </div>

                                    <div className="space-y-2">
                                        <Label>Marketplace Description</Label>
                                        <Textarea
                                            value={editingMcp.description || ''}
                                            onChange={(e) => setEditingMcp({ ...editingMcp, description: e.target.value })}
                                            rows={3}
                                            className="bg-white"
                                        />
                                    </div>

                                    <div className="flex items-center space-x-2">
                                        <Switch
                                            checked={editingMcp.is_featured}
                                            onCheckedChange={(checked) => setEditingMcp({ ...editingMcp, is_featured: checked })}
                                        />
                                        <Label>Show prominently in Client Onboarding (Featured)</Label>
                                    </div>

                                    <div className="flex justify-end gap-2 pt-2">
                                        <Button variant="outline" onClick={() => setEditingMcp(null)}>
                                            Discard Changes
                                        </Button>
                                        <Button onClick={() => handleSave(editingMcp)} className="bg-blue-600 hover:bg-blue-700">
                                            <Save className="h-4 w-4 mr-2" />
                                            Sync to Platform
                                        </Button>
                                    </div>
                                </CardContent>
                            )}

                            {(!editingMcp || editingMcp.id !== mcp.id) && (
                                <CardContent className="text-xs text-muted-foreground border-t pt-4">
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                        <div className="flex flex-col">
                                            <span className="font-semibold text-slate-700 uppercase tracking-wider mb-1">Provider</span>
                                            {mcp.vendor_name || '--'}
                                        </div>
                                        <div className="flex flex-col">
                                            <span className="font-semibold text-slate-700 uppercase tracking-wider mb-1">Priority</span>
                                            {mcp.sort_order}
                                        </div>
                                        <div className="col-span-2 flex flex-col">
                                            <span className="font-semibold text-slate-700 uppercase tracking-wider mb-1">Partner Link</span>
                                            {mcp.affiliate_link ? (
                                                <a href={mcp.affiliate_link} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 hover:underline inline-flex items-center">
                                                    {mcp.affiliate_link.substring(0, 40)}...
                                                    <ExternalLink className="h-3 w-3 ml-1" />
                                                </a>
                                            ) : (
                                                'Direct signup integration'
                                            )}
                                        </div>
                                    </div>
                                </CardContent>
                            )}
                        </Card>
                    ))
                )}
            </div>
        </div>
    );
}
