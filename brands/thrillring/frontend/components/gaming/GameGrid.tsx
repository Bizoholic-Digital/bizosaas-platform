'use client';

import React from 'react';
import { Game } from '@/lib/types/gaming';
import { Card, CardContent } from '@/lib/ui/card'; // Assuming Card components exist

// Fallbacks if UI components don't exist
const FallbackCard = ({ children, className }: { children: React.ReactNode, className?: string }) => <div className={`rounded-lg border bg-card text-card-foreground shadow-sm ${className}`}>{children}</div>
const FallbackCardContent = ({ children, className }: { children: React.ReactNode, className?: string }) => <div className={`p-6 ${className}`}>{children}</div>


interface GameGridProps {
    games: Game[];
    loading?: boolean;
}

export function GameGrid({ games, loading }: GameGridProps) {
    if (loading) {
        return <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map(i => <div key={i} className="aspect-[3/4] bg-muted animate-pulse rounded-lg" />)}
        </div>
    }

    const GameCardWrapper = FallbackCard;
    const GameContent = FallbackCardContent;

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {games.map((game) => (
                <GameCardWrapper key={game.id} className="group overflow-hidden relative border-0 bg-transparent shadow-none hover:shadow-xl transition-all">
                    <div className="aspect-[3/4] w-full overflow-hidden rounded-lg bg-gray-900 relative">
                        {game.image_url ? (
                            <img src={game.image_url} alt={game.name} className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-110 opacity-80 group-hover:opacity-100" />
                        ) : (
                            <div className="h-full w-full flex items-center justify-center bg-gray-800 text-gray-500">{game.name[0]}</div>
                        )}

                        <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent p-4 flex flex-col justify-end opacity-100">
                            <h4 className="font-bold text-white text-lg leading-tight">{game.name}</h4>
                            <p className="text-xs text-gray-300 mt-1">{game.active_players?.toLocaleString()} players</p>
                        </div>
                    </div>
                </GameCardWrapper>
            ))}
        </div>
    );
}
