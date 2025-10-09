import { Suspense } from 'react';
import ClientPortalDashboard from "../page";

export default function AnalyticsPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ClientPortalDashboard />
    </Suspense>
  );
}
