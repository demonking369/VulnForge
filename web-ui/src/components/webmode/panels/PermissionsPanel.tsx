'use client';

<<<<<<< HEAD
import { useState } from 'react';
import { ShieldCheck, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import { useWebModeContext } from '@/components/webmode/WebModeProvider';
import { cn } from '@/lib/utils';

const MOCK_PERMISSIONS = [
    {
        id: 'perm-1', title: 'Scope Expansion: External DNS', description: 'Agent requests access to external DNS resolution for reconnaissance.',
        riskLevel: 'medium' as const, origin: 'operator', status: 'pending' as const, stage: 1, totalStages: 2,
        policyDelta: '+DNS:external.resolve → operator.network',
    },
    {
        id: 'perm-2', title: 'Config Mutation: Sandbox Level', description: 'Self-evolution engine proposes sandbox relaxation for model fine-tuning.',
        riskLevel: 'high' as const, origin: 'evolution-engine', status: 'pending' as const, stage: 1, totalStages: 3,
        policyDelta: 'neurorift.sandboxLevel: hardened → strict',
    },
];

const RISK_COLORS: Record<string, string> = {
    low: 'text-emerald-400 border-emerald-500/30',
    medium: 'text-amber-400 border-amber-500/30',
    high: 'text-rose-400 border-rose-500/30',
    critical: 'text-red-500 border-red-500/50',
};

export function PermissionsPanel() {
    const { resolvePermission, permissionQueue } = useWebModeContext();
    const [enforcementFlash, setEnforcementFlash] = useState<string | null>(null);

    const displayPerms = permissionQueue.length > 0 ? permissionQueue : MOCK_PERMISSIONS;

    const handleAction = (id: string, approved: boolean) => {
        setEnforcementFlash(id);
        setTimeout(() => {
            resolvePermission(id, approved);
            setEnforcementFlash(null);
        }, 600);
    };

    return (
        <div className="space-y-4">
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-neuro-text-muted">
                <ShieldCheck className="w-4 h-4 text-rose-300" />
                Permission Decisions
                {displayPerms.length > 0 && (
                    <span className="ml-auto px-2 py-0.5 bg-rose-950/30 border border-rose-500/30 rounded text-[10px] text-rose-300">{displayPerms.length} pending</span>
                )}
            </div>

            <div className="space-y-3">
                {displayPerms.map(req => (
                    <div key={req.id} className={cn("rounded-xl border bg-neuro-bg/60 p-4 transition-all relative overflow-hidden", RISK_COLORS[req.riskLevel] || RISK_COLORS.low, enforcementFlash === req.id && "ring-2 ring-cyan-400/50")}>
                        {enforcementFlash === req.id && (
                            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/5 to-transparent animate-pulse" />
                        )}
                        <div className="flex items-start justify-between mb-2">
                            <div>
                                <h5 className="text-sm text-neuro-text-primary font-medium">{req.title}</h5>
                                <p className="text-[10px] text-neuro-text-muted mt-0.5">{req.description}</p>
                            </div>
                            <span className={cn("text-[9px] uppercase tracking-wider px-2 py-0.5 rounded border", RISK_COLORS[req.riskLevel])}>{req.riskLevel}</span>
                        </div>

                        {/* Risk Vectors */}
                        <div className="mt-3 p-2 rounded bg-black/30 border border-neuro-border/20 space-y-1">
                            <div className="text-[9px] uppercase tracking-wider text-neuro-text-muted">Risk Vectors</div>
                            <div className="flex flex-wrap gap-2 text-[10px]">
                                <span className="px-1.5 py-0.5 bg-amber-950/30 border border-amber-500/20 rounded text-amber-200">Scope Expansion</span>
                                <span className="px-1.5 py-0.5 bg-violet-950/30 border border-violet-500/20 rounded text-violet-200">Config Mutation</span>
                            </div>
                        </div>

                        {/* Policy Delta */}
                        {req.policyDelta && (
                            <div className="mt-2 p-2 rounded bg-black/20 border border-neuro-border/20 font-mono text-[10px] text-cyan-300">{req.policyDelta}</div>
                        )}

                        {/* Stage + Actions */}
                        <div className="flex items-center justify-between mt-3">
                            <div className="flex gap-1">
                                {Array.from({ length: req.totalStages }).map((_, i) => (
                                    <div key={i} className={cn("w-4 h-1 rounded-full", i < req.stage ? "bg-cyan-400" : "bg-neuro-border/40")} />
                                ))}
                                <span className="text-[9px] text-neuro-text-muted ml-1.5">{req.stage}/{req.totalStages}</span>
                            </div>
                            <div className="flex gap-2">
                                <button onClick={() => handleAction(req.id, true)} className="group/btn flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-950/30 border border-emerald-500/30 hover:bg-emerald-900/40 transition-all">
                                    <span className="text-[10px] uppercase tracking-wider text-emerald-200">Approve</span>
                                    <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
                                </button>
                                <button onClick={() => handleAction(req.id, false)} className="group/btn flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-950/30 border border-rose-500/30 hover:bg-rose-900/40 transition-all">
                                    <span className="text-[10px] uppercase tracking-wider text-rose-200">Reject</span>
                                    <XCircle className="w-3.5 h-3.5 text-rose-400" />
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
=======
import { useNeuroRift } from '@/lib/hooks';
import { cn } from '@/lib/utils';

export function PermissionsPanel() {
    const { approvals } = useNeuroRift();

    return (
        <div className="space-y-3">
            {approvals.map(approval => (
                <div key={approval.id} className="rounded-xl border border-neuro-border/60 bg-neuro-bg/70 p-4">
                    <div className="flex items-center justify-between text-xs uppercase tracking-[0.3em] text-neuro-text-muted">
                        <span>{approval.status}</span>
                        <span className={cn(
                            approval.risk === 'high' && 'text-rose-200',
                            approval.risk === 'medium' && 'text-amber-200',
                            approval.risk === 'low' && 'text-emerald-200'
                        )}>
                            {approval.risk} risk
                        </span>
                    </div>
                    <p className="mt-2 text-sm text-neuro-text-primary">{approval.label}</p>
                    <div className="mt-3 flex items-center gap-2 text-[10px] uppercase tracking-[0.3em] text-neuro-text-muted">
                        <span className="px-2 py-1 rounded-full bg-neuro-surface/70 border border-neuro-border/60">Approve</span>
                        <span className="px-2 py-1 rounded-full bg-neuro-surface/70 border border-neuro-border/60">Reject</span>
                    </div>
                </div>
            ))}
>>>>>>> main
        </div>
    );
}
