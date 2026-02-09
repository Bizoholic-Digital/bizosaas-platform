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
    is_recommended: boolean;
    quality_score: number;
    github_stars?: number;
    tags: string[];
    capabilities: string[];
}

interface McpApproval {
    id: string;
    mcp_name: string;
    mcp_slug: string;
    description: string;
    requested_by_user?: string;
    requested_by_agent?: string;
    status: 'pending' | 'approved' | 'rejected';
    review_notes?: string;
    created_at: string;
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
    const [approvals, setApprovals] = useState<McpApproval[]>([]);
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
            const [mcpsRes, categoriesRes, approvalsRes] = await Promise.all([
                fetch('/api/brain/mcp/registry'),
                fetch('/api/brain/mcp/categories'),
                fetch('/api/brain/mcp/approvals')
            ]);

            if (mcpsRes.ok && categoriesRes.ok) {
                const mcpsData = await mcpsRes.json();
                const categoriesData = await categoriesRes.json();
                const approvalsData = approvalsRes.ok ? await approvalsRes.json() : [];

                setMcps(mcpsData);
                setCategories(categoriesData);
                setApprovals(approvalsData);

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

    const handleReviewApproval = async (approvalId: string, status: 'approved' | 'rejected', notes: string) => {
        try {
            const response = await fetch(`/api/brain/mcp/approvals/${approvalId}/review`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status, notes })
            });

