'use client'

import Link from 'next/link'
import { Plus, Search } from 'lucide-react'

export default function ProjectsPage() {
  const projects = [
    { id: 1, name: 'SEO Campaign Q1', status: 'Active', progress: 75 },
    { id: 2, name: 'PPC Ads - Summer Sale', status: 'Active', progress: 60 },
    { id: 3, name: 'Email Automation', status: 'Completed', progress: 100 }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Projects</h1>
          <button className="btn-primary flex items-center gap-2">
            <Plus className="w-5 h-5" />
            New Project
          </button>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="mb-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="search"
                placeholder="Search projects..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          <div className="space-y-4">
            {projects.map((project) => (
              <div key={project.id} className="p-4 border border-gray-200 rounded-lg hover:border-primary-500 transition-colors">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-lg font-semibold text-gray-900">{project.name}</h3>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${project.status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'}`}>
                    {project.status}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                  <div className="bg-primary-600 h-2 rounded-full" style={{ width: `${project.progress}%` }}></div>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">{project.progress}% complete</span>
                  <Link href={`/dashboard/projects/${project.id}`} className="text-primary-600 hover:text-primary-700 font-medium">
                    View Details
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
