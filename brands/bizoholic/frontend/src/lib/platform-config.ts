'use client'

import { useState } from 'react'

export const platformConfig = {
  name: 'Bizoholic',
  domain: 'bizoholic.com',
  logo: '/bizoholic-logo-hq.png',
  primaryColor: '#2563eb',
  description: 'AI-Powered Marketing Platform',
  className: 'platform-bizoholic'
}

export function usePlatform() {
  const [platform] = useState('bizoholic')
  const [config] = useState(platformConfig)
  
  return { platform, config }
}
