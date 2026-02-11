'use client';

import { useState, useEffect } from 'react';
import { Brain, TrendingUp, TrendingDown, Minus, AlertTriangle } from 'lucide-react';
import { useWebModeContext } from '@/components/webmode/WebModeProvider';
import { cn } from '@/lib/utils';

interface MemoryDisplay {
    id: string;
    label: string;
    value: number;
    trend: 'up' | 'down' | 'stable';
    type: string;
    decayRate: number;
    barColor: string;
    icon: string;
}

const DEFAULT_METRICS: MemoryDisplay[] = [
    { id: 'episodic', label: 'Episodic Memory', value: 0.72, trend: 'down', type: 'episodic', decayRate: 0.03, barColor: 'bg-gradient-to-r from-violet-500 to-fuchsia-500', icon: '🧠' },
    { id: 'working', label: 'Working Context', value: 0.89, trend: 'up', type: 'preference', decayRate: 0.01, barColor: 'bg-gradient-to-r from-cyan-400 to-blue-500', icon: '⚡' },
    { id: 'prefs', label: 'Preferences', value: 0.45, trend: 'stable', type: 'reinforcement', decayRate: 0.005, barColor: 'bg-gradient-to-r from-emerald-500 to-teal-400', icon: '🎯' },
];

const TrendIcon = ({ trend }: { trend: string }) => {
    if (trend === 'up') return <TrendingUp className="w-3 h-3 text-emerald-400" />;
    if (trend === 'down') return <TrendingDown className="w-3 h-3 text-rose-400" />;
    return <Minus className="w-3 h-3 text-neutral-400" />;
};

export function MemoryPulsePanel() {
    const { config } = useWebModeContext();
    const [metrics, setMetrics] = useState<MemoryDisplay[]>(DEFAULT_METRICS);
    const [cadence, setCadence] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setMetrics(prev => prev.map(m => ({
                ...m,
                value: Math.max(0.05, Math.min(0.99, m.value + (Math.random() - 0.52) * m.decayRate * 2)),
            })));
            setCadence(p => (p + 1) % 4);
        }, 2500);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-neuro-text-muted">
                    <Brain className="w-4 h-4 text-fuchsia-300" />
                    Memory Pulse
                </div>
                <div className="flex gap-1">
                    {[0, 1, 2, 3].map(i => (
                        <div key={i} className={cn("w-1.5 h-3 rounded-full transition-all duration-300", i === cadence ? "bg-cyan-400 shadow-[0_0_6px_cyan]" : "bg-neuro-border/50")} />
                    ))}
                </div>
            </div>

            <div className="space-y-3">
                {metrics.map(metric => (
                    <div key={metric.id} className="group rounded-xl bg-neuro-bg/60 border border-neuro-border/60 p-3 hover:border-fuchsia-500/30 transition-colors">
                        <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                                <span className="text-sm">{metric.icon}</span>
                                <span className="text-xs text-neuro-text-secondary uppercase tracking-wider">{metric.label}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <TrendIcon trend={metric.trend} />
                                <span className="text-xs font-mono text-neuro-text-primary">{Math.round(metric.value * 100)}%</span>
                            </div>
                        </div>

                        {/* Progress Bar */}
                        <div className="relative h-2 bg-neuro-surface rounded-full overflow-hidden">
                            <div className={cn("absolute top-0 left-0 h-full transition-all duration-1000 ease-out shadow-[0_0_10px_rgba(0,0,0,0.5)]", metric.barColor)} style={{ width: `${metric.value * 100}%` }}>
                                <div className="absolute top-0 right-0 bottom-0 w-[1px] bg-white/50 shadow-[0_0_5px_white]" />
                            </div>
                        </div>

                        {/* Details on hover */}
                        <div className="max-h-0 overflow-hidden group-hover:max-h-12 transition-all duration-300">
                            <div className="flex justify-between text-[9px] text-neuro-text-muted mt-2">
                                <span>Decay: {(metric.decayRate * 100).toFixed(1)}%/cycle</span>
                                {metric.value > 0.85 && (
                                    <span className="flex items-center gap-1 text-amber-400"><AlertTriangle className="w-2.5 h-2.5" /> High Influence</span>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
