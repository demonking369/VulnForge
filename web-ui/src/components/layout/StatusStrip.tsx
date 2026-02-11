'use client';

import { useNeuroRift } from '@/lib/hooks';
import { Loader2, AlertCircle, CheckCircle } from 'lucide-react';

export function StatusStrip() {
    const { tasks, approvals } = useNeuroRift();

    const runningTasks = tasks.filter((t) => t.status === 'running').length;
    const pendingApprovals = approvals.filter((a) => a.status === 'pending').length;

    return (
        <footer className="h-8 bg-neuro-surface border-t border-neuro-border flex items-center px-6 gap-6 text-xs">
            {/* Running Tasks */}
            {runningTasks > 0 && (
                <div className="flex items-center gap-2 text-neuro-text-secondary">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    <span>{runningTasks} running</span>
                </div>
            )}

            {/* Pending Approvals */}
            {pendingApprovals > 0 && (
                <div className="flex items-center gap-2 px-2 py-1 bg-severity-medium/10 text-severity-medium rounded">
                    <AlertCircle className="w-3 h-3" />
                    <span>{pendingApprovals} pending approval</span>
                </div>
            )}

            {/* Idle State */}
            {runningTasks === 0 && pendingApprovals === 0 && (
                <div className="flex items-center gap-2 text-neuro-text-muted">
                    <CheckCircle className="w-3 h-3" />
                    <span>Ready</span>
                </div>
            )}

            <div className="flex-1" />

            {/* Status */}
            <div className="text-neuro-text-muted">
                <span>NeuroRift Core • Connected</span>
            </div>
        </footer>
    );
}
