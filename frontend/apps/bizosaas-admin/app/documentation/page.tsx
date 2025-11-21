'use client';

import React, { useState } from 'react';
import {
  FileText,
  BookOpen,
  Code,
  Users,
  Zap,
  Download,
  RefreshCw,
  CheckCircle,
  Clock,
  AlertCircle,
  Play,
  Eye,
  Settings
} from 'lucide-react';

interface Documentation {
  id: string;
  title: string;
  type: 'technical' | 'user-guide' | 'api' | 'developer';
  status: 'generated' | 'pending' | 'outdated' | 'error';
  lastGenerated: string;
  generatedBy: string;
  language: 'simple' | 'technical';
  wordCount: number;
  sections: number;
  autoUpdate: boolean;
}

interface DocAgent {
  id: string;
  name: string;
  description: string;
  icon: any;
  status: 'active' | 'idle' | 'generating';
  docsGenerated: number;
  lastRun: string;
  nextRun: string;
}

export default function DocumentationPage() {
  const [selectedDoc, setSelectedDoc] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const [agents, setAgents] = useState<DocAgent[]>([
    {
      id: 'technical-doc-agent',
      name: 'Technical Documentation Agent',
      description: 'Generates comprehensive technical docs for developers',
      icon: Code,
      status: 'idle',
      docsGenerated: 145,
      lastRun: '2025-10-06 04:00:00',
      nextRun: '2025-10-06 12:00:00'
    },
    {
      id: 'user-guide-agent',
      name: 'User Guide Agent',
      description: 'Creates simple, user-friendly guides and tutorials',
      icon: Users,
      status: 'idle',
      docsGenerated: 234,
      lastRun: '2025-10-06 03:30:00',
      nextRun: '2025-10-06 11:30:00'
    },
    {
      id: 'api-doc-agent',
      name: 'API Documentation Agent',
      description: 'Auto-generates OpenAPI/Swagger documentation from code',
      icon: Zap,
      status: 'idle',
      docsGenerated: 89,
      lastRun: '2025-10-06 02:00:00',
      nextRun: '2025-10-06 10:00:00'
    }
  ]);

  const [docs, setDocs] = useState<Documentation[]>([
    {
      id: 'getting-started',
      title: 'Getting Started with BizOSaaS',
      type: 'user-guide',
      status: 'generated',
      lastGenerated: '2025-10-06 04:15:00',
      generatedBy: 'user-guide-agent',
      language: 'simple',
      wordCount: 1245,
      sections: 8,
      autoUpdate: true
    },
    {
      id: 'llm-integration',
      title: 'LLM Provider Integration Guide',
      type: 'technical',
      status: 'generated',
      lastGenerated: '2025-10-06 04:00:00',
      generatedBy: 'technical-doc-agent',
      language: 'technical',
      wordCount: 2345,
      sections: 12,
      autoUpdate: true
    },
    {
      id: 'api-reference',
      title: 'Central Hub API Reference',
      type: 'api',
      status: 'generated',
      lastGenerated: '2025-10-06 02:00:00',
      generatedBy: 'api-doc-agent',
      language: 'technical',
      wordCount: 5678,
      sections: 45,
      autoUpdate: true
    },
    {
      id: 'multi-tenancy',
      title: 'Multi-Tenancy Architecture',
      type: 'developer',
      status: 'generated',
      lastGenerated: '2025-10-05 18:30:00',
      generatedBy: 'technical-doc-agent',
      language: 'technical',
      wordCount: 3456,
      sections: 15,
      autoUpdate: true
    },
    {
      id: 'feature-toggles',
      title: 'Feature Toggle Management',
      type: 'user-guide',
      status: 'generated',
      lastGenerated: '2025-10-05 16:00:00',
      generatedBy: 'user-guide-agent',
      language: 'simple',
      wordCount: 987,
      sections: 6,
      autoUpdate: false
    },
    {
      id: 'ai-agents',
      title: 'AI Agents Developer Guide',
      type: 'developer',
      status: 'outdated',
      lastGenerated: '2025-09-28 10:00:00',
      generatedBy: 'technical-doc-agent',
      language: 'technical',
      wordCount: 4123,
      sections: 20,
      autoUpdate: false
    },
    {
      id: 'authentication',
      title: 'Authentication & SSO Setup',
      type: 'technical',
      status: 'generated',
      lastGenerated: '2025-10-04 12:00:00',
      generatedBy: 'technical-doc-agent',
      language: 'technical',
      wordCount: 1876,
      sections: 10,
      autoUpdate: true
    },
    {
      id: 'tenant-onboarding',
      title: 'Tenant Onboarding Tutorial',
      type: 'user-guide',
      status: 'pending',
      lastGenerated: '',
      generatedBy: '',
      language: 'simple',
      wordCount: 0,
      sections: 0,
      autoUpdate: false
    }
  ]);

  const generateDoc = (docId: string) => {
    setIsGenerating(true);
    setDocs(docs.map(d =>
      d.id === docId ? { ...d, status: 'pending' as const } : d
    ));

    // Simulate doc generation
    setTimeout(() => {
      setDocs(docs.map(d =>
        d.id === docId
          ? {
              ...d,
              status: 'generated' as const,
              lastGenerated: new Date().toISOString(),
              generatedBy: 'user-guide-agent',
              wordCount: Math.floor(Math.random() * 3000) + 500,
              sections: Math.floor(Math.random() * 15) + 5
            }
          : d
      ));
      setIsGenerating(false);
    }, 3000);
  };

  const regenerateAll = () => {
    setIsGenerating(true);
    docs.filter(d => d.autoUpdate).forEach(doc => {
      generateDoc(doc.id);
    });
  };

  const stats = {
    total: docs.length,
    generated: docs.filter(d => d.status === 'generated').length,
    pending: docs.filter(d => d.status === 'pending').length,
    outdated: docs.filter(d => d.status === 'outdated').length
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'generated': return 'text-green-600 bg-green-100';
      case 'pending': return 'text-yellow-600 bg-yellow-100';
      case 'outdated': return 'text-orange-600 bg-orange-100';
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'technical': return Code;
      case 'user-guide': return Users;
      case 'api': return Zap;
      case 'developer': return BookOpen;
      default: return FileText;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-3">
            <FileText className="w-8 h-8 text-indigo-600" />
            <h1 className="text-3xl font-bold text-gray-900">Documentation Management</h1>
          </div>
          <button
            onClick={regenerateAll}
            disabled={isGenerating}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCw className={`w-4 h-4 ${isGenerating ? 'animate-spin' : ''}`} />
            Regenerate All
          </button>
        </div>
        <p className="text-gray-600">
          AI-powered documentation generation with simple language validation and auto-updates
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
              <FileText className="w-6 h-6 text-indigo-600" />
            </div>
            <span className="text-2xl font-bold text-gray-900">{stats.total}</span>
          </div>
          <p className="text-sm text-gray-600">Total Documents</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <span className="text-2xl font-bold text-green-600">{stats.generated}</span>
          </div>
          <p className="text-sm text-gray-600">Generated</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <Clock className="w-6 h-6 text-yellow-600" />
            </div>
            <span className="text-2xl font-bold text-yellow-600">{stats.pending}</span>
          </div>
          <p className="text-sm text-gray-600">Pending</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <AlertCircle className="w-6 h-6 text-orange-600" />
            </div>
            <span className="text-2xl font-bold text-orange-600">{stats.outdated}</span>
          </div>
          <p className="text-sm text-gray-600">Outdated</p>
        </div>
      </div>

      {/* AI Agents Section */}
      <div className="mb-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Documentation Agents</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {agents.map((agent) => {
            const AgentIcon = agent.icon;
            return (
              <div key={agent.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                    agent.status === 'active' ? 'bg-green-100' :
                    agent.status === 'generating' ? 'bg-blue-100 animate-pulse' :
                    'bg-gray-100'
                  }`}>
                    <AgentIcon className={`w-6 h-6 ${
                      agent.status === 'active' ? 'text-green-600' :
                      agent.status === 'generating' ? 'text-blue-600' :
                      'text-gray-600'
                    }`} />
                  </div>
                  <span className={`text-xs px-2 py-1 rounded ${
                    agent.status === 'active' ? 'bg-green-100 text-green-700' :
                    agent.status === 'generating' ? 'bg-blue-100 text-blue-700' :
                    'bg-gray-100 text-gray-700'
                  }`}>
                    {agent.status}
                  </span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{agent.name}</h3>
                <p className="text-sm text-gray-600 mb-4">{agent.description}</p>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-xs text-gray-500">Docs Generated</p>
                    <p className="text-lg font-semibold text-gray-900">{agent.docsGenerated}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Last Run</p>
                    <p className="text-xs text-gray-900">{new Date(agent.lastRun).toLocaleTimeString()}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Documents List */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">Documentation Library</h2>
          <p className="text-sm text-gray-600 mt-1">
            All platform documentation with AI-powered generation and updates
          </p>
        </div>

        <div className="divide-y divide-gray-200">
          {docs.map((doc) => {
            const TypeIcon = getTypeIcon(doc.type);
            return (
              <div
                key={doc.id}
                className="p-6 hover:bg-gray-50 transition-colors cursor-pointer"
                onClick={() => setSelectedDoc(doc.id === selectedDoc ? null : doc.id)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4 flex-1">
                    <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center flex-shrink-0">
                      <TypeIcon className="w-5 h-5 text-indigo-600" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">{doc.title}</h3>
                        <span className={`text-xs px-2 py-1 rounded ${getStatusColor(doc.status)}`}>
                          {doc.status}
                        </span>
                        <span className="text-xs px-2 py-1 rounded bg-gray-100 text-gray-700">
                          {doc.type}
                        </span>
                        {doc.autoUpdate && (
                          <span className="text-xs px-2 py-1 rounded bg-blue-100 text-blue-700">
                            Auto-update
                          </span>
                        )}
                      </div>

                      {doc.status === 'generated' && (
                        <div className="flex items-center gap-4 text-xs text-gray-500 mb-2">
                          <span>{doc.wordCount.toLocaleString()} words</span>
                          <span>{doc.sections} sections</span>
                          <span>Language: {doc.language}</span>
                          <span>Last updated: {new Date(doc.lastGenerated).toLocaleDateString()}</span>
                        </div>
                      )}

                      {selectedDoc === doc.id && (
                        <div className="mt-4 pt-4 border-t border-gray-100">
                          <div className="flex items-center gap-2 mb-3">
                            <Settings className="w-4 h-4 text-gray-400" />
                            <span className="text-sm font-medium text-gray-700">Document Actions</span>
                          </div>
                          <div className="flex flex-wrap gap-2">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                generateDoc(doc.id);
                              }}
                              disabled={isGenerating}
                              className="flex items-center gap-2 px-3 py-2 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50"
                            >
                              <RefreshCw className={`w-4 h-4 ${isGenerating ? 'animate-spin' : ''}`} />
                              Regenerate
                            </button>
                            <button className="flex items-center gap-2 px-3 py-2 bg-white text-gray-700 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                              <Eye className="w-4 h-4" />
                              Preview
                            </button>
                            <button className="flex items-center gap-2 px-3 py-2 bg-white text-gray-700 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                              <Download className="w-4 h-4" />
                              Download
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
