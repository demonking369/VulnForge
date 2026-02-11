'use client';

<<<<<<< HEAD
import { Activity } from 'lucide-react';
import { cn } from '@/lib/utils';

const EVENTS = [
    { id: 1, text: 'Agent "planner" transitioned to idle', time: '2s ago', type: 'info' },
    { id: 2, text: 'Policy lattice compiled (0 conflicts)', time: '5s ago', type: 'success' },
    { id: 3, text: 'Memory decay cycle completed', time: '8s ago', type: 'info' },
];

export function ActivityStreamPanel() {
    return (
        <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-neuro-text-muted">
                <Activity className="w-4 h-4 text-cyan-300" />
                Activity Stream
            </div>
            <div className="space-y-2">
                {EVENTS.map(ev => (
                    <div key={ev.id} className="flex items-center gap-3 px-3 py-2 rounded-lg bg-neuro-bg/60 border border-neuro-border/40">
                        <div className={cn("w-1.5 h-1.5 rounded-full", ev.type === 'success' ? 'bg-emerald-400' : 'bg-cyan-400')} />
                        <span className="text-xs text-neuro-text-secondary flex-1">{ev.text}</span>
                        <span className="text-[9px] text-neuro-text-muted">{ev.time}</span>
                    </div>
                ))}
            </div>
=======
import { useSignalStream } from '@/lib/webmode/stream';
import { cn } from '@/lib/utils';

export function ActivityStreamPanel() {
    const events = useSignalStream();

    return (
        <div className="space-y-3 max-h-[320px] overflow-y-auto pr-2">
            {events.map(event => (
                <div
                    key={event.id}
                    className={cn(
                        'rounded-lg border px-3 py-2 text-xs',
                        event.tone === 'warning'
                            ? 'border-rose-400/40 bg-rose-500/10 text-rose-100'
                            : 'border-neuro-border/60 bg-neuro-bg/60 text-neuro-text-secondary'
                    )}
                >
                    <div className="flex items-center justify-between text-[10px] uppercase tracking-[0.3em] text-neuro-text-muted">
                        <span>{event.time}</span>
                        <span>{event.tone}</span>
                    </div>
                    <p className="mt-2 text-sm text-neuro-text-primary">{event.label}</p>
                </div>
            ))}
>>>>>>> main
        </div>
    );
}
