"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { Bot, ArrowRight, ChevronDown } from "lucide-react";
import { DarkModeToggle } from "@/components/DarkModeToggle";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/lib/auth";
import { usePlatform } from "@/lib/platform-config";
import { useState } from "react";

export function Header() {
  const { user, logout } = useAuth();
  const { platform, config } = usePlatform();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [servicesDropdownOpen, setServicesDropdownOpen] = useState(false);
  const pathname = usePathname();

  const isActive = (path: string) => {
    if (path === '/' && pathname === '/') return true;
    if (path !== '/' && pathname?.startsWith(path)) return true;
    return false;
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        {/* Logo */}
        <div className="flex items-center space-x-4">
          <Link href="/" className="flex items-center space-x-2">
            <Image
              src={config.logo}
              alt={`${config.name} Logo`}
              width={240}
              height={40}
              className="h-10 w-auto max-w-[240px]"
              priority
              quality={100}
              style={{ objectFit: 'contain' }}
              unoptimized
            />
          </Link>
          <Badge variant="secondary" className="hidden md:inline-flex text-xs">
            {config.description}
          </Badge>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden lg:flex items-center space-x-8 text-sm font-medium">
          <Link
            href="/"
            className={`transition-colors relative ${
              isActive('/') 
                ? 'text-primary border-b-2 border-primary pb-1' 
                : 'text-foreground/60 hover:text-foreground'
            }`}
          >
            Home
          </Link>
          <div className="relative group">
            <Link
              href="/services"
              className={`transition-colors relative flex items-center gap-1 ${
                isActive('/services') 
                  ? 'text-primary border-b-2 border-primary pb-1' 
                  : 'text-foreground/60 hover:text-foreground'
              }`}
              onMouseEnter={() => setServicesDropdownOpen(true)}
            >
              Services
              <ChevronDown className="h-3 w-3" />
            </Link>
            
            {/* Services Dropdown */}
            <div 
              className={`absolute top-full left-0 mt-2 w-64 bg-background border rounded-lg shadow-lg z-50 transition-all duration-200 ${
                servicesDropdownOpen ? 'opacity-100 visible' : 'opacity-0 invisible'
              }`}
              onMouseEnter={() => setServicesDropdownOpen(true)}
              onMouseLeave={() => setServicesDropdownOpen(false)}
            >
              <div className="p-4 space-y-3">
                <Link href="/services/ai-campaign-management" 
                      className="block text-sm hover:text-primary transition-colors"
                      onClick={() => setServicesDropdownOpen(false)}>
                  🤖 AI Campaign Management
                </Link>
                <Link href="/services/content-generation" 
                      className="block text-sm hover:text-primary transition-colors"
                      onClick={() => setServicesDropdownOpen(false)}>
                  🎯 Content Generation
                </Link>
                <Link href="/services/performance-analytics" 
                      className="block text-sm hover:text-primary transition-colors"
                      onClick={() => setServicesDropdownOpen(false)}>
                  📊 Performance Analytics
                </Link>
                <Link href="/services/marketing-automation" 
                      className="block text-sm hover:text-primary transition-colors"
                      onClick={() => setServicesDropdownOpen(false)}>
                  🚀 Marketing Automation
                </Link>
                <Link href="/services/strategy-consulting" 
                      className="block text-sm hover:text-primary transition-colors"
                      onClick={() => setServicesDropdownOpen(false)}>
                  💡 Strategy Consulting
                </Link>
                <Link href="/services/creative-design" 
                      className="block text-sm hover:text-primary transition-colors"
                      onClick={() => setServicesDropdownOpen(false)}>
                  🎨 Creative Design
                </Link>
                <Link href="/services/seo-optimization" 
                      className="block text-sm hover:text-primary transition-colors"
                      onClick={() => setServicesDropdownOpen(false)}>
                  🔍 SEO Optimization
                </Link>
                <Link href="/services/email-marketing" 
                      className="block text-sm hover:text-primary transition-colors"
                      onClick={() => setServicesDropdownOpen(false)}>
                  📧 Email Marketing
                </Link>
                <Link href="/services/social-media-marketing" 
                      className="block text-sm hover:text-primary transition-colors"
                      onClick={() => setServicesDropdownOpen(false)}>
                  📱 Social Media Marketing
                </Link>
                <hr className="border-border my-2" />
                <Link href="/services" 
                      className="block text-sm font-medium text-primary hover:text-primary/80 transition-colors"
                      onClick={() => setServicesDropdownOpen(false)}>
                  View All Services →
                </Link>
              </div>
            </div>
          </div>
          <Link
            href="/resources"
            className={`transition-colors relative ${
              isActive('/resources') 
                ? 'text-primary border-b-2 border-primary pb-1' 
                : 'text-foreground/60 hover:text-foreground'
            }`}
          >
            Resources
          </Link>
          <Link
            href="/case-studies"
            className={`transition-colors relative ${
              isActive('/case-studies') 
                ? 'text-primary border-b-2 border-primary pb-1' 
                : 'text-foreground/60 hover:text-foreground'
            }`}
          >
            Case Studies
          </Link>
          <Link
            href="/blog"
            className={`transition-colors relative ${
              isActive('/blog') 
                ? 'text-primary border-b-2 border-primary pb-1' 
                : 'text-foreground/60 hover:text-foreground'
            }`}
          >
            Blog
          </Link>
          <Link
            href="/about"
            className={`transition-colors relative ${
              isActive('/about') 
                ? 'text-primary border-b-2 border-primary pb-1' 
                : 'text-foreground/60 hover:text-foreground'
            }`}
          >
            About
          </Link>
          <Link
            href="/bizosaas"
            className={`font-medium transition-colors flex items-center gap-1 ${
              isActive('/bizosaas')
                ? 'text-primary border-b-2 border-primary pb-1'
                : 'text-primary hover:text-primary/80'
            }`}
          >
            BizOSaaS
            <ArrowRight className="h-3 w-3" />
          </Link>
        </nav>

        {/* Auth Section */}
        <div className="flex items-center space-x-4">
          <DarkModeToggle />
          {user ? (
            <div className="flex items-center space-x-4">
              <Link href="/dashboard">
                <Button variant="outline" size="sm">
                  Dashboard
                </Button>
              </Link>
              <Button variant="ghost" size="sm" onClick={logout}>
                Logout
              </Button>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <Link href="/auth/login">
                <Button variant="ghost" size="sm">
                  Sign In
                </Button>
              </Link>
              <Link href="/auth/register">
                <Button size="sm">
                  Get Started
                  <ArrowRight className="ml-1 h-4 w-4" />
                </Button>
              </Link>
            </div>
          )}

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {mobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t bg-background/95 backdrop-blur">
          <div className="container py-4 space-y-3">
            <Link
              href="/"
              className="block text-sm font-medium hover:text-primary transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link
              href="/about"
              className="block text-sm font-medium hover:text-primary transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              About
            </Link>
            <div className="space-y-2">
              <Link
                href="/services"
                className="block text-sm font-medium hover:text-primary transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Services
              </Link>
              <div className="pl-4 space-y-2">
                <Link href="/services/ai-campaign-management" 
                      className="block text-xs text-muted-foreground hover:text-primary transition-colors"
                      onClick={() => setMobileMenuOpen(false)}>
                  🤖 AI Campaign Management
                </Link>
                <Link href="/services/content-generation" 
                      className="block text-xs text-muted-foreground hover:text-primary transition-colors"
                      onClick={() => setMobileMenuOpen(false)}>
                  🎯 Content Generation
                </Link>
                <Link href="/services/performance-analytics" 
                      className="block text-xs text-muted-foreground hover:text-primary transition-colors"
                      onClick={() => setMobileMenuOpen(false)}>
                  📊 Performance Analytics
                </Link>
                <Link href="/services/marketing-automation" 
                      className="block text-xs text-muted-foreground hover:text-primary transition-colors"
                      onClick={() => setMobileMenuOpen(false)}>
                  🚀 Marketing Automation
                </Link>
                <Link href="/services/strategy-consulting" 
                      className="block text-xs text-muted-foreground hover:text-primary transition-colors"
                      onClick={() => setMobileMenuOpen(false)}>
                  💡 Strategy Consulting
                </Link>
                <Link href="/services/creative-design" 
                      className="block text-xs text-muted-foreground hover:text-primary transition-colors"
                      onClick={() => setMobileMenuOpen(false)}>
                  🎨 Creative Design
                </Link>
                <Link href="/services/seo-optimization" 
                      className="block text-xs text-muted-foreground hover:text-primary transition-colors"
                      onClick={() => setMobileMenuOpen(false)}>
                  🔍 SEO Optimization
                </Link>
                <Link href="/services/email-marketing" 
                      className="block text-xs text-muted-foreground hover:text-primary transition-colors"
                      onClick={() => setMobileMenuOpen(false)}>
                  📧 Email Marketing
                </Link>
                <Link href="/services/social-media-marketing" 
                      className="block text-xs text-muted-foreground hover:text-primary transition-colors"
                      onClick={() => setMobileMenuOpen(false)}>
                  📱 Social Media Marketing
                </Link>
              </div>
            </div>
            <Link
              href="/blog"
              className="block text-sm font-medium hover:text-primary transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              Blog
            </Link>
            <Link
              href="/pricing"
              className="block text-sm font-medium hover:text-primary transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              Pricing
            </Link>
            <Link
              href="/contact"
              className="block text-sm font-medium hover:text-primary transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              Contact
            </Link>
            <hr className="border-border" />
            <Link
              href="/bizosaas"
              className="block text-sm font-medium text-primary hover:text-primary/80 transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              BizoSaaS Platform →
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}