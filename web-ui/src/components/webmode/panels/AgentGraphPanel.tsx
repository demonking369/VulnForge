'use client';

import { useState } from 'react';
import { Cpu, GitBranch, Eye } from 'lucide-react';
import { useWebModeContext } from '@/components/webmode/WebModeProvider';
import { cn } from '@/lib/utils';

const NODE_POSITIONS: Record<string, { x: number; y: number }> = {
    planner: { x: 20, y: 20 },
    operator: { x: 70, y: 15 },
    analyst: { x: 75, y: 70 },
    scribe: { x: 25, y: 75 },
};

const AGENT_ICONS: Record<string, React.ComponentType<any>> = {
    planner: Cpu,
    operator: GitBranch,
    analyst: Eye,
    scribe: Cpu,
};

const STATUS_COLORS: Record<string, string> = {
    idle: 'border-neutral-600 bg-neutral-800/60',
    planning: 'border-cyan-400/60 bg-cyan-900/30',
    executing: 'border-emerald-400/60 bg-emerald-900/30',
    analyzing: 'border-amber-400/60 bg-amber-900/30',
    error: 'border-rose-400/60 bg-rose-900/30',
};

const PULSE_COLORS: Record<string, string> = {
    idle: 'bg-neutral-500',
    planning: 'bg-cyan-400',
    executing: 'bg-emerald-400',
    analyzing: 'bg-amber-400',
    error: 'bg-rose-500',
};

export function AgentGraphPanel() {
    const { agentState } = useWebModeContext();
    const [hoveredAgent, setHoveredAgent] = useState<string | null>(null);

    const agents = Object.values(agentState);

    return (
        <div className="space-y-4">
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-neuro-text-muted">
                <GitBranch className="w-4 h-4 text-violet-300" />
                Agent Dependency Graph
            </div>

            <div className="relative w-full h-64 rounded-xl bg-neuro-bg/60 border border-neuro-border/60 overflow-hidden">
                {/* SVG Connections */}
                <svg className="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg">
                    {agents.map(agent =>
                        agent.dependencies?.map((depId: string) => {
                            const from = NODE_POSITIONS[depId];
                            const to = NODE_POSITIONS[agent.id];
                            if (!from || !to) return null;
                            return (
                                <line key={`${depId}-${agent.id}`} x1={`${from.x}%`} y1={`${from.y}%`} x2={`${to.x}%`} y2={`${to.y}%`} stroke="rgba(100, 116, 139, 0.25)" strokeWidth="1" strokeDasharray="4 4" />
                            );
                        })
                    )}
                </svg>

                {/* Agent Nodes */}
                {agents.map(agent => {
                    const pos = NODE_POSITIONS[agent.id];
                    if (!pos) return null;
                    const IconComponent = AGENT_ICONS[agent.id] || Cpu;
                    return (
                        <div
                            key={agent.id}
                            style={{ left: `${pos.x}%`, top: `${pos.y}%` }}
                            className="absolute -translate-x-1/2 -translate-y-1/2 group cursor-pointer"
                            onMouseEnter={() => setHoveredAgent(agent.id)}
                            onMouseLeave={() => setHoveredAgent(null)}
                        >
                            <div className={cn("relative w-10 h-10 rounded-lg border flex items-center justify-center transition-all", STATUS_COLORS[agent.status] || STATUS_COLORS.idle, hoveredAgent === agent.id && "scale-110 shadow-lg")}>
                                <IconComponent className="w-4 h-4 text-neuro-text-primary" />
                                <div className={cn("absolute -top-0.5 -right-0.5 w-2.5 h-2.5 rounded-full border border-black/50", PULSE_COLORS[agent.status] || PULSE_COLORS.idle, agent.status !== 'idle' && "animate-pulse")} />
                            </div>
                            <div className="text-[9px] text-center mt-1 text-neuro-text-muted uppercase tracking-wider whitespace-nowrap">{agent.name}</div>

                            {/* Introspection Card */}
                            <div className={cn("absolute bottom-full left-1/2 -translate-x-1/2 mb-2 p-3 rounded-lg bg-black/90 border border-neuro-border/60 backdrop-blur w-48 transition-all pointer-events-none z-20", hoveredAgent === agent.id ? "opacity-100 scale-100" : "opacity-0 scale-95")}>
                                <div className="text-[10px] text-cyan-300 uppercase tracking-wider mb-1">{agent.role}</div>
                                <div className="text-xs text-neuro-text-primary mb-2">{agent.name}</div>
                                <div className="space-y-1 text-[10px] text-neuro-text-secondary">
                                    <div className="flex justify-between"><span>State</span><span className="text-neuro-text-primary">{agent.status}</span></div>
                                    <div className="flex justify-between"><span>Load</span><span className="text-neuro-text-primary">{Math.round(agent.load * 100)}%</span></div>
                                    <div className="flex justify-between"><span>Task</span><span className="text-neuro-text-primary truncate max-w-[100px]">{agent.currentTask || 'Standby'}</span></div>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Legend */}
            <div className="flex flex-wrap gap-2 text-[9px] text-neuro-text-muted mt-2">
                {Object.entries(PULSE_COLORS).map(([status, color]) => (
                    <span key={status} className="flex items-center gap-1"><span className={cn("w-1.5 h-1.5 rounded-full", color)} />{status}</span>
                ))}
            </div>
        </div>
    );
}
