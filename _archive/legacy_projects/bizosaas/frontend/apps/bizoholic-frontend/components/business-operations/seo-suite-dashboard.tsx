"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Progress } from "@/components/ui/progress";
import { DataTable } from "@/components/ui/data-table";
import { toast } from "sonner";
import {
  Search,
  Globe,
  TrendingUp,
  TrendingDown,
  BarChart3,
  Target,
  CheckCircle2,
  AlertCircle,
  Clock,
  RefreshCw,
  Plus,
  Settings,
  Eye,
  ExternalLink,
  Download,
  Filter,
  ArrowUp,
  ArrowDown,
  Minus,
  FileText,
  Link,
  Image,
  Code,
  Zap,
  Activity
} from "lucide-react";
import { ColumnDef } from "@tanstack/react-table";
import { formatDistanceToNow } from "date-fns";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";

interface SEOKeyword {
  id: string;
  keyword: string;
  currentRank: number;
  previousRank: number;
  searchVolume: number;
  difficulty: number;
  url: string;
  searchEngine: string;
  country: string;
  updatedAt: string;
}

interface SEOAudit {
  id: string;
  url: string;
  score: number;
  issues: {
    critical: number;
    warning: number;
    notice: number;
  };
  metrics: {
    loadTime: number;
    mobileScore: number;
    accessibilityScore: number;
    seoScore: number;
  };
  status: 'completed' | 'running' | 'failed';
  createdAt: string;
}

interface SEOStats {
  totalKeywords: number;
  avgRanking: number;
  organicTraffic: number;
  indexedPages: number;
  domainAuthority: number;
  backlinks: number;
  searchEngineStats: Record<string, {
    keywords: number;
    avgRank: number;
    traffic: number;
  }>;
}

