import { useLeaderboard } from '@/lib/hooks/useGamingData';

export function Leaderboard({ gameSlug = 'chess' }: { gameSlug?: string }) {
    const { leaderboard, loading, error } = useLeaderboard(gameSlug);

    if (loading) return <div className="p-8 text-center">Loading Leaderboard...</div>;
    if (error) return <div className="p-8 text-center text-red-500">Error: {error}</div>;

    const data = leaderboard.length > 0 ? leaderboard : [
        { rank: 1, user_id: '1', mmr: 1200, wins: 0, losses: 0, avatar: '👑' }, // Fallback if empty but success
    ];

    return (
        <div className="rounded-xl border bg-card">
            <div className="p-6 border-b">
                <h3 className="text-xl font-bold">Top Players</h3>
                <p className="text-sm text-muted-foreground">Global rankings for Season 2</p>
            </div>
            <div className="relative w-full overflow-auto">
                <table className="w-full caption-bottom text-sm">
                    <thead className="[&_tr]:border-b">
                        <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                            <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground w-[80px]">Rank</th>
                            <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Player</th>
                            <th className="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Wins</th>
                            <th className="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Points</th>
                            <th className="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Earnings</th>
                        </tr>
                    </thead>
                    <tbody className="[&_tr:last-child]:border-0">
                        {data.map((player: any) => (
                            <tr key={player.rank || player.user_id} className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                                <td className="p-4 align-middle font-medium">{player.avatar || '👤'} #{player.rank || '-'}</td>
                                <td className="p-4 align-middle font-bold text-foreground">{player.name}</td>
                                <td className="p-4 align-middle text-right">{player.wins}</td>
                                <td className="p-4 align-middle text-right">{player.points.toLocaleString()}</td>
                                <td className="p-4 align-middle text-right text-green-500">${player.earnings.toLocaleString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
