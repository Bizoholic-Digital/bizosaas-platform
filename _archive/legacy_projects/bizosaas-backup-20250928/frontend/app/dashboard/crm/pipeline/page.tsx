"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  TrendingUp,
  ArrowLeft,
  DollarSign,
  Target,
  Users,
  BarChart3
} from 'lucide-react'
import Link from 'next/link'
import { HydrationSafe } from '@/components/hydration-safe'

export default function PipelinePage() {
  return (
    <div className="space-y-6">
      {/* Breadcrumb Navigation */}
      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
        <Link href="/dashboard/crm" className="hover:text-foreground flex items-center">
          <ArrowLeft className="h-4 w-4 mr-1" />
          CRM Management
        </Link>
        <span>/</span>
        <span className="text-foreground">Sales Pipeline</span>
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Sales Pipeline</h1>
          <p className="text-muted-foreground">
            Visual overview of your sales process and deal progression
          </p>
        </div>
      </div>

      {/* Pipeline Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Pipeline Value</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$145,600</div>
            <p className="text-xs text-muted-foreground">+8.2% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Deals</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">23</div>
            <p className="text-xs text-muted-foreground">Across all stages</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Win Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">67.4%</div>
            <p className="text-xs text-muted-foreground">Last 3 months</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Deal Size</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$6,330</div>
            <p className="text-xs text-muted-foreground">Per closed deal</p>
          </CardContent>
        </Card>
      </div>

      {/* Pipeline Stages */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card className="border-blue-200 bg-blue-50">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-blue-900">Prospecting</CardTitle>
              <Badge variant="outline" className="bg-blue-100 text-blue-700">8</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-lg font-bold text-blue-900">$24,800</div>
            <p className="text-xs text-blue-700 mt-1">Early stage leads</p>
          </CardContent>
        </Card>

        <Card className="border-yellow-200 bg-yellow-50">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-yellow-900">Qualification</CardTitle>
              <Badge variant="outline" className="bg-yellow-100 text-yellow-700">6</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-lg font-bold text-yellow-900">$38,200</div>
            <p className="text-xs text-yellow-700 mt-1">Qualified prospects</p>
          </CardContent>
        </Card>

        <Card className="border-purple-200 bg-purple-50">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-purple-900">Proposal</CardTitle>
              <Badge variant="outline" className="bg-purple-100 text-purple-700">5</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-lg font-bold text-purple-900">$45,900</div>
            <p className="text-xs text-purple-700 mt-1">Proposals sent</p>
          </CardContent>
        </Card>

        <Card className="border-green-200 bg-green-50">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-green-900">Negotiation</CardTitle>
              <Badge variant="outline" className="bg-green-100 text-green-700">4</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-lg font-bold text-green-900">$36,700</div>
            <p className="text-xs text-green-700 mt-1">Close to winning</p>
          </CardContent>
        </Card>
      </div>

      {/* Pipeline Visualization */}
      <Card>
        <CardHeader>
          <CardTitle>Pipeline Visualization</CardTitle>
          <CardDescription>Interactive pipeline board with drag-and-drop functionality</CardDescription>
        </CardHeader>
        <CardContent>
          <HydrationSafe fallback={
            <div className="text-center py-12 text-muted-foreground">
              <TrendingUp className="h-16 w-16 mx-auto mb-4" />
              <p>Loading pipeline...</p>
            </div>
          }>
            <div className="text-center py-12 text-muted-foreground">
              <TrendingUp className="h-16 w-16 mx-auto mb-4" />
              <p>Interactive pipeline visualization coming soon</p>
              <p className="text-sm mt-2">Drag-and-drop deal management will be available here</p>
            </div>
          </HydrationSafe>
        </CardContent>
      </Card>
    </div>
  )
}