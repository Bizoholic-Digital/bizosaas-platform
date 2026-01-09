import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertCircle, Plug } from 'lucide-react';
import Link from 'next/link';

interface ConnectionPromptProps {
    serviceName: string;
    serviceIcon?: React.ReactNode;
    description?: string;
    onConnect?: () => void;
    actionUrl?: string;
}

export function ConnectionPrompt({
    serviceName,
    serviceIcon,
    description,
    onConnect,
    actionUrl
}: ConnectionPromptProps) {
    return (
        <div className="flex items-center justify-center min-h-[400px]">
            <Card className="max-w-md w-full">
                <CardHeader className="text-center">
                    <div className="mx-auto mb-4 w-16 h-16 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                        {serviceIcon || <Plug className="w-8 h-8 text-blue-600 dark:text-blue-400" />}
                    </div>
                    <CardTitle className="text-2xl">Connect to {serviceName}</CardTitle>
                    <CardDescription>
                        {description || `Connect your ${serviceName} account to view and manage your data.`}
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-start gap-3 p-3 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-800">
                        <AlertCircle className="w-5 h-5 text-amber-600 dark:text-amber-400 mt-0.5" />
                        <div className="text-sm text-amber-800 dark:text-amber-200">
                            <p className="font-medium mb-1">Connection Required</p>
                            <p className="text-amber-700 dark:text-amber-300">
                                You need to connect your {serviceName} account before you can access this page.
                            </p>
                        </div>
                    </div>

                    {onConnect ? (
                        <Button onClick={onConnect} className="w-full" size="lg">
                            <Plug className="w-4 h-4 mr-2" />
                            Connect {serviceName}
                        </Button>
                    ) : (
                        <Link href={actionUrl || "/dashboard/connectors"} className="block">
                            <Button className="w-full" size="lg">
                                <Plug className="w-4 h-4 mr-2" />
                                {actionUrl ? `Connect ${serviceName}` : "Go to Connectors"}
                            </Button>
                        </Link>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
