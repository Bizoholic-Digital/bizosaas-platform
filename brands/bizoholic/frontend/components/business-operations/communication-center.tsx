"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Progress } from "@/components/ui/progress";
import { DataTable } from "@/components/ui/data-table";
import { toast } from "sonner";
import {
  Mail,
  MessageSquare,
  Phone,
  Send,
  Users,
  TrendingUp,
  Clock,
  CheckCircle2,
  AlertCircle,
  Play,
  Pause,
  BarChart3,
  Target,
  Eye,
  Edit,
  Trash2,
  Copy,
  Plus,
  Filter,
  Download,
  Settings,
  RefreshCw,
  Megaphone,
  Zap,
  Globe
} from "lucide-react";
import { ColumnDef } from "@tanstack/react-table";
import { formatDistanceToNow, format } from "date-fns";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";

interface Campaign {
  id: string;
  name: string;
  type: 'email' | 'sms' | 'voice' | 'social' | 'push';
  status: 'draft' | 'scheduled' | 'running' | 'paused' | 'completed' | 'failed';
  channel: string;
  audience: {
    total: number;
    targeted: number;
  };
  metrics: {
    sent: number;
    delivered: number;
    opened: number;
    clicked: number;
    converted: number;
  };
  schedule: {
    startDate: string;
    endDate?: string;
    timezone: string;
  };
  createdAt: string;
  updatedAt: string;
}

interface CommunicationStats {
  totalCampaigns: number;
  activeCampaigns: number;
  totalSent: number;
  deliveryRate: number;
  openRate: number;
  clickRate: number;
  conversionRate: number;
  channelStats: Record<string, {
    sent: number;
    delivered: number;
    engagement: number;
  }>;
}

