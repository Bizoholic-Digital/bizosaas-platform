'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Loader2, ArrowRight, ArrowLeft, Check, Mail } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { useToast } from '@/components/ui/use-toast';

export default function CreateCampaignPage() {
    const router = useRouter();
    const { toast } = useToast();
    const [step, setStep] = useState(1);
    const [isLoading, setIsLoading] = useState(false);

    // Form State
    const [name, setName] = useState('');
    const [goal, setGoal] = useState('');
    const [selectedList, setSelectedList] = useState('');
    const [subject, setSubject] = useState('');

    // Data State
    const [emailLists, setEmailLists] = useState<any[]>([]);

    useEffect(() => {
        // Load email lists when reaching step 2
        if (step === 2 && emailLists.length === 0) {
            loadLists();
        }
    }, [step]);

    const loadLists = async () => {
        try {
            const lists = await brainApi.marketing.getLists();
            setEmailLists(lists || []);
        } catch (error) {
            console.error('Failed to load email lists', error);
        }
    };

    const handleCreate = async () => {
        setIsLoading(true);
        try {
            // 1. Create Campaign
            const campaignData = {
                name,
                goal,
                channels: [
                    {
                        channel_type: 'email',
                        connector_id: 'mailchimp', // simplified for now
                        config: {
                            list_id: selectedList,
                            subject: subject
                        }
                    }
                ]
            };

            const campaign = await brainApi.campaigns.create(campaignData);

            // 2. Publish (Optional, could be separate action)
            await brainApi.campaigns.publish(campaign.id);

            toast({
                title: "Campaign Created",
                description: "Your campaign has been created and queued for publishing.",
            });

            router.push('/dashboard/marketing');
        } catch (error) {
            console.error('Failed to create campaign', error);
            toast({
                title: "Error",
                description: "Failed to create campaign. Please try again.",
                variant: "destructive"
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto p-6 space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Create Campaign</h1>
                <p className="text-muted-foreground mt-1">Design and launch a new marketing campaign</p>
            </div>

            {/* Progress */}
            <div className="flex items-center justify-between mb-8">
                {[1, 2, 3].map((s) => (
                    <div key={s} className="flex items-center">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${step >= s ? 'bg-blue-600 text-white' : 'bg-slate-200 text-slate-500'
                            }`}>
                            {step > s ? <Check className="w-5 h-5" /> : s}
                        </div>
                        {s < 3 && (
                            <div className={`w-24 h-1 mx-2 ${step > s ? 'bg-blue-600' : 'bg-slate-200'
                                }`} />
                        )}
                    </div>
                ))}
            </div>

            <Card>
                {step === 1 && (
                    <>
                        <CardHeader>
                            <CardTitle>Campaign Details</CardTitle>
                            <CardDescription>Start by naming your campaign and defining its goal.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="name">Campaign Name</Label>
                                <Input
                                    id="name"
                                    placeholder="e.g. Summer Sale 2024"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="goal">Goal (Optional)</Label>
                                <Input
                                    id="goal"
                                    placeholder="e.g. Increase revenue by 20%"
                                    value={goal}
                                    onChange={(e) => setGoal(e.target.value)}
                                />
                            </div>
                        </CardContent>
                        <CardFooter className="flex justify-end">
                            <Button onClick={() => setStep(2)} disabled={!name}>
                                Next Step <ArrowRight className="w-4 h-4 ml-2" />
                            </Button>
                        </CardFooter>
                    </>
                )}

                {step === 2 && (
                    <>
                        <CardHeader>
                            <CardTitle>Audience & Content</CardTitle>
                            <CardDescription>Select your audience list and configure email settings.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label>Channel</Label>
                                <div className="flex items-center p-3 border rounded-md bg-slate-50 dark:bg-slate-800">
                                    <Mail className="w-5 h-5 mr-3 text-blue-600" />
                                    <span className="font-medium">Email (Mailchimp)</span>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="list">Target Audience</Label>
                                <Select value={selectedList} onValueChange={setSelectedList}>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select an email list" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {emailLists.map(list => (
                                            <SelectItem key={list.id} value={list.id}>
                                                {list.name} ({list.subscriber_count} subscribers)
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="subject">Subject Line</Label>
                                <Input
                                    id="subject"
                                    placeholder="Enter email subject line"
                                    value={subject}
                                    onChange={(e) => setSubject(e.target.value)}
                                />
                            </div>
                        </CardContent>
                        <CardFooter className="flex justify-between">
                            <Button variant="outline" onClick={() => setStep(1)}>
                                <ArrowLeft className="w-4 h-4 mr-2" /> Back
                            </Button>
                            <Button onClick={() => setStep(3)} disabled={!selectedList || !subject}>
                                Next Step <ArrowRight className="w-4 h-4 ml-2" />
                            </Button>
                        </CardFooter>
                    </>
                )}

                {step === 3 && (
                    <>
                        <CardHeader>
                            <CardTitle>Review & Launch</CardTitle>
                            <CardDescription>Review your campaign settings before launching.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="bg-slate-50 dark:bg-slate-800 p-4 rounded-md space-y-3">
                                <div className="flex justify-between">
                                    <span className="text-muted-foreground">Name:</span>
                                    <span className="font-medium">{name}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-muted-foreground">Goal:</span>
                                    <span className="font-medium">{goal || '-'}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-muted-foreground">Audience:</span>
                                    <span className="font-medium">
                                        {emailLists.find(l => l.id === selectedList)?.name || selectedList}
                                    </span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-muted-foreground">Subject:</span>
                                    <span className="font-medium">{subject}</span>
                                </div>
                            </div>
                        </CardContent>
                        <CardFooter className="flex justify-between">
                            <Button variant="outline" onClick={() => setStep(2)}>
                                <ArrowLeft className="w-4 h-4 mr-2" /> Back
                            </Button>
                            <Button onClick={handleCreate} disabled={isLoading}>
                                {isLoading ? (
                                    <>
                                        <Loader2 className="w-4 h-4 mr-2 animate-spin" /> Publishing...
                                    </>
                                ) : (
                                    <>
                                        <Check className="w-4 h-4 mr-2" /> Launch Campaign
                                    </>
                                )}
                            </Button>
                        </CardFooter>
                    </>
                )}
            </Card>
        </div>
    );
}
