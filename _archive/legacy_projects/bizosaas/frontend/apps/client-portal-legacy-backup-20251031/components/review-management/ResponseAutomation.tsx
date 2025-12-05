"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import {
  Bot,
  MessageSquare,
  Settings,
  Edit,
  Save,
  Plus,
  Trash2,
  CheckCircle,
  XCircle,
  Clock,
  Zap,
  Brain,
  Users,
  Globe,
  Sliders,
  RefreshCw,
  Play,
  Pause
} from 'lucide-react';

interface ResponseTemplate {
  id: string;
  name: string;
  category: string;
  sentiment: string;
  content: string;
  tone: string;
  language: string;
  active: boolean;
  usage_count: number;
  created_at: string;
  updated_at: string;
}

interface AutomationRule {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  conditions: {
    platforms: string[];
    sentiment: string[];
    rating_range: [number, number];
    keywords: string[];
    urgency_level: number;
  };
  actions: {
    auto_respond: boolean;
    require_approval: boolean;
    notify_team: boolean;
    escalate_to: string;
    response_delay: number;
  };
  created_at: string;
  last_triggered: string;
  trigger_count: number;
}

interface WorkflowStatus {
  id: string;
  type: string;
  status: string;
  started_at: string;
  progress: number;
  details: string;
}

