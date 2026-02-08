"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Shield,
  AlertTriangle,
  CheckCircle,
  Bell,
  Settings,
  Zap,
  TrendingDown,
  Eye,
  Play,
  Pause,
  RefreshCw
} from 'lucide-react';

interface MonitoringAlert {
  id: string;
  type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  timestamp: string;
  acknowledged: boolean;
  resolved: boolean;
}

interface MonitoringSettings {
  enabled: boolean;
  alertThresholds: {
    ratingDrop: number;
    negativeReviewSpike: number;
    responseTimeExceeded: number;
    competitorGap: number;
  };
  notificationChannels: {
    email: boolean;
    slack: boolean;
    sms: boolean;
    webhook: boolean;
  };
}

export default function ReputationMonitoring() {
  const [alerts, setAlerts] = useState<MonitoringAlert[]>([]);
  const [settings, setSettings] = useState<MonitoringSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [monitoring, setMonitoring] = useState(true);

  useEffect(() => {
    fetchMonitoringData();
    const interval = setInterval(fetchMonitoringData, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchMonitoringData = async () => {
    try {
      const [alertsResponse, settingsResponse] = await Promise.all([
        fetch('/api/brain/review-management/alerts'),
        fetch('/api/brain/review-management/monitoring-settings')
      ]);
      
      const alertsData = await alertsResponse.json();
      const settingsData = await settingsResponse.json();
      
      setAlerts(alertsData.alerts || []);
      setSettings(settingsData.settings || null);
    } catch (error) {
      console.error('Failed to fetch monitoring data:', error);
    } finally {
      setLoading(false);
    }
  };

  const acknowledgeAlert = async (alertId: string) => {
    try {
      await fetch(`/api/brain/review-management/alerts/${alertId}/acknowledge`, {
        method: 'POST'
      });
      fetchMonitoringData();
    } catch (error) {
      console.error('Failed to acknowledge alert:', error);
    }
  };

  const resolveAlert = async (alertId: string) => {
    try {
      await fetch(`/api/brain/review-management/alerts/${alertId}/resolve`, {
        method: 'POST'
      });
      fetchMonitoringData();
    } catch (error) {
      console.error('Failed to resolve alert:', error);
    }
  };

  const toggleMonitoring = async () => {
    try {
      const newStatus = !monitoring;
      await fetch('/api/brain/review-management/monitoring', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled: newStatus })
      });
      setMonitoring(newStatus);
    } catch (error) {
      console.error('Failed to toggle monitoring:', error);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-300';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'low': return 'bg-blue-100 text-blue-800 border-blue-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
      case 'high':
        return <AlertTriangle className="h-4 w-4" />;
      case 'medium':
        return <Eye className="h-4 w-4" />;
      case 'low':
        return <Bell className="h-4 w-4" />;
      default:
        return <Bell className="h-4 w-4" />;
    }
  };

  const activeAlerts = alerts.filter(alert => !alert.resolved);
  const criticalAlerts = activeAlerts.filter(alert => alert.severity === 'critical').length;
  const highAlerts = activeAlerts.filter(alert => alert.severity === 'high').length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Reputation Monitoring</h2>
          <p className="text-muted-foreground">
            Real-time monitoring and alerts for your online reputation
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant={monitoring ? "default" : "outline"}
            onClick={toggleMonitoring}
          >
            {monitoring ? (
              <>
                <Pause className="h-4 w-4 mr-2" />
                Pause Monitoring
              </>
            ) : (
              <>
                <Play className="h-4 w-4 mr-2" />
                Resume Monitoring
              </>
            )}
          </Button>
          <Button variant="outline" onClick={fetchMonitoringData}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Monitoring Status */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                Monitoring Status
              </CardTitle>
              <CardDescription>
                Current monitoring status and alert summary
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${
                monitoring ? 'bg-green-500' : 'bg-red-500'
              }`} />
              <span className="text-sm font-medium">
                {monitoring ? 'Active' : 'Paused'}
              </span>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4 border rounded-lg">
              <div className="text-2xl font-bold text-red-600">{criticalAlerts}</div>
              <div className="text-sm text-muted-foreground">Critical Alerts</div>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <div className="text-2xl font-bold text-orange-600">{highAlerts}</div>
              <div className="text-sm text-muted-foreground">High Priority</div>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <div className="text-2xl font-bold text-green-600">{activeAlerts.length}</div>
              <div className="text-sm text-muted-foreground">Total Active</div>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{alerts.length - activeAlerts.length}</div>
              <div className="text-sm text-muted-foreground">Resolved</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Active Alerts */}
      <Card>
        <CardHeader>
          <CardTitle>Active Alerts</CardTitle>
          <CardDescription>
            Recent alerts requiring attention
          </CardDescription>
        </CardHeader>
        <CardContent>
          {activeAlerts.length === 0 ? (
            <div className="text-center py-8">
              <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">All Clear!</h3>
              <p className="text-muted-foreground">
                No active alerts. Your reputation monitoring is working smoothly.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {activeAlerts.map((alert) => (
                <Alert key={alert.id} className={getSeverityColor(alert.severity)}>
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3">
                      {getSeverityIcon(alert.severity)}
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <Badge className={getSeverityColor(alert.severity)}>
                            {alert.severity.toUpperCase()}
                          </Badge>
                          <Badge variant="outline">
                            {alert.type.replace('_', ' ')}
                          </Badge>
                        </div>
                        <AlertDescription className="text-sm">
                          {alert.message}
                        </AlertDescription>
                        <div className="text-xs text-muted-foreground mt-2">
                          {new Date(alert.timestamp).toLocaleString()}
                        </div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      {!alert.acknowledged && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => acknowledgeAlert(alert.id)}
                        >
                          <Eye className="h-4 w-4 mr-1" />
                          Acknowledge
                        </Button>
                      )}
                      <Button
                        size="sm"
                        onClick={() => resolveAlert(alert.id)}
                      >
                        <CheckCircle className="h-4 w-4 mr-1" />
                        Resolve
                      </Button>
                    </div>
                  </div>
                </Alert>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Monitoring Settings */}
      {settings && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              Monitoring Settings
            </CardTitle>
            <CardDescription>
              Configure alert thresholds and notification preferences
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <h4 className="text-sm font-medium">Alert Thresholds</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="rating-drop">Rating Drop Threshold</Label>
                  <Input
                    id="rating-drop"
                    type="number"
                    step="0.1"
                    value={settings.alertThresholds.ratingDrop}
                    onChange={(e) => {
                      const newSettings = {
                        ...settings,
                        alertThresholds: {
                          ...settings.alertThresholds,
                          ratingDrop: parseFloat(e.target.value)
                        }
                      };
                      setSettings(newSettings);
                    }}
                  />
                  <p className="text-xs text-muted-foreground">
                    Alert when average rating drops by this amount
                  </p>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="negative-spike">Negative Review Spike</Label>
                  <Input
                    id="negative-spike"
                    type="number"
                    value={settings.alertThresholds.negativeReviewSpike}
                    onChange={(e) => {
                      const newSettings = {
                        ...settings,
                        alertThresholds: {
                          ...settings.alertThresholds,
                          negativeReviewSpike: parseInt(e.target.value)
                        }
                      };
                      setSettings(newSettings);
                    }}
                  />
                  <p className="text-xs text-muted-foreground">
                    Alert when this many negative reviews received in 24h
                  </p>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="response-time">Response Time Exceeded</Label>
                  <Input
                    id="response-time"
                    type="number"
                    value={settings.alertThresholds.responseTimeExceeded}
                    onChange={(e) => {
                      const newSettings = {
                        ...settings,
                        alertThresholds: {
                          ...settings.alertThresholds,
                          responseTimeExceeded: parseInt(e.target.value)
                        }
                      };
                      setSettings(newSettings);
                    }}
                  />
                  <p className="text-xs text-muted-foreground">
                    Alert when response time exceeds this many hours
                  </p>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="competitor-gap">Competitor Gap</Label>
                  <Input
                    id="competitor-gap"
                    type="number"
                    step="0.1"
                    value={settings.alertThresholds.competitorGap}
                    onChange={(e) => {
                      const newSettings = {
                        ...settings,
                        alertThresholds: {
                          ...settings.alertThresholds,
                          competitorGap: parseFloat(e.target.value)
                        }
                      };
                      setSettings(newSettings);
                    }}
                  />
                  <p className="text-xs text-muted-foreground">
                    Alert when competitors exceed rating by this amount
                  </p>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-sm font-medium">Notification Channels</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div>
                    <Label>Email Notifications</Label>
                    <p className="text-xs text-muted-foreground">
                      Send alerts via email
                    </p>
                  </div>
                  <Switch
                    checked={settings.notificationChannels.email}
                    onCheckedChange={(checked) => {
                      const newSettings = {
                        ...settings,
                        notificationChannels: {
                          ...settings.notificationChannels,
                          email: checked
                        }
                      };
                      setSettings(newSettings);
                    }}
                  />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <Label>Slack Notifications</Label>
                    <p className="text-xs text-muted-foreground">
                      Send alerts to Slack channel
                    </p>
                  </div>
                  <Switch
                    checked={settings.notificationChannels.slack}
                    onCheckedChange={(checked) => {
                      const newSettings = {
                        ...settings,
                        notificationChannels: {
                          ...settings.notificationChannels,
                          slack: checked
                        }
                      };
                      setSettings(newSettings);
                    }}
                  />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <Label>SMS Notifications</Label>
                    <p className="text-xs text-muted-foreground">
                      Send critical alerts via SMS
                    </p>
                  </div>
                  <Switch
                    checked={settings.notificationChannels.sms}
                    onCheckedChange={(checked) => {
                      const newSettings = {
                        ...settings,
                        notificationChannels: {
                          ...settings.notificationChannels,
                          sms: checked
                        }
                      };
                      setSettings(newSettings);
                    }}
                  />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <Label>Webhook Notifications</Label>
                    <p className="text-xs text-muted-foreground">
                      Send alerts to custom webhook
                    </p>
                  </div>
                  <Switch
                    checked={settings.notificationChannels.webhook}
                    onCheckedChange={(checked) => {
                      const newSettings = {
                        ...settings,
                        notificationChannels: {
                          ...settings.notificationChannels,
                          webhook: checked
                        }
                      };
                      setSettings(newSettings);
                    }}
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-end">
              <Button onClick={() => {
                // Save settings
                fetch('/api/brain/review-management/monitoring-settings', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(settings)
                });
              }}>
                Save Settings
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}