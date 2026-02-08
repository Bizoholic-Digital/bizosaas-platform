"use client"

import { MainHeader } from "@/components/layout/main-header"
import { BusinessDirectory } from "@/components/business-directory"

export default function DirectoryPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <MainHeader />
      
      <main className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Business Directory
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Discover and connect with verified local businesses. Find services, read reviews, and get AI-powered recommendations with advanced Meilisearch integration.
          </p>
        </div>

        <div className="max-w-6xl mx-auto">
          <BusinessDirectory enableMockData={true} />
        </div>
      </main>
    </div>
  )
}