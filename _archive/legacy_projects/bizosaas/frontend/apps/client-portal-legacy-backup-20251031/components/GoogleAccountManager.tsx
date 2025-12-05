'use client';

import React, { useState, useEffect } from 'react';
import { 
  User, Link, Unlink, CheckCircle, AlertCircle, 
  Clock, RefreshCw, Shield, MapPin, Calendar,
  Settings, Eye, Trash2
} from 'lucide-react';

interface GoogleAccount {
  id: string;
  email: string;
  name: string;
  type: string;
  verified: boolean;
  connected_at: string;
  last_sync: string;
  locations_count: number;
  status: string;
  permissions: string[];
  profile_photo?: string;
}

interface GoogleAccountData {
  accounts: GoogleAccount[];
  total: number;
  source?: string;
}

export function GoogleAccountManager() {
  const [accounts, setAccounts] = useState<GoogleAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [connecting, setConnecting] = useState(false);
  const [disconnecting, setDisconnecting] = useState<string | null>(null);

  useEffect(() => {
    fetchGoogleAccounts();
  }, []);

  const fetchGoogleAccounts = async () => {
    try {
      const response = await fetch('/api/brain/business-directory/google/accounts');
      const data: GoogleAccountData = await response.json();
      setAccounts(data.accounts || []);
    } catch (error) {
      console.error('Error fetching Google accounts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleConnectGoogle = async () => {
    setConnecting(true);
    try {
      const response = await fetch('/api/brain/business-directory/google/auth/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          redirect_uri: window.location.origin + '/api/brain/business-directory/google/auth/callback'
        }),
      });

      const data = await response.json();
      if (data.auth_url) {
        // Open OAuth URL in a popup or redirect
        window.location.href = data.auth_url;
      }
    } catch (error) {
      console.error('Error starting Google OAuth:', error);
    } finally {
      setConnecting(false);
    }
  };

  const handleDisconnectAccount = async (accountId: string) => {
    setDisconnecting(accountId);
    try {
      await fetch(`/api/brain/business-directory/google/accounts?account_id=${accountId}`, {
        method: 'DELETE',
      });
      
      // Remove account from state
      setAccounts(accounts.filter(account => account.id !== accountId));
    } catch (error) {
      console.error('Error disconnecting Google account:', error);
    } finally {
      setDisconnecting(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400';
      case 'expired': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
      case 'limited': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-400';
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
      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Google Business Profile Accounts
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Connect and manage your Google Business Profile accounts to sync location data across platforms.
            </p>
          </div>
          <button
            onClick={handleConnectGoogle}
            disabled={connecting}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {connecting ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Link className="w-4 h-4 mr-2" />
            )}
            {connecting ? 'Connecting...' : 'Connect Google Account'}
          </button>
        </div>

        {accounts.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
              <User className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No Google Accounts Connected
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Connect your Google Business Profile account to start syncing your business locations.
            </p>
            <button
              onClick={handleConnectGoogle}
              disabled={connecting}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 flex items-center mx-auto disabled:opacity-50"
            >
              <Link className="w-5 h-5 mr-2" />
              Connect Your First Account
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {accounts.map((account) => (
              <div
                key={account.id}
                className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                      {account.profile_photo ? (
                        <img 
                          src={account.profile_photo} 
                          alt={account.name}
                          className="w-12 h-12 rounded-full object-cover"
                        />
                      ) : (
                        <User className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                      )}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                          {account.name}
                        </h3>
                        {account.verified && (
                          <CheckCircle className="w-5 h-5 text-green-600" />
                        )}
                        <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(account.status)}`}>
                          {account.status}
                        </span>
                      </div>
                      <p className="text-gray-600 dark:text-gray-400 mb-2">{account.email}</p>
                      <div className="flex items-center space-x-6 text-sm text-gray-500 dark:text-gray-400">
                        <div className="flex items-center">
                          <MapPin className="w-4 h-4 mr-1" />
                          {account.locations_count} locations
                        </div>
                        <div className="flex items-center">
                          <Calendar className="w-4 h-4 mr-1" />
                          Connected {formatDate(account.connected_at)}
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-1" />
                          Last sync {formatDate(account.last_sync)}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <button
                      className="p-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                      title="View Account Details"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      className="p-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                      title="Account Settings"
                    >
                      <Settings className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDisconnectAccount(account.id)}
                      disabled={disconnecting === account.id}
                      className="p-2 text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 disabled:opacity-50"
                      title="Disconnect Account"
                    >
                      {disconnecting === account.id ? (
                        <RefreshCw className="w-4 h-4 animate-spin" />
                      ) : (
                        <Unlink className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Permissions */}
                <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
                        Permissions
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {account.permissions.map((permission) => (
                          <span
                            key={permission}
                            className="px-2 py-1 bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 text-xs rounded-full"
                          >
                            {permission}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                      <Shield className="w-4 h-4 mr-1" />
                      {account.verified ? 'Verified' : 'Unverified'}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Account Statistics */}
      {accounts.length > 0 && (
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Account Overview
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
              <div className="flex items-center">
                <User className="w-8 h-8 text-blue-600 dark:text-blue-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Total Accounts
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {accounts.length}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
              <div className="flex items-center">
                <CheckCircle className="w-8 h-8 text-green-600 dark:text-green-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Active Accounts
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {accounts.filter(acc => acc.status === 'active').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
              <div className="flex items-center">
                <MapPin className="w-8 h-8 text-purple-600 dark:text-purple-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Total Locations
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {accounts.reduce((sum, acc) => sum + acc.locations_count, 0)}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg">
              <div className="flex items-center">
                <Shield className="w-8 h-8 text-orange-600 dark:text-orange-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Verified Accounts
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {accounts.filter(acc => acc.verified).length}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}