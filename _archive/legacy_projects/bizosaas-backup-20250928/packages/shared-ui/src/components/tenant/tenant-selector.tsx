'use client';

import { useState } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../select';
import { Building2 } from 'lucide-react';

interface Tenant {
  id: string;
  name: string;
  slug: string;
}

interface TenantSelectorProps {
  tenants: Tenant[];
  value?: string;
  onValueChange: (tenantId: string) => void;
  placeholder?: string;
}

export function TenantSelector({ 
  tenants, 
  value, 
  onValueChange, 
  placeholder = "Select tenant..." 
}: TenantSelectorProps) {
  return (
    <Select value={value} onValueChange={onValueChange}>
      <SelectTrigger className="w-full">
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent>
        {tenants.map((tenant) => (
          <SelectItem key={tenant.id} value={tenant.id}>
            <div className="flex items-center">
              <Building2 className="mr-2 h-4 w-4" />
              {tenant.name}
            </div>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}