'use client';

import { AgentStatus } from '@/lib/types';
import { Microscope, AlertTriangle, FileText, BarChart3 } from 'lucide-react';

interface AnalystViewProps {
    status: AgentStatus;
}

export function AnalystView({ status }: AnalystViewProps) {
    return (
        <div className="space-y-4">
            <div className="grid grid-cols-3 gap-3">
                <div className="p-3 bg-severity-critical/10 border border-severity-critical/30 rounded-lg text-center">
                    <div className="text-2xl font-bold text-severity-critical">2</div>
                    <div className="text-xs text-severity-critical/80 mt-1">Critical</div>
                </div>
                <div className="p-3 bg-severity-high/10 border border-severity-high/30 rounded-lg text-center">
                    <div className="text-2xl font-bold text-severity-high">5</div>
                    <div className="text-xs text-severity-high/80 mt-1">High</div>
                </div>
                <div className="p-3 bg-severity-medium/10 border border-severity-medium/30 rounded-lg text-center">
                    <div className="text-2xl font-bold text-severity-medium">12</div>
                    <div className="text-xs text-severity-medium/80 mt-1">Medium</div>
                </div>
            </div>

            <div className="bg-neuro-surface rounded-lg border border-neuro-border p-3">
                <h4 className="text-sm font-medium text-neuro-text-primary mb-3 flex items-center gap-2">
                    <Microscope className="w-4 h-4" />
                    Analysis Stream
                </h4>
                <div className="space-y-3">
                    <div className="flex gap-3 text-sm">
                        <AlertTriangle className="w-4 h-4 text-severity-high shrink-0 mt-0.5" />
                        <div>
                            <p className="text-neuro-text-primary">SQL Injection candidates identified</p>
                            <p className="text-xs text-neuro-text-muted mt-1">Endpoint: /api/v1/users</p>
                        </div>
                    </div>
                    <div className="flex gap-3 text-sm">
                        <FileText className="w-4 h-4 text-neuro-primary shrink-0 mt-0.5" />
                        <div>
                            <p className="text-neuro-text-primary">Sensitive data exposure pattern matched</p>
                            <p className="text-xs text-neuro-text-muted mt-1">Pattern: AWS Access Key ID</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
