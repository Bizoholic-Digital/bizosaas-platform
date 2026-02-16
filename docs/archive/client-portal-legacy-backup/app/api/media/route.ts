/**
 * Media Management API Route for Client Portal
 * Handles file uploads, media library, and asset management
 */

import { NextRequest, NextResponse } from 'next/server'

// Mock media data for demo
const mockMediaData = {
  files: [
    {
      id: 'media_001',
      name: 'company-logo.png',
      original_name: 'BizOSaaS-Logo.png',
      type: 'image',
      mime_type: 'image/png',
      size: 45678,
      size_human: '44.6 KB',
      url: '/api/placeholder/400/200',
      thumbnail: '/api/placeholder/150/150',
      width: 800,
      height: 400,
      alt_text: 'BizOSaaS Company Logo',
      created_at: '2024-09-20T10:30:00Z',
      updated_at: '2024-09-20T10:30:00Z',
      folder: 'branding',
      tags: ['logo', 'branding', 'header'],
      usage_count: 5,
      last_used: '2024-09-25T08:15:00Z'
    },
    {
      id: 'media_002',
      name: 'hero-banner.jpg',
      original_name: 'Website-Hero-Banner.jpg',
      type: 'image',
      mime_type: 'image/jpeg',
      size: 234567,
      size_human: '229.1 KB',
      url: '/api/placeholder/1200/600',
      thumbnail: '/api/placeholder/150/150',
      width: 1920,
      height: 1080,
      alt_text: 'Hero banner for website homepage',
      created_at: '2024-09-18T14:20:00Z',
      updated_at: '2024-09-22T16:45:00Z',
      folder: 'website',
      tags: ['hero', 'banner', 'homepage'],
      usage_count: 12,
      last_used: '2024-09-25T12:30:00Z'
    },
    {
      id: 'media_003',
      name: 'product-demo.mp4',
      original_name: 'BizOSaaS-Product-Demo-Video.mp4',
      type: 'video',
      mime_type: 'video/mp4',
      size: 15678901,
      size_human: '15.0 MB',
      url: '/api/placeholder/video/1280x720',
      thumbnail: '/api/placeholder/150/150',
      width: 1280,
      height: 720,
      duration: 180, // seconds
      alt_text: 'Product demonstration video',
      created_at: '2024-09-15T09:45:00Z',
      updated_at: '2024-09-15T09:45:00Z',
      folder: 'videos',
      tags: ['product', 'demo', 'marketing'],
      usage_count: 8,
      last_used: '2024-09-24T15:20:00Z'
    },
    {
      id: 'media_004',
      name: 'pricing-guide.pdf',
      original_name: 'BizOSaaS-Pricing-Guide-2024.pdf',
      type: 'document',
      mime_type: 'application/pdf',
      size: 567890,
      size_human: '554.6 KB',
      url: '/api/placeholder/document/pricing-guide.pdf',
      thumbnail: '/api/placeholder/150/150',
      pages: 8,
      alt_text: 'BizOSaaS pricing guide document',
      created_at: '2024-09-12T11:15:00Z',
      updated_at: '2024-09-20T13:30:00Z',
      folder: 'documents',
      tags: ['pricing', 'guide', 'sales'],
      usage_count: 23,
      last_used: '2024-09-25T10:10:00Z'
    },
    {
      id: 'media_005',
      name: 'team-photo.jpg',
      original_name: 'BizOSaaS-Team-Photo-2024.jpg',
      type: 'image',
      mime_type: 'image/jpeg',
      size: 345678,
      size_human: '337.6 KB',
      url: '/api/placeholder/800/600',
      thumbnail: '/api/placeholder/150/150',
      width: 1600,
      height: 1200,
      alt_text: 'BizOSaaS team photo',
      created_at: '2024-09-10T16:00:00Z',
      updated_at: '2024-09-10T16:00:00Z',
      folder: 'team',
      tags: ['team', 'about', 'people'],
      usage_count: 3,
      last_used: '2024-09-22T14:25:00Z'
    },
    {
      id: 'media_006',
      name: 'icon-set.svg',
      original_name: 'BizOSaaS-Icons-Set.svg',
      type: 'image',
      mime_type: 'image/svg+xml',
      size: 12345,
      size_human: '12.1 KB',
      url: '/api/placeholder/icon/icon-set.svg',
      thumbnail: '/api/placeholder/150/150',
      alt_text: 'BizOSaaS icon set collection',
      created_at: '2024-09-08T13:45:00Z',
      updated_at: '2024-09-18T10:20:00Z',
      folder: 'icons',
      tags: ['icons', 'ui', 'design'],
      usage_count: 45,
      last_used: '2024-09-25T11:50:00Z'
    }
  ],
  folders: [
    {
      id: 'folder_001',
      name: 'branding',
      display_name: 'Branding Assets',
      description: 'Logos, brand guidelines, and identity assets',
      file_count: 8,
      created_at: '2024-09-01T10:00:00Z'
    },
    {
      id: 'folder_002',
      name: 'website',
      display_name: 'Website Content',
      description: 'Images and content for website pages',
      file_count: 15,
      created_at: '2024-09-01T10:05:00Z'
    },
    {
      id: 'folder_003',
      name: 'videos',
      display_name: 'Video Content',
      description: 'Marketing videos and demonstrations',
      file_count: 4,
      created_at: '2024-09-01T10:10:00Z'
    },
    {
      id: 'folder_004',
      name: 'documents',
      display_name: 'Documents',
      description: 'PDFs, guides, and documentation',
      file_count: 12,
      created_at: '2024-09-01T10:15:00Z'
    },
    {
      id: 'folder_005',
      name: 'team',
      display_name: 'Team Photos',
      description: 'Team member photos and group pictures',
      file_count: 6,
      created_at: '2024-09-01T10:20:00Z'
    },
    {
      id: 'folder_006',
      name: 'icons',
      display_name: 'Icons & Graphics',
      description: 'Icon sets and graphic elements',
      file_count: 23,
      created_at: '2024-09-01T10:25:00Z'
    }
  ],
  storage: {
    total_storage: 2147483648, // 2GB
    used_storage: 234567890, // ~234MB
    used_percentage: 10.9,
    remaining_storage: 1912915758,
    files_count: 68,
    last_cleanup: '2024-09-20T02:00:00Z'
  },
  upload_settings: {
    max_file_size: 52428800, // 50MB
    allowed_types: ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml', 'video/mp4', 'video/webm', 'application/pdf', 'text/plain'],
    auto_optimize_images: true,
    generate_thumbnails: true,
    scan_for_duplicates: true
  }
}

