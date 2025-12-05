"use client"

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
  Globe, Settings, Info, Check, AlertTriangle,
  ChevronDown, RefreshCw
} from 'lucide-react'
import { useAuth } from '@/hooks/use-auth'
import { MultilingualManager, Language, MultilingualSettings } from '@/lib/multilingual-manager'

interface LanguageSelectorProps {
  onLanguageChange?: (language: string) => void
  className?: string
}

export function LanguageSelector({ onLanguageChange, className = "" }: LanguageSelectorProps) {
  const { user } = useAuth()
  const [multilingualManager] = useState(() => 
    new MultilingualManager('http://localhost:8001', user?.user.tenant_id || 'demo')
  )
  
  const [isInitialized, setIsInitialized] = useState(false)
  const [currentLanguage, setCurrentLanguage] = useState('en')
  const [availableLanguages, setAvailableLanguages] = useState<Language[]>([])
  const [settings, setSettings] = useState<MultilingualSettings | null>(null)
  const [showDetails, setShowDetails] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  const isAdmin = user?.user.role === 'super_admin' || user?.user.role === 'tenant_admin'

  // Initialize multilingual system
  useEffect(() => {
    initializeMultilingual()
  }, [])

  const initializeMultilingual = async () => {
    setIsLoading(true)
    try {
      await multilingualManager.initialize()
      
      setCurrentLanguage(multilingualManager.getCurrentLanguage())
      setAvailableLanguages(multilingualManager.getAvailableLanguages())
      setSettings(multilingualManager.getSettings())
      setIsInitialized(true)
    } catch (error) {
      console.error('Failed to initialize multilingual system:', error)
      // Set English as fallback
      setCurrentLanguage('en')
      setAvailableLanguages([{
        code: 'en',
        name: 'English',
        nativeName: 'English',
        flag: '🇺🇸',
        enabled: true,
        translationProgress: 100,
        lastUpdated: new Date().toISOString()
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleLanguageChange = async (languageCode: string) => {
    try {
      const success = await multilingualManager.changeLanguage(languageCode)
      if (success) {
        setCurrentLanguage(languageCode)
        if (onLanguageChange) {
          onLanguageChange(languageCode)
        }
      }
    } catch (error) {
      console.error('Failed to change language:', error)
    }
  }

  const getCurrentLanguageInfo = () => {
    return availableLanguages.find(lang => lang.code === currentLanguage)
  }

  const getProgressColor = (progress: number) => {
    if (progress >= 90) return 'text-green-600 bg-green-100'
    if (progress >= 70) return 'text-yellow-600 bg-yellow-100'
    if (progress >= 50) return 'text-orange-600 bg-orange-100'
    return 'text-red-600 bg-red-100'
  }

  // Don't render if multilingual is disabled or not initialized
  if (!isInitialized || !settings?.enabled) {
    return null
  }

  // If only English is available, don't show selector
  if (availableLanguages.length <= 1) {
    return null
  }

  const currentLangInfo = getCurrentLanguageInfo()

  if (isLoading) {
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <div className="w-4 h-4 rounded-full bg-gray-300 animate-pulse"></div>
        <span className="text-sm text-muted-foreground">Loading languages...</span>
      </div>
    )
  }

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      {/* Language Selector */}
      <Select value={currentLanguage} onValueChange={handleLanguageChange}>
        <SelectTrigger className="w-36">
          <div className="flex items-center space-x-2">
            <span className="text-lg">{currentLangInfo?.flag || '🌐'}</span>
            <SelectValue placeholder="Language" />
          </div>
        </SelectTrigger>
        <SelectContent>
          {availableLanguages.map((language) => (
            <SelectItem key={language.code} value={language.code}>
              <div className="flex items-center justify-between w-full">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">{language.flag}</span>
                  <span className="font-medium">{language.nativeName}</span>
                </div>
                <div className="flex items-center space-x-1">
                  {language.translationProgress < 100 && (
                    <Badge 
                      variant="secondary"
                      className={`text-xs ${getProgressColor(language.translationProgress)}`}
                    >
                      {language.translationProgress}%
                    </Badge>
                  )}
                  {language.code === currentLanguage && (
                    <Check className="w-3 h-3 text-green-500" />
                  )}
                </div>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      {/* Language Details Button */}
      <Dialog open={showDetails} onOpenChange={setShowDetails}>
        <DialogTrigger asChild>
          <Button variant="outline" size="sm">
            <Info className="w-4 h-4" />
          </Button>
        </DialogTrigger>
        
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center space-x-2">
              <Globe className="w-5 h-5" />
              <span>Language Settings</span>
            </DialogTitle>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* Current Language */}
            {currentLangInfo && (
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm flex items-center space-x-2">
                    <span className="text-xl">{currentLangInfo.flag}</span>
                    <span>Current Language</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Language:</span>
                    <span className="text-sm font-medium">{currentLangInfo.nativeName}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Code:</span>
                    <span className="text-sm font-medium">{currentLangInfo.code.toUpperCase()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Translation:</span>
                    <Badge className={getProgressColor(currentLangInfo.translationProgress)}>
                      {currentLangInfo.translationProgress}% Complete
                    </Badge>
                  </div>
                  {currentLangInfo.rtl && (
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Direction:</span>
                      <span className="text-sm font-medium">Right-to-Left</span>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Available Languages */}
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm">Available Languages</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {availableLanguages.map((language) => (
                    <div 
                      key={language.code} 
                      className="flex items-center justify-between p-2 rounded hover:bg-gray-50"
                    >
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">{language.flag}</span>
                        <div>
                          <span className="text-sm font-medium">{language.nativeName}</span>
                          <div className="text-xs text-muted-foreground">{language.name}</div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Badge 
                          variant="secondary"
                          className={`text-xs ${getProgressColor(language.translationProgress)}`}
                        >
                          {language.translationProgress}%
                        </Badge>
                        {language.code === currentLanguage && (
                          <Check className="w-3 h-3 text-green-500" />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Translation Status */}
            <Alert>
              <Info className="h-4 w-4" />
              <AlertDescription>
                {currentLangInfo?.translationProgress === 100 
                  ? 'This language is fully translated and ready to use.'
                  : `This language is ${currentLangInfo?.translationProgress}% translated. Some text may appear in English.`
                }
              </AlertDescription>
            </Alert>

            {/* Admin Notice */}
            {!isAdmin && (
              <Alert>
                <Settings className="h-4 w-4" />
                <AlertDescription>
                  Language availability is controlled by your administrator. Contact them to enable additional languages.
                </AlertDescription>
              </Alert>
            )}

            {/* Admin Controls */}
            {isAdmin && (
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm flex items-center space-x-2">
                    <Settings className="w-4 h-4" />
                    <span>Admin Controls</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-sm text-muted-foreground">
                    Manage language availability and translation settings in the Super Admin dashboard.
                  </div>
                </CardContent>
              </Card>
            )}

            <Button 
              onClick={() => setShowDetails(false)} 
              className="w-full"
            >
              Close
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Quick Language Indicator */}
      {currentLangInfo && (
        <div className="flex items-center space-x-1">
          <span className="text-xs text-muted-foreground">
            {currentLangInfo.code.toUpperCase()}
          </span>
          {currentLangInfo.translationProgress < 100 && (
            <div className="w-1 h-1 bg-yellow-500 rounded-full" title="Partial translation" />
          )}
        </div>
      )}
    </div>
  )
}