'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

type MobileSidebarContextType = {
    isSidebarOpen: boolean;
    toggleSidebar: () => void;
    closeSidebar: () => void;
    isMobile: boolean;
    isTablet: boolean;
    isDesktop: boolean;
};

const MobileSidebarContext = createContext<MobileSidebarContextType | undefined>(undefined);

export function MobileSidebarProvider({ children }: { children: React.ReactNode }) {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [isMobile, setIsMobile] = useState(false);
    const [isTablet, setIsTablet] = useState(false);
    const [isDesktop, setIsDesktop] = useState(true);

    useEffect(() => {
        const handleResize = () => {
            const width = window.innerWidth;
            const mobile = width < 768;
            const tablet = width >= 768 && width < 1024;
            const desktop = width >= 1024;

            setIsMobile(mobile);
            setIsTablet(tablet);
            setIsDesktop(desktop);

            // specific logic for initial load or resize behavior
            if (desktop) {
                setIsSidebarOpen(true);
            } else if (tablet) {
                setIsSidebarOpen(false); // Collapsed by default on tablet
            } else {
                setIsSidebarOpen(false); // Hidden by default on mobile
            }
        };

        // Initial check
        handleResize();

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);
    const closeSidebar = () => setIsSidebarOpen(false);

    return (
        <MobileSidebarContext.Provider
            value={{
                isSidebarOpen,
                toggleSidebar,
                closeSidebar,
                isMobile,
                isTablet,
                isDesktop,
            }}
        >
            {children}
        </MobileSidebarContext.Provider>
    );
}

export const useMobileSidebar = () => {
    const context = useContext(MobileSidebarContext);
    if (context === undefined) {
        throw new Error('useMobileSidebar must be used within a MobileSidebarProvider');
    }
    return context;
};
