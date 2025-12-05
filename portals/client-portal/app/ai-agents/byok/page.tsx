'use client'

import { useState } from 'react'
import {
    Plus,
    Key,
    Check,
    X,
    Eye,
    EyeOff,
    RotateCcw,
    Trash2,
    TestTube,
    ExternalLink,
    AlertCircle,
    CheckCircle,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Progress } from '@/components/ui/progress'
import { SERVICE_CATALOG, maskAPIKey, validateKeyFormat, calculateKeyStrength, type ServiceId } from '@/lib/ai'

export default function BYOKManagementPage() {
    const [selectedCategory, setSelectedCategory] = useState<string>('all')
    const [showAddDialog, setShowAddDialog] = useState(false)
    const [selectedService, setSelectedService] = useState<ServiceId | ''>('')
    const [selectedKeyType, setSelectedKeyType] = useState('')
    const [keyValue, setKeyValue] = useState('')
    const [showKey, setShowKey] = useState(false)
    const [isValidating, setIsValidating] = useState(false)

    // Mock data - would come from API
    const [configuredKeys, setConfiguredKeys] = useState<Record<string, any>>({
        openai: {
            service: 'openai',
            keyType: 'api_key',
            value: 'sk-proj-1234567890abcdefghijklmnopqrstuvwxyz1234',
            isValid: true,
            lastUsed: '2 hours ago',
            requests: 1234,
            cost: 12.45,
        },
        stripe: {
            service: 'stripe',
            keyType: 'secret_key',
            value: 'sk_live_placeholder_key_DoNotUse',
            isValid: true,
            lastUsed: '1 day ago',
            requests: 456,
            cost: 0,
        },
    })

    const categories = [
        { value: 'all', label: 'All Services' },
        { value: 'ai', label: 'AI Services' },
        { value: 'marketing', label: 'Marketing' },
        { value: 'payment', label: 'Payment' },
        { value: 'analytics', label: 'Analytics' },
        { value: 'email', label: 'Email' },
        { value: 'sms', label: 'SMS' },
        { value: 'storage', label: 'Storage' },
        { value: 'crm', label: 'CRM' },
    ]

    interface ServiceConfig {
        name: string;
        category: string;
        keyTypes: readonly string[];
        requiredKeys: readonly string[];
        documentation: string;
    }

    const services = (Object.entries(SERVICE_CATALOG) as [string, ServiceConfig][]).filter(([_, service]) =>
        selectedCategory === 'all' || service.category === selectedCategory
    )

    const handleValidateKey = () => {
        if (!selectedService || !selectedKeyType || !keyValue) return

        setIsValidating(true)
        // Simulate API call
        setTimeout(() => {
            setIsValidating(false)
            // Would call actual validation API
        }, 1500)
    }

    const handleAddKey = () => {
        if (!selectedService || !selectedKeyType || !keyValue) return

        setConfiguredKeys({
            ...configuredKeys,
            [selectedService]: {
                service: selectedService,
                keyType: selectedKeyType,
                value: keyValue,
                isValid: true,
                lastUsed: 'Never',
                requests: 0,
                cost: 0,
            },
        })

        // Reset form
        setSelectedService('')
        setSelectedKeyType('')
        setKeyValue('')
        setShowAddDialog(false)
    }

    const handleDeleteKey = (serviceId: string) => {
        const newKeys = { ...configuredKeys }
        delete newKeys[serviceId]
        setConfiguredKeys(newKeys)
    }

    const validation = selectedService && selectedKeyType && keyValue
        ? validateKeyFormat(selectedService as ServiceId, selectedKeyType, keyValue)
        : null

    const keyStrength = keyValue ? calculateKeyStrength(keyValue) : 0

    return (
        <div className="flex-1 space-y-6 p-8">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
                        <Key className="h-8 w-8 text-blue-600" />
                        BYOK Management
                    </h1>
                    <p className="text-muted-foreground mt-1">
                        Bring Your Own Keys - Manage API keys for all services
                    </p>
                </div>
                <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
                    <DialogTrigger asChild>
                        <Button>
                            <Plus className="mr-2 h-4 w-4" />
                            Add API Key
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="max-w-2xl">
                        <DialogHeader>
                            <DialogTitle>Add API Key</DialogTitle>
                            <DialogDescription>
                                Add a new API key for any service. Your keys are encrypted and stored securely in HashiCorp Vault.
                            </DialogDescription>
                        </DialogHeader>

                        <div className="space-y-4 py-4">
                            <div className="space-y-2">
                                <Label htmlFor="service">Service</Label>
                                <Select value={selectedService} onValueChange={(value) => {
                                    setSelectedService(value as ServiceId)
                                    setSelectedKeyType('')
                                    setKeyValue('')
                                }}>
                                    <SelectTrigger id="service">
                                        <SelectValue placeholder="Select a service" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {(Object.entries(SERVICE_CATALOG) as [string, ServiceConfig][]).map(([id, service]) => (
                                            <SelectItem key={id} value={id}>
                                                {service.name} ({service.category})
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>

                            {selectedService && (
                                <div className="space-y-2">
                                    <Label htmlFor="key-type">Key Type</Label>
                                    <Select value={selectedKeyType} onValueChange={setSelectedKeyType}>
                                        <SelectTrigger id="key-type">
                                            <SelectValue placeholder="Select key type" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {SERVICE_CATALOG[selectedService as ServiceId].keyTypes.map((type) => (
                                                <SelectItem key={type} value={type}>
                                                    {type.replace('_', ' ')}
                                                    {SERVICE_CATALOG[selectedService as ServiceId].requiredKeys.includes(type) && (
                                                        <Badge variant="destructive" className="ml-2">Required</Badge>
                                                    )}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>
                            )}

                            {selectedKeyType && (
                                <>
                                    <div className="space-y-2">
                                        <Label htmlFor="key-value">API Key</Label>
                                        <div className="relative">
                                            <Input
                                                id="key-value"
                                                type={showKey ? 'text' : 'password'}
                                                value={keyValue}
                                                onChange={(e) => setKeyValue(e.target.value)}
                                                placeholder="Enter your API key"
                                                className="pr-10"
                                            />
                                            <Button
                                                type="button"
                                                variant="ghost"
                                                size="icon"
                                                className="absolute right-0 top-0"
                                                onClick={() => setShowKey(!showKey)}
                                            >
                                                {showKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                            </Button>
                                        </div>
                                    </div>

                                    {keyValue && (
                                        <>
                                            {/* Validation */}
                                            {validation && (
                                                <Alert variant={validation.isValid ? 'default' : 'destructive'}>
                                                    {validation.isValid ? (
                                                        <CheckCircle className="h-4 w-4" />
                                                    ) : (
                                                        <AlertCircle className="h-4 w-4" />
                                                    )}
                                                    <AlertTitle>
                                                        {validation.isValid ? 'Valid Format' : 'Invalid Format'}
                                                    </AlertTitle>
                                                    <AlertDescription>
                                                        {validation.error || 'Key format is correct'}
                                                    </AlertDescription>
                                                </Alert>
                                            )}

                                            {/* Key Strength */}
                                            <div className="space-y-2">
                                                <div className="flex items-center justify-between text-sm">
                                                    <Label>Key Strength</Label>
                                                    <span className="font-medium">{keyStrength}/100</span>
                                                </div>
                                                <Progress value={keyStrength} className="h-2" />
                                                <p className="text-xs text-muted-foreground">
                                                    {keyStrength < 50 && 'Weak - Consider using a stronger key'}
                                                    {keyStrength >= 50 && keyStrength < 75 && 'Moderate - Acceptable'}
                                                    {keyStrength >= 75 && 'Strong - Excellent security'}
                                                </p>
                                            </div>

                                            {/* Documentation Link */}
                                            {selectedService && (
                                                <Alert>
                                                    <ExternalLink className="h-4 w-4" />
                                                    <AlertTitle>Need help?</AlertTitle>
                                                    <AlertDescription>
                                                        <a
                                                            href={SERVICE_CATALOG[selectedService as ServiceId].documentation}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            className="text-blue-600 hover:underline"
                                                        >
                                                            View {SERVICE_CATALOG[selectedService as ServiceId].name} documentation
                                                        </a>
                                                    </AlertDescription>
                                                </Alert>
                                            )}
                                        </>
                                    )}
                                </>
                            )}
                        </div>

                        <DialogFooter>
                            <Button variant="outline" onClick={() => setShowAddDialog(false)}>
                                Cancel
                            </Button>
                            <Button
                                variant="outline"
                                onClick={handleValidateKey}
                                disabled={!validation?.isValid || isValidating}
                            >
                                <TestTube className="mr-2 h-4 w-4" />
                                {isValidating ? 'Testing...' : 'Test Key'}
                            </Button>
                            <Button
                                onClick={handleAddKey}
                                disabled={!validation?.isValid}
                            >
                                <Plus className="mr-2 h-4 w-4" />
                                Add Key
                            </Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            {/* Stats */}
            <div className="grid gap-4 md:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Services</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{Object.keys(SERVICE_CATALOG).length}</div>
                        <p className="text-xs text-muted-foreground">Available integrations</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Configured</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-green-600">
                            {Object.keys(configuredKeys).length}
                        </div>
                        <p className="text-xs text-muted-foreground">Keys configured</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">This Month</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {Object.values(configuredKeys).reduce((sum, k) => sum + k.requests, 0)}
                        </div>
                        <p className="text-xs text-muted-foreground">Total requests</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Cost</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            ${Object.values(configuredKeys).reduce((sum, k) => sum + k.cost, 0).toFixed(2)}
                        </div>
                        <p className="text-xs text-muted-foreground">Using your keys</p>
                    </CardContent>
                </Card>
            </div>

            {/* Tabs */}
            <Tabs defaultValue="configured" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="configured">Configured Keys</TabsTrigger>
                    <TabsTrigger value="available">Available Services</TabsTrigger>
                </TabsList>

                {/* Configured Keys */}
                <TabsContent value="configured" className="space-y-4">
                    {Object.keys(configuredKeys).length === 0 ? (
                        <Card>
                            <CardContent className="flex flex-col items-center justify-center py-12">
                                <Key className="h-12 w-12 text-muted-foreground mb-4" />
                                <h3 className="text-lg font-semibold mb-2">No API Keys Configured</h3>
                                <p className="text-muted-foreground text-center mb-4">
                                    Add your first API key to start using BYOK features
                                </p>
                                <Button onClick={() => setShowAddDialog(true)}>
                                    <Plus className="mr-2 h-4 w-4" />
                                    Add API Key
                                </Button>
                            </CardContent>
                        </Card>
                    ) : (
                        <div className="space-y-4">
                            {Object.entries(configuredKeys).map(([serviceId, key]) => {
                                const service = SERVICE_CATALOG[serviceId as ServiceId]
                                return (
                                    <Card key={serviceId}>
                                        <CardHeader>
                                            <div className="flex items-start justify-between">
                                                <div className="flex-1">
                                                    <CardTitle className="flex items-center gap-2">
                                                        {service.name}
                                                        <Badge variant={key.isValid ? 'default' : 'destructive'}>
                                                            {key.isValid ? 'Valid' : 'Invalid'}
                                                        </Badge>
                                                    </CardTitle>
                                                    <CardDescription className="mt-1">
                                                        Category: {service.category} • Key Type: {key.keyType}
                                                    </CardDescription>
                                                </div>
                                            </div>
                                        </CardHeader>
                                        <CardContent>
                                            <div className="space-y-4">
                                                {/* Key Value */}
                                                <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                                                    <code className="text-sm font-mono">
                                                        {maskAPIKey(key.value)}
                                                    </code>
                                                    <div className="flex gap-2">
                                                        <Button variant="ghost" size="icon">
                                                            <Eye className="h-4 w-4" />
                                                        </Button>
                                                    </div>
                                                </div>

                                                {/* Stats */}
                                                <div className="grid grid-cols-3 gap-4 text-sm">
                                                    <div>
                                                        <p className="text-muted-foreground">Last Used</p>
                                                        <p className="font-medium">{key.lastUsed}</p>
                                                    </div>
                                                    <div>
                                                        <p className="text-muted-foreground">Requests</p>
                                                        <p className="font-medium">{key.requests.toLocaleString()}</p>
                                                    </div>
                                                    <div>
                                                        <p className="text-muted-foreground">Cost</p>
                                                        <p className="font-medium">${key.cost.toFixed(2)}</p>
                                                    </div>
                                                </div>

                                                {/* Actions */}
                                                <div className="flex gap-2">
                                                    <Button variant="outline" size="sm">
                                                        <TestTube className="mr-2 h-4 w-4" />
                                                        Test Key
                                                    </Button>
                                                    <Button variant="outline" size="sm">
                                                        <RotateCcw className="mr-2 h-4 w-4" />
                                                        Rotate Key
                                                    </Button>
                                                    <Button
                                                        variant="outline"
                                                        size="sm"
                                                        className="text-destructive"
                                                        onClick={() => handleDeleteKey(serviceId)}
                                                    >
                                                        <Trash2 className="mr-2 h-4 w-4" />
                                                        Delete
                                                    </Button>
                                                </div>
                                            </div>
                                        </CardContent>
                                    </Card>
                                )
                            })}
                        </div>
                    )}
                </TabsContent>

                {/* Available Services */}
                <TabsContent value="available" className="space-y-4">
                    {/* Category Filter */}
                    <div className="flex gap-2">
                        {categories.map((cat) => (
                            <Button
                                key={cat.value}
                                variant={selectedCategory === cat.value ? 'default' : 'outline'}
                                size="sm"
                                onClick={() => setSelectedCategory(cat.value)}
                            >
                                {cat.label}
                            </Button>
                        ))}
                    </div>

                    {/* Services Grid */}
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {services.map(([id, service]) => {
                            const isConfigured = configuredKeys[id]
                            return (
                                <Card key={id} className={isConfigured ? 'border-green-500' : ''}>
                                    <CardHeader>
                                        <div className="flex items-start justify-between">
                                            <div className="flex-1">
                                                <CardTitle className="text-lg">{service.name}</CardTitle>
                                                <CardDescription className="mt-1">
                                                    {service.category}
                                                </CardDescription>
                                            </div>
                                            {isConfigured && (
                                                <Badge variant="default">
                                                    <Check className="mr-1 h-3 w-3" />
                                                    Configured
                                                </Badge>
                                            )}
                                        </div>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="space-y-3">
                                            <div className="text-sm">
                                                <p className="text-muted-foreground mb-2">Required Keys:</p>
                                                <div className="flex flex-wrap gap-1">
                                                    {service.keyTypes.map((type) => (
                                                        <Badge key={type} variant="outline" className="text-xs">
                                                            {type}
                                                            {service.requiredKeys.includes(type) && ' *'}
                                                        </Badge>
                                                    ))}
                                                </div>
                                            </div>
                                            <div className="flex gap-2">
                                                <Button
                                                    className="flex-1"
                                                    size="sm"
                                                    variant={isConfigured ? 'outline' : 'default'}
                                                    onClick={() => {
                                                        setSelectedService(id as ServiceId)
                                                        setShowAddDialog(true)
                                                    }}
                                                >
                                                    {isConfigured ? 'Update' : 'Configure'}
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    asChild
                                                >
                                                    <a href={service.documentation} target="_blank" rel="noopener noreferrer">
                                                        <ExternalLink className="h-4 w-4" />
                                                    </a>
                                                </Button>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            )
                        })}
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    )
}
