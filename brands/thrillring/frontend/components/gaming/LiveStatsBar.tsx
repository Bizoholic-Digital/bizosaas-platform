'use client';

import React from 'react';
import { GamingStats } from '@/lib/types/gaming';

interface LiveStatsBarProps {
    stats: GamingStats;
    loading: boolean;
}

export function LiveStatsBar({ stats, loading }: LiveStatsBarProps) {
    if (loading) {
        return (
            <div className="w-full h-24 bg-muted/20 animate-pulse rounded-lg"></div>
        )
    }

    const statItems = [
        { label: 'Active Players', value: stats.totalPlayers.toLocaleString(), icon: '🎮' },
        { label: 'Live Tournaments', value: stats.activeTournaments.toLocaleString(), icon: '🏆' },
        { label: 'Prize Pool', value: `$${stats.totalPrizePool.toLocaleString()}`, icon: '💰' },
        { label: 'Live Matches', value: stats.liveMatches.toLocaleString(), icon: '⚡' },
    ];

    return (
        <div className="w-full bg-card border-y border-border/50 py-6">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
                    {statItems.map((item) => (
                        <div key={item.label} className="flex flex-col items-center justify-center p-4 rounded-lg bg-background/50 hover:bg-muted/50 transition-colors">
                            <div className="text-2xl mb-2">{item.icon}</div>
                            <div className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-500 to-pink-500">
                                {item.value}
                            </div>
                            <div className="text-sm text-muted-foreground mt-1">{item.label}</div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
