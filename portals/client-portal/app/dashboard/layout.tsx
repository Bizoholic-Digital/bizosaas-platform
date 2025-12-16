import DashboardLayout from '@/components/ui/dashboard-layout';

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <DashboardLayout title="Dashboard" description="Overview of your business">
            {children}
        </DashboardLayout>
    );
}
