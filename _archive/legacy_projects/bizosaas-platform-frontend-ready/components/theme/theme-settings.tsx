'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Switch } from '@/components/ui/switch'
import { 
  Palette, 
  Save, 
  RotateCcw, 
  Eye, 
  Paintbrush,
  Download,
  Upload,
  Trash2,
  Check,
  Moon,
  Sun
} from 'lucide-react'
import { useTheme, useThemeCustomization } from '@/hooks/use-theme'
import { themePresets, hslToHex, hexToHsl } from '@/lib/theme-system'

interface ColorPickerProps {
  label: string
  value: string
  onChange: (value: string) => void
  description?: string
}

function ColorPicker({ label, value, onChange, description }: ColorPickerProps) {
  const [hexValue, setHexValue] = useState(hslToHex(value))

  const handleHexChange = (hex: string) => {
    setHexValue(hex)
    const hsl = hexToHsl(hex)
    onChange(hsl)
  }

  return (
    <div className="space-y-2">
      <Label className="text-sm font-medium">{label}</Label>
      {description && <p className="text-xs text-muted-foreground">{description}</p>}
      <div className="flex items-center space-x-2">
        <div 
          className="w-8 h-8 rounded-md border border-border"
          style={{ backgroundColor: hexValue }}
        />
        <Input
          type="color"
          value={hexValue}
          onChange={(e) => handleHexChange(e.target.value)}
          className="w-16 h-8 p-0 border-0"
        />
        <Input
          value={hexValue}
          onChange={(e) => handleHexChange(e.target.value)}
          placeholder="#000000"
          className="font-mono text-xs"
        />
      </div>
      <div className="text-xs text-muted-foreground font-mono">
        HSL: {value}
      </div>
    </div>
  )
}

function ThemePreview({ themeName, colors }: { themeName: string, colors: any }) {
  return (
    <div className={`theme-preview-${themeName} p-4 rounded-lg border space-y-3`} style={{
      '--primary': colors.primary,
      '--secondary': colors.secondary,
      '--background': colors.background,
      '--foreground': colors.foreground,
      '--muted': colors.muted,
      '--border': colors.border,
    } as any}>
      <div className="bg-background text-foreground p-2 rounded">
        <div className="text-sm font-medium">Theme Preview</div>
        <div className="text-xs text-muted-foreground">Sample content</div>
      </div>
      <div className="flex space-x-2">
        <div className="bg-primary text-primary-foreground px-2 py-1 rounded text-xs">
          Primary
        </div>
        <div className="bg-secondary text-secondary-foreground px-2 py-1 rounded text-xs">
          Secondary
        </div>
        <div className="bg-muted text-muted-foreground px-2 py-1 rounded text-xs">
          Muted
        </div>
      </div>
    </div>
  )
}

