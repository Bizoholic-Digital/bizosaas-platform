'use client';

import React, { useState, useEffect, createContext, useContext } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { 
  Shield,
  Users,
  Key,
  Lock,
  Unlock,
  Eye,
  EyeOff,
  Settings,
  Edit,
  Trash2,
  Plus,
  Crown,
  UserCheck,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
  Calendar,
  Globe,
  Database,
  Server,
  Network,
  FileText,
  Activity,
  Ban,
  UserX
} from 'lucide-react';

// Role and permission interfaces
interface Permission {
  id: string;
  name: string;
  description: string;
  category: 'agent_management' | 'configuration' | 'monitoring' | 'tasks' | 'analytics' | 'system';
  level: 'read' | 'write' | 'execute' | 'admin';
  resource?: string; // specific agent, domain, or resource
}

interface Role {
  id: string;
  name: string;
  description: string;
  level: 'super_admin' | 'platform_admin' | 'domain_admin' | 'agent_operator' | 'viewer';
  permissions: Permission[];
  restrictions: {
    allowedDomains?: string[];
    allowedAgents?: string[];
    timeRestrictions?: {
      startTime: string;
      endTime: string;
      allowedDays: number[]; // 0-6 (Sunday-Saturday)
    };
    ipRestrictions?: string[];
    maxSessions?: number;
  };
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

interface User {
  id: string;
  email: string;
  name: string;
  role: Role;
  lastLogin?: Date;
  sessionCount: number;
  isActive: boolean;
  failedLoginAttempts: number;
  lockedUntil?: Date;
  permissions: Permission[]; // effective permissions (role + user-specific)
  auditLog: AuditEntry[];
}

interface AuditEntry {
  id: string;
  userId: string;
  action: string;
  resource: string;
  timestamp: Date;
  ipAddress: string;
  userAgent: string;
  success: boolean;
  details?: any;
}

// Access control context
interface AccessControlContextType {
  currentUser: User | null;
  hasPermission: (permission: string, resource?: string) => boolean;
  hasRole: (role: string) => boolean;
  canAccessAgent: (agentId: string) => boolean;
  canAccessDomain: (domain: string) => boolean;
}

const AccessControlContext = createContext<AccessControlContextType | null>(null);

export const useAccessControl = () => {
  const context = useContext(AccessControlContext);
  if (!context) {
    throw new Error('useAccessControl must be used within an AccessControlProvider');
  }
  return context;
};

// Mock data
const mockPermissions: Permission[] = [
  // Agent Management
  { id: 'agent.view', name: 'View Agents', description: 'View agent status and basic information', category: 'agent_management', level: 'read' },
  { id: 'agent.configure', name: 'Configure Agents', description: 'Modify agent settings and configurations', category: 'agent_management', level: 'write' },
  { id: 'agent.start_stop', name: 'Start/Stop Agents', description: 'Start, stop, or restart agents', category: 'agent_management', level: 'execute' },
  { id: 'agent.delete', name: 'Delete Agents', description: 'Permanently delete agents', category: 'agent_management', level: 'admin' },
  
  // Configuration
  { id: 'config.view', name: 'View Configuration', description: 'View system and agent configurations', category: 'configuration', level: 'read' },
  { id: 'config.modify', name: 'Modify Configuration', description: 'Change system and agent configurations', category: 'configuration', level: 'write' },
  { id: 'config.deploy', name: 'Deploy Configuration', description: 'Deploy configuration changes', category: 'configuration', level: 'execute' },
  
  // Monitoring
  { id: 'monitor.view', name: 'View Monitoring', description: 'Access monitoring dashboards and metrics', category: 'monitoring', level: 'read' },
  { id: 'monitor.alerts', name: 'Manage Alerts', description: 'Configure and manage monitoring alerts', category: 'monitoring', level: 'write' },
  
  // Tasks
  { id: 'task.view', name: 'View Tasks', description: 'View task status and history', category: 'tasks', level: 'read' },
  { id: 'task.create', name: 'Create Tasks', description: 'Create and assign new tasks', category: 'tasks', level: 'write' },
  { id: 'task.manage', name: 'Manage Tasks', description: 'Modify, cancel, or reassign tasks', category: 'tasks', level: 'execute' },
  
  // Analytics
  { id: 'analytics.view', name: 'View Analytics', description: 'Access performance analytics and reports', category: 'analytics', level: 'read' },
  { id: 'analytics.export', name: 'Export Analytics', description: 'Export analytics data and reports', category: 'analytics', level: 'write' },
  
  // System
  { id: 'system.admin', name: 'System Administration', description: 'Full system administration access', category: 'system', level: 'admin' },
  { id: 'user.manage', name: 'User Management', description: 'Manage users and their permissions', category: 'system', level: 'admin' },
  { id: 'audit.view', name: 'View Audit Logs', description: 'Access system audit logs', category: 'system', level: 'read' }
];

const mockRoles: Role[] = [
  {
    id: 'super-admin',
    name: 'Super Administrator',
    description: 'Full system access with all permissions',
    level: 'super_admin',
    permissions: mockPermissions, // All permissions
    restrictions: {},
    isActive: true,
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-01')
  },
  {
    id: 'platform-admin',
    name: 'Platform Administrator',
    description: 'Platform-wide administration with most permissions',
    level: 'platform_admin',
    permissions: mockPermissions.filter(p => p.level !== 'admin' || p.category !== 'system'),
    restrictions: {
      timeRestrictions: {
        startTime: '06:00',
        endTime: '22:00',
        allowedDays: [1, 2, 3, 4, 5] // Monday to Friday
      },
      maxSessions: 3
    },
    isActive: true,
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-01')
  },
  {
    id: 'domain-admin',
    name: 'Domain Administrator',
    description: 'Administrative access within specific domains',
    level: 'domain_admin',
    permissions: mockPermissions.filter(p => 
      p.category === 'agent_management' || 
      p.category === 'configuration' || 
      p.category === 'monitoring' ||
      (p.category === 'tasks' && p.level !== 'admin')
    ),
    restrictions: {
      allowedDomains: ['CRM', 'E-commerce'],
      timeRestrictions: {
        startTime: '08:00',
        endTime: '18:00',
        allowedDays: [1, 2, 3, 4, 5]
      },
      maxSessions: 2
    },
    isActive: true,
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-01')
  },
  {
    id: 'agent-operator',
    name: 'Agent Operator',
    description: 'Operational access to manage agents and tasks',
    level: 'agent_operator',
    permissions: mockPermissions.filter(p => 
      (p.category === 'agent_management' && p.level !== 'admin') ||
      p.category === 'monitoring' ||
      p.category === 'tasks'
    ),
    restrictions: {
      allowedAgents: ['lead-scoring-agent', 'content-creation-agent'],
      maxSessions: 1
    },
    isActive: true,
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-01')
  },
  {
    id: 'viewer',
    name: 'Viewer',
    description: 'Read-only access to monitoring and analytics',
    level: 'viewer',
    permissions: mockPermissions.filter(p => p.level === 'read'),
    restrictions: {
      timeRestrictions: {
        startTime: '09:00',
        endTime: '17:00',
        allowedDays: [1, 2, 3, 4, 5]
      },
      maxSessions: 1
    },
    isActive: true,
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-01')
  }
];

const mockUsers: User[] = [
  {
    id: 'user-1',
    email: 'admin@bizosaas.com',
    name: 'System Administrator',
    role: mockRoles[0], // Super Admin
    lastLogin: new Date(),
    sessionCount: 1,
    isActive: true,
    failedLoginAttempts: 0,
    permissions: mockRoles[0].permissions,
    auditLog: []
  },
  {
    id: 'user-2',
    email: 'platform.admin@bizosaas.com',
    name: 'Platform Manager',
    role: mockRoles[1], // Platform Admin
    lastLogin: new Date(Date.now() - 3600000),
    sessionCount: 2,
    isActive: true,
    failedLoginAttempts: 0,
    permissions: mockRoles[1].permissions,
    auditLog: []
  },
  {
    id: 'user-3',
    email: 'crm.admin@bizosaas.com',
    name: 'CRM Domain Lead',
    role: mockRoles[2], // Domain Admin
    lastLogin: new Date(Date.now() - 7200000),
    sessionCount: 1,
    isActive: true,
    failedLoginAttempts: 1,
    permissions: mockRoles[2].permissions,
    auditLog: []
  }
];

// Permission check utilities
const checkPermission = (user: User, permissionId: string, resource?: string): boolean => {
  const permission = user.permissions.find(p => p.id === permissionId);
  if (!permission) return false;

  // Check resource-specific restrictions
  if (resource && user.role.restrictions.allowedAgents) {
    return user.role.restrictions.allowedAgents.includes(resource);
  }

  return true;
};

const checkDomainAccess = (user: User, domain: string): boolean => {
  if (user.role.level === 'super_admin' || user.role.level === 'platform_admin') {
    return true;
  }

  return user.role.restrictions.allowedDomains?.includes(domain) || false;
};

// Role badge component
const RoleBadge: React.FC<{ role: Role }> = ({ role }) => {
  const getRoleColor = () => {
    switch (role.level) {
      case 'super_admin': return 'bg-purple-100 text-purple-800';
      case 'platform_admin': return 'bg-blue-100 text-blue-800';
      case 'domain_admin': return 'bg-green-100 text-green-800';
      case 'agent_operator': return 'bg-yellow-100 text-yellow-800';
      case 'viewer': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getRoleIcon = () => {
    switch (role.level) {
      case 'super_admin': return <Crown className="w-3 h-3 mr-1" />;
      case 'platform_admin': return <Shield className="w-3 h-3 mr-1" />;
      case 'domain_admin': return <Users className="w-3 h-3 mr-1" />;
      case 'agent_operator': return <Settings className="w-3 h-3 mr-1" />;
      case 'viewer': return <Eye className="w-3 h-3 mr-1" />;
      default: return <Users className="w-3 h-3 mr-1" />;
    }
  };

  return (
    <Badge variant="outline" className={getRoleColor()}>
      {getRoleIcon()}
      {role.name}
    </Badge>
  );
};

// Permission list component
const PermissionsList: React.FC<{ 
  permissions: Permission[]; 
  userPermissions: Permission[];
  onToggle?: (permission: Permission, granted: boolean) => void;
  readonly?: boolean;
}> = ({ permissions, userPermissions, onToggle, readonly = false }) => {
  const groupedPermissions = permissions.reduce((groups, permission) => {
    if (!groups[permission.category]) {
      groups[permission.category] = [];
    }
    groups[permission.category].push(permission);
    return groups;
  }, {} as Record<string, Permission[]>);

  const hasPermission = (permission: Permission) => {
    return userPermissions.some(p => p.id === permission.id);
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'agent_management': return <Settings className="w-4 h-4" />;
      case 'configuration': return <Key className="w-4 h-4" />;
      case 'monitoring': return <Activity className="w-4 h-4" />;
      case 'tasks': return <CheckCircle className="w-4 h-4" />;
      case 'analytics': return <BarChart3 className="w-4 h-4" />;
      case 'system': return <Shield className="w-4 h-4" />;
      default: return <FileText className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-6">
      {Object.entries(groupedPermissions).map(([category, categoryPermissions]) => (
        <div key={category} className="space-y-3">
          <div className="flex items-center space-x-2">
            {getCategoryIcon(category)}
            <h4 className="font-medium capitalize">{category.replace('_', ' ')}</h4>
          </div>
          <div className="space-y-2 ml-6">
            {categoryPermissions.map((permission) => (
              <div key={permission.id} className="flex items-center justify-between p-2 border rounded">
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-sm">{permission.name}</span>
                    <Badge variant="outline" className="text-xs">
                      {permission.level}
                    </Badge>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">{permission.description}</p>
                </div>
                {!readonly && onToggle && (
                  <Switch
                    checked={hasPermission(permission)}
                    onCheckedChange={(checked) => onToggle(permission, checked)}
                  />
                )}
                {readonly && (
                  <div className="flex items-center">
                    {hasPermission(permission) ? (
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    ) : (
                      <XCircle className="w-4 h-4 text-gray-400" />
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

// User management component
const UserManagement: React.FC<{ 
  users: User[]; 
  roles: Role[];
  onUserUpdate: (user: User) => void;
}> = ({ users, roles, onUserUpdate }) => {
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);

  const getUserStatusIcon = (user: User) => {
    if (!user.isActive) return <Ban className="w-4 h-4 text-red-500" />;
    if (user.lockedUntil && user.lockedUntil > new Date()) return <Lock className="w-4 h-4 text-orange-500" />;
    if (user.sessionCount > 0) return <Activity className="w-4 h-4 text-green-500" />;
    return <UserCheck className="w-4 h-4 text-gray-400" />;
  };

  const getTimeRestrictionStatus = (user: User) => {
    const restrictions = user.role.restrictions.timeRestrictions;
    if (!restrictions) return null;

    const now = new Date();
    const currentDay = now.getDay();
    const currentTime = now.toTimeString().slice(0, 5);

    const isAllowedDay = restrictions.allowedDays.includes(currentDay);
    const isAllowedTime = currentTime >= restrictions.startTime && currentTime <= restrictions.endTime;

    if (!isAllowedDay || !isAllowedTime) {
      return <Clock className="w-4 h-4 text-orange-500" title="Outside allowed hours" />;
    }

    return <Clock className="w-4 h-4 text-green-500" title="Within allowed hours" />;
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 gap-4">
        {users.map((user) => (
          <Card key={user.id}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    {getUserStatusIcon(user)}
                    <div>
                      <h4 className="font-medium">{user.name}</h4>
                      <p className="text-sm text-gray-500">{user.email}</p>
                    </div>
                  </div>
                  <RoleBadge role={user.role} />
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="text-right text-sm">
                    <p className="text-gray-500">Last Login</p>
                    <p className="font-medium">
                      {user.lastLogin ? user.lastLogin.toLocaleString() : 'Never'}
                    </p>
                  </div>
                  
                  <div className="flex items-center space-x-1">
                    <span className="text-sm">{user.sessionCount} sessions</span>
                    {getTimeRestrictionStatus(user)}
                  </div>
                  
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      setSelectedUser(user);
                      setIsEditDialogOpen(true);
                    }}
                  >
                    <Edit className="w-4 h-4 mr-1" />
                    Edit
                  </Button>
                </div>
              </div>

              {user.role.restrictions.allowedDomains && (
                <div className="mt-3 pt-3 border-t">
                  <p className="text-xs text-gray-500 mb-2">Allowed Domains:</p>
                  <div className="flex space-x-2">
                    {user.role.restrictions.allowedDomains.map((domain) => (
                      <Badge key={domain} variant="secondary" className="text-xs">
                        {domain}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {user.failedLoginAttempts > 0 && (
                <div className="mt-3 pt-3 border-t">
                  <div className="flex items-center space-x-2 text-orange-600">
                    <AlertTriangle className="w-4 h-4" />
                    <span className="text-sm">
                      {user.failedLoginAttempts} failed login attempts
                    </span>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Edit User Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="max-w-4xl">
          <DialogHeader>
            <DialogTitle>Edit User: {selectedUser?.name}</DialogTitle>
            <DialogDescription>
              Modify user role and permissions
            </DialogDescription>
          </DialogHeader>

          {selectedUser && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Role</Label>
                  <Select
                    value={selectedUser.role.id}
                    onValueChange={(value) => {
                      const newRole = roles.find(r => r.id === value);
                      if (newRole) {
                        setSelectedUser({
                          ...selectedUser,
                          role: newRole,
                          permissions: newRole.permissions
                        });
                      }
                    }}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {roles.map((role) => (
                        <SelectItem key={role.id} value={role.id}>
                          {role.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="space-y-2">
                  <Label>Status</Label>
                  <div className="flex items-center space-x-2">
                    <Switch
                      checked={selectedUser.isActive}
                      onCheckedChange={(checked) =>
                        setSelectedUser({ ...selectedUser, isActive: checked })
                      }
                    />
                    <span className="text-sm">
                      {selectedUser.isActive ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
              </div>

              <div>
                <Label>Permissions</Label>
                <div className="mt-2 max-h-96 overflow-y-auto">
                  <PermissionsList
                    permissions={mockPermissions}
                    userPermissions={selectedUser.permissions}
                    readonly
                  />
                </div>
              </div>
            </div>
          )}

          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>
              Cancel
            </Button>
            <Button
              onClick={() => {
                if (selectedUser) {
                  onUserUpdate(selectedUser);
                }
                setIsEditDialogOpen(false);
              }}
            >
              Save Changes
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

// Main access control component
export default function AgentAccessControl() {
  const [users, setUsers] = useState<User[]>(mockUsers);
  const [roles, setRoles] = useState<Role[]>(mockRoles);
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);
  const [currentUser] = useState<User>(mockUsers[0]); // Simulate current user

  const handleUserUpdate = (updatedUser: User) => {
    setUsers(prev => prev.map(user => 
      user.id === updatedUser.id ? updatedUser : user
    ));
  };

  // Access control provider value
  const accessControlValue: AccessControlContextType = {
    currentUser,
    hasPermission: (permission: string, resource?: string) => 
      checkPermission(currentUser, permission, resource),
    hasRole: (role: string) => currentUser.role.level === role,
    canAccessAgent: (agentId: string) => 
      checkPermission(currentUser, 'agent.view', agentId),
    canAccessDomain: (domain: string) => 
      checkDomainAccess(currentUser, domain)
  };

  return (
    <AccessControlContext.Provider value={accessControlValue}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center">
              <Shield className="w-6 h-6 mr-2" />
              Access Control & Security
            </h2>
            <p className="text-gray-600">Manage user roles, permissions, and access controls</p>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant="outline" className="bg-green-100 text-green-800">
              <UserCheck className="w-4 h-4 mr-1" />
              {users.filter(u => u.isActive).length} Active Users
            </Badge>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Add User
            </Button>
          </div>
        </div>

        {/* Security Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Users</p>
                  <p className="text-2xl font-bold">{users.length}</p>
                </div>
                <Users className="w-8 h-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Active Roles</p>
                  <p className="text-2xl font-bold">{roles.filter(r => r.isActive).length}</p>
                </div>
                <Crown className="w-8 h-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Active Sessions</p>
                  <p className="text-2xl font-bold">{users.reduce((sum, u) => sum + u.sessionCount, 0)}</p>
                </div>
                <Activity className="w-8 h-8 text-green-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Failed Logins</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {users.reduce((sum, u) => sum + u.failedLoginAttempts, 0)}
                  </p>
                </div>
                <AlertTriangle className="w-8 h-8 text-orange-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Interface */}
        <Tabs defaultValue="users" className="space-y-4">
          <TabsList>
            <TabsTrigger value="users">Users</TabsTrigger>
            <TabsTrigger value="roles">Roles</TabsTrigger>
            <TabsTrigger value="permissions">Permissions</TabsTrigger>
            <TabsTrigger value="audit">Audit Log</TabsTrigger>
          </TabsList>

          <TabsContent value="users" className="space-y-4">
            <UserManagement
              users={users}
              roles={roles}
              onUserUpdate={handleUserUpdate}
            />
          </TabsContent>

          <TabsContent value="roles" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div className="lg:col-span-1">
                <Card>
                  <CardHeader>
                    <CardTitle>System Roles</CardTitle>
                    <CardDescription>Predefined role hierarchy</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {roles.map((role) => (
                      <div
                        key={role.id}
                        className={`p-3 border rounded cursor-pointer hover:bg-gray-50 ${
                          selectedRole?.id === role.id ? 'border-blue-500 bg-blue-50' : ''
                        }`}
                        onClick={() => setSelectedRole(role)}
                      >
                        <div className="flex items-center justify-between">
                          <RoleBadge role={role} />
                          <span className="text-sm text-gray-500">
                            {role.permissions.length} permissions
                          </span>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">{role.description}</p>
                      </div>
                    ))}
                  </CardContent>
                </Card>
              </div>

              <div className="lg:col-span-2">
                {selectedRole ? (
                  <Card>
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div>
                          <CardTitle>{selectedRole.name}</CardTitle>
                          <CardDescription>{selectedRole.description}</CardDescription>
                        </div>
                        <RoleBadge role={selectedRole} />
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {/* Role Restrictions */}
                        {Object.keys(selectedRole.restrictions).length > 0 && (
                          <div>
                            <h4 className="font-medium mb-2">Restrictions</h4>
                            <div className="grid grid-cols-2 gap-4 text-sm">
                              {selectedRole.restrictions.allowedDomains && (
                                <div>
                                  <p className="text-gray-500">Allowed Domains</p>
                                  <div className="flex flex-wrap gap-1 mt-1">
                                    {selectedRole.restrictions.allowedDomains.map((domain) => (
                                      <Badge key={domain} variant="secondary" className="text-xs">
                                        {domain}
                                      </Badge>
                                    ))}
                                  </div>
                                </div>
                              )}
                              {selectedRole.restrictions.timeRestrictions && (
                                <div>
                                  <p className="text-gray-500">Time Restrictions</p>
                                  <p className="font-medium">
                                    {selectedRole.restrictions.timeRestrictions.startTime} - {' '}
                                    {selectedRole.restrictions.timeRestrictions.endTime}
                                  </p>
                                </div>
                              )}
                              {selectedRole.restrictions.maxSessions && (
                                <div>
                                  <p className="text-gray-500">Max Sessions</p>
                                  <p className="font-medium">{selectedRole.restrictions.maxSessions}</p>
                                </div>
                              )}
                            </div>
                          </div>
                        )}

                        {/* Permissions */}
                        <div>
                          <h4 className="font-medium mb-2">Permissions</h4>
                          <div className="max-h-96 overflow-y-auto">
                            <PermissionsList
                              permissions={mockPermissions}
                              userPermissions={selectedRole.permissions}
                              readonly
                            />
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ) : (
                  <Card>
                    <CardContent className="p-8 text-center">
                      <Crown className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-500">Select a role to view its permissions and restrictions</p>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="permissions">
            <Card>
              <CardHeader>
                <CardTitle>System Permissions</CardTitle>
                <CardDescription>All available permissions in the system</CardDescription>
              </CardHeader>
              <CardContent>
                <PermissionsList
                  permissions={mockPermissions}
                  userPermissions={mockPermissions} // Show all as reference
                  readonly
                />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="audit">
            <Card>
              <CardHeader>
                <CardTitle>Audit Log</CardTitle>
                <CardDescription>Security events and user activities</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8">
                  <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">Audit log functionality will be implemented here</p>
                  <p className="text-sm text-gray-400">Track user activities, permission changes, and security events</p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </AccessControlContext.Provider>
  );
}