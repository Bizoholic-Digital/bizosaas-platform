'use client';

import React, { useEffect, useState } from 'react';
import {
  Building2, MapPin, Phone, Mail, Globe, Clock, Image as ImageIcon,
  Upload, X, Plus, Minus, Edit3, Camera, User,
  Briefcase, Star, Calendar, AlertCircle, CheckCircle
} from 'lucide-react';

interface BusinessHours {
  [key: string]: {
    open: string;
    close: string;
    closed: boolean;
  };
}

interface BusinessAddress {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
  latitude?: number;
  longitude?: number;
}

interface BusinessContact {
  phone: string;
  email: string;
  website: string;
  fax?: string;
  secondaryPhone?: string;
}

export interface BusinessProfile {
  name: string;
  description: string;
  category: string;
  subcategory: string;
  keywords: string[];
  address: BusinessAddress;
  contact: BusinessContact;
  hours: BusinessHours;
  serviceAreas: string[];
  photos: string[];
  specialHours: Array<{
    date: string;
    hours: string;
    type: 'holiday' | 'special' | 'closed';
  }>;
  attributes: {
    hasWifi: boolean;
    hasParking: boolean;
    wheelchairAccessible: boolean;
    acceptsCreditCards: boolean;
    hasOutdoorSeating: boolean;
    petFriendly: boolean;
    hasDelivery: boolean;
    hasTakeout: boolean;
  };
  socialMedia: {
    facebook?: string;
    instagram?: string;
    twitter?: string;
    linkedin?: string;
    youtube?: string;
  };
  targetAudience: {
    type: 'country-wide' | 'city' | 'county' | 'global';
    locations: string[];
  };
}

interface BusinessProfileSetupProps {
  profile: BusinessProfile;
  onUpdate: (profile: BusinessProfile) => void;
  onValidate: () => boolean;
  forcedTab?: 'basic' | 'contact' | 'hours' | 'attributes' | 'media';
}

const BUSINESS_CATEGORIES = [
  { value: 'restaurant', label: 'Restaurant & Food Service', subcategories: ['Fine Dining', 'Fast Food', 'Cafe', 'Bar', 'Bakery', 'Catering'] },
  { value: 'retail', label: 'Retail & Shopping', subcategories: ['Clothing Store', 'Electronics', 'Grocery Store', 'Bookstore', 'Jewelry', 'Furniture'] },
  { value: 'service', label: 'Professional Services', subcategories: ['Consulting', 'Legal Services', 'Accounting', 'Marketing', 'IT Services', 'Cleaning'] },
  { value: 'healthcare', label: 'Healthcare & Medical', subcategories: ['General Practice', 'Dental', 'Veterinary', 'Pharmacy', 'Physical Therapy', 'Mental Health'] },
  { value: 'beauty', label: 'Beauty & Wellness', subcategories: ['Hair Salon', 'Nail Salon', 'Spa', 'Massage Therapy', 'Fitness Studio', 'Yoga Studio'] },
  { value: 'automotive', label: 'Automotive', subcategories: ['Auto Repair', 'Car Dealership', 'Gas Station', 'Car Wash', 'Auto Parts', 'Towing'] },
  { value: 'real-estate', label: 'Real Estate', subcategories: ['Residential Sales', 'Commercial', 'Property Management', 'Real Estate Agent', 'Mortgage'] },
  { value: 'education', label: 'Education & Training', subcategories: ['School', 'Tutoring', 'Music Lessons', 'Dance Studio', 'Training Center', 'Library'] },
  { value: 'entertainment', label: 'Entertainment & Recreation', subcategories: ['Movie Theater', 'Bowling Alley', 'Amusement Park', 'Sports Venue', 'Art Gallery', 'Museum'] },
  { value: 'home-services', label: 'Home & Garden Services', subcategories: ['Plumbing', 'Electrical', 'HVAC', 'Landscaping', 'Pest Control', 'House Cleaning'] }
];

const DAYS_OF_WEEK = [
  'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
];

