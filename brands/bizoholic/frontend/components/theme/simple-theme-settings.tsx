'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useTheme } from 'next-themes'
import {
  Palette,
  Save,
  RotateCcw,
  Eye,
  Moon,
  Sun,
  Monitor
} from 'lucide-react'

interface ThemePreset {
  name: string
  displayName: string
  description: string
  primaryColor: string
  secondaryColor: string
  accentColor: string
}

const themePresets: ThemePreset[] = [
  {
    name: 'default',
    displayName: 'Ocean Blue (Default)',
    description: 'Clean and professional blue theme',
    primaryColor: '#3B82F6',
    secondaryColor: '#EFF6FF',
    accentColor: '#1D4ED8'
  },
  {
    name: 'forest',
    displayName: 'Forest Green',
    description: 'Nature-inspired green theme',
    primaryColor: '#059669',
    secondaryColor: '#ECFDF5',
    accentColor: '#047857'
  },
  {
    name: 'sunset',
    displayName: 'Sunset Orange',
    description: 'Warm and energetic orange theme',
    primaryColor: '#EA580C',
    secondaryColor: '#FFF7ED',
    accentColor: '#C2410C'
  },
  {
    name: 'purple',
    displayName: 'Royal Purple',
    description: 'Luxurious purple theme',
    primaryColor: '#9333EA',
    secondaryColor: '#FAF5FF',
    accentColor: '#7C3AED'
  },
  {
    name: 'coral',
    displayName: 'Coral Pink',
    description: 'Modern coral theme',
    primaryColor: '#F43F5E',
    secondaryColor: '#FFF1F2',
    accentColor: '#E11D48'
  }
]

