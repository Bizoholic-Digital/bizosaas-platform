'use client';

import React, { useState, useRef } from 'react';
import { useFormContext } from 'react-hook-form';
import { 
  Package, Upload, Plus, Trash2, Edit, Image as ImageIcon, 
  Download, FileSpreadsheet, Database, ShoppingCart 
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
import { BUSINESS_TEMPLATES } from '../constants';

interface ProductCatalogStepProps {
  data: StoreSetupData['productCatalog'];
  onChange: (data: Partial<StoreSetupData['productCatalog']>) => void;
  readonly?: boolean;
}

interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  price: number;
  images: File[];
  inventory: number;
  sku: string;
}

export function ProductCatalogStep({ data, onChange, readonly = false }: ProductCatalogStepProps) {
  const { register, formState: { errors } } = useFormContext();
  const [selectedTemplate, setSelectedTemplate] = useState<string>('');
  const [newProduct, setNewProduct] = useState<Partial<Product>>({});
  const [editingProduct, setEditingProduct] = useState<string | null>(null);
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Add category
  const addCategory = (category: string) => {
    if (category && !data.categories.includes(category)) {
      onChange({
        ...data,
        categories: [...data.categories, category]
      });
    }
  };

  // Remove category
  const removeCategory = (category: string) => {
    onChange({
      ...data,
      categories: data.categories.filter(c => c !== category)
    });
  };

  // Apply business template
  const applyTemplate = (templateId: string) => {
    const template = BUSINESS_TEMPLATES.find(t => t.id === templateId);
    if (template) {
      onChange({
        ...data,
        categories: template.categories,
        products: template.sampleProducts.map((product, index) => ({
          id: `template-${index}`,
          ...product,
          description: `Sample ${product.name.toLowerCase()} for your ${template.name.toLowerCase()} store`,
          images: [],
          inventory: 10,
          sku: `SKU-${product.name.replace(/\s+/g, '-').toUpperCase()}-001`
        }))
      });
      setSelectedTemplate(templateId);
    }
  };

  // Add product
  const addProduct = () => {
    if (newProduct.name && newProduct.category && newProduct.price) {
      const product: Product = {
        id: `product-${Date.now()}`,
        name: newProduct.name,
        description: newProduct.description || '',
        category: newProduct.category,
        price: newProduct.price,
        images: newProduct.images || [],
        inventory: newProduct.inventory || 0,
        sku: newProduct.sku || `SKU-${newProduct.name.replace(/\s+/g, '-').toUpperCase()}-${Date.now()}`
      };

      onChange({
        ...data,
        products: [...data.products, product]
      });

      setNewProduct({});
    }
  };

  // Remove product
  const removeProduct = (productId: string) => {
    onChange({
      ...data,
      products: data.products.filter(p => p.id !== productId)
    });
  };

  // Handle CSV upload
  const handleCsvUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'text/csv') {
      setCsvFile(file);
      // Here you would typically parse the CSV and convert to products
      // For now, we'll just show the file is selected
      onChange({ ...data, importMethod: 'csv' });
    }
  };

  // Handle product image upload
  const handleProductImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    setNewProduct({ ...newProduct, images: files });
  };

  // Download CSV template
  const downloadCsvTemplate = () => {
    const csvContent = [
      ['Product Name', 'Description', 'Category', 'Price', 'Inventory', 'SKU'],
      ['Example Product', 'This is a sample product description', 'Category 1', '999', '50', 'SKU-EXAMPLE-001'],
      ['Another Product', 'Another sample product', 'Category 2', '1599', '25', 'SKU-ANOTHER-002']
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'product-template.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Import Method Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Database className="h-5 w-5" />
            <span>Product Import Method</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                data.importMethod === 'manual' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => !readonly && onChange({ ...data, importMethod: 'manual' })}
            >
              <Plus className="h-8 w-8 text-blue-600 mb-2" />
              <h4 className="font-medium">Manual Entry</h4>
              <p className="text-sm text-gray-600">Add products one by one</p>
            </div>

            <div
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                data.importMethod === 'csv' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => !readonly && onChange({ ...data, importMethod: 'csv' })}
            >
              <FileSpreadsheet className="h-8 w-8 text-green-600 mb-2" />
              <h4 className="font-medium">CSV Upload</h4>
              <p className="text-sm text-gray-600">Bulk import from CSV</p>
            </div>

            <div
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                data.importMethod === 'excel' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => !readonly && onChange({ ...data, importMethod: 'excel' })}
            >
              <FileSpreadsheet className="h-8 w-8 text-orange-600 mb-2" />
              <h4 className="font-medium">Excel Upload</h4>
              <p className="text-sm text-gray-600">Import from Excel file</p>
            </div>

            <div
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                data.importMethod === 'api' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => !readonly && onChange({ ...data, importMethod: 'api' })}
            >
              <Database className="h-8 w-8 text-purple-600 mb-2" />
              <h4 className="font-medium">API Integration</h4>
              <p className="text-sm text-gray-600">Connect existing catalog</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Business Template Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <ShoppingCart className="h-5 w-5" />
            <span>Quick Start Templates</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {BUSINESS_TEMPLATES.map((template) => (
              <div
                key={template.id}
                className={`p-4 border rounded-lg cursor-pointer transition-all ${
                  selectedTemplate === template.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => !readonly && applyTemplate(template.id)}
              >
                <h4 className="font-medium text-gray-900 mb-2">{template.name}</h4>
                <p className="text-sm text-gray-600 mb-3">{template.description}</p>
                <div className="flex flex-wrap gap-1">
                  {template.categories.slice(0, 3).map((category) => (
                    <Badge key={category} variant="outline" className="text-xs">
                      {category}
                    </Badge>
                  ))}
                  {template.categories.length > 3 && (
                    <Badge variant="outline" className="text-xs">
                      +{template.categories.length - 3}
                    </Badge>
                  )}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Product Categories */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Package className="h-5 w-5" />
            <span>Product Categories</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex space-x-2">
              <Input
                placeholder="Add new category"
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    addCategory((e.target as HTMLInputElement).value);
                    (e.target as HTMLInputElement).value = '';
                  }
                }}
                disabled={readonly}
              />
              <Button
                type="button"
                variant="outline"
                onClick={() => {
                  const input = document.querySelector('input[placeholder="Add new category"]') as HTMLInputElement;
                  if (input?.value) {
                    addCategory(input.value);
                    input.value = '';
                  }
                }}
                disabled={readonly}
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>

            <div className="flex flex-wrap gap-2">
              {data.categories.map((category) => (
                <Badge
                  key={category}
                  variant="secondary"
                  className="flex items-center space-x-1"
                >
                  <span>{category}</span>
                  {!readonly && (
                    <button
                      type="button"
                      onClick={() => removeCategory(category)}
                      className="ml-1 hover:text-red-600"
                    >
                      <Trash2 className="h-3 w-3" />
                    </button>
                  )}
                </Badge>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Product Management */}
      <Card>
        <CardHeader>
          <CardTitle>Product Catalog</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="add" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="add">Add Products</TabsTrigger>
              <TabsTrigger value="list">Product List ({data.products.length})</TabsTrigger>
              <TabsTrigger value="bulk">Bulk Import</TabsTrigger>
            </TabsList>

            {/* Add Products Tab */}
            <TabsContent value="add" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="productName">Product Name *</Label>
                  <Input
                    id="productName"
                    placeholder="Enter product name"
                    value={newProduct.name || ''}
                    onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
                    disabled={readonly}
                  />
                </div>

                <div>
                  <Label htmlFor="productCategory">Category *</Label>
                  <Select
                    value={newProduct.category}
                    onValueChange={(value) => setNewProduct({ ...newProduct, category: value })}
                    disabled={readonly}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      {data.categories.map((category) => (
                        <SelectItem key={category} value={category}>
                          {category}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label htmlFor="productDescription">Description</Label>
                <Textarea
                  id="productDescription"
                  placeholder="Describe your product..."
                  value={newProduct.description || ''}
                  onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
                  disabled={readonly}
                  rows={3}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="productPrice">Price (₹) *</Label>
                  <Input
                    id="productPrice"
                    type="number"
                    placeholder="0.00"
                    value={newProduct.price || ''}
                    onChange={(e) => setNewProduct({ ...newProduct, price: parseFloat(e.target.value) })}
                    disabled={readonly}
                  />
                </div>

                <div>
                  <Label htmlFor="productInventory">Inventory</Label>
                  <Input
                    id="productInventory"
                    type="number"
                    placeholder="0"
                    value={newProduct.inventory || ''}
                    onChange={(e) => setNewProduct({ ...newProduct, inventory: parseInt(e.target.value) })}
                    disabled={readonly}
                  />
                </div>

                <div>
                  <Label htmlFor="productSku">SKU</Label>
                  <Input
                    id="productSku"
                    placeholder="Auto-generated"
                    value={newProduct.sku || ''}
                    onChange={(e) => setNewProduct({ ...newProduct, sku: e.target.value })}
                    disabled={readonly}
                  />
                </div>
              </div>

              <div>
                <Label>Product Images</Label>
                <div className="mt-2 border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <ImageIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-600 mb-2">
                    Drag and drop images here, or click to select
                  </p>
                  <input
                    type="file"
                    multiple
                    accept="image/*"
                    onChange={handleProductImageUpload}
                    className="hidden"
                    id="productImages"
                    disabled={readonly}
                  />
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => document.getElementById('productImages')?.click()}
                    disabled={readonly}
                  >
                    Choose Images
                  </Button>
                </div>
                
                {newProduct.images && newProduct.images.length > 0 && (
                  <div className="mt-4 grid grid-cols-4 gap-2">
                    {newProduct.images.map((image, index) => (
                      <div key={index} className="relative">
                        <img
                          src={URL.createObjectURL(image)}
                          alt={`Product ${index + 1}`}
                          className="w-full h-20 object-cover rounded border"
                        />
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <Button
                type="button"
                onClick={addProduct}
                disabled={readonly || !newProduct.name || !newProduct.category || !newProduct.price}
                className="w-full"
              >
                <Plus className="h-4 w-4 mr-2" />
                Add Product
              </Button>
            </TabsContent>

            {/* Product List Tab */}
            <TabsContent value="list" className="space-y-4">
              {data.products.length === 0 ? (
                <div className="text-center py-8">
                  <Package className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No products added yet</h3>
                  <p className="text-gray-600">Start by adding your first product or using a template.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {data.products.map((product) => (
                    <div key={product.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-medium text-gray-900 truncate">{product.name}</h4>
                        {!readonly && (
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            onClick={() => removeProduct(product.id)}
                          >
                            <Trash2 className="h-3 w-3" />
                          </Button>
                        )}
                      </div>
                      
                      <p className="text-sm text-gray-600 mb-2 line-clamp-2">{product.description}</p>
                      
                      <div className="space-y-1">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Price:</span>
                          <span className="font-medium">₹{product.price}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Category:</span>
                          <Badge variant="outline" className="text-xs">{product.category}</Badge>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Stock:</span>
                          <span className={product.inventory > 0 ? 'text-green-600' : 'text-red-600'}>
                            {product.inventory}
                          </span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">SKU:</span>
                          <span className="text-xs font-mono">{product.sku}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </TabsContent>

            {/* Bulk Import Tab */}
            <TabsContent value="bulk" className="space-y-4">
              <div className="text-center">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Bulk Product Import</h3>
                <p className="text-gray-600 mb-4">
                  Upload a CSV or Excel file to import multiple products at once
                </p>

                <div className="flex justify-center space-x-4 mb-6">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={downloadCsvTemplate}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download CSV Template
                  </Button>
                </div>

                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8">
                  <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-lg font-medium text-gray-900 mb-2">
                    Drag and drop your file here
                  </p>
                  <p className="text-gray-600 mb-4">or click to select a file</p>
                  
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv,.xlsx,.xls"
                    onChange={handleCsvUpload}
                    className="hidden"
                    disabled={readonly}
                  />
                  
                  <Button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={readonly}
                  >
                    Select File
                  </Button>

                  {csvFile && (
                    <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded">
                      <p className="text-green-800">
                        File selected: {csvFile.name}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Pricing Strategy & Inventory */}
      <Card>
        <CardHeader>
          <CardTitle>Pricing & Inventory Settings</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label>Pricing Strategy</Label>
              <Select
                value={data.pricingStrategy}
                onValueChange={(value: 'fixed' | 'dynamic' | 'tiered') => 
                  onChange({ ...data, pricingStrategy: value })
                }
                disabled={readonly}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="fixed">Fixed Pricing</SelectItem>
                  <SelectItem value="dynamic">Dynamic Pricing</SelectItem>
                  <SelectItem value="tiered">Tiered Pricing</SelectItem>
                </SelectContent>
              </Select>
              <p className="text-xs text-gray-500 mt-1">
                Fixed: Set prices, Dynamic: Based on demand, Tiered: Volume discounts
              </p>
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="inventoryTracking"
                checked={data.inventoryTracking}
                onChange={(e) => onChange({ ...data, inventoryTracking: e.target.checked })}
                disabled={readonly}
                className="h-4 w-4 rounded border-gray-300"
              />
              <Label htmlFor="inventoryTracking">Enable Inventory Tracking</Label>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}