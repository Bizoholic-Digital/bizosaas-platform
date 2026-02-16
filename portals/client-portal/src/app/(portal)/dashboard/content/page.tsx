import { ContentDashboard } from '@/features/content/components/ContentDashboard'

export default function ContentPage() {
  return (
    <div className="min-h-screen bg-gray-50/50">
      <div className="container py-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <ContentDashboard />
      </div>
    </div>
  )
}
