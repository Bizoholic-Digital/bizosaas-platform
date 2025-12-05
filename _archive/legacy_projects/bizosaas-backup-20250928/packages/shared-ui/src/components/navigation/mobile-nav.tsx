'use client';

import React, { useState } from 'react';
import { Button } from '../button';
import { HamburgerMenuIcon, Cross1Icon } from '@radix-ui/react-icons';

export function MobileNav() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="md:hidden">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setIsOpen(!isOpen)}
        className="h-9 w-9 p-0"
      >
        {isOpen ? (
          <Cross1Icon className="h-4 w-4" />
        ) : (
          <HamburgerMenuIcon className="h-4 w-4" />
        )}
      </Button>
      
      {isOpen && (
        <div className="absolute top-16 left-0 right-0 bg-white border-b shadow-lg p-4">
          <nav className="flex flex-col space-y-2">
            <a href="/" className="text-sm font-medium">Dashboard</a>
            <a href="/analytics" className="text-sm font-medium">Analytics</a>
            <a href="/bizoholic" className="text-sm font-medium">Bizoholic</a>
            <a href="/coreldove" className="text-sm font-medium">CoreLDove</a>
            <a href="/clients" className="text-sm font-medium">Clients</a>
            <a href="/settings" className="text-sm font-medium">Settings</a>
          </nav>
        </div>
      )}
    </div>
  );
}