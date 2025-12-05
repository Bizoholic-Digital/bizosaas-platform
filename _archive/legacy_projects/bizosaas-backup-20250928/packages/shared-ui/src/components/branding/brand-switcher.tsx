'use client';

import React from 'react';
import { useBrand } from './brand-provider';
import { Button } from '../button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '../dropdown-menu';
import { ChevronDownIcon } from '@radix-ui/react-icons';

export function BrandSwitcher() {
  const { currentBrand, setBrand, brands } = useBrand();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className="w-[200px] justify-between">
          <div className="flex items-center">
            <div 
              className="w-4 h-4 rounded mr-2" 
              style={{ backgroundColor: currentBrand.primaryColor }}
            />
            {currentBrand.name}
          </div>
          <ChevronDownIcon className="ml-2 h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-[200px]">
        {brands.map((brand) => (
          <DropdownMenuItem
            key={brand.name}
            onClick={() => setBrand(brand)}
            className="flex items-center"
          >
            <div 
              className="w-4 h-4 rounded mr-2" 
              style={{ backgroundColor: brand.primaryColor }}
            />
            {brand.name}
            {brand.name === currentBrand.name && (
              <span className="ml-auto text-blue-600">✓</span>
            )}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}