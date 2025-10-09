"use client"

import Image from "next/image"
import Link from "next/link"
import { ThemeToggle } from "@/components/ui/theme-toggle"
import { Button } from "@/components/ui/button"
import { Menu } from "lucide-react"
import { usePlatform } from "@/lib/platform-config"

interface MainHeaderProps {
  showNavigation?: boolean
}

export function MainHeader({ showNavigation = true }: MainHeaderProps) {
  const { platform, config } = usePlatform()
  
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <div className="flex items-center space-x-4">
          <Link href="/" className="flex items-center space-x-2">
            <Image
              src={config.logo}
              alt={`${config.name} Logo`}
              width={40}
              height={40}
              className="h-8 w-auto"
              priority
              quality={100}
            />
          </Link>
        </div>

        {showNavigation && (
          <nav className="hidden md:flex items-center space-x-6">
            <Link 
              href="/onboarding" 
              className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
            >
              Get Started
            </Link>
            <Link 
              href="/services" 
              className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
            >
              Services
            </Link>
            <Link 
              href="/directory" 
              className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
            >
              Directory
            </Link>
            <Link 
              href="/about" 
              className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
            >
              About
            </Link>
          </nav>
        )}

        <div className="flex items-center space-x-4">
          <ThemeToggle />
          {showNavigation && (
            <>
              <Button variant="ghost" size="sm" asChild className="hidden md:inline-flex">
                <Link href="/auth/login">Sign In</Link>
              </Button>
              <Button size="sm" asChild>
                <Link href="/onboarding">Start Free Trial</Link>
              </Button>
              <Button variant="ghost" size="sm" className="md:hidden">
                <Menu className="h-5 w-5" />
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  )
}