export function BusinessProfileSetup({ profile, onUpdate, onValidate, forcedTab }: BusinessProfileSetupProps) {
  const [activeTab, setActiveTab] = useState<'basic' | 'contact' | 'hours' | 'attributes' | 'media'>(forcedTab || 'basic');

  useEffect(() => {
    if (forcedTab) {
      setActiveTab(forcedTab);
    }
  }, [forcedTab]);

  const [newKeyword, setNewKeyword] = useState('');
  const [newServiceArea, setNewServiceArea] = useState('');

  const updateProfile = (updates: Partial<BusinessProfile>) => {
    onUpdate({ ...profile, ...updates });
  };

  const updateAddress = (updates: Partial<BusinessAddress>) => {
    updateProfile({ address: { ...profile.address, ...updates } });
  };

  const updateContact = (updates: Partial<BusinessContact>) => {
    updateProfile({ contact: { ...profile.contact, ...updates } });
  };

  const updateHours = (day: string, updates: Partial<BusinessHours[string]>) => {
    updateProfile({
      hours: {
        ...profile.hours,
        [day]: { ...profile.hours[day], ...updates }
      }
    });
  };

  const updateAttributes = (updates: Partial<BusinessProfile['attributes']>) => {
    updateProfile({ attributes: { ...profile.attributes, ...updates } });
  };

  const updateSocialMedia = (updates: Partial<BusinessProfile['socialMedia']>) => {
    updateProfile({ socialMedia: { ...profile.socialMedia, ...updates } });
  };

  const addKeyword = () => {
    if (newKeyword.trim() && !profile.keywords.includes(newKeyword.trim())) {
      updateProfile({ keywords: [...profile.keywords, newKeyword.trim()] });
      setNewKeyword('');
    }
  };

  const removeKeyword = (keyword: string) => {
    updateProfile({ keywords: profile.keywords.filter(k => k !== keyword) });
  };

  const addServiceArea = () => {
    if (newServiceArea.trim() && !profile.serviceAreas.includes(newServiceArea.trim())) {
      updateProfile({ serviceAreas: [...profile.serviceAreas, newServiceArea.trim()] });
      setNewServiceArea('');
    }
  };

  const removeServiceArea = (area: string) => {
    updateProfile({ serviceAreas: profile.serviceAreas.filter(a => a !== area) });
  };

  const addTargetLocation = () => {
    if (newServiceArea.trim() && !profile.targetAudience.locations.includes(newServiceArea.trim())) {
      updateProfile({
        targetAudience: {
          ...profile.targetAudience,
          locations: [...profile.targetAudience.locations, newServiceArea.trim()]
        }
      });
      setNewServiceArea('');
    }
  };

  const removeTargetLocation = (location: string) => {
    updateProfile({
      targetAudience: {
        ...profile.targetAudience,
        locations: profile.targetAudience.locations.filter(l => l !== location)
      }
    });
  };

  const getSelectedCategory = () => {
    return BUSINESS_CATEGORIES.find(cat => cat.value === profile.category);
  };

  const validateBasicInfo = () => {
    return profile.name.trim() !== '' &&
      profile.description.trim() !== '' &&
      profile.category !== '' &&
      profile.targetAudience.locations.length > 0;
  };

  const validateContactInfo = () => {
    return profile.contact.phone.trim() !== '' &&
      profile.contact.email.trim() !== '' &&
      profile.address.street.trim() !== '' &&
      profile.address.city.trim() !== '' &&
      profile.address.state.trim() !== '' &&
      profile.address.zipCode.trim() !== '';
  };

  const validateBusinessHours = () => {
    return Object.values(profile.hours).some(hours => !hours.closed);
  };

  const renderBasicInfoTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Business Name *
            </label>
            <input
              type="text"
              value={profile.name}
              onChange={(e) => updateProfile({ name: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter your business name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Business Description *
            </label>
            <textarea
              value={profile.description}
              onChange={(e) => updateProfile({ description: e.target.value })}
              rows={4}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Describe your business, services, and what makes you unique..."
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {profile.description.length}/500 characters
            </p>
          </div>

          <div className="pt-4 border-t border-gray-100 dark:border-gray-800">
            <h4 className="text-md font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <MapPin className="w-5 h-5 mr-2 text-blue-500" />
              Target Audience Focus *
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Audience Type
                </label>
                <select
                  value={profile.targetAudience.type}
                  onChange={(e) => updateProfile({ targetAudience: { ...profile.targetAudience, type: e.target.value as any } })}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                >
                  <option value="country-wide">Country-wide</option>
                  <option value="city">Specific City</option>
                  <option value="county">Specific County</option>
                  <option value="global">Global Focus</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Add Location
                </label>
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={newServiceArea}
                    onChange={(e) => setNewServiceArea(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTargetLocation())}
                    className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                    placeholder={`e.g. ${profile.targetAudience.type === 'country-wide' ? 'United States' : 'New York City'}`}
                  />
                  <button
                    onClick={addTargetLocation}
                    className="px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    type="button"
                  >
                    <Plus className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>

            {profile.targetAudience.locations.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-4">
                {profile.targetAudience.locations.map(loc => (
                  <span key={loc} className="inline-flex items-center px-3 py-1 bg-blue-50 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-lg border border-blue-100 dark:border-blue-800 text-sm">
                    {loc}
                    <button onClick={() => removeTargetLocation(loc)} className="ml-2 hover:text-red-500" type="button">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            )}
            {!profile.targetAudience.locations.length && (
              <p className="text-sm text-amber-600 dark:text-amber-400 flex items-center">
                <AlertCircle className="w-4 h-4 mr-1" />
                Please add at least one target location to proceed.
              </p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Business Category *
              </label>
              <select
                value={profile.category}
                onChange={(e) => updateProfile({ category: e.target.value, subcategory: '' })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select category</option>
                {BUSINESS_CATEGORIES.map(cat => (
                  <option key={cat.value} value={cat.value}>{cat.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Subcategory
              </label>
              <select
                value={profile.subcategory}
                onChange={(e) => updateProfile({ subcategory: e.target.value })}
                disabled={!profile.category}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
              >
                <option value="">Select subcategory</option>
                {getSelectedCategory()?.subcategories.map(sub => (
                  <option key={sub} value={sub}>{sub}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Keywords & Tags
            </label>
            <div className="flex items-center space-x-2 mb-2">
              <input
                type="text"
                value={newKeyword}
                onChange={(e) => setNewKeyword(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addKeyword())}
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Add keyword..."
              />
              <button
                onClick={addKeyword}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {profile.keywords.map((keyword, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400 rounded-full text-sm"
                >
                  {keyword}
                  <button
                    onClick={() => removeKeyword(keyword)}
                    className="ml-2 hover:text-blue-600"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Service Areas
            </label>
            <div className="flex items-center space-x-2 mb-2">
              <input
                type="text"
                value={newServiceArea}
                onChange={(e) => setNewServiceArea(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addServiceArea())}
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Add service area..."
              />
              <button
                onClick={addServiceArea}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {profile.serviceAreas.map((area, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400 rounded-full text-sm"
                >
                  <MapPin className="w-3 h-3 mr-1" />
                  {area}
                  <button
                    onClick={() => removeServiceArea(area)}
                    className="ml-2 hover:text-green-600"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>

          <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
            <h4 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">💡 Tips for Better Visibility</h4>
            <ul className="text-sm text-blue-800 dark:text-blue-400 space-y-1">
              <li>• Use specific keywords customers search for</li>
              <li>• Include your neighborhood or city names</li>
              <li>• Mention unique services or specialties</li>
              <li>• Keep descriptions clear and engaging</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );

  const renderContactInfoTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
            <Phone className="w-5 h-5 mr-2" />
            Contact Information
          </h4>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Primary Phone Number *
            </label>
            <input
              type="tel"
              value={profile.contact.phone}
              onChange={(e) => updateContact({ phone: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="(555) 123-4567"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Secondary Phone
            </label>
            <input
              type="tel"
              value={profile.contact.secondaryPhone || ''}
              onChange={(e) => updateContact({ secondaryPhone: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="(555) 987-6543"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Email Address *
            </label>
            <input
              type="email"
              value={profile.contact.email}
              onChange={(e) => updateContact({ email: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="business@example.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Website
            </label>
            <input
              type="url"
              value={profile.contact.website}
              onChange={(e) => updateContact({ website: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="https://www.yourbusiness.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Fax Number
            </label>
            <input
              type="tel"
              value={profile.contact.fax || ''}
              onChange={(e) => updateContact({ fax: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="(555) 123-4568"
            />
          </div>
        </div>

        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
            <MapPin className="w-5 h-5 mr-2" />
            Business Address
          </h4>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Street Address *
            </label>
            <input
              type="text"
              value={profile.address.street}
              onChange={(e) => updateAddress({ street: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="123 Main Street"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                City *
              </label>
              <input
                type="text"
                value={profile.address.city}
                onChange={(e) => updateAddress({ city: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="City"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                State *
              </label>
              <input
                type="text"
                value={profile.address.state}
                onChange={(e) => updateAddress({ state: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="State"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                ZIP Code *
              </label>
              <input
                type="text"
                value={profile.address.zipCode}
                onChange={(e) => updateAddress({ zipCode: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="12345"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Country
              </label>
              <select
                value={profile.address.country}
                onChange={(e) => updateAddress({ country: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="US">United States</option>
                <option value="CA">Canada</option>
                <option value="GB">United Kingdom</option>
                <option value="AU">Australia</option>
              </select>
            </div>
          </div>

          <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
            <h5 className="font-semibold text-yellow-900 dark:text-yellow-300 mb-2">📍 Address Verification</h5>
            <p className="text-sm text-yellow-800 dark:text-yellow-400 mb-2">
              We'll verify this address with mapping services to ensure accuracy.
            </p>
            <button className="text-sm bg-yellow-600 text-white px-3 py-1 rounded hover:bg-yellow-700">
              Verify Address
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  const renderBusinessHoursTab = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <Clock className="w-5 h-5 mr-2" />
          Business Hours
        </h4>
        <div className="flex space-x-2">
          <button className="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">
            Copy to All Days
          </button>
          <button className="text-sm bg-gray-600 text-white px-3 py-1 rounded hover:bg-gray-700">
            Set Typical Hours
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          {DAYS_OF_WEEK.slice(0, 4).map(day => (
            <div key={day} className="flex items-center space-x-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="w-24">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">
                  {day}
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={!profile.hours[day]?.closed}
                  onChange={(e) => updateHours(day, { closed: !e.target.checked })}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-600 dark:text-gray-400">Open</span>
              </div>
              {!profile.hours[day]?.closed && (
                <>
                  <input
                    type="time"
                    value={profile.hours[day]?.open || '09:00'}
                    onChange={(e) => updateHours(day, { open: e.target.value })}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                  />
                  <span className="text-gray-500">to</span>
                  <input
                    type="time"
                    value={profile.hours[day]?.close || '17:00'}
                    onChange={(e) => updateHours(day, { close: e.target.value })}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                  />
                </>
              )}
            </div>
          ))}
        </div>

        <div className="space-y-4">
          {DAYS_OF_WEEK.slice(4).map(day => (
            <div key={day} className="flex items-center space-x-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="w-24">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">
                  {day}
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={!profile.hours[day]?.closed}
                  onChange={(e) => updateHours(day, { closed: !e.target.checked })}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-600 dark:text-gray-400">Open</span>
              </div>
              {!profile.hours[day]?.closed && (
                <>
                  <input
                    type="time"
                    value={profile.hours[day]?.open || '09:00'}
                    onChange={(e) => updateHours(day, { open: e.target.value })}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                  />
                  <span className="text-gray-500">to</span>
                  <input
                    type="time"
                    value={profile.hours[day]?.close || '17:00'}
                    onChange={(e) => updateHours(day, { close: e.target.value })}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                  />
                </>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Special Hours Section */}
      <div className="mt-8">
        <h5 className="text-md font-semibold text-gray-900 dark:text-white mb-4">Special Hours & Holidays</h5>
        <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-medium text-blue-900 dark:text-blue-300">
              Add holiday hours or special operating times
            </span>
            <button className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
              Add Special Hours
            </button>
          </div>
          {profile.specialHours.length === 0 ? (
            <p className="text-sm text-blue-800 dark:text-blue-400">
              No special hours configured. Add holiday hours or temporary schedule changes.
            </p>
          ) : (
            <div className="space-y-2">
              {profile.specialHours.map((special, index) => (
                <div key={index} className="flex items-center justify-between bg-white dark:bg-gray-800 p-3 rounded">
                  <div>
                    <span className="font-medium">{special.date}</span>
                    <span className="ml-2 text-sm text-gray-600">{special.hours}</span>
                  </div>
                  <button className="text-red-600 hover:text-red-700">
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );

  const renderAttributesTab = () => (
    <div className="space-y-6">
      <h4 className="text-lg font-semibold text-gray-900 dark:text-white">Business Attributes & Amenities</h4>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <h5 className="font-medium text-gray-900 dark:text-white">Accessibility & Amenities</h5>
          {[
            { key: 'wheelchairAccessible', label: 'Wheelchair Accessible', icon: '♿' },
            { key: 'hasParking', label: 'Parking Available', icon: '🚗' },
            { key: 'hasWifi', label: 'Free WiFi', icon: '📶' },
            { key: 'petFriendly', label: 'Pet Friendly', icon: '🐕' },
            { key: 'hasOutdoorSeating', label: 'Outdoor Seating', icon: '🌞' }
          ].map(attr => (
            <div key={attr.key} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="flex items-center">
                <span className="text-lg mr-3">{attr.icon}</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">{attr.label}</span>
              </div>
              <input
                type="checkbox"
                checked={profile.attributes[attr.key as keyof typeof profile.attributes]}
                onChange={(e) => updateAttributes({ [attr.key]: e.target.checked })}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
            </div>
          ))}
        </div>

        <div className="space-y-4">
          <h5 className="font-medium text-gray-900 dark:text-white">Payment & Services</h5>
          {[
            { key: 'acceptsCreditCards', label: 'Accepts Credit Cards', icon: '💳' },
            { key: 'hasDelivery', label: 'Delivery Available', icon: '🚚' },
            { key: 'hasTakeout', label: 'Takeout Available', icon: '🥡' }
          ].map(attr => (
            <div key={attr.key} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="flex items-center">
                <span className="text-lg mr-3">{attr.icon}</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">{attr.label}</span>
              </div>
              <input
                type="checkbox"
                checked={profile.attributes[attr.key as keyof typeof profile.attributes]}
                onChange={(e) => updateAttributes({ [attr.key]: e.target.checked })}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
            </div>
          ))}
        </div>
      </div>

      {/* Social Media */}
      <div className="mt-8">
        <h5 className="font-medium text-gray-900 dark:text-white mb-4">Social Media Profiles</h5>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            { key: 'facebook', label: 'Facebook', placeholder: 'https://facebook.com/yourbusiness' },
            { key: 'instagram', label: 'Instagram', placeholder: 'https://instagram.com/yourbusiness' },
            { key: 'twitter', label: 'Twitter', placeholder: 'https://twitter.com/yourbusiness' },
            { key: 'linkedin', label: 'LinkedIn', placeholder: 'https://linkedin.com/company/yourbusiness' },
            { key: 'youtube', label: 'YouTube', placeholder: 'https://youtube.com/channel/yourbusiness' }
          ].map(social => (
            <div key={social.key}>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {social.label}
              </label>
              <input
                type="url"
                value={profile.socialMedia[social.key as keyof typeof profile.socialMedia] || ''}
                onChange={(e) => updateSocialMedia({ [social.key]: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder={social.placeholder}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderMediaTab = () => (
    <div className="space-y-6">
      <h4 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
        <Camera className="w-5 h-5 mr-2" />
        Photos & Media
      </h4>

      <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
        <div className="text-center">
          <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
            <Upload className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          </div>
          <h5 className="font-semibold text-gray-900 dark:text-white mb-2">Upload Business Photos</h5>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Add photos of your business, products, team, and interior/exterior views
          </p>
          <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 flex items-center mx-auto">
            <Camera className="w-5 h-5 mr-2" />
            Choose Photos
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Placeholder for photo grid */}
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="aspect-square bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center">
            <ImageIcon className="w-8 h-8 text-gray-400" />
          </div>
        ))}
      </div>

      <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
        <h5 className="font-semibold text-yellow-900 dark:text-yellow-300 mb-2">📸 Photo Tips</h5>
        <ul className="text-sm text-yellow-800 dark:text-yellow-400 space-y-1">
          <li>• Use high-quality, well-lit photos</li>
          <li>• Show your business exterior and interior</li>
          <li>• Include photos of products or services</li>
          <li>• Add team photos to build trust</li>
          <li>• Keep photos current and relevant</li>
        </ul>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <nav className="flex space-x-8">
          {[
            { id: 'basic', label: 'Basic Info', icon: Building2, valid: validateBasicInfo() },
            { id: 'contact', label: 'Contact & Address', icon: MapPin, valid: validateContactInfo() },
            { id: 'hours', label: 'Business Hours', icon: Clock, valid: validateBusinessHours() },
            { id: 'attributes', label: 'Attributes', icon: Star, valid: true },
            { id: 'media', label: 'Photos & Media', icon: Camera, valid: true }
          ].map(tab => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${activeTab === tab.id
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
                {tab.valid && (
                  <CheckCircle className="w-4 h-4 text-green-500" />
                )}
                {!tab.valid && tab.id !== 'attributes' && tab.id !== 'media' && (
                  <AlertCircle className="w-4 h-4 text-yellow-500" />
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="min-h-96">
        {activeTab === 'basic' && renderBasicInfoTab()}
        {activeTab === 'contact' && renderContactInfoTab()}
        {activeTab === 'hours' && renderBusinessHoursTab()}
        {activeTab === 'attributes' && renderAttributesTab()}
        {activeTab === 'media' && renderMediaTab()}
      </div>

      {/* Progress Summary */}
      <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <span className="text-sm font-medium text-gray-900 dark:text-white">Profile Completion:</span>
            <div className="flex space-x-2">
              {[validateBasicInfo(), validateContactInfo(), validateBusinessHours()].map((valid, index) => (
                <div
                  key={index}
                  className={`w-3 h-3 rounded-full ${valid ? 'bg-green-500' : 'bg-gray-300 dark:bg-gray-600'}`}
                />
              ))}
            </div>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {[validateBasicInfo(), validateContactInfo(), validateBusinessHours()].filter(Boolean).length}/3 required sections
            </span>
          </div>
          <div className="text-sm text-green-600 dark:text-green-400">
            Ready for AI analysis
          </div>
        </div>
      </div>
    </div>
  );
}