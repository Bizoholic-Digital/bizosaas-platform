'use client'

import { useState, useEffect } from 'react'
import { Users, UserCheck, UserX, Mail, Calendar, Search, Plus, Eye, Edit, Trash2, Shield, Loader2, Key, History, Activity, Monitor, LogOut } from 'lucide-react'
import { useUsers } from '@/lib/hooks/use-api'
import { adminApi, AuditLog } from '@/lib/api/admin'
import { toast } from 'sonner'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  role: string
  is_active: boolean
  is_verified: boolean
  tenant_id: string
  created_at: string
  last_login_at: string | null
  login_count: number
}

export default function UsersPage() {
  const { data: usersData, isLoading, error } = useUsers()
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedRole, setSelectedRole] = useState<string>('all')
  const [selectedStatus, setSelectedStatus] = useState<string>('all')
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  const [isDetailOpen, setIsDetailOpen] = useState(false)
  const [userSessions, setUserSessions] = useState<any[]>([])
  const [userLogs, setUserLogs] = useState<AuditLog[]>([])
  const [loadingExtra, setLoadingExtra] = useState(false)
  const [isEditOpen, setIsEditOpen] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [editFormData, setEditFormData] = useState({
    id: '',
    first_name: '',
    last_name: '',
    email: '',
    role: 'user',
    is_active: true
  })

  const users: User[] = usersData || []

  const filteredUsers = users.filter(user => {
    const fullName = `${user.first_name || ''} ${user.last_name || ''}`.toLowerCase()
    const matchesSearch =
      user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      fullName.includes(searchTerm.toLowerCase())

    const matchesRole = selectedRole === 'all' || user.role === selectedRole
    const matchesStatus = selectedStatus === 'all' ||
      (selectedStatus === 'active' && user.is_active) ||
      (selectedStatus === 'inactive' && !user.is_active)

    return matchesSearch && matchesRole && matchesStatus
  })

  const handleImpersonate = async (userId: string) => {
    try {
      const res = await adminApi.impersonateUser(userId)
      if (res.data?.token) {
        toast.success('Impersonation token generated')
        // In a real app, redirection logic would go here
        // window.open(`${process.env.NEXT_PUBLIC_CLIENT_PORTAL_URL}/auth/impersonate?token=${res.data.token}`, '_blank')
        console.log('Impersonation Token:', res.data.token)
      }
    } catch (e) {
      toast.error('Impersonation failed')
    }
  }

  const handleViewUser = async (user: User) => {
    setSelectedUser(user)
    setIsDetailOpen(true)
    setLoadingExtra(true)
    try {
      const [sessions, logs] = await Promise.all([
        adminApi.getUserSessions(user.id),
        adminApi.getAuditLogs(user.id, 20)
      ])
      setUserSessions(sessions.data || [])
      setUserLogs(logs.data || [])
    } catch (e) {
      console.error('Failed to load user details', e)
    } finally {
      setLoadingExtra(false)
    }
  }

  const handleRevokeSession = async (sessionId: string) => {
    try {
      await adminApi.revokeSession(sessionId)
      toast.success('Session terminated')
      if (selectedUser) {
        const sessions = await adminApi.getUserSessions(selectedUser.id)
        setUserSessions(sessions.data || [])
      }
    } catch (e) {
      toast.error('Failed to revoke session')
    }
  }

  const handleEditUser = (user: User) => {
    setEditFormData({
      id: user.id,
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      role: user.role,
      is_active: user.is_active
    })
    setIsEditOpen(true)
  }

  const handleDeleteUser = async (user: User) => {
    if (!confirm(`Are you sure you want to delete user ${user.email}? This action cannot be undone.`)) return
    try {
      await adminApi.deleteUser(user.id)
      toast.success('User deleted successfully')
    } catch (e) {
      toast.error('Failed to delete user')
    }
  }

  const handleSaveUser = async () => {
    setIsSaving(true)
    try {
      if (editFormData.id) {
        await adminApi.updateUser(editFormData.id, editFormData)
        toast.success('User updated successfully')
      } else {
        await adminApi.createUser(editFormData)
        toast.success('User created successfully')
      }
      setIsEditOpen(false)
    } catch (e) {
      toast.error('Failed to save user')
    } finally {
      setIsSaving(false)
    }
  }

  const getStatusColor = (isActive: boolean) => {
    return isActive ? 'text-green-600 bg-green-100' : 'text-gray-600 bg-gray-100'
  }

  const getRoleColor = (role: string) => {
    switch (role?.toLowerCase()) {
      case 'super_admin': return 'text-purple-600 bg-purple-100'
      case 'tenant_admin': return 'text-blue-600 bg-blue-100'
      case 'user': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getRoleIcon = (role: string) => {
    switch (role?.toLowerCase()) {
      case 'super_admin': return <Shield className="h-4 w-4" />
      case 'tenant_admin': return <UserCheck className="h-4 w-4" />
      default: return <Users className="h-4 w-4" />
    }
  }

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Never'
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    } catch {
      return 'Invalid Date'
    }
  }

  const formatDateTime = (dateString: string | null) => {
    if (!dateString) return 'Never'
    try {
      return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return 'Invalid Date'
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="animate-spin h-12 w-12 text-blue-600 mx-auto" />
          <p className="mt-4 text-gray-600">Loading platform users...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">User Management</h1>
          <p className="text-gray-600">Manage platform users across all tenant organizations</p>
        </div>
        <button
          onClick={() => {
            setEditFormData({ id: '', first_name: '', last_name: '', email: '', role: 'user', is_active: true })
            setIsEditOpen(true)
          }}
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-bold shadow-lg shadow-blue-100"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add User
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          <p>Error loading users. Please ensure the Brain Gateway is online.</p>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search by email or name..."
              className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="flex flex-col sm:flex-row items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-4 gap-2 sm:gap-0">
            <select
              className="px-3 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value)}
            >
              <option value="all">All Roles</option>
              <option value="super_admin">Super Admin</option>
              <option value="tenant_admin">Tenant Admin</option>
              <option value="user">User</option>
            </select>

            <select
              className="px-3 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>
      </div>

      {/* Users Table */}
      <div className="bg-white shadow-sm border border-gray-100 rounded-2xl overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between bg-gray-50/50">
          <div>
            <h3 className="text-lg font-black text-gray-900">Platform Directory</h3>
            <p className="text-sm text-gray-500">{filteredUsers.length} active users distributed across nodes</p>
          </div>
          <Badge variant="outline" className="font-bold">{filteredUsers.length} total</Badge>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50/50">
              <tr>
                <th className="px-6 py-3 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">User Details</th>
                <th className="px-6 py-3 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">Access Layer</th>
                <th className="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">Status</th>
                <th className="px-6 py-3 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">Metrics</th>
                <th className="px-6 py-3 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">Last Activity</th>
                <th className="px-6 py-3 text-right text-[10px] font-black text-gray-400 uppercase tracking-widest">Administrative Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-100">
              {filteredUsers.map((user) => (
                <tr key={user.id} className="group hover:bg-blue-50/30 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100/50 flex items-center justify-center shadow-sm">
                          <span className="text-sm font-black text-blue-600">
                            {(user.first_name?.[0] || user.email[0]).toUpperCase()}
                          </span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="flex items-center gap-2">
                          <div className="text-sm font-black text-gray-900">
                            {user.first_name} {user.last_name}
                          </div>
                          {user.is_verified && (
                            <div className="p-0.5 bg-green-50 rounded-full">
                              <UserCheck className="h-3 w-3 text-green-500" />
                            </div>
                          )}
                        </div>
                        <div className="text-xs text-gray-400 font-medium">{user.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-tight ${getRoleColor(user.role)}`}>
                      {getRoleIcon(user.role)}
                      <span className="ml-1.5">{user.role?.replace('_', ' ')}</span>
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold ${getStatusColor(user.is_active)}`}>
                      <span className={`h-1.5 w-1.5 rounded-full mr-1.5 ${user.is_active ? 'bg-green-500' : 'bg-gray-400'}`} />
                      {user.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <div className="flex items-center gap-2">
                      <Activity className="h-3 w-3 text-gray-300" />
                      <span className="font-bold text-gray-700">{user.login_count}</span>
                      <span className="text-[10px] font-black text-gray-300 uppercase">logins</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-xs text-gray-900 font-bold">{formatDateTime(user.last_login_at)}</div>
                    <div className="text-[10px] text-gray-400 font-medium tracking-tight">Joined {formatDate(user.created_at)}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center justify-end gap-1">
                      <button
                        onClick={() => handleViewUser(user)}
                        className="p-2 text-blue-400 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                        title="View Intelligence"
                      >
                        <Eye className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleImpersonate(user.id)}
                        className="p-2 text-indigo-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-xl transition-all"
                        title="Impersonate Identity"
                      >
                        <Shield className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleEditUser(user)}
                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                        title="Configure Profile"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteUser(user)}
                        className="p-2 text-gray-300 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all"
                        title="Delete User"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredUsers.length === 0 && !isLoading && (
            <div className="px-6 py-12 text-center bg-gray-50/30">
              <div className="inline-flex p-4 bg-white rounded-3xl shadow-sm mb-4">
                <UserX className="h-8 w-8 text-gray-300" />
              </div>
              <p className="text-gray-400 font-bold">No users detected in the current namespace</p>
            </div>
          )}
        </div>
      </div>

      {/* User Detail Dialog */}
      <Dialog open={isDetailOpen} onOpenChange={setIsDetailOpen}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto border-none shadow-2xl bg-white dark:bg-gray-950 p-0 rounded-3xl">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 text-white relative">
            <div className="absolute top-0 right-0 p-8 opacity-10">
              <Users className="h-32 w-32 rotate-12" />
            </div>
            <DialogHeader className="relative z-10 flex flex-row items-center gap-6 text-left">
              <div className="h-20 w-20 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center border border-white/30 shadow-xl overflow-hidden">
                <span className="text-3xl font-black">
                  {(selectedUser?.first_name?.[0] || selectedUser?.email?.[0] || 'U').toUpperCase()}
                </span>
              </div>
              <div className="space-y-1">
                <DialogTitle className="text-3xl font-black tracking-tight flex items-center gap-3">
                  {selectedUser?.first_name} {selectedUser?.last_name}
                  {selectedUser?.role && (
                    <Badge className="bg-white/20 text-white border-white/30 uppercase text-[10px] font-black px-3">
                      {selectedUser.role}
                    </Badge>
                  )}
                </DialogTitle>
                <DialogDescription className="text-blue-100 text-lg flex items-center gap-2">
                  <Mail className="h-4 w-4" /> {selectedUser?.email}
                </DialogDescription>
              </div>
            </DialogHeader>
          </div>

          <div className="p-8">
            <Tabs defaultValue="overview" className="w-full">
              <TabsList className="grid w-full grid-cols-3 bg-gray-50 dark:bg-black/40 p-1 rounded-2xl mb-8 border border-gray-100 dark:border-gray-800">
                <TabsTrigger value="overview" className="rounded-xl font-bold data-[state=active]:bg-white data-[state=active]:shadow-sm">
                  <Activity className="h-4 w-4 mr-2" /> Overview
                </TabsTrigger>
                <TabsTrigger value="security" className="rounded-xl font-bold data-[state=active]:bg-white data-[state=active]:shadow-sm">
                  <Key className="h-4 w-4 mr-2" /> Security
                </TabsTrigger>
                <TabsTrigger value="activity" className="rounded-xl font-bold data-[state=active]:bg-white data-[state=active]:shadow-sm">
                  <History className="h-4 w-4 mr-2" /> Activity
                </TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800">
                    <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Status</p>
                    <Badge className={selectedUser?.is_active ? 'bg-green-100 text-green-700 border-none' : 'bg-red-100 text-red-700 border-none'}>
                      {selectedUser?.is_active ? 'Active' : 'Deactivated'}
                    </Badge>
                  </div>
                  <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800">
                    <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Tenant ID</p>
                    <p className="font-mono text-xs text-gray-600 truncate">{selectedUser?.tenant_id || 'Global'}</p>
                  </div>
                  <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800">
                    <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Logins</p>
                    <p className="text-xl font-black text-gray-900 dark:text-gray-100">{selectedUser?.login_count || 0}</p>
                  </div>
                  <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800">
                    <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Member Since</p>
                    <p className="font-bold text-gray-700">{formatDate(selectedUser?.created_at || null)}</p>
                  </div>
                </div>

                <div className="flex gap-4">
                  <Button
                    className="flex-1 h-12 bg-indigo-600 hover:bg-indigo-700 text-white font-black rounded-xl shadow-lg shadow-indigo-200 dark:shadow-none transition-all"
                    onClick={() => selectedUser && handleImpersonate(selectedUser.id)}
                  >
                    <Shield className="h-4 w-4 mr-2" /> Launch Impersonation
                  </Button>
                  <Button
                    variant="outline"
                    className="flex-1 h-12 rounded-xl font-bold border-gray-100"
                  >
                    <Edit className="h-4 w-4 mr-2" /> Modify Permissions
                  </Button>
                </div>
              </TabsContent>

              <TabsContent value="security" className="space-y-4">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="text-sm font-black uppercase tracking-widest text-gray-400">Active Identity Sessions</h4>
                  <Badge variant="outline" className="font-bold">{userSessions.length} active</Badge>
                </div>
                {loadingExtra ? (
                  <div className="flex justify-center p-12"><Loader2 className="animate-spin h-8 w-8 text-blue-600" /></div>
                ) : userSessions.length === 0 ? (
                  <div className="p-12 text-center bg-gray-50 dark:bg-gray-900 rounded-3xl border border-dashed text-gray-400 font-medium">No active sessions detected</div>
                ) : (
                  <div className="space-y-3">
                    {userSessions.map((session: any) => (
                      <div key={session.id} className="flex items-center justify-between p-4 bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 rounded-2xl hover:shadow-md transition-shadow">
                        <div className="flex items-center gap-4">
                          <div className="p-3 bg-blue-50 dark:bg-blue-900/40 rounded-xl text-blue-600">
                            <Monitor className="h-5 w-5" />
                          </div>
                          <div>
                            <p className="text-sm font-black text-gray-900 dark:text-gray-100">{session.user_agent || 'Unknown Browser'}</p>
                            <div className="flex gap-3 text-[10px] text-gray-400 font-bold uppercase tracking-wider mt-0.5">
                              <span>IP: {session.ip_address || '0.0.0.0'}</span>
                              <span>•</span>
                              <span>Last: {formatDateTime(session.last_used)}</span>
                            </div>
                          </div>
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="text-red-600 hover:bg-red-50 hover:text-red-700 rounded-xl font-bold"
                          onClick={() => handleRevokeSession(session.id)}
                        >
                          <LogOut className="h-4 w-4 mr-2" /> Revoke
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </TabsContent>

              <TabsContent value="activity">
                <div className="space-y-4">
                  <h4 className="text-sm font-black uppercase tracking-widest text-gray-400">System Activity Audit Log</h4>
                  {loadingExtra ? (
                    <div className="flex justify-center p-12"><Loader2 className="animate-spin h-8 w-8 text-blue-600" /></div>
                  ) : userLogs.length === 0 ? (
                    <div className="p-12 text-center bg-gray-50 dark:bg-gray-900 rounded-3xl border border-dashed text-gray-400 font-medium">No recent activity logs</div>
                  ) : (
                    <div className="relative border-l-2 border-gray-100 dark:border-gray-800 ml-3 space-y-6 py-2">
                      {userLogs.map((log: AuditLog) => (
                        <div key={log.id} className="relative pl-8">
                          <div className="absolute left-[-9px] top-1.5 h-4 w-4 rounded-full bg-white dark:bg-gray-950 border-2 border-indigo-500 shadow-sm" />
                          <div className="flex items-center justify-between mb-1">
                            <p className="font-black text-sm text-gray-900 dark:text-gray-100">{log.action.replace(/_/g, ' ')}</p>
                            <span className="text-[10px] font-bold text-gray-400">{formatDateTime(log.created_at)}</span>
                          </div>
                          <pre className="text-[10px] bg-gray-50 dark:bg-gray-900 p-2 rounded-lg text-gray-500 font-mono overflow-x-auto whitespace-pre-wrap">
                            {JSON.stringify(log.details, null, 2)}
                          </pre>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </DialogContent>
      </Dialog>

      {/* Edit/Create User Dialog */}
      <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
        <DialogContent className="max-w-md border-none shadow-2xl bg-white dark:bg-gray-950 p-0 rounded-3xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-6 text-white">
            <DialogHeader>
              <DialogTitle className="text-xl font-black uppercase tracking-tight">
                {editFormData.id ? 'Modify Identity' : 'Provision New Identity'}
              </DialogTitle>
              <DialogDescription className="text-blue-100 border-none">
                {editFormData.id ? 'Update system-wide user credentials and permissions.' : 'Create a new platform identity with global access settings.'}
              </DialogDescription>
            </DialogHeader>
          </div>
          <div className="p-6 space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">First Name</label>
                <input
                  type="text"
                  className="w-full px-4 py-2 bg-gray-50 border border-gray-100 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all font-bold text-sm"
                  value={editFormData.first_name}
                  onChange={(e) => setEditFormData({ ...editFormData, first_name: e.target.value })}
                />
              </div>
              <div className="space-y-1">
                <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Last Name</label>
                <input
                  type="text"
                  className="w-full px-4 py-2 bg-gray-50 border border-gray-100 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all font-bold text-sm"
                  value={editFormData.last_name}
                  onChange={(e) => setEditFormData({ ...editFormData, last_name: e.target.value })}
                />
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Email Address</label>
              <input
                type="email"
                className="w-full px-4 py-2 bg-gray-50 border border-gray-100 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all font-bold text-sm"
                value={editFormData.email}
                onChange={(e) => setEditFormData({ ...editFormData, email: e.target.value })}
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Access Layer (Role)</label>
              <select
                className="w-full px-4 py-2 bg-gray-50 border border-gray-100 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all font-bold text-sm"
                value={editFormData.role}
                onChange={(e) => setEditFormData({ ...editFormData, role: e.target.value })}
              >
                <option value="user">User</option>
                <option value="tenant_admin">Tenant Admin</option>
                <option value="super_admin">Super Admin</option>
              </select>
            </div>
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-2xl border border-gray-100">
              <div>
                <p className="text-xs font-black uppercase tracking-tight text-gray-900">Active Status</p>
                <p className="text-[10px] text-gray-500">Allow user to authenticate</p>
              </div>
              <input
                type="checkbox"
                className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                checked={editFormData.is_active}
                onChange={(e) => setEditFormData({ ...editFormData, is_active: e.target.checked })}
              />
            </div>
            <div className="pt-4 flex gap-3">
              <Button
                variant="outline"
                className="flex-1 h-12 rounded-xl font-bold"
                onClick={() => setIsEditOpen(false)}
              >
                Cancel
              </Button>
              <Button
                className="flex-1 h-12 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-xl shadow-lg shadow-blue-200"
                onClick={handleSaveUser}
                disabled={isSaving}
              >
                {isSaving ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Synchronize Identity'}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}