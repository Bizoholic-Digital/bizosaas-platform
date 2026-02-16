'use client'

import { use, useState } from 'react'
import { useRouter } from 'next/navigation'
import {
    ArrowLeft,
    Save,
    RotateCcw,
    Power,
    Settings,
    Sparkles,
    Wrench,
    Key,
    Shield,
    Code,
    Zap,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import { Slider } from '@/components/ui/slider'
import { Checkbox } from '@/components/ui/checkbox'
import { getAgentById } from '@/lib/ai'

export default function AgentConfigPage({
    params,
}: {
    params: Promise<{ agentId: string }>
}) {
    const { agentId } = use(params)
    const router = useRouter()
    const agent = getAgentById(agentId)

    const [isActive, setIsActive] = useState(agent?.status === 'active')
    const [systemPrompt, setSystemPrompt] = useState(agent?.systemPrompt || '')
    const [temperature, setTemperature] = useState(0.7)
    const [maxTokens, setMaxTokens] = useState(2000)

    if (!agent) {
        return (
            <div className="flex-1 p-8">
                <div className="text-center py-12">
                    <h2 className="text-2xl font-bold">Agent Not Found</h2>
                    <p className="text-muted-foreground mt-2">
                        The agent you're looking for doesn't exist.
                    </p>
                    <Button className="mt-4" onClick={() => router.push('/ai-agents')}>
                        Back to Agents
                    </Button>
                </div>
            </div>
        )
    }

    return (
        <div className="flex-1 space-y-6 p-8">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Button variant="ghost" size="icon" onClick={() => router.push('/ai-agents')}>
                        <ArrowLeft className="h-5 w-5" />
                    </Button>
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
                            {agent.name}
                            <Badge variant={isActive ? 'default' : 'secondary'}>
                                {isActive ? 'Active' : 'Inactive'}
                            </Badge>
                        </h1>
                        <p className="text-muted-foreground mt-1">{agent.description}</p>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <Button variant="outline">
                        <RotateCcw className="mr-2 h-4 w-4" />
                        Reset to Default
                    </Button>
                    <Button>
                        <Save className="mr-2 h-4 w-4" />
                        Save Changes
                    </Button>
                </div>
            </div>

            {/* Quick Stats */}
            <div className="grid gap-4 md:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Category</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold capitalize">{agent.category}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Cost Tier</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold capitalize">{agent.costTier}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Capabilities</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{agent.capabilities.length}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Status</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center gap-2">
                            <Switch checked={isActive} onCheckedChange={setIsActive} />
                            <span className="text-sm">{isActive ? 'Enabled' : 'Disabled'}</span>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Configuration Tabs */}
            <Tabs defaultValue="basic" className="space-y-4">
                <TabsList className="grid w-full grid-cols-7">
                    <TabsTrigger value="basic">
                        <Settings className="mr-2 h-4 w-4" />
                        Basic
                    </TabsTrigger>
                    <TabsTrigger value="prompt">
                        <Sparkles className="mr-2 h-4 w-4" />
                        System Prompt
                    </TabsTrigger>
                    <TabsTrigger value="finetuning">
                        <Code className="mr-2 h-4 w-4" />
                        Fine-Tuning
                    </TabsTrigger>
                    <TabsTrigger value="llm">
                        <Zap className="mr-2 h-4 w-4" />
                        LLM Config
                    </TabsTrigger>
                    <TabsTrigger value="tools">
                        <Wrench className="mr-2 h-4 w-4" />
                        Tools
                    </TabsTrigger>
                    <TabsTrigger value="apis">
                        <Key className="mr-2 h-4 w-4" />
                        APIs
                    </TabsTrigger>
                    <TabsTrigger value="permissions">
                        <Shield className="mr-2 h-4 w-4" />
                        Permissions
                    </TabsTrigger>
                </TabsList>

                {/* Basic Settings */}
                <TabsContent value="basic" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Basic Settings</CardTitle>
                            <CardDescription>Configure basic agent properties</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            <div className="space-y-2">
                                <Label htmlFor="agent-name">Agent Name</Label>
                                <Input id="agent-name" defaultValue={agent.name} />
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="description">Description</Label>
                                <Textarea
                                    id="description"
                                    defaultValue={agent.description}
                                    rows={3}
                                />
                            </div>

                            <div className="grid gap-4 md:grid-cols-2">
                                <div className="space-y-2">
                                    <Label htmlFor="cost-tier">Cost Tier</Label>
                                    <Select defaultValue={agent.costTier}>
                                        <SelectTrigger id="cost-tier">
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="free">Free</SelectItem>
                                            <SelectItem value="standard">Standard</SelectItem>
                                            <SelectItem value="premium">Premium</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="priority">Priority</Label>
                                    <Select defaultValue="medium">
                                        <SelectTrigger id="priority">
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="low">Low</SelectItem>
                                            <SelectItem value="medium">Medium</SelectItem>
                                            <SelectItem value="high">High</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>

                            <div className="space-y-3">
                                <Label>Capabilities</Label>
                                <div className="space-y-2">
                                    {agent.capabilities.map((cap) => (
                                        <div key={cap.id} className="flex items-start space-x-2 p-3 border rounded-lg">
                                            <div className="flex-1">
                                                <p className="font-medium">{cap.name}</p>
                                                <p className="text-sm text-muted-foreground">{cap.description}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* System Prompt */}
                <TabsContent value="prompt" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>System Prompt</CardTitle>
                            <CardDescription>
                                Define the agent's behavior and personality (Super Admin only)
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="system-prompt">System Prompt</Label>
                                <Textarea
                                    id="system-prompt"
                                    value={systemPrompt}
                                    onChange={(e) => setSystemPrompt(e.target.value)}
                                    rows={15}
                                    className="font-mono text-sm"
                                    placeholder="You are an expert AI assistant specializing in..."
                                />
                                <p className="text-sm text-muted-foreground">
                                    This prompt defines how the agent behaves and responds to user queries.
                                </p>
                            </div>

                            <div className="flex gap-2">
                                <Button variant="outline">Load Template</Button>
                                <Button variant="outline">Preview</Button>
                                <Button variant="outline">Test Prompt</Button>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* Fine-Tuning Instructions */}
                <TabsContent value="finetuning" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Fine-Tuning Instructions</CardTitle>
                            <CardDescription>
                                Additional instructions to customize agent behavior (Super Admin only)
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="instructions">Custom Instructions</Label>
                                <Textarea
                                    id="instructions"
                                    rows={10}
                                    placeholder="- Always include ROI calculations&#10;- Prioritize cost-per-acquisition metrics&#10;- Suggest A/B testing opportunities"
                                />
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="examples">Example Conversations</Label>
                                <Textarea
                                    id="examples"
                                    rows={10}
                                    placeholder="User: How can I improve my campaigns?&#10;Agent: Based on your data, I recommend..."
                                />
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="constraints">Constraints & Rules</Label>
                                <Textarea
                                    id="constraints"
                                    rows={5}
                                    placeholder="- Never recommend budgets over $10,000&#10;- Always verify data before making suggestions"
                                />
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* LLM Configuration */}
                <TabsContent value="llm" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>LLM Configuration</CardTitle>
                            <CardDescription>Configure the language model settings</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            <div className="grid gap-4 md:grid-cols-2">
                                <div className="space-y-2">
                                    <Label htmlFor="provider">LLM Provider</Label>
                                    <Select defaultValue="openai">
                                        <SelectTrigger id="provider">
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="openai">OpenAI</SelectItem>
                                            <SelectItem value="anthropic">Anthropic (Claude)</SelectItem>
                                            <SelectItem value="openrouter">OpenRouter</SelectItem>
                                            <SelectItem value="google">Google AI (Gemini)</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="model">Model</Label>
                                    <Select defaultValue="gpt-4-turbo-preview">
                                        <SelectTrigger id="model">
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="gpt-4-turbo-preview">GPT-4 Turbo</SelectItem>
                                            <SelectItem value="gpt-4">GPT-4</SelectItem>
                                            <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>

                            <div className="space-y-4">
                                <div className="space-y-2">
                                    <div className="flex items-center justify-between">
                                        <Label>Temperature: {temperature}</Label>
                                        <span className="text-sm text-muted-foreground">Creativity</span>
                                    </div>
                                    <Slider
                                        value={[temperature]}
                                        onValueChange={([value]) => setTemperature(value)}
                                        min={0}
                                        max={2}
                                        step={0.1}
                                    />
                                    <p className="text-xs text-muted-foreground">
                                        Lower = more focused, Higher = more creative
                                    </p>
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="max-tokens">Max Tokens: {maxTokens}</Label>
                                    <Slider
                                        value={[maxTokens]}
                                        onValueChange={([value]) => setMaxTokens(value)}
                                        min={100}
                                        max={4000}
                                        step={100}
                                    />
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="top-p">Top P</Label>
                                    <Slider defaultValue={[1]} min={0} max={1} step={0.1} />
                                </div>

                                <div className="grid gap-4 md:grid-cols-2">
                                    <div className="space-y-2">
                                        <Label htmlFor="frequency-penalty">Frequency Penalty</Label>
                                        <Slider defaultValue={[0]} min={0} max={2} step={0.1} />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="presence-penalty">Presence Penalty</Label>
                                        <Slider defaultValue={[0]} min={0} max={2} step={0.1} />
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* Tools & Services */}
                <TabsContent value="tools" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Available Tools & Services</CardTitle>
                            <CardDescription>
                                Select which tools and services this agent can access
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-3">
                                <Label>Tools</Label>
                                {agent.requiredTools.map((tool) => (
                                    <div key={tool} className="flex items-center space-x-2">
                                        <Checkbox id={`tool-${tool}`} defaultChecked />
                                        <label
                                            htmlFor={`tool-${tool}`}
                                            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                                        >
                                            {tool}
                                        </label>
                                    </div>
                                ))}
                            </div>

                            <div className="space-y-3">
                                <Label>Services</Label>
                                {agent.requiredServices.map((service) => (
                                    <div key={service} className="flex items-center space-x-2">
                                        <Checkbox id={`service-${service}`} defaultChecked />
                                        <label
                                            htmlFor={`service-${service}`}
                                            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                                        >
                                            {service}
                                        </label>
                                    </div>
                                ))}
                            </div>

                            <Button variant="outline" className="w-full">
                                <Wrench className="mr-2 h-4 w-4" />
                                Add Custom Tool
                            </Button>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* API Requirements */}
                <TabsContent value="apis" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Required API Keys</CardTitle>
                            <CardDescription>
                                Configure API keys required by this agent
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {agent.requiredAPIs.length > 0 ? (
                                agent.requiredAPIs.map((api) => (
                                    <div key={api.service} className="p-4 border rounded-lg space-y-2">
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <p className="font-medium capitalize">{api.service.replace('_', ' ')}</p>
                                                <p className="text-sm text-muted-foreground">
                                                    Key Type: {api.keyType}
                                                </p>
                                            </div>
                                            <Badge variant={api.required ? 'destructive' : 'secondary'}>
                                                {api.required ? 'Required' : 'Optional'}
                                            </Badge>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Badge variant="outline">
                                                {api.fallbackToPlatform ? 'Using Platform Key' : 'Not Configured'}
                                            </Badge>
                                            <Button variant="outline" size="sm">
                                                Configure in BYOK
                                            </Button>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <p className="text-muted-foreground text-center py-4">
                                    No API keys required for this agent
                                </p>
                            )}
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* Permissions */}
                <TabsContent value="permissions" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Permissions & Access Control</CardTitle>
                            <CardDescription>
                                Control who can use this agent and set usage limits
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            <div className="space-y-3">
                                <Label>Who can use this agent?</Label>
                                <div className="space-y-2">
                                    <div className="flex items-center space-x-2">
                                        <Checkbox id="all-users" defaultChecked />
                                        <label htmlFor="all-users" className="text-sm font-medium">
                                            All users
                                        </label>
                                    </div>
                                    <div className="flex items-center space-x-2">
                                        <Checkbox id="admins-only" />
                                        <label htmlFor="admins-only" className="text-sm font-medium">
                                            Admins only
                                        </label>
                                    </div>
                                    <div className="flex items-center space-x-2">
                                        <Checkbox id="specific-roles" />
                                        <label htmlFor="specific-roles" className="text-sm font-medium">
                                            Specific roles
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <div className="grid gap-4 md:grid-cols-2">
                                <div className="space-y-2">
                                    <Label htmlFor="max-requests">Max Requests (per user/day)</Label>
                                    <Input id="max-requests" type="number" defaultValue="100" />
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="max-cost">Max Cost (per user/day)</Label>
                                    <Input id="max-cost" type="number" defaultValue="5.00" step="0.01" />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label>Required Permissions</Label>
                                <div className="space-y-2">
                                    {agent.permissions.map((permission) => (
                                        <div key={permission} className="flex items-center space-x-2">
                                            <Checkbox id={`perm-${permission}`} defaultChecked />
                                            <label
                                                htmlFor={`perm-${permission}`}
                                                className="text-sm font-medium"
                                            >
                                                {permission}
                                            </label>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    )
}
