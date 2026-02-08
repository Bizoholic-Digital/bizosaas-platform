'use client';
import { useAuth } from '@/components/auth/AuthProvider';
import { Plug, Sparkles, BarChart3, TrendingUp, Loader2 } from 'lucide-react';
import { getUserDisplayInfoFromSession } from '@/utils/rbac';
import { ProjectTasksWidget } from '@/components/dashboard/widgets/ProjectTasksWidget';
import { ServiceStatusWidget } from '@/components/dashboard/widgets/ServiceStatusWidget';
import { MagicDiscovery } from '@/components/discovery/MagicDiscovery';
import { CreditBalanceWidget } from '@/components/billing/CreditBalanceWidget';
import { useSetHeader } from '@/lib/contexts/HeaderContext';
import { gql, useQuery } from 'urql';
import Link from 'next/link';

const GET_DASHBOARD_STATS = gql`
  query GetDashboardStats($tenantId: String!) {
    cmsStats(tenantId: $tenantId) {
      posts
      pages
    }
    crmStats(tenantId: $tenantId) {
      contacts
      deals
    }
    ecommerceStats(tenantId: $tenantId) {
      totalSales
      totalOrders
    }
  }
`;

export default function DashboardPage() {
  useSetHeader("Product Dashboard", "Manage your connected platforms and automation flows.");
  const { user } = useAuth();

  const [result] = useQuery({
    query: GET_DASHBOARD_STATS,
    variables: { tenantId: user?.tenant || 'default' },
    pause: !user,
  });

  const { data, fetching } = result;

  const sessionUser = user ? {
    role: user.role,
    tenant_id: user.tenant,
    name: user.name,
    email: user.email
  } : null;

  const userInfo = getUserDisplayInfoFromSession(sessionUser);
  const { tenantId } = userInfo;

  const stats = {
    connectors: (data?.cmsStats ? 1 : 0) + (data?.crmStats ? 1 : 0) + (data?.ecommerceStats ? 1 : 0),
    contacts: data?.crmStats?.contacts || 0,
    sales: data?.ecommerceStats?.totalSales || 0,
    posts: data?.cmsStats?.posts || 0
  };

  return (
    <div className="p-4 md:p-6 space-y-4 md:space-y-6">
      <MagicDiscovery />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Link href="/dashboard/connectors" className="group">
              <div className="bg-white dark:bg-gray-900 p-4 md:p-6 rounded-xl border border-gray-200 dark:border-gray-800 hover:border-blue-500 transition-all duration-200 shadow-sm hover:shadow-md cursor-pointer h-full">
                <div className="flex items-center">
                  <div className="w-10 h-10 md:w-12 md:h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center group-hover:bg-blue-600 transition-colors">
                    <Plug className="w-5 h-5 md:w-6 md:h-6 text-blue-600 dark:text-blue-400 group-hover:text-white transition-colors" />
                  </div>
                  <div className="ml-3 md:ml-4">
                    <p className="text-[10px] md:text-sm font-bold text-gray-400 uppercase tracking-tight font-sans">Platforms</p>
                    <p className="text-lg md:text-2xl font-black text-gray-900 dark:text-white leading-none mt-1">{stats.connectors || '...'}</p>
                  </div>
                </div>
              </div>
            </Link>

            <Link href="/crm/contacts" className="group">
              <div className="bg-white dark:bg-gray-900 p-4 md:p-6 rounded-xl border border-gray-200 dark:border-gray-800 hover:border-green-500 transition-all duration-200 shadow-sm hover:shadow-md cursor-pointer h-full">
                <div className="flex items-center">
                  <div className="w-10 h-10 md:w-12 md:h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center group-hover:bg-green-600 transition-colors">
                    <Sparkles className="w-5 h-5 md:w-6 md:h-6 text-green-600 dark:text-green-400 group-hover:text-white transition-colors" />
                  </div>
                  <div className="ml-3 md:ml-4">
                    <p className="text-[10px] md:text-sm font-bold text-gray-400 uppercase tracking-tight font-sans">Contacts</p>
                    <p className="text-lg md:text-2xl font-black text-gray-900 dark:text-white leading-none mt-1">{stats.contacts}</p>
                  </div>
                </div>
              </div>
            </Link>

            <Link href="/content/blog" className="group">
              <div className="bg-white dark:bg-gray-900 p-4 md:p-6 rounded-xl border border-gray-200 dark:border-gray-800 hover:border-purple-500 transition-all duration-200 shadow-sm hover:shadow-md cursor-pointer h-full">
                <div className="flex items-center">
                  <div className="w-10 h-10 md:w-12 md:h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center group-hover:bg-purple-600 transition-colors">
                    <BarChart3 className="w-5 h-5 md:w-6 md:h-6 text-purple-600 dark:text-purple-400 group-hover:text-white transition-colors" />
                  </div>
                  <div className="ml-3 md:ml-4">
                    <p className="text-[10px] md:text-sm font-bold text-gray-400 uppercase tracking-tight font-sans">Posts</p>
                    <p className="text-lg md:text-2xl font-black text-gray-900 dark:text-white leading-none mt-1">{stats.posts}</p>
                  </div>
                </div>
              </div>
            </Link>

            <Link href="/ecommerce" className="group">
              <div className="bg-white dark:bg-gray-900 p-4 md:p-6 rounded-xl border border-gray-200 dark:border-gray-800 hover:border-orange-500 transition-all duration-200 shadow-sm hover:shadow-md cursor-pointer h-full">
                <div className="flex items-center">
                  <div className="w-10 h-10 md:w-12 md:h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center group-hover:bg-orange-600 transition-colors">
                    <TrendingUp className="w-5 h-5 md:w-6 md:h-6 text-orange-600 dark:text-orange-400 group-hover:text-white transition-colors" />
                  </div>
                  <div className="ml-3 md:ml-4">
                    <p className="text-[10px] md:text-sm font-bold text-gray-400 uppercase tracking-tight font-sans">Sales</p>
                    <p className="text-lg md:text-2xl font-black text-gray-900 dark:text-white leading-none mt-1">${stats.sales.toLocaleString()}</p>
                  </div>
                </div>
              </div>
            </Link>
          </div>
        </div>
        <div className="lg:col-span-1 space-y-6">
          <CreditBalanceWidget balance={1125} used={250} available={875} />
          <ServiceStatusWidget />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* GraphQL Powered Widget */}
        <ProjectTasksWidget tenantId={tenantId} />

        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Activity</h3>
            <Link href="/dashboard/activity">
              <button className="text-sm text-blue-500 hover:underline">View All</button>
            </Link>
          </div>
          <div className="space-y-4">
            {[
              { label: 'Agent "SEO Expert" generated a report', time: '2 minutes ago', href: '/dashboard/ai-agents', type: 'AI', color: 'bg-blue-100 text-blue-600' },
              { label: 'New Lead via HubSpot', time: '1 hour ago', href: '/dashboard/crm', type: 'CRM', color: 'bg-green-100 text-green-600' },
              { label: 'WooCommerce Sync Completed', time: '3 hours ago', href: '/dashboard/ecommerce', type: 'SHOP', color: 'bg-purple-100 text-purple-600' }
            ].map((item, i) => (
              <Link key={i} href={item.href} className="flex items-center gap-3 hover:bg-slate-50 dark:hover:bg-slate-800/50 p-2 -mx-2 rounded-lg transition-colors cursor-pointer group">
                <div className={`w-8 h-8 rounded-full ${item.color} flex items-center justify-center text-[10px] font-black group-hover:scale-110 transition-transform`}>{item.type}</div>
                <div>
                  <p className="text-sm font-medium text-slate-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{item.label}</p>
                  <p className="text-xs text-gray-500">{item.time}</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Welcome to Bizo</h3>
        <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
          Your central hub for managing your digital presence. Connect your platforms, activate AI agents, and scale your business effortlessly.
        </p>
      </div>
    </div>
  );
}