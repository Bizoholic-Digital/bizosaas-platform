'use client';

import React, { useState, useEffect } from 'react';
import { 
  RefreshCw, MapPin, CheckCircle, AlertCircle, Clock,
  Play, Pause, Eye, Download, Upload, Filter,
  Calendar, User, Building, Phone, Globe
} from 'lucide-react';

interface SyncOperation {
  id: string;
  status: 'in_progress' | 'completed' | 'failed' | 'paused';
  account_id: string;
  locations_synced: number;
  started_at: string;
  completed_at?: string;
  progress: {
    total: number;
    completed: number;
    failed: number;
    skipped: number;
  };
  results?: {
    created: number;
    updated: number;
    conflicts: number;
  };
}

interface SyncData {
  syncs: SyncOperation[];
  total: number;
  source?: string;
}

interface GoogleLocation {
  id: string;
  name: string;
  address: string;
  phone?: string;
  website?: string;
  rating: number;
  reviews_count: number;
  verified: boolean;
  last_updated: string;
  sync_status: 'synced' | 'pending' | 'conflict' | 'failed';
}

export function GoogleLocationSync() {
  const [syncs, setSyncs] = useState<SyncOperation[]>([]);
  const [locations, setLocations] = useState<GoogleLocation[]>([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    fetchSyncOperations();
    fetchGoogleLocations();
  }, []);

  const fetchSyncOperations = async () => {
    try {
      const response = await fetch('/api/brain/business-directory/google/sync/locations');
      const data: SyncData = await response.json();
      setSyncs(data.syncs || []);
    } catch (error) {
      console.error('Error fetching sync operations:', error);
    }
  };

  const fetchGoogleLocations = async () => {
    try {
      // This would fetch Google locations from the API
      const mockLocations: GoogleLocation[] = [
        {
          id: 'loc_001',
          name: 'Downtown Store',
          address: '123 Main St, New York, NY 10001',
          phone: '+1-555-0123',
          website: 'https://downtown.example.com',
          rating: 4.8,
          reviews_count: 234,
          verified: true,
          last_updated: '2024-09-18T09:15:00Z',
          sync_status: 'synced'
        },
        {
          id: 'loc_002',
          name: 'Mall Location',
          address: '456 Shopping Center, Brooklyn, NY 11201',
          phone: '+1-555-0456',
          rating: 4.5,
          reviews_count: 156,
          verified: true,
          last_updated: '2024-09-18T08:30:00Z',
          sync_status: 'conflict'
        },
        {
          id: 'loc_003',
          name: 'Warehouse Store',
          address: '789 Industrial Blvd, Queens, NY 11373',
          rating: 4.2,
          reviews_count: 78,
          verified: false,
          last_updated: '2024-09-17T15:45:00Z',
          sync_status: 'pending'
        }
      ];
      setLocations(mockLocations);
    } catch (error) {
      console.error('Error fetching Google locations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStartSync = async (accountId?: string) => {
    setSyncing(true);
    try {
      const body = accountId ? { account_id: accountId } : { sync_all: true };
      const response = await fetch('/api/brain/business-directory/google/sync/locations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      const newSync = await response.json();
      setSyncs([newSync, ...syncs]);
      
      // Refresh operations after a short delay
      setTimeout(fetchSyncOperations, 2000);
    } catch (error) {
      console.error('Error starting sync:', error);
    } finally {
      setSyncing(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400';
      case 'in_progress': return 'text-blue-600 bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400';
      case 'failed': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
      case 'paused': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-400';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const getSyncStatusColor = (status: string) => {
    switch (status) {
      case 'synced': return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400';
      case 'pending': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'conflict': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
      case 'failed': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getProgressPercentage = (progress: SyncOperation['progress']) => {
    return progress.total > 0 ? Math.round((progress.completed / progress.total) * 100) : 0;
  };

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded mb-4"></div>
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded mb-6"></div>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                <div className="h-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Sync Control Panel */}
      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Google Location Sync
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Synchronize your Google Business Profile locations with your local directory listings.
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <select 
              value={selectedAccount}
              onChange={(e) => setSelectedAccount(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            >
              <option value="all">All Accounts</option>
              <option value="google_account_001">Acme Corporation</option>
              <option value="google_account_002">Acme Marketing</option>
            </select>
            <button
              onClick={() => handleStartSync(selectedAccount === 'all' ? undefined : selectedAccount)}
              disabled={syncing}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {syncing ? (
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <Play className="w-4 h-4 mr-2" />
              )}
              {syncing ? 'Starting Sync...' : 'Start Sync'}
            </button>
          </div>
        </div>

        {/* Sync Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
            <div className="flex items-center">
              <MapPin className="w-8 h-8 text-blue-600 dark:text-blue-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Total Locations
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {locations.length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
            <div className="flex items-center">
              <CheckCircle className="w-8 h-8 text-green-600 dark:text-green-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Synced
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {locations.filter(loc => loc.sync_status === 'synced').length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
            <div className="flex items-center">
              <Clock className="w-8 h-8 text-yellow-600 dark:text-yellow-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Pending
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {locations.filter(loc => loc.sync_status === 'pending').length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
            <div className="flex items-center">
              <AlertCircle className="w-8 h-8 text-red-600 dark:text-red-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Conflicts
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {locations.filter(loc => loc.sync_status === 'conflict').length}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Sync Operations */}
      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Recent Sync Operations
        </h3>
        {syncs.length === 0 ? (
          <div className="text-center py-8">
            <RefreshCw className="w-12 h-12 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 dark:text-gray-400">
              No sync operations yet. Start your first sync to see progress here.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {syncs.map((sync) => (
              <div
                key={sync.id}
                className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(sync.status)}`}>
                      {sync.status.replace('_', ' ')}
                    </span>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      Account: {sync.account_id}
                    </span>
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Started {formatDate(sync.started_at)}
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="mb-3">
                  <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-1">
                    <span>Progress</span>
                    <span>{getProgressPercentage(sync.progress)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${getProgressPercentage(sync.progress)}%` }}
                    ></div>
                  </div>
                </div>

                {/* Progress Details */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Total:</span>
                    <span className="ml-2 font-medium text-gray-900 dark:text-white">
                      {sync.progress.total}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Completed:</span>
                    <span className="ml-2 font-medium text-green-600">
                      {sync.progress.completed}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Failed:</span>
                    <span className="ml-2 font-medium text-red-600">
                      {sync.progress.failed}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Skipped:</span>
                    <span className="ml-2 font-medium text-yellow-600">
                      {sync.progress.skipped}
                    </span>
                  </div>
                </div>

                {/* Results (if completed) */}
                {sync.results && (
                  <div className="mt-4 pt-3 border-t border-gray-200 dark:border-gray-600">
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600 dark:text-gray-400">Created:</span>
                        <span className="ml-2 font-medium text-blue-600">
                          {sync.results.created}
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-600 dark:text-gray-400">Updated:</span>
                        <span className="ml-2 font-medium text-green-600">
                          {sync.results.updated}
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-600 dark:text-gray-400">Conflicts:</span>
                        <span className="ml-2 font-medium text-red-600">
                          {sync.results.conflicts}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Google Locations */}
      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Google Business Locations
          </h3>
          <div className="flex items-center space-x-3">
            <select 
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
            >
              <option value="all">All Status</option>
              <option value="synced">Synced</option>
              <option value="pending">Pending</option>
              <option value="conflict">Conflicts</option>
              <option value="failed">Failed</option>
            </select>
            <button className="p-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
              <Filter className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="space-y-4">
          {locations
            .filter(location => filterStatus === 'all' || location.sync_status === filterStatus)
            .map((location) => (
              <div
                key={location.id}
                className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                        {location.name}
                      </h4>
                      {location.verified && (
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      )}
                      <span className={`px-2 py-1 text-xs rounded-full ${getSyncStatusColor(location.sync_status)}`}>
                        {location.sync_status}
                      </span>
                    </div>
                    
                    <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                      <div className="flex items-center">
                        <Building className="w-4 h-4 mr-2" />
                        {location.address}
                      </div>
                      {location.phone && (
                        <div className="flex items-center">
                          <Phone className="w-4 h-4 mr-2" />
                          {location.phone}
                        </div>
                      )}
                      {location.website && (
                        <div className="flex items-center">
                          <Globe className="w-4 h-4 mr-2" />
                          <a 
                            href={location.website} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-700 dark:text-blue-400"
                          >
                            {location.website}
                          </a>
                        </div>
                      )}
                    </div>
                    
                    <div className="flex items-center space-x-4 mt-3 text-sm">
                      <div className="flex items-center">
                        <span className="text-yellow-400 mr-1">★</span>
                        <span>{location.rating} ({location.reviews_count} reviews)</span>
                      </div>
                      <div className="flex items-center text-gray-500 dark:text-gray-400">
                        <Calendar className="w-4 h-4 mr-1" />
                        Updated {formatDate(location.last_updated)}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <button
                      className="p-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                      title="View Location Details"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      className="p-2 text-blue-600 hover:text-blue-700 dark:text-blue-400 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20"
                      title="Sync Location"
                    >
                      <RefreshCw className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}