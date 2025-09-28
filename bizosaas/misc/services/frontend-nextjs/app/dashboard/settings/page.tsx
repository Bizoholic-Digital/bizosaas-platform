'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Separator } from '@/components/ui/separator'
import { Upload, Eye, Save, RefreshCw, Palette, Settings2, Globe, Image } from 'lucide-react'
import { toast } from 'sonner'

interface TenantBranding {
  id: string
  name: string
  domain: string
  logo: string
  favicon: string
  primaryColor: string
  secondaryColor: string
  brandGradient: string
  status: 'active' | 'inactive' | 'pending'
}

export default function SettingsPage() {
  const [tenants] = useState<TenantBranding[]>([
    {
      id: 'bizoholic',
      name: 'Bizoholic',
      domain: 'bizoholic.com',
      logo: '/logos/bizoholic-logo.png',
      favicon: '/favicons/bizoholic-favicon.png',
      primaryColor: '#2563EB',
      secondaryColor: '#10B981',
      brandGradient: 'from-blue-600 to-emerald-500',
      status: 'active'
    },
    {
      id: 'coreldove',
      name: 'CoreLDove',
      domain: 'coreldove.com',
      logo: '/logos/coreldove-logo.png',
      favicon: '/favicons/coreldove-favicon.png',
      primaryColor: '#EF4444',
      secondaryColor: '#3B82F6',
      brandGradient: 'from-red-500 to-blue-500',
      status: 'active'
    },
    {
      id: 'bizosaas',
      name: 'BizOSaaS',
      domain: 'app.bizoholic.com',
      logo: '/logos/bizosaas-logo.png',
      favicon: '/favicons/bizosaas-favicon.png',
      primaryColor: '#8B5CF6',
      secondaryColor: '#7C3AED',
      brandGradient: 'from-violet-600 to-purple-600',
      status: 'active'
    }
  ])

  const [selectedTenant, setSelectedTenant] = useState<TenantBranding>(tenants[0])
  const [isUploading, setIsUploading] = useState(false)

  const handleLogoUpload = async (file: File, type: 'logo' | 'favicon') => {
    setIsUploading(true)
    try {
      // Simulate upload process
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const reader = new FileReader()
      reader.onload = (e) => {
        setSelectedTenant(prev => ({
          ...prev,
          [type]: e.target?.result as string
        }))
      }
      reader.readAsDataURL(file)
      
      toast.success(`${type === 'logo' ? 'Logo' : 'Favicon'} uploaded successfully`)
    } catch (error) {
      toast.error('Upload failed. Please try again.')
    } finally {
      setIsUploading(false)
    }
  }

  const handleSaveBranding = async () => {
    try {
      // Simulate API call to update branding
      await new Promise(resolve => setTimeout(resolve, 1500))
      toast.success('Branding settings saved successfully')
    } catch (error) {
      toast.error('Failed to save branding settings')
    }
  }

  const handleColorChange = (field: 'primaryColor' | 'secondaryColor', color: string) => {
    setSelectedTenant(prev => ({
      ...prev,
      [field]: color,
      brandGradient: field === 'primaryColor' 
        ? `from-[${color}] to-[${prev.secondaryColor}]`
        : `from-[${prev.primaryColor}] to-[${color}]`
    }))
  }

  return (
    <div className="container mx-auto p-6 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
          <p className="text-muted-foreground">
            Manage tenant branding, configurations, and platform settings
          </p>
        </div>
        <Button onClick={handleSaveBranding} className="bg-violet-600 hover:bg-violet-700">
          <Save className="w-4 h-4 mr-2" />
          Save Changes
        </Button>
      </div>

      <Tabs defaultValue="branding" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="branding" className="flex items-center gap-2">
            <Palette className="w-4 h-4" />
            Branding
          </TabsTrigger>
          <TabsTrigger value="tenants" className="flex items-center gap-2">
            <Globe className="w-4 h-4" />
            Tenants
          </TabsTrigger>
          <TabsTrigger value="system" className="flex items-center gap-2">
            <Settings2 className="w-4 h-4" />
            System
          </TabsTrigger>
          <TabsTrigger value="integrations" className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Integrations
          </TabsTrigger>
        </TabsList>

        <TabsContent value="branding" className="space-y-6">
          {/* Tenant Selector */}
          <Card>
            <CardHeader>
              <CardTitle>Select Tenant</CardTitle>
              <CardDescription>
                Choose a tenant to manage their branding settings
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {tenants.map((tenant) => (
                  <Card 
                    key={tenant.id}
                    className={`cursor-pointer transition-all hover:shadow-md ${
                      selectedTenant.id === tenant.id ? 'ring-2 ring-violet-500' : ''
                    }`}
                    onClick={() => setSelectedTenant(tenant)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold">{tenant.name}</h3>
                        <Badge 
                          variant={tenant.status === 'active' ? 'default' : 'secondary'}
                          className={`tenant-badge ${tenant.id}`}
                        >
                          {tenant.status}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mb-3">{tenant.domain}</p>
                      <div className={`h-2 rounded-full bg-gradient-to-r ${tenant.brandGradient}`}></div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Branding Configuration */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Logo & Assets */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Image className="w-5 h-5" />
                  Logo & Assets
                </CardTitle>
                <CardDescription>
                  Manage {selectedTenant.name}'s visual assets
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Logo Upload */}
                <div className="space-y-3">
                  <Label htmlFor="logo">Company Logo</Label>
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center overflow-hidden">
                      {selectedTenant.logo ? (
                        <img 
                          src={selectedTenant.logo} 
                          alt={`${selectedTenant.name} logo`}
                          className="w-full h-full object-contain"
                        />
                      ) : (
                        <Image className="w-6 h-6 text-gray-400" />
                      )}
                    </div>
                    <div className="flex-1">
                      <Input
                        id="logo"
                        type="file"
                        accept="image/*"
                        onChange={(e) => {
                          const file = e.target.files?.[0]
                          if (file) handleLogoUpload(file, 'logo')
                        }}
                        className="mb-2"
                      />
                      <p className="text-xs text-muted-foreground">
                        PNG, JPG up to 2MB. Recommended: 200x60px
                      </p>
                    </div>
                  </div>
                </div>

                <Separator />

                {/* Favicon Upload */}
                <div className="space-y-3">
                  <Label htmlFor="favicon">Favicon</Label>
                  <div className="flex items-center gap-4">
                    <div className="w-8 h-8 border-2 border-dashed border-gray-300 rounded flex items-center justify-center overflow-hidden">
                      {selectedTenant.favicon ? (
                        <img 
                          src={selectedTenant.favicon} 
                          alt={`${selectedTenant.name} favicon`}
                          className="w-full h-full object-contain"
                        />
                      ) : (
                        <Image className="w-3 h-3 text-gray-400" />
                      )}
                    </div>
                    <div className="flex-1">
                      <Input
                        id="favicon"
                        type="file"
                        accept="image/*"
                        onChange={(e) => {
                          const file = e.target.files?.[0]
                          if (file) handleLogoUpload(file, 'favicon')
                        }}
                        className="mb-2"
                      />
                      <p className="text-xs text-muted-foreground">
                        ICO, PNG up to 1MB. Recommended: 32x32px
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Brand Colors */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Palette className="w-5 h-5" />
                  Brand Colors
                </CardTitle>
                <CardDescription>
                  Configure {selectedTenant.name}'s color scheme
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  {/* Primary Color */}
                  <div className="space-y-3">
                    <Label htmlFor="primary-color">Primary Color</Label>
                    <div className="flex items-center gap-3">
                      <Input
                        id="primary-color"
                        type="color"
                        value={selectedTenant.primaryColor}
                        onChange={(e) => handleColorChange('primaryColor', e.target.value)}
                        className="w-12 h-10 p-1 border-2"
                      />
                      <Input
                        type="text"
                        value={selectedTenant.primaryColor}
                        onChange={(e) => handleColorChange('primaryColor', e.target.value)}
                        className="font-mono"
                        placeholder="#000000"
                      />
                    </div>
                  </div>

                  {/* Secondary Color */}
                  <div className="space-y-3">
                    <Label htmlFor="secondary-color">Secondary Color</Label>
                    <div className="flex items-center gap-3">
                      <Input
                        id="secondary-color"
                        type="color"
                        value={selectedTenant.secondaryColor}
                        onChange={(e) => handleColorChange('secondaryColor', e.target.value)}
                        className="w-12 h-10 p-1 border-2"
                      />
                      <Input
                        type="text"
                        value={selectedTenant.secondaryColor}
                        onChange={(e) => handleColorChange('secondaryColor', e.target.value)}
                        className="font-mono"
                        placeholder="#000000"
                      />
                    </div>
                  </div>

                  {/* Gradient Preview */}
                  <div className="space-y-3">
                    <Label>Brand Gradient Preview</Label>
                    <div 
                      className={`h-12 rounded-lg bg-gradient-to-r`}
                      style={{
                        background: `linear-gradient(to right, ${selectedTenant.primaryColor}, ${selectedTenant.secondaryColor})`
                      }}
                    ></div>
                    <p className="text-xs text-muted-foreground">
                      This gradient will be used for buttons, highlights, and accents
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Preview Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="w-5 h-5" />
                Brand Preview
              </CardTitle>
              <CardDescription>
                See how {selectedTenant.name}'s branding will appear
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-50 rounded-lg p-6 space-y-4">
                {/* Header Preview */}
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {selectedTenant.logo && (
                        <img 
                          src={selectedTenant.logo} 
                          alt={`${selectedTenant.name} logo`}
                          className="h-8 object-contain"
                        />
                      )}
                      <span className="font-semibold text-lg">{selectedTenant.name}</span>
                    </div>
                    <Button 
                      size="sm" 
                      style={{ 
                        background: `linear-gradient(to right, ${selectedTenant.primaryColor}, ${selectedTenant.secondaryColor})`,
                        border: 'none',
                        color: 'white'
                      }}
                    >
                      CTA Button
                    </Button>
                  </div>
                </div>

                {/* Card Preview */}
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <div className="flex items-center gap-3 mb-3">
                    <div 
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: selectedTenant.primaryColor }}
                    ></div>
                    <h3 className="font-medium">Sample Card Title</h3>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">
                    This is how content cards will appear with the selected branding.
                  </p>
                  <div 
                    className="h-1 rounded-full"
                    style={{
                      background: `linear-gradient(to right, ${selectedTenant.primaryColor}, ${selectedTenant.secondaryColor})`
                    }}
                  ></div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="tenants">
          <Card>
            <CardHeader>
              <CardTitle>Tenant Management</CardTitle>
              <CardDescription>
                Manage tenant configurations and access permissions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Tenant management interface coming soon...</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="system">
          <Card>
            <CardHeader>
              <CardTitle>System Settings</CardTitle>
              <CardDescription>
                Configure platform-wide settings and preferences
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">System settings interface coming soon...</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="integrations">
          <Card>
            <CardHeader>
              <CardTitle>Platform Integrations</CardTitle>
              <CardDescription>
                Manage third-party integrations and API connections
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Integration settings interface coming soon...</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}