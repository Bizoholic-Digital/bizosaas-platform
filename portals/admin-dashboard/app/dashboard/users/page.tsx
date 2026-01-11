'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { User, Shield, UserCheck, MoreVertical, Search, Filter, ShieldAlert, Mail, RefreshCw, Plus, Trash2, Pencil, Eye } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { adminApi } from '@/lib/api/admin';
import { toast } from 'sonner';
import { PageHeader } from '@/components/dashboard/PageHeader';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from '@/components/ui/label';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Checkbox } from '@/components/ui/checkbox';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { UserActivityLog } from '@/components/UserActivityLog';

export default function GlobalUsersPage() {
    const [users, setUsers] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    // Dialog States
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [isEditOpen, setIsEditOpen] = useState(false);
    const [currentUser, setCurrentUser] = useState<any>(null);
    const [formData, setFormData] = useState({ name: '', email: '', role: 'User', status: 'active' });
    const [permissions, setPermissions] = useState({
        ai_access: false,
        crm_access: false,
        analytics_advanced: false,
        beta_features: false
    });
    const [isSubmitting, setIsSubmitting] = useState(false);

    const loadUsers = async () => {
        setLoading(true);
        try {
            const res = await adminApi.getUsers();
            if (Array.isArray(res.data)) {
                setUsers(res.data);
            } else {
                setUsers([]);
            }
        } catch (error) {
            console.error(error);
            toast.error("Failed to load users");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadUsers();
    }, []);

    const handleCreate = async () => {
        setIsSubmitting(true);
        try {
            await adminApi.createUser(formData);
            toast.success("User created successfully");
            setIsCreateOpen(false);
            setFormData({ name: '', email: '', role: 'User', status: 'active' });
            loadUsers();
        } catch (e) {
            toast.error("Failed to create user");
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleUpdate = async () => {
        if (!currentUser) return;
        setIsSubmitting(true);
        try {
            await Promise.all([
                adminApi.updateUser(currentUser.id, formData),
                adminApi.updateUserPermissions(currentUser.id, permissions)
            ]);
            toast.success("User updated successfully");
            setIsEditOpen(false);
            setCurrentUser(null);
            loadUsers();
        } catch (e) {
            toast.error("Failed to update user");
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleDelete = async (userId: string) => {
        if (!window.confirm("Are you sure you want to delete this user?")) return;
        try {
            await adminApi.deleteUser(userId);
            toast.success("User deleted successfully");
            loadUsers();
        } catch (e) {
            toast.error("Failed to delete user");
        }
    };

    const handleImpersonate = async (userId: string, userName: string) => {
        if (!window.confirm(`Are you sure you want to impersonate ${userName}?`)) return;
        try {
            const res = await adminApi.impersonateUser(userId);
            if (res.data?.token) {
                // In a real scenario, redirect to Client Portal with token
                // For now, we'll assume Client Portal is on localhost:3000 for dev
                // or similar structure.
                const isLocal = window.location.hostname === 'localhost';
                const clientUrl = isLocal ? 'http://localhost:3000' : 'https://app.bizoholic.net';
                const url = `${clientUrl}/auth/impersonate?token=${res.data.token}`;
                window.open(url, '_blank');
                toast.success(`Impersonating ${userName}`);
            }
        } catch (e) {
            toast.error("Failed to start impersonation");
        }
    };

    const openEdit = (user: any) => {
        setCurrentUser(user);
        setFormData({ name: user.name, email: user.email, role: user.role, status: user.status });
        setPermissions(user.permissions || {
            ai_access: false,
            crm_access: false,
            analytics_advanced: false,
            beta_features: false
        });
        setIsEditOpen(true);
    };

    const safeUsers = Array.isArray(users) ? users : [];
    const filteredUsers = safeUsers.filter(u =>
        u.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        u.email?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="p-4 md:p-6 space-y-6 bg-slate-50 dark:bg-slate-950 min-h-full">
            <PageHeader
                title={
                    <>Global User <span className="text-indigo-600">Management</span></>
                }
                description="Manage all user accounts and roles across the entire platform."
            >
                <Button variant="outline" size="sm" className="border-slate-200 dark:border-slate-800" onClick={loadUsers} disabled={loading}>
                    <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Sync Directory
                </Button>
                <Button className="bg-indigo-600 hover:bg-indigo-700 font-bold" size="sm" onClick={() => setIsCreateOpen(true)}>
                    <UserCheck className="mr-2 h-4 w-4" /> Provision User
                </Button>
            </PageHeader>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Users</CardTitle>
                        <User className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{users.length}</div>
                        <p className="text-xs text-muted-foreground">Registered accounts</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Active Admins</CardTitle>
                        <Shield className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{users.filter(u => u.role === 'Admin' || u.role === 'Super Admin').length}</div>
                        <p className="text-xs text-muted-foreground">Across all tenants</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">New Today</CardTitle>
                        <UserCheck className="h-4 w-4 text-green-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-green-600">0</div>
                        <p className="text-xs text-muted-foreground">New signups</p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div>
                            <CardTitle>Global Directory</CardTitle>
                            <CardDescription>Managed view of accounts and their cross-tenant access level.</CardDescription>
                        </div>
                        <div className="relative w-full md:w-64">
                            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search users..."
                                className="pl-8"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    {/* Desktop View */}
                    <div className="hidden md:block">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>User</TableHead>
                                    <TableHead>Role</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Last Login</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {loading ? (
                                    <TableRow>
                                        <TableCell colSpan={5} className="text-center py-8">
                                            <RefreshCw className="h-8 w-8 animate-spin mx-auto text-blue-600" />
                                        </TableCell>
                                    </TableRow>
                                ) : filteredUsers.length === 0 ? (
                                    <TableRow>
                                        <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                                            No users found.
                                        </TableCell>
                                    </TableRow>
                                ) : (
                                    filteredUsers.map((u) => (
                                        <TableRow key={u.id}>
                                            <TableCell>
                                                <div className="flex items-center gap-3">
                                                    <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center font-bold text-xs">
                                                        {u.name?.charAt(0) || 'U'}
                                                    </div>
                                                    <div>
                                                        <div className="font-bold">{u.name}</div>
                                                        <div className="text-xs text-muted-foreground">{u.email}</div>
                                                    </div>
                                                </div>
                                            </TableCell>
                                            <TableCell>
                                                <Badge variant="outline" className={u.role === 'Super Admin' ? 'border-purple-500 text-purple-600' : ''}>
                                                    {u.role || 'User'}
                                                </Badge>
                                            </TableCell>
                                            <TableCell>
                                                <div className="flex items-center gap-2">
                                                    <div className={`w-2 h-2 rounded-full ${u.status === 'active' ? 'bg-green-500' : 'bg-gray-400'}`} />
                                                    <span className="capitalize">{u.status || 'inactive'}</span>
                                                </div>
                                            </TableCell>
                                            <TableCell className="text-muted-foreground">{u.lastLogin || 'Never'}</TableCell>
                                            <TableCell className="text-right">
                                                <div className="flex justify-end gap-2">
                                                    <Button variant="ghost" size="icon" title="Impersonate" onClick={() => handleImpersonate(u.id, u.name)}>
                                                        <Eye className="h-4 w-4" />
                                                    </Button>
                                                    <Button variant="ghost" size="icon" onClick={() => openEdit(u)}>
                                                        <Pencil className="h-4 w-4" />
                                                    </Button>
                                                    <Button variant="ghost" size="icon" className="text-red-500 hover:text-red-700 hover:bg-red-50" onClick={() => handleDelete(u.id)}>
                                                        <Trash2 className="h-4 w-4" />
                                                    </Button>
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                )}
                            </TableBody>
                        </Table>
                    </div>

                    {/* Mobile View */}
                    <div className="md:hidden space-y-4">
                        {loading ? (
                            <div className="flex justify-center py-8">
                                <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
                            </div>
                        ) : filteredUsers.length === 0 ? (
                            <div className="text-center py-8 text-muted-foreground">
                                No users found.
                            </div>
                        ) : (
                            filteredUsers.map((u) => (
                                <div key={u.id} className="p-4 border rounded-lg space-y-3 bg-white dark:bg-slate-900 shadow-sm">
                                    <div className="flex justify-between items-start">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center font-bold">
                                                {u.name?.charAt(0) || 'U'}
                                            </div>
                                            <div>
                                                <div className="font-bold">{u.name}</div>
                                                <div className="text-xs text-muted-foreground">{u.email}</div>
                                            </div>
                                        </div>
                                        <div className="flex gap-1">
                                            <Button variant="ghost" size="icon" onClick={() => handleImpersonate(u.id, u.name)}>
                                                <Eye className="h-4 w-4" />
                                            </Button>
                                            <Button variant="ghost" size="icon" onClick={() => openEdit(u)}>
                                                <Pencil className="h-4 w-4" />
                                            </Button>
                                            <Button variant="ghost" size="icon" className="text-red-500" onClick={() => handleDelete(u.id)}>
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </div>
                                    <div className="flex justify-between items-center text-sm pt-2 border-t border-slate-100 dark:border-slate-800">
                                        <Badge variant="outline">{u.role || 'User'}</Badge>
                                        <div className="flex items-center gap-2">
                                            <div className={`w-2 h-2 rounded-full ${u.status === 'active' ? 'bg-green-500' : 'bg-gray-400'}`} />
                                            <span className="capitalize">{u.status || 'inactive'}</span>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </CardContent>
            </Card>

            {/* Create Dialog */}
            <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Provision New User</DialogTitle>
                        <DialogDescription>Add a new user to the platform. They will receive an email invitation.</DialogDescription>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                        <div className="space-y-2">
                            <Label>Full Name</Label>
                            <Input value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} placeholder="John Doe" />
                        </div>
                        <div className="space-y-2">
                            <Label>Email Address</Label>
                            <Input value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} placeholder="john@example.com" type="email" />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label>Role</Label>
                                <Select value={formData.role} onValueChange={v => setFormData({ ...formData, role: v })}>
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="User">User</SelectItem>
                                        <SelectItem value="Admin">Admin</SelectItem>
                                        <SelectItem value="Super Admin">Super Admin</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="space-y-2">
                                <Label>Status</Label>
                                <Select value={formData.status} onValueChange={v => setFormData({ ...formData, status: v })}>
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="active">Active</SelectItem>
                                        <SelectItem value="inactive">Inactive</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsCreateOpen(false)}>Cancel</Button>
                        <Button onClick={handleCreate} disabled={isSubmitting}>
                            {isSubmitting ? "Creating..." : "Create User"}
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            {/* Edit Dialog */}
            <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
                <DialogContent className="max-w-2xl max-h-[90vh] flex flex-col">
                    <DialogHeader>
                        <DialogTitle>User Details: {formData.name}</DialogTitle>
                        <DialogDescription>Manage profile, permissions, and view activity history.</DialogDescription>
                    </DialogHeader>

                    <div className="flex-1 overflow-y-auto py-4">
                        <Tabs defaultValue="profile" className="w-full">
                            <TabsList className="grid w-full grid-cols-3">
                                <TabsTrigger value="profile">Profile & Account</TabsTrigger>
                                <TabsTrigger value="permissions">Permissions (RBAC)</TabsTrigger>
                                <TabsTrigger value="activity">Activity Log</TabsTrigger>
                            </TabsList>

                            <TabsContent value="profile" className="space-y-4 py-4">
                                <div className="space-y-4">
                                    <div className="space-y-2">
                                        <Label>Full Name</Label>
                                        <Input value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} />
                                    </div>
                                    <div className="space-y-2">
                                        <Label>Email Address</Label>
                                        <Input value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} type="email" />
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <Label>Role</Label>
                                            <Select value={formData.role} onValueChange={v => setFormData({ ...formData, role: v })}>
                                                <SelectTrigger>
                                                    <SelectValue />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    <SelectItem value="User">User</SelectItem>
                                                    <SelectItem value="Admin">Admin</SelectItem>
                                                    <SelectItem value="Super Admin">Super Admin</SelectItem>
                                                </SelectContent>
                                            </Select>
                                        </div>
                                        <div className="space-y-2">
                                            <Label>Status</Label>
                                            <Select value={formData.status} onValueChange={v => setFormData({ ...formData, status: v })}>
                                                <SelectTrigger>
                                                    <SelectValue />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    <SelectItem value="active">Active</SelectItem>
                                                    <SelectItem value="inactive">Inactive</SelectItem>
                                                </SelectContent>
                                            </Select>
                                        </div>
                                    </div>
                                </div>
                            </TabsContent>

                            <TabsContent value="permissions" className="space-y-4 py-4">
                                <div className="space-y-4">
                                    <p className="text-sm text-muted-foreground">
                                        Control granular feature access for this user. These override role-based defaults.
                                    </p>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="flex items-center space-x-2 border p-4 rounded-lg">
                                            <Checkbox
                                                id="ai_access"
                                                checked={permissions.ai_access}
                                                onCheckedChange={(c) => setPermissions({ ...permissions, ai_access: c as boolean })}
                                            />
                                            <div className="grid gap-1.5 leading-none">
                                                <Label htmlFor="ai_access" className="cursor-pointer">AI Assistant Access</Label>
                                                <p className="text-xs text-muted-foreground">Access to specific AI Agents.</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center space-x-2 border p-4 rounded-lg">
                                            <Checkbox
                                                id="crm_access"
                                                checked={permissions.crm_access}
                                                onCheckedChange={(c) => setPermissions({ ...permissions, crm_access: c as boolean })}
                                            />
                                            <div className="grid gap-1.5 leading-none">
                                                <Label htmlFor="crm_access" className="cursor-pointer">CRM Module</Label>
                                                <p className="text-xs text-muted-foreground">Contacts & Deals management.</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center space-x-2 border p-4 rounded-lg">
                                            <Checkbox
                                                id="analytics_advanced"
                                                checked={permissions.analytics_advanced}
                                                onCheckedChange={(c) => setPermissions({ ...permissions, analytics_advanced: c as boolean })}
                                            />
                                            <div className="grid gap-1.5 leading-none">
                                                <Label htmlFor="analytics_advanced" className="cursor-pointer">Advanced Analytics</Label>
                                                <p className="text-xs text-muted-foreground">Full data export capabilities.</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center space-x-2 border p-4 rounded-lg">
                                            <Checkbox
                                                id="beta_features"
                                                checked={permissions.beta_features}
                                                onCheckedChange={(c) => setPermissions({ ...permissions, beta_features: c as boolean })}
                                            />
                                            <div className="grid gap-1.5 leading-none">
                                                <Label htmlFor="beta_features" className="cursor-pointer">Beta Features (Labs)</Label>
                                                <p className="text-xs text-muted-foreground">Experimental tools access.</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </TabsContent>

                            <TabsContent value="activity" className="py-4 h-[400px]">
                                <UserActivityLog userId={currentUser?.id} />
                            </TabsContent>
                        </Tabs>
                    </div>

                    <DialogFooter className="mt-4 border-t pt-4">
                        <Button variant="outline" onClick={() => setIsEditOpen(false)}>Close</Button>
                        <Button onClick={handleUpdate} disabled={isSubmitting}>
                            {isSubmitting ? "Saving..." : "Save Changes"}
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}
