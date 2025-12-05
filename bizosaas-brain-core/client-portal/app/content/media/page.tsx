'use client';

import React, { useState, useEffect } from 'react';
import { 
  Image, Plus, Search, Filter, Download, RefreshCw, Upload,
  Edit, Eye, Trash2, MoreHorizontal, Folder, Grid3X3, List,
  Video, Music, FileText, Archive, Star, Calendar, User,
  HardDrive, Play, Pause, Volume2, Copy, Share2, Tags
} from 'lucide-react';
import DashboardLayout from '../../../components/ui/dashboard-layout';

const MediaPage = () => {
  const [loading, setLoading] = useState(true);
  const [mediaFiles, setMediaFiles] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedCategory, setSelectedCategory] = useState('all');

  useEffect(() => {
    const fetchMedia = async () => {
      try {
        setLoading(true);
        // Mock API call - replace with actual Wagtail Media API calls through Brain Hub
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setMediaFiles([
          {
            id: '1',
            name: 'hero-banner.jpg',
            originalName: 'hero-banner-2024.jpg',
            type: 'image',
            mimeType: 'image/jpeg',
            category: 'banners',
            size: 2400000, // bytes
            dimensions: { width: 1920, height: 1080 },
            uploadDate: '2024-09-24T08:00:00Z',
            uploadedBy: 'Marketing Team',
            usedIn: 3,
            url: '/media/hero-banner.jpg',
            thumbnail: '/media/thumbnails/hero-banner.jpg',
            alt: 'Hero banner showcasing digital marketing services',
            tags: ['hero', 'banner', 'marketing', 'homepage'],
            featured: true,
            avgLoadTime: 1.2,
            viewCount: 15420
          },
          {
            id: '2',
            name: 'company-logo.svg',
            originalName: 'bizosaas-logo-final.svg',
            type: 'image',
            mimeType: 'image/svg+xml',
            category: 'logos',
            size: 45000,
            dimensions: { width: 500, height: 500 },
            uploadDate: '2024-09-23T12:00:00Z',
            uploadedBy: 'Design Team',
            usedIn: 8,
            url: '/media/company-logo.svg',
            thumbnail: '/media/thumbnails/company-logo.svg',
            alt: 'BizOSaaS company logo',
            tags: ['logo', 'brand', 'identity', 'svg'],
            featured: true,
            avgLoadTime: 0.3,
            viewCount: 8970
          },
          {
            id: '3',
            name: 'demo-video.mp4',
            originalName: 'platform-demo-final.mp4',
            type: 'video',
            mimeType: 'video/mp4',
            category: 'videos',
            size: 45000000,
            dimensions: { width: 1280, height: 720 },
            duration: 180, // seconds
            uploadDate: '2024-09-22T15:30:00Z',
            uploadedBy: 'Video Team',
            usedIn: 2,
            url: '/media/demo-video.mp4',
            thumbnail: '/media/thumbnails/demo-video.jpg',
            alt: 'Platform demo video showing key features',
            tags: ['demo', 'video', 'features', 'tutorial'],
            featured: false,
            avgLoadTime: 5.8,
            viewCount: 3450
          },
          {
            id: '4',
            name: 'team-photo.jpg',
            originalName: 'team-photo-conference-2024.jpg',
            type: 'image',
            mimeType: 'image/jpeg',
            category: 'team',
            size: 1800000,
            dimensions: { width: 1600, height: 900 },
            uploadDate: '2024-09-21T10:15:00Z',
            uploadedBy: 'HR Team',
            usedIn: 1,
            url: '/media/team-photo.jpg',
            thumbnail: '/media/thumbnails/team-photo.jpg',
            alt: 'Team photo from 2024 conference',
            tags: ['team', 'photo', 'conference', '2024'],
            featured: false,
            avgLoadTime: 2.1,
            viewCount: 2340
          },
          {
            id: '5',
            name: 'product-showcase.png',
            originalName: 'product-showcase-dashboard.png',
            type: 'image',
            mimeType: 'image/png',
            category: 'screenshots',
            size: 890000,
            dimensions: { width: 1440, height: 900 },
            uploadDate: '2024-09-20T14:20:00Z',
            uploadedBy: 'Product Team',
            usedIn: 5,
            url: '/media/product-showcase.png',
            thumbnail: '/media/thumbnails/product-showcase.png',
            alt: 'Product dashboard screenshot',
            tags: ['product', 'dashboard', 'screenshot', 'interface'],
            featured: true,
            avgLoadTime: 1.8,
            viewCount: 6780
          },
          {
            id: '6',
            name: 'background-music.mp3',
            originalName: 'corporate-background-track.mp3',
            type: 'audio',
            mimeType: 'audio/mp3',
            category: 'audio',
            size: 5400000,
            duration: 120, // seconds
            uploadDate: '2024-09-19T11:45:00Z',
            uploadedBy: 'Content Team',
            usedIn: 1,
            url: '/media/background-music.mp3',
            thumbnail: '/media/thumbnails/audio-placeholder.svg',
            alt: 'Corporate background music track',
            tags: ['music', 'background', 'corporate', 'audio'],
            featured: false,
            avgLoadTime: 3.2,
            viewCount: 890
          },
          {
            id: '7',
            name: 'pricing-guide.pdf',
            originalName: 'pricing-guide-2024.pdf',
            type: 'document',
            mimeType: 'application/pdf',
            category: 'documents',
            size: 1200000,
            pageCount: 12,
            uploadDate: '2024-09-18T16:00:00Z',
            uploadedBy: 'Sales Team',
            usedIn: 3,
            url: '/media/pricing-guide.pdf',
            thumbnail: '/media/thumbnails/pdf-placeholder.svg',
            alt: 'Pricing guide document',
            tags: ['pricing', 'guide', 'sales', 'document'],
            featured: false,
            avgLoadTime: 2.5,
            viewCount: 1560
          }
        ]);
      } catch (error) {
        console.error('Failed to fetch media:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMedia();
  }, []);

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getFileIcon = (type: string, mimeType: string) => {
    switch (type) {
      case 'image':
        return <Image className="w-5 h-5" />;
      case 'video':
        return <Video className="w-5 h-5" />;
      case 'audio':
        return <Music className="w-5 h-5" />;
      case 'document':
        return <FileText className="w-5 h-5" />;
      default:
        return <Archive className="w-5 h-5" />;
    }
  };

  const getTypeBadge = (type: string) => {
    const typeConfig = {
      image: { color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300', label: 'Image' },
      video: { color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300', label: 'Video' },
      audio: { color: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300', label: 'Audio' },
      document: { color: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300', label: 'Document' }
    };

    const config = typeConfig[type as keyof typeof typeConfig] || { color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300', label: type };
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const filteredMedia = mediaFiles.filter(file => {
    const matchesSearch = file.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         file.alt.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         file.tags.some((tag: string) => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesType = selectedFilter === 'all' || file.type === selectedFilter;
    const matchesCategory = selectedCategory === 'all' || file.category === selectedCategory;
    return matchesSearch && matchesType && matchesCategory;
  });

  const stats = {
    total: mediaFiles.length,
    images: mediaFiles.filter(f => f.type === 'image').length,
    videos: mediaFiles.filter(f => f.type === 'video').length,
    audio: mediaFiles.filter(f => f.type === 'audio').length,
    documents: mediaFiles.filter(f => f.type === 'document').length,
    totalSize: mediaFiles.reduce((sum, f) => sum + f.size, 0),
    totalUsage: mediaFiles.reduce((sum, f) => sum + f.usedIn, 0)
  };

  if (loading) {
    return (
      <DashboardLayout title="Media Library" description="Manage your media files">
        <div className="p-6 animate-pulse">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
            ))}
          </div>
          <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Media Library" description="Manage your media files and assets">
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Media Library</h1>
            <p className="text-gray-600 dark:text-gray-300">Manage images, videos, audio files, and documents</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1 border border-gray-300 dark:border-gray-600 rounded-lg">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded-l-lg ${viewMode === 'grid' ? 'bg-blue-600 text-white' : 'hover:bg-gray-50 dark:hover:bg-gray-700'}`}
              >
                <Grid3X3 className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded-r-lg ${viewMode === 'list' ? 'bg-blue-600 text-white' : 'hover:bg-gray-50 dark:hover:bg-gray-700'}`}
              >
                <List className="w-4 h-4" />
              </button>
            </div>
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
              <Folder className="w-4 h-4" />
              New Folder
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              <Upload className="w-4 h-4" />
              Upload Files
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-6 gap-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <Archive className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Total Files</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
                <Image className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Images</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.images}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-lg">
                <Video className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Videos</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.videos}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-orange-100 dark:bg-orange-900 rounded-lg">
                <FileText className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Documents</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.documents}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-indigo-100 dark:bg-indigo-900 rounded-lg">
                <HardDrive className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Total Size</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{formatFileSize(stats.totalSize)}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-pink-100 dark:bg-pink-900 rounded-lg">
                <Star className="w-6 h-6 text-pink-600 dark:text-pink-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Usage</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.totalUsage}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search files by name, alt text, or tags..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 w-full border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            <select
              value={selectedFilter}
              onChange={(e) => setSelectedFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Types</option>
              <option value="image">Images</option>
              <option value="video">Videos</option>
              <option value="audio">Audio</option>
              <option value="document">Documents</option>
            </select>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Categories</option>
              <option value="banners">Banners</option>
              <option value="logos">Logos</option>
              <option value="team">Team</option>
              <option value="screenshots">Screenshots</option>
              <option value="videos">Videos</option>
              <option value="documents">Documents</option>
            </select>
            <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
              <RefreshCw className="w-4 h-4 text-gray-600 dark:text-gray-300" />
            </button>
          </div>
        </div>

        {/* Media Grid/List */}
        {viewMode === 'grid' ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
            {filteredMedia.map((file) => (
              <div key={file.id} className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden group">
                {/* Thumbnail */}
                <div className="aspect-square bg-gray-100 dark:bg-gray-700 relative overflow-hidden">
                  {file.type === 'image' ? (
                    <img 
                      src={file.thumbnail} 
                      alt={file.alt}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.style.display = 'none';
                        target.nextElementSibling?.classList.remove('hidden');
                      }}
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      {getFileIcon(file.type, file.mimeType)}
                    </div>
                  )}
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                    <div className="flex gap-2">
                      <button className="p-2 bg-white rounded-full shadow-md hover:bg-gray-100">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="p-2 bg-white rounded-full shadow-md hover:bg-gray-100">
                        <Download className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  {file.featured && (
                    <div className="absolute top-2 left-2">
                      <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    </div>
                  )}
                  {file.type === 'video' && file.duration && (
                    <div className="absolute bottom-2 right-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded text-xs">
                      {formatDuration(file.duration)}
                    </div>
                  )}
                </div>

                {/* File Info */}
                <div className="p-3">
                  <div className="flex items-center gap-2 mb-2">
                    {getTypeBadge(file.type)}
                    {file.usedIn > 0 && (
                      <span className="text-xs text-green-600 dark:text-green-400">
                        Used {file.usedIn}x
                      </span>
                    )}
                  </div>
                  <h4 className="text-sm font-medium text-gray-900 dark:text-white truncate mb-1">
                    {file.name}
                  </h4>
                  <div className="text-xs text-gray-500 dark:text-gray-400 space-y-1">
                    <div>{formatFileSize(file.size)}</div>
                    {file.dimensions && (
                      <div>{file.dimensions.width} × {file.dimensions.height}</div>
                    )}
                    <div>{new Date(file.uploadDate).toLocaleDateString()}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    File
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Size
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Dimensions
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Usage
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Uploaded
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {filteredMedia.map((file) => (
                  <tr key={file.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-10 h-10 flex-shrink-0 mr-4">
                          {file.type === 'image' ? (
                            <img 
                              src={file.thumbnail} 
                              alt={file.alt}
                              className="w-10 h-10 rounded-lg object-cover"
                            />
                          ) : (
                            <div className="w-10 h-10 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                              {getFileIcon(file.type, file.mimeType)}
                            </div>
                          )}
                        </div>
                        <div>
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {file.name}
                            {file.featured && <Star className="w-4 h-4 text-yellow-500 inline ml-1" />}
                          </div>
                          <div className="text-sm text-gray-500 dark:text-gray-400 truncate max-w-xs">
                            {file.alt}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {getTypeBadge(file.type)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {formatFileSize(file.size)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {file.dimensions 
                        ? `${file.dimensions.width} × ${file.dimensions.height}`
                        : file.duration 
                        ? formatDuration(file.duration)
                        : '-'
                      }
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {file.usedIn > 0 ? (
                        <span className="text-green-600 dark:text-green-400">
                          Used in {file.usedIn} place{file.usedIn > 1 ? 's' : ''}
                        </span>
                      ) : (
                        <span className="text-gray-500 dark:text-gray-400">Unused</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900 dark:text-white">
                        {new Date(file.uploadDate).toLocaleDateString()}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        by {file.uploadedBy}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center gap-2 justify-end">
                        <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300">
                          <Download className="w-4 h-4" />
                        </button>
                        <button className="text-purple-600 hover:text-purple-900 dark:text-purple-400 dark:hover:text-purple-300">
                          <Copy className="w-4 h-4" />
                        </button>
                        <button className="text-orange-600 hover:text-orange-900 dark:text-orange-400 dark:hover:text-orange-300">
                          <Share2 className="w-4 h-4" />
                        </button>
                        <button className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300">
                          <MoreHorizontal className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {filteredMedia.length === 0 && (
          <div className="text-center py-12">
            <Image className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No media files found</h3>
            <p className="text-gray-500 dark:text-gray-400">
              {searchTerm ? 'Try adjusting your search terms' : 'Get started by uploading your first media file'}
            </p>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default MediaPage;