'use client';

import { useNeuroRift } from '@/lib/hooks';
import { Activity, Shield, AlertTriangle, FileText } from 'lucide-react';
import { cn, getSeverityColor } from '@/lib/utils';

export default function DashboardPage() {
    const { session, agents, tasks, approvals } = useNeuroRift();

    if (!session) {
        return (
            <div className="h-full flex items-center justify-center">
                <div className="text-center">
                    <Shield className="w-16 h-16 text-neuro-text-muted mx-auto mb-4" />
                    <h2 className="text-2xl font-bold text-neuro-text-primary mb-2">No Active Session</h2>
                    <p className="text-neuro-text-secondary">Create or load a session to get started</p>
                </div>
            </div>
        );
    }

    const findingsBySeverity = session.findings.reduce((acc, finding) => {
        acc[finding.severity] = (acc[finding.severity] || 0) + 1;
        return acc;
    }, {} as Record<string, number>);

    return (
        <div className="p-6 space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-neuro-text-primary">Dashboard</h1>
                <p className="text-neuro-text-secondary mt-1">Overview of {session.name}</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-4 gap-4">
                <StatsCard
                    icon={Shield}
                    label="Total Findings"
                    value={session.findings.length}
                    color="text-neuro-primary"
                />
                <StatsCard
                    icon={Activity}
                    label="Active Tasks"
                    value={tasks.filter((t) => t.status === 'running').length}
                    color="text-neuro-success"
                />
                <StatsCard
                    icon={AlertTriangle}
                    label="Pending Approvals"
                    value={approvals.filter((a) => a.status === 'pending').length}
                    color="text-severity-medium"
                />
                <StatsCard
                    icon={FileText}
                    label="Artifacts"
                    value={session.artifacts.length}
                    color="text-neuro-text-secondary"
                />
            </div>

            {/* Severity Breakdown */}
            <div className="glass-card p-6">
                <h2 className="text-xl font-semibold text-neuro-text-primary mb-4">Findings by Severity</h2>
                <div className="space-y-3">
                    {(['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'] as const).map((severity) => {
                        const count = findingsBySeverity[severity] || 0;
                        const total = session.findings.length || 1;
                        const percentage = (count / total) * 100;

                        return (
                            <div key={severity}>
                                <div className="flex items-center justify-between mb-1">
                                    <span className={cn('text-sm font-medium', getSeverityColor(severity))}>
                                        {severity}
                                    </span>
                                    <span className="text-sm text-neuro-text-muted">{count}</span>
                                </div>
                                <div className="h-2 bg-neuro-bg rounded-full overflow-hidden">
                                    <div
                                        className={cn('h-full transition-all', getSeverityColor(severity).replace('text-', 'bg-'))}
                                        style={{ width: `${percentage}%` }}
                                    />
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Agent Status */}
            <div className="glass-card p-6">
                <h2 className="text-xl font-semibold text-neuro-text-primary mb-4">Agent Status</h2>
                <div className="grid grid-cols-5 gap-4">
                    {Object.entries(agents).map(([agentType, status]) => (
                        <div key={agentType} className="text-center">
                            <div className={cn(
                                'w-12 h-12 rounded-full mx-auto mb-2 flex items-center justify-center',
                                status.state === 'idle' ? 'bg-neuro-bg' :
                                    status.state === 'error' ? 'bg-severity-critical/20' :
                                        'bg-neuro-primary/20'
                            )}>
                                <Activity className={cn(
                                    'w-6 h-6',
                                    status.state === 'idle' ? 'text-neuro-text-muted' :
                                        status.state === 'error' ? 'text-severity-critical' :
                                            'text-neuro-primary'
                                )} />
                            </div>
                            <p className="text-sm font-medium text-neuro-text-primary">{agentType}</p>
                            <p className="text-xs text-neuro-text-muted capitalize">{status.state}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

function StatsCard({
    icon: Icon,
    label,
    value,
    color,
}: {
    icon: any;
    label: string;
    value: number;
    color: string;
}) {
    return (
        <div className="glass-card p-4">
            <div className="flex items-center gap-3">
                <div className={cn('p-2 rounded-lg bg-neuro-bg', color)}>
                    <Icon className="w-6 h-6" />
                </div>
                <div>
                    <p className="text-2xl font-bold text-neuro-text-primary">{value}</p>
                    <p className="text-sm text-neuro-text-secondary">{label}</p>
                </div>
            </div>
        </div>
    );
}
