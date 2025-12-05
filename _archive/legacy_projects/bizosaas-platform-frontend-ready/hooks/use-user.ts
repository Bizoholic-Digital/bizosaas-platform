import { useState, useEffect } from 'react'

export interface User {
  id: string
  name: string
  email: string
  avatar?: string
  role: string
  permissions: string[]
}

export function useUser() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Mock user data for development
    const mockUser: User = {
      id: '1',
      name: 'Demo User',
      email: 'demo@bizosaas.com',
      role: 'admin',
      permissions: ['bizosaas', 'bizoholic', 'coreldove']
    }
    
    // Simulate API call
    setTimeout(() => {
      setUser(mockUser)
      setLoading(false)
    }, 1000)
  }, [])

  return { user, loading }
}