'use client';

import { AgentType, AgentStatus } from '@/lib/types';
import { cn } from '@/lib/utils';
import { Activity, Brain, Clock, Terminal, ChevronRight } from 'lucide-react';

interface AgentPanelProps {
    agent: AgentType;
    status: AgentStatus;
    isActive: boolean;
    onClick: () => void;
    children?: React.ReactNode;
}

const AGENT_COLORS = {
    Planner: 'text-blue-400',
    Operator: 'text-red-400',
    Navigator: 'text-green-400',
    Analyst: 'text-yellow-400',
    Scribe: 'text-purple-400'
};

const AGENT_DESCRIPTIONS = {
    Planner: 'Strategic reasoning & task decomposition',
    Operator: 'Tool execution & command handling',
    Navigator: 'Browser automation & web interaction',
    Analyst: 'Data correlation & vulnerability analysis',
    Scribe: 'Documentation & reporting'
};

export function AgentPanel({ agent, status, isActive, onClick, children }: AgentPanelProps) {
    return (
        <div
            className={cn(
                "glass-card transition-all duration-300 overflow-hidden",
                isActive ? "ring-1 ring-neuro-primary shadow-lg shadow-neuro-primary/10" : "hover:bg-neuro-surface/50 cursor-pointer"
            )}
            onClick={!isActive ? onClick : undefined}
        >
            <div className="p-4">
                <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                        <div className={cn(
                            "p-2 rounded-lg bg-neuro-bg/50",
                            AGENT_COLORS[agent as keyof typeof AGENT_COLORS]
                        )}>
                            <Brain className="w-5 h-5" />
                        </div>
                        <div>
                            <h3 className="font-semibold text-neuro-text-primary">{agent}</h3>
                            <p className="text-xs text-neuro-text-secondary">{AGENT_DESCRIPTIONS[agent as keyof typeof AGENT_DESCRIPTIONS]}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3">
                        <div className={cn(
                            "px-2 py-1 rounded-full text-xs font-medium border",
                            status?.state === 'executing' ? "bg-green-500/10 border-green-500/30 text-green-400" :
                                status?.state === 'planning' ? "bg-blue-500/10 border-blue-500/30 text-blue-400" :
                                    status?.state === 'error' ? "bg-red-500/10 border-red-500/30 text-red-400" :
                                        "bg-neuro-surface border-neuro-border text-neuro-text-muted"
                        )}>
                            {status?.state || 'offline'}
                        </div>
                    </div>
                </div>

                <div className="space-y-3">
                    {status?.current_task && (
                        <div className="p-3 rounded-md bg-neuro-bg/30 border border-neuro-border/50">
                            <div className="flex items-center gap-2 text-xs text-neuro-text-muted mb-1">
                                <Activity className="w-3 h-3" />
                                Current Activity
                            </div>
                            <p className="text-sm text-neuro-text-primary line-clamp-2">
                                {status.current_task}
                            </p>
                        </div>
                    )}

                    <div className="flex items-center gap-4 text-xs text-neuro-text-muted">
                        <div className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            Last active: {status ? new Date(status.last_update).toLocaleTimeString() : 'Never'}
                        </div>
                    </div>
                </div>
            </div>

            {isActive && children && (
                <div className="border-t border-neuro-border bg-neuro-bg/20 p-4 animate-in slide-in-from-top-2">
                    {children}
                </div>
            )}
        </div>
    );
}
