'use client'

import React, { useState } from 'react'
import { ChevronDown, Building2, ShoppingCart, Users, Gamepad2 } from 'lucide-react'

interface TenantOption {
  id: string
  name: string
  industry: string
  icon: React.ComponentType<any>
  color: string
}

interface TenantSelectorProps {
  currentTenant: string
  onTenantChange: (tenantId: string) => void
}

const tenantOptions: TenantOption[] = [
  {
    id: 'coreldove',
    name: 'CorelDove E-commerce',
    industry: 'E-commerce Platform',
    icon: ShoppingCart,
    color: 'bg-red-500'
  },
  {
    id: 'business_directory',
    name: 'Business Directory',
    industry: 'Local Business Platform',
    icon: Building2,
    color: 'bg-blue-500'
  },
  {
    id: 'thrillring',
    name: 'ThrillRing Gaming',
    industry: 'Gaming & E-sports',
    icon: Gamepad2,
    color: 'bg-purple-500'
  },
  {
    id: 'demo',
    name: 'Demo Client',
    industry: 'General Platform',
    icon: Users,
    color: 'bg-gray-500'
  }
]

export default function TenantSelector({ currentTenant, onTenantChange }: TenantSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)

  const currentTenantData = tenantOptions.find(t => t.id === currentTenant) || tenantOptions[3]
  const CurrentIcon = currentTenantData.icon

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-3 w-full p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750 transition-colors"
      >
        <div className={`w-10 h-10 ${currentTenantData.color} rounded-lg flex items-center justify-center`}>
          <CurrentIcon className="w-5 h-5 text-white" />
        </div>
        <div className="flex-1 text-left">
          <div className="font-semibold text-gray-900 dark:text-white text-sm">
            {currentTenantData.name}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {currentTenantData.industry}
          </div>
        </div>
        <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50">
          <div className="p-2 space-y-1">
            {tenantOptions.map((tenant) => {
              const Icon = tenant.icon
              const isSelected = tenant.id === currentTenant

              return (
                <button
                  key={tenant.id}
                  onClick={() => {
                    onTenantChange(tenant.id)
                    setIsOpen(false)
                  }}
                  className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-colors ${
                    isSelected
                      ? 'bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400'
                      : 'hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                  }`}
                >
                  <div className={`w-8 h-8 ${tenant.color} rounded-lg flex items-center justify-center`}>
                    <Icon className="w-4 h-4 text-white" />
                  </div>
                  <div className="flex-1 text-left">
                    <div className="font-medium text-sm">
                      {tenant.name}
                    </div>
                    <div className="text-xs opacity-75">
                      {tenant.industry}
                    </div>
                  </div>
                  {isSelected && (
                    <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  )}
                </button>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}