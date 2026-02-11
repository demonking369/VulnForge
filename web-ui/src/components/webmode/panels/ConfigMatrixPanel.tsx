'use client';

import { useMemo } from 'react';
import { useWebModeContext } from '@/components/webmode/WebModeProvider';
import { configSchema } from '@/lib/webmode/config-schema';
import { AlertTriangle, Lock, RefreshCw } from 'lucide-react';
import { cn } from '@/lib/utils';

function getValue(source: any, path: string) {
    if (!source) return undefined;
    return path.split('.').reduce((acc: any, key: string) => (acc ? acc[key] : undefined), source);
}

export function ConfigMatrixPanel() {
    const { config, updateConfig, controlMode } = useWebModeContext();

    const conflicts = useMemo(() => {
        const list: string[] = [];
        if (config.stealth?.enabled && config.neurorift?.sandboxLevel === 'hardened') {
            list.push('Warning: Stealth Mode optimal with Sealed sandbox (currently Hardened).');
        }
        if (config.aiBehavior?.selfEvolution && config.agentModes?.supervision === 'strict') {
            list.push('Constraint: Self-Evolution dampened by Strict supervision.');
        }
        return list;
    }, [config]);

    const sections = useMemo(() => configSchema, []);

    return (
        <div className="space-y-6">
            {conflicts.length > 0 && (
                <div className="p-3 rounded-xl bg-amber-950/30 border border-amber-500/30 animate-pulse">
                    <div className="flex items-center gap-2 mb-2 text-amber-400">
                        <AlertTriangle className="w-4 h-4" />
                        <span className="text-[10px] uppercase tracking-widest font-bold">Policy Conflicts Detected</span>
                    </div>
                    {conflicts.map((c, i) => (
                        <div key={i} className="text-[10px] text-amber-200/80 ml-6 list-disc list-item">{c}</div>
                    ))}
                </div>
            )}

            {sections.map(section => (
                <div key={section.id} className="group rounded-xl border border-neuro-border/60 bg-neuro-bg/60 p-4 hover:border-cyan-500/30 transition-colors">
                    <div className="mb-4 flex items-start justify-between">
                        <div>
                            <h4 className="text-xs uppercase tracking-[0.4em] text-neuro-text-muted">{section.title}</h4>
                            <p className="text-[10px] text-neuro-text-secondary mt-1 max-w-[90%]">{section.description}</p>
                        </div>
                        {controlMode === 'read' && <Lock className="w-3 h-3 text-neuro-text-muted opacity-50" />}
                    </div>

                    <div className="space-y-5">
                        {section.fields.map(field => {
                            const value = getValue(config, field.path);
                            const isLocked = controlMode === 'read';
                            return (
                                <div key={field.path} className={cn("relative transition-opacity", isLocked && "opacity-60 pointer-events-none")}>
                                    <div className="flex items-center justify-between text-[10px] uppercase tracking-wider text-neuro-text-secondary mb-1.5">
                                        <span className="flex items-center gap-1.5">{field.label}{isLocked && <Lock className="w-2.5 h-2.5" />}</span>
                                        <span className="font-mono text-cyan-300">{typeof value === 'number' ? value.toFixed(2) : String(value)}</span>
                                    </div>

                                    {field.type === 'slider' && (
                                        <div className="relative h-4 flex items-center">
                                            <input type="range" min={field.min} max={field.max} step={field.step} value={value as number} onChange={e => updateConfig(field.path, Number(e.target.value))} disabled={isLocked} className="w-full h-1 bg-neuro-border/50 rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:bg-cyan-400 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:shadow-[0_0_10px_cyan]" />
                                            <div className="absolute inset-0 pointer-events-none opacity-20 bg-gradient-to-r from-emerald-500 via-amber-500 to-rose-500 rounded-full h-1 top-1.5 mix-blend-overlay" />
                                        </div>
                                    )}

                                    {field.type === 'toggle' && (
                                        <button onClick={() => updateConfig(field.path, !value)} disabled={isLocked} className={cn("w-full py-1.5 rounded border text-[10px] uppercase tracking-widest transition-all", value ? "bg-cyan-950/40 border-cyan-500/50 text-cyan-300 shadow-[0_0_10px_rgba(6,182,212,0.1)]" : "bg-black/20 border-neuro-border/30 text-neuro-text-muted hover:bg-white/5")}>{value ? 'Active' : 'Dormant'}</button>
                                    )}

                                    {field.type === 'select' && (
                                        <select value={value as string} onChange={e => updateConfig(field.path, e.target.value)} disabled={isLocked} className="w-full py-1.5 px-2 rounded bg-black/20 border border-neuro-border/30 text-[10px] text-neuro-text-primary focus:border-cyan-500/50 outline-none">
                                            {field.options?.map((opt: any) => (
                                                <option key={opt.value} value={opt.value}>{opt.label}</option>
                                            ))}
                                        </select>
                                    )}
                                </div>
                            );
                        })}
                    </div>

                    <div className="mt-4 pt-3 border-t border-neuro-border/20 flex items-center justify-between text-[9px] text-neuro-text-muted/60">
                        <span className="flex items-center gap-1"><RefreshCw className="w-2.5 h-2.5" /> Policy Compilation</span>
                        <span className="font-mono">HASH: {Math.random().toString(16).slice(2, 8).toUpperCase()}</span>
                    </div>
                </div>
            ))}
        </div>
    );
}
