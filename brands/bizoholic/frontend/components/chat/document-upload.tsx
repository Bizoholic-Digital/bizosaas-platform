"use client"

import React, { useState, useCallback, useRef } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
  Upload, FileText, FileSpreadsheet, File, X, Check,
  AlertTriangle, Loader2, Download, Eye, Trash2,
  Package, ShoppingCart, BarChart3, Database,
  RefreshCw, ExternalLink, MessageCircle
} from 'lucide-react'
import { useAuth } from '@/hooks/use-auth'

interface DocumentFile {
  id: string
  file: File
  name: string
  size: number
  type: string
  status: 'pending' | 'uploading' | 'processing' | 'completed' | 'error'
  progress: number
  error?: string
  result?: {
    type: 'csv' | 'pdf' | 'excel' | 'json' | 'txt'
    structure?: any
    preview?: string
    ecommerce_potential?: boolean
    product_count?: number
    ai_analysis?: string
  }
}

interface UploadedDocument {
  id: string
  filename: string
  file_type: string
  file_size: number
  upload_date: string
  processing_status: string
  metadata: {
    type: 'csv' | 'pdf' | 'excel' | 'json' | 'txt'
    structure?: any
    preview?: string
    ecommerce_potential?: boolean
    product_count?: number
    ai_analysis?: string
  }
}

interface DocumentUploadProps {
  onDocumentProcessed?: (document: UploadedDocument) => void
  onReferenceDocument?: (document: UploadedDocument) => void
  className?: string
}

