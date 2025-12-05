export type Platform = 'bizoholic' | 'bizosaas' | 'coreldove';

export function getCurrentPlatform(): Platform {
  return 'bizoholic';
}

export function getPlatformConfig(platform?: Platform | string) {
  return {
    name: 'Bizoholic',
    domain: 'bizoholic.com',
    logo: '/bizoholic-logo-hq.png',
    primaryColor: '#2563eb',
    description: 'AI-Powered Marketing Platform',
    className: 'platform-bizoholic'
  }
}

export function getPlatform() {
  return {
    name: 'bizoholic',
    displayName: 'Bizoholic',
    theme: {
      primary: '#2563eb',
      secondary: '#1e40af',
    }
  }
}
