'use client';

import { FileText, Brain, Download, ExternalLink } from 'lucide-react';

interface ContentViewerProps {
    title?: string;
    summary?: string;
    content: string;
    url?: string;
}

export function ContentViewer({ title, summary, content, url }: ContentViewerProps) {
    return (
        <div className="flex flex-col h-full bg-neuro-surface border border-neuro-border rounded-lg overflow-hidden">
            <div className="p-4 border-b border-neuro-border bg-neuro-bg/30">
                <h2 className="text-lg font-semibold text-neuro-text-primary mb-1">
                    {title || "No Content Selected"}
                </h2>
                {url && (
                    <a
                        href="#"
                        className="text-xs text-neuro-primary hover:underline flex items-center gap-1"
                        onClick={(e) => e.preventDefault()}
                    >
                        {url} <ExternalLink className="w-3 h-3" />
                    </a>
                )}
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {summary && (
                    <div className="bg-purple-500/5 border border-purple-500/20 rounded-lg p-4">
                        <h3 className="text-sm font-medium text-purple-400 mb-2 flex items-center gap-2">
                            <Brain className="w-4 h-4" />
                            AI Summary
                        </h3>
                        <p className="text-sm text-neuro-text-primary leading-relaxed">
                            {summary}
                        </p>
                    </div>
                )}

                <div>
                    <h3 className="text-sm font-medium text-neuro-text-secondary mb-2 flex items-center gap-2">
                        <FileText className="w-4 h-4" />
                        Raw Content
                    </h3>
                    <div className="bg-neuro-bg rounded border border-neuro-border p-4 font-mono text-xs text-neuro-text-muted overflow-x-auto whitespace-pre-wrap">
                        {content || "Select a result to view content..."}
                    </div>
                </div>
            </div>

            <div className="p-3 border-t border-neuro-border bg-neuro-bg/30 flex justify-end gap-2">
                <button className="px-3 py-1.5 text-xs bg-neuro-surface hover:bg-neuro-bg border border-neuro-border rounded text-neuro-text-primary transition-colors flex items-center gap-2">
                    <Download className="w-3 h-3" />
                    Export Data
                </button>
            </div>
        </div>
    );
}
