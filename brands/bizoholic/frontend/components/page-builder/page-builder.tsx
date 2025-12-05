'use client'

import { useState } from 'react'
import { Editor, Frame, Element } from '@craftjs/core'
// import { Layers } from '@craftjs/layers' // Package not installed
import { 
  Palette, 
  Eye, 
  Code, 
  Settings, 
  Save, 
  Undo, 
  Redo,
  Smartphone,
  Tablet,
  Monitor,
  Plus,
  Layout,
  Type,
  Image as ImageIcon,
  Square,
  Play
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import { 
  Container,
  Text,
  Button as CraftButton,
  Hero,
  Card as CraftCard
} from './components'
// import { Toolbox } from './toolbox' // File not found
// import { SettingsPanel } from './settings-panel' // File not found
import { cn } from '@/lib/utils'

const components = {
  Container,
  Text,
  Button: CraftButton,
  Hero,
  Card: CraftCard
}

type ViewportType = 'desktop' | 'tablet' | 'mobile'

export function PageBuilder() {
  const [viewport, setViewport] = useState<ViewportType>('desktop')
  const [isPreview, setIsPreview] = useState(false)
  const [activeTool, setActiveTool] = useState<string>('design')

  const getViewportClasses = () => {
    switch (viewport) {
      case 'mobile':
        return 'w-[375px] h-[812px]'
      case 'tablet':
        return 'w-[768px] h-[1024px]'
      default:
        return 'w-full h-full'
    }
  }

  const getViewportIcon = (type: ViewportType) => {
    switch (type) {
      case 'mobile': return Smartphone
      case 'tablet': return Tablet
      default: return Monitor
    }
  }

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="border-b bg-background px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Palette className="h-5 w-5 text-primary" />
              <h1 className="font-semibold">Page Builder</h1>
              <Badge variant="secondary">AI-Powered</Badge>
            </div>
            
            <Separator orientation="vertical" className="h-6" />
            
            {/* Tool Tabs */}
            <Tabs value={activeTool} onValueChange={setActiveTool}>
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="design">Design</TabsTrigger>
                <TabsTrigger value="layers">Layers</TabsTrigger>
                <TabsTrigger value="settings">Settings</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
          
          <div className="flex items-center space-x-2">
            {/* Viewport Controls */}
            <div className="flex items-center space-x-1 mr-4">
              {(['desktop', 'tablet', 'mobile'] as ViewportType[]).map((type) => {
                const Icon = getViewportIcon(type)
                return (
                  <Button
                    key={type}
                    variant={viewport === type ? 'secondary' : 'ghost'}
                    size="sm"
                    onClick={() => setViewport(type)}
                  >
                    <Icon className="h-4 w-4" />
                  </Button>
                )
              })}
            </div>
            
            <Separator orientation="vertical" className="h-6" />
            
            {/* Action Buttons */}
            <Button variant="ghost" size="sm">
              <Undo className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm">
              <Redo className="h-4 w-4" />
            </Button>
            
            <Separator orientation="vertical" className="h-6" />
            
            <Button
              variant={isPreview ? 'secondary' : 'ghost'}
              size="sm"
              onClick={() => setIsPreview(!isPreview)}
            >
              {isPreview ? <Code className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              {isPreview ? 'Edit' : 'Preview'}
            </Button>
            
            <Button size="sm">
              <Save className="h-4 w-4 mr-2" />
              Save
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        <Editor resolver={components}>
          {/* Left Sidebar */}
          {!isPreview && (
            <div className="w-80 border-r bg-muted/30 flex flex-col">
              <Tabs value={activeTool} onValueChange={setActiveTool} className="flex-1">
                <TabsContent value="design" className="flex-1 p-4">
                  <div className="space-y-4">
                    <h3 className="font-medium flex items-center">
                      <Palette className="h-4 w-4 mr-2" />
                      Components
                    </h3>
                    <div className="text-sm text-muted-foreground p-4">
                      Component toolbox unavailable - Toolbox component not found
                    </div>
                  </div>
                </TabsContent>
                
                <TabsContent value="layers" className="flex-1 p-4">
                  <div className="space-y-4">
                    <h3 className="font-medium flex items-center">
                      <Layout className="h-4 w-4 mr-2" />
                      Layers
                    </h3>
                    {/* <Layers expandRootOnLoad={true} /> */}
                    <div className="text-sm text-muted-foreground p-4">
                      Layers panel unavailable - @craftjs/layers not installed
                    </div>
                  </div>
                </TabsContent>
                
                <TabsContent value="settings" className="flex-1 p-4">
                  <div className="space-y-4">
                    <h3 className="font-medium flex items-center">
                      <Settings className="h-4 w-4 mr-2" />
                      Settings
                    </h3>
                    <div className="text-sm text-muted-foreground p-4">
                      Settings panel unavailable - SettingsPanel component not found
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          )}

          {/* Canvas Area */}
          <div className="flex-1 flex flex-col overflow-hidden">
            <div className="flex-1 flex items-center justify-center bg-gray-100 p-4">
              <div 
                className={cn(
                  'bg-white shadow-lg transition-all duration-300 overflow-auto',
                  getViewportClasses(),
                  viewport !== 'desktop' && 'rounded-lg border'
                )}
              >
                <Frame>
                  <Element
                    is={Container}
                    padding={["40", "40", "40", "40"]}
                    background={{r: 255, g: 255, b: 255, a: 1}}
                    canvas
                  >
                    <Element
                      is={Hero}
                      title="Welcome to Your Landing Page"
                      subtitle="Create stunning pages with our AI-powered drag & drop builder"
                      backgroundImage="https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80"
                    />
                    
                    <Element
                      is={Container}
                      padding={["60", "20", "60", "20"]}
                      canvas
                    >
                      <Element
                        is={Text}
                        text="Key Features"
                        fontSize={32}
                        fontWeight={700}
                        textAlign="center"
                        margin={["0", "0", "40", "0"]}
                      />
                      
                      <Element
                        is={Container}
                        className="grid grid-cols-3 gap-6"
                        canvas
                      >
                        <Element
                          is={CraftCard}
                          title="AI-Powered"
                          description="Intelligent suggestions and optimizations"
                          icon="🤖"
                        />
                        <Element
                          is={CraftCard}
                          title="Drag & Drop"
                          description="Build pages without coding"
                          icon="🎨"
                        />
                        <Element
                          is={CraftCard}
                          title="Multi-tenant"
                          description="Separate client workspaces"
                          icon="🏢"
                        />
                      </Element>
                    </Element>
                    
                    <Element
                      is={Container}
                      padding={["40", "20", "40", "20"]}
                      background={{r: 248, g: 250, b: 252, a: 1}}
                      canvas
                    >
                      <Element
                        is={Text}
                        text="Ready to get started?"
                        fontSize={24}
                        fontWeight={600}
                        textAlign="center"
                        margin={["0", "0", "20", "0"]}
                      />
                      
                      <Element
                        is={CraftButton}
                        text="Get Started Now"
                        size="lg"
                        variant="default"
                        margin={["0", "auto", "0", "auto"]}
                        display="block"
                        width="fit-content"
                      />
                    </Element>
                  </Element>
                </Frame>
              </div>
            </div>
            
            {/* Bottom Status Bar */}
            <div className="border-t bg-background px-4 py-2 flex items-center justify-between text-sm text-muted-foreground">
              <div className="flex items-center space-x-4">
                <span>Elements: 8</span>
                <span>Viewport: {viewport}</span>
                <span className="flex items-center">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2" />
                  Auto-save enabled
                </span>
              </div>
              
              <div className="flex items-center space-x-2">
                <Button variant="ghost" size="sm">
                  <Play className="h-3 w-3 mr-1" />
                  Test
                </Button>
                <Button variant="ghost" size="sm">
                  Export Code
                </Button>
              </div>
            </div>
          </div>
        </Editor>
      </div>
    </div>
  )
}