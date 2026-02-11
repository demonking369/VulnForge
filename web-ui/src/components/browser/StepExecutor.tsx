'use client';

import { Play, Pause, SkipForward, AlertCircle } from 'lucide-react';

interface StepExecutorProps {
    steps: any[];
    currentStep: number;
    status: 'idle' | 'running' | 'paused' | 'error';
    onPlay: () => void;
    onPause: () => void;
    onStep: () => void;
}

export function StepExecutor({ steps, currentStep, status, onPlay, onPause, onStep }: StepExecutorProps) {
    return (
        <div className="bg-neuro-surface border border-neuro-border rounded-lg overflow-hidden flex flex-col h-full">
            <div className="p-3 border-b border-neuro-border flex items-center justify-between">
                <h3 className="text-sm font-medium text-neuro-text-primary">Execution Queue</h3>
                <div className="flex items-center gap-1">
                    <button
                        onClick={status === 'running' ? onPause : onPlay}
                        className="p-1.5 hover:bg-neuro-bg rounded text-neuro-text-primary transition-colors"
                    >
                        {status === 'running' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                    </button>
                    <button
                        onClick={onStep}
                        disabled={status === 'running'}
                        className="p-1.5 hover:bg-neuro-bg rounded text-neuro-text-primary transition-colors disabled:opacity-50"
                    >
                        <SkipForward className="w-4 h-4" />
                    </button>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-3 space-y-2">
                {steps.length > 0 ? (
                    steps.map((step, i) => (
                        <div
                            key={i}
                            className={`p-2 rounded text-sm border flex items-center gap-3 ${i === currentStep
                                    ? 'bg-neuro-primary/10 border-neuro-primary/30 text-neuro-text-primary'
                                    : i < currentStep
                                        ? 'bg-neuro-bg/50 border-transparent text-neuro-text-muted opacity-50'
                                        : 'bg-neuro-surface border-transparent text-neuro-text-secondary'
                                }`}
                        >
                            <div className={`w-1.5 h-1.5 rounded-full ${i === currentStep ? 'bg-neuro-primary animate-pulse' :
                                    i < currentStep ? 'bg-green-500' :
                                        'bg-neuro-border'
                                }`} />
                            <span className="flex-1 truncate">{step.description || step.action}</span>
                        </div>
                    ))
                ) : (
                    <div className="flex flex-col items-center justify-center h-full text-neuro-text-muted text-xs text-center p-4">
                        <AlertCircle className="w-6 h-6 mb-2 opacity-50" />
                        No steps queued
                    </div>
                )}
            </div>
        </div>
    );
}
