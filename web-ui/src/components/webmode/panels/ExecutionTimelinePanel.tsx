'use client';

import { Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

const TIMELINE = [
    { id: 1, label: 'Boot Sequence', status: 'complete', time: '0ms' },
    { id: 2, label: 'Bus Sync', status: 'complete', time: '200ms' },
    { id: 3, label: 'Agent Registration', status: 'complete', time: '450ms' },
    { id: 4, label: 'Policy Lattice Compile', status: 'active', time: '800ms' },
    { id: 5, label: 'Intent Router Online', status: 'pending', time: '—' },
];

export function ExecutionTimelinePanel() {
    return (
        <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-neuro-text-muted">
                <Clock className="w-4 h-4 text-amber-300" />
                Execution Timeline
            </div>
            <div className="space-y-1">
                {TIMELINE.map(step => (
                    <div key={step.id} className="flex items-center gap-3 px-3 py-2 rounded-lg">
                        <div className={cn("w-2 h-2 rounded-full", step.status === 'complete' ? 'bg-emerald-400' : step.status === 'active' ? 'bg-cyan-400 animate-pulse' : 'bg-neuro-border/40')} />
                        <span className={cn("text-xs flex-1", step.status === 'pending' ? 'text-neuro-text-muted' : 'text-neuro-text-secondary')}>{step.label}</span>
                        <span className="text-[9px] font-mono text-neuro-text-muted">{step.time}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}
