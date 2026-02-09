<header class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
  <div class="container mx-auto flex h-16 items-center justify-between px-4">
    <!-- Logo -->
    <div class="flex items-center space-x-4">
      <a href="{{ home_url('/') }}" class="flex items-center space-x-2">
        <img src="https://bizoholic.com/logo.png" alt="Bizoholic Logo" class="h-10 w-auto">
      </a>
      <span class="hidden md:inline-flex px-2 py-1 rounded-full bg-secondary text-secondary-foreground text-xs font-medium">
        AI-Powered Marketing Agency
      </span>
    </div>

    <!-- Desktop Navigation -->
    <nav class="hidden lg:flex items-center space-x-8 text-sm font-medium">
      <a href="{{ home_url('/') }}" class="transition-colors hover:text-primary {{ is_front_page() ? 'text-primary' : 'text-foreground/60 focus:text-foreground' }}">Home</a>
      
      <div class="relative group" x-data="{ open: false }">
        <button @mouseenter="open = true" @mouseleave="open = false" class="flex items-center gap-1 transition-colors hover:text-foreground text-foreground/60">
          Services <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
        </button>
        <div x-show="open" @mouseenter="open = true" @mouseleave="open = false" class="absolute top-full left-0 mt-2 w-64 bg-background border rounded-lg shadow-lg z-50 p-4 space-y-3">
          <a href="/services/seo" class="block text-sm hover:text-primary transition-colors">🔍 SEO Optimization</a>
          <a href="/services/ppc" class="block text-sm hover:text-primary transition-colors">💰 Paid Advertising</a>
          <a href="/services/social" class="block text-sm hover:text-primary transition-colors">📱 Social Media</a>
          <a href="/services/content" class="block text-sm hover:text-primary transition-colors">✍️ Content Marketing</a>
          <hr class="border-border my-2">
          <a href="/services" class="block text-sm font-medium text-primary hover:text-primary/80 transition-colors">View All Services →</a>
        </div>
      </div>

      <a href="/resources" class="text-foreground/60 hover:text-foreground transition-colors">Resources</a>
      <a href="/case-studies" class="text-foreground/60 hover:text-foreground transition-colors">Case Studies</a>
      <a href="/blog" class="text-foreground/60 hover:text-foreground transition-colors">Blog</a>
      <a href="/about" class="text-foreground/60 hover:text-foreground transition-colors">About</a>
    </nav>

    <!-- Auth Section -->
    <div class="flex items-center space-x-4">
      <a href="https://app.bizoholic.net/login" class="inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground">
        Client Portal
      </a>
      <a href="https://app.bizoholic.net/register" class="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90">
        Get Started <svg class="ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
      </a>
    </div>
  </div>
</header>
