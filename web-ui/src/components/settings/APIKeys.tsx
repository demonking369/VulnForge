'use client';

import { Label } from '@/components/ui/label';
import { Key, Eye, EyeOff } from 'lucide-react';
import { useState } from 'react';

export function APIKeys() {
    const [showKeys, setShowKeys] = useState<Record<string, boolean>>({});

    const toggleVisibility = (key: string) => {
        setShowKeys(prev => ({ ...prev, [key]: !prev[key] }));
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
                <Key className="w-5 h-5 text-neuro-primary" />
                <h2 className="text-lg font-semibold text-neuro-text-primary">API Integrations</h2>
            </div>

            <div className="space-y-5">
                <div className="grid gap-2">
                    <Label>OpenAI API Key</Label>
                    <div className="relative">
                        <input
                            type={showKeys['openai'] ? 'text' : 'password'}
                            placeholder="sk-..."
                            className="w-full bg-neuro-bg border border-neuro-border rounded-md px-3 py-2 pr-10 text-sm text-neuro-text-primary focus:outline-none focus:ring-1 focus:ring-neuro-primary"
                        />
                        <button
                            onClick={() => toggleVisibility('openai')}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-neuro-text-muted hover:text-neuro-primary"
                        >
                            {showKeys['openai'] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                    </div>
                </div>

                <div className="grid gap-2">
                    <Label>Anthropic API Key</Label>
                    <div className="relative">
                        <input
                            type={showKeys['anthropic'] ? 'text' : 'password'}
                            placeholder="sk-ant-..."
                            className="w-full bg-neuro-bg border border-neuro-border rounded-md px-3 py-2 pr-10 text-sm text-neuro-text-primary focus:outline-none focus:ring-1 focus:ring-neuro-primary"
                        />
                        <button
                            onClick={() => toggleVisibility('anthropic')}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-neuro-text-muted hover:text-neuro-primary"
                        >
                            {showKeys['anthropic'] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                    </div>
                </div>

                <div className="grid gap-2">
                    <Label>Shodan API Key</Label>
                    <div className="relative">
                        <input
                            type={showKeys['shodan'] ? 'text' : 'password'}
                            placeholder="Enter Shodan API Key"
                            className="w-full bg-neuro-bg border border-neuro-border rounded-md px-3 py-2 pr-10 text-sm text-neuro-text-primary focus:outline-none focus:ring-1 focus:ring-neuro-primary"
                        />
                        <button
                            onClick={() => toggleVisibility('shodan')}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-neuro-text-muted hover:text-neuro-primary"
                        >
                            {showKeys['shodan'] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
