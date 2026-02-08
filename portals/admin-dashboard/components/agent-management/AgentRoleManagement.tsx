'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
    Shield,
    User,
    Users,
    Briefcase,
    CheckCircle,
    XCircle,
    MoreVertical,
    Search,
    UserPlus,
    Crown
} from 'lucide-react';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface UserRole {
    id: string;
    name: string;
    email: string;
    role: 'client' | 'partner' | 'admin';
    accessLevel: 'read' | 'write' | 'maintainer' | 'owner';
    status: 'active' | 'suspended';
    lastActive: string;
}

// Mock data
const MOCK_USERS: UserRole[] = [
    {
        id: 'u1',
        name: 'Sarah Connor',
        email: 'sarah@skynet.com',
        role: 'admin',
        accessLevel: 'owner',
        status: 'active',
        lastActive: 'Now'
    },
    {
        id: 'u2',
        name: 'John Doe',
        email: 'john@example.com',
        role: 'client',
        accessLevel: 'read',
        status: 'active',
        lastActive: '2h ago'
    },
    {
        id: 'u3',
        name: 'Tech Solutions Inc.',
        email: 'admin@techsolutions.com',
        role: 'partner',
        accessLevel: 'maintainer',
        status: 'active',
        lastActive: '1d ago'
    }
];

export function AgentRoleManagement({ agentId }: { agentId: string }) {
    const [users, setUsers] = useState<UserRole[]>(MOCK_USERS);
    const [searchQuery, setSearchQuery] = useState('');

    const handleRoleChange = (userId: string, newRole: UserRole['role']) => {
        setUsers(users.map(u => u.id === userId ? { ...u, role: newRole } : u));
    };

    const handleAccessChange = (userId: string, newAccess: UserRole['accessLevel']) => {
        setUsers(users.map(u => u.id === userId ? { ...u, accessLevel: newAccess } : u));
    };

    const filteredUsers = users.filter(u =>
        u.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        u.email.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const getRoleBadgeColor = (role: string) => {
        switch (role) {
            case 'admin': return 'bg-purple-100 text-purple-800 border-purple-200';
            case 'partner': return 'bg-blue-100 text-blue-800 border-blue-200';
            case 'client': return 'bg-gray-100 text-gray-800 border-gray-200';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    return (
        <div className="space-y-6 max-w-4xl">
            {/* Header / Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-gray-500">Total Access</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center gap-2">
                            <Users className="w-5 h-5 text-blue-600" />
                            <span className="text-2xl font-bold">{users.length}</span>
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-gray-500">Partners</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center gap-2">
                            <Briefcase className="w-5 h-5 text-purple-600" />
                            <span className="text-2xl font-bold">{users.filter(u => u.role === 'partner').length}</span>
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-gray-500">Admins</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center gap-2">
                            <Shield className="w-5 h-5 text-red-600" />
                            <span className="text-2xl font-bold">{users.filter(u => u.role === 'admin').length}</span>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* User List */}
            <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                    <div>
                        <CardTitle>User Roles & Access</CardTitle>
                        <CardDescription>Manage who can access and control this agent</CardDescription>
                    </div>
                    <Button>
                        <UserPlus className="w-4 h-4 mr-2" />
                        Grant Access
                    </Button>
                </CardHeader>
                <CardContent>
                    <div className="mb-4">
                        <div className="relative">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
                            <Input
                                placeholder="Search users..."
                                className="pl-9"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className="space-y-4">
                        {filteredUsers.map((user) => (
                            <div key={user.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors">
                                <div className="flex items-center gap-4">
                                    <Avatar>
                                        <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.email}`} />
                                        <AvatarFallback>{user.name.substring(0, 2).toUpperCase()}</AvatarFallback>
                                    </Avatar>
                                    <div>
                                        <div className="flex items-center gap-2">
                                            <h4 className="font-semibold text-gray-900">{user.name}</h4>
                                            {user.accessLevel === 'owner' && (
                                                <Crown className="w-3 h-3 text-yellow-500" />
                                            )}
                                        </div>
                                        <p className="text-sm text-gray-500">{user.email}</p>
                                    </div>
                                </div>

                                <div className="flex items-center gap-4">
                                    <Badge variant="outline" className={getRoleBadgeColor(user.role)}>
                                        {user.role.toUpperCase()}
                                    </Badge>

                                    <div className="flex items-center text-sm text-gray-500">
                                        <span className="mr-2">Permission:</span>
                                        <Select
                                            value={user.accessLevel}
                                            onValueChange={(val: any) => handleAccessChange(user.id, val)}
                                        >
                                            <SelectTrigger className="w-[110px] h-8">
                                                <SelectValue />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="read">Read Only</SelectItem>
                                                <SelectItem value="write">Write</SelectItem>
                                                <SelectItem value="maintainer">Maintainer</SelectItem>
                                                <SelectItem value="owner">Owner</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>

                                    <DropdownMenu>
                                        <DropdownMenuTrigger asChild>
                                            <Button variant="ghost" size="icon">
                                                <MoreVertical className="w-4 h-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuLabel>Actions</DropdownMenuLabel>
                                            <DropdownMenuSeparator />
                                            <DropdownMenuItem onClick={() => handleRoleChange(user.id, 'partner')}>
                                                Promote to Partner
                                            </DropdownMenuItem>
                                            <DropdownMenuItem onClick={() => handleRoleChange(user.id, 'client')}>
                                                Demote to Client
                                            </DropdownMenuItem>
                                            <DropdownMenuSeparator />
                                            <DropdownMenuItem className="text-red-600">
                                                Revoke Access
                                            </DropdownMenuItem>
                                        </DropdownMenuContent>
                                    </DropdownMenu>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
