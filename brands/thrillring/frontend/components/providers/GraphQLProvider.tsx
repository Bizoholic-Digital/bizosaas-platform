'use client';

import { Client, Provider, cacheExchange, fetchExchange } from 'urql';
import { useMemo } from 'react';

export function GraphQLProvider({ children }: { children: React.ReactNode }) {
    const client = useMemo(() => {
        return new Client({
            url: process.env.NEXT_PUBLIC_GRAPHQL_URL || `${process.env.NEXT_PUBLIC_BRAIN_API_URL}/graphql` || 'http://localhost:8000/graphql',
            exchanges: [cacheExchange, fetchExchange],
        });
    }, []);

    return <Provider value={client}>{children}</Provider>;
}
