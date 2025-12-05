'use client';

import React, { useState } from 'react';
import { useFormContext } from 'react-hook-form';
import { Upload, Building2, Mail, Phone, MapPin, Palette, FileText } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Textarea } from '../../ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { Checkbox } from '../../ui/checkbox';
import { Badge } from '../../ui/badge';

import { StoreSetupData } from '../types';
import { BUSINESS_TYPES, CURRENCIES, INDIAN_STATES } from '../constants';

interface StoreInfoStepProps {
  data: StoreSetupData['storeInfo'];
  onChange: (data: Partial<StoreSetupData['storeInfo']>) => void;
  readonly?: boolean;
}

export function StoreInfoStep({ data, onChange, readonly = false }: StoreInfoStepProps) {
  const { register, formState: { errors }, setValue, watch } = useFormContext();
  const [selectedLogo, setSelectedLogo] = useState<File | null>(null);
  const [logoPreview, setLogoPreview] = useState<string>('');

  // Handle logo upload
  const handleLogoUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedLogo(file);
      const reader = new FileReader();
      reader.onload = () => {
        setLogoPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      onChange({ ...data, logo: file });
    }
  };

  // Handle color change
  const handleColorChange = (color: string) => {
    onChange({ ...data, brandColor: color });
    setValue('storeInfo.brandColor', color);
  };

  // Predefined brand colors
  const brandColors = [
    '#3B82F6', '#EF4444', '#10B981', '#F59E0B',
    '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16',
    '#F97316', '#6366F1', '#14B8A6', '#F43F5E'
  ];

  return (
    <div className="space-y-6">
      {/* Basic Store Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Building2 className="h-5 w-5" />
            <span>Basic Store Information</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="storeName">Store Name *</Label>
              <Input
                id="storeName"
                placeholder="Enter your store name"
                value={data.name}
                onChange={(e) => onChange({ ...data, name: e.target.value })}
                disabled={readonly}
                className={errors.storeInfo?.name ? 'border-red-500' : ''}
                {...register('storeInfo.name')}
              />
              {errors.storeInfo?.name && (
                <p className="text-sm text-red-500 mt-1">{errors.storeInfo.name.message}</p>
              )}
            </div>

            <div>
              <Label htmlFor="businessType">Business Type *</Label>
              <Select
                value={data.businessType}
                onValueChange={(value) => onChange({ ...data, businessType: value })}
                disabled={readonly}
              >
                <SelectTrigger className={errors.storeInfo?.businessType ? 'border-red-500' : ''}>
                  <SelectValue placeholder="Select business type" />
                </SelectTrigger>
                <SelectContent>
                  {BUSINESS_TYPES.map((type) => (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.storeInfo?.businessType && (
                <p className="text-sm text-red-500 mt-1">{errors.storeInfo.businessType.message}</p>
              )}
            </div>
          </div>

          <div>
            <Label htmlFor="storeDescription">Store Description *</Label>
            <Textarea
              id="storeDescription"
              placeholder="Describe your store and what you sell..."
              value={data.description}
              onChange={(e) => onChange({ ...data, description: e.target.value })}
              disabled={readonly}
              rows={3}
              className={errors.storeInfo?.description ? 'border-red-500' : ''}
              {...register('storeInfo.description')}
            />
            {errors.storeInfo?.description && (
              <p className="text-sm text-red-500 mt-1">{errors.storeInfo.description.message}</p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Branding */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Palette className="h-5 w-5" />
            <span>Branding</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Logo Upload */}
            <div>
              <Label>Store Logo</Label>
              <div className="mt-2">
                {logoPreview ? (
                  <div className="relative">
                    <img
                      src={logoPreview}
                      alt="Logo preview"
                      className="w-32 h-32 object-contain border rounded-lg"
                    />
                    {!readonly && (
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        className="mt-2"
                        onClick={() => {
                          setLogoPreview('');
                          setSelectedLogo(null);
                          onChange({ ...data, logo: undefined });
                        }}
                      >
                        Remove Logo
                      </Button>
                    )}
                  </div>
                ) : (
                  <div
                    className={`border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors ${
                      readonly ? 'cursor-not-allowed' : 'cursor-pointer'
                    }`}
                    onClick={() => !readonly && document.getElementById('logoUpload')?.click()}
                  >
                    <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-600">
                      Click to upload logo<br />
                      <span className="text-xs text-gray-500">PNG, JPG up to 2MB</span>
                    </p>
                  </div>
                )}
                
                <input
                  id="logoUpload"
                  type="file"
                  accept="image/*"
                  onChange={handleLogoUpload}
                  className="hidden"
                  disabled={readonly}
                />
              </div>
            </div>

            {/* Brand Color */}
            <div>
              <Label>Brand Color</Label>
              <div className="mt-2 space-y-3">
                <div className="flex items-center space-x-2">
                  <div
                    className="w-8 h-8 rounded border shadow-sm"
                    style={{ backgroundColor: data.brandColor }}
                  />
                  <Input
                    type="color"
                    value={data.brandColor}
                    onChange={(e) => handleColorChange(e.target.value)}
                    disabled={readonly}
                    className="w-16 h-8 p-1 border rounded"
                  />
                  <span className="text-sm text-gray-600">{data.brandColor}</span>
                </div>
                
                {/* Predefined Colors */}
                <div className="grid grid-cols-6 gap-2">
                  {brandColors.map((color) => (
                    <button
                      key={color}
                      type="button"
                      className={`w-8 h-8 rounded border-2 ${
                        data.brandColor === color ? 'border-gray-400' : 'border-gray-200'
                      } hover:border-gray-400 transition-colors`}
                      style={{ backgroundColor: color }}
                      onClick={() => !readonly && handleColorChange(color)}
                      disabled={readonly}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Contact Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Mail className="h-5 w-5" />
            <span>Contact Information</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="email">Email Address *</Label>
              <Input
                id="email"
                type="email"
                placeholder="store@example.com"
                value={data.contactInfo.email}
                onChange={(e) => onChange({
                  ...data,
                  contactInfo: { ...data.contactInfo, email: e.target.value }
                })}
                disabled={readonly}
                className={errors.storeInfo?.contactInfo?.email ? 'border-red-500' : ''}
                {...register('storeInfo.contactInfo.email')}
              />
              {errors.storeInfo?.contactInfo?.email && (
                <p className="text-sm text-red-500 mt-1">{errors.storeInfo.contactInfo.email.message}</p>
              )}
            </div>

            <div>
              <Label htmlFor="phone">Phone Number *</Label>
              <Input
                id="phone"
                type="tel"
                placeholder="+91 98765 43210"
                value={data.contactInfo.phone}
                onChange={(e) => onChange({
                  ...data,
                  contactInfo: { ...data.contactInfo, phone: e.target.value }
                })}
                disabled={readonly}
                className={errors.storeInfo?.contactInfo?.phone ? 'border-red-500' : ''}
                {...register('storeInfo.contactInfo.phone')}
              />
              {errors.storeInfo?.contactInfo?.phone && (
                <p className="text-sm text-red-500 mt-1">{errors.storeInfo.contactInfo.phone.message}</p>
              )}
            </div>
          </div>

          {/* Address */}
          <div>
            <Label htmlFor="street">Business Address *</Label>
            <Input
              id="street"
              placeholder="Street Address"
              value={data.contactInfo.address.street}
              onChange={(e) => onChange({
                ...data,
                contactInfo: {
                  ...data.contactInfo,
                  address: { ...data.contactInfo.address, street: e.target.value }
                }
              })}
              disabled={readonly}
              className={errors.storeInfo?.contactInfo?.address?.street ? 'border-red-500' : ''}
              {...register('storeInfo.contactInfo.address.street')}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <Label htmlFor="city">City *</Label>
              <Input
                id="city"
                placeholder="City"
                value={data.contactInfo.address.city}
                onChange={(e) => onChange({
                  ...data,
                  contactInfo: {
                    ...data.contactInfo,
                    address: { ...data.contactInfo.address, city: e.target.value }
                  }
                })}
                disabled={readonly}
                {...register('storeInfo.contactInfo.address.city')}
              />
            </div>

            <div>
              <Label htmlFor="state">State *</Label>
              <Select
                value={data.contactInfo.address.state}
                onValueChange={(value) => onChange({
                  ...data,
                  contactInfo: {
                    ...data.contactInfo,
                    address: { ...data.contactInfo.address, state: value }
                  }
                })}
                disabled={readonly}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select state" />
                </SelectTrigger>
                <SelectContent>
                  {INDIAN_STATES.map((state) => (
                    <SelectItem key={state} value={state}>
                      {state}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="pincode">Pincode *</Label>
              <Input
                id="pincode"
                placeholder="123456"
                value={data.contactInfo.address.pincode}
                onChange={(e) => onChange({
                  ...data,
                  contactInfo: {
                    ...data.contactInfo,
                    address: { ...data.contactInfo.address, pincode: e.target.value }
                  }
                })}
                disabled={readonly}
                {...register('storeInfo.contactInfo.address.pincode')}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Currency & Business Registration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <FileText className="h-5 w-5" />
            <span>Business Registration & Currency</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label>Primary Currency</Label>
              <Select
                value={data.currency.primary}
                onValueChange={(value) => onChange({
                  ...data,
                  currency: { ...data.currency, primary: value }
                })}
                disabled={readonly}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {CURRENCIES.map((currency) => (
                    <SelectItem key={currency.code} value={currency.code}>
                      {currency.symbol} {currency.name} ({currency.code})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label>Supported Currencies</Label>
              <div className="flex flex-wrap gap-2 mt-2">
                {CURRENCIES.map((currency) => (
                  <Badge
                    key={currency.code}
                    variant={data.currency.supported.includes(currency.code) ? 'default' : 'outline'}
                    className="cursor-pointer"
                    onClick={() => {
                      if (readonly) return;
                      const supported = data.currency.supported.includes(currency.code)
                        ? data.currency.supported.filter(c => c !== currency.code)
                        : [...data.currency.supported, currency.code];
                      onChange({
                        ...data,
                        currency: { ...data.currency, supported }
                      });
                    }}
                  >
                    {currency.code}
                  </Badge>
                ))}
              </div>
            </div>
          </div>

          {/* Business Registration */}
          <div className="space-y-4 pt-4 border-t">
            <h4 className="font-medium text-gray-900">Business Registration (Optional)</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="gst">GST Number</Label>
                <Input
                  id="gst"
                  placeholder="22AAAAA0000A1Z5"
                  value={data.businessRegistration.gst || ''}
                  onChange={(e) => onChange({
                    ...data,
                    businessRegistration: { ...data.businessRegistration, gst: e.target.value }
                  })}
                  disabled={readonly}
                  {...register('storeInfo.businessRegistration.gst')}
                />
                <p className="text-xs text-gray-500 mt-1">
                  Required for Indian businesses selling above ₹40 lakhs annually
                </p>
              </div>

              <div>
                <Label htmlFor="pan">PAN Number</Label>
                <Input
                  id="pan"
                  placeholder="ABCDE1234F"
                  value={data.businessRegistration.pan || ''}
                  onChange={(e) => onChange({
                    ...data,
                    businessRegistration: { ...data.businessRegistration, pan: e.target.value }
                  })}
                  disabled={readonly}
                  {...register('storeInfo.businessRegistration.pan')}
                />
              </div>
            </div>

            <div>
              <Label htmlFor="registrationNumber">Business Registration Number</Label>
              <Input
                id="registrationNumber"
                placeholder="Enter your business registration number"
                value={data.businessRegistration.registrationNumber || ''}
                onChange={(e) => onChange({
                  ...data,
                  businessRegistration: { ...data.businessRegistration, registrationNumber: e.target.value }
                })}
                disabled={readonly}
                {...register('storeInfo.businessRegistration.registrationNumber')}
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}