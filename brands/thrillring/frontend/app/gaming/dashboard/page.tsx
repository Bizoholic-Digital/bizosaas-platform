'use client';

import React, { useState } from 'react';
import { HeroSection } from '@/components/gaming/HeroSection';
import { GameGrid } from '@/components/gaming/GameGrid';
import { Leaderboard } from '@/components/gaming/Leaderboard';
import { TournamentBracket } from '@/components/gaming/TournamentBracket';
import { LiveStatsBar } from '@/components/gaming/LiveStatsBar';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Trophy, Users, BarChart3, Presentation } from 'lucide-react';
import { usePopularGames, useGamingStats } from '@/lib/hooks/useGamingData';

// Mocked matches for the bracket demonstration
const MOCK_MATCHES: any[] = [
    {
        id: 1,
        nextMatchId: 3,
        tournamentRoundText: 'Round 1',
        startTime: '2026-02-10',
        state: 'DONE',
        participants: [
            { id: 'p1', resultText: '2', isWinner: true, status: null, name: 'ProGamer123' },
            { id: 'p2', resultText: '1', isWinner: false, status: null, name: 'ShadowNinja' }
        ]
    },
    {
        id: 2,
        nextMatchId: 3,
        tournamentRoundText: 'Round 1',
        startTime: '2026-02-10',
        state: 'DONE',
        participants: [
            { id: 'p3', resultText: '0', isWinner: false, status: null, name: 'EliteSniper' },
            { id: 'p4', resultText: '2', isWinner: true, status: null, name: 'TacticalAce' }
        ]
    },
    {
        id: 3,
        nextMatchId: null,
        tournamentRoundText: 'Final',
        startTime: '2026-02-12',
        state: 'SCHEDULED',
        participants: [
            { id: 'p1', resultText: null, isWinner: false, status: null, name: 'ProGamer123' },
            { id: 'p4', resultText: null, isWinner: false, status: null, name: 'TacticalAce' }
        ]
    }
];

export default function GamingDashboard() {
    const [activeGame, setActiveGame] = useState('chess');
    const { stats, loading: statsLoading } = useGamingStats();
    const { games, loading: gamesLoading } = usePopularGames(12);

    return (
        <div className="min-h-screen bg-background pb-12">
            <LiveStatsBar stats={stats} loading={statsLoading} />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
                <HeroSection />

                <Tabs defaultValue="tournaments" className="w-full">
                    <TabsList className="grid w-full grid-cols-4 max-w-2xl mx-auto mb-8">
                        <TabsTrigger value="tournaments" className="flex gap-2">
                            <Trophy size={16} /> Tournaments
                        </TabsTrigger>
                        <TabsTrigger value="leaderboard" className="flex gap-2">
                            <BarChart3 size={16} /> Ranking
                        </TabsTrigger>
                        <TabsTrigger value="games" className="flex gap-2">
                            <Presentation size={16} /> Games
                        </TabsTrigger>
                        <TabsTrigger value="players" className="flex gap-2">
                            <Users size={16} /> Players
                        </TabsTrigger>
                    </TabsList>

                    <TabsContent value="tournaments" className="space-y-8">
                        <section className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                            <TournamentBracket matches={MOCK_MATCHES} />
                        </section>
                        <section>
                            <h2 className="text-2xl font-bold mb-4">Upcoming Events</h2>
                            <GameGrid games={games} loading={gamesLoading} />
                        </section>
                    </TabsContent>

                    <TabsContent value="leaderboard">
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                            <div className="lg:col-span-2">
                                <Leaderboard gameSlug={activeGame} />
                            </div>
                            <div className="space-y-6">
                                <div className="p-6 rounded-xl border bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border-indigo-500/20">
                                    <h4 className="font-bold mb-2 flex items-center gap-2">
                                        <Trophy size={18} className="text-yellow-500" />
                                        Your Standing
                                    </h4>
                                    <p className="text-sm text-slate-400 mb-4">Complete 5 placement matches to see your rank.</p>
                                    <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                                        <div className="h-full bg-indigo-500 w-[60%]" />
                                    </div>
                                    <p className="text-right text-xs mt-1 text-slate-500">3/5 Matchs</p>
                                </div>
                            </div>
                        </div>
                    </TabsContent>

                    <TabsContent value="games">
                        <GameGrid games={games} loading={gamesLoading} />
                    </TabsContent>

                    <TabsContent value="players">
                        <div className="flex h-64 items-center justify-center rounded-xl border bg-card text-muted-foreground italic">
                            Player social features coming soon in Season 3
                        </div>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
}
