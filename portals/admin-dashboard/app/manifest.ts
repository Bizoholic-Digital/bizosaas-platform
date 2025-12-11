import { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
    return {
        name: 'BizOSaaS Admin Dashboard',
        short_name: 'BizOSaaS Admin',
        description: 'BizoSaaS Platform Multi-Tenant Admin Dashboard',
        start_url: '/',
        display: 'standalone',
        background_color: '#ffffff',
        theme_color: '#000000',
        icons: [
            {
                src: '/favicon.ico',
                sizes: 'any',
                type: 'image/x-icon',
            },
        ],
    }
}
