'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Slider } from "@/components/ui/slider";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import {
    Bot,
    Zap,
    Save,
    RotateCcw,
    Play,
    FlaskConical,
    Sparkles,
    History,
    CheckCircle,
    AlertCircle
} from 'lucide-react';

// Playground configuration interface (Subset of full agent config)
interface PlaygroundConfiguration {
    id: string;
    name: string;
    version: string;

    // Customizable parameters for playground
    parameters: {
        systemPrompt: string;
        temperature: number;
        maxTokens: number;
        topP: number;
        frequencyPenalty: number;
        presencePenalty: number;
    };

    // Test scenarios
    testScenarios: {
        id: string;
        name: string;
        input: string;
        expectedOutput?: string;
    }[];
}

// Mock playground data
const createMockPlaygroundConfig = (agentId: string): PlaygroundConfiguration => ({
    id: agentId,
    name: 'Lead Scoring Scout (Playground)',
    version: '2.1.4-draft',

    parameters: {
        systemPrompt: "You are an expert lead scoring assistant. Analyze the following lead details and assign a score from 0-100 based on likelihood to convert. Explain your reasoning.",
        temperature: 0.7,
        maxTokens: 1000,
        topP: 1,
        frequencyPenalty: 0,
        presencePenalty: 0,
    },

    testScenarios: [
        {
            id: '1',
            name: ' Enterprise Lead',
            input: "Company: Acme Corp, Employees: 5000, Industry: Tech, Budget: $100k+, Role: CTO",
            expectedOutput: "Score: 95/100"
        },
        {
            id: '2',
            name: 'Small Business Lead',
            input: "Company: Joe's Pizza, Employees: 5, Industry: Food, Budget: $1k, Role: Owner",
            expectedOutput: "Score: 40/100"
        }
    ]
});

