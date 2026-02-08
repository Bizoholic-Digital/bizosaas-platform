import { LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface StatsCardProps {
  title: string
  value: string | number
  change?: {
    value: number
    label: string
    positive?: boolean
  }
  icon: LucideIcon
  iconColor?: string
  loading?: boolean
}

export default function StatsCard({
  title,
  value,
  change,
  icon: Icon,
  iconColor = 'bg-solid-900',
  loading = false,
}: StatsCardProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="h-4 bg-gray-200 rounded w-24 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-32"></div>
          </div>
          <div className="h-12 w-12 bg-gray-200 rounded-lg"></div>
        </div>
        {change && (
          <div className="mt-4 h-4 bg-gray-200 rounded w-20"></div>
        )}
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        <div className={cn('p-3 rounded-lg', iconColor)}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>

      {change && (
        <div className="mt-4 flex items-center gap-1">
          <span
            className={cn(
              'text-sm font-semibold',
              change.positive ? 'text-green-600' : 'text-red-600'
            )}
          >
            {change.positive ? '+' : ''}
            {change.value}%
          </span>
          <span className="text-sm text-gray-600">{change.label}</span>
        </div>
      )}
    </div>
  )
}
