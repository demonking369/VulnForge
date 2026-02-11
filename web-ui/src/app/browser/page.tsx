'use client';

import { useState, useEffect } from 'react';
import { useNeuroRift } from '@/lib/hooks';
import { getWebSocket } from '@/lib/websocket';
import { LiveView } from '@/components/browser/LiveView';
import { ActionControls } from '@/components/browser/ActionControls';
import { StepExecutor } from '@/components/browser/StepExecutor';
import { Globe, Shield } from 'lucide-react';

export default function BrowserPage() {
    const { session, browserActive } = useNeuroRift();
    const [url, setUrl] = useState<string | null>(null);
    const [steps, setSteps] = useState<any[]>([]);
    const [executionStatus, setExecutionStatus] = useState<'idle' | 'running' | 'paused' | 'error'>('idle');

    // WebSocket listeners would go here to update state
    useEffect(() => {
        // Mock initial state
        if (!browserActive) {
            setSteps([
                { action: 'Navigate to target', status: 'pending' },
                { action: 'Wait for login form', status: 'pending' },
                { action: 'Check for CSRF token', status: 'pending' }
            ]);
        }
    }, [browserActive]);

    const handleAction = (action: string, params: any) => {
        const ws = getWebSocket();
        ws.send({
            type: 'queue_task',
            tool_name: 'browser_action',
            target: url || 'current',
            args: { action, ...params }
        });
    };

    return (
        <div className="p-6 h-[calc(100vh-4rem)] flex flex-col gap-6">
            <div className="flex items-center justify-between shrink-0">
                <div>
                    <h1 className="text-3xl font-bold text-neuro-text-primary">Browser Automation</h1>
                    <p className="text-neuro-text-secondary mt-1">Live browser control and interaction</p>
                </div>

                <div className="flex items-center gap-3">
                    <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border ${browserActive
                            ? 'bg-green-500/10 border-green-500/30 text-green-400'
                            : 'bg-neuro-surface border-neuro-border text-neuro-text-muted'
                        }`}>
                        <Globe className="w-3 h-3" />
                        {browserActive ? 'Connected' : 'Disconnected'}
                    </div>
                    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium bg-neuro-surface border border-neuro-border text-neuro-text-secondary">
                        <Shield className="w-3 h-3" />
                        Safe Mode Active
                    </div>
                </div>
            </div>

            <div className="flex-1 grid grid-cols-12 gap-6 min-h-0">
                {/* Main View - 8 cols */}
                <div className="col-span-12 lg:col-span-8 flex flex-col gap-4 min-h-0">
                    <div className="flex-1 min-h-0">
                        <LiveView
                            url={url}
                            isActive={browserActive}
                        />
                    </div>
                    <div className="h-auto shrink-0">
                        <ActionControls
                            onAction={handleAction}
                            disabled={!browserActive}
                        />
                    </div>
                </div>

                {/* Sidebar - 4 cols */}
                <div className="col-span-12 lg:col-span-4 flex flex-col min-h-0">
                    <StepExecutor
                        steps={steps}
                        currentStep={0}
                        status={executionStatus}
                        onPlay={() => setExecutionStatus('running')}
                        onPause={() => setExecutionStatus('paused')}
                        onStep={() => { }}
                    />
                </div>
            </div>
        </div>
    );
}
