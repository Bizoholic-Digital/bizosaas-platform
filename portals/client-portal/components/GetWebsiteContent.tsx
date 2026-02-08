'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Globe, ArrowRight } from 'lucide-react';

export function GetWebsiteContent() {
    return (
        <div className="max-w-4xl mx-auto space-y-8">
            <div className="text-center space-y-4">
                <h2 className="text-3xl font-bold tracking-tight">Get Your Professional Website</h2>
                <p className="text-lg text-muted-foreground">Use our AI-powered builder to launch your site in minutes.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <Card className="border-2 border-primary/20 hover:border-primary/50 transition-colors cursor-pointer">
                    <CardHeader>
                        <CardTitle>AI Generator</CardTitle>
                        <CardDescription>Let AI build a site based on your business description.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="h-32 bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg flex items-center justify-center">
                            <Globe className="h-12 w-12 text-primary" />
                        </div>
                        <Button className="w-full">Start AI Builder <ArrowRight className="ml-2 h-4 w-4" /></Button>
                    </CardContent>
                </Card>

                <Card className="hover:border-primary/50 transition-colors cursor-pointer">
                    <CardHeader>
                        <CardTitle>Choose Template</CardTitle>
                        <CardDescription>Browse our professional templates.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="h-32 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                            <div className="grid grid-cols-2 gap-2 w-2/3">
                                <div className="h-12 bg-white dark:bg-gray-700 rounded shadow-sm"></div>
                                <div className="h-12 bg-white dark:bg-gray-700 rounded shadow-sm"></div>
                                <div className="h-12 bg-white dark:bg-gray-700 rounded shadow-sm"></div>
                                <div className="h-12 bg-white dark:bg-gray-700 rounded shadow-sm"></div>
                            </div>
                        </div>
                        <Button variant="outline" className="w-full">Browse Templates</Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
