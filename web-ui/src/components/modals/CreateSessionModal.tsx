'use client';

import { useState } from 'react';
import { X, AlertCircle } from 'lucide-react';
import { OperationalMode } from '@/lib/types';

interface CreateSessionModalProps {
    isOpen: boolean;
    onClose: () => void;
    onCreate: (name: string, mode: OperationalMode, description?: string) => void;
}

export function CreateSessionModal({ isOpen, onClose, onCreate }: CreateSessionModalProps) {
    const [name, setName] = useState('');
    const [mode, setMode] = useState<OperationalMode>('OFFENSIVE');
    const [description, setDescription] = useState('');
    const [error, setError] = useState('');

    if (!isOpen) return null;

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!name.trim()) {
            setError('Session name is required');
            return;
        }

        onCreate(name.trim(), mode, description.trim() || undefined);

        // Reset form
        setName('');
        setMode('OFFENSIVE');
        setDescription('');
        setError('');
        onClose();
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="glass-card p-6 w-full max-w-md mx-4">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-semibold text-neuro-text-primary">Create New Session</h2>
                    <button
                        onClick={onClose}
                        className="p-1 hover:bg-neuro-surface rounded transition-colors"
                    >
                        <X className="w-5 h-5 text-neuro-text-muted" />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    {error && (
                        <div className="p-3 bg-severity-critical/10 border border-severity-critical/30 rounded-lg flex items-center gap-2">
                            <AlertCircle className="w-4 h-4 text-severity-critical" />
                            <span className="text-sm text-severity-critical">{error}</span>
                        </div>
                    )}

                    <div>
                        <label className="block text-sm font-medium text-neuro-text-secondary mb-2">
                            Session Name *
                        </label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="e.g., Acme Corp Assessment"
                            className="w-full px-3 py-2 bg-neuro-surface border border-neuro-border rounded-lg text-neuro-text-primary placeholder-neuro-text-muted focus:outline-none focus:border-neuro-primary"
                            autoFocus
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-neuro-text-secondary mb-2">
                            Operational Mode *
                        </label>
                        <div className="grid grid-cols-2 gap-3">
                            <button
                                type="button"
                                onClick={() => setMode('OFFENSIVE')}
                                className={`p-3 rounded-lg border transition-all ${mode === 'OFFENSIVE'
                                        ? 'bg-severity-critical/20 border-severity-critical text-severity-critical'
                                        : 'bg-neuro-surface border-neuro-border text-neuro-text-secondary hover:border-neuro-primary/50'
                                    }`}
                            >
                                <div className="font-medium">Offensive</div>
                                <div className="text-xs mt-1 opacity-80">Active testing</div>
                            </button>
                            <button
                                type="button"
                                onClick={() => setMode('DEFENSIVE')}
                                className={`p-3 rounded-lg border transition-all ${mode === 'DEFENSIVE'
                                        ? 'bg-neuro-primary/20 border-neuro-primary text-neuro-primary'
                                        : 'bg-neuro-surface border-neuro-border text-neuro-text-secondary hover:border-neuro-primary/50'
                                    }`}
                            >
                                <div className="font-medium">Defensive</div>
                                <div className="text-xs mt-1 opacity-80">Passive recon</div>
                            </button>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-neuro-text-secondary mb-2">
                            Description (Optional)
                        </label>
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="Brief description of this assessment..."
                            rows={3}
                            className="w-full px-3 py-2 bg-neuro-surface border border-neuro-border rounded-lg text-neuro-text-primary placeholder-neuro-text-muted focus:outline-none focus:border-neuro-primary resize-none"
                        />
                    </div>

                    <div className="flex items-center gap-3 pt-4">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 px-4 py-2 bg-neuro-surface border border-neuro-border rounded-lg text-neuro-text-secondary hover:bg-neuro-bg transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="flex-1 btn-primary"
                        >
                            Create Session
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
