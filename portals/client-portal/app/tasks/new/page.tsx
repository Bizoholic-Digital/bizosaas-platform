'use client';

import React, { useState } from 'react';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useRouter } from 'next/navigation';
import { Calendar, Clock, User, Tag, ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';

export default function NewTaskPage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);

    // Controlled form state
    const [title, setTitle] = useState('');
    const [category, setCategory] = useState('marketing');
    const [priority, setPriority] = useState('medium');
    const [description, setDescription] = useState('');
    const [dueDate, setDueDate] = useState('');
    const [assignee, setAssignee] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            // Plane API usually needs specific state IDs too, but we start with name/description
            const response = await fetch('/api/brain/plane', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    data: {
                        name: title,
                        description: description,
                        priority: priority,
                        target_date: dueDate || null,
                    },
                    // If marketing is chosen, we target the specific project. 
                    // In a real scenario, we'd fetch projects first and let the user pick.
                    project: category === 'marketing' ? '031b7a9e-ee6d-46f5-99da-8e9e911ae71d' : undefined,
                    workspace: 'bizosaas'
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Failed to create task');
            }

            toast.success("Task created successfully in Plane.so!");
            router.push('/tasks');
        } catch (error: any) {
            console.error('Task creation error:', error);
            toast.error(`Error: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <DashboardLayout title="Create New Task" description="Add a new assignment to your project">
            <div className="p-6 max-w-2xl mx-auto space-y-6">
                <Button variant="ghost" className="mb-4" onClick={() => router.back()}>
                    <ArrowLeft className="mr-2 h-4 w-4" /> Back to Tasks
                </Button>

                <Card className="shadow-xl border-blue-100 dark:border-slate-800">
                    <CardHeader className="bg-slate-50/50 dark:bg-slate-900/50">
                        <CardTitle className="text-xl font-bold">Task Details</CardTitle>
                        <CardDescription>Enter the specifics of the task you want to delegate to your agents.</CardDescription>
                    </CardHeader>
                    <CardContent className="pt-6">
                        <form id="task-form" onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-2">
                                <Label htmlFor="title">Task Title</Label>
                                <Input
                                    id="title"
                                    placeholder="e.g. Update website homepage copy"
                                    value={title}
                                    onChange={(e) => setTitle(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="category">Project Category</Label>
                                    <Select value={category} onValueChange={setCategory}>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select project" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="marketing">Marketing Hub</SelectItem>
                                            <SelectItem value="sales">Sales Pipeline</SelectItem>
                                            <SelectItem value="ops">Business Operations</SelectItem>
                                            <SelectItem value="tech">Technical Infrastructure</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="priority">Priority</Label>
                                    <Select value={priority} onValueChange={setPriority}>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Set priority" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="low">Low</SelectItem>
                                            <SelectItem value="medium">Medium</SelectItem>
                                            <SelectItem value="high">High</SelectItem>
                                            <SelectItem value="urgent">Urgent</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="description">Description (Optional)</Label>
                                <Textarea
                                    id="description"
                                    placeholder="Provide more context or sub-tasks..."
                                    className="min-h-[120px]"
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="due-date">Due Date</Label>
                                    <div className="relative">
                                        <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                                        <Input
                                            id="due-date"
                                            type="date"
                                            className="pl-10"
                                            value={dueDate}
                                            onChange={(e) => setDueDate(e.target.value)}
                                        />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="assignee">Assignee</Label>
                                    <div className="relative">
                                        <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                                        <Input
                                            id="assignee"
                                            placeholder="Team member name"
                                            className="pl-10"
                                            value={assignee}
                                            onChange={(e) => setAssignee(e.target.value)}
                                        />
                                    </div>
                                </div>
                            </div>
                        </form>
                    </CardContent>
                    <CardFooter className="bg-slate-50/50 dark:bg-slate-900/50 pt-6 flex justify-end gap-3">
                        <Button variant="outline" type="button" onClick={() => router.back()}>Cancel</Button>
                        <Button type="submit" form="task-form" disabled={loading} className="bg-blue-600 hover:bg-blue-700">
                            {loading ? "Creating..." : "Create Task"}
                        </Button>
                    </CardFooter>
                </Card>
            </div>
        </DashboardLayout>
    );
}
