"use client"

import { DashboardLayout } from "@/components/dashboard-layout"
import { DropshippingDashboard } from "@/components/dropshipping-dashboard"

export default function DropshippingPage() {
  return (
    <DashboardLayout userRole="seller">
      <div className="space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-foreground mb-4">
            CoreLDove Dropshipping Portal
          </h1>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
            Source profitable products from Amazon, process them with AI, and automatically list across multiple platforms including MedusaJS, Amazon Marketplace, and Flipkart.
          </p>
        </div>

        <DropshippingDashboard />
      </div>
    </DashboardLayout>
  )
}