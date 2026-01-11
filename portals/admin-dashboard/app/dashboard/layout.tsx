import DashboardLayout from '@/components/ui/dashboard-layout';
import { HeaderProvider } from '@/lib/contexts/HeaderContext';

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <HeaderProvider>
            <DashboardLayout>
                {children}
            </DashboardLayout>
        </HeaderProvider>
    );
}