// GET /api/media - Fetch media library
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const folder = searchParams.get('folder')
    const type = searchParams.get('type')
    const search = searchParams.get('search')
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '20')
    const sort = searchParams.get('sort') || 'created_at'
    const order = searchParams.get('order') || 'desc'
    
    console.log('[CLIENT-PORTAL] GET media library', { folder, type, search, page, limit })
    
    // Simulate slight delay
    await new Promise(resolve => setTimeout(resolve, 200))
    
    // Filter files based on query parameters
    let filteredFiles = [...mockMediaData.files]
    
    if (folder && folder !== 'all') {
      filteredFiles = filteredFiles.filter(file => file.folder === folder)
    }
    
    if (type && type !== 'all') {
      filteredFiles = filteredFiles.filter(file => file.type === type)
    }
    
    if (search) {
      filteredFiles = filteredFiles.filter(file => 
        file.name.toLowerCase().includes(search.toLowerCase()) ||
        file.alt_text.toLowerCase().includes(search.toLowerCase()) ||
        file.tags.some(tag => tag.toLowerCase().includes(search.toLowerCase()))
      )
    }
    
    // Sort files
    filteredFiles.sort((a, b) => {
      const aVal = a[sort as keyof typeof a]
      const bVal = b[sort as keyof typeof b]
      if (order === 'desc') {
        return aVal > bVal ? -1 : 1
      } else {
        return aVal < bVal ? -1 : 1
      }
    })
    
    // Paginate results
    const startIndex = (page - 1) * limit
    const paginatedFiles = filteredFiles.slice(startIndex, startIndex + limit)
    
    return NextResponse.json({
      success: true,
      data: {
        files: paginatedFiles,
        folders: mockMediaData.folders,
        storage: mockMediaData.storage,
        upload_settings: mockMediaData.upload_settings,
        pagination: {
          current_page: page,
          total_pages: Math.ceil(filteredFiles.length / limit),
          total_files: filteredFiles.length,
          per_page: limit
        },
        filters_applied: {
          folder,
          type,
          search
        }
      },
      last_updated: new Date().toISOString(),
      source: "fallback"
    })
  } catch (error) {
    console.error('Error fetching media:', error)
    return NextResponse.json(
      { error: 'Failed to fetch media', details: error.message },
      { status: 500 }
    )
  }
}

