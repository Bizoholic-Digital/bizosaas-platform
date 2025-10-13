'use client'

import React, { useState, useEffect, useContext, createContext, ReactNode } from 'react'
import { ThemeManager, ThemePreset, themePresets, darkThemePresets } from '@/lib/theme-system'

interface ThemeContextType {
  currentTheme: ThemePreset
  isDarkMode: boolean
  availableThemes: ThemePreset[]
  applyTheme: (theme: ThemePreset, darkMode?: boolean) => void
  toggleDarkMode: () => void
  resetToDefault: () => void
  isLoading: boolean
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [themeManager] = useState(() => ThemeManager.getInstance())
  const [currentTheme, setCurrentTheme] = useState<ThemePreset>(themePresets[0])
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  // Initialize theme on component mount
  useEffect(() => {
    const initTheme = () => {
      const theme = themeManager.getCurrentTheme()
      const darkMode = themeManager.getDarkMode()
      
      setCurrentTheme(theme)
      setIsDarkMode(darkMode)
      
      // Apply theme immediately
      themeManager.applyTheme(theme, darkMode)
      setIsLoading(false)
    }

    initTheme()
  }, [themeManager])

  const applyTheme = (theme: ThemePreset, darkMode?: boolean) => {
    const newDarkMode = darkMode !== undefined ? darkMode : isDarkMode
    
    themeManager.applyTheme(theme, newDarkMode)
    setCurrentTheme(theme)
    setIsDarkMode(newDarkMode)
  }

  const toggleDarkMode = () => {
    const newDarkMode = !isDarkMode
    themeManager.applyTheme(currentTheme, newDarkMode)
    setIsDarkMode(newDarkMode)
  }

  const resetToDefault = () => {
    const defaultTheme = themePresets[0]
    themeManager.applyTheme(defaultTheme, false)
    setCurrentTheme(defaultTheme)
    setIsDarkMode(false)
  }

  const value: ThemeContextType = {
    currentTheme,
    isDarkMode,
    availableThemes: [...themePresets, ...darkThemePresets],
    applyTheme,
    toggleDarkMode,
    resetToDefault,
    isLoading
  }

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

// Hook for theme customization in settings
export function useThemeCustomization() {
  const { currentTheme, applyTheme, availableThemes } = useTheme()
  const [customColors, setCustomColors] = useState<Record<string, string>>({})

  // Initialize custom colors from current theme
  useEffect(() => {
    const colors: Record<string, string> = {}
    Object.entries(currentTheme.colors).forEach(([key, value]) => {
      colors[key] = value
    })
    setCustomColors(colors)
  }, [currentTheme])

  const updateCustomColor = (colorKey: string, hslValue: string) => {
    const newColors = { ...customColors, [colorKey]: hslValue }
    setCustomColors(newColors)
    
    // Create and apply custom theme
    const customTheme: ThemePreset = {
      name: 'custom-live',
      displayName: 'Custom (Live Preview)',
      description: 'Live preview of custom theme',
      colors: {
        primary: newColors.primary || currentTheme.colors.primary,
        primaryForeground: newColors.primaryForeground || currentTheme.colors.primaryForeground,
        secondary: newColors.secondary || currentTheme.colors.secondary,
        background: newColors.background || currentTheme.colors.background,
        foreground: newColors.foreground || currentTheme.colors.foreground,
        accent: newColors.accent || currentTheme.colors.accent,
        muted: newColors.muted || currentTheme.colors.muted,
        border: newColors.border || currentTheme.colors.border,
        ring: newColors.ring || currentTheme.colors.ring
      }
    }
    
    applyTheme(customTheme)
  }

  const saveCustomTheme = (name: string) => {
    const customTheme: ThemePreset = {
      name: `custom-${name.toLowerCase().replace(/\s+/g, '-')}`,
      displayName: `Custom: ${name}`,
      description: 'User-created custom theme',
      colors: {
        primary: customColors.primary || currentTheme.colors.primary,
        primaryForeground: customColors.primaryForeground || currentTheme.colors.primaryForeground,
        secondary: customColors.secondary || currentTheme.colors.secondary,
        background: customColors.background || currentTheme.colors.background,
        foreground: customColors.foreground || currentTheme.colors.foreground,
        accent: customColors.accent || currentTheme.colors.accent,
        muted: customColors.muted || currentTheme.colors.muted,
        border: customColors.border || currentTheme.colors.border,
        ring: customColors.ring || currentTheme.colors.ring
      }
    }

    // Save to localStorage
    const savedThemes = JSON.parse(localStorage.getItem('bizosaas-custom-themes') || '[]')
    savedThemes.push(customTheme)
    localStorage.setItem('bizosaas-custom-themes', JSON.stringify(savedThemes))
    
    applyTheme(customTheme)
    return customTheme
  }

  const getCustomThemes = (): ThemePreset[] => {
    if (typeof window === 'undefined') return []
    return JSON.parse(localStorage.getItem('bizosaas-custom-themes') || '[]')
  }

  return {
    currentTheme,
    customColors,
    availableThemes,
    updateCustomColor,
    saveCustomTheme,
    getCustomThemes,
    applyTheme
  }
}