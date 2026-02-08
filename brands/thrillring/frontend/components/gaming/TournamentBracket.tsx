'use client';

import React from 'react';
import { Bracket, Seed, SeedItem, SeedTeam, SeedTime } from '@g-loot/react-tournament-brackets';

interface Team {
    id: string | number;
    name: string;
}

interface Match {
    id: number | string;
    nextMatchId: number | string | null;
    tournamentRoundText: string;
    startTime: string;
    state: 'DONE' | 'SCHEDULED' | 'WALK_OVER' | 'NO_SHOW' | 'RUNNING';
    participants: {
        id: string | number;
        resultText: string | null;
        isWinner: boolean;
        status: string | null;
        name: string;
    }[];
}

interface TournamentBracketProps {
    matches: Match[];
}

export function TournamentBracket({ matches }: TournamentBracketProps) {
    if (!matches || matches.length === 0) {
        return (
            <div className="flex h-64 items-center justify-center rounded-xl border bg-card text-muted-foreground">
                No bracket data available
            </div>
        );
    }

    return (
        <div className="rounded-xl border bg-card p-6 overflow-x-auto">
            <h3 className="text-xl font-bold mb-6">Tournament Bracket</h3>
            <div className="min-w-[800px]">
                <Bracket
                    matches={matches}
                    renderSeedComponent={CustomSeed}
                    mobileBreakpoint={768}
                />
            </div>
        </div>
    );
}

const CustomSeed = ({ seed, breakpoint, roundIndex, seedIndex }: any) => {
    return (
        <Seed mobileBreakpoint={breakpoint} style={{ fontSize: 12 }}>
            <SeedItem style={{ backgroundColor: '#1e293b', borderRadius: '8px', border: '1px solid #334155' }}>
                <div>
                    <SeedTeam
                        style={{
                            color: seed.teams[0]?.isWinner ? '#22c55e' : '#94a3b8',
                            fontWeight: seed.teams[0]?.isWinner ? 'bold' : 'normal'
                        }}
                    >
                        {seed.teams[0]?.name || 'TBD'}
                    </SeedTeam>
                    <div style={{ height: '1px', backgroundColor: '#334155' }} />
                    <SeedTeam
                        style={{
                            color: seed.teams[1]?.isWinner ? '#22c55e' : '#94a3b8',
                            fontWeight: seed.teams[1]?.isWinner ? 'bold' : 'normal'
                        }}
                    >
                        {seed.teams[1]?.name || 'TBD'}
                    </SeedTeam>
                </div>
            </SeedItem>
            <SeedTime style={{ color: '#64748b', marginTop: '4px' }}>
                {seed.date}
            </SeedTime>
        </Seed>
    );
};
