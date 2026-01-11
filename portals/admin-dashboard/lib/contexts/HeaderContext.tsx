'use client';

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

interface HeaderContextType {
    title: string;
    description: string;
    setHeader: (title: string, description?: string) => void;
}

const HeaderContext = createContext<HeaderContextType | undefined>(undefined);

export function HeaderProvider({ children, initialTitle = "Platform Administration", initialDescription = "Centralized orchestration and platform health at a glance." }: {
    children: ReactNode;
    initialTitle?: string;
    initialDescription?: string;
}) {
    const [title, setTitleState] = useState(initialTitle);
    const [description, setDescriptionState] = useState(initialDescription);

    const setHeader = useCallback((newTitle: string, newDescription?: string) => {
        setTitleState(newTitle);
        setDescriptionState(newDescription || "");
    }, []);

    return (
        <HeaderContext.Provider value={{ title, description, setHeader }}>
            {children}
        </HeaderContext.Provider>
    );
}

export function useHeader() {
    const context = useContext(HeaderContext);
    if (context === undefined) {
        throw new Error('useHeader must be used within a HeaderProvider');
    }
    return context;
}

export function useSetHeader(title: string, description?: string) {
    const { setHeader } = useHeader();

    React.useEffect(() => {
        setHeader(title, description);
    }, [title, description, setHeader]);
}
