'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';

export function HeroSection() {
    return (
        <div className="relative overflow-hidden bg-background py-24 sm:py-32">
            {/* Background gradient/image would go here */}
            <div className="absolute inset-0 bg-[url('/grid-pattern.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]"></div>
            <div className="absolute inset-y-0 right-1/2 -z-10 mr-16 w-[200%] origin-bottom-left skew-x-[-30deg] bg-background shadow-xl shadow-indigo-600/10 ring-1 ring-indigo-50 sm:mr-28 lg:mr-0 xl:mr-16 xl:origin-center"></div>

            <div className="mx-auto max-w-7xl px-6 lg:px-8 relative">
                <div className="mx-auto max-w-2xl lg:max-w-none lg:text-center">
                    <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-6xl bg-clip-text text-transparent bg-gradient-to-r from-purple-500 to-pink-500">
                        ThrillRing Gaming
                    </h1>
                    <p className="mt-6 text-lg leading-8 text-muted-foreground">
                        Where Champions Are Made. Join thousands of players in daily tournaments, climb the leaderboards, and win real prizes.
                    </p>
                    <div className="mt-10 flex flex-col gap-y-4 sm:flex-row sm:justify-center sm:gap-x-6">
                        <Button size="lg" className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg border-0">
                            Join Tournament
                        </Button>
                        <Button variant="outline" size="lg">
                            View Leaderboard
                        </Button>
                    </div>
                </div>

                {/* Stats Preview or Hero Image could go here */}
            </div>
        </div>
    );
}
