'use client';

import { Client, Provider, cacheExchange, fetchExchange } from 'urql';
import { authExchange } from '@urql/exchange-auth';
import { useMemo } from 'react';
import { useAuth } from '../auth/AuthProvider';

export function GraphQLProvider({ children }: { children: React.ReactNode }) {
    const { getToken } = useAuth();

    const client = useMemo(() => {
        return new Client({
            url: process.env.NEXT_PUBLIC_GRAPHQL_URL || `${process.env.NEXT_PUBLIC_BRAIN_API_URL}/graphql` || 'http://localhost:8000/graphql',
            exchanges: [
                cacheExchange,
                authExchange(async (utils) => {
                    const token = await getToken();
                    return {
                        addAuthToOperation(operation) {
                            if (!token) return operation;
                            return utils.appendHeaders(operation, {
                                Authorization: `Bearer ${token}`,
                            });
                        },
                        didAuthError(error) {
                            return error.graphQLErrors.some(e => e.extensions?.code === 'FORBIDDEN');
                        },
                        async refreshAuth() {
                            // NextAuth handles refresh, so we just return null or re-fetch
                        }
                    };
                }),
                fetchExchange
            ],
        });
    }, [getToken]);

    return <Provider value={client}>{children}</Provider>;
}
