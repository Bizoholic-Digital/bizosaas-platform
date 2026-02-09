'use client';

import React from 'react';
import Link from 'next/link';
import { Building2, Menu, Search, User } from 'lucide-react';
import { Button } from '@/lib/ui';

export function Header() {
  return (
    <header className="directory-header">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <Building2 className="w-8 h-8 text-primary" />
              <span className="text-xl font-bold text-gray-900 dark:text-white">
                BizDirectory
              </span>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link
              href="/"
              className="text-gray-700 hover:text-primary dark:text-gray-300 dark:hover:text-primary transition-colors"
            >
              Home
            </Link>
            <Link
              href="/c"
              className="text-gray-700 hover:text-primary dark:text-gray-300 dark:hover:text-primary transition-colors"
            >
              Categories
            </Link>
            <Link
              href="/search"
              className="text-gray-700 hover:text-primary dark:text-gray-300 dark:hover:text-primary transition-colors"
            >
              Search
            </Link>
            <Link
              href="/dashboard/my-businesses"
              className="text-gray-700 hover:text-primary dark:text-gray-300 dark:hover:text-primary transition-colors"
            >
              My Businesses
            </Link>
          </nav>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-4">
            {/* Quick Search */}
            <Button
              variant="ghost"
              size="icon"
              className="hidden md:flex"
              asChild
            >
              <Link href="/search">
                <Search className="w-5 h-5" />
              </Link>
            </Button>

            {/* User Menu */}
            <Button
              variant="ghost"
              size="icon"
              className="hidden md:flex"
            >
              <User className="w-5 h-5" />
            </Button>

            {/* List Your Business */}
            <Button asChild className="hidden md:flex">
              <Link href="/list-business">
                List Your Business
              </Link>
            </Button>

            {/* Mobile Menu */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
            >
              <Menu className="w-6 h-6" />
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden border-t border-gray-200 dark:border-gray-700 py-3">
          <nav className="flex flex-col space-y-2">
            <Link
              href="/"
              className="text-gray-700 hover:text-primary dark:text-gray-300 dark:hover:text-primary transition-colors py-2"
            >
              Home
            </Link>
            <Link
              href="/c"
              className="text-gray-700 hover:text-primary dark:text-gray-300 dark:hover:text-primary transition-colors py-2"
            >
              Categories
            </Link>
            <Link
              href="/search"
              className="text-gray-700 hover:text-primary dark:text-gray-300 dark:hover:text-primary transition-colors py-2"
            >
              Search
            </Link>
            <Link
              href="/dashboard/my-businesses"
              className="text-gray-700 hover:text-primary dark:text-gray-300 dark:hover:text-primary transition-colors py-2"
            >
              My Businesses
            </Link>
            <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
              <Button asChild className="w-full">
                <Link href="/list-business">
                  List Your Business
                </Link>
              </Button>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
}