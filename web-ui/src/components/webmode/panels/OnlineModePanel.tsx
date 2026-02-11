'use client';

import { useEffect, useState } from 'react';
import { Globe, ShieldAlert, ShieldCheck } from 'lucide-react';
import { useWebModeContext } from '@/components/webmode/WebModeProvider';
import { cn } from '@/lib/utils';

export function OnlineModePanel() {
    const { config, updateConfig, controlMode } = useWebModeContext();
    const [latency, setLatency] = useState(12);

    useEffect(() => {
        if (!config.onlineMode.enabled) return;
        const interval = setInterval(() => {
            setLatency((prev: number) => Math.max(8, Math.min(45, prev + (Math.random() - 0.5) * 5)));
        }, 2000);
        return () => clearInterval(interval);
    }, [config.onlineMode.enabled]);

    return (
        <div className="space-y-4">
            {/* Header Toggle */}
            <div className="flex items-center justify-between p-3 rounded-xl border border-neuro-border/40 bg-neuro-bg/40">
                <div className="flex items-center gap-3">
                    <div className={cn("p-2 rounded-lg", config.onlineMode.enabled ? "bg-emerald-500/20 text-emerald-400" : "bg-neuro-surface/60 text-neuro-text-muted")}>
                        <Globe className="w-5 h-5" />
                    </div>
                    <div>
                        <div className="text-xs uppercase tracking-[0.2em] font-bold text-neuro-text-primary">Secure Tunnel</div>
                        <div className="text-[10px] text-neuro-text-secondary">{config.onlineMode.enabled ? 'Encrypted Link Active' : 'Offline / Isolated'}</div>
                    </div>
                </div>
                <button onClick={() => updateConfig('onlineMode.enabled', !config.onlineMode.enabled)} disabled={controlMode === 'read'} className={cn("relative w-12 h-6 rounded-full transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-cyan-500/50", config.onlineMode.enabled ? "bg-emerald-500/30 border border-emerald-500/50" : "bg-neuro-surface border border-neuro-border/60")}>
                    <div className={cn("absolute top-0.5 left-0.5 w-4 h-4 rounded-full transition-transform duration-300 shadow-md", config.onlineMode.enabled ? "translate-x-6 bg-emerald-400" : "bg-neuro-text-muted")} />
                </button>
            </div>

            {config.onlineMode.enabled && (
                <div className="space-y-4">
                    {/* Tunnel Visualization */}
                    <div className="relative h-24 rounded-xl bg-black/40 border border-neuro-border/30 p-4 flex items-center justify-between overflow-hidden">
                        <div className="z-10 flex flex-col items-center gap-1">
                            <div className="w-8 h-8 rounded-lg bg-cyan-900/30 border border-cyan-500/30 flex items-center justify-center">
                                <ShieldCheck className="w-4 h-4 text-cyan-400" />
                            </div>
                            <span className="text-[9px] uppercase tracking-wider text-cyan-200">Local</span>
                        </div>

                        <div className="flex-1 px-4 relative h-0.5 bg-neuro-border/30">
                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 px-2 py-0.5 bg-black rounded text-[9px] text-emerald-400 border border-emerald-500/20 font-mono">
                                AES-256 • {Math.round(latency)}ms
                            </div>
                        </div>

                        <div className="z-10 flex flex-col items-center gap-1">
                            <div className="w-8 h-8 rounded-lg bg-emerald-900/30 border border-emerald-500/30 flex items-center justify-center animate-pulse">
                                <Globe className="w-4 h-4 text-emerald-400" />
                            </div>
                            <span className="text-[9px] uppercase tracking-wider text-emerald-200">Remote</span>
                        </div>
                    </div>

                    {/* Scopes & Access */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div className="rounded-xl border border-neuro-border/40 bg-neuro-bg/40 p-3 space-y-2">
                            <div className="text-[10px] uppercase tracking-wider text-neuro-text-muted mb-2">Exposure Scopes</div>
                            {['API Access', 'Chat Interface', 'Full Dashboard'].map(scope => (
                                <div key={scope} className="flex items-center justify-between p-2 rounded bg-black/20 border border-neuro-border/20">
                                    <span className="text-xs text-neuro-text-secondary">{scope}</span>
                                    <div className={cn("w-2 h-2 rounded-full", scope === 'Chat Interface' ? "bg-emerald-500 shadow-[0_0_5px_rgba(16,185,129,0.5)]" : "bg-neutral-700")} />
                                </div>
                            ))}
                        </div>
                        <div className="rounded-xl border border-neuro-border/40 bg-neuro-bg/40 p-3 space-y-3">
                            <div className="text-[10px] uppercase tracking-wider text-neuro-text-muted">Access Policy</div>
                            <select value={config.onlineMode.access} onChange={e => updateConfig('onlineMode.access', e.target.value)} disabled={controlMode === 'read'} className="w-full rounded-lg border border-neuro-border/60 bg-black/20 px-3 py-2 text-xs text-neuro-text-primary focus:border-cyan-500/50 outline-none">
                                <option value="read">Read-only (Safe)</option>
                                <option value="control">Control (Auth Req)</option>
                            </select>
                            <div className="flex items-start gap-2 p-2 rounded bg-rose-950/20 border border-rose-500/20">
                                <ShieldAlert className="w-3.5 h-3.5 text-rose-400 mt-0.5" />
                                <span className="text-[10px] text-rose-200/80 leading-tight">MFA enforcement recommended for remote admin sessions.</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