export function SimpleThemeSettings() {
  const { theme, setTheme } = useTheme()
  const isDarkMode = theme === 'dark'
  const [selectedTheme, setSelectedTheme] = useState(themePresets[0])
  const [customPrimary, setCustomPrimary] = useState(selectedTheme.primaryColor)
  const [customSecondary, setCustomSecondary] = useState(selectedTheme.secondaryColor)
  const [customAccent, setCustomAccent] = useState(selectedTheme.accentColor)

  // Load theme from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('bizosaas-simple-theme')

    if (savedTheme) {
      const themePreset = themePresets.find(t => t.name === savedTheme) || themePresets[0]
      setSelectedTheme(themePreset)
      setCustomPrimary(themePreset.primaryColor)
      setCustomSecondary(themePreset.secondaryColor)
      setCustomAccent(themePreset.accentColor)
      applyThemeToDocument(themePreset)
    } else {
      applyThemeToDocument(themePresets[0])
    }
  }, [])

  const applyThemeToDocument = (themePreset: ThemePreset) => {
    const root = document.documentElement

    // Apply CSS custom properties for brand colors
    root.style.setProperty('--primary-brand', themePreset.primaryColor)
    root.style.setProperty('--secondary-brand', themePreset.secondaryColor)
    root.style.setProperty('--accent-brand', themePreset.accentColor)
  }

  const handlePresetSelect = (preset: ThemePreset) => {
    setSelectedTheme(preset)
    setCustomPrimary(preset.primaryColor)
    setCustomSecondary(preset.secondaryColor)
    setCustomAccent(preset.accentColor)

    applyThemeToDocument(preset)

    // Save to localStorage
    localStorage.setItem('bizosaas-simple-theme', preset.name)
  }

  const handleCustomColorChange = () => {
    const customTheme: ThemePreset = {
      ...selectedTheme,
      name: 'custom',
      displayName: 'Custom Theme',
      primaryColor: customPrimary,
      secondaryColor: customSecondary,
      accentColor: customAccent
    }

    applyThemeToDocument(customTheme)
    localStorage.setItem('bizosaas-custom-colors', JSON.stringify({
      primary: customPrimary,
      secondary: customSecondary,
      accent: customAccent
    }))
  }

  const cycleTheme = () => {
    const themes = ['light', 'dark', 'system'] as const
    const currentIndex = themes.indexOf(theme as typeof themes[number] || 'system')
    const nextIndex = (currentIndex + 1) % themes.length
    setTheme(themes[nextIndex])
  }

  const getThemeIcon = () => {
    switch (theme) {
      case 'light':
        return Sun
      case 'dark':
        return Moon
      case 'system':
        return Monitor
      default:
        return Monitor
    }
  }

  const getThemeLabel = () => {
    switch (theme) {
      case 'light':
        return 'Light'
      case 'dark':
        return 'Dark'
      case 'system':
        return 'System'
      default:
        return 'System'
    }
  }

  const resetToDefault = () => {
    const defaultTheme = themePresets[0]
    setSelectedTheme(defaultTheme)
    setCustomPrimary(defaultTheme.primaryColor)
    setCustomSecondary(defaultTheme.secondaryColor)
    setCustomAccent(defaultTheme.accentColor)
    setTheme('light')

    applyThemeToDocument(defaultTheme)
    localStorage.removeItem('bizosaas-simple-theme')
    localStorage.removeItem('bizosaas-dark-mode')
    localStorage.removeItem('bizosaas-custom-colors')
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <Palette className="w-6 h-6" />
            Theme Customization
          </h2>
          <p className="text-muted-foreground">
            Personalize your dashboard with custom colors and themes
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={cycleTheme}>
            {(() => {
              const Icon = getThemeIcon()
              return <Icon className="w-4 h-4 mr-2" />
            })()}
            {getThemeLabel()} Mode
          </Button>
          <Button variant="outline" size="sm" onClick={resetToDefault}>
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
        </div>
      </div>

      {/* Current Theme Info */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Eye className="w-5 h-5" />
            Current Theme
          </CardTitle>
          <CardDescription>
            Active theme configuration and preview
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-medium">{selectedTheme.displayName}</h3>
              <p className="text-sm text-muted-foreground">{selectedTheme.description}</p>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant={isDarkMode ? 'default' : 'secondary'}>
                {isDarkMode ? 'Dark Mode' : 'Light Mode'}
              </Badge>
            </div>
          </div>

          {/* Theme Preview */}
          <div className="p-4 rounded-lg border space-y-3" style={{
            backgroundColor: selectedTheme.secondaryColor,
            borderColor: selectedTheme.accentColor + '40'
          }}>
            <div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 p-3 rounded">
              <div className="text-sm font-medium">Theme Preview</div>
              <div className="text-xs text-gray-500 dark:text-gray-400">Sample dashboard content</div>
            </div>
            <div className="flex space-x-2">
              <div
                className="px-3 py-1 rounded text-xs text-white font-medium"
                style={{ backgroundColor: selectedTheme.primaryColor }}
              >
                Primary Button
              </div>
              <div
                className="px-3 py-1 rounded text-xs"
                style={{
                  backgroundColor: selectedTheme.secondaryColor,
                  color: selectedTheme.primaryColor,
                  border: `1px solid ${selectedTheme.primaryColor}`
                }}
              >
                Secondary Button
              </div>
              <div
                className="px-3 py-1 rounded text-xs text-white font-medium"
                style={{ backgroundColor: selectedTheme.accentColor }}
              >
                Accent
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Theme Presets */}
      <Card>
        <CardHeader>
          <CardTitle>Theme Presets</CardTitle>
          <CardDescription>
            Choose from carefully crafted theme presets
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {themePresets.map((preset) => (
              <div key={preset.name} className="space-y-2">
                <div className="flex items-center justify-between">
                  <h4 className="font-medium text-sm">{preset.displayName}</h4>
                  <Button
                    size="sm"
                    variant={selectedTheme.name === preset.name ? "default" : "outline"}
                    onClick={() => handlePresetSelect(preset)}
                  >
                    {selectedTheme.name === preset.name ? "Active" : "Apply"}
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground">{preset.description}</p>

                {/* Mini Preview */}
                <div className="p-2 rounded border space-y-2" style={{ backgroundColor: preset.secondaryColor }}>
                  <div className="flex space-x-1">
                    <div
                      className="w-4 h-4 rounded"
                      style={{ backgroundColor: preset.primaryColor }}
                    />
                    <div
                      className="w-4 h-4 rounded"
                      style={{ backgroundColor: preset.accentColor }}
                    />
                    <div className="w-4 h-4 rounded bg-white border" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Custom Colors */}
      <Card>
        <CardHeader>
          <CardTitle>Custom Colors</CardTitle>
          <CardDescription>
            Fine-tune colors to match your brand
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <Label>Primary Color</Label>
              <div className="flex items-center space-x-2">
                <Input
                  type="color"
                  value={customPrimary}
                  onChange={(e) => setCustomPrimary(e.target.value)}
                  className="w-12 h-8 p-0 border-0"
                />
                <Input
                  value={customPrimary}
                  onChange={(e) => setCustomPrimary(e.target.value)}
                  placeholder="#3B82F6"
                  className="font-mono text-xs"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label>Secondary Color</Label>
              <div className="flex items-center space-x-2">
                <Input
                  type="color"
                  value={customSecondary}
                  onChange={(e) => setCustomSecondary(e.target.value)}
                  className="w-12 h-8 p-0 border-0"
                />
                <Input
                  value={customSecondary}
                  onChange={(e) => setCustomSecondary(e.target.value)}
                  placeholder="#EFF6FF"
                  className="font-mono text-xs"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label>Accent Color</Label>
              <div className="flex items-center space-x-2">
                <Input
                  type="color"
                  value={customAccent}
                  onChange={(e) => setCustomAccent(e.target.value)}
                  className="w-12 h-8 p-0 border-0"
                />
                <Input
                  value={customAccent}
                  onChange={(e) => setCustomAccent(e.target.value)}
                  placeholder="#1D4ED8"
                  className="font-mono text-xs"
                />
              </div>
            </div>
          </div>

          <Button onClick={handleCustomColorChange} className="w-full">
            <Save className="w-4 h-4 mr-2" />
            Apply Custom Colors
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}