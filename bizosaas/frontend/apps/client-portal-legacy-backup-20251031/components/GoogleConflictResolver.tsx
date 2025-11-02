'use client';

import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, CheckCircle, X, RefreshCw, Eye,
  ArrowRight, Clock, Building, Phone, Globe,
  Calendar, User, Filter, Search
} from 'lucide-react';

interface ConflictData {
  google_data: any;
  platform_data: any;
}

interface Conflict {
  id: string;
  type: 'data_mismatch' | 'hours_mismatch' | 'category_mismatch' | 'address_mismatch';
  severity: 'high' | 'medium' | 'low';
  location_id: string;
  location_name: string;
  google_data: any;
  platform_data: any;
  detected_at: string;
  status: 'pending' | 'resolved' | 'ignored';
  suggested_resolution: 'use_google_data' | 'use_platform_data' | 'manual_review';
}

interface ConflictSummary {
  pending: number;
  resolved: number;
  ignored: number;
  by_severity: {
    high: number;
    medium: number;
    low: number;
  };
}

interface ConflictResponse {
  conflicts: Conflict[];
  total: number;
  summary: ConflictSummary;
  source?: string;
}

export function GoogleConflictResolver() {
  const [conflicts, setConflicts] = useState<Conflict[]>([]);
  const [summary, setSummary] = useState<ConflictSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [resolving, setResolving] = useState<string | null>(null);
  const [filterSeverity, setFilterSeverity] = useState('all');
  const [filterStatus, setFilterStatus] = useState('pending');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchConflicts();
  }, []);

  const fetchConflicts = async () => {
    try {
      const response = await fetch('/api/brain/business-directory/google/conflicts');
      const data: ConflictResponse = await response.json();
      setConflicts(data.conflicts || []);
      setSummary(data.summary || null);
    } catch (error) {
      console.error('Error fetching conflicts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleResolveConflict = async (conflictId: string, resolution: string) => {
    setResolving(conflictId);
    try {
      await fetch('/api/brain/business-directory/google/conflicts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conflict_id: conflictId,
          resolution: resolution
        }),
      });

      // Update conflict status locally
      setConflicts(conflicts.map(conflict => 
        conflict.id === conflictId 
          ? { ...conflict, status: 'resolved' as const }
          : conflict
      ));
    } catch (error) {
      console.error('Error resolving conflict:', error);
    } finally {
      setResolving(null);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'low': return 'text-blue-600 bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'resolved': return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400';
      case 'pending': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'ignored': return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-300';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const getConflictIcon = (type: string) => {
    switch (type) {
      case 'data_mismatch': return Building;
      case 'hours_mismatch': return Clock;
      case 'address_mismatch': return Building;
      case 'category_mismatch': return User;
      default: return AlertTriangle;
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

  const renderConflictDetails = (conflict: Conflict) => {
    const { google_data, platform_data, type } = conflict;

    switch (type) {
      case 'data_mismatch':
        return (
          <div className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <h5 className="font-medium text-blue-900 dark:text-blue-100 mb-2">
                  Google Business Profile Data
                </h5>
                <div className="space-y-2 text-sm">
                  <div><strong>Name:</strong> {google_data.name}</div>
                  <div><strong>Phone:</strong> {google_data.phone}</div>
                  <div><strong>Address:</strong> {google_data.address}</div>
                </div>
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
                <h5 className="font-medium text-purple-900 dark:text-purple-100 mb-2">
                  Platform Data
                </h5>
                <div className="space-y-2 text-sm">
                  <div><strong>Name:</strong> {platform_data.name}</div>
                  <div><strong>Phone:</strong> {platform_data.phone}</div>
                  <div><strong>Address:</strong> {platform_data.address}</div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'hours_mismatch':
        return (
          <div className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <h5 className="font-medium text-blue-900 dark:text-blue-100 mb-2">
                  Google Business Hours
                </h5>
                <div className="space-y-1 text-sm">
                  {Object.entries(google_data.hours || {}).map(([day, hours]) => (
                    <div key={day}>
                      <strong>{day}:</strong> {hours as string}
                    </div>
                  ))}
                </div>
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
                <h5 className="font-medium text-purple-900 dark:text-purple-100 mb-2">
                  Platform Hours
                </h5>
                <div className="space-y-1 text-sm">
                  {Object.entries(platform_data.hours || {}).map(([day, hours]) => (
                    <div key={day}>
                      <strong>{day}:</strong> {hours as string}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return (
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Conflict details will be displayed here based on the conflict type.
          </div>
        );
    }
  };

  const filteredConflicts = conflicts.filter(conflict => {
    const matchesSeverity = filterSeverity === 'all' || conflict.severity === filterSeverity;
    const matchesStatus = filterStatus === 'all' || conflict.status === filterStatus;
    const matchesSearch = searchTerm === '' || 
      conflict.location_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      conflict.type.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesSeverity && matchesStatus && matchesSearch;
  });

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded mb-4"></div>
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded mb-6"></div>
          <div className="space-y-4">
            {[1, 2].map((i) => (
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
      {/* Conflict Summary */}
      {summary && (
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Google Conflict Resolution
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
              <div className="flex items-center">
                <Clock className="w-8 h-8 text-yellow-600 dark:text-yellow-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Pending
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {summary.pending}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
              <div className="flex items-center">
                <CheckCircle className="w-8 h-8 text-green-600 dark:text-green-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Resolved
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {summary.resolved}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
              <div className="flex items-center">
                <AlertTriangle className="w-8 h-8 text-red-600 dark:text-red-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    High Priority
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {summary.by_severity.high}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
              <div className="flex items-center">
                <X className="w-8 h-8 text-gray-600 dark:text-gray-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Ignored
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {summary.ignored}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filters and Search */}
      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search conflicts..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <select 
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            >
              <option value="all">All Status</option>
              <option value="pending">Pending</option>
              <option value="resolved">Resolved</option>
              <option value="ignored">Ignored</option>
            </select>
            
            <select 
              value={filterSeverity}
              onChange={(e) => setFilterSeverity(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            >
              <option value="all">All Severity</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
        </div>
      </div>

      {/* Conflicts List */}
      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Data Conflicts ({filteredConflicts.length})
        </h3>

        {filteredConflicts.length === 0 ? (
          <div className="text-center py-12">
            <CheckCircle className="w-16 h-16 mx-auto text-green-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No Conflicts Found
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              All your Google Business Profile data is synchronized correctly.
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {filteredConflicts.map((conflict) => {
              const ConflictIcon = getConflictIcon(conflict.type);
              
              return (
                <div
                  key={conflict.id}
                  className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
                        <ConflictIcon className="w-5 h-5 text-orange-600 dark:text-orange-400" />
                      </div>
                      <div>
                        <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                          {conflict.location_name}
                        </h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {conflict.type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 text-xs rounded-full ${getSeverityColor(conflict.severity)}`}>
                        {conflict.severity} priority
                      </span>
                      <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(conflict.status)}`}>
                        {conflict.status}
                      </span>
                    </div>
                  </div>

                  {/* Conflict Details */}
                  {renderConflictDetails(conflict)}

                  {/* Resolution Actions */}
                  {conflict.status === 'pending' && (
                    <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-600">
                      <div className="flex items-center justify-between">
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          <span className="font-medium">Detected:</span> {formatDate(conflict.detected_at)}
                        </div>
                        
                        <div className="flex items-center space-x-3">
                          <button
                            onClick={() => handleResolveConflict(conflict.id, 'use_google_data')}
                            disabled={resolving === conflict.id}
                            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            Use Google Data
                          </button>
                          
                          <button
                            onClick={() => handleResolveConflict(conflict.id, 'use_platform_data')}
                            disabled={resolving === conflict.id}
                            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            Use Platform Data
                          </button>
                          
                          <button
                            onClick={() => handleResolveConflict(conflict.id, 'manual_review')}
                            disabled={resolving === conflict.id}
                            className="border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-sm disabled:opacity-50"
                          >
                            Review Later
                          </button>
                          
                          {resolving === conflict.id && (
                            <RefreshCw className="w-4 h-4 animate-spin text-gray-400" />
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}