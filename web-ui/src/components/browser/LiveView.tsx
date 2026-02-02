'use client';

import { useState } from 'react';
import { Camera, RefreshCw, Smartphone, Monitor } from 'lucide-react';
import Image from 'next/image';

interface LiveViewProps {
    url: string | null;
    screenshot?: string;
    isActive: boolean;
}

export function LiveView({ url, screenshot, isActive }: LiveViewProps) {
    const [viewport, setViewport] = useState<'desktop' | 'mobile'>('desktop');

    return (
        <div className="flex flex-col h-full bg-neuro-surface border border-neuro-border rounded-lg overflow-hidden">
            {/* Browser Toolbar */}
            <div className="flex items-center gap-2 p-2 border-b border-neuro-border bg-neuro-bg/50">
                <div className="flex gap-1.5 ml-1">
                    <div className="w-2.5 h-2.5 rounded-full bg-red-500/50" />
                    <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/50" />
                    <div className="w-2.5 h-2.5 rounded-full bg-green-500/50" />
                </div>

                <div className="flex-1 flex items-center gap-2 px-3 py-1.5 bg-neuro-bg rounded text-xs text-neuro-text-secondary border border-neuro-border/30">
                    <span className="truncate flex-1">{url || 'No active session'}</span>
                    <RefreshCw className="w-3 h-3 cursor-pointer hover:text-neuro-primary" />
                </div>

                <div className="flex items-center gap-1 border-l border-neuro-border pl-2">
                    <button
                        onClick={() => setViewport('desktop')}
                        className={`p-1.5 rounded hover:bg-neuro-bg transition-colors ${viewport === 'desktop' ? 'text-neuro-primary bg-neuro-bg' : 'text-neuro-text-muted'
                            }`}
                    >
                        <Monitor className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => setViewport('mobile')}
                        className={`p-1.5 rounded hover:bg-neuro-bg transition-colors ${viewport === 'mobile' ? 'text-neuro-primary bg-neuro-bg' : 'text-neuro-text-muted'
                            }`}
                    >
                        <Smartphone className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* Viewport */}
            <div className="flex-1 relative bg-neuro-bg flex items-center justify-center p-4">
                {isActive ? (
                    screenshot ? (
                        <div className={`relative ${viewport === 'mobile' ? 'w-[375px]' : 'w-full'} h-full transition-all duration-300`}>
                            <img
                                src={screenshot}
                                alt="Browser View"
                                className="w-full h-full object-contain border border-neuro-border shadow-2xl"
                            />
                        </div>
                    ) : (
                        <div className="flex flex-col items-center gap-3 text-neuro-text-muted animate-pulse">
                            <Camera className="w-8 h-8 opacity-50" />
                            <span className="text-sm">Waiting for frame...</span>
                        </div>
                    )
                ) : (
                    <div className="flex flex-col items-center gap-3 text-neuro-text-muted">
                        <div className="w-16 h-16 rounded-full bg-neuro-surface border border-neuro-border flex items-center justify-center">
                            <Monitor className="w-8 h-8 opacity-20" />
                        </div>
                        <p>Browser session not active</p>
                    </div>
                )}
            </div>
        </div>
    );
}
