'use client';

import { useNeuroRift } from '@/lib/hooks';
import { Activity, Save, Zap } from 'lucide-react';
import { cn } from '@/lib/utils';

export function TopCommandBar() {
    const { session, systemHealth, torConnected } = useNeuroRift();

    return (
        <header className="h-14 bg-neuro-surface border-b border-neuro-border flex items-center px-6 gap-6">
            {/* Logo */}
            <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-gradient-to-br from-neuro-primary to-purple-600 rounded-lg flex items-center justify-center">
                    <Zap className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-neuro-text-primary">NeuroRift</span>
            </div>

            {/* Session Info */}
            {session && (
                <>
                    <div className="flex items-center gap-2 px-3 py-1 bg-neuro-bg rounded-md border border-neuro-border">
                        <div className="w-2 h-2 bg-neuro-success rounded-full animate-pulse" />
                        <span className="text-sm text-neuro-text-primary">{session.name}</span>
                    </div>

                    <div
                        className={cn(
                            'px-3 py-1 rounded-md text-xs font-medium',
                            session.mode === 'OFFENSIVE'
                                ? 'bg-severity-critical/10 text-severity-critical border border-severity-critical/20'
                                : 'bg-neuro-primary/10 text-neuro-primary border border-neuro-primary/20'
                        )}
                    >
                        {session.mode}
                    </div>
                </>
            )}

            {/* Tor Status */}
            <div className="flex items-center gap-2 px-3 py-1 bg-neuro-bg rounded-md border border-neuro-border">
                <div className={cn('w-2 h-2 rounded-full', torConnected ? 'bg-neuro-success' : 'bg-severity-critical')} />
                <span className="text-xs text-neuro-text-secondary">Tor</span>
            </div>

            {/* Spacer */}
            <div className="flex-1" />

            {/* System Health */}
            {systemHealth && (
                <div className="flex items-center gap-4 text-xs text-neuro-text-secondary">
                    <div className="flex items-center gap-2">
                        <Activity className="w-4 h-4" />
                        <span>CPU: {systemHealth.cpu.toFixed(1)}%</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <Activity className="w-4 h-4" />
                        <span>MEM: {systemHealth.memory.toFixed(1)}%</span>
                    </div>
                </div>
            )}

            {/* Auto-save Indicator */}
            <div className="flex items-center gap-2 text-xs text-neuro-text-muted">
                <Save className="w-4 h-4" />
                <span>Auto-saved</span>
            </div>
        </header>
    );
}
