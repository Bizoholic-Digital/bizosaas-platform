import { useState, useEffect } from 'react';

export interface NavItem {
    title: string;
    href: string;
    description?: string;
    icon?: string;
}

export interface NavigationData {
    services: NavItem[];
    loading: boolean;
}

export function useNavigation(): NavigationData {
    const [services, setServices] = useState<NavItem[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchNavigation = async () => {
            try {
                const response = await fetch('/api/brain/wagtail/services');
                if (response.ok) {
                    const data = await response.json();
                    if (data.services && data.services.length > 0) {
                        const mappedServices = data.services.map((service: any) => ({
                            title: service.title,
                            href: `/services/${service.slug}`,
                            description: service.service_description || service.description,
                            icon: service.icon
                        }));
                        setServices(mappedServices);
                    }
                }
            } catch (error) {
                console.error('Error fetching navigation:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchNavigation();
    }, []);

    return { services, loading };
}
