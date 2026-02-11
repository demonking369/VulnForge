'use client';

import { Workflow } from 'lucide-react';

export function IntentFlowPanel() {
    return (
        <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-neuro-text-muted">
                <Workflow className="w-4 h-4 text-violet-300" />
                Intent Flow
            </div>
            <div className="text-xs text-neuro-text-secondary p-4 rounded-xl bg-neuro-bg/60 border border-neuro-border/40 text-center">
                Submit an intent to visualize the negotiation flow.
            </div>
        </div>
    );
}