// POST /api/media - Upload new media file
export async function POST(request: NextRequest) {
  try {
    console.log('[CLIENT-PORTAL] POST upload media file')
    
    // Simulate file upload processing
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Generate mock uploaded file data
    const uploadedFile = {
      id: 'media_' + Date.now(),
      name: 'uploaded-file-' + Date.now(),
      original_name: 'user-uploaded-file.jpg',
      type: 'image',
      mime_type: 'image/jpeg',
      size: Math.floor(Math.random() * 500000) + 100000,
      size_human: '245.8 KB',
      url: '/api/placeholder/800/600',
      thumbnail: '/api/placeholder/150/150',
      width: 1024,
      height: 768,
      alt_text: 'User uploaded image',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      folder: 'uploads',
      tags: ['uploaded'],
      usage_count: 0,
      last_used: null
    }
    
    return NextResponse.json({
      success: true,
      message: 'File uploaded successfully',
      file: uploadedFile,
      upload_id: 'upload_' + Date.now(),
      source: "fallback"
    })
  } catch (error) {
    console.error('Error uploading media:', error)
    return NextResponse.json(
      { error: 'Failed to upload media', details: error.message },
      { status: 500 }
    )
  }
}

// PUT /api/media - Update media file metadata
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const { file_id, updates } = body
    
    console.log(`[CLIENT-PORTAL] PUT update media file: ${file_id}`)
    
    if (!file_id) {
      return NextResponse.json(
        { error: 'File ID is required' },
        { status: 400 }
      )
    }
    
    // Simulate update
    await new Promise(resolve => setTimeout(resolve, 300))
    
    return NextResponse.json({
      success: true,
      message: 'Media file updated successfully',
      file_id,
      updates_applied: Object.keys(updates),
      updated_at: new Date().toISOString(),
      source: "fallback"
    })
  } catch (error) {
    console.error('Error updating media:', error)
    return NextResponse.json(
      { error: 'Failed to update media', details: error.message },
      { status: 500 }
    )
  }
}

// DELETE /api/media - Delete media file
export async function DELETE(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const fileId = searchParams.get('fileId')
    
    console.log(`[CLIENT-PORTAL] DELETE media file: ${fileId}`)
    
    if (!fileId) {
      return NextResponse.json(
        { error: 'File ID is required' },
        { status: 400 }
      )
    }
    
    // Simulate deletion
    await new Promise(resolve => setTimeout(resolve, 400))
    
    return NextResponse.json({
      success: true,
      message: 'Media file deleted successfully',
      file_id: fileId,
      deleted_at: new Date().toISOString(),
      source: "fallback"
    })
  } catch (error) {
    console.error('Error deleting media:', error)
    return NextResponse.json(
      { error: 'Failed to delete media', details: error.message },
      { status: 500 }
    )
  }
}