export default function ResponseAutomation() {
  const [activeTab, setActiveTab] = useState('templates');
  const [templates, setTemplates] = useState<ResponseTemplate[]>([]);
  const [automationRules, setAutomationRules] = useState<AutomationRule[]>([]);
  const [workflowStatuses, setWorkflowStatuses] = useState<WorkflowStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingTemplate, setEditingTemplate] = useState<ResponseTemplate | null>(null);
  const [editingRule, setEditingRule] = useState<AutomationRule | null>(null);

  useEffect(() => {
    fetchAutomationData();
  }, []);

  const fetchAutomationData = async () => {
    try {
      setLoading(true);
      
      // Fetch response templates
      const templatesResponse = await fetch('/api/brain/review-management/templates');
      const templatesData = await templatesResponse.json();
      setTemplates(templatesData.templates || []);
      
      // Fetch automation rules
      const rulesResponse = await fetch('/api/brain/review-management/automation-rules');
      const rulesData = await rulesResponse.json();
      setAutomationRules(rulesData.rules || []);
      
      // Fetch workflow statuses
      const workflowsResponse = await fetch('/api/brain/review-management/workflows');
      const workflowsData = await workflowsResponse.json();
      setWorkflowStatuses(workflowsData.workflows || []);
      
    } catch (error) {
      console.error('Failed to fetch automation data:', error);
    } finally {
      setLoading(false);
    }
  };

  const saveTemplate = async (template: Partial<ResponseTemplate>) => {
    try {
      const method = template.id ? 'PUT' : 'POST';
      const url = template.id 
        ? `/api/brain/review-management/templates/${template.id}`
        : '/api/brain/review-management/templates';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(template),
      });
      
      if (response.ok) {
        fetchAutomationData();
        setEditingTemplate(null);
      }
    } catch (error) {
      console.error('Failed to save template:', error);
    }
  };

  const deleteTemplate = async (templateId: string) => {
    try {
      const response = await fetch(`/api/brain/review-management/templates/${templateId}`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        fetchAutomationData();
      }
    } catch (error) {
      console.error('Failed to delete template:', error);
    }
  };

  const toggleRule = async (ruleId: string, enabled: boolean) => {
    try {
      const response = await fetch(`/api/brain/review-management/automation-rules/${ruleId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ enabled }),
      });
      
      if (response.ok) {
        fetchAutomationData();
      }
    } catch (error) {
      console.error('Failed to toggle rule:', error);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'bg-green-100 text-green-800';
      case 'negative': return 'bg-red-100 text-red-800';
      case 'neutral': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'paused': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Response Automation</h2>
          <p className="text-muted-foreground">
            Manage AI response templates and automation rules
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={fetchAutomationData}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button>
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="templates">Templates</TabsTrigger>
          <TabsTrigger value="rules">Automation Rules</TabsTrigger>
          <TabsTrigger value="workflows">Active Workflows</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        {/* Response Templates */}
        <TabsContent value="templates" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Response Templates</h3>
            <Dialog>
              <DialogTrigger asChild>
                <Button onClick={() => setEditingTemplate({} as ResponseTemplate)}>
                  <Plus className="h-4 w-4 mr-2" />
                  New Template
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle>
                    {editingTemplate?.id ? 'Edit Template' : 'Create Template'}
                  </DialogTitle>
                  <DialogDescription>
                    Create or modify response templates for automated responses
                  </DialogDescription>
                </DialogHeader>
                
                {editingTemplate && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="name">Template Name</Label>
                        <Input
                          id="name"
                          value={editingTemplate.name || ''}
                          onChange={(e) => setEditingTemplate({
                            ...editingTemplate,
                            name: e.target.value
                          })}
                          placeholder="e.g., Positive Response Template"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="category">Category</Label>
                        <Select
                          value={editingTemplate.category || ''}
                          onValueChange={(value) => setEditingTemplate({
                            ...editingTemplate,
                            category: value
                          })}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select category" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="general">General</SelectItem>
                            <SelectItem value="service">Service</SelectItem>
                            <SelectItem value="product">Product</SelectItem>
                            <SelectItem value="complaint">Complaint</SelectItem>
                            <SelectItem value="praise">Praise</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="sentiment">Sentiment</Label>
                        <Select
                          value={editingTemplate.sentiment || ''}
                          onValueChange={(value) => setEditingTemplate({
                            ...editingTemplate,
                            sentiment: value
                          })}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select sentiment" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="positive">Positive</SelectItem>
                            <SelectItem value="neutral">Neutral</SelectItem>
                            <SelectItem value="negative">Negative</SelectItem>
                            <SelectItem value="mixed">Mixed</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="tone">Tone</Label>
                        <Select
                          value={editingTemplate.tone || ''}
                          onValueChange={(value) => setEditingTemplate({
                            ...editingTemplate,
                            tone: value
                          })}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select tone" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="professional">Professional</SelectItem>
                            <SelectItem value="friendly">Friendly</SelectItem>
                            <SelectItem value="empathetic">Empathetic</SelectItem>
                            <SelectItem value="apologetic">Apologetic</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="language">Language</Label>
                        <Select
                          value={editingTemplate.language || 'en'}
                          onValueChange={(value) => setEditingTemplate({
                            ...editingTemplate,
                            language: value
                          })}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select language" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="en">English</SelectItem>
                            <SelectItem value="es">Spanish</SelectItem>
                            <SelectItem value="fr">French</SelectItem>
                            <SelectItem value="de">German</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="content">Template Content</Label>
                      <Textarea
                        id="content"
                        value={editingTemplate.content || ''}
                        onChange={(e) => setEditingTemplate({
                          ...editingTemplate,
                          content: e.target.value
                        })}
                        placeholder="Enter your response template here. Use variables like {{customer_name}}, {{business_name}}, etc."
                        rows={6}
                      />
                    </div>

                    <div className="flex items-center space-x-2">
                      <Switch
                        id="active"
                        checked={editingTemplate.active || false}
                        onCheckedChange={(checked) => setEditingTemplate({
                          ...editingTemplate,
                          active: checked
                        })}
                      />
                      <Label htmlFor="active">Active template</Label>
                    </div>

                    <div className="flex justify-end gap-2">
                      <Button variant="outline" onClick={() => setEditingTemplate(null)}>
                        Cancel
                      </Button>
                      <Button onClick={() => saveTemplate(editingTemplate)}>
                        <Save className="h-4 w-4 mr-2" />
                        Save Template
                      </Button>
                    </div>
                  </div>
                )}
              </DialogContent>
            </Dialog>
          </div>

          <div className="grid gap-4">
            {templates.map((template) => (
              <Card key={template.id}>
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-lg">{template.name}</CardTitle>
                      <CardDescription>
                        {template.category} • {template.tone} tone
                      </CardDescription>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge className={getSentimentColor(template.sentiment)}>
                        {template.sentiment}
                      </Badge>
                      {template.active ? (
                        <Badge className="bg-green-100 text-green-800">Active</Badge>
                      ) : (
                        <Badge variant="secondary">Inactive</Badge>
                      )}
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setEditingTemplate(template)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => deleteTemplate(template.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-3 line-clamp-3">
                    {template.content}
                  </p>
                  <div className="flex justify-between items-center text-xs text-muted-foreground">
                    <span>Used {template.usage_count} times</span>
                    <span>Updated {new Date(template.updated_at).toLocaleDateString()}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Automation Rules */}
        <TabsContent value="rules" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Automation Rules</h3>
            <Button onClick={() => setEditingRule({} as AutomationRule)}>
              <Plus className="h-4 w-4 mr-2" />
              New Rule
            </Button>
          </div>

          <div className="grid gap-4">
            {automationRules.map((rule) => (
              <Card key={rule.id}>
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-lg">{rule.name}</CardTitle>
                      <CardDescription>{rule.description}</CardDescription>
                    </div>
                    <div className="flex items-center gap-2">
                      <Switch
                        checked={rule.enabled}
                        onCheckedChange={(checked) => toggleRule(rule.id, checked)}
                      />
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setEditingRule(rule)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <Label className="text-xs font-medium">Conditions</Label>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {rule.conditions.platforms.map((platform) => (
                          <Badge key={platform} variant="outline" className="text-xs">
                            {platform}
                          </Badge>
                        ))}
                        {rule.conditions.sentiment.map((sentiment) => (
                          <Badge key={sentiment} className={`${getSentimentColor(sentiment)} text-xs`}>
                            {sentiment}
                          </Badge>
                        ))}
                        <Badge variant="outline" className="text-xs">
                          Rating {rule.conditions.rating_range[0]}-{rule.conditions.rating_range[1]}
                        </Badge>
                      </div>
                    </div>
                    
                    <div>
                      <Label className="text-xs font-medium">Actions</Label>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {rule.actions.auto_respond && (
                          <Badge className="bg-blue-100 text-blue-800 text-xs">Auto Respond</Badge>
                        )}
                        {rule.actions.require_approval && (
                          <Badge className="bg-yellow-100 text-yellow-800 text-xs">Requires Approval</Badge>
                        )}
                        {rule.actions.notify_team && (
                          <Badge className="bg-purple-100 text-purple-800 text-xs">Notify Team</Badge>
                        )}
                        {rule.actions.response_delay > 0 && (
                          <Badge variant="outline" className="text-xs">
                            Delay {rule.actions.response_delay}h
                          </Badge>
                        )}
                      </div>
                    </div>
                    
                    <div className="flex justify-between items-center text-xs text-muted-foreground">
                      <span>Triggered {rule.trigger_count} times</span>
                      <span>
                        Last triggered: {rule.last_triggered 
                          ? new Date(rule.last_triggered).toLocaleDateString()
                          : 'Never'
                        }
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Active Workflows */}
        <TabsContent value="workflows" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Active Workflows</h3>
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                <Pause className="h-4 w-4 mr-2" />
                Pause All
              </Button>
              <Button variant="outline" size="sm">
                <Play className="h-4 w-4 mr-2" />
                Resume All
              </Button>
            </div>
          </div>

          <div className="grid gap-4">
            {workflowStatuses.map((workflow) => (
              <Card key={workflow.id}>
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-lg capitalize">{workflow.type.replace('_', ' ')}</CardTitle>
                      <CardDescription>{workflow.details}</CardDescription>
                    </div>
                    <Badge className={getStatusColor(workflow.status)}>
                      {workflow.status}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <Label className="text-xs font-medium">Progress</Label>
                        <span className="text-xs text-muted-foreground">{workflow.progress}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${workflow.progress}%` }}
                        />
                      </div>
                    </div>
                    
                    <div className="text-xs text-muted-foreground">
                      Started: {new Date(workflow.started_at).toLocaleString()}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
            
            {workflowStatuses.length === 0 && (
              <Card>
                <CardContent className="flex flex-col items-center justify-center py-12">
                  <Bot className="h-12 w-12 text-muted-foreground mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No Active Workflows</h3>
                  <p className="text-muted-foreground text-center">
                    All automation workflows are currently idle
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>

        {/* Settings */}
        <TabsContent value="settings" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Automation Settings</CardTitle>
              <CardDescription>
                Configure global automation behavior and preferences
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <h4 className="text-sm font-medium">Response Generation</h4>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <Label>Auto-generate responses</Label>
                      <p className="text-xs text-muted-foreground">
                        Automatically generate AI responses for new reviews
                      </p>
                    </div>
                    <Switch defaultChecked />
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <Label>Require approval for negative reviews</Label>
                      <p className="text-xs text-muted-foreground">
                        All responses to negative reviews require manual approval
                      </p>
                    </div>
                    <Switch defaultChecked />
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <Label>Smart response delay</Label>
                      <p className="text-xs text-muted-foreground">
                        Add realistic delays to make responses appear more human
                      </p>
                    </div>
                    <Switch />
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="text-sm font-medium">Notifications</h4>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <Label>Email notifications</Label>
                      <p className="text-xs text-muted-foreground">
                        Send email alerts for important review events
                      </p>
                    </div>
                    <Switch defaultChecked />
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <Label>Slack notifications</Label>
                      <p className="text-xs text-muted-foreground">
                        Send alerts to configured Slack channels
                      </p>
                    </div>
                    <Switch />
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="text-sm font-medium">AI Model Settings</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Response model</Label>
                    <Select defaultValue="gpt-4">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="gpt-4">GPT-4 (Recommended)</SelectItem>
                        <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                        <SelectItem value="claude-3">Claude 3</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="space-y-2">
                    <Label>Response creativity</Label>
                    <Select defaultValue="balanced">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="conservative">Conservative</SelectItem>
                        <SelectItem value="balanced">Balanced</SelectItem>
                        <SelectItem value="creative">Creative</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

              <div className="flex justify-end">
                <Button>
                  <Save className="h-4 w-4 mr-2" />
                  Save Settings
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}