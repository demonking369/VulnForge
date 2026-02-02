'use client';

import { AgentStatus } from '@/lib/types';
import { Globe, MousePointer, Search, Camera } from 'lucide-react';

interface NavigatorViewProps {
    status: AgentStatus;
}

export function NavigatorView({ status }: NavigatorViewProps) {
    return (
        <div className="space-y-4">
            <div className="aspect-video bg-neuro-bg relative rounded-lg border border-neuro-border overflow-hidden group">
                {/* Mock Browser UI */}
                <div className="absolute top-0 left-0 right-0 h-8 bg-neuro-surface border-b border-neuro-border flex items-center px-3 gap-2">
                    <div className="flex gap-1.5">
                        <div className="w-2.5 h-2.5 rounded-full bg-red-500/50" />
                        <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/50" />
                        <div className="w-2.5 h-2.5 rounded-full bg-green-500/50" />
                    </div>
                    <div className="flex-1 bg-neuro-bg h-5 rounded flex items-center px-2 text-xs text-neuro-text-muted truncate">
                        https://target-site.com/login
                    </div>
                </div>

                {/* Placeholder Content */}
                <div className="mt-8 p-4 flex flex-col items-center justify-center h-[calc(100%-2rem)] text-neuro-text-muted">
                    <div className="w-12 h-12 rounded-full bg-neuro-surface flex items-center justify-center mb-3">
                        <Camera className="w-6 h-6 opacity-50" />
                    </div>
                    <p className="text-sm">Live preview active</p>
                </div>

                {/* Action Overlay */}
                <div className="absolute bottom-4 right-4 bg-black/80 backdrop-blur text-white text-xs px-3 py-1.5 rounded-full flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                    Interacting with DOM
                </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
                <button className="p-2 bg-neuro-surface hover:bg-neuro-bg border border-neuro-border rounded flex items-center justify-center gap-2 text-sm text-neuro-text-secondary transition-colors">
                    <MousePointer className="w-4 h-4" />
                    Click Element
                </button>
                <button className="p-2 bg-neuro-surface hover:bg-neuro-bg border border-neuro-border rounded flex items-center justify-center gap-2 text-sm text-neuro-text-secondary transition-colors">
                    <Search className="w-4 h-4" />
                    Inspect DOM
                </button>
            </div>
        </div>
    );
}
