'use client';

import React, { useState } from 'react';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'sonner';

interface Workflow {
    id: string;
    name: string;
    type: string;
    status: string;
    description: string;
    config?: {
        retries?: number;
        timeout?: number;
        notifyOnError?: boolean;
        priority?: string;
    };
}

interface WorkflowConfigModalProps {
    workflow: Workflow | null;
    isOpen: boolean;
    onClose: () => void;
    onSave: (id: string, config: any) => void;
}

export const WorkflowConfigModal: React.FC<WorkflowConfigModalProps> = ({
    workflow,
    isOpen,
    onClose,
    onSave
}) => {
    const [retries, setRetries] = useState(3);
    const [timeout, setTimeoutVal] = useState(30);
    const [notifyOnError, setNotifyOnError] = useState(true);
    const [priority, setPriority] = useState('medium');

    React.useEffect(() => {
        if (workflow?.config) {
            setRetries(workflow.config.retries || 3);
            setTimeoutVal(workflow.config.timeout || 30);
            setNotifyOnError(workflow.config.notifyOnError !== false);
            setPriority(workflow.config.priority || 'medium');
        }
    }, [workflow]);

    if (!workflow) return null;

    const handleSave = () => {
        onSave(workflow.id, {
            retries,
            timeout,
            notifyOnError,
            priority
        });
        toast.success(`Configuration saved for ${workflow.name}`);
        onClose();
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Configure {workflow.name}</DialogTitle>
                    <DialogDescription>
                        Adjust the execution parameters for this {workflow.type.toLowerCase()} workflow.
                    </DialogDescription>
                </DialogHeader>
                <div className="grid gap-6 py-4">
                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <Label htmlFor="retries" className="text-right">Retry Attempts</Label>
                            <span className="text-xs font-mono bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded">{retries}</span>
                        </div>
                        <Slider
                            id="retries"
                            max={10}
                            step={1}
                            value={[retries]}
                            onValueChange={(vals) => setRetries(vals[0])}
                        />
                    </div>

                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <Label htmlFor="timeout" className="text-right">Timeout (seconds)</Label>
                            <span className="text-xs font-mono bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded">{timeout}s</span>
                        </div>
                        <Slider
                            id="timeout"
                            max={300}
                            step={5}
                            value={[timeout]}
                            onValueChange={(vals) => setTimeoutVal(vals[0])}
                        />
                    </div>

                    <div className="flex items-center justify-between space-x-2">
                        <Label htmlFor="notify" className="flex flex-col gap-1">
                            <span>Notify on failure</span>
                            <span className="font-normal text-xs text-muted-foreground">Send an alert if the workflow fails.</span>
                        </Label>
                        <Switch
                            id="notify"
                            checked={notifyOnError}
                            onCheckedChange={setNotifyOnError}
                        />
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="priority">Execution Priority</Label>
                        <Select value={priority} onValueChange={setPriority}>
                            <SelectTrigger id="priority">
                                <SelectValue placeholder="Select priority" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="low">Low - Background processing</SelectItem>
                                <SelectItem value="medium">Medium - Standard priority</SelectItem>
                                <SelectItem value="high">High - Immediate execution</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" onClick={onClose}>Cancel</Button>
                    <Button onClick={handleSave}>Save Changes</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};
