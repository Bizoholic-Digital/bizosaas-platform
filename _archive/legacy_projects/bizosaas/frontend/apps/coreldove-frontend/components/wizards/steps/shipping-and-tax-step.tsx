'use client';

import React, { useState } from 'react';
import { useFormContext } from 'react-hook-form';
import { 
  Truck, MapPin, Calculator, Globe, Plus, Trash2, 
  Clock, IndianRupee, Percent, Building2, Package 
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Badge } from '../../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select-new';
import { Checkbox } from '../../ui/checkbox';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';

import { StoreSetupData } from '../types';
import { SHIPPING_ZONES, DELIVERY_PARTNERS, INDIAN_STATES } from '../constants';

interface ShippingAndTaxStepProps {
  data: StoreSetupData['shippingAndTax'];
  onChange: (data: Partial<StoreSetupData['shippingAndTax']>) => void;
  readonly?: boolean;
}

interface NewShippingZone {
  name: string;
  type: 'domestic' | 'international';
  countries: string[];
  states: string[];
  methods: Array<{
    name: string;
    description: string;
    calculation: 'flat' | 'weight' | 'zone';
    rate: number;
    freeThreshold?: number;
    estimatedDays: string;
  }>;
}

const COUNTRIES = [
  'United States', 'Canada', 'United Kingdom', 'Australia', 
  'Germany', 'France', 'Japan', 'Singapore', 'UAE', 'Saudi Arabia'
];