export function ThemeSettings() {
  const { currentTheme, isDarkMode, toggleDarkMode, resetToDefault, applyTheme } = useTheme()
  const { 
    customColors, 
    updateCustomColor, 
    saveCustomTheme, 
    getCustomThemes,
    availableThemes 
  } = useThemeCustomization()
  
  const [customThemeName, setCustomThemeName] = useState('')
  const [activeTab, setActiveTab] = useState('presets')
  const [previewMode, setPreviewMode] = useState(false)

  const handlePresetSelect = (preset: any) => {
    applyTheme(preset, isDarkMode)
  }

  const handleSaveCustomTheme = () => {
    if (!customThemeName.trim()) return
    
    const saved = saveCustomTheme(customThemeName)
    setCustomThemeName('')
    // Show success message or toast here
  }

  const exportTheme = () => {
    const themeData = {
      theme: currentTheme,
      isDarkMode,
      customColors,
      exportedAt: new Date().toISOString()
    }
    
    const blob = new Blob([JSON.stringify(themeData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `bizosaas-theme-${currentTheme.name}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const importTheme = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const themeData = JSON.parse(e.target?.result as string)
        if (themeData.theme && themeData.theme.colors) {
          applyTheme(themeData.theme, themeData.isDarkMode || false)
        }
      } catch (error) {
        console.error('Failed to import theme:', error)
      }
    }
    reader.readAsText(file)
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
          <Button variant="outline" size="sm" onClick={toggleDarkMode}>
            {isDarkMode ? <Sun className="w-4 h-4 mr-2" /> : <Moon className="w-4 h-4 mr-2" />}
            {isDarkMode ? 'Light' : 'Dark'} Mode
          </Button>
          <Button variant="outline" size="sm" onClick={exportTheme}>
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
          <Button variant="outline" size="sm" asChild>
            <label className="cursor-pointer">
              <Upload className="w-4 h-4 mr-2" />
              Import
              <input
                type="file"
                accept=".json"
                onChange={importTheme}
                className="hidden"
              />
            </label>
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
              <h3 className="font-medium">{currentTheme.displayName}</h3>
              <p className="text-sm text-muted-foreground">{currentTheme.description}</p>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant={isDarkMode ? 'default' : 'secondary'}>
                {isDarkMode ? 'Dark Mode' : 'Light Mode'}
              </Badge>
            </div>
          </div>
          
          <ThemePreview themeName={currentTheme.name} colors={currentTheme.colors} />
        </CardContent>
      </Card>

      {/* Theme Customization Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="presets">Theme Presets</TabsTrigger>
          <TabsTrigger value="customize">Custom Colors</TabsTrigger>
          <TabsTrigger value="saved">Saved Themes</TabsTrigger>
        </TabsList>

        {/* Preset Themes Tab */}
        <TabsContent value="presets" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Preset Themes</CardTitle>
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
                        variant={currentTheme.name === preset.name ? "default" : "outline"}
                        onClick={() => handlePresetSelect(preset)}
                      >
                        {currentTheme.name === preset.name ? <Check className="w-3 h-3" /> : "Apply"}
                      </Button>
                    </div>
                    <p className="text-xs text-muted-foreground">{preset.description}</p>
                    <ThemePreview themeName={preset.name} colors={preset.colors} />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Custom Colors Tab */}
        <TabsContent value="customize" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Paintbrush className="w-5 h-5" />
                Custom Color Palette
              </CardTitle>
              <CardDescription>
                Fine-tune colors to match your brand exactly
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <ColorPicker
                  label="Primary Color"
                  value={customColors.primary || currentTheme.colors.primary}
                  onChange={(value) => updateCustomColor('primary', value)}
                  description="Main brand color for buttons and highlights"
                />
                <ColorPicker
                  label="Secondary Color"
                  value={customColors.secondary || currentTheme.colors.secondary}
                  onChange={(value) => updateCustomColor('secondary', value)}
                  description="Secondary elements and backgrounds"
                />
                <ColorPicker
                  label="Accent Color"
                  value={customColors.accent || currentTheme.colors.accent}
                  onChange={(value) => updateCustomColor('accent', value)}
                  description="Accent elements and hover states"
                />
                <ColorPicker
                  label="Border Color"
                  value={customColors.border || currentTheme.colors.border}
                  onChange={(value) => updateCustomColor('border', value)}
                  description="Borders and dividers"
                />
                <ColorPicker
                  label="Muted Color"
                  value={customColors.muted || currentTheme.colors.muted}
                  onChange={(value) => updateCustomColor('muted', value)}
                  description="Subtle backgrounds and disabled states"
                />
                <ColorPicker
                  label="Ring Color"
                  value={customColors.ring || currentTheme.colors.ring}
                  onChange={(value) => updateCustomColor('ring', value)}
                  description="Focus rings and outlines"
                />
              </div>

              <div className="pt-4 border-t">
                <div className="flex items-center space-x-2">
                  <Input
                    placeholder="Theme name (e.g., My Brand Colors)"
                    value={customThemeName}
                    onChange={(e) => setCustomThemeName(e.target.value)}
                    className="flex-1"
                  />
                  <Button onClick={handleSaveCustomTheme} disabled={!customThemeName.trim()}>
                    <Save className="w-4 h-4 mr-2" />
                    Save Theme
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Saved Themes Tab */}
        <TabsContent value="saved" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Saved Custom Themes</CardTitle>
              <CardDescription>
                Your personally created theme variations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {getCustomThemes().map((theme, index) => (
                  <div key={`${theme.name}-${index}`} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium text-sm">{theme.displayName}</h4>
                      <div className="flex items-center space-x-1">
                        <Button
                          size="sm"
                          variant={currentTheme.name === theme.name ? "default" : "outline"}
                          onClick={() => handlePresetSelect(theme)}
                        >
                          {currentTheme.name === theme.name ? <Check className="w-3 h-3" /> : "Apply"}
                        </Button>
                        <Button size="sm" variant="outline">
                          <Trash2 className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                    <ThemePreview themeName={theme.name} colors={theme.colors} />
                  </div>
                ))}
                {getCustomThemes().length === 0 && (
                  <div className="col-span-full text-center py-8 text-muted-foreground">
                    <Palette className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>No saved themes yet</p>
                    <p className="text-sm">Create custom themes in the "Custom Colors" tab</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}