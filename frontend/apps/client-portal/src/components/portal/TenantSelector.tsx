'use client'

import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'
import { Check, ChevronsUpDown, Building2 } from 'lucide-react'
import { useTenant } from '@/contexts/TenantContext'
import { cn } from '@/lib/utils'

export default function TenantSelector() {
  const { currentTenant, availableTenants, switchTenant, isLoading } = useTenant()

  if (!currentTenant && !isLoading) {
    return null
  }

  if (isLoading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg animate-pulse">
        <div className="h-8 w-8 bg-gray-300 rounded-lg" />
        <div className="flex-1">
          <div className="h-4 bg-gray-300 rounded w-24 mb-1" />
          <div className="h-3 bg-gray-300 rounded w-16" />
        </div>
      </div>
    )
  }

  return (
    <Menu as="div" className="relative">
      <Menu.Button className="flex items-center gap-2 w-full px-3 py-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
        {currentTenant?.logo ? (
          <img
            src={currentTenant.logo}
            alt={currentTenant.name}
            className="h-8 w-8 rounded-lg object-cover"
          />
        ) : (
          <div className="h-8 w-8 rounded-lg bg-solid-900 flex items-center justify-center">
            <Building2 className="h-5 w-5 text-white" />
          </div>
        )}
        <div className="flex-1 text-left">
          <p className="text-sm font-semibold text-gray-900">{currentTenant?.name}</p>
          <p className="text-xs text-gray-500 capitalize">{currentTenant?.plan} Plan</p>
        </div>
        <ChevronsUpDown className="h-4 w-4 text-gray-400" />
      </Menu.Button>

      <Transition
        as={Fragment}
        enter="transition ease-out duration-100"
        enterFrom="transform opacity-0 scale-95"
        enterTo="transform opacity-100 scale-100"
        leave="transition ease-in duration-75"
        leaveFrom="transform opacity-100 scale-100"
        leaveTo="transform opacity-0 scale-95"
      >
        <Menu.Items className="absolute left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-80 overflow-y-auto">
          <div className="p-2">
            {availableTenants.map((tenant) => (
              <Menu.Item key={tenant.id}>
                {({ active }) => (
                  <button
                    onClick={() => {
                      if (tenant.id !== currentTenant?.id) {
                        switchTenant(tenant.id)
                      }
                    }}
                    className={cn(
                      'flex items-center gap-3 w-full px-3 py-2 rounded-md text-left',
                      active && 'bg-gray-50',
                      tenant.id === currentTenant?.id && 'bg-solid-50'
                    )}
                  >
                    {tenant.logo ? (
                      <img
                        src={tenant.logo}
                        alt={tenant.name}
                        className="h-8 w-8 rounded-lg object-cover flex-shrink-0"
                      />
                    ) : (
                      <div className="h-8 w-8 rounded-lg bg-solid-900 flex items-center justify-center flex-shrink-0">
                        <Building2 className="h-5 w-5 text-white" />
                      </div>
                    )}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {tenant.name}
                      </p>
                      <div className="flex items-center gap-2">
                        <p className="text-xs text-gray-500 capitalize">{tenant.plan}</p>
                        <span
                          className={cn(
                            'text-xs px-2 py-0.5 rounded-full',
                            tenant.status === 'active'
                              ? 'bg-green-100 text-green-700'
                              : tenant.status === 'trial'
                              ? 'bg-blue-100 text-blue-700'
                              : 'bg-red-100 text-red-700'
                          )}
                        >
                          {tenant.status}
                        </span>
                      </div>
                    </div>
                    {tenant.id === currentTenant?.id && (
                      <Check className="h-5 w-5 text-solid-900 flex-shrink-0" />
                    )}
                  </button>
                )}
              </Menu.Item>
            ))}
          </div>
        </Menu.Items>
      </Transition>
    </Menu>
  )
}
