import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'CMS Dashboard | BizOSaaS',
    description: 'Manage your website content',
};

export default function CMSPage() {
    return (
        <div className="flex flex-col h-[calc(100vh-8rem)] w-full">
            <div className="flex items-center justify-between space-y-2 mb-4">
                <h2 className="text-3xl font-bold tracking-tight">Content Management</h2>
                <div className="flex items-center space-x-2">
                    <a
                        href="https://cms.bizoholic.net/admin/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-blue-600 hover:underline"
                    >
                        Open in New Tab
                    </a>
                </div>
            </div>
            <div className="flex-1 w-full overflow-hidden bg-white rounded-lg shadow-sm border border-gray-200">
                <iframe
                    src="https://cms.bizoholic.net/admin/"
                    className="w-full h-full border-none"
                    title="Wagtail CMS Dashboard"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    loading="lazy"
                />
            </div>
        </div>
    );
}