export default function PlaygroundManager({ agentId }: { agentId: string }) {
    const [config, setConfig] = useState<PlaygroundConfiguration>(createMockPlaygroundConfig(agentId));
    const [hasChanges, setHasChanges] = useState(false);
    const [isSimulating, setIsSimulating] = useState(false);
    const [simulationResult, setSimulationResult] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState('parameters');

    useEffect(() => {
        setHasChanges(true);
    }, [config]);

    const updateParameter = (field: keyof PlaygroundConfiguration['parameters'], value: any) => {
        setConfig(prev => ({
            ...prev,
            parameters: {
                ...prev.parameters,
                [field]: value
            }
        }));
    };

    const handleRunSimulation = async () => {
        setIsSimulating(true);
        setSimulationResult(null);

        // Simulate AI processing
        setTimeout(() => {
            setSimulationResult(
                "Based on the input provided, I have analyzed the lead scoring criteria.\n\n" +
                "**Score: 88/100**\n\n" +
                "**Reasoning:**\n" +
                "- Strong budget alignment (+30)\n" +
                "- Decision maker role detected (+25)\n" +
                "- Industry match (+20)\n" +
                "- Company size fits ICP (+13)"
            );
            setIsSimulating(false);
        }, 1500);
    };

    const saveExperiment = async () => {
        // Save execution logic here
        setHasChanges(false);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold flex items-center">
                        <FlaskConical className="w-6 h-6 mr-2 text-purple-600" />
                        Agent Playground
                    </h2>
                    <p className="text-gray-600">
                        Sandboxed environment for fine-tuning {config.name}
                    </p>
                </div>
                <div className="flex items-center space-x-2">
                    <Button variant="outline" size="sm" onClick={() => setConfig(createMockPlaygroundConfig(agentId))}>
                        <RotateCcw className="w-4 h-4 mr-2" />
                        Reset
                    </Button>
                    <Button
                        onClick={saveExperiment}
                        disabled={!hasChanges}
                        className="bg-purple-600 hover:bg-purple-700"
                    >
                        <Save className="w-4 h-4 mr-2" />
                        Save Experiment
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Panel: Configuration */}
                <div className="lg:col-span-1 space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-lg">Model Parameters</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label>Temperature: {config.parameters.temperature}</Label>
                                <div className="flex items-center space-x-2">
                                    <span className="text-xs text-gray-500">Precise</span>
                                    <Slider
                                        value={[config.parameters.temperature]}
                                        onValueChange={([val]) => updateParameter('temperature', val)}
                                        min={0}
                                        max={2}
                                        step={0.1}
                                        className="flex-1"
                                    />
                                    <span className="text-xs text-gray-500">Creative</span>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label>Max Tokens</Label>
                                <Input
                                    type="number"
                                    value={config.parameters.maxTokens}
                                    onChange={(e) => updateParameter('maxTokens', parseInt(e.target.value))}
                                />
                            </div>

                            <div className="space-y-2">
                                <div className="flex justify-between">
                                    <Label>Top P</Label>
                                    <span className="text-xs text-gray-500">{config.parameters.topP}</span>
                                </div>
                                <Slider
                                    value={[config.parameters.topP]}
                                    onValueChange={([val]) => updateParameter('topP', val)}
                                    min={0}
                                    max={1}
                                    step={0.01}
                                />
                            </div>

                            <div className="space-y-2">
                                <div className="flex justify-between">
                                    <Label>Frequency Penalty</Label>
                                    <span className="text-xs text-gray-500">{config.parameters.frequencyPenalty}</span>
                                </div>
                                <Slider
                                    value={[config.parameters.frequencyPenalty]}
                                    onValueChange={([val]) => updateParameter('frequencyPenalty', val)}
                                    min={0}
                                    max={2}
                                    step={0.1}
                                />
                            </div>

                            <div className="space-y-2">
                                <div className="flex justify-between">
                                    <Label>Presence Penalty</Label>
                                    <span className="text-xs text-gray-500">{config.parameters.presencePenalty}</span>
                                </div>
                                <Slider
                                    value={[config.parameters.presencePenalty]}
                                    onValueChange={([val]) => updateParameter('presencePenalty', val)}
                                    min={0}
                                    max={2}
                                    step={0.1}
                                />
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Middle/Right Panel: Prompt & Simulation */}
                <div className="lg:col-span-2 space-y-6">
                    <Card className="h-full flex flex-col">
                        <CardHeader>
                            <CardTitle className="flex justify-between items-center">
                                <span>Prompt Engineering</span>
                                <Button size="sm" onClick={handleRunSimulation} disabled={isSimulating}>
                                    {isSimulating ? (
                                        <Sparkles className="w-4 h-4 mr-2 animate-spin" />
                                    ) : (
                                        <Play className="w-4 h-4 mr-2" />
                                    )}
                                    Run Simulation
                                </Button>
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="flex-1 space-y-4">
                            <div className="space-y-2">
                                <Label>System Prompt</Label>
                                <Textarea
                                    className="min-h-[150px] font-mono text-sm"
                                    value={config.parameters.systemPrompt}
                                    onChange={(e) => updateParameter('systemPrompt', e.target.value)}
                                    placeholder="Define the agent's persona and constraints..."
                                />
                            </div>

                            <div className="space-y-2">
                                <Label>Test Input</Label>
                                <Textarea
                                    className="min-h-[100px]"
                                    placeholder="Enter user input to test..."
                                    defaultValue={config.testScenarios[0].input}
                                />
                            </div>

                            {simulationResult && (
                                <div className="mt-4 p-4 bg-slate-50 border rounded-lg animate-in fade-in slide-in-from-bottom-2">
                                    <Label className="text-green-600 flex items-center mb-2">
                                        <CheckCircle className="w-4 h-4 mr-2" />
                                        Simulation Result
                                    </Label>
                                    <div className="prose prose-sm max-w-none">
                                        <pre className="whitespace-pre-wrap font-sans text-sm text-gray-700">
                                            {simulationResult}
                                        </pre>
                                    </div>
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
