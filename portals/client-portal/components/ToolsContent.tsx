'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Wrench, Search, Zap } from 'lucide-react';

export function ToolsContent() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold tracking-tight">Tools</h2>
                <p className="text-muted-foreground">Utility tools to enhance your workflow.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2"><Search className="h-5 w-5" /> SEO Analyzer</CardTitle>
                        <CardDescription>Analyze pages for SEO performance.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Button className="w-full">Launch Tool</Button>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2"><Zap className="h-5 w-5" /> Speed Test</CardTitle>
                        <CardDescription>Check your website loading speed.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Button className="w-full">Launch Tool</Button>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2"><Wrench className="h-5 w-5" /> Broken Link Checker</CardTitle>
                        <CardDescription>Scan site for 404 errors.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Button className="w-full">Launch Tool</Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
