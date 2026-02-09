'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
    Search,
    ShieldAlert,
    Database,
    Link as LinkIcon,
    FileText,
    Trash2,
    RefreshCw,
    Binary,
    Clock,
    Layers,
    Cpu
} from 'lucide-react';
import { toast } from 'sonner';

export default function GovernancePage() {
    const [searchQuery, setSearchQuery] = useState('');
    const [knowledgeChunks, setKnowledgeChunks] = useState<any[]>([]);
    const [isSearching, setIsSearching] = useState(false);

    // Mock data for demonstration
    const MOCK_CHUNKS = [
        { id: 1, content: "Pricing tier 'Starter' includes 1 managed WP site and basic analytics.", tenant_id: "global", agent_id: "billing_agent", created_at: "2024-06-20" },
        { id: 2, content: "Security policy requires 2FA for all Super Admin accounts.", tenant_id: "global", agent_id: "security_agent", created_at: "2024-06-21" },
        { id: 3, content: "Bizoholic brand site uses Roots Bedrock for WordPress management.", tenant_id: "bizoholic", agent_id: "cms_agent", created_at: "2024-06-22" },
    ];

    useEffect(() => {
        setKnowledgeChunks(MOCK_CHUNKS);
    }, []);

    const handleSearch = async () => {
        setIsSearching(true);
        // In a real implementation, call /api/rag/search
        setTimeout(() => {
            setIsSearching(false);
            toast.success("RAG Hybrid Search completed");
        }, 800);
    };

    return (
        <div className="p-6 space-y-6 max-w-7xl mx-auto">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold flex items-center gap-2">
                        <ShieldAlert className="w-8 h-8 text-indigo-600" />
                        AI Governance & Knowledge Base
                    </h1>
                    <p className="text-muted-foreground">Manage agent long-term memory, knowledge chunks, and RAG metadata.</p>
                </div>
                <div className="flex items-center gap-3">
                    <Button variant="outline" className="gap-2">
                        <RefreshCw className="w-4 h-4" />
                        Re-index Vector DB
                    </Button>
                    <Button className="bg-indigo-600 hover:bg-indigo-700 gap-2">
                        <Database className="w-4 h-4" />
                        Add Knowledge
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium flex items-center gap-2">
                            <Binary className="w-4 h-4 text-indigo-500" />
                            Total Embeddings
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">12,482</div>
                        <p className="text-xs text-muted-foreground">+420 added this week</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium flex items-center gap-2">
                            <Layers className="w-4 h-4 text-green-500" />
                            Vector Dimensions
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">1536</div>
                        <p className="text-xs text-muted-foreground">text-embedding-3-small</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium flex items-center gap-2">
                            <Cpu className="w-4 h-4 text-purple-500" />
                            Agent Citations
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">89%</div>
                        <p className="text-xs text-muted-foreground">Knowledge retrieval accuracy</p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Knowledge Search</CardTitle>
                    <CardDescription>Perform hybrid vector + metadata search across the platform's knowledge base.</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex gap-2">
                        <div className="relative flex-1">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search knowledge base (e.g. 'WordPress provisioning policies')..."
                                className="pl-9"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                            />
                        </div>
                        <Button onClick={handleSearch} disabled={isSearching}>
                            {isSearching ? <RefreshCw className="w-4 h-4 animate-spin mr-2" /> : <Search className="w-4 h-4 mr-2" />}
                            Hybrid Search
                        </Button>
                    </div>

                    <div className="mt-8 space-y-4">
                        {knowledgeChunks.map((chunk) => (
                            <div key={chunk.id} className="p-4 rounded-lg border bg-slate-50 relative group">
                                <div className="flex justify-between items-start mb-2">
                                    <div className="flex gap-2">
                                        <Badge variant="secondary" className="bg-indigo-100 text-indigo-700">{chunk.agent_id}</Badge>
                                        <Badge variant="outline">{chunk.tenant_id}</Badge>
                                    </div>
                                    <div className="opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">
                                        <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400">
                                            <FileText className="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="icon" className="h-8 w-8 text-red-400">
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>
                                <p className="text-sm font-medium text-slate-800">{chunk.content}</p>
                                <div className="mt-2 flex items-center text-[10px] text-slate-400 gap-4">
                                    <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {chunk.created_at}</span>
                                    <span className="flex items-center gap-1"><LinkIcon className="w-3 h-3" /> UUID: {chunk.id}000-xxxx</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