            if (response.ok) {
                toast({
                    title: 'Review Submitted',
                    description: `Approval request ${status} successfully`
                });
                fetchData();
            } else {
                throw new Error('Failed to submit review');
            }
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to submit review',
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
                    <h1 className="text-3xl font-bold">MCP Management</h1>
                    <p className="text-muted-foreground">
                        Govern the platform's AI tool registry and approve new capability requests
                    </p>
                </div>
                <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
                    <DialogTrigger asChild>
                        <Button className="bg-blue-600 hover:bg-blue-700">
                            <Plus className="h-4 w-4 mr-2" />
                            Register New Server
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[600px]">
                        <DialogHeader>
                            <DialogTitle>Register New MCP Server</DialogTitle>
                            <DialogDescription>
                                Add a verified MCP server to the global registry.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Name *</Label>
                                    <Input
                                        placeholder="e.g. Google BigQuery"
                                        value={newMcp.name}
                                        onChange={e => setNewMcp({ ...newMcp, name: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label>Slug *</Label>
                                    <Input
                                        placeholder="e.g. bigquery"
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
                                    placeholder="Capabilities and use cases"
                                    value={newMcp.description}
                                    onChange={e => setNewMcp({ ...newMcp, description: e.target.value })}
                                />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Vendor Name</Label>
                                    <Input
                                        placeholder="Google"
                                        value={newMcp.vendor_name}
                                        onChange={e => setNewMcp({ ...newMcp, vendor_name: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label>Affiliate/Partner Link</Label>
                                    <Input
                                        placeholder="Internal or External URL"
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

            <Tabs defaultValue="marketplace" className="space-y-6">
                <TabsList className="grid w-full grid-cols-2 lg:w-[400px]">
                    <TabsTrigger value="marketplace">Marketplace</TabsTrigger>
                    <TabsTrigger value="approvals" className="relative">
                        Approval Requests
                        {approvals.filter(a => a.status === 'pending').length > 0 && (
                            <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[10px] text-white">
                                {approvals.filter(a => a.status === 'pending').length}
                            </span>
                        )}
                    </TabsTrigger>
                </TabsList>

                <TabsContent value="marketplace" className="space-y-6">
                    {/* Stats Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Marketplace Size</CardTitle>
                                <Package className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">{mcps.length} Servers</div>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Avg Quality Score</CardTitle>
                                <TrendingUp className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">
                                    {(mcps.reduce((acc, m) => acc + (m.quality_score || 0), 0) / (mcps.length || 1)).toFixed(1)}
                                </div>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Official Partners</CardTitle>
                                <Badge className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">
                                    {mcps.filter(m => m.is_official).length}
                                </div>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Pending Approvals</CardTitle>
                                <AlertCircle className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-red-600">
                                    {approvals.filter(a => a.status === 'pending').length}
                                </div>
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
                                            placeholder="Search servers, tags, or capabilities..."
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
                                        Syncing with Global Registry...
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
                                                    <Badge variant="outline" className="text-[10px] font-normal uppercase tracking-wider">
                                                        SCORE: {mcp.quality_score}/100
                                                    </Badge>
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
                                                    <span className="font-semibold text-slate-700 uppercase tracking-wider mb-1">Tags</span>
                                                    <div className="flex flex-wrap gap-1">
                                                        {mcp.tags?.map(tag => (
                                                            <Badge key={tag} variant="secondary" className="px-1 py-0 text-[9px] uppercase">{tag}</Badge>
                                                        ))}
                                                    </div>
                                                </div>
                                                <div className="flex flex-col">
                                                    <span className="font-semibold text-slate-700 uppercase tracking-wider mb-1">GitHub Stars</span>
                                                    {mcp.github_stars || 0}
                                                </div>
                                                <div className="col-span-2 flex flex-col">
                                                    <span className="font-semibold text-slate-700 uppercase tracking-wider mb-1">Capabilities</span>
                                                    <div className="flex flex-wrap gap-1">
                                                        {mcp.capabilities?.map(cap => (
                                                            <span key={cap} className="bg-slate-100 px-1 rounded">{cap}</span>
                                                        ))}
                                                    </div>
                                                </div>
                                            </div>
                                        </CardContent>
                                    )}
                                </Card>
                            ))
                        )}
                    </div>
                </TabsContent>

                <TabsContent value="approvals" className="space-y-6">
                    <div className="grid grid-cols-1 gap-4">
                        {approvals.length === 0 ? (
                            <Card>
                                <CardContent className="flex flex-col items-center justify-center py-12">
                                    <div className="h-12 w-12 rounded-full bg-slate-100 flex items-center justify-center mb-4">
                                        <Search className="h-6 w-6 text-slate-400" />
                                    </div>
                                    <h3 className="text-lg font-semibold">No Pending Requests</h3>
                                    <p className="text-muted-foreground text-center max-w-sm">
                                        AI Agents and Users have not submitted any new MCP servers for approval yet.
                                    </p>
                                </CardContent>
                            </Card>
                        ) : (
                            approvals.map(approval => (
                                <Card key={approval.id} className={approval.status === 'pending' ? 'border-l-4 border-l-blue-500' : ''}>
                                    <CardHeader className="pb-4">
                                        <div className="flex justify-between items-start">
                                            <div>
                                                <div className="flex items-center gap-2 mb-1">
                                                    <CardTitle className="text-lg">{approval.mcp_name}</CardTitle>
                                                    <Badge variant={
                                                        approval.status === 'approved' ? 'default' :
                                                            approval.status === 'rejected' ? 'destructive' : 'secondary'
                                                    }>
                                                        {approval.status}
                                                    </Badge>
                                                </div>
                                                <CardDescription>
                                                    Requested {new Date(approval.created_at).toLocaleDateString()} by {approval.requested_by_agent ? 'Agent' : 'User'}
                                                </CardDescription>
                                            </div>
                                            {approval.status === 'pending' && (
                                                <div className="flex gap-2">
                                                    <Button
                                                        variant="outline"
                                                        size="sm"
                                                        className="text-red-600 hover:bg-red-50"
                                                        onClick={() => handleReviewApproval(approval.id, 'rejected', 'Does not meet security standards')}
                                                    >
                                                        Reject
                                                    </Button>
                                                    <Button
                                                        size="sm"
                                                        className="bg-green-600 hover:bg-green-700"
                                                        onClick={() => handleReviewApproval(approval.id, 'approved', 'Verified and recommended')}
                                                    >
                                                        Approve
                                                    </Button>
                                                </div>
                                            )}
                                        </div>
                                    </CardHeader>
                                    <CardContent className="pt-0 space-y-4">
                                        <div className="bg-slate-50 p-3 rounded-md text-sm italic">
                                            "{approval.description}"
                                        </div>
                                        {approval.review_notes && (
                                            <div className="text-xs text-muted-foreground">
                                                <strong>Admin Note:</strong> {approval.review_notes}
                                            </div>
                                        )}
                                    </CardContent>
                                </Card>
                            ))
                        )}
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
}
