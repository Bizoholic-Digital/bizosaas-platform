'use client';

import React, { useState } from 'react';
import { useFormContext } from 'react-hook-form';
import { 
  Palette, Layout, Search, Share2, Eye, Edit, 
  Plus, Trash2, ExternalLink, Smartphone, Monitor
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Textarea } from '../../ui/textarea';
import { Badge } from '../../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select-new';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';

import { StoreSetupData } from '../types';
import { THEMES } from '../constants';

interface CustomizationStepProps {
  data: StoreSetupData['customization'];
  onChange: (data: Partial<StoreSetupData['customization']>) => void;
  readonly?: boolean;
}

interface NavigationItem {
  label: string;
  url: string;
  children?: Array<{ label: string; url: string; }>;
}

const HOMEPAGE_LAYOUTS = [
  { id: 'grid', name: 'Product Grid', description: 'Classic grid layout with featured products' },
  { id: 'hero', name: 'Hero Banner', description: 'Large banner with call-to-action' },
  { id: 'categories', name: 'Category Focus', description: 'Highlight product categories' },
  { id: 'minimal', name: 'Minimal', description: 'Clean and simple design' },
  { id: 'magazine', name: 'Magazine', description: 'Editorial-style layout' }
];

export function CustomizationStep({ data, onChange, readonly = false }: CustomizationStepProps) {
  const { register, formState: { errors } } = useFormContext();
  const [selectedTheme, setSelectedTheme] = useState(data.theme);
  const [previewDevice, setPreviewDevice] = useState<'desktop' | 'mobile'>('desktop');
  const [newNavItem, setNewNavItem] = useState<Partial<NavigationItem>>({});
  const [newFooterLink, setNewFooterLink] = useState({ label: '', url: '' });
  const [newKeyword, setNewKeyword] = useState('');

  // Select theme
  const selectTheme = (themeId: string) => {
    setSelectedTheme(themeId);
    onChange({ ...data, theme: themeId });
  };

  // Update homepage layout
  const updateHomepageLayout = (layout: string) => {
    onChange({
      ...data,
      layout: { ...data.layout, homepage: layout }
    });
  };

  // Add navigation item
  const addNavigationItem = () => {
    if (newNavItem.label && newNavItem.url) {
      const navigation = [...data.layout.navigation, newNavItem as NavigationItem];
      onChange({
        ...data,
        layout: { ...data.layout, navigation }
      });
      setNewNavItem({});
    }
  };

  // Remove navigation item
  const removeNavigationItem = (index: number) => {
    const navigation = data.layout.navigation.filter((_, i) => i !== index);
    onChange({
      ...data,
      layout: { ...data.layout, navigation }
    });
  };

  // Add footer link
  const addFooterLink = () => {
    if (newFooterLink.label && newFooterLink.url) {
      const links = [...data.layout.footer.links, newFooterLink];
      onChange({
        ...data,
        layout: {
          ...data.layout,
          footer: { ...data.layout.footer, links }
        }
      });
      setNewFooterLink({ label: '', url: '' });
    }
  };

  // Remove footer link
  const removeFooterLink = (index: number) => {
    const links = data.layout.footer.links.filter((_, i) => i !== index);
    onChange({
      ...data,
      layout: {
        ...data.layout,
        footer: { ...data.layout.footer, links }
      }
    });
  };

  // Add SEO keyword
  const addKeyword = () => {
    if (newKeyword && !data.seo.keywords.includes(newKeyword)) {
      const keywords = [...data.seo.keywords, newKeyword];
      onChange({
        ...data,
        seo: { ...data.seo, keywords }
      });
      setNewKeyword('');
    }
  };

  // Remove SEO keyword
  const removeKeyword = (keyword: string) => {
    const keywords = data.seo.keywords.filter(k => k !== keyword);
    onChange({
      ...data,
      seo: { ...data.seo, keywords }
    });
  };

  // Update social media link
  const updateSocialMedia = (platform: keyof StoreSetupData['customization']['socialMedia'], url: string) => {
    onChange({
      ...data,
      socialMedia: { ...data.socialMedia, [platform]: url }
    });
  };

  // Get selected theme details
  const getSelectedTheme = () => THEMES.find(t => t.id === selectedTheme);

  return (
    <div className="space-y-6">
      <Tabs defaultValue="theme" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="theme">Theme Selection</TabsTrigger>
          <TabsTrigger value="layout">Layout & Navigation</TabsTrigger>
          <TabsTrigger value="seo">SEO Settings</TabsTrigger>
          <TabsTrigger value="social">Social Media</TabsTrigger>
        </TabsList>

        {/* Theme Selection Tab */}
        <TabsContent value="theme" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Palette className="h-5 w-5" />
                <span>Choose Your Theme</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {THEMES.map((theme) => (
                  <div
                    key={theme.id}
                    className={`border-2 rounded-lg overflow-hidden cursor-pointer transition-all ${
                      selectedTheme === theme.id
                        ? 'border-blue-500 shadow-lg'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => !readonly && selectTheme(theme.id)}
                  >
                    <div className="relative">
                      <img
                        src={theme.preview}
                        alt={theme.name}
                        className="w-full h-48 object-cover"
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = '/themes/default-preview.jpg';
                        }}
                      />
                      {selectedTheme === theme.id && (
                        <div className="absolute top-2 right-2">
                          <Badge variant="default">Selected</Badge>
                        </div>
                      )}
                      <div className="absolute top-2 left-2">
                        <Badge variant="outline" className="bg-white">
                          {theme.category}
                        </Badge>
                      </div>
                    </div>

                    <div className="p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-medium text-gray-900">{theme.name}</h4>
                        {theme.price > 0 ? (
                          <Badge variant="secondary">₹{theme.price}</Badge>
                        ) : (
                          <Badge variant="default">Free</Badge>
                        )}
                      </div>

                      <p className="text-sm text-gray-600 mb-3">{theme.description}</p>

                      <div className="space-y-2">
                        <div className="flex flex-wrap gap-1">
                          {theme.features.slice(0, 3).map((feature) => (
                            <Badge key={feature} variant="outline" className="text-xs">
                              {feature}
                            </Badge>
                          ))}
                          {theme.features.length > 3 && (
                            <Badge variant="outline" className="text-xs">
                              +{theme.features.length - 3}
                            </Badge>
                          )}
                        </div>

                        <div className="flex items-center space-x-3 text-xs text-gray-500">
                          {theme.responsive && (
                            <div className="flex items-center space-x-1">
                              <Smartphone className="h-3 w-3" />
                              <span>Responsive</span>
                            </div>
                          )}
                          {theme.customizable.colors && (
                            <div className="flex items-center space-x-1">
                              <Palette className="h-3 w-3" />
                              <span>Customizable</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Theme Customization */}
          {selectedTheme && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>Theme Customization</span>
                  <div className="flex items-center space-x-2">
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => setPreviewDevice(previewDevice === 'desktop' ? 'mobile' : 'desktop')}
                    >
                      {previewDevice === 'desktop' ? (
                        <Smartphone className="h-4 w-4" />
                      ) : (
                        <Monitor className="h-4 w-4" />
                      )}
                    </Button>
                    <Button type="button" variant="outline" size="sm">
                      <Eye className="h-4 w-4 mr-2" />
                      Preview
                    </Button>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium mb-3">Current Theme: {getSelectedTheme()?.name}</h4>
                    <p className="text-sm text-gray-600 mb-4">{getSelectedTheme()?.description}</p>
                    
                    <div className="space-y-4">
                      <div>
                        <Label>Homepage Layout</Label>
                        <Select
                          value={data.layout.homepage}
                          onValueChange={updateHomepageLayout}
                          disabled={readonly}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select layout" />
                          </SelectTrigger>
                          <SelectContent>
                            {HOMEPAGE_LAYOUTS.map((layout) => (
                              <SelectItem key={layout.id} value={layout.id}>
                                {layout.name} - {layout.description}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      {getSelectedTheme()?.customizable.colors && (
                        <div>
                          <Label>Brand Colors</Label>
                          <p className="text-sm text-gray-600">
                            Colors are inherited from your store branding settings.
                          </p>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="bg-gray-100 rounded-lg p-4">
                    <div className="text-center text-gray-500">
                      <div className="border-2 border-dashed border-gray-300 rounded h-48 flex items-center justify-center">
                        <div>
                          <Eye className="h-8 w-8 mx-auto mb-2" />
                          <p>Theme Preview</p>
                          <p className="text-xs">{previewDevice} view</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Layout & Navigation Tab */}
        <TabsContent value="layout" className="space-y-6">
          {/* Navigation Menu */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Layout className="h-5 w-5" />
                <span>Navigation Menu</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                {data.layout.navigation.length === 0 ? (
                  <p className="text-gray-500 text-center py-4">
                    No navigation items added yet
                  </p>
                ) : (
                  data.layout.navigation.map((item, index) => (
                    <div key={index} className="flex items-center justify-between bg-gray-50 p-3 rounded">
                      <div>
                        <span className="font-medium">{item.label}</span>
                        <span className="text-gray-600 ml-2 text-sm">{item.url}</span>
                      </div>
                      {!readonly && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => removeNavigationItem(index)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  ))
                )}
              </div>

              {!readonly && (
                <div className="border-t pt-4">
                  <h5 className="font-medium mb-3">Add Navigation Item</h5>
                  <div className="flex space-x-2">
                    <Input
                      placeholder="Menu label"
                      value={newNavItem.label || ''}
                      onChange={(e) => setNewNavItem({ ...newNavItem, label: e.target.value })}
                    />
                    <Input
                      placeholder="URL"
                      value={newNavItem.url || ''}
                      onChange={(e) => setNewNavItem({ ...newNavItem, url: e.target.value })}
                    />
                    <Button
                      type="button"
                      onClick={addNavigationItem}
                      disabled={!newNavItem.label || !newNavItem.url}
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Footer Configuration */}
          <Card>
            <CardHeader>
              <CardTitle>Footer Configuration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="copyright">Copyright Text</Label>
                <Input
                  id="copyright"
                  placeholder="© 2024 Your Store Name. All rights reserved."
                  value={data.layout.footer.copyright}
                  onChange={(e) => onChange({
                    ...data,
                    layout: {
                      ...data.layout,
                      footer: { ...data.layout.footer, copyright: e.target.value }
                    }
                  })}
                  disabled={readonly}
                />
              </div>

              <div>
                <Label>Footer Links</Label>
                <div className="space-y-2 mt-2">
                  {data.layout.footer.links.map((link, index) => (
                    <div key={index} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                      <div>
                        <span className="font-medium">{link.label}</span>
                        <span className="text-gray-600 ml-2 text-sm">{link.url}</span>
                      </div>
                      {!readonly && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => removeFooterLink(index)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  ))}
                </div>

                {!readonly && (
                  <div className="flex space-x-2 mt-3">
                    <Input
                      placeholder="Link label"
                      value={newFooterLink.label}
                      onChange={(e) => setNewFooterLink({ ...newFooterLink, label: e.target.value })}
                    />
                    <Input
                      placeholder="URL"
                      value={newFooterLink.url}
                      onChange={(e) => setNewFooterLink({ ...newFooterLink, url: e.target.value })}
                    />
                    <Button
                      type="button"
                      onClick={addFooterLink}
                      disabled={!newFooterLink.label || !newFooterLink.url}
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* SEO Settings Tab */}
        <TabsContent value="seo" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Search className="h-5 w-5" />
                <span>SEO Configuration</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="seoTitle">SEO Title *</Label>
                <Input
                  id="seoTitle"
                  placeholder="Best Online Store for Your Products"
                  value={data.seo.title}
                  onChange={(e) => onChange({
                    ...data,
                    seo: { ...data.seo, title: e.target.value }
                  })}
                  disabled={readonly}
                  maxLength={60}
                  className={errors.customization?.seo?.title ? 'border-red-500' : ''}
                />
                <p className="text-xs text-gray-500 mt-1">
                  {data.seo.title.length}/60 characters (optimal: 50-60)
                </p>
              </div>

              <div>
                <Label htmlFor="seoDescription">Meta Description *</Label>
                <Textarea
                  id="seoDescription"
                  placeholder="Discover amazing products at great prices. Shop now for the best deals on quality items with fast shipping and excellent customer service."
                  value={data.seo.description}
                  onChange={(e) => onChange({
                    ...data,
                    seo: { ...data.seo, description: e.target.value }
                  })}
                  disabled={readonly}
                  maxLength={160}
                  rows={3}
                  className={errors.customization?.seo?.description ? 'border-red-500' : ''}
                />
                <p className="text-xs text-gray-500 mt-1">
                  {data.seo.description.length}/160 characters (optimal: 150-160)
                </p>
              </div>

              <div>
                <Label>SEO Keywords</Label>
                <div className="flex flex-wrap gap-2 mt-2 mb-3">
                  {data.seo.keywords.map((keyword) => (
                    <Badge
                      key={keyword}
                      variant="secondary"
                      className="flex items-center space-x-1"
                    >
                      <span>{keyword}</span>
                      {!readonly && (
                        <button
                          type="button"
                          onClick={() => removeKeyword(keyword)}
                          className="ml-1 hover:text-red-600"
                        >
                          <Trash2 className="h-3 w-3" />
                        </button>
                      )}
                    </Badge>
                  ))}
                </div>

                {!readonly && (
                  <div className="flex space-x-2">
                    <Input
                      placeholder="Add keyword"
                      value={newKeyword}
                      onChange={(e) => setNewKeyword(e.target.value)}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          addKeyword();
                        }
                      }}
                    />
                    <Button
                      type="button"
                      onClick={addKeyword}
                      disabled={!newKeyword || data.seo.keywords.length >= 10}
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                )}

                <p className="text-xs text-gray-500 mt-1">
                  {data.seo.keywords.length}/10 keywords (recommended: 5-8 relevant keywords)
                </p>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg">
                <h5 className="font-medium text-blue-900 mb-2">SEO Preview</h5>
                <div className="space-y-1">
                  <div className="text-blue-600 text-lg font-medium">
                    {data.seo.title || 'Your Store Title'}
                  </div>
                  <div className="text-green-600 text-sm">
                    yourstore.coreldove.com
                  </div>
                  <div className="text-gray-600 text-sm">
                    {data.seo.description || 'Your store description will appear here in search results.'}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Social Media Tab */}
        <TabsContent value="social" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Share2 className="h-5 w-5" />
                <span>Social Media Integration</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-600">
                Connect your social media accounts to display them on your store and enable social sharing.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="facebook">Facebook Page URL</Label>
                  <Input
                    id="facebook"
                    type="url"
                    placeholder="https://facebook.com/yourpage"
                    value={data.socialMedia.facebook || ''}
                    onChange={(e) => updateSocialMedia('facebook', e.target.value)}
                    disabled={readonly}
                  />
                </div>

                <div>
                  <Label htmlFor="instagram">Instagram Profile URL</Label>
                  <Input
                    id="instagram"
                    type="url"
                    placeholder="https://instagram.com/yourprofile"
                    value={data.socialMedia.instagram || ''}
                    onChange={(e) => updateSocialMedia('instagram', e.target.value)}
                    disabled={readonly}
                  />
                </div>

                <div>
                  <Label htmlFor="twitter">Twitter Profile URL</Label>
                  <Input
                    id="twitter"
                    type="url"
                    placeholder="https://twitter.com/yourprofile"
                    value={data.socialMedia.twitter || ''}
                    onChange={(e) => updateSocialMedia('twitter', e.target.value)}
                    disabled={readonly}
                  />
                </div>

                <div>
                  <Label htmlFor="youtube">YouTube Channel URL</Label>
                  <Input
                    id="youtube"
                    type="url"
                    placeholder="https://youtube.com/yourchannel"
                    value={data.socialMedia.youtube || ''}
                    onChange={(e) => updateSocialMedia('youtube', e.target.value)}
                    disabled={readonly}
                  />
                </div>
              </div>

              <div className="bg-green-50 p-4 rounded-lg">
                <h5 className="font-medium text-green-900 mb-2">Social Media Benefits</h5>
                <ul className="text-sm text-green-800 space-y-1">
                  <li>• Increase brand visibility and customer engagement</li>
                  <li>• Enable social sharing of products</li>
                  <li>• Build trust through social proof</li>
                  <li>• Drive traffic from social platforms</li>
                </ul>
              </div>

              {/* Social Media Preview */}
              <div className="border rounded-lg p-4">
                <h5 className="font-medium mb-3">Social Media Links Preview</h5>
                <div className="flex space-x-4">
                  {Object.entries(data.socialMedia).map(([platform, url]) => (
                    url && (
                      <a
                        key={platform}
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center space-x-2 text-blue-600 hover:text-blue-800"
                      >
                        <ExternalLink className="h-4 w-4" />
                        <span className="capitalize">{platform}</span>
                      </a>
                    )
                  ))}
                  {Object.values(data.socialMedia).every(url => !url) && (
                    <p className="text-gray-500 text-sm">No social media links added yet</p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}