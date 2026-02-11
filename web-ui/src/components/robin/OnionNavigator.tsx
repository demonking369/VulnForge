'use client';

import { useState } from 'react';
import { Search, Globe, RotateCw } from 'lucide-react';

interface OnionNavigatorProps {
    onNavigate: (url: string) => void;
    isLoading: boolean;
}

export function OnionNavigator({ onNavigate, isLoading }: OnionNavigatorProps) {
    const [url, setUrl] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (url) onNavigate(url);
    };

    return (
        <div className="bg-neuro-surface border border-neuro-border rounded-lg p-4">
            <form onSubmit={handleSubmit} className="flex gap-2">
                <div className="flex-1 relative">
                    <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neuro-text-muted" />
                    <input
                        type="text"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="Enter .onion URL or search query..."
                        className="w-full bg-neuro-bg border border-neuro-border rounded-md py-2 pl-9 pr-4 text-sm text-neuro-text-primary focus:outline-none focus:ring-1 focus:ring-neuro-primary placeholder:text-neuro-text-muted"
                    />
                </div>
                <button
                    type="button"
                    className="p-2 bg-neuro-bg border border-neuro-border rounded-md text-neuro-text-secondary hover:text-neuro-primary transition-colors"
                    onClick={() => { }}
                    title="New Identity"
                >
                    <RotateCw className="w-4 h-4" />
                </button>
                <button
                    type="submit"
                    disabled={isLoading || !url}
                    className="px-4 bg-neuro-primary/20 text-neuro-primary border border-neuro-primary/50 hover:bg-neuro-primary/30 rounded-md text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                    {isLoading ? 'Loading...' : (
                        <>
                            <Search className="w-4 h-4" />
                            Navigate
                        </>
                    )}
                </button>
            </form>

            <div className="mt-3 flex gap-2 overflow-x-auto pb-2 scrollbar-thin">
                {['Hidden Wiki', 'Torch', 'Ahmia', 'Dread'].map((bookmark) => (
                    <button
                        key={bookmark}
                        type="button"
                        onClick={() => setUrl(`http://${bookmark.toLowerCase()}.onion`)}
                        className="px-3 py-1 bg-neuro-bg/50 border border-neuro-border rounded text-xs text-neuro-text-secondary hover:text-neuro-primary hover:border-neuro-primary/50 transition-colors whitespace-nowrap"
                    >
                        {bookmark}
                    </button>
                ))}
            </div>
        </div>
    );
}
