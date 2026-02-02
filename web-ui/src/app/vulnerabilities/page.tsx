'use client';

import { useNeuroRift } from '@/lib/hooks';
import { AlertTriangle } from 'lucide-react';
import { getSeverityColor } from '@/lib/utils';

export default function VulnerabilitiesPage() {
    const { session } = useNeuroRift();

    return (
        <div className="p-6 space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-neuro-text-primary">Vulnerabilities</h1>
                <p className="text-neuro-text-secondary mt-1">Security findings and vulnerabilities discovered</p>
            </div>

            <div className="glass-card p-6">
                {session && session.findings.length > 0 ? (
                    <div className="space-y-3">
                        {session.findings.map((finding) => (
                            <div key={finding.id} className="p-4 bg-neuro-bg rounded-lg border border-neuro-border hover:border-neuro-primary/50 transition-colors cursor-pointer">
                                <div className="flex items-start justify-between">
                                    <div className="flex items-start gap-3">
                                        <AlertTriangle className={`w-5 h-5 mt-1 ${getSeverityColor(finding.severity)}`} />
                                        <div>
                                            <h3 className="font-medium text-neuro-text-primary">{finding.title}</h3>
                                            <p className="text-sm text-neuro-text-secondary mt-1">{finding.description}</p>
                                            <div className="flex items-center gap-3 mt-2 text-xs text-neuro-text-muted">
                                                <span>Tool: {finding.tool_source}</span>
                                                <span>•</span>
                                                <span>{new Date(finding.discovered_at).toLocaleString()}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <span className={`px-2 py-1 rounded text-xs font-medium ${getSeverityColor(finding.severity)}`}>
                                        {finding.severity}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-12">
                        <AlertTriangle className="w-16 h-16 text-neuro-text-muted mx-auto mb-4" />
                        <p className="text-neuro-text-secondary">No vulnerabilities found yet</p>
                        <p className="text-sm text-neuro-text-muted mt-1">Run security scans to discover vulnerabilities</p>
                    </div>
                )}
            </div>
        </div>
    );
}
