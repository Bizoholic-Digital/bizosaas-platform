'use client';

import React from 'react';
import Image from 'next/image';
import { Tournament } from '@/lib/types/gaming';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge'; // Badge exists in components/ui

// Fallback Badge if not imported
const FallbackBadge = ({ children, className }: { children: React.ReactNode, className?: string }) => (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border border-transparent bg-primary text-primary-foreground hover:bg-primary/80 ${className || ''}`}>
        {children}
    </span>
);

interface TournamentCardProps {
    tournament: Tournament;
}

export function TournamentCard({ tournament }: TournamentCardProps) {
    // Use existing Badge or Fallback
    const StatusBadge = FallbackBadge;

    return (
        <div className="group relative overflow-hidden rounded-xl border bg-card text-card-foreground shadow transition-all hover:shadow-lg">
            <div className="aspect-video w-full overflow-hidden bg-muted">
                {tournament.image_url ? (
                    <img src={tournament.image_url} alt={tournament.title} className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105" />
                ) : (
                    <div className="flex h-full items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900 text-gray-400">
                        <span className="text-4xl">🏆</span>
                    </div>
                )}
                <div className="absolute top-2 right-2">
                    <StatusBadge className={tournament.status === 'live' ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-500 hover:bg-blue-600'}>
                        {tournament.status === 'live' ? 'LIVE NOW' : tournament.status.replace('_', ' ').toUpperCase()}
                    </StatusBadge>
                </div>
            </div>

            <div className="p-6">
                <h3 className="text-xl font-bold leading-none tracking-tight mb-2">{tournament.title}</h3>
                <p className="text-sm text-muted-foreground mb-4 line-clamp-2">{tournament.description}</p>

                <div className="flex justify-between items-center text-sm mb-4">
                    <div className="flex flex-col">
                        <span className="text-muted-foreground">Prize Pool</span>
                        <span className="font-semibold text-green-500">${tournament.prize_pool.toLocaleString()}</span>
                    </div>
                    <div className="flex flex-col items-end">
                        <span className="text-muted-foreground">Players</span>
                        <span className="font-semibold">{tournament.participants}/{tournament.max_participants}</span>
                    </div>
                </div>

                <div className="flex gap-2">
                    <Button className="w-full bg-primary hover:bg-primary/90">
                        {tournament.status === 'live' ? 'Watch Stream' : 'Register Now'}
                    </Button>
                </div>
            </div>
        </div>
    );
}
