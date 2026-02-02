'use client';

import { AgentStatus } from '@/lib/types';
import { FileEdit, CheckCircle2, History } from 'lucide-react';

interface ScribeViewProps {
    status: AgentStatus;
}

export function ScribeView({ status }: ScribeViewProps) {
    return (
        <div className="space-y-4">
            <div className="bg-neuro-surface rounded-lg border border-neuro-border p-4">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-medium text-neuro-text-primary flex items-center gap-2">
                        <FileEdit className="w-4 h-4" />
                        Live Report
                    </h3>
                    <span className="text-xs text-green-400 flex items-center gap-1">
                        <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                        Auto-saving
                    </span>
                </div>

                <div className="space-y-2 text-sm text-neuro-text-muted font-mono bg-neuro-bg p-3 rounded border border-neuro-border/50">
                    <p>## Executive Summary</p>
                    <p>During the assessment of target 10.10.11.24, several critical vulnerabilities were identified...</p>
                    <p className="opacity-50">...</p>
                    <p>### Finding: SQL Injection on Login</p>
                    <p><span className="text-blue-400">writing...</span></p>
                </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-neuro-surface rounded-lg border border-neuro-border">
                    <div className="text-xs text-neuro-text-secondary mb-1">Sections Completed</div>
                    <div className="text-xl font-bold text-neuro-text-primary">3/7</div>
                </div>
                <div className="p-3 bg-neuro-surface rounded-lg border border-neuro-border">
                    <div className="text-xs text-neuro-text-secondary mb-1">Evidence Collected</div>
                    <div className="text-xl font-bold text-neuro-text-primary">14</div>
                </div>
            </div>
        </div>
    );
}
