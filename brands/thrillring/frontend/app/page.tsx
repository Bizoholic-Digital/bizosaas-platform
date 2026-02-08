'use client';

import React from 'react';
import { useQuery, gql } from 'urql';

// Components
import { HeroSection } from '@/components/gaming/HeroSection';
import { LiveStatsBar } from '@/components/gaming/LiveStatsBar';
import { TournamentCard } from '@/components/gaming/TournamentCard';
import { GameGrid } from '@/components/gaming/GameGrid';
import { Leaderboard } from '@/components/gaming/Leaderboard';
import { NewsSection } from '@/components/gaming/NewsSection';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

// Hooks
import { useGamingStats, useTournaments, usePopularGames } from '@/lib/hooks/useGamingData';

const GET_CMS_POSTS = gql`
  query GetCmsPosts($tenantId: String!) {
    cmsPosts(tenantId: $tenantId) {
      id
      title
      slug
      excerpt
      publishedAt
      coverImage
    }
  }
`;

export default function HomePage() {
  // 1. Gaming Data Hooks
  const { stats, loading: statsLoading } = useGamingStats();
  const { tournaments, loading: tournamentsLoading } = useTournaments('featured', 'all', 3);
  const { games, loading: gamesLoading } = usePopularGames(6);

  // 2. CMS News Data
  const [newsResult] = useQuery({
    query: GET_CMS_POSTS,
    variables: { tenantId: 'thrillring' },
  });
  const { data: newsData, fetching: newsLoading } = newsResult;


  return (
    <main className="min-h-screen bg-background">

      {/* Hero Section */}
      <HeroSection />

      {/* Live Stats Bar */}
      <LiveStatsBar stats={stats} loading={statsLoading} />

      {/* Featured Tournaments */}
      <section className="py-16 px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="flex justify-between items-end mb-8">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Featured Tournaments</h2>
            <p className="text-muted-foreground mt-2">Compete for glory and real prizes in our curated events.</p>
          </div>
          <Link href="/tournaments">
            <Button variant="ghost" className="hidden sm:flex">View All Tournaments &rarr;</Button>
          </Link>
        </div>

        {tournamentsLoading ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3].map(i => <div key={i} className="h-80 bg-muted/20 animate-pulse rounded-xl"></div>)}
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {tournaments.map((tournament) => (
              <TournamentCard key={tournament.id} tournament={tournament} />
            ))}
          </div>
        )}

        <div className="mt-8 text-center sm:hidden">
          <Link href="/tournaments">
            <Button variant="outline">View All Tournaments</Button>
          </Link>
        </div>
      </section>

      {/* Popular Games */}
      <section className="py-16 bg-muted/30">
        <div className="px-6 lg:px-8 max-w-7xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight mb-8">Popular Games</h2>
          <GameGrid games={games} loading={gamesLoading} />
        </div>
      </section>

      {/* Leaderboard & Community Split */}
      <section className="py-16 px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">

          {/* Leaderboard (2/3 width) */}
          <div className="lg:col-span-2">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Global Rankings</h2>
              <Button variant="outline" size="sm">View Full Standings</Button>
            </div>
            <Leaderboard />
          </div>

          {/* Community / CTA (1/3 width) */}
          <div className="lg:col-span-1 flex flex-col gap-6">
            <div className="rounded-xl border bg-card p-6">
              <h3 className="text-xl font-bold mb-2">Join the Community</h3>
              <p className="text-muted-foreground mb-4 text-sm">Connect with thousands of other players on our Discord server. Find teammates, scrims, and more.</p>
              <Button className="w-full bg-[#5865F2] hover:bg-[#4752C4] text-white">
                Join Discord
              </Button>
            </div>

            <div className="rounded-xl border bg-gradient-to-br from-indigo-900 to-purple-900 p-6 text-white">
              <h3 className="text-xl font-bold mb-2">Create Your Guild</h3>
              <p className="text-indigo-200 mb-4 text-sm">Start your own team, manage rosters, and challenge others.</p>
              <Button variant="secondary" className="w-full">
                Start a Guild
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Gaming News */}
      <section className="py-16 bg-muted/30">
        <div className="px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="flex justify-between items-end mb-8">
            <h2 className="text-2xl font-bold">Latest News</h2>
          </div>
          {newsLoading ? (
            <div className="grid gap-8 md:grid-cols-3">
              {[1, 2, 3].map(i => <div key={i} className="h-64 bg-muted animate-pulse rounded-xl"></div>)}
            </div>
          ) : (
            <NewsSection posts={newsData?.cmsPosts || []} />
          )}
        </div>
      </section>

    </main>
  );
}