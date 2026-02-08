'use client';

import React from 'react';
import { Coins, TrendingUp, ArrowUpRight, History } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

interface CreditWidgetProps {
    balance: number;
    used: number;
    available: number;
}

export function CreditBalanceWidget({ balance, used, available }: CreditWidgetProps) {
    return (
        <Card className="overflow-hidden border-none shadow-md bg-gradient-to-br from-slate-900 to-indigo-950 text-white">
            <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-400 flex items-center justify-between">
                    Credit Balance
                    <Coins className="w-4 h-4 text-emerald-400" />
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex flex-col space-y-4">
                    <div>
                        <div className="text-4xl font-black tracking-tight">{available.toLocaleString()}</div>
                        <p className="text-xs text-slate-400 mt-1">Available Bizo Credits</p>
                    </div>

                    <div className="grid grid-cols-2 gap-4 pt-2">
                        <div className="space-y-1">
                            <p className="text-[10px] uppercase font-bold text-slate-500">Total Earned</p>
                            <p className="text-sm font-bold text-emerald-400">+{balance.toLocaleString()}</p>
                        </div>
                        <div className="space-y-1">
                            <p className="text-[10px] uppercase font-bold text-slate-500">Total Spent</p>
                            <p className="text-sm font-bold text-rose-400">-{used.toLocaleString()}</p>
                        </div>
                    </div>

                    <div className="flex gap-2 pt-2">
                        <Button asChild size="sm" className="flex-1 bg-indigo-600 hover:bg-indigo-500 border-none">
                            <Link href="/billing/buy-credits">
                                <ArrowUpRight className="w-3 h-3 mr-1" /> Buy Credits
                            </Link>
                        </Button>
                        <Button asChild variant="outline" size="sm" className="flex-1 bg-white/5 border-white/10 hover:bg-white/10 text-white">
                            <Link href="/billing/credits">
                                <History className="w-3 h-3 mr-1" /> History
                            </Link>
                        </Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
