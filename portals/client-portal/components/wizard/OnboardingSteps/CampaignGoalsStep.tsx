import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { CampaignGoals } from '../types/onboarding';
import { Target, Users, ShoppingBag, Radio } from 'lucide-react';

interface Props {
    data: CampaignGoals;
    onUpdate: (data: Partial<CampaignGoals>) => void;
}

const GOALS = [
    { id: 'lead_gen', label: 'Lead Generation', desc: 'Get more signups & inquiries', icon: Users },
    { id: 'brand_awareness', label: 'Brand Awareness', desc: 'Reach more people', icon: Radio },
    { id: 'ecommerce_sales', label: 'Drive Sales', desc: 'Increase online orders', icon: ShoppingBag },
    { id: 'app_installs', label: 'App Installs', desc: 'Get more users', icon: Target },
];

export function CampaignGoalsStep({ data, onUpdate }: Props) {
    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Campaign Goals</h2>
                <p className="text-gray-500">What does success look like?</p>
            </div>

            <div className="space-y-4">
                <Label>Primary Objective</Label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {GOALS.map((goal) => (
                        <div
                            key={goal.id}
                            onClick={() => onUpdate({ primaryGoal: goal.id as any })}
                            className={`
                cursor-pointer p-4 rounded-xl border transition-all
                ${data.primaryGoal === goal.id
                                    ? 'border-blue-500 bg-blue-50 ring-1 ring-blue-500'
                                    : 'border-gray-200 hover:border-blue-200'
                                }
              `}
                        >
                            <div className="flex items-center gap-3">
                                <div className={`p-2 rounded-lg ${data.primaryGoal === goal.id ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'}`}>
                                    <goal.icon size={20} />
                                </div>
                                <div>
                                    <h4 className="font-semibold text-sm">{goal.label}</h4>
                                    <p className="text-xs text-gray-500">{goal.desc}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="space-y-4 pt-4 border-t">
                <div className="flex justify-between">
                    <Label>Monthly Ad Budget</Label>
                    <span className="text-sm font-semibold text-blue-700">
                        {data.currency} {data.monthlyBudget.toLocaleString()}
                    </span>
                </div>
                <Slider
                    value={[data.monthlyBudget]}
                    min={100}
                    max={50000}
                    step={100}
                    onValueChange={(val) => onUpdate({ monthlyBudget: val[0] })}
                    className="py-4"
                />
                <div className="flex justify-between text-xs text-gray-400">
                    <span>$100</span>
                    <span>$50,000+</span>
                </div>
            </div>

            <div className="space-y-4 pt-4 border-t">
                <Label>Target Audience</Label>
                <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label className="text-xs text-gray-500">Age Range</Label>
                        <Select
                            value={data.targetAudience.ageRange}
                            onValueChange={(val) => onUpdate({ targetAudience: { ...data.targetAudience, ageRange: val } })}
                        >
                            <SelectTrigger>
                                <SelectValue placeholder="Age" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="18-24">18-24</SelectItem>
                                <SelectItem value="25-34">25-34</SelectItem>
                                <SelectItem value="35-44">35-44</SelectItem>
                                <SelectItem value="45-54">45-54</SelectItem>
                                <SelectItem value="55+">55+</SelectItem>
                                <SelectItem value="all">All Ages</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="space-y-2">
                        <Label className="text-xs text-gray-500">Location</Label>
                        <Input
                            placeholder="Region / Country"
                            onChange={(e) => onUpdate({ targetAudience: { ...data.targetAudience, locations: [e.target.value] } })}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}
