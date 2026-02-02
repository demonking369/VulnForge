'use client';

import { AgentStatus } from '@/lib/types';
import { Network, GitBranch, Target } from 'lucide-react';

interface PlannerViewProps {
    status: AgentStatus;
}

export function PlannerView({ status }: PlannerViewProps) {
    return (
        <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
                <div className="p-3 bg-neuro-surface rounded-lg border border-neuro-border">
                    <div className="flex items-center gap-2 mb-2 text-neuro-text-secondary text-sm">
                        <Target className="w-4 h-4" />
                        Active Strategy
                    </div>
                    <p className="text-neuro-text-primary text-sm">
                        Depth-first network mapping with stealth optimization
                    </p>
                </div>

                <div className="p-3 bg-neuro-surface rounded-lg border border-neuro-border">
                    <div className="flex items-center gap-2 mb-2 text-neuro-text-secondary text-sm">
                        <Network className="w-4 h-4" />
                        Reasoning Depth
                    </div>
                    <div className="w-full bg-neuro-bg h-2 rounded-full overflow-hidden">
                        <div className="bg-blue-500 h-full w-[75%]" />
                    </div>
                </div>
            </div>

            <div className="space-y-2">
                <h4 className="text-sm font-medium text-neuro-text-primary flex items-center gap-2">
                    <GitBranch className="w-4 h-4" />
                    Execution Plan
                </h4>
                <div className="space-y-2 pl-2 border-l-2 border-neuro-border ml-2">
                    {[
                        { step: 'Initial Reconnaissance', status: 'completed' },
                        { step: 'Port Scanning & Fingerprinting', status: 'in-progress' },
                        { step: 'Vulnerability Assessment', status: 'pending' },
                        { step: 'Exploitation Feasibility', status: 'pending' }
                    ].map((item, i) => (
                        <div key={i} className="flex items-center gap-3 text-sm">
                            <div className={`w-2 h-2 rounded-full ${item.status === 'completed' ? 'bg-green-500' :
                                    item.status === 'in-progress' ? 'bg-blue-500 animate-pulse' :
                                        'bg-neuro-border'
                                }`} />
                            <span className={item.status === 'pending' ? 'text-neuro-text-muted' : 'text-neuro-text-primary'}>
                                {item.step}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
