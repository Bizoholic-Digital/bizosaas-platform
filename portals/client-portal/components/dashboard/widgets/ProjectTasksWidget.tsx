'use client';

import { useQuery, gql } from 'urql';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const PROJECTS_QUERY = gql`
  query GetProjects($tenantId: String!) {
    projects(tenantId: $tenantId) {
      id
      name
      status
      sourceSystem
      externalUrl
    }
  }
`;

export function ProjectTasksWidget({ tenantId = "default-tenant" }: { tenantId?: string }) {
    const [result] = useQuery({
        query: PROJECTS_QUERY,
        variables: { tenantId },
        pause: !tenantId
    });

    const { data, fetching, error } = result;

    if (!tenantId) return <Card><CardContent className="pt-6"><p className="text-sm text-muted-foreground">Please log in to view projects.</p></CardContent></Card>;

    if (fetching) return <div className="p-4 text-sm text-muted-foreground">Loading projects...</div>;
    if (error) return <div className="p-4 text-sm text-red-500">Error loading projects: {error.message}</div>;

    return (
        <Card>
            <CardHeader>
                <CardTitle className="text-sm font-medium">Active Projects</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    {data?.projects.length === 0 ? (
                        <p className="text-sm text-muted-foreground">No active projects.</p>
                    ) : (
                        data?.projects.map((project: any) => (
                            <div key={project.id} className="flex items-center justify-between border-b pb-2 last:border-0">
                                <div className="space-y-1">
                                    <p className="text-sm font-medium leading-none">{project.name}</p>
                                    <p className="text-xs text-muted-foreground capitalize">
                                        via {project.sourceSystem}
                                    </p>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Badge variant={project.status === 'active' ? 'default' : 'secondary'}>
                                        {project.status}
                                    </Badge>
                                    {project.externalUrl && (
                                        <a
                                            href={project.externalUrl}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-xs text-blue-500 hover:underline"
                                        >
                                            Open ↗
                                        </a>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </CardContent>
        </Card>
    );
}
