'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { User, Shield, UserCheck, MoreVertical, Search, Filter, ShieldAlert } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

export default function GlobalUsersPage() {
    const users = [
        { id: '1', name: 'Alagiri S', email: 'alagiri@bizoholic.net', role: 'Super Admin', status: 'active', lastLogin: '2 mins ago' },
        { id: '2', name: 'John Doe', email: 'john@client.com', role: 'Admin', status: 'active', lastLogin: '1 hour ago' },
        { id: '3', name: 'Jane Smith', email: 'jane@client.com', role: 'User', status: 'inactive', lastLogin: '3 days ago' },
    ];

    return (
        <div className="p-6 space-y-6 bg-slate-50 dark:bg-slate-950 min-h-full">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Global User Management</h1>
                    <p className="text-muted-foreground">Manage all user accounts and roles across the entire platform.</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline">
                        <Filter className="mr-2 h-4 w-4" /> Filter
                    </Button>
                    <Button className="bg-blue-600 hover:bg-blue-700">
                        <UserCheck className="mr-2 h-4 w-4" /> Add User
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Users</CardTitle>
                        <User className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">1,234</div>
                        <p className="text-xs text-muted-foreground">+12% from last month</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Active Admins</CardTitle>
                        <Shield className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">12</div>
                        <p className="text-xs text-muted-foreground">Across all tenants</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Security Alerts</CardTitle>
                        <ShieldAlert className="h-4 w-4 text-red-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-red-600">0</div>
                        <p className="text-xs text-muted-foreground">Active warnings</p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle>Global Directory</CardTitle>
                            <CardDescription>Managed view of accounts and their cross-tenant access level.</CardDescription>
                        </div>
                        <div className="relative w-64">
                            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input placeholder="Search users..." className="pl-8" />
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
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
                            {users.map((u) => (
                                <TableRow key={u.id}>
                                    <TableCell>
                                        <div>
                                            <div className="font-bold">{u.name}</div>
                                            <div className="text-xs text-muted-foreground">{u.email}</div>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant="outline">{u.role}</Badge>
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex items-center gap-2">
                                            <div className={`w-2 h-2 rounded-full ${u.status === 'active' ? 'bg-green-500' : 'bg-gray-400'}`} />
                                            {u.status}
                                        </div>
                                    </TableCell>
                                    <TableCell className="text-muted-foreground">{u.lastLogin}</TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="icon">
                                            <MoreVertical className="h-4 w-4" />
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
