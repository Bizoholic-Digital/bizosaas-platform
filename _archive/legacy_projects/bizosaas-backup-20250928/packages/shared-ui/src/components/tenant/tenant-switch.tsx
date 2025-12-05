'use client';

import { useState } from 'react';
import { Button } from '../button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '../dropdown-menu';
import { ChevronDown, Building2 } from 'lucide-react';

interface Tenant {
  id: string;
  name: string;
  slug: string;
}

interface TenantSwitchProps {
  currentTenant: Tenant;
  tenants: Tenant[];
  onTenantChange: (tenant: Tenant) => void;
}

export function TenantSwitch({ currentTenant, tenants, onTenantChange }: TenantSwitchProps) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className="w-full justify-between">
          <div className="flex items-center">
            <Building2 className="mr-2 h-4 w-4" />
            {currentTenant.name}
          </div>
          <ChevronDown className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start" className="w-full">
        {tenants.map((tenant) => (
          <DropdownMenuItem
            key={tenant.id}
            onClick={() => onTenantChange(tenant)}
            className="cursor-pointer"
          >
            <Building2 className="mr-2 h-4 w-4" />
            {tenant.name}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}