'use client';

import React, { useState, useEffect } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/components/ui/use-toast';
import { brainApi } from '@/lib/brain-api';
import { Pencil, Loader2, Star, Link as LinkIcon, ExternalLink } from 'lucide-react';
import { Label } from '@/components/ui/label';

interface McpTool {
    id: string;
    name: string;
    slug: string;
    category_id: string;
    vendor_name?: string;
    affiliate_link?: string;
    sort_order: number;
    is_featured: boolean;
    description?: string;
}

export default function ToolsManagementPage() {
    const [tools, setTools] = useState<McpTool[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [editingTool, setEditingTool] = useState<McpTool | null>(null);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const { toast } = useToast();

    const fetchTools = async () => {
        setIsLoading(true);
        try {
            const data = await brainApi.mcp.getRegistry();
            setTools(data);
        } catch (error) {
            console.error('Failed to fetch tools:', error);
            toast({
                title: "Error fetching tools",
                description: "Could not load the tool registry.",
                variant: "destructive"
            });
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchTools();
    }, []);

    const handleEdit = (tool: McpTool) => {
        setEditingTool({ ...tool });
        setIsDialogOpen(true);
    };

    const handleSave = async () => {
        if (!editingTool) return;

        setIsSaving(true);
        try {
            await brainApi.mcp.updateMcp(editingTool.id, {
                vendor_name: editingTool.vendor_name,
                affiliate_link: editingTool.affiliate_link,
                sort_order: editingTool.sort_order,
                is_featured: editingTool.is_featured,
                description: editingTool.description
            });

            toast({
                title: "Tool updated",
                description: "The tool configuration has been saved successfully.",
            });

            // Update local state or refetch
            setTools(tools.map(t => t.id === editingTool.id ? editingTool : t));
            setIsDialogOpen(false);
        } catch (error) {
            console.error('Failed to update tool:', error);
            toast({
                title: "Update failed",
                description: "Failed to save tool configuration.",
                variant: "destructive"
            });
        } finally {
            setIsSaving(false);
        }
    };

    if (isLoading) {
        return (
            <div className="flex h-96 items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <div className="space-y-6 p-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Tool Registry Management</h2>
                    <p className="text-muted-foreground">
                        Manage tool listings, vendors, affiliate links, and prioritization.
                    </p>
                </div>
                <Button onClick={fetchTools} variant="outline">
                    Refresh Registry
                </Button>
            </div>

            <div className="rounded-md border bg-white dark:bg-gray-800">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead className="w-[80px]">Order</TableHead>
                            <TableHead>Tool Name</TableHead>
                            <TableHead>Vendor</TableHead>
                            <TableHead>Featured</TableHead>
                            <TableHead>Affiliate Link</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {tools.map((tool) => (
                            <TableRow key={tool.id}>
                                <TableCell className="font-medium text-center">{tool.sort_order}</TableCell>
                                <TableCell>
                                    <div className="flex flex-col">
                                        <span className="font-semibold">{tool.name}</span>
                                        <span className="text-xs text-muted-foreground">{tool.slug}</span>
                                    </div>
                                </TableCell>
                                <TableCell>
                                    {tool.vendor_name || <span className="text-muted-foreground italic">--</span>}
                                </TableCell>
                                <TableCell>
                                    {tool.is_featured ? (
                                        <Badge variant="default" className="bg-yellow-500 hover:bg-yellow-600">Featured</Badge>
                                    ) : (
                                        <span className="text-muted-foreground text-sm">No</span>
                                    )}
                                </TableCell>
                                <TableCell>
                                    {tool.affiliate_link ? (
                                        <a href={tool.affiliate_link} target="_blank" rel="noopener noreferrer" className="flex items-center text-blue-600 hover:underline text-sm">
                                            <LinkIcon className="h-3 w-3 mr-1" />
                                            Link configured
                                        </a>
                                    ) : (
                                        <span className="text-muted-foreground text-sm italic">Not set</span>
                                    )}
                                </TableCell>
                                <TableCell className="text-right">
                                    <Button size="sm" variant="ghost" onClick={() => handleEdit(tool)}>
                                        <Pencil className="h-4 w-4" />
                                        <span className="sr-only">Edit</span>
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>

            {/* Edit Dialog */}
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                <DialogContent className="sm:max-w-[500px]">
                    <DialogHeader>
                        <DialogTitle>Edit Tool Configuration</DialogTitle>
                    </DialogHeader>
                    {editingTool && (
                        <div className="grid gap-4 py-4">
                            <div className="grid gap-2">
                                <Label htmlFor="name">Tool Name</Label>
                                <Input id="name" value={editingTool.name} disabled />
                            </div>

                            <div className="grid gap-2">
                                <Label htmlFor="vendor">Vendor Name</Label>
                                <Input
                                    id="vendor"
                                    value={editingTool.vendor_name || ''}
                                    onChange={(e) => setEditingTool({ ...editingTool, vendor_name: e.target.value })}
                                    placeholder="e.g. Automattic"
                                />
                            </div>

                            <div className="grid gap-2">
                                <Label htmlFor="affiliate">Affiliate Link</Label>
                                <div className="flex gap-2">
                                    <Input
                                        id="affiliate"
                                        value={editingTool.affiliate_link || ''}
                                        onChange={(e) => setEditingTool({ ...editingTool, affiliate_link: e.target.value })}
                                        placeholder="https://partner.com/ref/..."
                                    />
                                    {editingTool.affiliate_link && (
                                        <Button size="icon" variant="ghost" asChild>
                                            <a href={editingTool.affiliate_link} target="_blank" rel="noopener noreferrer">
                                                <ExternalLink className="h-4 w-4" />
                                            </a>
                                        </Button>
                                    )}
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="grid gap-2">
                                    <Label htmlFor="sort">Sort Order (Priority)</Label>
                                    <Input
                                        id="sort"
                                        type="number"
                                        value={editingTool.sort_order}
                                        onChange={(e) => setEditingTool({ ...editingTool, sort_order: parseInt(e.target.value) || 0 })}
                                    />
                                </div>

                                <div className="flex items-center justify-between rounded-lg border p-3 shadow-sm">
                                    <div className="space-y-0.5">
                                        <Label htmlFor="featured" className="text-base">Featured</Label>
                                        <p className="text-xs text-muted-foreground">Highlight this tool</p>
                                    </div>
                                    <Switch
                                        id="featured"
                                        checked={editingTool.is_featured}
                                        onCheckedChange={(checked) => setEditingTool({ ...editingTool, is_featured: checked })}
                                    />
                                </div>
                            </div>
                        </div>
                    )}
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
                        <Button onClick={handleSave} disabled={isSaving}>
                            {isSaving && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            Save Changes
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}
