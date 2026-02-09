'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

interface ApprovalItem {
  id: string
  workflow_type: string
  title: string
  description: string
  status: 'pending' | 'approved' | 'rejected'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  created_at: string
  data: any
}

export function ApprovalQueue() {
  const [items, setItems] = useState<ApprovalItem[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<string>('all')

  useEffect(() => {
    fetchApprovalItems()
  }, [])

  const fetchApprovalItems = async () => {
    try {
      // Mock data - replace with actual API call
      const mockItems: ApprovalItem[] = [
        {
          id: 'approval_001',
          workflow_type: 'product_sourcing',
          title: 'Product Sourcing: Premium Yoga Mat',
          description: 'AI has identified a high-potential product for dropshipping',
          status: 'pending',
          priority: 'high',
          created_at: new Date(Date.now() - 3600000).toISOString(),
          data: {
            product_name: 'Premium Boldfit Yoga Mat',
            asin: 'B0DX1QJFK4',
            price: 1599,
            rating: 4.5,
            reviews: 2341
          }
        },
        {
          id: 'approval_002',
          workflow_type: 'lead_qualification',
          title: 'Lead Qualification: Enterprise Customer',
          description: 'High-value lead requires manual review',
          status: 'pending',
          priority: 'urgent',
          created_at: new Date(Date.now() - 1800000).toISOString(),
          data: {
            company: 'Tech Solutions Inc',
            budget: 50000,
            score: 95
          }
        },
        {
          id: 'approval_003',
          workflow_type: 'content_generation',
          title: 'Content Review: Blog Post',
          description: 'AI-generated blog post ready for review',
          status: 'pending',
          priority: 'medium',
          created_at: new Date(Date.now() - 7200000).toISOString(),
          data: {
            title: '10 AI Marketing Strategies for 2025',
            word_count: 2500
          }
        }
      ]

      setItems(mockItems)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching approval items:', error)
      setLoading(false)
    }
  }

  const handleApprove = async (id: string) => {
    // Update item status
    setItems(items.map(item =>
      item.id === id ? { ...item, status: 'approved' as const } : item
    ))

    // Call approval API
    try {
      await fetch(`/api/brain/hitl/approve/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
    } catch (error) {
      console.error('Error approving item:', error)
    }
  }

  const handleReject = async (id: string) => {
    // Update item status
    setItems(items.map(item =>
      item.id === id ? { ...item, status: 'rejected' as const } : item
    ))

    // Call rejection API
    try {
      await fetch(`/api/brain/hitl/reject/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
    } catch (error) {
      console.error('Error rejecting item:', error)
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'destructive'
      case 'high': return 'default'
      case 'medium': return 'secondary'
      case 'low': return 'outline'
      default: return 'outline'
    }
  }

  const getWorkflowIcon = (type: string) => {
    switch (type) {
      case 'product_sourcing': return '📦'
      case 'lead_qualification': return '👤'
      case 'content_generation': return '📝'
      case 'campaign_optimization': return '📊'
      default: return '⚙️'
    }
  }

  const filteredItems = filter === 'all'
    ? items
    : items.filter(item => item.status === filter)

  const pendingCount = items.filter(i => i.status === 'pending').length

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Approval Queue</h2>
          <p className="text-muted-foreground">
            {pendingCount} items awaiting your review
          </p>
        </div>

        <div className="flex gap-2">
          <Button
            variant={filter === 'all' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilter('all')}
          >
            All ({items.length})
          </Button>
          <Button
            variant={filter === 'pending' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilter('pending')}
          >
            Pending ({pendingCount})
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-8">Loading approval queue...</div>
      ) : (
        <div className="space-y-4">
          {filteredItems.map((item) => (
            <Card key={item.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    <span className="text-3xl">{getWorkflowIcon(item.workflow_type)}</span>
                    <div>
                      <CardTitle className="text-lg">{item.title}</CardTitle>
                      <CardDescription>{item.description}</CardDescription>
                      <div className="flex gap-2 mt-2">
                        <Badge variant={getPriorityColor(item.priority)}>
                          {item.priority}
                        </Badge>
                        <Badge variant="outline">{item.workflow_type}</Badge>
                        {item.status !== 'pending' && (
                          <Badge variant={item.status === 'approved' ? 'default' : 'destructive'}>
                            {item.status}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>

                  {item.status === 'pending' && (
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleReject(item.id)}
                      >
                        Reject
                      </Button>
                      <Button
                        size="sm"
                        onClick={() => handleApprove(item.id)}
                      >
                        Approve
                      </Button>
                    </div>
                  )}
                </div>
              </CardHeader>

              <CardContent>
                <div className="bg-muted/50 rounded-lg p-4">
                  <p className="text-sm font-medium mb-2">Details:</p>
                  <pre className="text-xs">
                    {JSON.stringify(item.data, null, 2)}
                  </pre>
                </div>
                <p className="text-xs text-muted-foreground mt-2">
                  Created {new Date(item.created_at).toLocaleString()}
                </p>
              </CardContent>
            </Card>
          ))}

          {filteredItems.length === 0 && (
            <Card>
              <CardContent className="py-8 text-center">
                <p className="text-muted-foreground">No items found</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  )
}