export function SEOSuiteDashboard() {
  const [selectedEngine, setSelectedEngine] = useState<string>('google');
  const [isAuditDialogOpen, setIsAuditDialogOpen] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Mock data
  const mockStats: SEOStats = {
    totalKeywords: 1247,
    avgRanking: 12.4,
    organicTraffic: 15420,
    indexedPages: 1247,
    domainAuthority: 68,
    backlinks: 2543,
    searchEngineStats: {
      google: { keywords: 892, avgRank: 11.2, traffic: 12340 },
      bing: { keywords: 156, avgRank: 15.8, traffic: 1820 },
      yandex: { keywords: 89, avgRank: 18.3, traffic: 680 },
      baidu: { keywords: 67, avgRank: 22.1, traffic: 420 },
      duckduckgo: { keywords: 43, avgRank: 16.7, traffic: 160 }
    }
  };

  const mockKeywords: SEOKeyword[] = [
    {
      id: 'kw_001',
      keyword: 'ai marketing automation',
      currentRank: 3,
      previousRank: 5,
      searchVolume: 8900,
      difficulty: 75,
      url: '/services/ai-marketing',
      searchEngine: 'google',
      country: 'IN',
      updatedAt: new Date(Date.now() - 1000 * 60 * 30).toISOString()
    },
    {
      id: 'kw_002',
      keyword: 'digital marketing agency india',
      currentRank: 7,
      previousRank: 7,
      searchVolume: 12400,
      difficulty: 82,
      url: '/about',
      searchEngine: 'google',
      country: 'IN',
      updatedAt: new Date(Date.now() - 1000 * 60 * 45).toISOString()
    },
    {
      id: 'kw_003',
      keyword: 'social media management tools',
      currentRank: 15,
      previousRank: 12,
      searchVolume: 6700,
      difficulty: 68,
      url: '/services/social-media',
      searchEngine: 'google',
      country: 'IN',
      updatedAt: new Date(Date.now() - 1000 * 60 * 60).toISOString()
    }
  ];

  const mockAudits: SEOAudit[] = [
    {
      id: 'audit_001',
      url: 'https://bizoholic.com',
      score: 87,
      issues: { critical: 2, warning: 8, notice: 15 },
      metrics: {
        loadTime: 2.1,
        mobileScore: 92,
        accessibilityScore: 88,
        seoScore: 87
      },
      status: 'completed',
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString()
    }
  ];

  const keywordColumns: ColumnDef<SEOKeyword>[] = [
    {
      accessorKey: "keyword",
      header: "Keyword",
      cell: ({ row }) => (
        <div className="space-y-1">
          <div className="font-medium">{row.getValue("keyword")}</div>
          <div className="text-sm text-muted-foreground">{row.original.url}</div>
        </div>
      ),
    },
    {
      accessorKey: "currentRank",
      header: "Current Rank",
      cell: ({ row }) => {
        const currentRank = row.getValue("currentRank") as number;
        const previousRank = row.original.previousRank;
        const change = previousRank - currentRank;
        
        return (
          <div className="flex items-center space-x-2">
            <span className="text-2xl font-bold">{currentRank}</span>
            {change > 0 && (
              <div className="flex items-center text-green-600">
                <ArrowUp className="h-4 w-4" />
                <span className="text-sm">+{change}</span>
              </div>
            )}
            {change < 0 && (
              <div className="flex items-center text-red-600">
                <ArrowDown className="h-4 w-4" />
                <span className="text-sm">{change}</span>
              </div>
            )}
            {change === 0 && (
              <div className="flex items-center text-muted-foreground">
                <Minus className="h-4 w-4" />
                <span className="text-sm">0</span>
              </div>
            )}
          </div>
        );
      },
    },
    {
      accessorKey: "searchVolume",
      header: "Search Volume",
      cell: ({ row }) => (
        <div className="text-sm">
          {(row.getValue("searchVolume") as number).toLocaleString()}/mo
        </div>
      ),
    },
    {
      accessorKey: "difficulty",
      header: "Difficulty",
      cell: ({ row }) => {
        const difficulty = row.getValue("difficulty") as number;
        const getColor = (diff: number) => {
          if (diff < 30) return "text-green-600";
          if (diff < 60) return "text-yellow-600";
          return "text-red-600";
        };
        
        return (
          <div className="flex items-center space-x-2">
            <span className={`font-medium ${getColor(difficulty)}`}>{difficulty}%</span>
            <Progress value={difficulty} className="w-16 h-2" />
          </div>
        );
      },
    },
    {
      accessorKey: "searchEngine",
      header: "Engine",
      cell: ({ row }) => (
        <Badge variant="outline" className="capitalize">
          {row.getValue("searchEngine")}
        </Badge>
      ),
    },
    {
      accessorKey: "updatedAt",
      header: "Last Updated",
      cell: ({ row }) => (
        <div className="text-sm text-muted-foreground">
          {formatDistanceToNow(new Date(row.getValue("updatedAt")), { addSuffix: true })}
        </div>
      ),
    },
  ];

  const auditColumns: ColumnDef<SEOAudit>[] = [
    {
      accessorKey: "url",
      header: "URL",
      cell: ({ row }) => (
        <div className="flex items-center space-x-2">
          <Globe className="h-4 w-4 text-muted-foreground" />
          <span className="font-mono text-sm">{row.getValue("url")}</span>
        </div>
      ),
    },
    {
      accessorKey: "score",
      header: "SEO Score",
      cell: ({ row }) => {
        const score = row.getValue("score") as number;
        const getColor = (score: number) => {
          if (score >= 80) return "text-green-600";
          if (score >= 60) return "text-yellow-600";
          return "text-red-600";
        };
        
        return (
          <div className="flex items-center space-x-2">
            <span className={`text-2xl font-bold ${getColor(score)}`}>{score}</span>
            <Progress value={score} className="w-16 h-2" />
          </div>
        );
      },
    },
    {
      accessorKey: "issues",
      header: "Issues",
      cell: ({ row }) => {
        const issues = row.original.issues;
        return (
          <div className="flex items-center space-x-3">
            {issues.critical > 0 && (
              <Badge variant="destructive">{issues.critical} Critical</Badge>
            )}
            {issues.warning > 0 && (
              <Badge variant="secondary">{issues.warning} Warning</Badge>
            )}
            {issues.notice > 0 && (
              <Badge variant="outline">{issues.notice} Notice</Badge>
            )}
          </div>
        );
      },
    },
    {
      accessorKey: "status",
      header: "Status",
      cell: ({ row }) => {
        const status = row.getValue("status") as string;
        const statusConfig = {
          completed: { variant: "default" as const, icon: CheckCircle2 },
          running: { variant: "secondary" as const, icon: Clock },
          failed: { variant: "destructive" as const, icon: AlertCircle }
        };
        const config = statusConfig[status as keyof typeof statusConfig];
        const IconComponent = config.icon;
        
        return (
          <div className="flex items-center space-x-2">
            <IconComponent className="h-4 w-4" />
            <Badge variant={config.variant}>
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </Badge>
          </div>
        );
      },
    },
    {
      accessorKey: "createdAt",
      header: "Created",
      cell: ({ row }) => (
        <div className="text-sm text-muted-foreground">
          {formatDistanceToNow(new Date(row.getValue("createdAt")), { addSuffix: true })}
        </div>
      ),
    },
    {
      id: "actions",
      cell: ({ row }) => {
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <Settings className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuItem>
                <Eye className="mr-2 h-4 w-4" />
                View Report
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Download className="mr-2 h-4 w-4" />
                Export PDF
              </DropdownMenuItem>
              <DropdownMenuItem>
                <RefreshCw className="mr-2 h-4 w-4" />
                Re-run Audit
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ];

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsRefreshing(false);
    toast.success("SEO data refreshed");
  };

  const handleRunAudit = () => {
    toast.success("SEO audit started");
    setIsAuditDialogOpen(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">SEO Suite Dashboard</h2>
          <p className="text-muted-foreground">
            Multi-search engine optimization tools and comprehensive SEO analytics
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={isRefreshing}
          >
            <RefreshCw className={`mr-2 h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Dialog open={isAuditDialogOpen} onOpenChange={setIsAuditDialogOpen}>
            <DialogTrigger asChild>
              <Button size="sm">
                <Plus className="mr-2 h-4 w-4" />
                Run SEO Audit
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Run SEO Audit</DialogTitle>
                <DialogDescription>
                  Perform a comprehensive SEO analysis of your website
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="audit-url" className="text-right">
                    Website URL
                  </Label>
                  <Input id="audit-url" placeholder="https://example.com" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="audit-engine" className="text-right">
                    Search Engine
                  </Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select search engine" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="google">Google</SelectItem>
                      <SelectItem value="bing">Bing</SelectItem>
                      <SelectItem value="yandex">Yandex</SelectItem>
                      <SelectItem value="baidu">Baidu</SelectItem>
                      <SelectItem value="duckduckgo">DuckDuckGo</SelectItem>
                      <SelectItem value="all">All Engines</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setIsAuditDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={handleRunAudit}>
                  Start Audit
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* SEO Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tracked Keywords</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.totalKeywords.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Avg rank: #{mockStats.avgRanking}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Organic Traffic</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.organicTraffic.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="inline h-3 w-3 text-green-500 mr-1" />
              +12.5% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Domain Authority</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.domainAuthority}</div>
            <p className="text-xs text-muted-foreground">
              {mockStats.backlinks.toLocaleString()} backlinks
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Indexed Pages</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.indexedPages.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Across all search engines
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="keywords" className="space-y-4">
        <TabsList>
          <TabsTrigger value="keywords">Keywords</TabsTrigger>
          <TabsTrigger value="audits">SEO Audits</TabsTrigger>
          <TabsTrigger value="engines">Search Engines</TabsTrigger>
          <TabsTrigger value="technical">Technical SEO</TabsTrigger>
        </TabsList>

        <TabsContent value="keywords" className="space-y-4">
          {/* Keyword Tracking */}
          <Card>
            <CardHeader>
              <CardTitle>Keyword Rankings</CardTitle>
              <CardDescription>
                Track your keyword positions across multiple search engines
              </CardDescription>
            </CardHeader>
            <CardContent>
              <DataTable columns={keywordColumns} data={mockKeywords} />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="audits" className="space-y-4">
          {/* SEO Audits */}
          <Card>
            <CardHeader>
              <CardTitle>SEO Audit Reports</CardTitle>
              <CardDescription>
                Comprehensive website analysis and optimization recommendations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <DataTable columns={auditColumns} data={mockAudits} />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="engines" className="space-y-4">
          {/* Search Engine Performance */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Object.entries(mockStats.searchEngineStats).map(([engine, stats]) => {
              const engineNames = {
                google: 'Google',
                bing: 'Bing',
                yandex: 'Yandex',
                baidu: 'Baidu',
                duckduckgo: 'DuckDuckGo'
              };
              const engineName = engineNames[engine as keyof typeof engineNames] || engine;
              
              return (
                <Card key={engine}>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">{engineName}</CardTitle>
                    <Search className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div>
                        <div className="text-2xl font-bold">{stats.keywords}</div>
                        <p className="text-xs text-muted-foreground">Tracked keywords</p>
                      </div>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Avg. Rank</span>
                          <span className="font-medium">#{stats.avgRank}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span>Traffic</span>
                          <span className="font-medium">{stats.traffic.toLocaleString()}</span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        <TabsContent value="technical" className="space-y-4">
          {/* Technical SEO */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Technical Health</CardTitle>
                <CardDescription>Core web vitals and technical performance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Zap className="h-4 w-4 text-yellow-500" />
                      <span className="text-sm">Page Load Speed</span>
                    </div>
                    <span className="text-sm font-medium">2.1s</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Activity className="h-4 w-4 text-green-500" />
                      <span className="text-sm">Mobile Performance</span>
                    </div>
                    <span className="text-sm font-medium">92/100</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <CheckCircle2 className="h-4 w-4 text-blue-500" />
                      <span className="text-sm">Accessibility Score</span>
                    </div>
                    <span className="text-sm font-medium">88/100</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Content Analysis</CardTitle>
                <CardDescription>Content optimization insights</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <FileText className="h-4 w-4 text-blue-500" />
                      <span className="text-sm">Meta Descriptions</span>
                    </div>
                    <Badge variant="outline">98% Complete</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Image className="h-4 w-4 text-green-500" />
                      <span className="text-sm">Image Alt Tags</span>
                    </div>
                    <Badge variant="outline">87% Complete</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Link className="h-4 w-4 text-purple-500" />
                      <span className="text-sm">Internal Links</span>
                    </div>
                    <Badge variant="outline">Good</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}