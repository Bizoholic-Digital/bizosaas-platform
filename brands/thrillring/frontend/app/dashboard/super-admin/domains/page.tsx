'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Globe, Plus, Edit, Trash2, ExternalLink, CheckCircle, 
  AlertCircle, RefreshCw, Settings, Shield, Zap,
  Eye, Copy, Link
} from 'lucide-react'

interface Domain {
  id: string
  domain: string
  tenantId: string
  tenantName: string
  status: 'active' | 'pending' | 'error' | 'suspended'
  sslStatus: 'active' | 'pending' | 'error'
  lastVerified: string
  createdAt: string
  redirectUrl?: string
  dnsVerified: boolean
  subscriptionTier: 'free' | 'starter' | 'professional' | 'enterprise'
}

interface DnsRecord {
  type: 'CNAME' | 'A'
  name: string
  value: string
  status: 'verified' | 'pending' | 'error'
}

export default function DomainManagement() {
  const [domains, setDomains] = useState<Domain[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isAddingDomain, setIsAddingDomain] = useState(false)
  const [newDomain, setNewDomain] = useState({
    domain: '',
    tenantId: '',
    redirectUrl: ''
  })
  const [selectedDomain, setSelectedDomain] = useState<Domain | null>(null)

  // Mock data for demonstration
  useEffect(() => {
    const loadDomains = async () => {
      setTimeout(() => {
        setDomains([
          {
            id: '1',
            domain: 'bizoholic.com',
            tenantId: 'bizoholic',
            tenantName: 'Bizoholic Digital',
            status: 'active',
            sslStatus: 'active',
            lastVerified: '2025-09-11T08:00:00Z',
            createdAt: '2025-08-15T10:30:00Z',
            redirectUrl: 'http://localhost:3000/dashboard',
            dnsVerified: true,
            subscriptionTier: 'enterprise'
          },
          {
            id: '2', 
            domain: 'coreldove.com',
            tenantId: 'coreldove',
            tenantName: 'CoreLDove',
            status: 'active',
            sslStatus: 'active',
            lastVerified: '2025-09-11T07:45:00Z',
            createdAt: '2025-08-20T14:20:00Z',
            redirectUrl: 'http://localhost:3000/dashboard/coreldove',
            dnsVerified: true,
            subscriptionTier: 'enterprise'
          },
          {
            id: '3',
            domain: 'thrillring.com', 
            tenantId: 'thrillring',
            tenantName: 'ThrillRing',
            status: 'pending',
            sslStatus: 'pending',
            lastVerified: '2025-09-11T06:30:00Z',
            createdAt: '2025-09-10T16:45:00Z',
            redirectUrl: 'http://localhost:3000/dashboard/thrillring',
            dnsVerified: false,
            subscriptionTier: 'professional'
          },
          {
            id: '4',
            domain: 'quanttrade.com',
            tenantId: 'quanttrade', 
            tenantName: 'QuantTrade',
            status: 'active',
            sslStatus: 'active',
            lastVerified: '2025-09-11T07:15:00Z',
            createdAt: '2025-08-25T11:10:00Z',
            redirectUrl: 'http://localhost:3000/dashboard/quanttrade',
            dnsVerified: true,
            subscriptionTier: 'enterprise'
          },
          {
            id: '5',
            domain: 'mydemosite.com',
            tenantId: 'demo123',
            tenantName: 'Demo Client',
            status: 'error',
            sslStatus: 'error',
            lastVerified: '2025-09-10T12:00:00Z',
            createdAt: '2025-09-05T09:30:00Z',
            redirectUrl: 'http://localhost:3000/dashboard',
            dnsVerified: false,
            subscriptionTier: 'starter'
          }
        ])
        setIsLoading(false)
      }, 1000)
    }

    loadDomains()
  }, [])

  const getDnsRecords = (domain: string): DnsRecord[] => {
    return [
      { type: 'CNAME', name: 'www', value: 'bizosaas.platform.com', status: 'verified' },
      { type: 'A', name: '@', value: '45.67.123.45', status: 'verified' }
    ]
  }

  const handleAddDomain = async () => {
    if (!newDomain.domain || !newDomain.tenantId) return

    setIsAddingDomain(true)
    
    // Simulate API call
    setTimeout(() => {
      const domain: Domain = {
        id: Date.now().toString(),
        domain: newDomain.domain,
        tenantId: newDomain.tenantId,
        tenantName: `Client ${newDomain.tenantId}`,
        status: 'pending',
        sslStatus: 'pending',
        lastVerified: new Date().toISOString(),
        createdAt: new Date().toISOString(),
        redirectUrl: newDomain.redirectUrl || 'http://localhost:3000/dashboard',
        dnsVerified: false,
        subscriptionTier: 'starter'
      }
      
      setDomains(prev => [domain, ...prev])
      setNewDomain({ domain: '', tenantId: '', redirectUrl: '' })
      setIsAddingDomain(false)
    }, 2000)
  }

  const verifyDomain = async (domainId: string) => {
    setDomains(prev => prev.map(d => 
      d.id === domainId 
        ? { ...d, status: 'active', dnsVerified: true, sslStatus: 'active', lastVerified: new Date().toISOString() }
        : d
    ))
  }

  const deleteDomain = async (domainId: string) => {
    setDomains(prev => prev.filter(d => d.id !== domainId))
  }

  const stats = [
    { title: 'Active Domains', value: domains.filter(d => d.status === 'active').length.toString(), icon: Globe, color: 'text-green-600' },
    { title: 'Pending Setup', value: domains.filter(d => d.status === 'pending').length.toString(), icon: RefreshCw, color: 'text-blue-600' },
    { title: 'SSL Secured', value: domains.filter(d => d.sslStatus === 'active').length.toString(), icon: Shield, color: 'text-green-600' },
    { title: 'DNS Verified', value: domains.filter(d => d.dnsVerified).length.toString(), icon: CheckCircle, color: 'text-green-600' },
  ]

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Domain Management</h1>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1,2,3,4].map(i => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-8 bg-gray-200 rounded mb-2"></div>
                <div className="h-4 bg-gray-200 rounded"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Domain Management</h1>
          <p className="text-muted-foreground mt-2">
            Manage client custom domains and DNS configuration
          </p>
        </div>
        <Dialog>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Domain
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>Add Custom Domain</DialogTitle>
              <DialogDescription>
                Add a new custom domain for a client tenant
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="domain">Domain</Label>
                <Input
                  id="domain"
                  value={newDomain.domain}
                  onChange={(e) => setNewDomain(prev => ({ ...prev, domain: e.target.value }))}
                  placeholder="example.com"
                />
              </div>
              <div>
                <Label htmlFor="tenant">Tenant ID</Label>
                <Input
                  id="tenant"
                  value={newDomain.tenantId}
                  onChange={(e) => setNewDomain(prev => ({ ...prev, tenantId: e.target.value }))}
                  placeholder="client-tenant-id"
                />
              </div>
              <div>
                <Label htmlFor="redirect">Redirect URL (Optional)</Label>
                <Input
                  id="redirect"
                  value={newDomain.redirectUrl}
                  onChange={(e) => setNewDomain(prev => ({ ...prev, redirectUrl: e.target.value }))}
                  placeholder="http://localhost:3000/dashboard/client"
                />
              </div>
              <Button 
                onClick={handleAddDomain} 
                disabled={isAddingDomain || !newDomain.domain || !newDomain.tenantId}
                className="w-full"
              >
                {isAddingDomain ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    Adding Domain...
                  </>
                ) : (
                  <>
                    <Plus className="h-4 w-4 mr-2" />
                    Add Domain
                  </>
                )}
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Domain List */}
      <Card>
        <CardHeader>
          <CardTitle>Client Domains</CardTitle>
          <CardDescription>Manage custom domains for all tenants</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {domains.map((domain) => (
              <div key={domain.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                    <Globe className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium">{domain.domain}</h3>
                      <Badge variant={
                        domain.status === 'active' ? 'default' :
                        domain.status === 'pending' ? 'secondary' :
                        domain.status === 'error' ? 'destructive' : 'outline'
                      }>
                        {domain.status}
                      </Badge>
                      {domain.sslStatus === 'active' && (
                        <Badge variant="outline" className="text-green-600">
                          <Shield className="h-3 w-3 mr-1" />
                          SSL
                        </Badge>
                      )}
                      {domain.dnsVerified && (
                        <Badge variant="outline" className="text-blue-600">
                          <CheckCircle className="h-3 w-3 mr-1" />
                          DNS
                        </Badge>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {domain.tenantName} • {domain.subscriptionTier}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Last verified: {new Date(domain.lastVerified).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {domain.status === 'pending' && (
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => verifyDomain(domain.id)}
                    >
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Verify
                    </Button>
                  )}
                  <Button 
                    variant="ghost" 
                    size="sm"
                    onClick={() => setSelectedDomain(domain)}
                  >
                    <Settings className="h-4 w-4" />
                  </Button>
                  <Button 
                    variant="ghost" 
                    size="sm"
                    onClick={() => window.open(`https://${domain.domain}`, '_blank')}
                  >
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                  <Button 
                    variant="ghost" 
                    size="sm"
                    onClick={() => deleteDomain(domain.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Domain Details Dialog */}
      {selectedDomain && (
        <Dialog open={!!selectedDomain} onOpenChange={() => setSelectedDomain(null)}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>{selectedDomain.domain} - Configuration</DialogTitle>
              <DialogDescription>
                Domain settings and DNS configuration
              </DialogDescription>
            </DialogHeader>
            
            <Tabs defaultValue="settings" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="settings">Settings</TabsTrigger>
                <TabsTrigger value="dns">DNS Records</TabsTrigger>
                <TabsTrigger value="ssl">SSL Certificate</TabsTrigger>
              </TabsList>
              
              <TabsContent value="settings" className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>Domain</Label>
                    <Input value={selectedDomain.domain} disabled />
                  </div>
                  <div>
                    <Label>Tenant ID</Label>
                    <Input value={selectedDomain.tenantId} disabled />
                  </div>
                  <div>
                    <Label>Status</Label>
                    <div className="flex items-center gap-2 pt-2">
                      <Badge variant={
                        selectedDomain.status === 'active' ? 'default' :
                        selectedDomain.status === 'pending' ? 'secondary' : 'destructive'
                      }>
                        {selectedDomain.status}
                      </Badge>
                    </div>
                  </div>
                  <div>
                    <Label>Subscription Tier</Label>
                    <div className="flex items-center gap-2 pt-2">
                      <Badge variant="outline">{selectedDomain.subscriptionTier}</Badge>
                    </div>
                  </div>
                </div>
                <div>
                  <Label>Redirect URL</Label>
                  <Input value={selectedDomain.redirectUrl} disabled />
                </div>
              </TabsContent>
              
              <TabsContent value="dns" className="space-y-4">
                <Alert>
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>
                    Configure these DNS records with your domain provider:
                  </AlertDescription>
                </Alert>
                <div className="space-y-3">
                  {getDnsRecords(selectedDomain.domain).map((record, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded">
                      <div className="grid grid-cols-3 gap-4 flex-1">
                        <div>
                          <div className="text-sm font-medium">{record.type}</div>
                          <div className="text-xs text-muted-foreground">{record.name}</div>
                        </div>
                        <div>
                          <div className="text-sm font-mono">{record.value}</div>
                        </div>
                        <div>
                          <Badge variant={record.status === 'verified' ? 'default' : 'secondary'}>
                            {record.status}
                          </Badge>
                        </div>
                      </div>
                      <Button variant="ghost" size="sm">
                        <Copy className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </TabsContent>
              
              <TabsContent value="ssl" className="space-y-4">
                <div className="flex items-center justify-between p-4 border rounded">
                  <div>
                    <div className="font-medium">SSL Certificate</div>
                    <div className="text-sm text-muted-foreground">
                      Let's Encrypt SSL Certificate
                    </div>
                  </div>
                  <Badge variant={selectedDomain.sslStatus === 'active' ? 'default' : 'secondary'}>
                    {selectedDomain.sslStatus}
                  </Badge>
                </div>
                {selectedDomain.sslStatus === 'active' && (
                  <div className="text-sm text-muted-foreground">
                    Certificate expires: December 15, 2025
                  </div>
                )}
              </TabsContent>
            </Tabs>
          </DialogContent>
        </Dialog>
      )}
    </div>
  )
}