'use client';

import React, { useState } from 'react';
import { CreditBalanceWidget } from '@/components/billing/CreditBalanceWidget';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { useSetHeader } from '@/lib/contexts/HeaderContext';
import { ArrowDownLeft, ArrowUpRight, ShoppingCart, RefreshCcw } from 'lucide-react';
import { cn } from '@/lib/utils';

// Mock Data matching the template's structure
const MOCK_TRANSACTIONS = [
    { id: 'TX-101', type: 'earned', amount: 50, description: 'Added new business listing', date: '2023-11-15 14:30', status: 'completed' },
    { id: 'TX-102', type: 'spent', amount: 200, description: 'Promoted listing: Rolex Villas', date: '2023-11-14 09:15', status: 'completed' },
    { id: 'TX-103', type: 'purchased', amount: 1000, description: 'Starter Credit Pack Purchase', date: '2023-11-10 18:45', status: 'completed' },
    { id: 'TX-104', type: 'earned', amount: 25, description: 'Completed profile onboarding', date: '2023-11-08 11:20', status: 'completed' },
    { id: 'TX-105', type: 'spent', amount: 50, description: 'SEO AI Report Generation', date: '2023-11-05 16:10', status: 'completed' },
    { id: 'TX-106', type: 'refunded', amount: 50, description: 'Refund: Failed AI Task', date: '2023-11-04 10:05', status: 'completed' },
];

export default function CreditsHistoryPage() {
    useSetHeader("Credit History", "View your points earnings and usage across the platform.");
    const [transactions] = useState(MOCK_TRANSACTIONS);

    const getIcon = (type: string) => {
        switch (type) {
            case 'earned': return <ArrowDownLeft className="w-4 h-4 text-emerald-500" />;
            case 'spent': return <ArrowUpRight className="w-4 h-4 text-rose-500" />;
            case 'purchased': return <ShoppingCart className="w-4 h-4 text-blue-500" />;
            case 'refunded': return <RefreshCcw className="w-4 h-4 text-amber-500" />;
            default: return null;
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'completed': return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400';
            case 'pending': return 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400';
            case 'failed': return 'bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-400';
            default: return '';
        }
    };

    return (
        <div className="p-6 space-y-6 max-w-7xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1">
                    <CreditBalanceWidget balance={1125} used={250} available={875} />

                    <Card className="mt-6 border-none shadow-sm bg-blue-50/50 dark:bg-blue-900/10">
                        <CardHeader>
                            <CardTitle className="text-sm">How to earn credits?</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-3">
                            {[
                                { task: 'Add a new listing', reward: '50 pts' },
                                { task: 'Review another business', reward: '10 pts' },
                                { task: 'Refer a new client', reward: '500 pts' },
                                { task: 'Complete daily check-in', reward: '5 pts' }
                            ].map((item, i) => (
                                <div key={i} className="flex justify-between items-center text-sm">
                                    <span className="text-slate-600 dark:text-slate-400">{item.task}</span>
                                    <Badge variant="secondary" className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 border-none font-bold">
                                        {item.reward}
                                    </Badge>
                                </div>
                            ))}
                        </CardContent>
                    </Card>
                </div>

                <div className="lg:col-span-2">
                    <Card className="border-none shadow-sm h-full">
                        <CardHeader className="flex flex-row items-center justify-between">
                            <CardTitle>Transaction History</CardTitle>
                            <div className="flex gap-2">
                                <Badge variant="outline" className="cursor-pointer hover:bg-slate-100">All</Badge>
                                <Badge variant="outline" className="cursor-pointer hover:bg-slate-100">Earned</Badge>
                                <Badge variant="outline" className="cursor-pointer hover:bg-slate-100">Spent</Badge>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <Table>
                                <TableHeader>
                                    <TableRow className="bg-slate-50/50 dark:bg-slate-900/50 border-none">
                                        <TableHead className="rounded-l-lg">Description</TableHead>
                                        <TableHead>Type</TableHead>
                                        <TableHead>Amount</TableHead>
                                        <TableHead>Date</TableHead>
                                        <TableHead className="rounded-r-lg text-right">Status</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {transactions.map((tx) => (
                                        <TableRow key={tx.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-950/50 border-slate-100 dark:border-slate-800">
                                            <TableCell className="font-medium">
                                                <div className="flex flex-col">
                                                    <span>{tx.description}</span>
                                                    <span className="text-[10px] text-slate-400 uppercase font-mono tracking-tighter">{tx.id}</span>
                                                </div>
                                            </TableCell>
                                            <TableCell>
                                                <div className="flex items-center gap-2 capitalize text-xs">
                                                    {getIcon(tx.type)}
                                                    {tx.type}
                                                </div>
                                            </TableCell>
                                            <TableCell>
                                                <span className={cn(
                                                    "font-bold",
                                                    tx.type === 'earned' || tx.type === 'purchased' || tx.type === 'refunded'
                                                        ? "text-emerald-600 dark:text-emerald-500"
                                                        : "text-rose-600 dark:text-rose-500"
                                                )}>
                                                    {tx.type === 'spent' ? '-' : '+'}{tx.amount}
                                                </span>
                                            </TableCell>
                                            <TableCell className="text-xs text-slate-500">
                                                {tx.date}
                                            </TableCell>
                                            <TableCell className="text-right">
                                                <Badge className={cn("border-none text-[10px] uppercase font-bold", getStatusColor(tx.status))}>
                                                    {tx.status}
                                                </Badge>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
