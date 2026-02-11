'use client';

import { SessionState } from '@/lib/types';
import { Folder, Clock, Activity, Trash2, Download } from 'lucide-react';
import { formatDate, cn } from '@/lib/utils';

interface SessionCardProps {
    session: SessionState;
    onLoad: (id: string) => void;
    onDelete: (id: string) => void;
    onExport: (id: string) => void;
    isActive?: boolean;
}

export function SessionCard({ session, onLoad, onDelete, onExport, isActive }: SessionCardProps) {
    return (
        <div
            className={cn(
                'p-4 bg-neuro-bg rounded-lg border transition-all cursor-pointer hover:border-neuro-primary/50',
                isActive ? 'border-neuro-primary' : 'border-neuro-border'
            )}
            onClick={() => onLoad(session.id)}
        >
            <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 flex-1">
                    <div className={cn(
                        'w-10 h-10 rounded-lg flex items-center justify-center',
                        isActive ? 'bg-neuro-primary/20' : 'bg-neuro-surface'
                    )}>
                        <Folder className={cn(
                            'w-5 h-5',
                            isActive ? 'text-neuro-primary' : 'text-neuro-text-muted'
                        )} />
                    </div>

                    <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-neuro-text-primary truncate">
                            {session.name}
                        </h3>

                        <div className="flex items-center gap-3 mt-1 text-xs text-neuro-text-muted">
                            <span className="capitalize">{session.mode.toLowerCase()}</span>
                            <span>•</span>
                            <span className="capitalize">{session.status}</span>
                        </div>

                        <div className="flex items-center gap-4 mt-2 text-xs text-neuro-text-secondary">
                            <div className="flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {formatDate(session.updated_at)}
                            </div>
                            <div className="flex items-center gap-1">
                                <Activity className="w-3 h-3" />
                                {session.findings.length} findings
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-2 ml-4" onClick={(e) => e.stopPropagation()}>
                    <button
                        onClick={() => onExport(session.id)}
                        className="p-2 hover:bg-neuro-surface rounded transition-colors"
                        title="Export session"
                    >
                        <Download className="w-4 h-4 text-neuro-text-muted hover:text-neuro-primary" />
                    </button>
                    <button
                        onClick={() => onDelete(session.id)}
                        className="p-2 hover:bg-neuro-surface rounded transition-colors"
                        title="Delete session"
                    >
                        <Trash2 className="w-4 h-4 text-neuro-text-muted hover:text-severity-critical" />
                    </button>
                </div>
            </div>

            {session.metadata.description && (
                <p className="mt-3 text-sm text-neuro-text-secondary line-clamp-2">
                    {session.metadata.description}
                </p>
            )}
        </div>
    );
}
