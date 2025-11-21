'use client'

// Force dynamic rendering to prevent Next.js from pre-rendering this page
export const dynamic = 'force-dynamic'

import React from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/lib/ui/card'
import { Button } from '@/lib/ui/button'
import {
  Trophy,
  Users,
  Calendar,
  TrendingUp,
  Play,
  Award,
  Target,
  Zap,
  Star,
  ChevronRight,
  Clock,
  MapPin,
  DollarSign
} from 'lucide-react'
import { usePopularGames, useTournaments, useGamingStats } from '@/lib/hooks/useGamingData'

function formatNumber(num: number): string {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`
  } else if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`
  }
  return num.toString()
}

function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount)
}

export default function ThrillRingHomePage() {
  const { games, loading: gamesLoading } = usePopularGames(6)
  const { tournaments, loading: tournamentsLoading } = useTournaments('all', 'all', 3)
  const { stats, loading: statsLoading } = useGamingStats()

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="relative z-50 border-b border-gray-800/50 bg-black/20 backdrop-blur-md">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
              className="flex items-center space-x-2"
            >
              <div className="bg-purple-600 p-2 rounded-lg">
                <Trophy className="h-6 w-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-white">ThrillRing</span>
            </motion.div>

            <nav className="hidden md:flex items-center space-x-8">
              <Link href="/tournaments" className="text-gray-300 hover:text-white transition-colors">
                Tournaments
              </Link>
              <Link href="/players" className="text-gray-300 hover:text-white transition-colors">
                Players
              </Link>
              <Link href="/leaderboards" className="text-gray-300 hover:text-white transition-colors">
                Leaderboards
              </Link>
              <Link href="/live-streams" className="text-gray-300 hover:text-white transition-colors">
                Live
              </Link>
              <Link href="/community" className="text-gray-300 hover:text-white transition-colors">
                Community
              </Link>
            </nav>

            <div className="flex items-center space-x-4">
              <Button variant="outline" className="border-purple-500 text-purple-400 hover:bg-purple-500 hover:text-white">
                Sign In
              </Button>
              <Button className="bg-purple-600 hover:bg-purple-700">
                Join Now
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 overflow-hidden">
        <div className="absolute inset-0 bg-purple-900/20" />
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center max-w-4xl mx-auto">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-5xl md:text-7xl font-bold text-white mb-6"
            >
              Welcome to the
              <span className="text-purple-400">
                {" "}Ultimate Gaming Arena
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl text-gray-300 mb-8 leading-relaxed"
            >
              Join millions of gamers in epic tournaments, climb leaderboards, and experience
              the thrill of competitive gaming like never before.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
            >
              <Button size="lg" className="bg-purple-600 hover:bg-purple-700 text-lg px-8 py-4">
                <Play className="mr-2 h-5 w-5" />
                Start Playing
              </Button>
              <Button size="lg" variant="outline" className="border-gray-600 text-gray-300 hover:bg-gray-700 text-lg px-8 py-4">
                Watch Live
                <ChevronRight className="ml-2 h-5 w-5" />
              </Button>
            </motion.div>
          </div>
        </div>

        {/* Floating Gaming Elements */}
        <div className="absolute top-20 left-10 animate-bounce">
          <Trophy className="h-8 w-8 text-yellow-400 opacity-60" />
        </div>
        <div className="absolute top-40 right-10 animate-pulse">
          <Target className="h-10 w-10 text-purple-400 opacity-60" />
        </div>
        <div className="absolute bottom-20 left-20 animate-spin">
          <Star className="h-6 w-6 text-pink-400 opacity-60" />
        </div>
      </section>

      {/* Stats Section - Dynamic Data */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { 
                icon: Users, 
                label: 'Active Players', 
                value: statsLoading ? 'Loading...': `${formatNumber(stats.totalPlayers)}+`, 
                color: 'text-blue-400' 
              },
              { 
                icon: Trophy, 
                label: 'Tournaments', 
                value: statsLoading ? 'Loading...': `${stats.activeTournaments}+`, 
                color: 'text-yellow-400' 
              },
              { 
                icon: Award, 
                label: 'Prize Pool', 
                value: statsLoading ? 'Loading...': formatCurrency(stats.totalPrizePool), 
                color: 'text-green-400' 
              },
              { 
                icon: Zap, 
                label: 'Live Matches', 
                value: statsLoading ? 'Loading...': `${stats.liveMatches}+`, 
                color: 'text-purple-400' 
              }
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card className="bg-black/40 border-gray-800 backdrop-blur-sm hover:bg-black/60 transition-colors">
                  <CardContent className="p-6 text-center">
                    <stat.icon className={`h-8 w-8 mx-auto mb-4 ${stat.color}`} />
                    <div className="text-3xl font-bold text-white mb-2">{stat.value}</div>
                    <div className="text-gray-400">{stat.label}</div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Tournaments - Dynamic Data */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-white mb-4">Featured Tournaments</h2>
            <p className="text-gray-400 text-lg">Join the biggest competitions in gaming</p>
          </div>

          {tournamentsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[1, 2, 3].map((i) => (
                <Card key={i} className="bg-black/40 border-gray-800 backdrop-blur-sm">
                  <div className="aspect-video bg-gray-800 animate-pulse" />
                  <CardHeader>
                    <div className="h-6 bg-gray-700 rounded animate-pulse" />
                    <div className="h-4 bg-gray-700 rounded animate-pulse w-3/4" />
                  </CardHeader>
                  <CardContent>
                    <div className="h-10 bg-gray-700 rounded animate-pulse" />
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {tournaments.map((tournament, index) => {
                const statusColors = {
                  live: 'bg-red-500',
                  registration_open: 'bg-green-500',
                  coming_soon: 'bg-blue-500',
                  closed: 'bg-gray-500'
                }
                
                return (
                  <motion.div
                    key={tournament.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.1 }}
                  >
                    <Card className="bg-black/40 border-gray-800 backdrop-blur-sm overflow-hidden hover:bg-black/60 transition-all hover:scale-105">
                      <div className="aspect-video bg-purple-700 relative">
                        <div className="absolute inset-0 bg-black/30" />
                        <div className="absolute top-4 right-4">
                          <span className={`px-3 py-1 rounded-full text-xs font-medium text-white ${statusColors[tournament.status as keyof typeof statusColors] || 'bg-gray-500'}`}>
                            {tournament.status.replace('_', ' ').toUpperCase()}
                          </span>
                        </div>
                        <div className="absolute bottom-4 left-4">
                          <div className="text-white font-semibold">{tournament.game}</div>
                        </div>
                        <div className="absolute bottom-4 right-4 flex items-center text-white text-sm">
                          <DollarSign className="h-4 w-4 mr-1" />
                          {formatCurrency(tournament.prize_pool)}
                        </div>
                      </div>
                      <CardHeader>
                        <CardTitle className="text-white">{tournament.title}</CardTitle>
                        <CardDescription className="text-gray-400">
                          Prize Pool: {formatCurrency(tournament.prize_pool)} • {formatNumber(tournament.participants)} Players
                        </CardDescription>
                        <div className="flex items-center text-gray-400 text-sm mt-2">
                          <MapPin className="h-4 w-4 mr-1" />
                          {tournament.region}
                          <Clock className="h-4 w-4 ml-4 mr-1" />
                          {new Date(tournament.start_date).toLocaleDateString()}
                        </div>
                      </CardHeader>
                      <CardContent>
                        <Button className="w-full bg-purple-600 hover:bg-purple-700">
                          View Tournament
                        </Button>
                      </CardContent>
                    </Card>
                  </motion.div>
                )
              })}
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-black/20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-white mb-4">Why Choose ThrillRing?</h2>
            <p className="text-gray-400 text-lg">Experience gaming like never before</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Trophy,
                title: 'Competitive Tournaments',
                description: 'Join tournaments across multiple games with real prizes and global recognition.'
              },
              {
                icon: TrendingUp,
                title: 'Skill-Based Matchmaking',
                description: 'Our advanced algorithm ensures fair matches based on your skill level and performance.'
              },
              {
                icon: Users,
                title: 'Community Driven',
                description: 'Connect with fellow gamers, form teams, and build lasting friendships in our community.'
              }
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card className="bg-black/40 border-gray-800 backdrop-blur-sm h-full hover:bg-black/60 transition-colors">
                  <CardContent className="p-8 text-center">
                    <feature.icon className="h-12 w-12 mx-auto mb-6 text-purple-400" />
                    <h3 className="text-xl font-semibold text-white mb-4">{feature.title}</h3>
                    <p className="text-gray-400 leading-relaxed">{feature.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-3xl mx-auto"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Dominate?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join millions of players and start your journey to becoming a gaming legend.
            </p>
            <Button size="lg" className="bg-purple-600 hover:bg-purple-700 text-lg px-12 py-4">
              Get Started Now
            </Button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 bg-black/40">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-gray-400">
            <p>&copy; 2024 ThrillRing Gaming Portal. All rights reserved.</p>
            <div className="mt-4 text-sm">
              {!gamesLoading && !tournamentsLoading && (
                <span className="text-green-400">● Live data integration active</span>
              )}
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