export function CommunicationCenter() {
  const [selectedChannel, setSelectedChannel] = useState<string>('email');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Mock data
  const mockStats: CommunicationStats = {
    totalCampaigns: 48,
    activeCampaigns: 12,
    totalSent: 125420,
    deliveryRate: 94.7,
    openRate: 27.3,
    clickRate: 4.2,
    conversionRate: 2.1,
    channelStats: {
      email: { sent: 89200, delivered: 84512, engagement: 25.3 },
      sms: { sent: 23100, delivered: 22654, engagement: 18.7 },
      voice: { sent: 8520, delivered: 7968, engagement: 12.4 },
      social: { sent: 3200, delivered: 3040, engagement: 8.9 },
      push: { sent: 1400, delivered: 1316, engagement: 15.2 }
    }
  };

  const mockCampaigns: Campaign[] = [
    {
      id: 'camp_001',
      name: 'Q4 Product Launch Email Series',
      type: 'email',
      status: 'running',
      channel: 'SendGrid',
      audience: { total: 15420, targeted: 12336 },
      metrics: { sent: 12336, delivered: 11680, opened: 3204, clicked: 518, converted: 89 },
      schedule: {
        startDate: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2).toISOString(),
        endDate: new Date(Date.now() + 1000 * 60 * 60 * 24 * 5).toISOString(),
        timezone: 'Asia/Kolkata'
      },
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 5).toISOString(),
      updatedAt: new Date(Date.now() - 1000 * 60 * 30).toISOString()
    },
    {
      id: 'camp_002',
      name: 'Customer Retention SMS Campaign',
      type: 'sms',
      status: 'scheduled',
      channel: 'Twilio',
      audience: { total: 8500, targeted: 6200 },
      metrics: { sent: 0, delivered: 0, opened: 0, clicked: 0, converted: 0 },
      schedule: {
        startDate: new Date(Date.now() + 1000 * 60 * 60 * 8).toISOString(),
        timezone: 'Asia/Kolkata'
      },
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2).toISOString(),
      updatedAt: new Date(Date.now() - 1000 * 60 * 60).toISOString()
    }
  ];

  const campaignColumns: ColumnDef<Campaign>[] = [
    {
      accessorKey: "name",
      header: "Campaign Name",
      cell: ({ row }) => {
        const campaign = row.original;
        const typeIcons = {
          email: Mail,
          sms: MessageSquare,
          voice: Phone,
          social: Globe,
          push: Megaphone
        };
        const IconComponent = typeIcons[campaign.type];
        
        return (
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-muted rounded-full">
              <IconComponent className="h-4 w-4" />
            </div>
            <div>
              <div className="font-medium">{campaign.name}</div>
              <div className="text-sm text-muted-foreground">{campaign.channel}</div>
            </div>
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
          draft: { variant: "secondary" as const, icon: Edit, color: "text-gray-600" },
          scheduled: { variant: "outline" as const, icon: Clock, color: "text-blue-600" },
          running: { variant: "default" as const, icon: Play, color: "text-green-600" },
          paused: { variant: "secondary" as const, icon: Pause, color: "text-yellow-600" },
          completed: { variant: "default" as const, icon: CheckCircle2, color: "text-green-600" },
          failed: { variant: "destructive" as const, icon: AlertCircle, color: "text-red-600" }
        };
        const config = statusConfig[status as keyof typeof statusConfig];
        const IconComponent = config.icon;
        
        return (
          <div className="flex items-center space-x-2">
            <IconComponent className={`h-4 w-4 ${config.color}`} />
            <Badge variant={config.variant}>
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </Badge>
          </div>
        );
      },
    },
    {
      accessorKey: "metrics",
      header: "Performance",
      cell: ({ row }) => {
        const metrics = row.original.metrics;
        const deliveryRate = metrics.sent > 0 ? (metrics.delivered / metrics.sent * 100) : 0;
        const openRate = metrics.delivered > 0 ? (metrics.opened / metrics.delivered * 100) : 0;
        
        return (
          <div className="space-y-1">
            <div className="flex items-center justify-between text-sm">
              <span>Delivery:</span>
              <span className="font-medium">{deliveryRate.toFixed(1)}%</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span>Open:</span>
              <span className="font-medium">{openRate.toFixed(1)}%</span>
            </div>
            <div className="text-xs text-muted-foreground">
              {metrics.sent.toLocaleString()} sent
            </div>
          </div>
        );
      },
    },
    {
      accessorKey: "audience",
      header: "Audience",
      cell: ({ row }) => {
        const audience = row.original.audience;
        return (
          <div className="text-sm">
            <div className="font-medium">{audience.targeted.toLocaleString()}</div>
            <div className="text-muted-foreground">of {audience.total.toLocaleString()}</div>
          </div>
        );
      },
    },
    {
      accessorKey: "schedule",
      header: "Schedule",
      cell: ({ row }) => {
        const schedule = row.original.schedule;
        return (
          <div className="text-sm">
            <div>{format(new Date(schedule.startDate), 'MMM dd, yyyy')}</div>
            <div className="text-muted-foreground">
              {format(new Date(schedule.startDate), 'HH:mm')} {schedule.timezone}
            </div>
          </div>
        );
      },
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const campaign = row.original;
        
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
                View Details
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Edit className="mr-2 h-4 w-4" />
                Edit Campaign
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Copy className="mr-2 h-4 w-4" />
                Duplicate
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              {campaign.status === 'running' && (
                <DropdownMenuItem>
                  <Pause className="mr-2 h-4 w-4" />
                  Pause Campaign
                </DropdownMenuItem>
              )}
              {campaign.status === 'paused' && (
                <DropdownMenuItem>
                  <Play className="mr-2 h-4 w-4" />
                  Resume Campaign
                </DropdownMenuItem>
              )}
              <DropdownMenuSeparator />
              <DropdownMenuItem className="text-red-600">
                <Trash2 className="mr-2 h-4 w-4" />
                Delete Campaign
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
    toast.success("Communication data refreshed");
  };

  const handleCreateCampaign = () => {
    toast.success("Campaign created successfully");
    setIsCreateDialogOpen(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Communication Center</h2>
          <p className="text-muted-foreground">
            Multi-channel communication hub for email, SMS, voice, and social campaigns
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
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button size="sm">
                <Plus className="mr-2 h-4 w-4" />
                Create Campaign
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px]">
              <DialogHeader>
                <DialogTitle>Create New Campaign</DialogTitle>
                <DialogDescription>
                  Set up a new communication campaign across multiple channels
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="campaign-name" className="text-right">
                    Campaign Name
                  </Label>
                  <Input id="campaign-name" placeholder="Product Launch Campaign" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="campaign-type" className="text-right">
                    Type
                  </Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select campaign type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="email">Email Campaign</SelectItem>
                      <SelectItem value="sms">SMS Campaign</SelectItem>
                      <SelectItem value="voice">Voice Campaign</SelectItem>
                      <SelectItem value="social">Social Media</SelectItem>
                      <SelectItem value="push">Push Notifications</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="campaign-channel" className="text-right">
                    Channel
                  </Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select communication channel" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="sendgrid">SendGrid (Email)</SelectItem>
                      <SelectItem value="twilio">Twilio (SMS/Voice)</SelectItem>
                      <SelectItem value="aws-sns">AWS SNS (Push)</SelectItem>
                      <SelectItem value="slack">Slack (Team Chat)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="campaign-message" className="text-right">
                    Message
                  </Label>
                  <Textarea 
                    id="campaign-message" 
                    placeholder="Enter your campaign message..." 
                    className="col-span-3" 
                    rows={4}
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={handleCreateCampaign}>
                  Create Campaign
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Communication Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Campaigns</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.totalCampaigns}</div>
            <p className="text-xs text-muted-foreground">
              {mockStats.activeCampaigns} currently active
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Messages Sent</CardTitle>
            <Send className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.totalSent.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              {mockStats.deliveryRate}% delivery rate
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Engagement Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.openRate}%</div>
            <p className="text-xs text-muted-foreground">
              {mockStats.clickRate}% click-through rate
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.conversionRate}%</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="inline h-3 w-3 text-green-500 mr-1" />
              +0.3% from last month
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="campaigns" className="space-y-4">
        <TabsList>
          <TabsTrigger value="campaigns">Campaigns</TabsTrigger>
          <TabsTrigger value="channels">Channel Analytics</TabsTrigger>
          <TabsTrigger value="templates">Message Templates</TabsTrigger>
          <TabsTrigger value="audiences">Audiences</TabsTrigger>
        </TabsList>

        <TabsContent value="campaigns" className="space-y-4">
          {/* Campaign Management */}
          <Card>
            <CardHeader>
              <CardTitle>Active Campaigns</CardTitle>
              <CardDescription>
                Manage and monitor all your communication campaigns
              </CardDescription>
            </CardHeader>
            <CardContent>
              <DataTable columns={campaignColumns} data={mockCampaigns} />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="channels" className="space-y-4">
          {/* Channel Performance */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Object.entries(mockStats.channelStats).map(([channel, stats]) => {
              const channelIcons = {
                email: Mail,
                sms: MessageSquare,
                voice: Phone,
                social: Globe,
                push: Megaphone
              };
              const IconComponent = channelIcons[channel as keyof typeof channelIcons] || MessageSquare;
              const deliveryRate = (stats.delivered / stats.sent * 100);
              
              return (
                <Card key={channel}>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium capitalize">
                      {channel} Channel
                    </CardTitle>
                    <IconComponent className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div>
                        <div className="text-2xl font-bold">{stats.sent.toLocaleString()}</div>
                        <p className="text-xs text-muted-foreground">Messages sent</p>
                      </div>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Delivery Rate</span>
                          <span className="font-medium">{deliveryRate.toFixed(1)}%</span>
                        </div>
                        <Progress value={deliveryRate} className="h-2" />
                        <div className="flex justify-between text-sm">
                          <span>Engagement</span>
                          <span className="font-medium">{stats.engagement}%</span>
                        </div>
                        <Progress value={stats.engagement} className="h-2" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        <TabsContent value="templates" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Message Templates</CardTitle>
              <CardDescription>
                Pre-built templates for quick campaign creation
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p className="text-muted-foreground">
                  Template management interface coming soon. Create custom templates for different campaign types.
                </p>
                <Button variant="outline">
                  <Plus className="mr-2 h-4 w-4" />
                  Create Template
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="audiences" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Audience Management</CardTitle>
              <CardDescription>
                Manage and segment your communication audiences
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p className="text-muted-foreground">
                  Advanced audience segmentation and management features coming soon.
                </p>
                <div className="flex items-center space-x-2">
                  <Button variant="outline">
                    <Users className="mr-2 h-4 w-4" />
                    Import Audience
                  </Button>
                  <Button variant="outline">
                    <Filter className="mr-2 h-4 w-4" />
                    Create Segment
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}