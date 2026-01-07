import { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
    return {
        name: 'Bizo Admin Hub',
        short_name: 'Bizo Admin',
        description: 'Elite Enterprise Platform Control Hub',
        start_url: '/',
        display: 'standalone',
        background_color: '#F8FAFC',
        theme_color: '#2563EB',
        orientation: 'portrait',
        scope: '/',
        icons: [
            {
                src: '/favicon.ico',
                sizes: 'any',
                type: 'image/x-icon',
            },
            {
                src: '/icons/icon-192x192.svg',
                sizes: '192x192',
                type: 'image/svg+xml',
                purpose: 'maskable'
            },
            {
                src: '/icons/icon-512x512.svg',
                sizes: '512x512',
                type: 'image/svg+xml'
            }
        ],
    }
}