export function DocumentUpload({
  onDocumentProcessed,
  onReferenceDocument,
  className = ""
}: DocumentUploadProps) {
  const { user } = useAuth()
  const [files, setFiles] = useState<DocumentFile[]>([])
  const [uploadedDocs, setUploadedDocs] = useState<UploadedDocument[]>([])
  const [isDragOver, setIsDragOver] = useState(false)
  const [isLoadingDocs, setIsLoadingDocs] = useState(false)
  const [selectedTab, setSelectedTab] = useState('upload')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://api.bizoholic.net'
  const tenantId = user?.tenant_id || 'demo'

  // Load user documents on component mount
  React.useEffect(() => {
    loadUserDocuments()
  }, [])

  const loadUserDocuments = async () => {
    setIsLoadingDocs(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/documents/user`, {
        headers: {
          'x-tenant-id': tenantId
        }
      })

      if (response.ok) {
        const data = await response.json()
        setUploadedDocs(data.documents || [])
      }
    } catch (error) {
      console.error('Failed to load documents:', error)
    } finally {
      setIsLoadingDocs(false)
    }
  }

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(false)
  }, [])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(false)

    const droppedFiles = Array.from(e.dataTransfer.files)
    addFiles(droppedFiles)
  }, [])

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files ? Array.from(e.target.files) : []
    addFiles(selectedFiles)

    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }, [])

  const addFiles = (newFiles: File[]) => {
    const supportedTypes = [
      'text/csv',
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/vnd.ms-excel',
      'application/json',
      'text/plain'
    ]

    const validFiles = newFiles.filter(file => {
      if (!supportedTypes.includes(file.type)) return false
      if (file.size > 50 * 1024 * 1024) return false // 50MB limit
      return true
    })

    const documentFiles: DocumentFile[] = validFiles.map(file => ({
      id: `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'pending',
      progress: 0
    }))

    setFiles(prev => [...prev, ...documentFiles])
  }

  const uploadFile = async (documentFile: DocumentFile) => {
    try {
      setFiles(prev =>
        prev.map(f => f.id === documentFile.id
          ? { ...f, status: 'uploading', progress: 0 }
          : f
        )
      )

      const formData = new FormData()
      formData.append('file', documentFile.file)
      formData.append('filename', documentFile.name)

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setFiles(prev =>
          prev.map(f => f.id === documentFile.id && f.status === 'uploading'
            ? { ...f, progress: Math.min(f.progress + 10, 90) }
            : f
          )
        )
      }, 200)

      const response = await fetch(`${API_BASE_URL}/api/documents/upload`, {
        method: 'POST',
        headers: {
          'x-tenant-id': tenantId
        },
        body: formData
      })

      clearInterval(progressInterval)

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`)
      }

      const result = await response.json()

      setFiles(prev =>
        prev.map(f => f.id === documentFile.id
          ? {
            ...f,
            status: 'processing',
            progress: 100,
            result: result.metadata
          }
          : f
        )
      )

      // Poll for processing status
      pollProcessingStatus(result.document_id, documentFile.id)

    } catch (error) {
      setFiles(prev =>
        prev.map(f => f.id === documentFile.id
          ? {
            ...f,
            status: 'error',
            error: error instanceof Error ? error.message : 'Upload failed'
          }
          : f
        )
      )
    }
  }

  const pollProcessingStatus = async (documentId: string, fileId: string) => {
    const maxAttempts = 30 // 30 seconds max
    let attempts = 0

    const poll = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/documents/${documentId}/status`, {
          headers: {
            'x-tenant-id': tenantId
          }
        })

        if (response.ok) {
          const status = await response.json()

          if (status.processing_status === 'completed') {
            setFiles(prev =>
              prev.map(f => f.id === fileId
                ? { ...f, status: 'completed', result: status.metadata }
                : f
              )
            )

            // Refresh documents list
            loadUserDocuments()

            // Notify parent component
            if (onDocumentProcessed) {
              onDocumentProcessed(status)
            }

            return
          } else if (status.processing_status === 'error') {
            setFiles(prev =>
              prev.map(f => f.id === fileId
                ? { ...f, status: 'error', error: 'Processing failed' }
                : f
              )
            )
            return
          }
        }

        attempts++
        if (attempts < maxAttempts) {
          setTimeout(poll, 1000)
        } else {
          setFiles(prev =>
            prev.map(f => f.id === fileId
              ? { ...f, status: 'error', error: 'Processing timeout' }
              : f
            )
          )
        }
      } catch (error) {
        setFiles(prev =>
          prev.map(f => f.id === fileId
            ? { ...f, status: 'error', error: 'Status check failed' }
            : f
          )
        )
      }
    }

    poll()
  }

  const removeFile = (fileId: string) => {
    setFiles(prev => prev.filter(f => f.id !== fileId))
  }

  const uploadAllFiles = async () => {
    const pendingFiles = files.filter(f => f.status === 'pending')
    for (const file of pendingFiles) {
      await uploadFile(file)
    }
  }

  const getFileIcon = (type: string) => {
    if (type.includes('csv')) return <FileSpreadsheet className="w-5 h-5 text-green-500" />
    if (type.includes('pdf')) return <FileText className="w-5 h-5 text-red-500" />
    if (type.includes('excel') || type.includes('spreadsheet')) return <FileSpreadsheet className="w-5 h-5 text-blue-500" />
    return <File className="w-5 h-5 text-gray-500" />
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const importToEcommerce = async (document: UploadedDocument) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/documents/${document.id}/import-ecommerce`, {
        method: 'POST',
        headers: {
          'x-tenant-id': tenantId,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const result = await response.json()
        alert(`Import started: ${result.message}`)
        // Refresh document list to show updated status
        loadUserDocuments()
      }
    } catch (error) {
      console.error('Import failed:', error)
      alert('Import failed. Please try again.')
    }
  }

  const referenceDocument = (document: UploadedDocument) => {
    if (onReferenceDocument) {
      onReferenceDocument(document)
    }
  }

  return (
    <div className={className}>
      <Dialog>
        <DialogTrigger asChild>
          <Button variant="outline" size="sm">
            <Upload className="w-4 h-4 mr-2" />
            Upload Documents
          </Button>
        </DialogTrigger>

        <DialogContent className="max-w-4xl max-h-[80vh] overflow-hidden flex flex-col">
          <DialogHeader>
            <DialogTitle>Document Upload & Management</DialogTitle>
          </DialogHeader>

          <Tabs value={selectedTab} onValueChange={setSelectedTab} className="flex-1 flex flex-col">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="upload">Upload New</TabsTrigger>
              <TabsTrigger value="library">Document Library</TabsTrigger>
            </TabsList>

            <TabsContent value="upload" className="flex-1 flex flex-col space-y-4">
              {/* Drop Zone */}
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${isDragOver
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
                  }`}
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
              >
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">
                  Drop files here or click to browse
                </h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Supports CSV, PDF, Excel, JSON, and TXT files up to 50MB
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept=".csv,.pdf,.xlsx,.xls,.json,.txt"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <Button
                  onClick={() => fileInputRef.current?.click()}
                  variant="outline"
                >
                  Select Files
                </Button>
              </div>

              {/* File List */}
              {files.length > 0 && (
                <div className="space-y-3 flex-1 min-h-0">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">Files to Upload ({files.length})</h4>
                    <Button onClick={uploadAllFiles} size="sm">
                      Upload All
                    </Button>
                  </div>

                  <ScrollArea className="h-64">
                    <div className="space-y-2">
                      {files.map((file) => (
                        <Card key={file.id} className="p-3">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3 flex-1 min-w-0">
                              {getFileIcon(file.type)}
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium truncate">{file.name}</p>
                                <p className="text-xs text-muted-foreground">
                                  {formatFileSize(file.size)} • {file.type}
                                </p>
                              </div>
                              <Badge variant={
                                file.status === 'completed' ? 'default' :
                                  file.status === 'error' ? 'destructive' :
                                    file.status === 'processing' ? 'secondary' : 'outline'
                              }>
                                {file.status === 'uploading' && <Loader2 className="w-3 h-3 mr-1 animate-spin" />}
                                {file.status === 'completed' && <Check className="w-3 h-3 mr-1" />}
                                {file.status === 'error' && <AlertTriangle className="w-3 h-3 mr-1" />}
                                {file.status}
                              </Badge>
                            </div>

                            <div className="flex items-center space-x-2 ml-3">
                              {file.status === 'pending' && (
                                <Button size="sm" onClick={() => uploadFile(file)}>
                                  Upload
                                </Button>
                              )}
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => removeFile(file.id)}
                              >
                                <X className="w-4 h-4" />
                              </Button>
                            </div>
                          </div>

                          {file.status === 'uploading' && (
                            <Progress value={file.progress} className="mt-2" />
                          )}

                          {file.error && (
                            <Alert className="mt-2">
                              <AlertTriangle className="h-4 w-4" />
                              <AlertDescription>{file.error}</AlertDescription>
                            </Alert>
                          )}

                          {file.result && (
                            <div className="mt-2 p-2 bg-gray-50 rounded text-sm">
                              {file.result.ecommerce_potential && (
                                <div className="flex items-center space-x-2 text-green-600 mb-1">
                                  <ShoppingCart className="w-4 h-4" />
                                  <span>E-commerce data detected ({file.result.product_count} products)</span>
                                </div>
                              )}
                              {file.result.ai_analysis && (
                                <p className="text-muted-foreground">{file.result.ai_analysis}</p>
                              )}
                            </div>
                          )}
                        </Card>
                      ))}
                    </div>
                  </ScrollArea>
                </div>
              )}
            </TabsContent>

            <TabsContent value="library" className="flex-1 flex flex-col space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="font-medium">Your Documents ({uploadedDocs.length})</h4>
                <Button onClick={loadUserDocuments} size="sm" variant="outline">
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Refresh
                </Button>
              </div>

              {isLoadingDocs ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="w-6 h-6 animate-spin mr-2" />
                  Loading documents...
                </div>
              ) : (
                <ScrollArea className="flex-1">
                  <div className="space-y-3">
                    {uploadedDocs.map((doc) => (
                      <Card key={doc.id} className="p-4">
                        <div className="flex items-start justify-between">
                          <div className="flex items-start space-x-3 flex-1">
                            {getFileIcon(doc.file_type)}
                            <div className="flex-1 min-w-0">
                              <h5 className="font-medium truncate">{doc.filename}</h5>
                              <p className="text-sm text-muted-foreground">
                                {formatFileSize(doc.file_size)} • {new Date(doc.upload_date).toLocaleDateString()}
                              </p>

                              {doc.metadata.ecommerce_potential && (
                                <div className="flex items-center space-x-2 mt-1">
                                  <Badge variant="secondary" className="text-xs">
                                    <Package className="w-3 h-3 mr-1" />
                                    {doc.metadata.product_count} products
                                  </Badge>
                                </div>
                              )}

                              {doc.metadata.ai_analysis && (
                                <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
                                  {doc.metadata.ai_analysis}
                                </p>
                              )}
                            </div>
                          </div>

                          <div className="flex items-center space-x-2 ml-3">
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => referenceDocument(doc)}
                              title="Reference in conversation"
                            >
                              <MessageCircle className="w-4 h-4" />
                            </Button>

                            {doc.metadata.ecommerce_potential && (
                              <Button
                                size="sm"
                                onClick={() => importToEcommerce(doc)}
                                title="Import to e-commerce"
                              >
                                <ShoppingCart className="w-4 h-4" />
                              </Button>
                            )}
                          </div>
                        </div>
                      </Card>
                    ))}

                    {uploadedDocs.length === 0 && (
                      <div className="text-center py-8 text-muted-foreground">
                        No documents uploaded yet. Switch to the Upload tab to get started.
                      </div>
                    )}
                  </div>
                </ScrollArea>
              )}
            </TabsContent>
          </Tabs>
        </DialogContent>
      </Dialog>
    </div>
  )
}