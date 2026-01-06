'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
    Users,
    TrendingUp,
    AlertCircle,
    Search,
    MoreVertical,
    Building2,
    ArrowUpRight,
    ArrowRight,
    LayoutDashboard
} from 'lucide-react';
import { useRouter } from 'next/navigation';

interface Client {
    id: string;
    name: string;
    email: string;
    plan: 'starter' | 'pro' | 'enterprise';
    status: 'active' | 'warning' | 'churned';
    revenue: number;
    agentsActive: number;
    healthScore: number;
    lastActive: string;
}

const MOCK_CLIENTS: Client[] = [
    {
        id: 'c1',
        name: 'Acme Corp',
        email: 'contact@acme.com',
        plan: 'enterprise',
        status: 'active',
        revenue: 4500,
        agentsActive: 12,
        healthScore: 98,
        lastActive: '10m ago'
    },
    {
        id: 'c2',
        name: 'TechStart Inc (Managed)',
        email: 'admin@techstart.io',
        plan: 'pro',
        status: 'warning',
        revenue: 1200,
        agentsActive: 5,
        healthScore: 72,
        lastActive: '2d ago'
    },
    {
        id: 'c3',
        name: 'Local Bakery',
        email: 'owner@bakery.local',
        plan: 'starter',
        status: 'active',
        revenue: 450,
        agentsActive: 2,
        healthScore: 95,
        lastActive: '5h ago'
    }
];

export default function PartnerDashboard() {
    const router = useRouter();
    const [clients, setClients] = useState<Client[]>(MOCK_CLIENTS);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedClient, setSelectedClient] = useState<string | null>(null);

    const filteredClients = clients.filter(c =>
        c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.email.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const totalRevenue = clients.reduce((acc, c) => acc + c.revenue, 0);
    const totalAgents = clients.reduce((acc, c) => acc + c.agentsActive, 0);
    const avgHealth = Math.round(clients.reduce((acc, c) => acc + c.healthScore, 0) / clients.length);

    const handleSwitchContext = (clientId: string) => {
        setSelectedClient(clientId);
        // In a real app, this would update a global context or auth session
        console.log(`Switching context to client: ${clientId}`);
        // router.push(`/dashboard?context=${clientId}`);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Partner Dashboard</h1>
                    <p className="text-gray-500">Manage your clients and oversee their AI operations</p>
                </div>
                <div className="flex gap-3">
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button variant="outline" className="w-[200px] justify-between">
                                <span className="flex items-center gap-2">
                                    <Building2 className="w-4 h-4" />
                                    {selectedClient ? clients.find(c => c.id === selectedClient)?.name : 'Global View'}
                                </span>
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent className="w-[200px]">
                            <DropdownMenuLabel>Switch Context</DropdownMenuLabel>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem onClick={() => setSelectedClient(null)}>
                                <LayoutDashboard className="w-4 h-4 mr-2" />
                                Global View
                            </DropdownMenuItem>
                            {clients.map(client => (
                                <DropdownMenuItem key={client.id} onClick={() => handleSwitchContext(client.id)}>
                                    <span className="truncate">{client.name}</span>
                                </DropdownMenuItem>
                            ))}
                        </DropdownMenuContent>
                    </DropdownMenu>
                    <Button>
                        <Users className="w-4 h-4 mr-2" />
                        Add Client
                    </Button>
                </div>
            </div>

            {/* Aggregated Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
                        <TrendingUp className="h-4 w-4 text-green-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">${totalRevenue.toLocaleString()}</div>
                        <p className="text-xs text-muted-foreground">+20.1% from last month</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
                        <Users className="h-4 w-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{totalAgents}</div>
                        <p className="text-xs text-muted-foreground">Across {clients.length} clients</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Avg Health Score</CardTitle>
                        <AlertCircle className="h-4 w-4 text-orange-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{avgHealth}/100</div>
                        <p className="text-xs text-muted-foreground">2 clients need attention</p>
                    </CardContent>
                </Card>
            </div>

            {/* Clients Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Managed Clients</CardTitle>
                    <CardDescription>Overview of all client accounts under your partnership</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="mb-4">
                        <div className="relative max-w-sm">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
                            <Input
                                placeholder="Search clients..."
                                className="pl-9"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Client</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Plan</TableHead>
                                    <TableHead className="text-right">Revenue</TableHead>
                                    <TableHead className="text-center">Health</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredClients.map((client) => (
                                    <TableRow key={client.id} className="hover:bg-muted/50">
                                        <TableCell>
                                            <div className="flex items-center gap-3">
                                                <Avatar className="h-9 w-9">
                                                    <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${client.name}`} />
                                                    <AvatarFallback>CL</AvatarFallback>
                                                </Avatar>
                                                <div>
                                                    <div className="font-medium">{client.name}</div>
                                                    <div className="text-xs text-muted-foreground">{client.email}</div>
                                                </div>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="secondary" className={
                                                client.status === 'active' ? 'bg-green-100 text-green-700' :
                                                    client.status === 'warning' ? 'bg-yellow-100 text-yellow-700' :
                                                        'bg-red-100 text-red-700'
                                            }>
                                                {client.status.toUpperCase()}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="outline">{client.plan.toUpperCase()}</Badge>
                                        </TableCell>
                                        <TableCell className="text-right font-medium">
                                            ${client.revenue.toLocaleString()}
                                        </TableCell>
                                        <TableCell className="text-center">
                                            <div className={`font-bold ${client.healthScore >= 90 ? 'text-green-600' :
                                                    client.healthScore >= 70 ? 'text-yellow-600' :
                                                        'text-red-600'
                                                }`}>
                                                {client.healthScore}%
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button variant="ghost" size="sm" onClick={() => handleSwitchContext(client.id)}>
                                                    Manage <ArrowRight className="w-4 h-4 ml-1" />
                                                </Button>
                                                <DropdownMenu>
                                                    <DropdownMenuTrigger asChild>
                                                        <Button variant="ghost" size="icon">
                                                            <MoreVertical className="w-4 h-4" />
                                                        </Button>
                                                    </DropdownMenuTrigger>
                                                    <DropdownMenuContent align="end">
                                                        <DropdownMenuItem>View Details</DropdownMenuItem>
                                                        <DropdownMenuItem>Billing settings</DropdownMenuItem>
                                                        <DropdownMenuSeparator />
                                                        <DropdownMenuItem className="text-red-600">Suspend Account</DropdownMenuItem>
                                                    </DropdownMenuContent>
                                                </DropdownMenu>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
