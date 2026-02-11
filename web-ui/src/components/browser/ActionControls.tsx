'use client';

import { MousePointer, Type, Search, ArrowRight, Camera, Download } from 'lucide-react';

interface ActionControlsProps {
    onAction: (action: string, params: any) => void;
    disabled?: boolean;
}

export function ActionControls({ onAction, disabled }: ActionControlsProps) {
    return (
        <div className="grid grid-cols-2 gap-3">
            <button
                disabled={disabled}
                onClick={() => onAction('click', { selector: '' })}
                className="p-3 bg-neuro-surface hover:bg-neuro-bg border border-neuro-border rounded-lg flex flex-col items-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
            >
                <MousePointer className="w-5 h-5 text-neuro-text-secondary group-hover:text-neuro-primary" />
                <span className="text-xs font-medium text-neuro-text-secondary">Click</span>
            </button>

            <button
                disabled={disabled}
                onClick={() => onAction('type', { text: '' })}
                className="p-3 bg-neuro-surface hover:bg-neuro-bg border border-neuro-border rounded-lg flex flex-col items-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
            >
                <Type className="w-5 h-5 text-neuro-text-secondary group-hover:text-neuro-primary" />
                <span className="text-xs font-medium text-neuro-text-secondary">Type</span>
            </button>

            <button
                disabled={disabled}
                onClick={() => onAction('navigate', { url: '' })}
                className="p-3 bg-neuro-surface hover:bg-neuro-bg border border-neuro-border rounded-lg flex flex-col items-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
            >
                <ArrowRight className="w-5 h-5 text-neuro-text-secondary group-hover:text-neuro-primary" />
                <span className="text-xs font-medium text-neuro-text-secondary">Navigate</span>
            </button>

            <button
                disabled={disabled}
                onClick={() => onAction('screenshot', {})}
                className="p-3 bg-neuro-surface hover:bg-neuro-bg border border-neuro-border rounded-lg flex flex-col items-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
            >
                <Camera className="w-5 h-5 text-neuro-text-secondary group-hover:text-neuro-primary" />
                <span className="text-xs font-medium text-neuro-text-secondary">Snapshot</span>
            </button>

            <button
                disabled={disabled}
                onClick={() => onAction('extract', { selector: '' })}
                className="col-span-2 p-3 bg-neuro-surface hover:bg-neuro-bg border border-neuro-border rounded-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
            >
                <Search className="w-4 h-4 text-neuro-text-secondary group-hover:text-neuro-primary" />
                <span className="text-sm font-medium text-neuro-text-secondary">Extract Element Data</span>
            </button>
        </div>
    );
}