export function ShippingAndTaxStep({ data, onChange, readonly = false }: ShippingAndTaxStepProps) {
  const { register, formState: { errors } } = useFormContext();
  const [newZone, setNewZone] = useState<Partial<NewShippingZone>>({
    type: 'domestic',
    countries: [],
    states: [],
    methods: []
  });
  const [newMethod, setNewMethod] = useState({
    name: '',
    description: '',
    calculation: 'flat' as 'flat' | 'weight' | 'zone',
    rate: 0,
    freeThreshold: 0,
    estimatedDays: ''
  });

  // Apply predefined shipping zones
  const applyPredefinedZones = () => {
    onChange({
      ...data,
      shippingZones: [
        ...data.shippingZones,
        ...SHIPPING_ZONES.map(zone => ({
          name: zone.name,
          countries: zone.coverage.countries || ['India'],
          states: zone.coverage.states || [],
          rates: zone.methods.map(method => ({
            method: method.name,
            cost: method.rate,
            freeThreshold: method.freeThreshold
          }))
        }))
      ]
    });
  };

  // Add shipping zone
  const addShippingZone = () => {
    if (newZone.name && newZone.methods && newZone.methods.length > 0) {
      const zone = {
        name: newZone.name,
        countries: newZone.type === 'domestic' ? ['India'] : newZone.countries || [],
        states: newZone.type === 'domestic' ? newZone.states || [] : [],
        rates: newZone.methods.map(method => ({
          method: method.name,
          cost: method.rate,
          freeThreshold: method.freeThreshold
        }))
      };

      onChange({
        ...data,
        shippingZones: [...data.shippingZones, zone]
      });

      setNewZone({ type: 'domestic', countries: [], states: [], methods: [] });
    }
  };

  // Remove shipping zone
  const removeShippingZone = (index: number) => {
    onChange({
      ...data,
      shippingZones: data.shippingZones.filter((_, i) => i !== index)
    });
  };

  // Add shipping method to new zone
  const addMethodToNewZone = () => {
    if (newMethod.name && newMethod.rate > 0) {
      setNewZone({
        ...newZone,
        methods: [...(newZone.methods || []), { ...newMethod }]
      });
      setNewMethod({
        name: '',
        description: '',
        calculation: 'flat',
        rate: 0,
        freeThreshold: 0,
        estimatedDays: ''
      });
    }
  };

  // Toggle delivery partner
  const toggleDeliveryPartner = (partnerId: string) => {
    const partners = data.deliveryPartners.includes(partnerId)
      ? data.deliveryPartners.filter(id => id !== partnerId)
      : [...data.deliveryPartners, partnerId];

    onChange({ ...data, deliveryPartners: partners });
  };

  // Update GST rates
  const updateGSTRate = (type: 'cgst' | 'sgst' | 'igst', rate: number) => {
    onChange({
      ...data,
      taxConfiguration: {
        ...data.taxConfiguration,
        gst: {
          ...data.taxConfiguration.gst,
          [type]: rate
        }
      }
    });
  };

  // Add international tax rate
  const addInternationalTax = (country: string, rate: number) => {
    if (country && rate >= 0) {
      const international = data.taxConfiguration.international.filter(tax => tax.country !== country);
      international.push({ country, rate });

      onChange({
        ...data,
        taxConfiguration: {
          ...data.taxConfiguration,
          international
        }
      });
    }
  };

  // Remove international tax rate
  const removeInternationalTax = (country: string) => {
    onChange({
      ...data,
      taxConfiguration: {
        ...data.taxConfiguration,
        international: data.taxConfiguration.international.filter(tax => tax.country !== country)
      }
    });
  };

  // Calculate shipping cost for demo
  const calculateShippingCost = (weight: number, zone: string) => {
    const shippingZone = data.shippingZones.find(z => z.name === zone);
    if (shippingZone && shippingZone.rates.length > 0) {
      return shippingZone.rates[0].cost;
    }
    return 0;
  };

  return (
    <div className="space-y-6">
      {/* Quick Setup */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Truck className="h-5 w-5" />
            <span>Quick Shipping Setup</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center">
            <p className="text-gray-600 mb-4">
              Get started quickly with our predefined shipping zones for Indian businesses.
            </p>
            <Button
              type="button"
              variant="outline"
              onClick={applyPredefinedZones}
              disabled={readonly || data.shippingZones.length > 0}
            >
              <MapPin className="h-4 w-4 mr-2" />
              Apply Standard Indian Shipping Zones
            </Button>
            {data.shippingZones.length > 0 && (
              <p className="text-sm text-green-600 mt-2">
                ✓ Shipping zones configured. You can customize them below.
              </p>
            )}
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="zones" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="zones">Shipping Zones</TabsTrigger>
          <TabsTrigger value="partners">Delivery Partners</TabsTrigger>
          <TabsTrigger value="tax">Tax Configuration</TabsTrigger>
        </TabsList>

        {/* Shipping Zones Tab */}
        <TabsContent value="zones" className="space-y-6">
          {/* Existing Shipping Zones */}
          <Card>
            <CardHeader>
              <CardTitle>Configured Shipping Zones ({data.shippingZones.length})</CardTitle>
            </CardHeader>
            <CardContent>
              {data.shippingZones.length === 0 ? (
                <div className="text-center py-8">
                  <MapPin className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No shipping zones configured</h3>
                  <p className="text-gray-600">Add shipping zones to start calculating delivery costs.</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {data.shippingZones.map((zone, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h4 className="font-medium text-gray-900">{zone.name}</h4>
                          <p className="text-sm text-gray-600">
                            {zone.countries.length > 0 && `Countries: ${zone.countries.join(', ')}`}
                            {zone.states && zone.states.length > 0 && ` | States: ${zone.states.slice(0, 3).join(', ')}${zone.states.length > 3 ? '...' : ''}`}
                          </p>
                        </div>
                        {!readonly && (
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            onClick={() => removeShippingZone(index)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        )}
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {zone.rates.map((rate, rateIndex) => (
                          <div key={rateIndex} className="bg-gray-50 p-3 rounded">
                            <h5 className="font-medium text-sm">{rate.method}</h5>
                            <p className="text-sm text-gray-600">₹{rate.cost}</p>
                            {rate.freeThreshold && (
                              <p className="text-xs text-green-600">
                                Free above ₹{rate.freeThreshold}
                              </p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Add New Shipping Zone */}
          {!readonly && (
            <Card>
              <CardHeader>
                <CardTitle>Add New Shipping Zone</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="zoneName">Zone Name</Label>
                    <Input
                      id="zoneName"
                      placeholder="e.g., Metro Cities"
                      value={newZone.name || ''}
                      onChange={(e) => setNewZone({ ...newZone, name: e.target.value })}
                    />
                  </div>

                  <div>
                    <Label>Zone Type</Label>
                    <Select
                      value={newZone.type}
                      onValueChange={(value: 'domestic' | 'international') => 
                        setNewZone({ ...newZone, type: value })
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="domestic">Domestic (India)</SelectItem>
                        <SelectItem value="international">International</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {newZone.type === 'domestic' ? (
                  <div>
                    <Label>Select States</Label>
                    <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 mt-2 max-h-48 overflow-y-auto border rounded p-2">
                      {INDIAN_STATES.map((state) => (
                        <div key={state} className="flex items-center space-x-2">
                          <Checkbox
                            id={`state-${state}`}
                            checked={newZone.states?.includes(state)}
                            onCheckedChange={(checked) => {
                              const states = checked
                                ? [...(newZone.states || []), state]
                                : (newZone.states || []).filter(s => s !== state);
                              setNewZone({ ...newZone, states });
                            }}
                          />
                          <Label htmlFor={`state-${state}`} className="text-sm">
                            {state}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div>
                    <Label>Select Countries</Label>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mt-2">
                      {COUNTRIES.map((country) => (
                        <div key={country} className="flex items-center space-x-2">
                          <Checkbox
                            id={`country-${country}`}
                            checked={newZone.countries?.includes(country)}
                            onCheckedChange={(checked) => {
                              const countries = checked
                                ? [...(newZone.countries || []), country]
                                : (newZone.countries || []).filter(c => c !== country);
                              setNewZone({ ...newZone, countries });
                            }}
                          />
                          <Label htmlFor={`country-${country}`} className="text-sm">
                            {country}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Shipping Methods */}
                <div className="border-t pt-4">
                  <h4 className="font-medium mb-3">Shipping Methods</h4>
                  
                  <div className="grid grid-cols-1 md:grid-cols-5 gap-2 mb-3">
                    <Input
                      placeholder="Method name"
                      value={newMethod.name}
                      onChange={(e) => setNewMethod({ ...newMethod, name: e.target.value })}
                    />
                    <Input
                      placeholder="Description"
                      value={newMethod.description}
                      onChange={(e) => setNewMethod({ ...newMethod, description: e.target.value })}
                    />
                    <Input
                      type="number"
                      placeholder="Cost (₹)"
                      value={newMethod.rate || ''}
                      onChange={(e) => setNewMethod({ ...newMethod, rate: parseFloat(e.target.value) || 0 })}
                    />
                    <Input
                      type="number"
                      placeholder="Free above (₹)"
                      value={newMethod.freeThreshold || ''}
                      onChange={(e) => setNewMethod({ ...newMethod, freeThreshold: parseFloat(e.target.value) || 0 })}
                    />
                    <Button
                      type="button"
                      size="sm"
                      onClick={addMethodToNewZone}
                      disabled={!newMethod.name || !newMethod.rate}
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>

                  <div className="space-y-2">
                    {newZone.methods?.map((method, index) => (
                      <div key={index} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                        <div>
                          <span className="font-medium">{method.name}</span>
                          <span className="text-gray-600 ml-2">₹{method.rate}</span>
                          {method.freeThreshold && (
                            <span className="text-green-600 ml-2 text-sm">
                              Free above ₹{method.freeThreshold}
                            </span>
                          )}
                        </div>
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => {
                            const methods = newZone.methods?.filter((_, i) => i !== index) || [];
                            setNewZone({ ...newZone, methods });
                          }}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>

                <Button
                  type="button"
                  onClick={addShippingZone}
                  disabled={!newZone.name || !newZone.methods?.length}
                  className="w-full"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Shipping Zone
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Delivery Partners Tab */}
        <TabsContent value="partners" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Package className="h-5 w-5" />
                <span>Delivery Partners</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-4">
                Select delivery partners to integrate with your store for automated shipping.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {DELIVERY_PARTNERS.map((partner) => (
                  <div
                    key={partner.id}
                    className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                      data.deliveryPartners.includes(partner.id)
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => !readonly && toggleDeliveryPartner(partner.id)}
                  >
                    <div className="flex items-center space-x-3">
                      <img
                        src={partner.icon}
                        alt={partner.name}
                        className="w-10 h-10 object-contain"
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = '/icons/delivery-default.svg';
                        }}
                      />
                      <div>
                        <h4 className="font-medium text-gray-900">{partner.name}</h4>
                        {data.deliveryPartners.includes(partner.id) && (
                          <Badge variant="default" className="text-xs mt-1">Selected</Badge>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {data.deliveryPartners.length > 0 && (
                <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                  <h4 className="font-medium text-green-900 mb-2">Selected Partners</h4>
                  <div className="flex flex-wrap gap-2">
                    {data.deliveryPartners.map((partnerId) => {
                      const partner = DELIVERY_PARTNERS.find(p => p.id === partnerId);
                      return (
                        <Badge key={partnerId} variant="outline">
                          {partner?.name}
                        </Badge>
                      );
                    })}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tax Configuration Tab */}
        <TabsContent value="tax" className="space-y-6">
          {/* GST Configuration */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Calculator className="h-5 w-5" />
                <span>GST Configuration (India)</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-600">
                Configure GST rates for your products. Standard rates are pre-filled but can be customized.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="cgst">CGST Rate (%)</Label>
                  <div className="flex items-center space-x-2">
                    <Percent className="h-4 w-4 text-gray-400" />
                    <Input
                      id="cgst"
                      type="number"
                      step="0.25"
                      min="0"
                      max="28"
                      value={data.taxConfiguration.gst.cgst}
                      onChange={(e) => updateGSTRate('cgst', parseFloat(e.target.value) || 0)}
                      disabled={readonly}
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="sgst">SGST Rate (%)</Label>
                  <div className="flex items-center space-x-2">
                    <Percent className="h-4 w-4 text-gray-400" />
                    <Input
                      id="sgst"
                      type="number"
                      step="0.25"
                      min="0"
                      max="28"
                      value={data.taxConfiguration.gst.sgst}
                      onChange={(e) => updateGSTRate('sgst', parseFloat(e.target.value) || 0)}
                      disabled={readonly}
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="igst">IGST Rate (%)</Label>
                  <div className="flex items-center space-x-2">
                    <Percent className="h-4 w-4 text-gray-400" />
                    <Input
                      id="igst"
                      type="number"
                      step="0.25"
                      min="0"
                      max="28"
                      value={data.taxConfiguration.gst.igst}
                      onChange={(e) => updateGSTRate('igst', parseFloat(e.target.value) || 0)}
                      disabled={readonly}
                    />
                  </div>
                </div>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg">
                <h5 className="font-medium text-blue-900 mb-2">GST Calculation Example</h5>
                <p className="text-sm text-blue-800">
                  For a ₹1000 product with {data.taxConfiguration.gst.cgst + data.taxConfiguration.gst.sgst}% total GST:
                </p>
                <div className="mt-2 space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span>Product Price:</span>
                    <span>₹1,000.00</span>
                  </div>
                  <div className="flex justify-between">
                    <span>CGST ({data.taxConfiguration.gst.cgst}%):</span>
                    <span>₹{(1000 * data.taxConfiguration.gst.cgst / 100).toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>SGST ({data.taxConfiguration.gst.sgst}%):</span>
                    <span>₹{(1000 * data.taxConfiguration.gst.sgst / 100).toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between font-medium border-t pt-1">
                    <span>Total (incl. GST):</span>
                    <span>₹{(1000 + (1000 * (data.taxConfiguration.gst.cgst + data.taxConfiguration.gst.sgst) / 100)).toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* International Tax Configuration */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Globe className="h-5 w-5" />
                <span>International Tax Rates</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-600">
                Configure tax rates for international customers. These will be applied based on shipping address.
              </p>

              {!readonly && (
                <div className="flex space-x-2">
                  <Select
                    onValueChange={(country) => {
                      const rateInput = document.getElementById('intlTaxRate') as HTMLInputElement;
                      const rate = parseFloat(rateInput?.value || '0');
                      if (country && rate >= 0) {
                        addInternationalTax(country, rate);
                        rateInput.value = '';
                      }
                    }}
                  >
                    <SelectTrigger className="flex-1">
                      <SelectValue placeholder="Select country" />
                    </SelectTrigger>
                    <SelectContent>
                      {COUNTRIES.map((country) => (
                        <SelectItem key={country} value={country}>
                          {country}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Input
                    id="intlTaxRate"
                    type="number"
                    placeholder="Tax rate %"
                    className="w-32"
                  />
                  <Button
                    type="button"
                    onClick={() => {
                      // This will be handled by the Select onValueChange
                    }}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              )}

              <div className="space-y-2">
                {data.taxConfiguration.international.length === 0 ? (
                  <p className="text-gray-500 text-center py-4">
                    No international tax rates configured
                  </p>
                ) : (
                  data.taxConfiguration.international.map((tax, index) => (
                    <div key={index} className="flex items-center justify-between bg-gray-50 p-3 rounded">
                      <div>
                        <span className="font-medium">{tax.country}</span>
                        <span className="text-gray-600 ml-2">{tax.rate}% tax</span>
                      </div>
                      {!readonly && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => removeInternationalTax(tax.country)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>

          {/* Tax Summary */}
          <Card>
            <CardHeader>
              <CardTitle>Tax Configuration Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Domestic (India)</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>CGST:</span>
                      <span>{data.taxConfiguration.gst.cgst}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>SGST:</span>
                      <span>{data.taxConfiguration.gst.sgst}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>IGST:</span>
                      <span>{data.taxConfiguration.gst.igst}%</span>
                    </div>
                    <div className="flex justify-between font-medium pt-1 border-t">
                      <span>Total GST:</span>
                      <span>{data.taxConfiguration.gst.cgst + data.taxConfiguration.gst.sgst}%</span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">International</h4>
                  {data.taxConfiguration.international.length === 0 ? (
                    <p className="text-sm text-gray-500">No international tax rates</p>
                  ) : (
                    <div className="space-y-1 text-sm">
                      {data.taxConfiguration.international.slice(0, 5).map((tax) => (
                        <div key={tax.country} className="flex justify-between">
                          <span>{tax.country}:</span>
                          <span>{tax.rate}%</span>
                        </div>
                      ))}
                      {data.taxConfiguration.international.length > 5 && (
                        <p className="text-xs text-gray-500">
                          +{data.taxConfiguration.international.length - 5} more countries
                        </p>
                      )}
                    </div>
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