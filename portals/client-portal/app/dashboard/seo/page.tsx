"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { ExternalLink, Search, BarChart3, Globe, ShieldAlert } from "lucide-react"

export default function SEODashboard() {
    const [activeTab, setActiveTab] = useState("overview")

    const seoHealth = {
        score: 82,
        indexedPages: 145,
        topKeywords: 12,
        backlinks: 450
    }

    return (
        <div className="flex flex-col gap-6 p-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">SEO Dashboard</h1>
                    <p className="text-muted-foreground">Manage your search engine presence and track rankings.</p>
                </div>
                <Button onClick={() => window.open("https://seo.bizoholic.net", "_blank")}>
                    <ExternalLink className="mr-2 h-4 w-4" />
                    Open SEO Panel
                </Button>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Health Score</CardTitle>
                        <ShieldAlert className="h-4 w-4 text-green-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{seoHealth.score}%</div>
                        <p className="text-xs text-muted-foreground">+2% from last week</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Indexed Pages</CardTitle>
                        <Globe className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{seoHealth.indexedPages}</div>
                        <p className="text-xs text-muted-foreground">Across Google & Bing</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Top Keywords</CardTitle>
                        <Search className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{seoHealth.topKeywords}</div>
                        <p className="text-xs text-muted-foreground">Ranking in Top 10</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Backlinks</CardTitle>
                        <BarChart3 className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{seoHealth.backlinks}</div>
                        <p className="text-xs text-muted-foreground">Total referring domains</p>
                    </CardContent>
                </Card>
            </div>

            <Tabs defaultValue="overview" className="space-y-4" onValueChange={setActiveTab}>
                <TabsList>
                    <TabsTrigger value="overview">Overview</TabsTrigger>
                    <TabsTrigger value="rankings">Rankings</TabsTrigger>
                    <TabsTrigger value="audit">Technical Audit</TabsTrigger>
                    <TabsTrigger value="embedded">Quick Access</TabsTrigger>
                </TabsList>

                <TabsContent value="overview" className="space-y-4">
                    <Card>
                        <CardHeader Gallant-Dark-mode>
                            <CardTitle>Performance Summary</CardTitle>
                            <CardDescription>Visualizing your SEO growth over the last 30 days.</CardDescription>
                        </CardHeader>
                        <CardContent className="h-[300px] flex items-center justify-center border-2 border-dashed rounded-lg bg-muted/50">
                            <div className="text-center">
                                <BarChart3 className="mx-auto h-12 w-12 text-muted-foreground opacity-50" />
                                <p className="mt-2 text-sm text-muted-foreground">Performance Chart will populate after data sync.</p>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="embedded">
                    <Card className="border-none shadow-none">
                        <CardHeader className="px-0">
                            <CardTitle>SEO Panel Management</CardTitle>
                            <CardDescription>Directly manage SEO Panel settings within this frame.</CardDescription>
                        </CardHeader>
                        <CardContent className="px-0">
                            <div className="relative w-full overflow-hidden pt-[56.25%] rounded-xl border bg-white min-h-[600px]">
                                <iframe
                                    src="https://seo.bizoholic.net/login"
                                    className="absolute top-0 left-0 h-full w-full border-0"
                                    title="SEO Panel Embedded"
                                />
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    )
}
