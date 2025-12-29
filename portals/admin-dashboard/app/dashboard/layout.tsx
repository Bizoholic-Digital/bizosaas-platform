import DashboardLayout from '@/components/ui/dashboard-layout';

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <DashboardLayout title="Platform Administration" description="Centralized orchestration and platform health at a glance.">
            {children}
        </DashboardLayout>
    );
}
